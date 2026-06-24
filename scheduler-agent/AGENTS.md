# Scheduler Agent

**ID:** `scheduler-agent` · **Model:** sonnet · **Codename:** `scheduler-agent-v0.1`

**Purpose:** Preference-aware calendar scheduling via Claude tool-use — find slots, book meetings, reschedule/cancel with fail-closed HITL on destructive ops.

**Runtime:** Python — [`scheduler_agent.py`](scheduler_agent.py)  
**Skill:** [`meeting_scheduling_skill.md`](meeting_scheduling_skill.md)

---

## Architecture

Single-agent + rich tools (not multi-agent). Appropriate for a **high-control, single-domain** task per Anthropic's agent framework.

| Component | Role |
|-----------|------|
| `SchedulerAgent` | Claude agentic loop |
| `SchedulerToolExecutor` | Tool dispatch + safety gates |
| `CalendarBackend` | Pluggable calendar API |
| `PreferencesStore` | User scheduling prefs |
| `HumanReviewQueue` | HITL for update/cancel |

## When to use

- "Find time for…" / "Book a meeting with…"
- Reschedule or cancel with human confirmation
- Preference-aware availability (working hours, buffers, caps)

## Not for

- Email triage, general assistant tasks
- Production calendar writes without wiring real backends + HITL

## Safety

- `create_event` requires prior `check_conflicts` or `find_availability` on exact slot
- `update_event` / `cancel_event` require approved `request_confirmation` (fail-closed)
- All datetimes ISO 8601 with explicit offset
- `AgentTrace` records every tool call

## Tools (9)

`get_user_preferences` · `list_events` · `get_event` · `find_availability` · `check_conflicts` · `create_event` · `request_confirmation` · `update_event` · `cancel_event`

## Quick start

```bash
cd scheduler-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python scheduler_agent.py   # smoke demo (in-memory backends)
pytest tests/ -q            # unit tests (no API key)
```

## Integration (before production)

1. Implement `CalendarBackend` → Google Calendar / MS Graph
2. Implement `PreferencesStore` → user prefs DB
3. Replace `AutoApproveReviewQueue` → Slack / email / web UI

## Invoke (orchestrators)

```
Task → subagent_type: scheduler-agent
```

Or programmatically:

```python
from anthropic import Anthropic
from scheduler_agent import SchedulerAgent, InMemoryCalendarBackend, InMemoryPreferencesStore, AutoApproveReviewQueue

agent = SchedulerAgent(
    client=Anthropic(),
    calendar=InMemoryCalendarBackend(),
    prefs=InMemoryPreferencesStore(),
    hitl=AutoApproveReviewQueue(),  # dev only
)
trace = agent.run("u_123", "Book 30 min with alex@ tomorrow morning")
```
