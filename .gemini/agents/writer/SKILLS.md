---
agent_id: writer
display_name: Casey
layer_type: skills
pairs_with: .gemini/agents/writer/writer.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Casey — Agent Skills

> Capability layer for Content & Research Writer. Pairs with `writer.md` (operations) and `SOUL.md` (identity).
> Casey uses research and writing workflow skills — delegates technical validation.

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
| `create-deep-research-prompt` | Deep research setup | no |

---

## Task Workflows (`.gemini/tasks/`)

| Task | Purpose | Required |
|------|---------|----------|
| `warmstart-article.yaml` | STORM warmstart research | yes |
| `synthesize-article.yaml` | Multi-perspective synthesis | yes |
| `research-topic.yaml` | Topic research workflow | yes |
| `optimize-content.yaml` | SEO/readability optimization | no |

---

## Checklists (`.gemini/checklists/`)

| Checklist | Purpose | Required |
|-----------|---------|----------|
| `content-quality-checklist.yaml` | Pre-publish content QA | yes |
---

## Layer Boundaries

| Layer | File | Owns |
|-------|------|------|
| Identity | `SOUL.md` | Who Casey is |
| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |
| Operations | `writer.md` | How to execute work |
| Delegation | `SUBAGENTS.md` | When to invoke other agents |

Skills answer *what to load*; they do not replace operational procedure in `writer.md`.
