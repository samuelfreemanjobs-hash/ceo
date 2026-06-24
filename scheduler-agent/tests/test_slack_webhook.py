"""Tests for Slack webhook route (signature bypass via injected store)."""

import json

import pytest

pytest.importorskip("flask")

from slack_hitl_queue import InMemoryConfirmationStore, build_confirmation_record, slack_action_value
from slack_webhook_server import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SLACK_SIGNING_SECRET", "test-secret")
    store = InMemoryConfirmationStore()
    app = create_app(store=store)

    from slack_sdk.signature import SignatureVerifier

    monkeypatch.setattr(
        SignatureVerifier,
        "is_valid_request",
        lambda self, body, headers: True,
    )
    app.config["TESTING"] = True
    return app.test_client(), store


def test_health(client):
    c, _ = client
    resp = c.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_slack_interaction_updates_store(client):
    c, store = client
    rec = build_confirmation_record("update_event", "high", "Reschedule", {"event_id": "e1"})
    store.register(rec)
    cid = rec.confirmation_id

    payload = {
        "type": "block_actions",
        "user": {"id": "U555"},
        "actions": [{"value": slack_action_value("deny", cid)}],
    }
    resp = c.post(
        "/slack/interactions",
        data={"payload": json.dumps(payload)},
    )
    assert resp.status_code == 200
    assert store.get(cid).decision is False
