# MCP & Integration Configuration

**Last updated:** 2026-06-15

Document of connected systems for agent automation. Credentials live in `.env` / platform secrets — never in git.

## Connected (when authenticated in Cursor)

| System | Use | Primary agents | Read / Write |
|--------|-----|----------------|--------------|
| GitHub | PRs, issues, Actions | Cleo, Devon, Quinn | Read + Write (PR) |
| Supabase | DB, auth (if project linked) | Devon | Read + Write (migrations gated) |
| Slack | Triggers, approvals (optional) | Cleo | Read; Write needs approval |
| Notion | Tasks, docs (optional) | Manny, Casey | Read; Write needs approval |
| Zapier MCP | Cross-app automation | Cleo | Per Zapier safety model |
| Firecrawl | Research, web fetch | Casey, Ana | Read |

## Data files (no API required)

| Path | Agent | Schedule |
|------|-------|----------|
| `data/analytics/campaign-weekly.csv` | Ana | Weekly export or sample |
| `.ai/data/orchestration-log.jsonl` | Cleo | Every Tier ≥2 run |
| `.ai/data/kb.yaml` | All | Session handoffs |

## Environment variables

See `.env.example`. Map to:

- **Cursor:** Settings → MCP → authenticate each server
- **GitHub Actions:** Repository secrets for scheduled jobs
- **Local scripts:** `source .env` (gitignored)

## Trigger → Cleo flow

1. **GitHub:** `workflow_dispatch` or `issues` labeled `ceo-triage` → comment with plan
2. **Slack:** Message in `#ceo-agent` (document webhook URL in secrets)
3. **Manual:** `*plan` in any agent session

## Adding a new integration

1. Authenticate MCP server in Cursor
2. Add row to this table
3. Update agent `SKILLS.md` trigger if specialist-owned
4. Add secret name to `.env.example`
5. If scheduled, extend `.github/workflows/automation-weekly.yml`
