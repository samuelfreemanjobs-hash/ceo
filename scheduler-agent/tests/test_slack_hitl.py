"""Tests for Slack HITL confirmation store and payload processing."""

import time

import pytest

from slack_hitl_queue import (
    InMemoryConfirmationStore,
    PendingConfirmation,
    parse_slack_action_value,
    process_slack_interaction_payload,
)


def _pending(cid: str = "abc123", **kwargs) -> PendingConfirmation:
    defaults = dict(
        confirmation_id=cid,
        action="cancel_event",
        risk="critical",
        summary="Cancel standup",
        details={"event_id": "evt_1"},
        channel="C_TEST",
        expires_at=time.time() + 300,
    )
    defaults.update(kwargs)
    return PendingConfirmation(**defaults)


def test_parse_slack_action_value():
    assert parse_slack_action_value("approve:abc") == ("approve", "abc")
    assert parse_slack_action_value("deny:abc") == ("deny", "abc")
    assert parse_slack_action_value("invalid") is None


def test_in_memory_store_approve_deny():
    store = InMemoryConfirmationStore()
    rec = _pending()
    store.create_pending(rec)

    assert store.set_decision(rec.confirmation_id, True, "U123") is True
    assert store.get(rec.confirmation_id).status == "approved"
    assert store.set_decision(rec.confirmation_id, False, "U456") is False


def test_process_slack_interaction_payload():
    store = InMemoryConfirmationStore()
    rec = _pending(cid="cid_xyz")
    store.create_pending(rec)

    payload = {
        "type": "block_actions",
        "user": {"id": "U777"},
        "actions": [{"value": "approve:cid_xyz"}],
    }
    assert process_slack_interaction_payload(payload, store) == 1
    assert store.get("cid_xyz").status == "approved"


def test_expired_confirmation_rejects_decision():
    store = InMemoryConfirmationStore()
    rec = _pending(expires_at=time.time() - 1)
    store.create_pending(rec)
    assert store.set_decision(rec.confirmation_id, True, "U1") is False


def test_mark_expired():
    store = InMemoryConfirmationStore()
    rec = _pending()
    store.create_pending(rec)
    store.mark_expired(rec.confirmation_id)
    assert store.get(rec.confirmation_id).status == "expired"
