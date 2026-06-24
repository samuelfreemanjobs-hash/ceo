"""Tests for Slack HITL confirmation store and payload processing."""

import json
from datetime import datetime, timedelta, timezone

import pytest

from slack_hitl_queue import (
    InMemoryConfirmationStore,
    build_confirmation_record,
    parse_slack_action_value,
    process_slack_interaction_payload,
    slack_action_value,
)


def test_parse_slack_action_value():
    assert parse_slack_action_value("approve:cnf_abc") == ("approve", "cnf_abc")
    assert parse_slack_action_value("deny:cnf_abc") == ("deny", "cnf_abc")
    assert parse_slack_action_value("invalid") is None


def test_in_memory_store_approve_deny():
    store = InMemoryConfirmationStore()
    rec = build_confirmation_record(
        "cancel_event",
        "critical",
        "Cancel standup",
        {"event_id": "evt_1", "notify_attendees": True},
        ttl_seconds=300,
    )
    store.register(rec)
    cid = rec.confirmation_id

    assert store.set_decision(cid, True, "U123") is True
    assert store.get(cid).decision is True
    assert store.set_decision(cid, False, "U456") is False


def test_wait_for_decision():
    store = InMemoryConfirmationStore()
    rec = build_confirmation_record("update_event", "high", "Move meeting", {"event_id": "e1"})
    store.register(rec)
    cid = rec.confirmation_id

    import threading

    def approve_later():
        store.set_decision(cid, True, "U999")

    threading.Timer(0.1, approve_later).start()
    assert store.wait_for_decision(cid, timeout_seconds=2.0) is True


def test_process_slack_interaction_payload():
    store = InMemoryConfirmationStore()
    rec = build_confirmation_record("cancel_event", "critical", "Cancel", {"event_id": "e2"})
    store.register(rec)
    cid = rec.confirmation_id

    payload = {
        "type": "block_actions",
        "user": {"id": "U777"},
        "actions": [{"value": slack_action_value("approve", cid)}],
    }
    assert process_slack_interaction_payload(payload, store) == 1
    assert store.get(cid).decision is True


def test_expired_confirmation_rejects_decision():
    store = InMemoryConfirmationStore()
    now = datetime.now(timezone.utc)
    rec = build_confirmation_record("cancel_event", "critical", "Cancel", {"event_id": "e3"})
    rec.expires_at = now - timedelta(seconds=1)
    store.register(rec)
    assert store.set_decision(rec.confirmation_id, True, "U1") is False
