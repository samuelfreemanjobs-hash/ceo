---
agent_id: ux-expert
display_name: Sally
layer_type: skills
pairs_with: .gemini/agents/ux-expert/ux-expert.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Sally — Agent Skills

> Capability layer for UX Expert. Pairs with `ux-expert.md` (operations) and `SOUL.md` (identity).
> Sally uses design doc and frontend prompt skills — delegates build and requirements.

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
| `brainstorming` | Design exploration before spec | no |

---

## Task Workflows (`.gemini/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| `create-doc.yaml` | UX spec documents | yes |
| `generate-ai-frontend-prompt.yaml` | AI UI generation prompts | yes |
| `execute-checklist.yaml` | Checklist-driven design review | no |

---

## Checklists (`.gemini/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| — | None assigned | — |
---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Sally is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `ux-expert.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `ux-expert.md`.
