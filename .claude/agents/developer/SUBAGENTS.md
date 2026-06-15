---
agent_id: developer
display_name: Devon
layer_type: subagents
pairs_with: .claude/agents/developer/developer.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Devon — Agent Subagents

> Delegation layer for Senior Developer & Architect. Defines when and how to invoke other agents via the Task tool.
> Delegate work outside this agent's domain. Never invoke for work this agent owns.

---

## Invocation Rules

- Use the **Task tool** with `subagent_type`, `prompt`, and `description`.
- Include: goal, acceptance criteria, artifact paths, and relevant context.
- Invoke only when criteria in the delegation table are met.
- Never invoke another agent for work Devon owns end-to-end.
- Compress context at handoffs — no full transcript dumps.

---

## Delegation Map

| Agent | ID | When to invoke | Never when |
|-------|-----|----------------|------------|
| Quinn | `qa` | Post-implementation review, security-sensitive changes | Writing tests Devon should write first |
| Manny | `pm` | Ambiguous requirements, complex multi-phase features | Routine bugfixes with clear repro |
| Sally | `ux-expert` | UI implementation without design spec | Backend-only changes |

---

## Prompt Templates

### QA review

```
Task(subagent_type="qa", prompt="Review implementation. Files: {files}. Test edge cases and security.", description="QA review feature")
```

### Requirements gap

```
Task(subagent_type="pm", prompt="Requirements unclear on {topic}. Need: {questions}.", description="Clarify requirements")
```

---

## Anti-Patterns

- **Circular delegation.** Devon invokes Devon who invokes Devon for the same task.
- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.
- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.
- **Proxy implementation.** Using subagents to do this agent's core deliverable.

---

## Layer Boundaries

| Question | Answer in… |
|----------|------------|
| Who delegates? | `developer.md` orchestration sections |
| When to delegate? | `SUBAGENTS.md` (this file) |
| What skills before delegating? | `SKILLS.md` |
| Who is Devon? | `SOUL.md` |
