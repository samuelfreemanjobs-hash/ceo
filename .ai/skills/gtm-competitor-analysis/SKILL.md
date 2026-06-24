---
name: gtm-competitor-analysis
description: Use when comparing public GTM across competitors — positioning, funnels, pricing signals, and user-supplied ad evidence. Invoke for landscape passes, GTM teardowns, white-space analysis, and monitoring checklists with P0 priorities. Not for login-gated scraping or ad claims without user artifacts.
---

# GTM Competitor Analysis

**Used by:** Competition Analyzer (primary), Marketing Director (positioning and offer work)

## Role

Compare **public** go-to-market motion across 3–7 competitors per pass. Output a **landscape**, **GTM teardown**, or **monitoring checklist** with **P0/priority** tags and **next verification** steps.

## Use when

- Positioning an offer or repositioning against the field
- Building or refreshing a **battle card** (GTM lens)
- Deciding **white space** vs. crowded plays
- Standing up ongoing competitive monitoring

## Not for

- Scraping content behind logins or paywalls
- Inventing "their ads say X" without user-supplied artifacts (screenshots, exports, links)
- Trash-talking people — critique **patterns and claims** only
- Deep financial / M&A diligence (use full competitor-profiling instead)

## Scope per competitor

| Dimension | What to capture | Source |
|-----------|-----------------|--------|
| Positioning | Homepage headline, value prop, ICP language | Public site (web_fetch) |
| Funnel signals | Lead magnet, trial path, demo CTA, checkout visibility | Public pages only |
| Pricing signals | Published tiers, "contact sales" opacity, anchoring tier | pricing-teardown skill |
| Ad evidence | Creative themes, offers, hooks | **User-supplied only** |
| Content motion | Blog cadence, changelog, case study focus | Public |

Tag each finding: observation | inference | hypothesis. Apply source-evaluation confidence labels.

## Pass constraints

- **3–7 competitors** per pass — depth beats sprawl
- **Disambiguate** same-name companies in one line (e.g., "Linear (project management, linear.app) vs. Linear (finance, linear.finance)")
- Parallelize independent competitor fetches; synthesize last

## Output types

### 1. GTM landscape

Comparison table: competitors × dimensions (positioning, funnel type, pricing signal, ad themes if artifacts provided).

Close with:
- **White space** — dimensions with weak competitor coverage (inference — labeled)
- **Crowded plays** — dimensions where messaging converges (observation-backed)
- **P0 follow-ups** — what to verify next

### 2. GTM teardown (single competitor)

1. Positioning snapshot (quoted headline + ICP)
2. Funnel map (awareness → conversion path from public pages)
3. Pricing signals (from pricing-teardown or inline)
4. Ad evidence summary (only if user supplied artifacts)
5. Implications for our offer (inference — invite human judgment)

### 3. Monitoring checklist

Prioritized watch list for ongoing tracking:

```markdown
| Priority | Signal | Competitor | Last checked | Next verification | Owner |
|----------|--------|------------|--------------|-------------------|-------|
| P0 | ... | ... | YYYY-MM-DD | [specific action] | — |
| P1 | ... | ... | ... | ... | — |
| P2 | ... | ... | ... | ... | — |
```

**P0:** Could change positioning or pricing decisions this quarter  
**P1:** Material but not urgent  
**P2:** Background monitoring

Every row includes a concrete **next verification** step (URL to re-fetch, artifact to collect, CRM query to run).

## Ad evidence rules

When the user provides ad artifacts (screenshots, Meta Ad Library exports, links):

- Describe **patterns** (offer type, hook structure, CTA) — not subjective mockery
- Quote on-screen text only if legible in the artifact
- Tag **Confirmed** only from the artifact; do not extrapolate to other channels without evidence
- If no artifacts supplied: note "Ad creative: no user artifacts — skip or request"

## Handoffs

See `docs/marketing/HANDOFFS.md`:

- **→ Offer Builder** — when white space implies a new offer angle
- **→ Funnel Map** — when teardown reveals funnel patterns to emulate or counter
- **→ Compliance** — before external battle card copy ships

## Required closing sections

1. Sources (URL, date, tier)
2. Confidence summary (Confirmed / Likely / Unverified)
3. Open questions + next verification steps
4. P0 action list (if monitoring checklist or landscape)

## Output paths

| Deliverable | Path |
|-------------|------|
| GTM landscape | `docs/marketing/research/{category}-gtm-landscape-{date}.md` |
| GTM teardown | `docs/marketing/research/{competitor}-gtm-teardown-{date}.md` |
| Monitoring checklist | `docs/marketing/research/alerts/{category}-monitoring-{date}.md` |
