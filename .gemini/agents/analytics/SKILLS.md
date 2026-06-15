---
agent_id: analytics
display_name: Ana
layer_type: skills
pairs_with: .gemini/agents/analytics/analytics.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Ana — Agent Skills

> Capability layer for Analytics Specialist. Pairs with `analytics.md` (operations) and `SOUL.md` (identity).
> Ana uses data tasks, checklists, and verification skills — not implementation skills.

---

## Invocation Rules

- Read skill file at `.gemini/skills/<name>/SKILL.md` when trigger matches.
- Required skills (below) run before deliverables.
- Follow skill instructions exactly — they override default behavior.
- Tasks and checklists are procedural skills; load YAML from `.gemini/tasks/` or `.gemini/checklists/`.

---

## Claude Skills (`.gemini/skills/`)

| Skill | Trigger | Required |
|-------|---------|----------|
| `verification-before-completion` | Before publishing analysis report | yes |
| `systematic-debugging` | Data pipeline or calculation anomalies | no |

---

## Task Workflows (`.gemini/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| `analyze-campaign-performance.yaml` | Full campaign analysis workflow | yes |

---

## Checklists (`.gemini/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| `analytics-checklist.yaml` | Pre-delivery report validation | yes |

---

## Supporting Resources

**Templates** (`.gemini/templates/`):
- `analytics-report-tmpl.yaml` — Standard report structure

**Data** (`.gemini/data/` or `.ai/data/`):
- `calculation-best-practices.yaml` — Metric calculation standards

---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Ana is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `analytics.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `analytics.md`.
