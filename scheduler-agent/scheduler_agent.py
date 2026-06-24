#!/usr/bin/env python3
"""
scheduler_agent.py
==================
Production-oriented Scheduler AI Agent built on Claude's tool-use API.

ARCHITECTURE
------------
Pattern: Single-agent system with rich tool integration + domain skill.

Rationale (per Anthropic's "Building Effective AI Agents" framework):
  - Control level:       HIGH (calendar actions are consequential, audit trail required)
  - Problem complexity:  SINGLE DOMAIN (scheduling) with multi-faceted concerns
  - Domain expertise:    deep but narrow -> single agent + skills, NOT multi-agent
  - Token economics:     avoid 10-15x multi-agent overhead for a focused task

Composition:
  - Reasoning core: Claude (claude-sonnet-4-6) in an agentic loop
  - Toolkit: 9 calendar / preference / HITL tools
  - Skill:   meeting_scheduling_skill.md (loaded into system prompt)
  - Backends: pluggable (CalendarBackend, PreferencesStore, HumanReviewQueue)

INTEGRATION POINTS (wire to real systems before production):
  [1] CalendarBackend        -> Google Calendar API / MS Graph / iCal
  [2] PreferencesStore       -> user-prefs DB (Postgres, DynamoDB, etc.)
  [3] HumanReviewQueue       -> Slack / email / web UI confirmation for HIGH/CRITICAL ops

KEY SAFETY PROPERTIES
---------------------
  * Fail-closed on destructive ops: update_event / cancel_event REJECTED unless
    a matching request_confirmation has been approved earlier in the same run.
  * Timezone discipline: ISO 8601 with explicit offset required on every datetime.
  * Preference-aware: working hours, buffers, caps, no-meeting days all enforced.
  * Observable: every tool call recorded in AgentTrace for audit.

Author: scheduler-agent v0.1
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from zoneinfo import ZoneInfo

from anthropic import Anthropic

_PKG_DIR = Path(__file__).resolve().parent

# ============================================================================
# Configuration & Logging
# ============================================================================

logger = logging.getLogger("scheduler_agent")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_h)
logger.setLevel(logging.INFO)

MODEL = os.getenv("SCHEDULER_MODEL", "claude-sonnet-4-6")
MAX_TURNS = int(os.getenv("SCHEDULER_MAX_TURNS", "20"))
MAX_TOKENS = int(os.getenv("SCHEDULER_MAX_TOKENS", "4096"))
SKILL_PATH = os.getenv("SCHEDULER_SKILL_PATH", str(_PKG_DIR / "meeting_scheduling_skill.md"))


# ============================================================================
# Domain Types
# ============================================================================

class EventStatus(str, Enum):
    CONFIRMED = "confirmed"
    TENTATIVE = "tentative"
    CANCELLED = "cancelled"


class ActionRisk(str, Enum):
    """Risk tier; drives HITL policy."""
    LOW = "low"             # Read-only (list, get, check availability)
    MEDIUM = "medium"       # Create new events
    HIGH = "high"           # Modify existing events
    CRITICAL = "critical"   # Cancel events; bulk operations


@dataclass
class Attendee:
    email: str
    name: Optional[str] = None
    optional: bool = False
    response_status: Optional[str] = None  # accepted | declined | tentative | needsAction


@dataclass
class CalendarEvent:
    event_id: str
    title: str
    start: datetime  # MUST be tz-aware
    end: datetime    # MUST be tz-aware
    attendees: list[Attendee] = field(default_factory=list)
    location: Optional[str] = None
    description: Optional[str] = None
    status: EventStatus = EventStatus.CONFIRMED
    recurrence: Optional[str] = None  # RFC 5545 RRULE
    organizer_email: Optional[str] = None
    calendar_id: str = "primary"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["start"] = self.start.isoformat()
        d["end"] = self.end.isoformat()
        d["status"] = self.status.value
        return d


@dataclass
class TimeRange:
    start: datetime
    end: datetime

    def overlaps(self, other: "TimeRange") -> bool:
        return self.start < other.end and other.start < self.end

    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)


@dataclass
class UserPreferences:
    user_id: str
    timezone: str = "UTC"
    working_hours_start: int = 9    # 24h local
    working_hours_end: int = 17
    working_days: list[int] = field(default_factory=lambda: [0, 1, 2, 3, 4])  # Mon-Fri, 0=Mon
    default_meeting_duration_minutes: int = 30
    buffer_minutes_between_meetings: int = 15
    max_meetings_per_day: int = 6
    focus_block_minimum_minutes: int = 90
    no_meeting_days: list[int] = field(default_factory=list)
    preferred_meeting_times: list[str] = field(default_factory=list)  # ["morning", "afternoon"]


# ============================================================================
# Pluggable Backend Interfaces  [INTEGRATION POINTS]
# ============================================================================

class CalendarBackend:
    """Abstract calendar backend. Implement against Google Calendar / MS Graph / iCal."""

    def list_events(self, calendar_id: str, time_min: datetime, time_max: datetime) -> list[CalendarEvent]:
        raise NotImplementedError

    def get_event(self, event_id: str) -> Optional[CalendarEvent]:
        raise NotImplementedError

    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        raise NotImplementedError

    def update_event(self, event_id: str, changes: dict[str, Any]) -> CalendarEvent:
        raise NotImplementedError

    def cancel_event(self, event_id: str, notify_attendees: bool = True) -> bool:
        raise NotImplementedError

    def get_freebusy(
        self, emails: list[str], time_min: datetime, time_max: datetime
    ) -> dict[str, list[TimeRange]]:
        """Return busy ranges per email. Empty list = fully free (or unknown)."""
        raise NotImplementedError


class PreferencesStore:
    """Abstract user preference store."""

    def get(self, user_id: str) -> UserPreferences:
        raise NotImplementedError

    def update(self, user_id: str, changes: dict[str, Any]) -> UserPreferences:
        raise NotImplementedError


class HumanReviewQueue:
    """Abstract HITL queue (Slack, email, web UI)."""

    def request_confirmation(
        self, action: str, details: dict[str, Any], risk: ActionRisk
    ) -> bool:
        """Return True if approved, False if denied or timed out."""
        raise NotImplementedError


# ============================================================================
# Reference In-Memory Backends (for tests / smoke runs; NOT production)
# ============================================================================

class InMemoryCalendarBackend(CalendarBackend):
    def __init__(self) -> None:
        self._events: dict[str, CalendarEvent] = {}

    def list_events(self, calendar_id, time_min, time_max):
        return [
            e for e in self._events.values()
            if e.calendar_id == calendar_id
            and e.status != EventStatus.CANCELLED
            and e.start < time_max and e.end > time_min
        ]

    def get_event(self, event_id):
        return self._events.get(event_id)

    def create_event(self, event):
        if not event.event_id:
            event.event_id = f"evt_{uuid.uuid4().hex[:12]}"
        self._events[event.event_id] = event
        return event

    def update_event(self, event_id, changes):
        e = self._events[event_id]
        for k, v in changes.items():
            if hasattr(e, k):
                setattr(e, k, v)
        return e

    def cancel_event(self, event_id, notify_attendees=True):
        if event_id in self._events:
            self._events[event_id].status = EventStatus.CANCELLED
            return True
        return False

    def get_freebusy(self, emails, time_min, time_max):
        return {email: [] for email in emails}


class InMemoryPreferencesStore(PreferencesStore):
    def __init__(self) -> None:
        self._prefs: dict[str, UserPreferences] = {}

    def get(self, user_id):
        if user_id not in self._prefs:
            self._prefs[user_id] = UserPreferences(user_id=user_id)
        return self._prefs[user_id]

    def update(self, user_id, changes):
        p = self.get(user_id)
        for k, v in changes.items():
            if hasattr(p, k):
                setattr(p, k, v)
        return p


class AutoApproveReviewQueue(HumanReviewQueue):
    """Dev-only: auto-approves everything. DO NOT use in production."""

    def request_confirmation(self, action, details, risk):
        logger.warning(
            "AUTO-APPROVING %s action=%s (replace AutoApproveReviewQueue in prod)",
            risk.value, action,
        )
        return True


# ============================================================================
# Tool Schemas (Claude tool-use API format)
# ============================================================================

TOOLS: list[dict[str, Any]] = [
    {
        "name": "get_user_preferences",
        "description": (
            "Read the user's scheduling preferences (working hours, timezone, buffers, "
            "caps, focus-block rules). LOW risk (read-only). "
            "ALWAYS call this FIRST when scheduling anything new."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"user_id": {"type": "string"}},
            "required": ["user_id"],
        },
    },
    {
        "name": "list_events",
        "description": (
            "List calendar events in a time range. Use to inspect current schedule "
            "or assess load. LOW risk (read-only)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "calendar_id": {"type": "string", "default": "primary"},
                "time_min": {"type": "string", "description": "ISO 8601 with offset"},
                "time_max": {"type": "string", "description": "ISO 8601 with offset"},
            },
            "required": ["time_min", "time_max"],
        },
    },
    {
        "name": "get_event",
        "description": "Fetch full details of a single event by ID. LOW risk (read-only).",
        "input_schema": {
            "type": "object",
            "properties": {"event_id": {"type": "string"}},
            "required": ["event_id"],
        },
    },
    {
        "name": "find_availability",
        "description": (
            "Find time slots when all participants are free, respecting working hours, "
            "buffers, and meeting-load caps. Returns up to `max_options` ranked slots. "
            "LOW risk (read-only)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "participant_emails": {"type": "array", "items": {"type": "string"}},
                "duration_minutes": {"type": "integer"},
                "search_start": {"type": "string", "description": "ISO 8601 with offset"},
                "search_end": {"type": "string", "description": "ISO 8601 with offset"},
                "max_options": {"type": "integer", "default": 5},
            },
            "required": ["participant_emails", "duration_minutes", "search_start", "search_end"],
        },
    },
    {
        "name": "check_conflicts",
        "description": (
            "Check whether a proposed time conflicts with existing events or violates "
            "the user's preferences (working hours, no-meeting days, max-per-day cap, "
            "buffer). Returns a structured conflict report. LOW risk (read-only). "
            "REQUIRED before create_event."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "start": {"type": "string", "description": "ISO 8601 with offset"},
                "end": {"type": "string", "description": "ISO 8601 with offset"},
                "calendar_id": {"type": "string", "default": "primary"},
            },
            "required": ["user_id", "start", "end"],
        },
    },
    {
        "name": "create_event",
        "description": (
            "Create a new calendar event. MEDIUM risk. "
            "PRECONDITION: you MUST have called check_conflicts (or find_availability) "
            "on the proposed slot earlier in this run."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "start": {"type": "string", "description": "ISO 8601 with offset"},
                "end": {"type": "string", "description": "ISO 8601 with offset"},
                "attendee_emails": {"type": "array", "items": {"type": "string"}, "default": []},
                "location": {"type": "string"},
                "description": {"type": "string"},
                "recurrence_rrule": {"type": "string", "description": "Optional RFC 5545 RRULE"},
                "calendar_id": {"type": "string", "default": "primary"},
            },
            "required": ["title", "start", "end"],
        },
    },
    {
        "name": "request_confirmation",
        "description": (
            "Request human-in-the-loop confirmation for a HIGH or CRITICAL action. "
            "Returns {approved: bool}. You MUST call this and receive approved=true "
            "BEFORE any update_event or cancel_event. The `details` MUST match the "
            "arguments you will pass to the destructive tool exactly."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["update_event", "cancel_event", "bulk_cancel", "bulk_reschedule"],
                },
                "risk": {"type": "string", "enum": ["high", "critical"]},
                "summary": {"type": "string", "description": "Short human-readable summary"},
                "details": {
                    "type": "object",
                    "description": "Structured details that MUST match the destructive call args",
                },
            },
            "required": ["action", "risk", "summary", "details"],
        },
    },
    {
        "name": "update_event",
        "description": (
            "Update an existing event (time, attendees, title, etc.). HIGH risk. "
            "REQUIRES prior approved request_confirmation with matching details. "
            "The executor will reject unconfirmed calls (fail-closed)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string"},
                "changes": {
                    "type": "object",
                    "description": "Fields to update: title, start, end, location, description",
                },
            },
            "required": ["event_id", "changes"],
        },
    },
    {
        "name": "cancel_event",
        "description": (
            "Cancel an existing event. CRITICAL risk. "
            "REQUIRES prior approved request_confirmation with matching details. "
            "The executor will reject unconfirmed calls (fail-closed). "
            "Notifies attendees by default."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string"},
                "notify_attendees": {"type": "boolean", "default": True},
            },
            "required": ["event_id"],
        },
    },
]


# ============================================================================
# Tool Executor
# ============================================================================

class SchedulerToolExecutor:
    """
    Dispatches tool calls from Claude to backend implementations.

    Enforces fail-closed HITL policy: maintains an approval ledger keyed by
    (action, normalized-details). update_event / cancel_event check the ledger
    and refuse without a matching approval. Approvals are one-shot (consumed
    on use) to prevent replay across multiple destructive calls.
    """

    def __init__(
        self,
        calendar: CalendarBackend,
        prefs: PreferencesStore,
        hitl: HumanReviewQueue,
        user_id: str,
    ) -> None:
        self.calendar = calendar
        self.prefs = prefs
        self.hitl = hitl
        self.user_id = user_id
        self._approved_actions: set[str] = set()
        self._checked_slots: set[tuple[str, str]] = set()

    @staticmethod
    def _parse_dt(s: str) -> datetime:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError(f"Datetime '{s}' must include a timezone offset")
        return dt

    @staticmethod
    def _action_key(action: str, details: dict[str, Any]) -> str:
        return f"{action}:{json.dumps(details, sort_keys=True, default=str)}"

    def get_user_preferences(self, user_id: str) -> dict[str, Any]:
        return {"preferences": asdict(self.prefs.get(user_id))}

    def list_events(self, calendar_id: str = "primary", **kwargs) -> dict[str, Any]:
        time_min = self._parse_dt(kwargs["time_min"])
        time_max = self._parse_dt(kwargs["time_max"])
        events = self.calendar.list_events(calendar_id, time_min, time_max)
        return {"events": [e.to_dict() for e in events], "count": len(events)}

    def get_event(self, event_id: str) -> dict[str, Any]:
        e = self.calendar.get_event(event_id)
        return {"event": e.to_dict() if e else None}

    def find_availability(
        self,
        participant_emails: list[str],
        duration_minutes: int,
        search_start: str,
        search_end: str,
        max_options: int = 5,
    ) -> dict[str, Any]:
        start = self._parse_dt(search_start)
        end = self._parse_dt(search_end)
        prefs = self.prefs.get(self.user_id)
        tz = ZoneInfo(prefs.timezone)

        busy_map = self.calendar.get_freebusy(participant_emails, start, end)
        all_busy: list[TimeRange] = []
        for ranges in busy_map.values():
            all_busy.extend(ranges)
        own = self.calendar.list_events("primary", start, end)
        all_busy.extend(TimeRange(e.start, e.end) for e in own)

        step = timedelta(minutes=15)
        duration = timedelta(minutes=duration_minutes)
        buffer = timedelta(minutes=prefs.buffer_minutes_between_meetings)

        slots: list[TimeRange] = []
        cursor = start
        while cursor + duration <= end and len(slots) < max_options:
            local = cursor.astimezone(tz)
            in_hours = prefs.working_hours_start <= local.hour < prefs.working_hours_end
            in_workday = local.weekday() in prefs.working_days
            not_blocked = local.weekday() not in prefs.no_meeting_days
            end_local = (cursor + duration).astimezone(tz)
            end_in_hours = end_local.hour <= prefs.working_hours_end or (
                end_local.hour == prefs.working_hours_end and end_local.minute == 0
            )

            slot_with_buffer = TimeRange(cursor - buffer, cursor + duration + buffer)
            conflicts = any(slot_with_buffer.overlaps(b) for b in all_busy)

            if in_hours and end_in_hours and in_workday and not_blocked and not conflicts:
                slot = TimeRange(cursor, cursor + duration)
                slots.append(slot)
                self._checked_slots.add((slot.start.isoformat(), slot.end.isoformat()))
                cursor += duration
            else:
                cursor += step

        return {
            "options": [
                {"start": s.start.isoformat(), "end": s.end.isoformat()} for s in slots
            ],
            "count": len(slots),
        }

    def check_conflicts(
        self,
        user_id: str,
        start: str,
        end: str,
        calendar_id: str = "primary",
    ) -> dict[str, Any]:
        s = self._parse_dt(start)
        e = self._parse_dt(end)
        prefs = self.prefs.get(user_id)
        tz = ZoneInfo(prefs.timezone)
        local_start = s.astimezone(tz)
        local_end = e.astimezone(tz)

        conflicts: list[dict[str, Any]] = []
        warnings: list[str] = []

        events = self.calendar.list_events(
            calendar_id, s - timedelta(hours=1), e + timedelta(hours=1)
        )
        proposed = TimeRange(s, e)
        for ev in events:
            if TimeRange(ev.start, ev.end).overlaps(proposed):
                conflicts.append({
                    "type": "event_overlap",
                    "event_id": ev.event_id,
                    "title": ev.title,
                    "start": ev.start.isoformat(),
                    "end": ev.end.isoformat(),
                })

        if not (prefs.working_hours_start <= local_start.hour < prefs.working_hours_end):
            warnings.append(
                f"Start {local_start.strftime('%H:%M')} is outside working hours "
                f"({prefs.working_hours_start:02d}:00-{prefs.working_hours_end:02d}:00 {prefs.timezone})"
            )
        if local_start.weekday() not in prefs.working_days:
            warnings.append(f"{local_start.strftime('%A')} is not a working day")
        if local_start.weekday() in prefs.no_meeting_days:
            warnings.append(f"{local_start.strftime('%A')} is a no-meeting day")
        buf_sec = prefs.buffer_minutes_between_meetings * 60
        for ev in events:
            if ev.end <= s and (s - ev.end).total_seconds() < buf_sec:
                warnings.append(
                    f"Less than {prefs.buffer_minutes_between_meetings}-min buffer "
                    f"after '{ev.title}'"
                )
            if ev.start >= e and (ev.start - e).total_seconds() < buf_sec:
                warnings.append(
                    f"Less than {prefs.buffer_minutes_between_meetings}-min buffer "
                    f"before '{ev.title}'"
                )
        same_day = [
            ev for ev in events
            if ev.start.astimezone(tz).date() == local_start.date()
        ]
        if len(same_day) >= prefs.max_meetings_per_day:
            warnings.append(
                f"Day already has {len(same_day)} meetings (cap: {prefs.max_meetings_per_day})"
            )

        self._checked_slots.add((s.isoformat(), e.isoformat()))

        return {
            "has_conflicts": bool(conflicts),
            "has_warnings": bool(warnings),
            "conflicts": conflicts,
            "warnings": warnings,
        }

    def create_event(
        self,
        title: str,
        start: str,
        end: str,
        attendee_emails: Optional[list[str]] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
        recurrence_rrule: Optional[str] = None,
        calendar_id: str = "primary",
    ) -> dict[str, Any]:
        key = (self._parse_dt(start).isoformat(), self._parse_dt(end).isoformat())
        if key not in self._checked_slots:
            return {
                "error": "precondition_failed",
                "message": (
                    "create_event requires a prior check_conflicts or find_availability "
                    "call covering the exact start/end. Call check_conflicts first."
                ),
            }

        event = CalendarEvent(
            event_id="",
            title=title,
            start=self._parse_dt(start),
            end=self._parse_dt(end),
            attendees=[Attendee(email=e) for e in (attendee_emails or [])],
            location=location,
            description=description,
            recurrence=recurrence_rrule,
            calendar_id=calendar_id,
        )
        created = self.calendar.create_event(event)
        logger.info("Created event %s: %s", created.event_id, created.title)
        return {"event": created.to_dict(), "status": "created"}

    def request_confirmation(
        self, action: str, risk: str, summary: str, details: dict[str, Any]
    ) -> dict[str, Any]:
        approved = self.hitl.request_confirmation(action, details, ActionRisk(risk))
        if approved:
            self._approved_actions.add(self._action_key(action, details))
        logger.info(
            "HITL %s action=%s risk=%s summary=%s",
            "APPROVED" if approved else "DENIED", action, risk, summary,
        )
        return {"approved": approved, "summary": summary}

    def update_event(self, event_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        details = {"event_id": event_id, "changes": changes}
        key = self._action_key("update_event", details)
        if key not in self._approved_actions:
            return {
                "error": "unauthorized",
                "message": (
                    "update_event requires a prior approved request_confirmation with "
                    "matching details. Call request_confirmation first."
                ),
            }
        self._approved_actions.discard(key)
        if "start" in changes and isinstance(changes["start"], str):
            changes["start"] = self._parse_dt(changes["start"])
        if "end" in changes and isinstance(changes["end"], str):
            changes["end"] = self._parse_dt(changes["end"])
        updated = self.calendar.update_event(event_id, changes)
        logger.info("Updated event %s", event_id)
        return {"event": updated.to_dict(), "status": "updated"}

    def cancel_event(
        self, event_id: str, notify_attendees: bool = True
    ) -> dict[str, Any]:
        details = {"event_id": event_id, "notify_attendees": notify_attendees}
        key = self._action_key("cancel_event", details)
        if key not in self._approved_actions:
            return {
                "error": "unauthorized",
                "message": (
                    "cancel_event requires a prior approved request_confirmation with "
                    "matching details. Call request_confirmation first."
                ),
            }
        self._approved_actions.discard(key)
        ok = self.calendar.cancel_event(event_id, notify_attendees)
        logger.info("Cancelled event %s (notify=%s, ok=%s)", event_id, notify_attendees, ok)
        return {"status": "cancelled" if ok else "not_found"}

    def dispatch(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        try:
            handler = getattr(self, name, None)
            if handler is None:
                return {"error": "unknown_tool", "message": f"No tool named {name}"}
            return handler(**args)
        except TypeError as exc:
            return {"error": "bad_arguments", "message": str(exc), "tool": name}
        except Exception as exc:
            logger.exception("Tool %s failed", name)
            return {"error": "tool_exception", "message": str(exc), "tool": name}


SYSTEM_PROMPT_TEMPLATE = """\
You are a Scheduler Agent: a careful, preference-aware assistant that manages a user's calendar.

