# Getting started — Marketing & Scheduler stack

One runbook to go from zero to first outputs. **Customize** [BRAND-PROFILE.md](BRAND-PROFILE.md) first (5 minutes).

---

## Prerequisites

| Requirement | Used by |
|-------------|---------|
| `ANTHROPIC_API_KEY` | All agents |
| Cursor or Task tool with agent cards | Prompt agents |
| Python 3.11+ | `marketing-dept`, `scheduler-agent` |

```bash
# One-time setup
./scripts/setup.sh
cp .env.example marketing-dept/.env   # add ANTHROPIC_API_KEY
```

---

## Path A — Marketing copy (fastest, Python)

**Best for:** email subject lines, ad copy, compliance check without full campaign.

```bash
cd marketing-dept
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
marketing-director --phase1 "Write three subject lines for our launch email."
```

Uses built-in **CopyAgent** + **ComplianceAgent** + brand skills.

---

## Path B — Services GTM chain (Cursor / agents)

**Best for:** offer → proposal → landing page for a productized service.

### 0. Customize brand (once)

Edit [BRAND-PROFILE.md](BRAND-PROFILE.md) — company name, ICP, voice, prohibited claims.

Mirror into `offer-builder/USER_PROFILE.md` for offer sessions.

### 1. Offer Builder

1. Fill `offer-builder/briefs/ACTIVE.md` from `offer-builder/templates/BRIEF.md`
2. Run: `@offer-builder/AGENTS.md` + brief
3. Save → `docs/marketing/offers/{slug}-offer-{date}.md`

**Example:** [offers/example-discovery-sprint-offer-2026-06-24.md](offers/example-discovery-sprint-offer-2026-06-24.md)

### 2. Proposal Agent

1. Fill `proposal-agent/briefs/ACTIVE.md` — offer path + client name
2. Run: `@proposal-agent/AGENTS.md` + brief
3. Save → `docs/marketing/proposals/{slug}-proposal-{date}.md`

**Example:** [proposals/example-discovery-sprint-proposal-2026-06-24.md](proposals/example-discovery-sprint-proposal-2026-06-24.md)

### 3. LP Agent

1. Fill `lp-agent/briefs/ACTIVE.md` — offer + proposal paths + CTA URL
2. Run: `@lp-agent/AGENTS.md` + brief
3. Save → `docs/marketing/landing-pages/{slug}-lp-{date}.md`
4. Route to compliance before publish

**Example:** [landing-pages/example-discovery-sprint-lp-2026-06-24.md](landing-pages/example-discovery-sprint-lp-2026-06-24.md)

Pre-filled briefs for the example chain: `offer-builder/briefs/ACTIVE.md` → `proposal-agent/` → `lp-agent/`

### CEO / Morgan routing

| Intent | Agent |
|--------|-------|
| Full campaign | `marketing-director` |
| Competitive intel | `competition-analyzer` |
| Funnel design | `funnel-architect` |
| Offer design | `offer-builder` |
| Client proposal | `proposal-agent` |
| Landing page | `lp-agent` |
| Enterprise CRM quote | `offer-director` |

Handoff contracts: [HANDOFFS.md](HANDOFFS.md)

---

## Path C — Scheduler agent

### Dev smoke (no Google/Slack)

```bash
cd scheduler-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python scheduler_agent.py
```

**HTTP API (optional):**

```bash
python api_server.py
# POST http://localhost:8080/schedule  {"user_id":"u1","message":"..."}
```

Uses in-memory calendar + auto-approve HITL.

### Production wiring

```bash
docker compose up -d          # Redis + Postgres
cp scheduler-agent/.env.example scheduler-agent/.env
pip install -r requirements-production.txt
```

| Process | Command | Purpose |
|---------|---------|---------|
| A (agent) | Your worker calling `production_wiring_example.build_agent_for_user` | Schedule meetings |
| B (webhook) | `gunicorn -w 4 -b 0.0.0.0:3000 webhook_main:app` | Slack approve/deny |

Env vars: see `scheduler-agent/.env.example`

**Dev without Postgres:** omit `DATABASE_URL` — uses SQLite at `scheduler-agent/data/preferences.db`

---

## Output directories

| Path | Agent |
|------|-------|
| `docs/marketing/offers/` | Offer Builder |
| `docs/marketing/proposals/` | Proposal Agent |
| `docs/marketing/landing-pages/` | LP Agent |
| `docs/marketing/research/` | Competition Analyzer |
| `docs/marketing/funnels/` | Funnel Architect |
| `docs/marketing/campaigns/` | Marketing Director |

---

## What's still manual / external

| Item | Notes |
|------|-------|
| Google OAuth consent flow | Obtain refresh tokens per user; set `GOOGLE_REFRESH_TOKEN` for dev |
| Slack app setup | Bot token + signing secret + interactions URL |
| Enterprise CRM tools | `offer-director` MCP integrations pending |
| Legal sign-off | Review `prohibited-claims-and-disclaimers` for your industry |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent not in CEO index | Run `.github/utils/generate-indexes.sh` |
| Phase 1 fails brand check | Fill `BRAND-PROFILE.md` |
| Scheduler tests fail on Google import | `pip install -r requirements-production.txt` or tests skip automatically |
| LP price mismatch | Offer §6 is source of truth — re-run offer-builder |

---

## Next steps

1. Replace example offer with your real flagship service
2. Run Scout (`competition-analyzer`) for positioning input
3. Connect scheduler to Google Calendar + Slack for team use
