"""Tests for Slack webhook route (signature bypass via injected store)."""

import json
import time

import pytest

pytest.importorskip("flask")

from slack_hitl_queue import InMemoryConfirmationStore, PendingConfirmation
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
    cid = "webhook_test_id"
    store.create_pending(
        PendingConfirmation(
            confirmation_id=cid,
            action="update_event",
            risk="high",
            summary="Reschedule",
            details={"event_id": "e1"},
            channel="C_TEST",
            expires_at=time.time() + 300,
        )
    )

    payload = {
        "type": "block_actions",
        "user": {"id": "U555"},
        "actions": [{"value": f"deny:{cid}"}],
    }
    resp = c.post(
        "/slack/interactions",
        data={"payload": json.dumps(payload)},
    )
    assert resp.status_code == 200
    assert store.get(cid).status == "denied"