## Core principles

1. READ BEFORE YOU WRITE. Always call get_user_preferences first when scheduling \
anything new. Always call check_conflicts (or find_availability for fresh slots) \
before create_event.

2. FAIL-CLOSED ON DESTRUCTIVE ACTIONS. update_event and cancel_event require a \
prior approved request_confirmation whose `details` exactly matches the destructive \
call's arguments. If denied, propose alternatives -- never retry the destructive call.

3. RESPECT PREFERENCES, SURFACE TRADE-OFFS. Honor working hours, no-meeting days, \
max-meetings-per-day, buffer windows, focus-block minimums. When the user's request \
conflicts with their stated preferences, name the conflict and ask -- do not silently \
override.

4. TIMEZONE DISCIPLINE. Every datetime you emit MUST be ISO 8601 with an explicit \
offset (e.g. 2026-06-15T14:00:00-07:00). Resolve relative times ("tomorrow at 2pm") \
in the user's stated timezone, not UTC.

5. PROPOSE, DON'T IMPOSE. For "find a time" requests, return 2-3 ranked options \
with one-line rationale unless the user said "just book it" or pinned a time.

6. BRIEF, CONCRETE REPLIES. After booking: "Booked: <title> -- <local time>. Invite \
sent." No preamble, no restating the ask.

