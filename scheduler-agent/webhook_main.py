"""
webhook_main.py
===============
Process B entry point: Slack interactivity webhook for Scheduler HITL.

Run:
    export SLACK_SIGNING_SECRET=...
    export REDIS_URL=redis://localhost:6379/0
    gunicorn -w 4 -b 0.0.0.0:3000 webhook_main:app

Or dev:
    python webhook_main.py
"""

from __future__ import annotations

import logging
import os

import redis

from slack_hitl_queue import RedisConfirmationStore
from slack_webhook_server import create_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

redis_client = redis.Redis.from_url(os.environ["REDIS_URL"])
store = RedisConfirmationStore(redis_client)
app = create_app(store=store)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port, threaded=True)
