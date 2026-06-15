# Rules For AI

Every agent in this repository must read this file (and `context/how-we-operate.md`) before acting.

## Required reading order

1. `context/how-we-operate.md`
2. `context/okrs.md`
3. `context/icp.md`
4. `context/mcp-integrations.md` (when using external APIs)
5. `context/learnings.md`
6. Active cycle under `specs/<current-cycle>/`
7. Agent layers: `SOUL.md`, `SKILLS.md`, `SUBAGENTS.md`, `DUTIES.md`, `rules/`, `memory/session-state.yaml`

If required context is missing or stale, stop and surface the gap — do not invent certainty.

## Repository law

- Time-bound work → `specs/<cycle>/`
- Durable knowledge → `context/`
- Raw notes → `inbox/` (then promote or archive)
- Agent session state → `<platform>/agents/<id>/memory/session-state.yaml`
- Cross-agent facts → `.ai/data/kb.yaml` → `orchestration_memory`
- Orchestration audit → `.ai/data/orchestration-log.jsonl`

## How to process `inbox/`

**Automated path:** GitHub Action runs `process-inbox.py process-all` daily.

**Manual/agent path:**

- Decisions → `specs/<cycle>/decision_log.md`
- Status/blockers → cycle `command_center.md` or `03-tasks.md`
- Learnings → `context/learnings.md`
- After processing → `inbox/archive/`

## What AI can do without asking

- Triage and route (Cleo Tier 0–3)
- Create drafts in `specs/` or `context/`
- Process inbox per script rules
- Append orchestration log entries (Tier ≥2)
- Update `memory/session-state.yaml` and kb pointers
- Open cycles via `open-cycle.sh`
- Run validation and CI checks

## What AI must not do without explicit approval

- Execute Tier 4 delivery (requires `*approve` or human confirmation)
- Pepe **Apply** optimizations
- Mark work as approved/final
- Change strategic priorities silently
- Invent metrics, decisions, or customer evidence
- Send external communications (see `rules/outbound-comms.yaml` on CEO)
- Delete historical records

## Approval channels

| Gate | Command / signal |
|------|------------------|
| Tier 4 orchestration | Cleo `*approve` or explicit "approved to proceed" |
| Pepe Apply | Human "APPROVE apply" in chat or PR review |
| Writer sections | Casey checkpoint per `rules/checkpoint-drafts.yaml` |
| External comms | Human only |

## When to escalate

- Contradictory source material
- KPI materially misses plan
- Blocker on critical delivery
- Action changes scope, staffing, budget, or public communication

## Secrets

- Never commit credentials. Use `.env` locally and GitHub Actions secrets in CI.
- See `.env.example` for required variable names.
