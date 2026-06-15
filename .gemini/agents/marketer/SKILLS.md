---
agent_id: marketer
display_name: Mark
layer_type: skills
pairs_with: .gemini/agents/marketer/marketer.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Mark — Agent Skills

> Capability layer for Marketing Strategist. Pairs with `marketer.md` (operations) and `SOUL.md` (identity).
> Mark uses GTM and content strategy skills — delegates data and copy.

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
| `developing-marketing-strategy` | GTM and channel strategy work | yes |
| `brainstorming` | Campaign ideation | no |

---

## Task Workflows (`.gemini/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| `create-marketing-strategy.yaml` | Full marketing strategy workflow | yes |
| `optimize-content.yaml` | Content performance optimization | no |

---

## Checklists (`.gemini/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| — | None assigned | — |
---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Mark is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `marketer.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `marketer.md`.
