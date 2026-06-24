---
name: funnel-metrics
description: Use when defining, modeling, projecting, or interpreting funnel metrics. Triggers on "KPIs", "conversion rate", "CAC", "LTV", "payback", "benchmarks", "model this funnel". Always use code_execution for math — never approximate in prose.
---

# Funnel Metrics

**Used by:** Funnel Architect (Phase 5 — Measure, Phase 6 — Optimize)

## Core definitions (precise)

| Metric | Definition |
|--------|------------|
| CAC | Total sales+marketing cost / new customers (specify blended vs paid) |
| LTV | Cohort-based revenue per customer over horizon — not ARPU × guessed lifespan |
| Payback | Months to recover CAC from gross margin |
| NRR / GRR | Net / gross revenue retention |
| Magic number | Net new ARR / prior quarter S&M spend |

## Per-stage KPIs

Recommend one **primary** KPI per stage + one guardrail. Tie to buyer state, not channel vanity metrics.

## Benchmarks

Cite via web_search or label **heuristic**. Include confidence: Confirmed / Likely / Unverified.

## Funnel projection

Use `scripts/funnel_projection.py` or code_execution:

```
visits × stage_rates → signups → activated → paid → MRR
```

Run **sensitivity** on the weakest-known stage rate.

## Attribution caveats

Note when first-touch / last-touch / linear mislead for the user's motion.

## Instrumentation plan template

| Event | Tool | Stage |
|-------|------|-------|
| | GA4 / Mixpanel / HubSpot / Salesforce | |

## Bundled scripts

- `scripts/funnel_projection.py` — projection + sensitivity + optional Monte Carlo
- `scripts/cac_ltv_calculator.py` — CAC/LTV/payback verdicts
- `scripts/cohort_retention.py` — naive vs projected retention comparison

## References

- `references/benchmarks-saas.md`
- `references/benchmarks-ecommerce.md`
- `references/benchmarks-services.md`
- `references/attribution.md`
