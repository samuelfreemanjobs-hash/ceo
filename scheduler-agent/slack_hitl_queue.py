"""
slack_hitl_queue.py
===================
Human-in-the-loop confirmation store + SlackHumanReviewQueue for Scheduler Agent.

The agent posts an interactive Slack message, then polls ConfirmationStore until
the webhook server (slack_webhook_server.py) records approve/deny from button clicks.

ARCHITECTURE
------------
  SchedulerAgent.request_confirmation tool call
    -> SlackHumanReviewQueue.request_confirmation()
         -> register pending in ConfirmationStore
         -> post Slack blocks (approve:{cid} / deny:{cid})
         -> poll store.wait_for_decision(cid)
    <- Slack user clicks button
    -> slack_webhook_server receives interaction
         -> store.set_decision(cid, approved, responder)
    -> polling loop returns; agent continues or proposes alternatives
"""

from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

logger = logging.getLogger("scheduler_agent.slack_hitl")

DEFAULT_CONFIRMATION_TTL_SECONDS = int(
    __import__("os").environ.get("HITL_CONFIRMATION_TTL_SECONDS", "600")
)
DEFAULT_POLL_TIMEOUT_SECONDS = int(
    __import__("os").environ.get("HITL_POLL_TIMEOUT_SECONDS", "300")
)
DEFAULT_POLL_INTERVAL_SECONDS = float(
    __import__("os").environ.get("HITL_POLL_INTERVAL_SECONDS", "0.5")
)


@dataclass
class ConfirmationRecord:
    confirmation_id: str
    action: str
    risk: str
    summary: str
    details: dict[str, Any]
    created_at: datetime
    expires_at: datetime
    decision: Optional[bool] = None
    responder: Optional[str] = None
    decided_at: Optional[datetime] = None

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at

    def to_json(self) -> str:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        d["expires_at"] = self.expires_at.isoformat()
        d["decided_at"] = self.decided_at.isoformat() if self.decided_at else None
        return json.dumps(d, default=str)

    @classmethod
    def from_json(cls, raw: str) -> "ConfirmationRecord":
        d = json.loads(raw)
        d["created_at"] = datetime.fromisoformat(d["created_at"])
        d["expires_at"] = datetime.fromisoformat(d["expires_at"])
        if d.get("decided_at"):
            d["decided_at"] = datetime.fromisoformat(d["decided_at"])
        return cls(**d)


class ConfirmationStore:
    """Shared store between SlackHumanReviewQueue (writer/poller) and webhook (writer)."""

    def register(self, record: ConfirmationRecord) -> str:
        raise NotImplementedError

    def get(self, confirmation_id: str) -> Optional[ConfirmationRecord]:
        raise NotImplementedError

    def set_decision(self, confirmation_id: str, approved: bool, responder: str) -> bool:
        """
        Record a human decision. Returns True if newly recorded;
        False if already decided, expired, or unknown id.
        """
        raise NotImplementedError

    def wait_for_decision(
        self,
        confirmation_id: str,
        timeout_seconds: float,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
    ) -> Optional[bool]:
        """
        Poll until decision recorded, timeout, or expiry.
        Returns True/False on decision, None on timeout/expiry without decision.
        """
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            rec = self.get(confirmation_id)
            if rec is None:
                return None
            if rec.is_expired() and rec.decision is None:
                return None
            if rec.decision is not None:
                return rec.decision
            time.sleep(poll_interval)
        return None


class InMemoryConfirmationStore(ConfirmationStore):
    """
    Process-local store. Works only when agent and webhook share the same process
    OR you run a single combined server. For split deployments use Redis.
    """

    def __init__(self) -> None:
        self._records: dict[str, ConfirmationRecord] = {}
        self._events: dict[str, threading.Event] = {}
        self._lock = threading.Lock()

    def register(self, record: ConfirmationRecord) -> str:
        with self._lock:
            self._records[record.confirmation_id] = record
            self._events[record.confirmation_id] = threading.Event()
        return record.confirmation_id

    def get(self, confirmation_id: str) -> Optional[ConfirmationRecord]:
        with self._lock:
            return self._records.get(confirmation_id)

    def set_decision(self, confirmation_id: str, approved: bool, responder: str) -> bool:
        with self._lock:
            rec = self._records.get(confirmation_id)
            if rec is None or rec.decision is not None or rec.is_expired():
                return False
            rec.decision = approved
            rec.responder = responder
            rec.decided_at = datetime.now(timezone.utc)
            ev = self._events.get(confirmation_id)
            if ev:
                ev.set()
            return True

    def wait_for_decision(
        self,
        confirmation_id: str,
        timeout_seconds: float,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
    ) -> Optional[bool]:
        ev = self._events.get(confirmation_id)
        if ev and ev.wait(timeout=timeout_seconds):
            rec = self.get(confirmation_id)
            return rec.decision if rec else None
        return super().wait_for_decision(confirmation_id, timeout_seconds, poll_interval)


