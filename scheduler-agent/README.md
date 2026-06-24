# Scheduler Agent

Production-oriented scheduling agent built on Claude tool-use.

## Install

```bash
cd scheduler-agent
pip install -r requirements.txt
```

Requires `ANTHROPIC_API_KEY` for live runs. Unit tests do not need it.

## Smoke demo

```bash
python scheduler_agent.py
```

Uses in-memory calendar + auto-approve HITL (dev only).

## Tests

```bash
pytest tests/ -q
```

## Package layout

| File | Purpose |
|------|---------|
| `scheduler_agent.py` | Agent, executor, backends, tools |
| `meeting_scheduling_skill.md` | Domain skill (loaded into system prompt) |
| `slack_hitl_queue.py` | Slack HITL + ConfirmationStore |
| `slack_webhook_server.py` | Flask interactivity webhook |
| `webhook_main.py` | Process B gunicorn entry point |
| `google_calendar_backend.py` | Google Calendar `CalendarBackend` sketch |
| `production_wiring_example.py` | End-to-end production composition pattern |
| `AGENTS.md` | Agent card |
| `tests/` | Safety + HITL unit tests |

## Production wiring

See [`production_wiring_example.py`](production_wiring_example.py) for the full two-process topology:

- **Process A:** `build_agent_for_user()` → Google Calendar + Postgres prefs + Slack HITL + Redis store
- **Process B:** `webhook_main.py` → same Redis, Slack signature verification

Optional deps: `pip install -r requirements-production.txt`

### Calendar backends

1. Implement `CalendarBackend` → Google Calendar / MS Graph
2. Implement `PreferencesStore` → user prefs DB

### Slack HITL (update / cancel confirmations)

| Component | File | Role |
|-----------|------|------|
| `SlackHumanReviewQueue` | `slack_hitl_queue.py` | Post approve/deny buttons; poll store |
| `ConfirmationStore` | `slack_hitl_queue.py` | Shared decision ledger |
| Webhook server | `slack_webhook_server.py` | Receive Slack button clicks |

**Split deployment (recommended):**

```bash
# Terminal 1 — webhook (public URL for Slack interactivity)
export SLACK_SIGNING_SECRET=...
export REDIS_URL=redis://localhost:6379/0
python3 slack_webhook_server.py

# Terminal 2 — agent with Redis store + Slack queue
export REDIS_URL=redis://localhost:6379/0
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_CHANNEL_ID=C...
```

```python
import redis
from slack_hitl_queue import RedisConfirmationStore, SlackHumanReviewQueue
from scheduler_agent import SchedulerAgent, InMemoryCalendarBackend, InMemoryPreferencesStore

store = RedisConfirmationStore(redis.Redis.from_url(os.environ["REDIS_URL"]))
hitl = SlackHumanReviewQueue(
    bot_token=os.environ["SLACK_BOT_TOKEN"],
    approval_channel=os.environ["SLACK_CHANNEL_ID"],
    store=store,
    timeout_seconds=300,
)
```

**Env vars**

| Variable | Purpose |
|----------|---------|
| `SLACK_SIGNING_SECRET` | Webhook signature verification |
| `SLACK_BOT_TOKEN` | Post HITL messages |
| `SLACK_CHANNEL_ID` | Channel ID for approval prompts (`approval_channel`) |
| `REDIS_URL` | Shared store (agent + webhook) |
| `HITL_POLL_TIMEOUT_SECONDS` | Agent wait for human (default 300) |
| `PORT` | Webhook port (default 3000) |

Replace `AutoApproveReviewQueue` in dev-only smoke runs.
