---
name: funnel-metrics
description: Use this skill any time the user wants to define, model, project, or interpret funnel metrics. Triggers on "what should I track", "KPIs", "conversion rate", "CAC", "LTV", "payback", "attribution", "benchmarks", "is X conversion rate good", "model this funnel", "what's a good rate for Y", "should I be worried about Z", or whenever numbers enter the conversation. ALWAYS uses the code_execution tool to do the math — never approximate. Provides industry benchmarks with appropriate caveats and forces projections to be grounded in stated assumptions. Use this skill BEFORE making any claim about funnel performance; numbers without code execution are guesses.
---

# Funnel Metrics

This skill is the agent's quantitative brain. It defines metrics precisely, computes projections rigorously, and contextualizes numbers against benchmarks — but never invents numbers.

## When to invoke

- The user asks about metrics, KPIs, or what to track
- The user shares numbers and asks if they're good
- The user wants to model or project funnel performance
- The user asks about CAC, LTV, payback, attribution
- You're in the Measure phase of the funnel workflow
- Any time a number needs to be computed — always use code_execution

## The hard rule: code, don't guess

Every projection, conversion, ratio, or unit-economics calculation MUST go through `code_execution`. Never compute funnel math in your head. Common ways agents get this wrong:

- Multiplying conversion rates in their head ("8% × 35% × 55% ≈ ...") — error-prone
- Approximating LTV/CAC ratios — easy to be 30% off
- Forecasting MRR without compounding correctly — silently wrong

Even simple math should be coded. The user is making business decisions on these numbers.

Bundled scripts (prefer when applicable):

```bash
python funnel-architect/skills/funnel-metrics/scripts/funnel_projection.py --json
python funnel-architect/skills/funnel-metrics/scripts/cac_ltv_calculator.py --cac 500 --ltv 2000 --json
python funnel-architect/skills/funnel-metrics/scripts/cohort_retention.py --json
```

## Core metric definitions (be precise)

Folk definitions of these metrics are wrong often enough that you should restate the precise version before using them.

### CAC (Customer Acquisition Cost)

**Precise definition:** Total fully-loaded marketing and sales spend in a period ÷ new paying customers acquired in that period.

**Common errors:**

- Excluding sales salaries from CAC ("marketing CAC" is a useful sub-metric, but blended CAC is what matters for unit economics)
- Excluding free-tier or trial users who later converted (proper CAC counts the _paying customer_, not the signup)
- Using monthly CAC for a business with a 6-month cycle (mismatched periods)

**Sub-metrics worth tracking:**

- **Paid CAC**: spend on paid channels only ÷ paid-attributed customers
- **Blended CAC**: total spend (paid + content + sales) ÷ all new customers
- **CAC by channel**: spend per channel ÷ attributed conversions per channel (with attribution caveats)

### LTV (Lifetime Value)

**Precise definition (subscription):** Average revenue per customer per period × gross margin × (1 ÷ churn rate).

For a SaaS business: `LTV = ARPU × Gross Margin % ÷ Monthly Churn Rate`

**Common errors:**

- Using revenue instead of gross profit ("LTV" excluding COGS is just lifetime revenue)
- Using logo churn instead of revenue churn (revenue churn is what matters for LTV)
- Computing LTV on a few months of data for a long-lived business (huge variance — use cohort survival curves)
- Pretending NRR > 100% creates infinite LTV (it doesn't — there's still a survival rate)

**Better approach for mature businesses:** cohort-based LTV. Take a 12-month or 24-month-old cohort, sum cumulative gross profit per customer, project forward with current retention curves.

### Payback period

**Precise definition:** Months until gross profit from a customer cohort recovers the CAC spent to acquire them.

**Formula:** `Payback (months) = CAC ÷ (ARPU × Gross Margin %)`

**Targets:**

- SaaS SMB: 12 months or less
- SaaS mid-market: 18 months or less
- SaaS enterprise: 24 months (sometimes longer)
- DTC: 0–3 months (often want first-purchase profitability)

