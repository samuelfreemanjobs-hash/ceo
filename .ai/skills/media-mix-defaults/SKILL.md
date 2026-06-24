---
name: media-mix-defaults
description: Default channel mix and test budgets for early-stage B2B services GTM. Override with marketing-plan-current-quarter when set.
---

# Media Mix Defaults — B2B Services (early stage)

Use when `media-agent` plans spend and no custom mix exists in quarterly plan.

## Default mix (pre-scale)

| Channel | % budget | Role | Notes |
|---------|----------|------|-------|
| Organic / content | 40% | Trust + SEO | LP, LinkedIn posts |
| Warm outbound | 30% | Conversion | Network, partners |
| Paid test | 20% | Learning | Small LinkedIn/Google tests only |
| Events / community | 10% | Optional | Podcasts, communities |

## Test budget guardrails

- Max $500/campaign until LP conversion baseline exists
- Kill test if CPA > 3× target sprint gross margin
- No competitor keyword bidding without legal review

## Channel economics (starter assumptions)

| Channel | Typical CPC/CPM | When to use |
|---------|-----------------|-------------|
| LinkedIn organic | Time | Primary for P1 |
| LinkedIn paid | $8–15 CPC | After LP live |
| Google search | $15–40 CPC | Branded + high-intent only |

## Handoff

- Funnel design → `funnel-architect`
- Ad copy → `ad-agent` or `writer`
- LP → `lp-agent`
