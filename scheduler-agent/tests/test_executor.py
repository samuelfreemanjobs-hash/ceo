"""Unit tests for SchedulerToolExecutor safety policies (no API key required)."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from scheduler_agent import (
    AutoApproveReviewQueue,
    CalendarEvent,
    InMemoryCalendarBackend,
    InMemoryPreferencesStore,
    SchedulerToolExecutor,
)


@pytest.fixture
def executor():
    cal = InMemoryCalendarBackend()
    prefs = InMemoryPreferencesStore()
    prefs.update("u_test", {
        "timezone": "America/Los_Angeles",
        "working_hours_start": 9,
        "working_hours_end": 17,
    })
    return SchedulerToolExecutor(cal, prefs, AutoApproveReviewQueue(), "u_test"), cal


def _slot_tomorrow_11am(tz_name: str = "America/Los_Angeles"):
    tz = ZoneInfo(tz_name)
    start = (datetime.now(tz) + timedelta(days=1)).replace(
        hour=11, minute=0, second=0, microsecond=0
    )
    end = start + timedelta(minutes=30)
    return start.isoformat(), end.isoformat()


def test_create_event_requires_prior_check(executor):
    ex, _ = executor
    start, end = _slot_tomorrow_11am()
    result = ex.create_event(title="Test", start=start, end=end)
    assert result["error"] == "precondition_failed"


def test_check_then_create_succeeds(executor):
    ex, cal = executor
    start, end = _slot_tomorrow_11am()
    ex.check_conflicts(user_id="u_test", start=start, end=end)
    result = ex.create_event(title="Test", start=start, end=end)
    assert result["status"] == "created"
    assert cal.list_events("primary", datetime.fromisoformat(start), datetime.fromisoformat(end))


def test_update_without_confirmation_rejected(executor):
    ex, cal = executor
    tz = ZoneInfo("America/Los_Angeles")
    start = (datetime.now(tz) + timedelta(days=1)).replace(hour=11, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=30)
    created = cal.create_event(CalendarEvent(event_id="", title="Old", start=start, end=end))

    result = ex.update_event(created.event_id, {"title": "New"})
    assert result["error"] == "unauthorized"


def test_update_after_confirmation_succeeds(executor):
    ex, cal = executor
    tz = ZoneInfo("America/Los_Angeles")
    start = (datetime.now(tz) + timedelta(days=1)).replace(hour=11, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=30)
    created = cal.create_event(CalendarEvent(event_id="", title="Old", start=start, end=end))

    details = {"event_id": created.event_id, "changes": {"title": "New"}}
    ex.request_confirmation(
        action="update_event",
        risk="high",
        summary="Rename meeting",
        details=details,
    )
    result = ex.update_event(created.event_id, {"title": "New"})
    assert result["status"] == "updated"
    assert cal.get_event(created.event_id).title == "New"


def test_cancel_without_confirmation_rejected(executor):
    ex, cal = executor
    tz = ZoneInfo("America/Los_Angeles")
    start = (datetime.now(tz) + timedelta(days=1)).replace(hour=11, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=30)
    created = cal.create_event(CalendarEvent(event_id="", title="Cancel me", start=start, end=end))

    result = ex.cancel_event(created.event_id)
    assert result["error"] == "unauthorized"


def test_naive_datetime_rejected(executor):
    ex, _ = executor
    with pytest.raises(ValueError, match="timezone offset"):
        ex.check_conflicts(
            user_id="u_test",
            start="2026-06-15T11:00:00",
            end="2026-06-15T11:30:00",
        )
