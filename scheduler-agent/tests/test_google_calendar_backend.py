"""Unit tests for google_calendar_backend conversion helpers (no live API)."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

try:
    import google_calendar_backend as google_calendar
except ImportError:
    pytest.skip(
        "google-api-python-client not installed; pip install -r requirements-production.txt",
        allow_module_level=True,
    )

GoogleCalendarBackend = google_calendar.GoogleCalendarBackend
_parse_rfc3339 = google_calendar._parse_rfc3339
_to_rfc3339 = google_calendar._to_rfc3339
_dt_to_google = google_calendar._dt_to_google


class _FakeService:
    pass


@pytest.fixture
def backend():
    return GoogleCalendarBackend(_FakeService())


def test_parse_and_format_rfc3339():
    dt = datetime(2026, 6, 16, 10, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    s = _to_rfc3339(dt)
    assert _parse_rfc3339(s) == dt


def test_dt_to_google_includes_timezone():
    dt = datetime(2026, 6, 16, 10, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    g = _dt_to_google(dt)
    assert g["dateTime"] == dt.isoformat()
    assert g["timeZone"] == "America/Los_Angeles"


def test_to_event_timed(backend):
    item = {
        "id": "evt_1",
        "summary": "Sync",
        "start": {"dateTime": "2026-06-16T10:00:00-07:00"},
        "end": {"dateTime": "2026-06-16T10:30:00-07:00"},
        "status": "confirmed",
    }
    ev = backend._to_event(item, "primary")
    assert ev is not None
    assert ev.title == "Sync"
    assert ev.event_id == "evt_1"


def test_to_event_drops_all_day(backend):
    item = {
        "id": "evt_2",
        "summary": "Holiday",
        "start": {"date": "2026-06-16"},
        "end": {"date": "2026-06-17"},
    }
    assert backend._to_event(item, "primary") is None


def test_from_event_includes_rrule(backend):
    start = datetime(2026, 6, 16, 10, 0, tzinfo=ZoneInfo("UTC"))
    end = start.replace(minute=30)
    from scheduler_agent import CalendarEvent

    body = backend._from_event(
        CalendarEvent(
            event_id="",
            title="Standup",
            start=start,
            end=end,
            recurrence="FREQ=WEEKLY;BYDAY=MO,WE,FR",
        )
    )
    assert body["recurrence"] == ["RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"]


def test_changes_to_body_parses_iso_strings(backend):
    body = backend._changes_to_body({
        "title": "Renamed",
        "start": "2026-06-16T10:00:00-07:00",
        "end": "2026-06-16T11:00:00-07:00",
    })
    assert body["summary"] == "Renamed"
    assert "dateTime" in body["start"]
    assert body["start"]["timeZone"]
