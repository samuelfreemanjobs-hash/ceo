# Pepe — Agent Memory

Persistent and session memory for `prepper`. **Pointers and structured facts only** — never paste full transcripts.

## Read on activation

- `memory/audit-log.yaml` — Prior optimization decisions
- `memory/progress-checklist.yaml` — Resume state for *resume-optimization

## Write on progress / handoff / completion

- `memory/audit-log.yaml` — Append-only optimization history
- `memory/progress-checklist.yaml` — Checklist position and pending items
- `memory/analysis-snapshot.yaml` — Last project analysis summary

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
