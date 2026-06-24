"""
google_calendar_backend.py
==========================
CalendarBackend implementation sketch for Google Calendar API v3.

NOT runnable without credentials and dependencies:
    pip install google-api-python-client google-auth google-auth-oauthlib

Wire per-user OAuth refresh tokens from your secrets store (see
production_wiring_example.py).
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

from scheduler_agent import (
    Attendee,
    CalendarBackend,
    CalendarEvent,
    EventStatus,
    TimeRange,
)

logger = logging.getLogger("scheduler_agent.google_calendar")


def build_service_from_refresh_token(
    refresh_token: str,
    client_id: str,
    client_secret: str,
    scopes: Optional[list[str]] = None,
) -> Any:
    """
    Build an authenticated Google Calendar API service from a stored refresh token.

    Returns a googleapiclient.discovery.Resource for calendar v3.
    """
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError as e:
        raise ImportError(
            "Google Calendar deps missing. Run: "
            "pip install google-api-python-client google-auth google-auth-oauthlib"
        ) from e

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes or ["https://www.googleapis.com/auth/calendar"],
    )
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


class GoogleCalendarBackend(CalendarBackend):
    """
    Google Calendar adapter implementing CalendarBackend.

    Args:
        service: Authenticated calendar v3 service from build_service_from_refresh_token
        default_calendar_id: Usually "primary"
        send_updates: "all" | "externalOnly" | "none" — passed to insert/patch/delete
    """

    def __init__(
        self,
        service: Any,
        default_calendar_id: str = "primary",
        send_updates: str = "all",
    ) -> None:
        self.service = service
        self.default_calendar_id = default_calendar_id
        self.send_updates = send_updates

    # ---- mapping helpers -------------------------------------------------

    @staticmethod
    def _parse_google_dt(raw: dict[str, str]) -> datetime:
        value = raw.get("dateTime") or raw.get("date")
        if not value:
            raise ValueError(f"Google event missing start/end: {raw}")
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError(f"Naive datetime from Google API: {value}")
        return dt

    def _to_domain(self, item: dict[str, Any], calendar_id: str) -> CalendarEvent:
        status_map = {
            "confirmed": EventStatus.CONFIRMED,
            "tentative": EventStatus.TENTATIVE,
            "cancelled": EventStatus.CANCELLED,
        }
        attendees = [
            Attendee(
                email=a["email"],
                name=a.get("displayName"),
                optional=a.get("optional", False),
                response_status=a.get("responseStatus"),
            )
            for a in item.get("attendees", [])
        ]
        return CalendarEvent(
            event_id=item["id"],
            title=item.get("summary", "(no title)"),
            start=self._parse_google_dt(item["start"]),
            end=self._parse_google_dt(item["end"]),
            attendees=attendees,
            location=item.get("location"),
            description=item.get("description"),
            status=status_map.get(item.get("status", "confirmed"), EventStatus.CONFIRMED),
            recurrence=item.get("recurrence", [None])[0] if item.get("recurrence") else None,
            organizer_email=(item.get("organizer") or {}).get("email"),
            calendar_id=calendar_id,
        )

    def _to_google_body(self, event: CalendarEvent) -> dict[str, Any]:
        body: dict[str, Any] = {
            "summary": event.title,
            "start": {"dateTime": event.start.isoformat()},
            "end": {"dateTime": event.end.isoformat()},
        }
        if event.location:
            body["location"] = event.location
        if event.description:
            body["description"] = event.description
        if event.attendees:
            body["attendees"] = [{"email": a.email, "optional": a.optional} for a in event.attendees]
        if event.recurrence:
            body["recurrence"] = [event.recurrence]
        return body

    # ---- CalendarBackend -------------------------------------------------

    def list_events(
        self, calendar_id: str, time_min: datetime, time_max: datetime
    ) -> list[CalendarEvent]:
        cal = calendar_id or self.default_calendar_id
        result = (
            self.service.events()
            .list(
                calendarId=cal,
                timeMin=time_min.isoformat(),
                timeMax=time_max.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return [self._to_domain(item, cal) for item in result.get("items", [])]

    def get_event(self, event_id: str) -> Optional[CalendarEvent]:
        try:
            item = (
                self.service.events()
                .get(calendarId=self.default_calendar_id, eventId=event_id)
                .execute()
            )
            return self._to_domain(item, self.default_calendar_id)
        except Exception as exc:
            logger.warning("get_event %s failed: %s", event_id, exc)
            return None

    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        cal = event.calendar_id or self.default_calendar_id
        created = (
            self.service.events()
            .insert(
                calendarId=cal,
                body=self._to_google_body(event),
                sendUpdates=self.send_updates,
            )
            .execute()
        )
        return self._to_domain(created, cal)

    def update_event(self, event_id: str, changes: dict[str, Any]) -> CalendarEvent:
        existing = self.get_event(event_id)
        if not existing:
            raise KeyError(f"Event not found: {event_id}")

        if "title" in changes:
            existing.title = changes["title"]
        if "start" in changes:
            existing.start = changes["start"]
        if "end" in changes:
            existing.end = changes["end"]
        if "location" in changes:
            existing.location = changes["location"]
        if "description" in changes:
            existing.description = changes["description"]

        updated = (
            self.service.events()
            .patch(
                calendarId=existing.calendar_id,
                eventId=event_id,
                body=self._to_google_body(existing),
                sendUpdates=self.send_updates,
            )
            .execute()
        )
        return self._to_domain(updated, existing.calendar_id)

    def cancel_event(self, event_id: str, notify_attendees: bool = True) -> bool:
        send = self.send_updates if notify_attendees else "none"
        try:
            self.service.events().delete(
                calendarId=self.default_calendar_id,
                eventId=event_id,
                sendUpdates=send,
            ).execute()
            return True
        except Exception as exc:
            logger.warning("cancel_event %s failed: %s", event_id, exc)
            return False

    def get_freebusy(
        self, emails: list[str], time_min: datetime, time_max: datetime
    ) -> dict[str, list[TimeRange]]:
        body = {
            "timeMin": time_min.isoformat(),
            "timeMax": time_max.isoformat(),
            "items": [{"id": email} for email in emails],
        }
        result = self.service.freebusy().query(body=body).execute()
        out: dict[str, list[TimeRange]] = {}
        for email in emails:
            busy = result.get("calendars", {}).get(email, {}).get("busy", [])
            out[email] = [
                TimeRange(
                    start=datetime.fromisoformat(b["start"].replace("Z", "+00:00")),
                    end=datetime.fromisoformat(b["end"].replace("Z", "+00:00")),
                )
                for b in busy
            ]
        return out
