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
| `AGENTS.md` | Agent card |
| `tests/test_executor.py` | Safety policy unit tests |

## Environment

| Variable | Default |
|----------|---------|
| `SCHEDULER_MODEL` | `claude-sonnet-4-6` |
| `SCHEDULER_MAX_TURNS` | `20` |
| `SCHEDULER_MAX_TOKENS` | `4096` |
| `SCHEDULER_SKILL_PATH` | `meeting_scheduling_skill.md` (package dir) |

## Production wiring

See [AGENTS.md](AGENTS.md) integration section — replace in-memory backends before real calendar writes.
