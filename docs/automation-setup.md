# Automation Setup

Quick reference for reaching ~80% automated operations.

## One-time local setup

```bash
# Enable GitAgent metadata pre-commit hook
git config core.hooksPath .githooks

# Optional: copy env template
cp .env.example .env
```

## Key scripts

| Script | Purpose |
|--------|---------|
| `.ai/utils/process-inbox.py` | Promote inbox → specs |
| `.ai/utils/open-cycle.sh` | Open new spec cycle |
| `.ai/utils/orchestration-log.py` | Append/tail/summary JSONL log |
| `.ai/utils/validate-agents.py` | CI agent + team-brain validation |
| `.ai/utils/sync-platform-agents.py` | Copy `.claude/agents` → codex/gemini |
| `.ai/utils/inject-metadata.py` | Layer frontmatter checksums |

## GitHub Actions

| Workflow | Schedule | Purpose |
|----------|----------|---------|
| `ci.yml` | PR + push to main | Validate agents, fixtures |
| `automation-daily.yml` | 14:00 UTC daily | Process inbox |
| `automation-weekly.yml` | Mon 15:00 UTC | Analytics pipeline trigger |
| `trigger-ceo-triage.yml` | Issue label `ceo-triage` | Cleo triage hook |

## Cleo commands (approval)

- `*tier` — dry-run triage
- `*plan` — execution plan (confirm Tier 3–4)
- `*approve` — human gate for Tier 4
- `*log` — orchestration history

## Regenerate indexes after agent changes

```bash
.claude/utils/generate-indexes.sh
.github/utils/generate-indexes.sh
.codex/utils/generate-indexes.sh
.gemini/utils/generate-indexes.sh
```

Or sync codex/gemini trees first:

```bash
python3 .ai/utils/sync-platform-agents.py
```

## Measuring 80%

See `docs/automation-gap-analysis.md` for definition. Track:

- % inbox items promoted without human
- % PRs passing `validate-agents.py` on first run
- Tier distribution in `orchestration-log.jsonl` summary
