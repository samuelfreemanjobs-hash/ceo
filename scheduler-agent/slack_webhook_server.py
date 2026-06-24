"""
slack_webhook_server.py
=======================
Flask webhook server that receives Slack interaction payloads (button clicks)
and updates the ConfirmationStore so the SchedulerAgent's polling loop can
read the decision.

Run as a separate process (or alongside the agent in the same process if
using InMemoryConfirmationStore). Slack expects a response within 3 seconds,
so the handler does the minimum work: verify signature, parse, update store,
return 200. The polling loop in SlackHumanReviewQueue picks up the decision.

INSTALL
-------
    pip install flask slack-sdk
    pip install redis              # if using RedisConfirmationStore

ENV VARS
--------
    SLACK_SIGNING_SECRET    Slack app signing secret (REQUIRED for verification)
    PORT                    Webhook port (default 3000)
    REDIS_URL               Optional; if set, uses RedisConfirmationStore

SLACK APP CONFIG
----------------
  - Interactivity & Shortcuts: ON
  - Request URL: https://your-domain/slack/interactions
  - Bot Token Scopes: chat:write, chat:write.public

USAGE (standalone)
------------------
    SLACK_SIGNING_SECRET=... python slack_webhook_server.py

USAGE (embedded in existing Flask app)
--------------------------------------
    from slack_webhook_server import register_slack_interactions

    app = Flask(__name__)
    register_slack_interactions(app, store=my_store, signing_secret="...")
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

try:
    from flask import Flask, jsonify, request
except ImportError as e:
    raise ImportError("flask not installed. Run: pip install flask") from e

try:
    from slack_sdk.signature import SignatureVerifier
except ImportError as e:
    raise ImportError("slack-sdk not installed. Run: pip install slack-sdk") from e

from slack_hitl_queue import (
    ConfirmationStore,
    InMemoryConfirmationStore,
    process_slack_interaction_payload,
)

logger = logging.getLogger("scheduler_agent.slack_webhook")


def register_slack_interactions(
    app: Flask,
    store: ConfirmationStore,
    signing_secret: str,
    path: str = "/slack/interactions",
) -> None:
    """Register the Slack interactions route on an existing Flask app."""
    verifier = SignatureVerifier(signing_secret=signing_secret)

    @app.route(path, methods=["POST"])
    def slack_interactions():
        if not verifier.is_valid_request(
            body=request.get_data().decode("utf-8"),
            headers=dict(request.headers),
        ):
            logger.warning("Invalid Slack signature on %s", path)
            return jsonify({"error": "invalid_signature"}), 401

        payload_str = request.form.get("payload")
        if not payload_str:
            return jsonify({"error": "missing_payload"}), 400
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            return jsonify({"error": "invalid_payload"}), 400

        process_slack_interaction_payload(payload, store)
        return ("", 200)


def _build_store_from_env() -> ConfirmationStore:
    """Build the appropriate store based on env config."""
    redis_url = os.environ.get("REDIS_URL")
    if redis_url:
        try:
            import redis
        except ImportError as e:
            raise ImportError("redis not installed. Run: pip install redis") from e
        from slack_hitl_queue import RedisConfirmationStore

        client = redis.Redis.from_url(redis_url)
        logger.info("Using RedisConfirmationStore at %s", redis_url)
        return RedisConfirmationStore(client)
    logger.warning(
        "REDIS_URL not set; using InMemoryConfirmationStore. "
        "This only works if the agent runs in the SAME process as this server."
    )
    return InMemoryConfirmationStore()


def create_app(store: ConfirmationStore | None = None) -> Flask:
    """Factory for a standalone webhook server."""
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
    if not signing_secret:
        raise RuntimeError("SLACK_SIGNING_SECRET environment variable is required")

    store = store or _build_store_from_env()
    app = Flask(__name__)
    register_slack_interactions(app, store=store, signing_secret=signing_secret)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    app = create_app()
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port, threaded=True)
