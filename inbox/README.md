# inbox/

Landing zone for raw notes. Nothing should live here permanently.

## Naming

```text
yyyy-mm-dd-type-short-description.md
```

Examples: `2026-06-15-daily-standup.md`, `2026-06-15-feature-idea-notifications.md`

## Processing

**Automated (daily):** GitHub Action runs:

```bash
python3 .ai/utils/process-inbox.py process-all
```

**Manual:**

```bash
python3 .ai/utils/process-inbox.py list
python3 .ai/utils/process-inbox.py promote 2026-06-15-feature-idea.md --title "User notifications"
python3 .ai/utils/process-inbox.py archive stale-note.md
```

Promoted items create `specs/<date>-<slug>/` and move the source file to `inbox/archive/`.
