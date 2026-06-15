---
agent_id: marketer
display_name: Mark
layer_type: subagents
pairs_with: .github/agents/marketer/marketer.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Mark — Agent Subagents

> Delegation layer for Marketing Strategist. Defines when and how to invoke other agents via the Task tool.
> Delegate work outside this agent's domain. Never invoke for work this agent owns.

---

## Invocation Rules

- Use the **Task tool** with `subagent_type`, `prompt`, and `description`.
- Include: goal, acceptance criteria, artifact paths, and relevant context.
- Invoke only when criteria in the delegation table are met.
- Never invoke another agent for work Mark owns end-to-end.
- Compress context at handoffs — no full transcript dumps.

---

## Delegation Map

| Agent | ID | When to invoke | Never when |
|-------|-----|----------------|------------|
| Ana | `analytics` | Campaign performance data, ROI, CAC trends | Inventing metrics |
| Casey | `writer` | Blog posts, copy, content series from strategy | Technical documentation |
| Sally | `ux-expert` | Landing page or conversion UX design | Implementing pages in code |
| Manny | `pm` | Product positioning tied to roadmap decisions | Engineering task breakdown |

---

## Prompt Templates

*See operational spec `Agent Orchestration` section for examples.*

---

## Anti-Patterns

- **Circular delegation.** Mark invokes Devon who invokes Mark for the same task.
- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.
- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.
- **Proxy implementation.** Using subagents to do this agent's core deliverable.

---

## Layer Boundaries

| Question | Answer in… |
|----------|------------|
| Who delegates? | `marketer.md` orchestration sections |
| When to delegate? | `SUBAGENTS.md` (this file) |
| What skills before delegating? | `SKILLS.md` |
| Who is Mark? | `SOUL.md` |
