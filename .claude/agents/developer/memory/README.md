# Devon — Agent Memory

Persistent and session memory for `developer`. **Pointers and structured facts only** — never paste full transcripts.

## Read on activation

- `memory/active-task.yaml` — Current task slug, spec path, acceptance criteria
- `.ai/data/technical-preferences.yaml` — Stack preferences

## Write on progress / handoff / completion

- `memory/active-task.yaml` — Task context and artifact paths
- `memory/verification-log.yaml` — Last verification commands and results

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
