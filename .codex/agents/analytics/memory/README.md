# Ana — Agent Memory

Persistent and session memory for `analytics`. **Pointers and structured facts only** — never paste full transcripts.

## Read on activation

- `memory/data-sources.yaml` — Configured primary/secondary files and metrics
- `.ai/data/calculation-best-practices.yaml` — Calculation standards

## Write on progress / handoff / completion

- `memory/data-sources.yaml` — Session data source configuration
- `memory/last-report.yaml` — Pointer to latest report path

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
