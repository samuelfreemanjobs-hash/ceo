# Manny — Agent Memory

Persistent and session memory for `pm`. **Pointers and structured facts only** — never paste full transcripts.

## Read on activation

- `memory/active-spec.yaml` — Current PRD/task in progress
- `.claude/checklists/pm-context-checklist.yaml` — Context gate

## Write on progress / handoff / completion

- `memory/active-spec.yaml` — Spec path, validation evidence, open questions
- `memory/backlog-pointers.yaml` — Links to prioritized docs

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
