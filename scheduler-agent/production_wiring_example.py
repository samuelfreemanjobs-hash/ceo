"""
production_wiring_example.py
============================
End-to-end example: compose the Scheduler Agent with Google Calendar +
Slack HITL + Redis confirmation store, the way you'd actually deploy it.

This is illustration code, not a runnable script -- you need real credentials
and infrastructure. Read top-to-bottom for the production composition pattern.

DEPLOYMENT TOPOLOGY
-------------------
  Process A (agent worker):
    - SchedulerAgent
    - GoogleCalendarBackend (one per active user)
    - SlackHumanReviewQueue
    - RedisConfirmationStore (client)
    - Your PreferencesStore implementation

  Process B (webhook server):
    - Flask app via slack_webhook_server.create_app()
    - RedisConfirmationStore (client, same Redis instance as A)

  Shared infrastructure:
    - Redis (for ConfirmationStore)
    - Postgres or equivalent (for PreferencesStore)
    - Secrets manager (for Google OAuth tokens, Slack tokens)
"""

from __future__ import annotations

import os
from pathlib import Path

from anthropic import Anthropic

from google_calendar_backend import (
    GoogleCalendarBackend,
    build_service_from_refresh_token,
)
from scheduler_agent import (
    PreferencesStore,
    SchedulerAgent,
)
from slack_hitl_queue import (
    RedisConfirmationStore,
    SlackHumanReviewQueue,
)
from preferences_store import PostgresPreferencesStore, SQLitePreferencesStore

_PKG_DIR = Path(__file__).resolve().parent


# ============================================================================
# PreferencesStore — SQLite (dev) or Postgres (production)
# ============================================================================

def build_preferences_store() -> PreferencesStore:
    """Pick store from env: DATABASE_URL → Postgres, else SQLite."""
    dsn = os.environ.get("DATABASE_URL", "").strip()
    if dsn.startswith("postgres"):
        return PostgresPreferencesStore(dsn)
    db_path = os.environ.get(
        "SCHEDULER_PREFS_DB",
        str(_PKG_DIR / "data" / "preferences.db"),
    )
    return SQLitePreferencesStore(db_path)


# ============================================================================
# Google OAuth token lookup
# ============================================================================

def get_user_google_refresh_token(user_id: str) -> str:
    """
    Look up the user's stored Google OAuth refresh token.

    Dev: set GOOGLE_REFRESH_TOKEN in env (single user).
    Prod: wire to your secrets store / user_tokens table.
    """
    token = os.environ.get("GOOGLE_REFRESH_TOKEN")
    if token:
        return token
    raise RuntimeError(
        f"No Google refresh token for user {user_id}. "
        "Set GOOGLE_REFRESH_TOKEN (dev) or implement secrets lookup."
    )


# ============================================================================
# Process A: Agent factory (per-request)
# ============================================================================

def build_agent_for_user(user_id: str) -> SchedulerAgent:
    """
    Construct a SchedulerAgent bound to one user's calendar and preferences.
    Call this on each incoming request (or pool by user_id with care).
    """
    refresh_token = get_user_google_refresh_token(user_id)
    google_service = build_service_from_refresh_token(
        refresh_token=refresh_token,
        client_id=os.environ["GOOGLE_OAUTH_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
    )
    calendar = GoogleCalendarBackend(
        service=google_service,
        default_calendar_id="primary",
        send_updates="all",
    )

    prefs = build_preferences_store()

    import redis

    redis_client = redis.Redis.from_url(os.environ["REDIS_URL"])
    confirmation_store = RedisConfirmationStore(redis_client)

    hitl = SlackHumanReviewQueue(
        bot_token=os.environ["SLACK_BOT_TOKEN"],
        approval_channel=_approval_channel_for_user(user_id),
        store=confirmation_store,
        timeout_seconds=300,
    )

    return SchedulerAgent(
        client=Anthropic(),
        calendar=calendar,
        prefs=prefs,
        hitl=hitl,
        skill_path=str(_PKG_DIR / "meeting_scheduling_skill.md"),
    )


def _approval_channel_for_user(user_id: str) -> str:
    """Slack channel or @user for HITL confirmations."""
    return os.environ.get("SLACK_APPROVAL_CHANNEL", "@U0123456")


# ============================================================================
# Process A: Request entry point
# ============================================================================

def handle_scheduling_request(user_id: str, user_message: str) -> dict:
    """
    Synchronous request handler. Hook this up to your HTTP/queue/Slack listener.
    """
    agent = build_agent_for_user(user_id)
    trace = agent.run(user_id=user_id, user_message=user_message)
    return {
        "request_id": trace.request_id,
        "response": trace.final_response,
        "error": trace.error,
        "turns": trace.turns,
        "tool_calls": trace.tool_calls,
    }


# ============================================================================
# Process B: Webhook server (see webhook_main.py)
# ============================================================================
#
#     gunicorn -w 4 -b 0.0.0.0:3000 webhook_main:app
#
# Slack interactions URL: https://your-host/slack/interactions
# ============================================================================


# ============================================================================
# Required env vars summary
# ============================================================================
#
#   ANTHROPIC_API_KEY            -- Claude API key
#   GOOGLE_OAUTH_CLIENT_ID       -- Google OAuth app client ID
#   GOOGLE_OAUTH_CLIENT_SECRET   -- Google OAuth app client secret
#   SLACK_BOT_TOKEN              -- xoxb-... (bot token for posting messages)
#   SLACK_SIGNING_SECRET         -- for webhook signature verification (Process B)
#   REDIS_URL                    -- redis://... (shared between A and B)
#   DATABASE_URL                 -- postgres://... (optional; SQLite if unset)
#   SCHEDULER_PREFS_DB           -- SQLite path when DATABASE_URL unset
#   GOOGLE_REFRESH_TOKEN         -- dev single-user refresh token
#   SLACK_APPROVAL_CHANNEL       -- @user or #channel for HITL
# ============================================================================
