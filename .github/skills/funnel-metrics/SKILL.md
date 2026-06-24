---
name: funnel-metrics
description: Use this skill any time the user wants to define, model, project, or interpret funnel metrics. Triggers on "what should I track", "KPIs", "conversion rate", "CAC", "LTV", "payback", "attribution", "benchmarks", "is X conversion rate good", "model this funnel", "what's a good rate for Y", "project revenue", "ICE score", "unit economics", or whenever numbers enter the conversation. Always uses code_execution or bundled scripts for math — never approximate in prose. Provides industry benchmarks with confidence ratings. Do NOT use for writing copy or picking channels without a metrics question.
---

# Funnel Metrics

**Phase:** Measure (5), Optimize (6) · **Invoke any phase** when numbers appear

## Purpose

Define precise KPIs, **compute** projections via code_execution, cite benchmarks honestly, and produce instrumentation + ICE test prioritization.

## Math policy (non-negotiable)

1. **Every calculated number** → `code_execution` or bundled script
2. **Exception:** Restating user-provided numbers verbatim
3. **No head math** in prose ("~800 conversions" without running code)
4. List **assumptions** before every projection

### Bundled scripts

```bash
# Funnel projection + sensitivity
python funnel-architect/skills/funnel-metrics/scripts/funnel_projection.py \
  --visits 12000 --signup 0.08 --activate 0.35 --pay 0.55 --seats 5 --price 29 --json

# CAC / LTV / payback
python funnel-architect/skills/funnel-metrics/scripts/cac_ltv_calculator.py \
  --cac 500 --ltv 2000 --margin 0.8 --json

# Cohort retention comparison
python funnel-architect/skills/funnel-metrics/scripts/cohort_retention.py --json
```

## Core metric definitions (precise)

| Metric | Definition | Common mistake |
|--------|------------|----------------|
| **CAC** | Total S&M cost / new customers in period | Blended vs paid not specified |
| **Paid CAC** | Paid media only / customers from paid | Ignoring creative + agency |
| **LTV** | Cohort revenue per customer over horizon | ARPU × guessed lifespan (wrong) |
| **Gross margin LTV** | LTV × gross margin % | Using revenue LTV for payback |
| **Payback** | Months to recover CAC from gross margin | Using revenue not margin |
| **NRR** | (Start + expansion - churn) / Start | Logo vs revenue confusion |
| **GRR** | Retention excluding expansion | |
| **Magic number** | Net new ARR / prior quarter S&M | |
| **Contribution margin** | Revenue - variable costs per unit | |

## Per-stage KPI design

For each funnel stage from `funnel-frameworks`:

| Element | Rule |
|---------|------|
| Primary KPI | One conversion or outcome metric |
| Guardrail | Quality metric (e.g., lead quality, churn) |
| Buyer state tie | KPI reflects state change, not vanity |
| Current vs target | Both columns in stage table |

### Examples by motion

| Motion | Stage | Primary KPI | Guardrail |
|--------|-------|-------------|-----------|
| PLG | Activation | Signup → activated % | Time to first value |
| PLG | Revenue | Trial → paid % | Refund rate |
| Sales-led | MOFU | MQL → SQL % | SAL disqualify rate |
| Sales-led | BOFU | Win rate | Discount % |
| DTC | Purchase | Session → order % | Return rate |

## Benchmark library usage

Load references by business model:

| Reference | Use |
|-----------|-----|
| `references/benchmarks-saas.md` | PLG, sales-led B2B |
| `references/benchmarks-ecommerce.md` | DTC |
| `references/benchmarks-services.md` | Agencies, consultancies |
| `references/attribution.md` | Instrumentation + attribution choice |

### Confidence ratings (always attach)

| Label | Meaning |
|-------|---------|
| **Confirmed** | Multiple sources or user's cohort data |
| **Likely** | Common industry heuristic |
| **Unverified** | Estimate — use sensitivity bands |

Run `web_search` for current-year benchmarks before citing Confirmed.

## Funnel projection workflow

1. **Inputs:** Top-of-funnel volume + stage conversion rates (user or benchmark)
2. **Compute:** Volume at each stage via code_execution
3. **Revenue:** `paid_users × ARPU` or `orders × AOV` — show formula
4. **Sensitivity:** Vary weakest-known rate ±25–50%
5. **Delta narrative:** Current vs target in dollars (MRR, revenue, pipeline $)

### Projection output template

```markdown
## Projected unit economics
**Assumptions:** [list]
**Current path:** [from code_execution]
**Target path:** [from code_execution]
**Delta:** [$ or %]
**Sensitivity:** Varying [stage] from X to Y changes [outcome] by Z
```

## Attribution guidance

Recommend **one primary model** + why. See `references/attribution.md`.

| Motion | Primary | Warning |
|--------|---------|---------|
| PLG | Product analytics cohorts | Don't trust last-touch alone |
| Sales-led | CRM opportunity source | Marketing-influenced field |
| DTC | MER + platform ROAS | Platform over-claims |

## Instrumentation plan template

| Event / KPI | Tool | Stage | Owner |
|-------------|------|-------|-------|
| Page view, signup | GA4 / Mixpanel | Acquire | |
| Activation event | Product analytics | Activate | |
| Trial → paid | Billing + product | Revenue | |
| Stage timestamp | HubSpot / Salesforce | MOFU/BOFU | |

Minimum viable: **one tool per layer** (web, product, CRM/billing).

## ICE scoring (Optimize phase)

**ICE = Impact × Confidence × Ease** (each 1–10)

| Test | Impact | Confidence | Ease | ICE | Order |
|------|--------|------------|------|-----|-------|
| | | | | | |

**Impact:** Effect on primary metric if it wins  
**Confidence:** Evidence it will work  
**Ease:** Time/cost to ship  

Top 3 tests only — resist laundry lists.

## Audit mode (existing funnel)

When user provides stage table:

1. Identify **largest absolute leak** (biggest volume drop)
2. Identify **largest relative leak** (worst conversion rate)
3. Prioritize fix where **absolute × improvability** is highest
4. Compute lift scenarios via code_execution

## Do not use when

- User only wants headline rewrite → `conversion-copywriting`
- User only wants channel pick → `channel-playbooks`
- No numbers requested and none implied → skip until Measure phase

## Anti-patterns

| Mistake | Fix |
|---------|-----|
| Head-math in chat | code_execution |
| Fake precision (3.847%) | Round + show assumptions |
| Benchmark without source | web_search or label heuristic |
| LTV = ARPU/churn blindly | Cohort-based or flag assumption |
| ICE without scores | Numeric 1–10 each dimension |

## Coordination

- **From funnel-frameworks:** Stage boundaries = KPI boundaries
- **From channel-playbooks:** CPL/CAC targets per channel
- **To conversion-copywriting:** Cohort stats copy must verify
- **Optimize:** Re-run projections after proposed tests

## Quality checklist

- [ ] All calculations via code_execution/scripts
- [ ] Assumptions listed explicitly
- [ ] Benchmarks have confidence rating
- [ ] Sensitivity on weakest stage
- [ ] Instrumentation table complete
- [ ] Top 3 ICE tests with numeric scores

## References

- `references/benchmarks-saas.md`
- `references/benchmarks-ecommerce.md`
- `references/benchmarks-services.md`
- `references/attribution.md`

## Scripts

- `scripts/funnel_projection.py` — projection + sensitivity + optional Monte Carlo
- `scripts/cac_ltv_calculator.py` — CAC/LTV/payback verdicts
- `scripts/cohort_retention.py` — retention curve comparison
