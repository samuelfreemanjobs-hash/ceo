---
agent_id: qa
display_name: Quinn
layer_type: skills
pairs_with: .codex/agents/qa/qa.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Quinn — Agent Skills

> Capability layer for Test Architect & Quality Advisor. Pairs with `qa.md` (operations) and `SOUL.md` (identity).
> Quinn uses quality, review, and verification skills — advisory not implementation.

---

## Invocation Rules

- Read skill file at `.codex/skills/<name>/SKILL.md` when trigger matches.
- Required skills (below) run before deliverables.
- Follow skill instructions exactly — they override default behavior.
- Tasks and checklists are procedural skills; load YAML from `.codex/tasks/` or `.codex/checklists/`.

---

## Claude Skills (`.codex/skills/`)

| Skill | Trigger | Required |
|-------|---------|----------|
| `requesting-code-review` | Structured review dispatch | yes |
| `verification-before-completion` | Before issuing gate verdict | yes |
| `systematic-debugging` | Root-cause analysis for failures | no |

---

## Task Workflows (`.codex/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| `test-scenarios.yaml` | Test design before review — required | yes |
| `create-qa-report.yaml` | Formal QA report generation | yes |
| `nfr-assess.yaml` | Non-functional requirements assessment | no |
| `review-task.yaml` | Task-level review workflow | no |

---

## Checklists (`.codex/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| `code-quality-checklist.yaml` | Code review depth | yes |
| `openai-sdk-compliance-checklist.yaml` | Orchestration compliance | no |
---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Quinn is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `qa.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `qa.md`.
