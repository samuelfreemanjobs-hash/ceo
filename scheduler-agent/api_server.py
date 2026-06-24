"""
api_server.py
=============
Minimal HTTP API for scheduling requests (Process A ingress).

Usage:
    export ANTHROPIC_API_KEY=...
    # Dev — in-memory calendar:
    python api_server.py

    # Production — wire production_wiring_example.build_agent_for_user:
    export SCHEDULER_PRODUCTION=1
    python api_server.py

POST /schedule
    {"user_id": "u1", "message": "Book 30 min with alex@co.com Thursday afternoon"}

GET /health
"""

from __future__ import annotations

import os

from flask import Flask, jsonify, request

app = Flask(__name__)


def _build_agent(user_id: str):
    if os.environ.get("SCHEDULER_PRODUCTION") == "1":
        from production_wiring_example import build_agent_for_user
        return build_agent_for_user(user_id)

    from anthropic import Anthropic
    from scheduler_agent import (
        AutoApproveReviewQueue,
        InMemoryCalendarBackend,
        InMemoryPreferencesStore,
        SchedulerAgent,
    )
    from pathlib import Path

    pkg = Path(__file__).resolve().parent
    return SchedulerAgent(
        client=Anthropic(),
        calendar=InMemoryCalendarBackend(),
        prefs=InMemoryPreferencesStore(),
        hitl=AutoApproveReviewQueue(),
        skill_path=str(pkg / "meeting_scheduling_skill.md"),
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/schedule")
def schedule():
    body = request.get_json(silent=True) or {}
    user_id = body.get("user_id", "default")
    message = body.get("message", "").strip()
    if not message:
        return jsonify({"error": "message required"}), 400

    agent = _build_agent(user_id)
    trace = agent.run(user_id=user_id, user_message=message)
    return jsonify({
        "request_id": trace.request_id,
        "response": trace.final_response,
        "error": trace.error,
        "turns": trace.turns,
        "tool_calls": trace.tool_calls,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
