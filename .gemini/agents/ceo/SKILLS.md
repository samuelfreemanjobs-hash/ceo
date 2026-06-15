---
agent_id: ceo
display_name: Cleo
layer_type: skills
pairs_with: .gemini/agents/ceo/ceo.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Cleo — Agent Skills

> Capability layer for Executive Orchestrator. Pairs with `ceo.md` (operations) and `SOUL.md` (identity).
> Cleo loads index catalogs and orchestration skills — never domain implementation skills.

---

## Invocation Rules

- Invoke `using-ceo` at session start before responding.
- Read skill files from `.gemini/skills/<name>/SKILL.md` when trigger matches.
- Never load implementation skills (TDD, debugging) — route to Devon instead.
- Consult indexes before Task invocation; do not guess agent capabilities.

---

## Claude Skills (`.gemini/skills/`)

| Skill | Trigger | Required |
|-------|---------|----------|
| `using-ceo` | Session start; skill discovery before any response | yes |
| `dispatching-parallel-agents` | Tier 3 parallel orchestration with independent subtasks | no |
| `subagent-driven-development` | Tier 3–4 multi-agent implementation pipelines | no |
| `verification-before-completion` | Before marking orchestration complete | yes |

---

## Task Workflows (`.gemini/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| — | See operational spec for ad-hoc workflows | — |

---

## Checklists (`.gemini/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| — | None assigned | — |

---

## Supporting Resources

**Indexes** (`.gemini/`):
- `agents.index.yaml`
- `tasks.index.yaml`
- `checklists.index.yaml`
- `data.index.yaml`

**Data** (`.gemini/data/` or `.ai/data/`):
- `.gemini/data/kb.yaml` — Durable orchestration memory and team context
- `.ai/data/orchestration-log.jsonl` — Append-only orchestration observability log

---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Cleo is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `ceo.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `ceo.md`.
