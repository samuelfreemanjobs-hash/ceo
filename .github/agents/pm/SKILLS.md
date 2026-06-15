---
agent_id: pm
display_name: Manny
layer_type: skills
pairs_with: .github/agents/pm/pm.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Manny — Agent Skills

> Capability layer for Lean Product Manager. Pairs with `pm.md` (operations) and `SOUL.md` (identity).
> Manny uses planning, brainstorming, and spec skills — not implementation.

---

## Invocation Rules

- Read skill file at `.claude/skills/<name>/SKILL.md` when trigger matches.
- Required skills (below) run before deliverables.
- Follow skill instructions exactly — they override default behavior.
- Tasks and checklists are procedural skills; load YAML from `.claude/tasks/` or `.claude/checklists/`.

---

## Claude Skills (`.github/skills/`)

| Skill | Trigger | Required |
|-------|---------|----------|
| `brainstorming` | New feature ideation before spec | yes |
| `speckit-specify` | Structured feature specifications | no |
| `speckit-plan` | Complex features needing implementation plan | no |
| `writing-plans` | Multi-step delivery plans | no |
| `create-deep-research-prompt` | Market/tech research prompts | no |

---

## Task Workflows (`.github/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| `create-task.yaml` | Developer-ready task definitions | yes |
| `create-doc.yaml` | PRDs and product documents | yes |
| `create-deep-research-prompt.yaml` | Research prompt generation | no |

---

## Checklists (`.github/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| `pm-context-checklist.yaml` | Before any spec — mandatory | yes |
---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Manny is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `pm.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `pm.md`.