Payback matters more than LTV/CAC for cash-constrained businesses — it determines how fast you can reinvest.

### LTV / CAC ratio

**Targets:**

- Healthy: 3:1 or better
- Excellent: 5:1 or better
- Problematic: < 2:1 (you're paying too much to acquire)
- Suspicious: > 7:1 (you're probably under-investing in growth, or measuring LTV wrong)

**Critical caveat:** LTV/CAC > 5 is sometimes a sign of _under-investment in marketing_, not a sign of efficiency. If your LTV/CAC is 8:1 and growth is slow, the answer is to spend more on acquisition, not celebrate.

### Conversion rates

**Stage-to-stage conversion:** `Stage N+1 entries ÷ Stage N entries` over a fixed cohort window.

Common error: computing conversion rates without cohorting. If your traffic doubled this month and trial-to-paid takes 14 days, the raw monthly conversion will look worse than reality.

Always specify the time window. "Trial-to-paid conversion" is meaningless without "within 30 days of trial start."

### NRR (Net Revenue Retention) and GRR (Gross Revenue Retention)

**GRR:** % of revenue retained from a cohort, excluding upgrades. Always ≤ 100%. **NRR:** GRR + expansion revenue from the cohort. Can exceed 100%.

**Targets (SaaS):**

- NRR > 120%: excellent (best-in-class)
- NRR 110–120%: strong
- NRR 100–110%: solid
- NRR < 100%: leaky bucket, growth depends entirely on new acquisition

NRR is more important than top-line growth rate for valuation in late-stage SaaS. Mention this when relevant.

### Magic number

`Magic Number = (Quarterly Net New ARR × 4) ÷ Prior Quarter S&M Spend`

**Interpretation:**

- < 0.5: poor sales efficiency, slow down spend
- 0.5–1.0: solid, current investment is producing
- > 1.0: invest more, the engine is working

Useful for series A/B SaaS deciding how aggressively to spend.

### Funnel velocity

Time-in-stage, by stage. Useful for diagnosing whether deals are progressing or stalling.

**Why it matters:** a funnel can look healthy by conversion rate while quietly slowing down. If your average time-in-stage doubles, your effective throughput halves.

## Per-stage KPI recommendations by business model

### PLG SaaS

| Stage | Primary KPI | Secondary | Target band |
|-------|-------------|-----------|-------------|
| Acquisition | Visit-to-signup % | Cost per signup | 2–8% organic, 1–4% paid |
| Activation | % of signups hitting activation milestone within 7 days | Time-to-activation | 25–60% depending on product |
| Retention | Week 4 retention of activated users | DAU/MAU, feature adoption | 40%+ at W4 = strong |
| Revenue | Free→paid conversion | ARPU growth | 2–10% free→paid |
| Referral | NPS, viral coefficient (k-factor) | Referral signups | k > 0.4 is meaningful |

### Sales-led B2B SaaS

| Stage | Primary KPI | Secondary | Target band |
|-------|-------------|-----------|-------------|
| Lead | MQLs / month | Cost per MQL | varies wildly by ACV |
| Qualified | SQL conversion %, MQL→SQL time | Disqualification rate | 20–40% MQL→SQL is typical |
| Opportunity | SQL→Opp %, Opp size | Stage velocity | 30–50% SQL→Opp |
| Closed-Won | Win rate, sales cycle length | ACV | 20–35% win rate is typical |
| Expansion | NRR, expansion-driven ARR | Logo retention | NRR 110%+ |

### DTC Ecommerce

| Stage | Primary KPI | Secondary | Target band |
|-------|-------------|-----------|-------------|
| Acquisition | CAC, ROAS | Traffic source mix | ROAS 2.0+ for sustainable scale |
| Consideration | Add-to-cart rate | Time on site, return visits | 5–15% ATC |
| Purchase | Checkout completion %, AOV | Cart abandonment % | 50–70% checkout completion |
| Retention | Repeat purchase rate, 90-day retention | Subscription rate (if applicable) | 20–40% 90d repeat |
| Advocacy | Referral rate, organic share % | UGC volume | 5–15% referral-attributed |

### Services / agencies

| Stage | Primary KPI | Secondary | Target band |
|-------|-------------|-----------|-------------|
| Lead | Qualified leads / month | Cost per lead | varies by ACV |
| Discovery | Discovery call → proposal % | Show-up rate | 40–70% to proposal |
| Proposal | Proposal → close % | Avg deal size | 25–50% close rate |
| Delivery | Project margin, NPS | Time-to-delivery | margin 30–50%+ |
| Retention | Retainer / repeat client % | Referral-sourced % | 30%+ from referrals is good |

## Benchmark library (with confidence ratings)

Benchmarks are slippery — they vary by stage, geography, vertical, and recency. Treat these as starting points; always pair with the user's own data.

**Confidence rating system:**

- 🟢 **High** — broadly consistent across reliable sources
- 🟡 **Medium** — directionally right but high variance
- 🔴 **Low** — wide range, treat as rough heuristic only

### B2B SaaS benchmarks

| Metric | Range | Confidence | Notes |
|--------|-------|------------|-------|
| Landing page → trial signup | 2–8% | 🟡 | Wide variance by ICP narrowness |
| Trial → paid (PLG) | 15–25% | 🟡 | Higher for freemium-to-paid; lower for ungated trial |
| Demo → opportunity | 30–50% | 🟢 | Sales-led B2B |
| MQL → SQL | 20–40% | 🟢 | Depends on lead-scoring strictness |
| SQL → Closed-Won | 15–30% | 🟢 | Stage definitions matter |
| Annual logo churn (SMB) | 10–20% | 🟢 | Higher = problem |
| Annual logo churn (mid-market) | 5–10% | 🟢 | |
| Annual logo churn (enterprise) | 2–7% | 🟢 | |
| NRR (best-in-class) | 120–140% | 🟢 | |
| LTV/CAC | 3–5× | 🟢 | Healthy band |
| Payback period (SMB SaaS) | 6–18mo | 🟢 | Faster = stronger |

### DTC Ecommerce benchmarks

| Metric | Range | Confidence | Notes |
|--------|-------|------------|-------|
| Site visitor → purchase | 1.5–3.5% | 🟢 | Varies by category |
| Add-to-cart rate | 5–12% | 🟡 | |
| Cart abandonment | 65–80% | 🟢 | Industry-wide |
| ROAS (Meta, scaled) | 1.5–3.0× | 🟡 | Highly creative-dependent |
| 90-day repeat purchase rate | 20–35% | 🟡 | |
| Email open rate (post-MPP) | 25–45% | 🟡 | Unreliable since iOS 15 |
| Email click rate | 2–5% | 🟢 | |

### Email marketing benchmarks

| Metric | Range | Confidence | Notes |
|--------|-------|------------|-------|
| Welcome email open rate | 50–70% | 🟢 | Highest-open email type |
| Nurture sequence open rate | 25–40% | 🟡 | |
| B2B cold outbound reply rate | 1–5% | 🟢 | Positive replies, not unsubscribe |
| B2B cold outbound meeting rate | 10–20% of replies | 🟢 | |
| List growth rate (healthy) | 3–5% / month | 🟡 | Pre-decay |

### Paid acquisition benchmarks

| Metric | Range | Confidence | Notes |
|--------|-------|------------|-------|
| Google Search CTR (top position) | 5–15% | 🟢 | Brand vs. non-brand differs |
| Meta CPM | $5–$50 | 🔴 | Highly variable |
| LinkedIn CPM | $30–$150 | 🔴 | Targeting-dependent |
| Meta CTR | 0.5–2% | 🟡 | |
| LinkedIn CTR | 0.3–1.0% | 🟡 | |

These should always be paired with the user's own data if they have it. If they don't, frame as "rough planning ranges" — never as guaranteed performance.

## Attribution

Every attribution model lies in a different way. Choose deliberately.

### First-touch attribution

- **Counts:** the first touchpoint that introduced the customer
- **Lies about:** the mid-funnel work that actually converted them
- **Use when:** evaluating top-of-funnel channel performance, brand awareness, demand creation

### Last-touch attribution

- **Counts:** the touchpoint immediately before conversion
- **Lies about:** all the brand-building that made them search your name in the first place
- **Use when:** evaluating bottom-of-funnel channels, retargeting, demand capture

### Linear attribution

- **Counts:** equal credit to all touchpoints
- **Lies about:** the reality that touchpoints have different weights
- **Use when:** you want a simple, defensible default

### Time-decay attribution

- **Counts:** more credit to recent touches
- **Lies about:** brand-building touches done months before
- **Use when:** longer cycles where late touches matter more

### Data-driven (algorithmic)

- **Counts:** machine-learned weights per touchpoint
- **Lies about:** you don't know how it lies (the black box problem)
- **Use when:** high data volume, mature instrumentation

### The honest answer: marketing mix modeling (MMM) + incrementality tests

- Self-reported attribution surveys ("how did you hear about us?") catch what tracking misses
- Geo-holdout tests prove channel incrementality
- MMM at scale (>$10M annual ad spend) for top-down channel allocation

What to tell the user: pick one primary attribution model for day-to-day decisions, run incrementality tests quarterly, and accept that any attribution number is ±25% directional.

See `references/attribution.md` for details.

## Funnel projection methodology

When projecting funnel volume, follow this process:

### Step 1: List all assumptions explicitly

```python
assumptions = {
    "monthly_visits": 12000,
    "visit_to_signup_rate": 0.08,
    "signup_to_activated_rate": 0.35,
    "activated_to_paid_rate": 0.55,
    "avg_seats_per_team": 5,
    "monthly_revenue_per_seat": 29,
    "monthly_churn_rate": 0.03,
    "cac_per_paid_customer": 180,
}
```

Show the assumptions table. If the user supplied numbers, label them as actuals. If you estimated, label as `[ESTIMATE — validate]`.

### Step 2: Run the projection in code

```python
def project_funnel(a):
    signups = a["monthly_visits"] * a["visit_to_signup_rate"]
    activated = signups * a["signup_to_activated_rate"]
    paid_customers = activated * a["activated_to_paid_rate"]
    new_mrr = paid_customers * a["avg_seats_per_team"] * a["monthly_revenue_per_seat"]
    cac_spend = paid_customers * a["cac_per_paid_customer"]
    arpu = a["avg_seats_per_team"] * a["monthly_revenue_per_seat"]
    ltv = arpu / a["monthly_churn_rate"]  # gross LTV — clarify if margin known
    return {
        "monthly_signups": signups,
        "monthly_activations": activated,
        "monthly_new_paid_customers": paid_customers,
        "monthly_new_mrr": new_mrr,
        "monthly_cac_spend": cac_spend,
        "ltv_per_customer": ltv,
        "ltv_cac": ltv / a["cac_per_paid_customer"],
    }
```

### Step 3: Run sensitivity scenarios

Show how the output changes when key inputs change. Useful framings:

- **Current state:** today's rates
- **Realistic upside:** modest 25–50% improvement on the leakiest stage
- **Aggressive target:** 2× improvement on the leakiest stage
- **Downside:** stage rates drop 20%

The sensitivity table tells the user which inputs matter most. Focus optimization where the sensitivity is highest.

### Step 4: Reality-check the numbers

If a projection says "$10M MRR in 6 months" off a small base, something's wrong. Sanity checks:

- Is the projected growth rate possible given the channel's known scaling characteristics?
- Does the projected CAC stay flat as you scale? (It usually doesn't — CAC inflates at scale.)
- Is there a channel saturation point? (TAM, audience size, competitive dynamics.)

Always include caveats: "This projection assumes channel performance holds at current scale. In practice, paid CACs typically inflate 20–40% when you 2–3× spend."

## Instrumentation plan template

When the user is designing a funnel, specify what to track, where, with what tool. Match instrumentation to business complexity.

### Minimum viable instrumentation (early stage)

- **Analytics:** Google Analytics 4 or Plausible for site analytics
- **Product:** PostHog or Mixpanel for in-product events
- **Email:** native platform analytics (no need for fancy)
- **Ads:** native platform analytics + UTM tagging on every link
- **CRM:** HubSpot Free, Pipedrive, or Attio for pipeline
- **Spreadsheet:** weekly funnel snapshot — manual is fine at this stage

Cost: $0–$500/month. Sufficient through ~$1M ARR.

### Mid-stage instrumentation ($1M–$10M ARR)

Add:

- **Product analytics:** Mixpanel/Amplitude with proper event taxonomy
- **Data warehouse:** Snowflake or BigQuery + Fivetran for source consolidation
- **BI tool:** Looker, Metabase, or Mode for dashboards
- **Attribution:** server-side tracking (CAPI for Meta) + UTM discipline
- **Customer data platform:** Segment if data fragmentation becomes painful

Cost: $2K–$15K/month.

### Late-stage instrumentation ($10M+ ARR)

Add:

- **MMM**: top-down marketing mix modeling
- **Incrementality testing infrastructure:** geo-holdouts, ghost-bidding
- **Advanced experimentation:** Optimizely, Statsig
- **Customer success platform:** Gainsight, Vitally for expansion/retention

Cost: $20K+/month.

Recommend the minimum tier that matches their stage. Pushing late-stage tooling on an early-stage company is a common consulting trap; resist it.

## Output checklist

When this skill is invoked, it should produce:

- [ ] Defined metrics, with precise definitions (not folk versions)
- [ ] Computed numbers via code_execution (never head-math)
- [ ] Assumptions explicitly labeled as actuals vs. estimates
- [ ] Benchmark comparison with confidence ratings
- [ ] Sensitivity analysis on key inputs
- [ ] Recommended instrumentation matched to business stage
- [ ] Honest caveats on attribution and projection limits

## Reference files

- `references/benchmarks-saas.md` — Deep benchmarks by SaaS sub-segment (PLG, sales-led, vertical SaaS)
- `references/benchmarks-ecommerce.md` — DTC benchmarks by category (apparel, beauty, food, etc.)
- `references/benchmarks-services.md` — Services benchmarks by type
- `references/attribution.md` — Full attribution model comparison and decision framework

## Bundled scripts

- `scripts/funnel_projection.py` — Funnel model with sensitivity bands
- `scripts/cac_ltv_calculator.py` — Unit economics with cohort-aware LTV
- `scripts/cohort_retention.py` — Cohort retention curves and survival modeling

## Anti-patterns

- **Head math**: computing without code_execution. Always wrong eventually.
- **Vanity metrics**: reporting impressions, opens, signups without conversion-to-revenue.
- **Benchmark worship**: declaring something good or bad based on a benchmark without context.
- **Single-attribution dogma**: treating last-touch attribution as truth.
- **Forecasting without sensitivity**: a single-point projection is overconfident. Always show ranges.
- **Premature precision**: 4-decimal-place CAC on a 3-month-old business with 12 customers. Round to the right precision.

## Final guidance to the agent

Numbers matter because business decisions ride on them. If you're not certain, say so. If a number is an estimate, mark it. If a benchmark has wide variance, show the range. The user is better served by a directionally-right answer with honest uncertainty than by a precise-looking number that's quietly wrong.

And: when the user says "is X conversion rate good?", don't answer yes/no. Answer: "It's [above/below/in the band of] typical for your business type, but the more useful question is 'good relative to your other stages and your channel mix.' Here's how to interpret it..."
