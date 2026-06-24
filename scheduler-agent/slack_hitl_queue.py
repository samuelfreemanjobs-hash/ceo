"""
slack_hitl_queue.py
===================
Production HumanReviewQueue for the Scheduler Agent, using Slack interactive messages.

ARCHITECTURE
------------
  [Scheduler Agent]           [Slack]              [Webhook server]
        |                        |                       |
   request_confirmation          |                       |
        |                        |                       |
    -- chat.postMessage -------->|                       |
        |                        |                       |
   poll ConfirmationStore        |                       |
        |                    user clicks               receive interaction
        |                    Approve/Deny      ----POST----> /slack/interactions
        |                        |                       |
        |                        |                   verify signature
        |                        |                   store.set_decision()
        |                        |                       |
   poll sees not-pending         |                       |
        |                        |                       |
   return True/False

The HITL request is SYNCHRONOUS from the agent's perspective (matches the
existing HumanReviewQueue interface). The webhook server runs separately and
updates a shared ConfirmationStore on button click.

For the InMemoryConfirmationStore the two must run in the SAME PROCESS
(e.g. Flask + agent threading). For multi-process deployments use the
RedisConfirmationStore or implement a Postgres equivalent.

INSTALL
-------
    pip install slack-sdk
    pip install redis              # only if using RedisConfirmationStore

USAGE
-----
    import redis
    from slack_hitl_queue import RedisConfirmationStore, SlackHumanReviewQueue

    store = RedisConfirmationStore(redis.Redis.from_url("redis://localhost:6379/0"))
    hitl = SlackHumanReviewQueue(
        bot_token=SLACK_BOT_TOKEN,
        approval_channel="C0123456",   # channel ID, or "@U0123456" for DM
        store=store,
        timeout_seconds=300,
    )
    agent = SchedulerAgent(client=..., calendar=..., prefs=..., hitl=hitl)

    # Run slack_webhook_server.py in a separate process pointing at the same store.

SLACK APP SETUP
---------------
  1. Create a Slack app at https://api.slack.com/apps
  2. Add OAuth scopes: chat:write, chat:write.public
  3. Install to your workspace; copy Bot User OAuth Token (xoxb-...) -> SLACK_BOT_TOKEN
  4. Enable Interactivity, set Request URL to https://your-host/slack/interactions
  5. Copy the Signing Secret -> SLACK_SIGNING_SECRET
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError as e:
    raise ImportError("slack-sdk not installed. Run: pip install slack-sdk") from e

from scheduler_agent import ActionRisk, HumanReviewQueue

logger = logging.getLogger("scheduler_agent.slack_hitl")


# ============================================================================
# Confirmation Record
# ============================================================================

@dataclass
class PendingConfirmation:
    confirmation_id: str
    action: str
    risk: str
    summary: str
    details: dict[str, Any]
    channel: str
    message_ts: Optional[str] = None
    status: str = "pending"  # pending | approved | denied | expired
    responder: Optional[str] = None  # Slack user ID of approver/denier
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0.0


# ============================================================================
# ConfirmationStore: abstract + two implementations
# ============================================================================

class ConfirmationStore:
    """
    Shared store between the SlackHumanReviewQueue (writer of pending, reader
    of status) and the webhook server (writer of decision).
    """

    def create_pending(self, confirmation: PendingConfirmation) -> None:
        raise NotImplementedError

    def get(self, confirmation_id: str) -> Optional[PendingConfirmation]:
        raise NotImplementedError

    def set_message_ts(self, confirmation_id: str, message_ts: str) -> None:
        raise NotImplementedError

    def set_decision(
        self, confirmation_id: str, approved: bool, responder: str
    ) -> bool:
        """Atomic: only the first decision wins. Returns True on success."""
        raise NotImplementedError

    def mark_expired(self, confirmation_id: str) -> None:
        raise NotImplementedError


class InMemoryConfirmationStore(ConfirmationStore):
    """
    In-process store. Use ONLY when HITL queue and webhook server run in the
    same process (e.g. dev, or single-process deployment with threaded Flask).
    """

    def __init__(self) -> None:
        import threading
        self._store: dict[str, PendingConfirmation] = {}
        self._lock = threading.Lock()

    def create_pending(self, c):
        with self._lock:
            self._store[c.confirmation_id] = c

    def get(self, confirmation_id):
        with self._lock:
            c = self._store.get(confirmation_id)
            if c and c.status == "pending" and c.expires_at and time.time() > c.expires_at:
                c.status = "expired"
            return c

    def set_message_ts(self, confirmation_id, message_ts):
        with self._lock:
            if confirmation_id in self._store:
                self._store[confirmation_id].message_ts = message_ts

    def set_decision(self, confirmation_id, approved, responder):
        with self._lock:
            c = self._store.get(confirmation_id)
            if not c or c.status != "pending":
                return False
            if c.expires_at and time.time() > c.expires_at:
                c.status = "expired"
                return False
            c.status = "approved" if approved else "denied"
            c.responder = responder
            return True

    def mark_expired(self, confirmation_id):
        with self._lock:
            if confirmation_id in self._store:
                self._store[confirmation_id].status = "expired"


class RedisConfirmationStore(ConfirmationStore):
    """
    Production-grade store using Redis. Atomic decision via WATCH/MULTI/EXEC.

    Schema:
      Key:   {prefix}{confirmation_id}      (default prefix: "scheduler:hitl:")
      Value: JSON of PendingConfirmation
      TTL:   matches expires_at; falls back to 600s
    """

    def __init__(
        self,
        redis_client: Any,  # redis.Redis instance
        key_prefix: str = "scheduler:hitl:",
    ) -> None:
        self.r = redis_client
        self.prefix = key_prefix

    def _key(self, cid: str) -> str:
        return f"{self.prefix}{cid}"

    def _ttl(self, c: PendingConfirmation) -> int:
        if c.expires_at:
            return max(60, int(c.expires_at - time.time()) + 60)  # +60s grace
        return 600

    def _save(self, c: PendingConfirmation) -> None:
        self.r.setex(self._key(c.confirmation_id), self._ttl(c), json.dumps(asdict(c)))

    def create_pending(self, c):
        self._save(c)

    def get(self, confirmation_id):
        raw = self.r.get(self._key(confirmation_id))
        if not raw:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        c = PendingConfirmation(**json.loads(raw))
        if c.status == "pending" and c.expires_at and time.time() > c.expires_at:
            c.status = "expired"
        return c

    def set_message_ts(self, confirmation_id, message_ts):
        c = self.get(confirmation_id)
        if not c:
            return
        c.message_ts = message_ts
        self._save(c)

    def set_decision(self, confirmation_id, approved, responder):
        try:
            from redis.exceptions import WatchError
        except ImportError:
            WatchError = Exception  # type: ignore

        key = self._key(confirmation_id)
        with self.r.pipeline() as pipe:
            for _ in range(5):
                try:
                    pipe.watch(key)
                    raw = pipe.get(key)
                    if not raw:
                        pipe.unwatch()
                        return False
                    if isinstance(raw, bytes):
                        raw = raw.decode("utf-8")
                    c = PendingConfirmation(**json.loads(raw))
                    if c.status != "pending":
                        pipe.unwatch()
                        return False
                    if c.expires_at and time.time() > c.expires_at:
                        c.status = "expired"
                        pipe.unwatch()
                        self._save(c)
                        return False
                    c.status = "approved" if approved else "denied"
                    c.responder = responder
                    pipe.multi()
                    pipe.setex(key, self._ttl(c), json.dumps(asdict(c)))
                    pipe.execute()
                    return True
                except WatchError:
                    continue
        return False

    def mark_expired(self, confirmation_id):
        c = self.get(confirmation_id)
        if c:
            c.status = "expired"
            self._save(c)


# ============================================================================
# Webhook payload helper
# ============================================================================

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
    """Apply button-click decisions from a Slack interaction payload."""
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


# ============================================================================
# SlackHumanReviewQueue
# ============================================================================

class SlackHumanReviewQueue(HumanReviewQueue):
    """
    HumanReviewQueue that posts an interactive message to Slack and blocks
    until the user clicks Approve or Deny (or timeout).
    """

    def __init__(
        self,
        bot_token: str,
        approval_channel: str,
        store: ConfirmationStore,
        timeout_seconds: int = 300,
        poll_interval_initial: float = 1.0,
        poll_interval_max: float = 5.0,
    ) -> None:
        self.client = WebClient(token=bot_token)
        self.channel = approval_channel
        self.store = store
        self.timeout = timeout_seconds
        self.poll_initial = poll_interval_initial
        self.poll_max = poll_interval_max

    def request_confirmation(
        self,
        action: str,
        details: dict[str, Any],
        risk: ActionRisk,
        *,
        summary: str = "",
    ) -> bool:
        cid = uuid.uuid4().hex
        summary = summary or details.get("summary") or f"{action}({', '.join(details.keys())})"
        pending = PendingConfirmation(
            confirmation_id=cid,
            action=action,
            risk=risk.value,
            summary=summary,
            details=details,
            channel=self.channel,
            expires_at=time.time() + self.timeout,
        )
        self.store.create_pending(pending)

        try:
            resp = self.client.chat_postMessage(
                channel=self.channel,
                blocks=self._build_blocks(cid, action, risk, summary, details),
                text=f"Scheduler approval needed: {action}",
            )
            self.store.set_message_ts(cid, resp["ts"])
        except SlackApiError as exc:
            logger.error(
                "chat.postMessage failed: %s",
                exc.response.get("error", str(exc)),
            )
            return False

        interval = self.poll_initial
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            time.sleep(interval)
            c = self.store.get(cid)
            if c is None:
                logger.warning("Confirmation %s vanished from store; denying", cid)
                return False
            if c.status == "approved":
                self._update_message(c, approved=True)
                return True
            if c.status == "denied":
                self._update_message(c, approved=False)
                return False
            if c.status == "expired":
                self._update_message(c, expired=True)
                return False
            interval = min(self.poll_max, interval * 1.5)

        self.store.mark_expired(cid)
        c = self.store.get(cid)
        if c:
            self._update_message(c, expired=True)
        logger.warning("Confirmation %s timed out after %ds", cid, self.timeout)
        return False

    def _build_blocks(
        self,
        cid: str,
        action: str,
        risk: ActionRisk,
        summary: str,
        details: dict[str, Any],
    ) -> list[dict[str, Any]]:
        emoji = {"high": "⚠️", "critical": "🚨"}.get(risk.value, "•")
        details_block = json.dumps(details, default=str, indent=2)
        if len(details_block) > 2800:
            details_block = details_block[:2800] + "\n…(truncated)"
        return [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Scheduler approval needed"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*Action:* `{action}`\n"
                        f"*Risk:* {emoji} *{risk.value.upper()}*\n"
                        f"*Summary:* {summary}"
                    ),
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Details:*\n```{details_block}```",
                },
            },
            {
                "type": "actions",
                "block_id": f"confirm_{cid}",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve"},
                        "style": "primary",
                        "value": f"approve:{cid}",
                        "action_id": "scheduler_approve",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Deny"},
                        "style": "danger",
                        "value": f"deny:{cid}",
                        "action_id": "scheduler_deny",
                    },
                ],
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"id: `{cid}` • expires in {self.timeout}s",
                    }
                ],
            },
        ]

    def _update_message(
        self,
        c: PendingConfirmation,
        approved: bool = False,
        expired: bool = False,
    ) -> None:
        if not c.message_ts:
            return
        if expired:
            status_text = "⏱️ *Expired* (no response in time)"
        elif approved:
            status_text = f"✅ *Approved* by <@{c.responder}>"
        else:
            status_text = f"❌ *Denied* by <@{c.responder}>"
        try:
            self.client.chat_update(
                channel=c.channel,
                ts=c.message_ts,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"*Action:* `{c.action}`\n"
                                f"*Risk:* `{c.risk}`\n"
                                f"*Summary:* {c.summary}\n\n"
                                f"{status_text}"
                            ),
                        },
                    },
                    {
                        "type": "context",
                        "elements": [
                            {"type": "mrkdwn", "text": f"id: `{c.confirmation_id}`"}
                        ],
                    },
                ],
                text=f"Confirmation {c.confirmation_id}: {status_text}",
            )
        except SlackApiError as exc:
            logger.warning(
                "chat.update failed for %s: %s",
                c.confirmation_id,
                exc.response.get("error", str(exc)),
            )
