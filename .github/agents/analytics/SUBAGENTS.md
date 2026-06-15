---
agent_id: analytics
display_name: Ana
layer_type: subagents
pairs_with: .github/agents/analytics/analytics.md
last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review
---

# Ana — Agent Subagents

> Delegation layer for Analytics Specialist. Defines when and how to invoke other agents via the Task tool.
> Delegate work outside this agent's domain. Never invoke for work this agent owns.

---

## Invocation Rules

- Use the **Task tool** with `subagent_type`, `prompt`, and `description`.
- Include: goal, acceptance criteria, artifact paths, and relevant context.
- Invoke only when criteria in the delegation table are met.
- Never invoke another agent for work Ana owns end-to-end.
- Compress context at handoffs — no full transcript dumps.

---

## Delegation Map

| Agent | ID | When to invoke | Never when |
|-------|-----|----------------|------------|
| Devon | `developer` | Data pipeline bugs, ETL fixes, custom analytics tooling | Interpreting campaign results Ana can compute |
| Mark | `marketer` | Strategy recommendations from analysis findings | Replacing Ana's metric calculations |

---

## Prompt Templates

### Pipeline fix

```
Task(subagent_type="developer", prompt="Analytics pipeline incomplete data. File: {path}. Issue: {issue}. Fix extraction logic.", description="Fix data pipeline")
```

### Strategy handoff

```
Task(subagent_type="marketer", prompt="Analysis complete: {report_path}. Key finding: {finding}. Develop optimization strategy.", description="Marketing strategy from data")
```

---

## Anti-Patterns

- **Circular delegation.** Ana invokes Devon who invokes Ana for the same task.
- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.
- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.
- **Proxy implementation.** Using subagents to do this agent's core deliverable.

---

## Layer Boundaries

| Question | Answer in… |
|----------|------------|
| Who delegates? | `analytics.md` orchestration sections |
| When to delegate? | `SUBAGENTS.md` (this file) |
| What skills before delegating? | `SKILLS.md` |
| Who is Ana? | `SOUL.md` |