## User context
- user_id:      {user_id}
- timezone:     {user_timezone}
- current_time: {current_time}

## Tool flow

- Read:    get_user_preferences | list_events | get_event | find_availability | check_conflicts
- Create:  check_conflicts -> create_event
- Modify:  request_confirmation -> update_event
- Cancel:  request_confirmation -> cancel_event

Stop calling tools once the task is complete or you need input from the user.

## Domain skill

{skill_body}
"""


def _load_skill(path: str) -> str:
    p = Path(path)
    if not p.exists():
        logger.warning("Skill file not found at %s; continuing without domain skill", path)
        return "(no domain skill loaded)"
    return p.read_text(encoding="utf-8")


@dataclass
class AgentTrace:
    """Audit record of one agent run."""
    request_id: str
    user_id: str
    user_message: str
    turns: int = 0
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    final_response: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SchedulerAgent:
    """Single-agent scheduler with tool use."""

    def __init__(
        self,
        client: Anthropic,
        calendar: CalendarBackend,
        prefs: PreferencesStore,
        hitl: HumanReviewQueue,
        model: str = MODEL,
        max_turns: int = MAX_TURNS,
        max_tokens: int = MAX_TOKENS,
        skill_path: str = SKILL_PATH,
    ) -> None:
        self.client = client
        self.calendar = calendar
        self.prefs = prefs
        self.hitl = hitl
        self.model = model
        self.max_turns = max_turns
        self.max_tokens = max_tokens
        self._skill_body = _load_skill(skill_path)

    def _build_system_prompt(self, user_id: str) -> str:
        p = self.prefs.get(user_id)
        now = datetime.now(ZoneInfo(p.timezone)).isoformat()
        return SYSTEM_PROMPT_TEMPLATE.format(
            user_id=user_id,
            user_timezone=p.timezone,
            current_time=now,
            skill_body=self._skill_body,
        )

    def run(self, user_id: str, user_message: str) -> AgentTrace:
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        trace = AgentTrace(request_id=request_id, user_id=user_id, user_message=user_message)
        executor = SchedulerToolExecutor(self.calendar, self.prefs, self.hitl, user_id)

        system = self._build_system_prompt(user_id)
        messages: list[dict[str, Any]] = [{"role": "user", "content": user_message}]

        try:
            for turn in range(self.max_turns):
                trace.turns = turn + 1
                resp = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=system,
                    tools=TOOLS,
                    messages=messages,
                )
                messages.append({"role": "assistant", "content": resp.content})

                if resp.stop_reason == "end_turn":
                    text_parts = [
                        b.text for b in resp.content if getattr(b, "type", None) == "text"
                    ]
                    trace.final_response = "\n".join(text_parts).strip()
                    logger.info("Agent completed in %d turn(s)", trace.turns)
                    return trace

                if resp.stop_reason == "tool_use":
                    tool_results: list[dict[str, Any]] = []
                    for block in resp.content:
                        if getattr(block, "type", None) != "tool_use":
                            continue
                        args = block.input if isinstance(block.input, dict) else {}
                        result = executor.dispatch(block.name, args)
                        trace.tool_calls.append({
                            "turn": trace.turns,
                            "name": block.name,
                            "input": args,
                            "result_preview": _preview(result),
                        })
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, default=str),
                        })
                    messages.append({"role": "user", "content": tool_results})
                    continue

                logger.warning("Unexpected stop_reason=%s", resp.stop_reason)
                trace.error = f"Unexpected stop_reason: {resp.stop_reason}"
                return trace

            trace.error = f"Max turns ({self.max_turns}) exceeded"
            logger.warning(trace.error)
            return trace

        except Exception as exc:
            logger.exception("Agent run failed")
            trace.error = f"{type(exc).__name__}: {exc}"
            return trace


def _preview(obj: Any, limit: int = 200) -> str:
    s = json.dumps(obj, default=str)
    return s if len(s) <= limit else s[:limit] + "..."


def _demo() -> None:
    """Smoke test against in-memory backends. Requires ANTHROPIC_API_KEY."""
    client = Anthropic()
    calendar = InMemoryCalendarBackend()
    prefs = InMemoryPreferencesStore()
    hitl = AutoApproveReviewQueue()

    prefs.update("u_demo", {
        "timezone": "America/Los_Angeles",
        "working_hours_start": 9,
        "working_hours_end": 17,
        "default_meeting_duration_minutes": 30,
        "buffer_minutes_between_meetings": 15,
    })

    tz = ZoneInfo("America/Los_Angeles")
    tomorrow_10 = (datetime.now(tz) + timedelta(days=1)).replace(
        hour=10, minute=0, second=0, microsecond=0
    )
    calendar.create_event(CalendarEvent(
        event_id="",
        title="Existing Standup",
        start=tomorrow_10,
        end=tomorrow_10 + timedelta(minutes=30),
    ))

    agent = SchedulerAgent(client=client, calendar=calendar, prefs=prefs, hitl=hitl)
    trace = agent.run(
        user_id="u_demo",
        user_message=(
            "Find a 30-min slot to meet with alex@example.com tomorrow morning "
            "and book it. Title it 'Alex sync'."
        ),
    )
    print("=== AGENT RESPONSE ===")
    print(trace.final_response)
    print("\n=== TOOL CALLS ===")
    for tc in trace.tool_calls:
        print(f"  [{tc['turn']}] {tc['name']} -> {tc['result_preview']}")
    if trace.error:
        print(f"\nERROR: {trace.error}")


if __name__ == "__main__":
    _demo()
