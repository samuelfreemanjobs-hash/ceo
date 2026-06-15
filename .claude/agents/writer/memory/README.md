# Casey — Agent Memory

Persistent and session memory for `writer`. **Pointers and structured facts only** — never paste full transcripts.

## Read on activation

- `memory/active-draft.yaml` — Topic, audience, outline, current section

## Write on progress / handoff / completion

- `memory/active-draft.yaml` — Draft path, sources collected, approval status
- `memory/source-index.yaml` — Sources used in current piece

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
