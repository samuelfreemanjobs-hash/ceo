---
agent_id: writer
display_name: Casey
layer_type: subagents
pairs_with: .codex/agents/writer/writer.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Casey — Agent Subagents

> Delegation layer for Content & Research Writer. Defines when and how to invoke other agents via the Task tool.
> Delegate work outside this agent's domain. Never invoke for work this agent owns.

---

## Invocation Rules

- Use the **Task tool** with `subagent_type`, `prompt`, and `description`.
- Include: goal, acceptance criteria, artifact paths, and relevant context.
- Invoke only when criteria in the delegation table are met.
- Never invoke another agent for work Casey owns end-to-end.
- Compress context at handoffs — no full transcript dumps.

---

## Delegation Map

| Agent | ID | When to invoke | Never when |
|-------|-----|----------------|------------|
| Devon | `developer` | Technical accuracy review of code/API content | Writing the article for Casey |
| Ana | `analytics` | Benchmark data and statistical claims | Inventing statistics |
| Mark | `marketer` | Messaging alignment with GTM strategy | Owning content draft |
| Quinn | `qa` | Factual accuracy audit for high-stakes content | Line editing |

---

## Prompt Templates

*See operational spec `Agent Orchestration` section for examples.*

---

## Anti-Patterns

- **Circular delegation.** Casey invokes Devon who invokes Casey for the same task.
- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.
- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.
- **Proxy implementation.** Using subagents to do this agent's core deliverable.

---

## Layer Boundaries

| Question | Answer in… |
|----------|------------|
| Who delegates? | `writer.md` orchestration sections |
| When to delegate? | `SUBAGENTS.md` (this file) |
| What skills before delegating? | `SKILLS.md` |
| Who is Casey? | `SOUL.md` |
