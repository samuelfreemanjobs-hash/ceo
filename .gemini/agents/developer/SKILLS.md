---
agent_id: developer
display_name: Devon
layer_type: skills
pairs_with: .gemini/agents/developer/developer.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Devon — Agent Skills

> Capability layer for Senior Developer & Architect. Pairs with `developer.md` (operations) and `SOUL.md` (identity).
> Devon loads implementation, debugging, and quality skills before coding.

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
| `test-driven-development` | New features and bugfixes before implementation | yes |
| `systematic-debugging` | Any bug or test failure investigation | yes |
| `verification-before-completion` | Before marking work complete | yes |
| `receiving-code-review` | When processing Quinn's feedback | no |
| `using-git-worktrees` | Isolated feature work when needed | no |
| `use-context7` | Library/framework documentation lookup | no |
| `executing-plans` | Multi-step implementation plans | no |
| `finishing-a-development-branch` | Merge/PR decision after completion | no |

---

## Task Workflows (`.gemini/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| — | See operational spec for ad-hoc workflows | — |

---

## Checklists (`.gemini/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| `code-quality-checklist.yaml` | Pre-commit quality review | yes |
| `openai-sdk-compliance-checklist.yaml` | SDK/orchestration compliance | no |
---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Devon is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `developer.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `developer.md`.
