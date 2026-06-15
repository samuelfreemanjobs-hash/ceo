---
agent_id: prepper
display_name: Pepe
layer_type: subagents
pairs_with: .gemini/agents/prepper/prepper.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Pepe — Agent Subagents

> Delegation layer for Project Preparation Specialist. Defines when and how to invoke other agents via the Task tool.
> Delegate work outside this agent's domain. Never invoke for work this agent owns.

---

## Invocation Rules

- Use the **Task tool** with `subagent_type`, `prompt`, and `description`.
- Include: goal, acceptance criteria, artifact paths, and relevant context.
- Invoke only when criteria in the delegation table are met.
- Never invoke another agent for work Pepe owns end-to-end.
- Compress context at handoffs — no full transcript dumps.

---

## Delegation Map

| Agent | ID | When to invoke | Never when |
|-------|-----|----------------|------------|
| Devon | `developer` | Validate technical preferences from analysis | Feature implementation |
| Manny | `pm` | Product context for task/agent alignment | Writing optimized agent files without approval |
| Quinn | `qa` | Quality standards for checklist optimization | Applying changes without user [1] Apply |

---

## Prompt Templates

*See operational spec `Agent Orchestration` section for examples.*

---

## Anti-Patterns

- **Circular delegation.** Pepe invokes Devon who invokes Pepe for the same task.
- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.
- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.
- **Proxy implementation.** Using subagents to do this agent's core deliverable.

---

## Layer Boundaries

| Question | Answer in… |
|----------|------------|
| Who delegates? | `prepper.md` orchestration sections |
| When to delegate? | `SUBAGENTS.md` (this file) |
| What skills before delegating? | `SKILLS.md` |
| Who is Pepe? | `SOUL.md` |
