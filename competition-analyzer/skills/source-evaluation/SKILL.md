---
name: source-evaluation
description: Use when assessing reliability, recency, and bias of any source during competitive intelligence work. Apply silently during research; surface source quality when it changes conclusions or when the user asks about evidence strength.
---

# Source Evaluation

**Used by:** Competition Analyzer (every investigation)

## Source tiers

| Tier | Examples | Default weight |
|------|----------|----------------|
| **Primary** | Competitor's website, pricing page, SEC filings, official blog, product docs | High — but biased toward self-narrative |
| **Secondary** | G2/Capterra reviews, analyst reports (Gartner, Forrester), reputable press, earnings calls | High when independent |
| **Tertiary** | Forums, Reddit, social posts, job listings, Glassdoor | Signal only — triangulate |
| **First-party internal** | Your sales call notes, win/loss data, customer mentions | Highest when available |

## Reliability checklist

For each source, score:

- **Independence:** Does the source have incentive to mislead?
- **Recency:** When was it published / last updated? Flag if >90 days for pricing/positioning.
- **Specificity:** Vague marketing vs. concrete claim?
- **Corroboration:** Can a second source confirm?

## Confidence mapping

| Evidence pattern | Label |
|------------------|-------|
| Primary + secondary agree | Confirmed |
| Single reliable secondary | Likely |
| Primary only (competitor claim) | Likely (note bias) |
| Single tertiary | Unverified |
| Inference without direct evidence | Unverified (label as hypothesis) |

## Bias flags

- **Self-reported metrics** from competitor → Likely at best
- **Anonymous reviews** → triangulate; never sole source for quantitative claims
- **SEO comparison pages** ("Us vs Them") → both sides biased
- **Outdated screenshots** in third-party content → verify against live site

## Staleness rules

| Data type | Stale after |
|-----------|-------------|
| Pricing | 30 days (verify live page) |
| Product features | 60 days |
| Leadership / funding | 90 days unless no signals |
| Strategic positioning | 90 days |

When stale, re-verify or downgrade confidence and note in output.

## Citation format

```
[Source title](URL) — retrieved YYYY-MM-DD — Tier: Primary|Secondary|Tertiary — Note: one-line reliability
```
