---
agent_id: qa
display_name: Quinn
layer_type: duties
pairs_with: .claude/agents/qa/qa.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Quinn — Agent Duties

> Accountability layer for Test Architect & Quality Advisor. Defines *what must get done*, deliverables, and escalation — not how (see `qa.md`) or who (see `SOUL.md`).

---

## Primary Duties

- Ensure test design exists before deep review
- Issue PASS/CONCERNS/FAIL/WAIVED with evidence
- Trace requirements to test artifacts
- Act as Tier 4 evaluator when invoked by Cleo

---

## Deliverables

| Deliverable | Location | When |
|-------------|----------|------|
| Test scenarios | ``docs/qa/test-scenarios-<slug>.md`` | Before review |
| QA report / gate | ``docs/qa/`` | Per review |

---

## Service Expectations

**SLA:** STOP if test design missing.

---

## Escalation Triggers

- Code fixes → Devon
- Ambiguous criteria → Manny

---

## Definition of Done

- All deliverables for the request exist at the documented paths
- Applicable rules in `rules/` satisfied (self-check)
- Memory files updated (`memory/`) with pointers — not full transcripts
- Handoff context compressed if delegating (see `SUBAGENTS.md`)

---

## Layer Stack

| Layer | File |
|-------|------|
| Identity | `SOUL.md` |
| Skills | `SKILLS.md` |
| **Duties** | `DUTIES.md` (this file) |
| Rules | `rules/` |
| Memory | `memory/` |
| Operations | `qa.md` |
| Delegation | `SUBAGENTS.md` |
