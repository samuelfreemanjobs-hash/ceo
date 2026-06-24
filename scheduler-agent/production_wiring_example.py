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
    UserPreferences,
)
from slack_hitl_queue import (
    RedisConfirmationStore,
    SlackHumanReviewQueue,
)

_PKG_DIR = Path(__file__).resolve().parent


# ============================================================================
# YOUR PreferencesStore implementation (sketch)
# ============================================================================

class PostgresPreferencesStore(PreferencesStore):
    """
    Sketch -- implement against your actual Postgres schema.
    Schema suggestion:
        CREATE TABLE user_preferences (
            user_id TEXT PRIMARY KEY,
            timezone TEXT NOT NULL DEFAULT 'UTC',
            working_hours_start INT NOT NULL DEFAULT 9,
            working_hours_end INT NOT NULL DEFAULT 17,
            working_days INT[] NOT NULL DEFAULT '{0,1,2,3,4}',
            default_meeting_duration_minutes INT NOT NULL DEFAULT 30,
            buffer_minutes_between_meetings INT NOT NULL DEFAULT 15,
            max_meetings_per_day INT NOT NULL DEFAULT 6,
            focus_block_minimum_minutes INT NOT NULL DEFAULT 90,
            no_meeting_days INT[] NOT NULL DEFAULT '{}',
            preferred_meeting_times TEXT[] NOT NULL DEFAULT '{}'
        );
    """

    def __init__(self, db_conn_string: str):
        self.dsn = db_conn_string

    def get(self, user_id: str) -> UserPreferences:
        raise NotImplementedError("Wire to your Postgres client")

    def update(self, user_id: str, changes: dict) -> UserPreferences:
        raise NotImplementedError("Wire to your Postgres client")


# ============================================================================
# YOUR Google OAuth token lookup (sketch)
# ============================================================================

def get_user_google_refresh_token(user_id: str) -> str:
    """Look up the user's stored Google OAuth refresh token from your secrets store."""
    raise NotImplementedError("Wire to your secrets store")


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

    prefs = PostgresPreferencesStore(os.environ["DATABASE_URL"])

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
    """
    Where should HIGH/CRITICAL confirmations go for this user?
    Common patterns:
      - DM to the user themselves (their Slack user ID prefixed with @)
      - Team channel for shared calendars
      - Per-org #scheduler-approvals channel
    """
    return "@U0123456"


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
#   DATABASE_URL                 -- postgres://... (for PreferencesStore)
# ============================================================================
