---
agent_id: prepper
display_name: Pepe
layer_type: skills
pairs_with: .gemini/agents/prepper/prepper.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Pepe — Agent Skills

> Capability layer for Project Preparation Specialist. Pairs with `prepper.md` (operations) and `SOUL.md` (identity).
> Pepe uses project analysis and optimization skills — meta-layer only.

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
| `analyze-project-context` | Before any optimization — mandatory | yes |
| `code-quality-check` | Auditing agent/task quality | no |
| `document-project-state` | Project documentation generation | no |

---

## Task Workflows (`.gemini/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| `analyze-project-context.yaml` | Initial project analysis | yes |
| `optimize-agent.yaml` | Agent file optimization | yes |
| `optimize-task.yaml` | Task workflow optimization | yes |
| `optimize-checklist.yaml` | Checklist optimization | yes |

---

## Checklists (`.gemini/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| — | None assigned | — |

---

## Supporting Resources

**Templates** (`.gemini/templates/`):
- `project-analysis-tmpl.yaml` — Analysis report structure

**Data** (`.gemini/data/` or `.ai/data/`):
- `optimization-best-practices.md` — Optimization standards

---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Pepe is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `prepper.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `prepper.md`.
