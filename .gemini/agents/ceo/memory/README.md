# Cleo — Agent Memory

Persistent and session memory for `ceo`. **Pointers and structured facts only** — never paste full transcripts.

## Read on activation

- `.ai/data/kb.yaml` — Team context, orchestration_memory, session_state
- `.ai/data/orchestration-log.jsonl` — Recent orchestration history
- `agents.index.yaml` — Agent capabilities

## Write on progress / handoff / completion

- `memory/session-state.yaml` — Current tier, pattern, request_id, pending approvals
- `memory/handoffs.yaml` — Compressed handoff queue between agents
- `.ai/data/kb.yaml#orchestration_memory` — Durable decisions only — not transcripts
- `.ai/data/orchestration-log.jsonl` — Append-only event log

## Files in this directory

| File | Purpose |
|------|---------|
| `session-state.yaml` | Ephemeral session context (reset each session) |
| `README.md` | This guide |

Additional files are created by the agent during work. Commit session-state only when it contains durable pointers worth preserving.

## Shared team memory (all agents)

- `.ai/data/kb.yaml` — cross-agent durable context
- `starter-kits/team-brain/context/` — OKRs, ICP, operating model (when adopted)
- `starter-kits/team-brain/inbox/` — raw notes awaiting processing

## Hygiene

- Summarize before writing; max ~50 lines per memory file
- Use YAML for structured state
- Cleo orchestrations also log to `.ai/data/orchestration-log.jsonl`
