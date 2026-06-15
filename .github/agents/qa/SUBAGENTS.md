---
agent_id: qa
display_name: Quinn
layer_type: subagents
pairs_with: .github/agents/qa/qa.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Quinn — Agent Subagents

> Delegation layer for Test Architect & Quality Advisor. Defines when and how to invoke other agents via the Task tool.
> Delegate work outside this agent's domain. Never invoke for work this agent owns.

---

## Invocation Rules

- Use the **Task tool** with `subagent_type`, `prompt`, and `description`.
- Include: goal, acceptance criteria, artifact paths, and relevant context.
- Invoke only when criteria in the delegation table are met.
- Never invoke another agent for work Quinn owns end-to-end.
- Compress context at handoffs — no full transcript dumps.

---

## Delegation Map

| Agent | ID | When to invoke | Never when |
|-------|-----|----------------|------------|
| Devon | `developer` | FAIL/CONCERNS requiring code fixes | Fixing code directly |
| Manny | `pm` | Missing or ambiguous acceptance criteria | Rewriting requirements without user |

---

## Prompt Templates

*See operational spec `Agent Orchestration` section for examples.*

---

## Anti-Patterns

- **Circular delegation.** Quinn invokes Devon who invokes Quinn for the same task.
- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.
- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.
- **Proxy implementation.** Using subagents to do this agent's core deliverable.

---

## Layer Boundaries

| Question | Answer in… |
|----------|------------|
| Who delegates? | `qa.md` orchestration sections |
| When to delegate? | `SUBAGENTS.md` (this file) |
| What skills before delegating? | `SKILLS.md` |
| Who is Quinn? | `SOUL.md` |
