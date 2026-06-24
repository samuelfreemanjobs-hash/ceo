"""
google_calendar_backend.py
==========================
Production CalendarBackend for the Scheduler Agent, backed by Google Calendar API v3.

AUTH STRATEGIES
---------------
  1. OAuth2 user credentials (refresh token) -- per-user delegation
  2. Service account with domain-wide delegation -- org-wide on behalf of users

INSTALL
-------
    pip install google-api-python-client google-auth google-auth-oauthlib

USAGE
-----
    from anthropic import Anthropic
    from google_calendar_backend import (
        GoogleCalendarBackend,
        build_service_from_refresh_token,
    )
    from scheduler_agent import SchedulerAgent

    service = build_service_from_refresh_token(
        refresh_token=stored_token,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
    )
    calendar = GoogleCalendarBackend(service, default_calendar_id="primary")
    agent = SchedulerAgent(client=Anthropic(), calendar=calendar, prefs=..., hitl=...)

NOTES
-----
  * The backend is bound to ONE user's credentials. For multi-tenant deployments,
    construct a fresh GoogleCalendarBackend per request (or pool by user_id).
  * `get_freebusy` accepts up to 50 calendar IDs per call; we batch automatically.
  * Retries on 408/429/5xx with exponential backoff (5 attempts, ~31s max wait).
  * All-day events (date-only, no dateTime) are SILENTLY DROPPED -- our domain
    model only handles timed events. Adjust _to_event if you need to model these.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any, Optional

try:
    from googleapiclient.errors import HttpError
except ImportError as e:
    raise ImportError(
        "google-api-python-client not installed. "
        "Run: pip install google-api-python-client google-auth google-auth-oauthlib"
    ) from e

from scheduler_agent import (
    Attendee,
    CalendarBackend,
    CalendarEvent,
    EventStatus,
    TimeRange,
)

logger = logging.getLogger("scheduler_agent.google_backend")

RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}
MAX_RETRIES = 5
BASE_BACKOFF = 1.0
FREEBUSY_MAX_CALENDARS = 50
LIST_PAGE_SIZE = 250
DEFAULT_SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarBackend(CalendarBackend):
    """
    CalendarBackend backed by Google Calendar API v3.

    Bound to ONE user's credentials at construction. For multi-tenant
    deployments construct a new instance per request, or pool by user_id.
    """

    def __init__(
        self,
        service: Any,
        default_calendar_id: str = "primary",
        send_updates: str = "all",
    ) -> None:
        self.svc = service
        self.default_calendar_id = default_calendar_id
        self.send_updates = send_updates

    def list_events(
        self,
        calendar_id: str,
        time_min: datetime,
        time_max: datetime,
    ) -> list[CalendarEvent]:
        cal_id = calendar_id or self.default_calendar_id
        items: list[dict[str, Any]] = []
        page_token: Optional[str] = None
        while True:
            resp = self._execute(
                self.svc.events().list(
                    calendarId=cal_id,
                    timeMin=_to_rfc3339(time_min),
                    timeMax=_to_rfc3339(time_max),
                    singleEvents=True,
                    orderBy="startTime",
                    pageToken=page_token,
                    maxResults=LIST_PAGE_SIZE,
                )
            )
            items.extend(resp.get("items", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        events = [self._to_event(item, cal_id) for item in items]
        return [e for e in events if e is not None]

    def get_event(self, event_id: str) -> Optional[CalendarEvent]:
        try:
            item = self._execute(
                self.svc.events().get(
                    calendarId=self.default_calendar_id,
                    eventId=event_id,
                )
            )
            return self._to_event(item, self.default_calendar_id)
        except HttpError as exc:
            if exc.resp.status == 404:
                return None
            raise

    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        body = self._from_event(event)
        body.pop("id", None)
        cal_id = event.calendar_id or self.default_calendar_id
        resp = self._execute(
            self.svc.events().insert(
                calendarId=cal_id,
                body=body,
                sendUpdates=self.send_updates,
            )
        )
        result = self._to_event(resp, cal_id)
        if result is None:
            raise RuntimeError("Google returned an event without dateTime fields")
        return result

    def update_event(self, event_id: str, changes: dict[str, Any]) -> CalendarEvent:
        body = self._changes_to_body(changes)
        resp = self._execute(
            self.svc.events().patch(
                calendarId=self.default_calendar_id,
                eventId=event_id,
                body=body,
                sendUpdates=self.send_updates,
            )
        )
        result = self._to_event(resp, self.default_calendar_id)
        if result is None:
            raise RuntimeError("Google returned an event without dateTime fields")
        return result

    def cancel_event(self, event_id: str, notify_attendees: bool = True) -> bool:
        try:
            self._execute(
                self.svc.events().delete(
                    calendarId=self.default_calendar_id,
                    eventId=event_id,
                    sendUpdates="all" if notify_attendees else "none",
                )
            )
            return True
        except HttpError as exc:
            if exc.resp.status in (404, 410):
                return False
            raise

    def get_freebusy(
        self,
        emails: list[str],
        time_min: datetime,
        time_max: datetime,
    ) -> dict[str, list[TimeRange]]:
        if not emails:
            return {}
        result: dict[str, list[TimeRange]] = {}
        for i in range(0, len(emails), FREEBUSY_MAX_CALENDARS):
            chunk = emails[i : i + FREEBUSY_MAX_CALENDARS]
            body = {
                "timeMin": _to_rfc3339(time_min),
                "timeMax": _to_rfc3339(time_max),
                "items": [{"id": email} for email in chunk],
            }
            resp = self._execute(self.svc.freebusy().query(body=body))
            calendars = resp.get("calendars", {})
            for email in chunk:
                cal_info = calendars.get(email, {})
                if "errors" in cal_info:
                    logger.warning(
                        "freebusy errors for %s: %s", email, cal_info["errors"]
                    )
                    result[email] = []
                    continue
                ranges = [
                    TimeRange(
                        start=_parse_rfc3339(busy["start"]),
                        end=_parse_rfc3339(busy["end"]),
                    )
                    for busy in cal_info.get("busy", [])
                ]
                result[email] = ranges
        return result

    def _to_event(
        self, item: dict[str, Any], calendar_id: str
    ) -> Optional[CalendarEvent]:
        start = item.get("start", {})
        end = item.get("end", {})

        if "dateTime" not in start or "dateTime" not in end:
            return None

        attendees = [
            Attendee(
                email=a.get("email", ""),
                name=a.get("displayName"),
                optional=a.get("optional", False),
                response_status=a.get("responseStatus"),
            )
            for a in item.get("attendees", [])
        ]

        status_str = item.get("status", "confirmed")
        try:
            status = EventStatus(status_str)
        except ValueError:
            status = EventStatus.CONFIRMED

        rrule: Optional[str] = None
        for line in item.get("recurrence", []) or []:
            if line.startswith("RRULE:"):
                rrule = line[len("RRULE:") :]
                break

        return CalendarEvent(
            event_id=item["id"],
            title=item.get("summary", "(no title)"),
            start=_parse_rfc3339(start["dateTime"]),
            end=_parse_rfc3339(end["dateTime"]),
            attendees=attendees,
            location=item.get("location"),
            description=item.get("description"),
            status=status,
            recurrence=rrule,
            organizer_email=item.get("organizer", {}).get("email"),
            calendar_id=calendar_id,
        )

    def _from_event(self, event: CalendarEvent) -> dict[str, Any]:
        body: dict[str, Any] = {
            "summary": event.title,
            "start": _dt_to_google(event.start),
            "end": _dt_to_google(event.end),
        }
        if event.location:
            body["location"] = event.location
        if event.description:
            body["description"] = event.description
        if event.attendees:
            body["attendees"] = [
                {
                    "email": a.email,
                    **({"displayName": a.name} if a.name else {}),
                    **({"optional": True} if a.optional else {}),
                }
                for a in event.attendees
            ]
        if event.recurrence:
            body["recurrence"] = [f"RRULE:{event.recurrence}"]
        if event.status and event.status != EventStatus.CONFIRMED:
            body["status"] = event.status.value
        return body

    def _changes_to_body(self, changes: dict[str, Any]) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if "title" in changes:
            body["summary"] = changes["title"]
        if "start" in changes:
            s = changes["start"]
            if isinstance(s, str):
                s = _parse_rfc3339(s)
            body["start"] = _dt_to_google(s)
        if "end" in changes:
            e = changes["end"]
            if isinstance(e, str):
                e = _parse_rfc3339(e)
            body["end"] = _dt_to_google(e)
        if "location" in changes:
            body["location"] = changes["location"]
        if "description" in changes:
            body["description"] = changes["description"]
        if "attendees" in changes:
            attendees = changes["attendees"] or []
            normalized = []
            for a in attendees:
                if isinstance(a, Attendee):
                    entry = {"email": a.email}
                    if a.name:
                        entry["displayName"] = a.name
                    if a.optional:
                        entry["optional"] = True
                    normalized.append(entry)
                elif isinstance(a, str):
                    normalized.append({"email": a})
                elif isinstance(a, dict):
                    normalized.append(a)
            body["attendees"] = normalized
        if "recurrence_rrule" in changes:
            rule = changes["recurrence_rrule"]
            body["recurrence"] = [f"RRULE:{rule}"] if rule else None
        return body

    def _execute(self, request: Any) -> Any:
        last_exc: Optional[Exception] = None
        for attempt in range(MAX_RETRIES):
            try:
                return request.execute()
            except HttpError as exc:
                status = exc.resp.status
                if status not in RETRYABLE_STATUS:
                    raise
                wait = BASE_BACKOFF * (2 ** attempt)
                logger.warning(
                    "Google API HTTP %d (attempt %d/%d); retry in %.1fs",
                    status, attempt + 1, MAX_RETRIES, wait,
                )
                last_exc = exc
                time.sleep(wait)
            except (ConnectionError, TimeoutError) as exc:
                wait = BASE_BACKOFF * (2 ** attempt)
                logger.warning(
                    "Transport error %s (attempt %d/%d); retry in %.1fs",
                    exc, attempt + 1, MAX_RETRIES, wait,
                )
                last_exc = exc
                time.sleep(wait)
        if last_exc:
            raise last_exc
        raise RuntimeError("Retry loop exited without success or exception")


def _to_rfc3339(dt: datetime) -> str:
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware for Google Calendar API")
    return dt.isoformat()


def _parse_rfc3339(s: str) -> datetime:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError(f"Google returned naive datetime: {s}")
    return dt


def _dt_to_google(dt: datetime) -> dict[str, str]:
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")
    tz_name = getattr(dt.tzinfo, "key", None) or str(dt.tzinfo)
    return {"dateTime": dt.isoformat(), "timeZone": tz_name}


def build_service_from_refresh_token(
    refresh_token: str,
    client_id: str,
    client_secret: str,
    scopes: Optional[list[str]] = None,
) -> Any:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=scopes or DEFAULT_SCOPES,
    )
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def build_service_from_service_account(
    service_account_file: str,
    impersonate_email: str,
    scopes: Optional[list[str]] = None,
) -> Any:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=scopes or DEFAULT_SCOPES,
        subject=impersonate_email,
    )
    return build("calendar", "v3", credentials=creds, cache_discovery=False)
