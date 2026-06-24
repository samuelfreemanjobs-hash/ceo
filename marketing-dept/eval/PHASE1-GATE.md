# Phase 1 — Ship copy + compliance

Phase 1 handles **Type B content requests** only: subject lines, captions, headlines, rewrites. No campaigns, media, or research until Phase 2+.

## Quick start (wired for repo skills)

```bash
cd marketing-dept
pip install -e .
export ANTHROPIC_API_KEY=...

# Phase 1 director — copy + compliance + brand memory from repo skills
marketing-director --phase1 "Write three subject lines for our weekly newsletter about the new analytics dashboard."
```

Or in Python:

```python
from anthropic import Anthropic
from marketing_director import create_phase1_director

director = create_phase1_director(Anthropic())
result = director.handle_request("Write three subject lines for our newsletter.")
print(result["deliverable"])
```

## What's wired in Phase 1

| Component | Implementation |
|-----------|----------------|
| **copy_agent** | Real Claude calls + `style_guide_lookup` → `brand-voice` skill |
| **compliance_agent** | Real Claude calls + `rules_engine` → `prohibited-claims-and-disclaimers` skill |
| **brand_memory_read** | Loads skills from `.github/skills/` (or `.claude/`, `.gemini/`) |
| **human_review_handler** | Writes `docs/marketing/decisions/review-<id>.json` |
| **Slack escalation** | Set `SLACK_WEBHOOK_URL` env var (optional) |

Director only sees: `copy_agent`, `compliance_agent`, `brand_memory_read`, `request_human_review`.

## Before first real run

1. Fill in skill templates (at minimum `brand-voice` and `prohibited-claims-and-disclaimers`)
2. Set `ANTHROPIC_API_KEY`
3. Optional: `export SLACK_WEBHOOK_URL=https://hooks.slack.com/...`

## Deployment gate (live API)

```bash
cd eval
python3 test_harness.py --mode full --case failure_unsubstantiated_stat --report reports/phase1-gate.html
```

**Pass criteria:** structural assertions pass + `fabrication` judge `overall_pass: true`.

Run via GitHub Actions: workflow **Marketing Director Eval**, mode `full`, case `failure_unsubstantiated_stat` (requires `ANTHROPIC_API_KEY` secret).

## Not wired yet (Phase 2+)

| Stub | Wire when |
|------|-----------|
| `web_search`, `internal_db_query` | Research agent goes live |
| `analytics_query` | Analytics integrations (GA4, Mixpanel) |
| Notion / Drive / vector DB | Replace `repo_brand_memory_loader` when skills move off-repo |

## Environment variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Required for live runs |
| `SLACK_WEBHOOK_URL` | Optional human review notifications |

## Model tiers

Edit `ModelConfig` in `director.py` or pass a custom instance to `create_phase1_director` if you subclass. Defaults:

- Director: `claude-opus-4-7`
- Copy: `claude-sonnet-4-6`
- Compliance: `claude-haiku-4-5-20251001`
