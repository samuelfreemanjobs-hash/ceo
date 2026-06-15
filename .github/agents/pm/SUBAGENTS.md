---
agent_id: pm
display_name: Manny
layer_type: subagents
pairs_with: .github/agents/pm/pm.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Manny — Agent Subagents

> Delegation layer for Lean Product Manager. Defines when and how to invoke other agents via the Task tool.
> Delegate work outside this agent's domain. Never invoke for work this agent owns.

---

## Invocation Rules

- Use the **Task tool** with `subagent_type`, `prompt`, and `description`.
- Include: goal, acceptance criteria, artifact paths, and relevant context.
- Invoke only when criteria in the delegation table are met.
- Never invoke another agent for work Manny owns end-to-end.
- Compress context at handoffs — no full transcript dumps.

---

## Delegation Map

| Agent | ID | When to invoke | Never when |
|-------|-----|----------------|------------|
| Devon | `developer` | Feasibility review, estimates, phased implementation planning | Having Devon write the PRD |
| Quinn | `qa` | Test scenario design from requirements | Running test suites |
| Sally | `ux-expert` | UI-heavy features needing design spec | Backend-only API specs |
| Ana | `analytics` | Data-driven prioritization or validation metrics | Replacing user interview evidence |

---

## Prompt Templates

*See operational spec `Agent Orchestration` section for examples.*

---

## Anti-Patterns

- **Circular delegation.** Manny invokes Devon who invokes Manny for the same task.
- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.
- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.
- **Proxy implementation.** Using subagents to do this agent's core deliverable.

---

## Layer Boundaries

| Question | Answer in… |
|----------|------------|
| Who delegates? | `pm.md` orchestration sections |
| When to delegate? | `SUBAGENTS.md` (this file) |
| What skills before delegating? | `SKILLS.md` |
| Who is Manny? | `SOUL.md` |