class RedisConfirmationStore(ConfirmationStore):
    """Redis-backed store for split agent / webhook deployments."""

    def __init__(self, client: Any, *, key_prefix: str = "scheduler:confirmation:") -> None:
        self._redis = client
        self._prefix = key_prefix

    def _key(self, confirmation_id: str) -> str:
        return f"{self._prefix}{confirmation_id}"

    def register(self, record: ConfirmationRecord) -> str:
        ttl = max(1, int((record.expires_at - datetime.now(timezone.utc)).total_seconds()))
        self._redis.setex(self._key(record.confirmation_id), ttl, record.to_json())
        return record.confirmation_id

    def get(self, confirmation_id: str) -> Optional[ConfirmationRecord]:
        raw = self._redis.get(self._key(confirmation_id))
        if not raw:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return ConfirmationRecord.from_json(raw)

    def set_decision(self, confirmation_id: str, approved: bool, responder: str) -> bool:
        key = self._key(confirmation_id)
        pipe = self._redis.pipeline(True)
        while True:
            try:
                pipe.watch(key)
                raw = pipe.get(key)
                if not raw:
                    pipe.unwatch()
                    return False
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8")
                rec = ConfirmationRecord.from_json(raw)
                if rec.decision is not None or rec.is_expired():
                    pipe.unwatch()
                    return False
                rec.decision = approved
                rec.responder = responder
                rec.decided_at = datetime.now(timezone.utc)
                ttl = pipe.ttl(key)
                pipe.multi()
                pipe.setex(key, max(ttl, 60), rec.to_json())
                pipe.execute()
                return True
            except Exception:
                continue


def build_confirmation_record(
    action: str,
    risk: str,
    summary: str,
    details: dict[str, Any],
    *,
    ttl_seconds: int = DEFAULT_CONFIRMATION_TTL_SECONDS,
) -> ConfirmationRecord:
    now = datetime.now(timezone.utc)
    return ConfirmationRecord(
        confirmation_id=f"cnf_{uuid.uuid4().hex[:12]}",
        action=action,
        risk=risk,
        summary=summary or action,
        details=details,
        created_at=now,
        expires_at=now + timedelta(seconds=ttl_seconds),
    )


def slack_action_value(decision: str, confirmation_id: str) -> str:
    return f"{decision}:{confirmation_id}"


def parse_slack_action_value(value: str) -> Optional[tuple[str, str]]:
    if ":" not in value:
        return None
    decision, cid = value.split(":", 1)
    if decision not in ("approve", "deny"):
        return None
    return decision, cid


def process_slack_interaction_payload(
    payload: dict[str, Any], store: ConfirmationStore
) -> int:
    """Apply button-click decisions from a Slack interaction payload. Returns count updated."""
    if payload.get("type") != "block_actions":
        return 0
    responder = payload.get("user", {}).get("id", "unknown")
    applied = 0
    for action in payload.get("actions", []):
        parsed = parse_slack_action_value(action.get("value", ""))
        if not parsed:
            continue
        decision, cid = parsed
        if store.set_decision(cid, decision == "approve", responder):
            applied += 1
            logger.info(
                "Confirmation %s %s by %s",
                cid,
                "APPROVED" if decision == "approve" else "DENIED",
                responder,
            )
        else:
            logger.warning(
                "Confirmation %s not updated (already decided or expired)", cid
            )
    return applied


class SlackHumanReviewQueue:
    """
    Production HITL queue: posts Slack interactive message, polls ConfirmationStore.

    Implements the HumanReviewQueue protocol used by SchedulerToolExecutor.
    """

    def __init__(
        self,
        store: ConfirmationStore,
        *,
        bot_token: str,
        channel_id: str,
        poll_timeout_seconds: int = DEFAULT_POLL_TIMEOUT_SECONDS,
        confirmation_ttl_seconds: int = DEFAULT_CONFIRMATION_TTL_SECONDS,
    ) -> None:
        try:
            from slack_sdk import WebClient
        except ImportError as e:
            raise ImportError("slack-sdk not installed. Run: pip install slack-sdk") from e

        self.store = store
        self.client = WebClient(token=bot_token)
        self.channel_id = channel_id
        self.poll_timeout_seconds = poll_timeout_seconds
        self.confirmation_ttl_seconds = confirmation_ttl_seconds

    def request_confirmation(
        self,
        action: str,
        details: dict[str, Any],
        risk: Any,
        *,
        summary: str = "",
    ) -> bool:
        risk_value = risk.value if hasattr(risk, "value") else str(risk)
        record = build_confirmation_record(
            action,
            risk_value,
            summary,
            details,
            ttl_seconds=self.confirmation_ttl_seconds,
        )
        self.store.register(record)
        cid = record.confirmation_id

        details_text = json.dumps(details, indent=2, default=str)
        if len(details_text) > 2800:
            details_text = details_text[:2800] + "\n..."

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*:calendar: Scheduler confirmation required*\n"
                        f"*Action:* `{action}` · *Risk:* `{risk_value}`\n"
                        f"{summary or '_No summary provided_'}\n"
                        f"```\n{details_text}\n```"
                    ),
                },
            },
            {
                "type": "actions",
                "block_id": f"hitl_{cid}",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve"},
                        "style": "primary",
                        "action_id": f"approve_{cid}",
                        "value": slack_action_value("approve", cid),
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Deny"},
                        "style": "danger",
                        "action_id": f"deny_{cid}",
                        "value": slack_action_value("deny", cid),
                    },
                ],
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"`{cid}` · expires in {self.confirmation_ttl_seconds // 60} min",
                    }
                ],
            },
        ]

        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=f"Scheduler HITL: {action} ({risk_value}) — approval required",
                blocks=blocks,
            )
        except Exception:
            logger.exception("Failed to post Slack HITL message for %s", cid)
            return False

        decision = self.store.wait_for_decision(cid, self.poll_timeout_seconds)
        if decision is None:
            logger.warning("HITL timeout for %s action=%s", cid, action)
            return False
        return bool(decision)
