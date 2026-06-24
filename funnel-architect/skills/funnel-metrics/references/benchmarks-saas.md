# SaaS funnel benchmarks

**Confidence key:** Confirmed (multiple sources) | Likely (common heuristics) | Unverified (use sensitivity bands)

Always prefer user's cohort data. Run `web_search` for current year benchmarks before citing.

## PLG self-serve

| Metric | Early stage | Growth | Confidence |
|--------|-------------|--------|------------|
| Visit → signup | 2–6% | 5–12% | Likely |
| Signup → activated | 25–40% | 40–65% | Likely |
| Trial → paid | 10–25% | 25–45% | Likely |
| Monthly logo churn | 3–7% | 1–3% | Likely |
| NRR | 90–105% | 105–130% | Likely |

## Sales-led B2B

| Metric | Range | Confidence |
|--------|-------|------------|
| MQL → SQL | 15–30% | Likely |
| SQL → Opp | 50–70% | Likely |
| Win rate | 20–35% | Likely |
| Sales cycle (mid-market) | 30–90 days | Varies |
| CAC payback | 12–24 mo target | Heuristic |

## Unit economics targets (rule of thumb)

| Metric | Healthy signal |
|--------|----------------|
| LTV:CAC | ≥ 3:1 |
| CAC payback | < 18 months (SMB), < 24 (enterprise) |
| Magic number | > 0.75 (efficient S&M) |

## Scripts

```bash
python funnel-architect/skills/funnel-metrics/scripts/funnel_projection.py --json
python funnel-architect/skills/funnel-metrics/scripts/cac_ltv_calculator.py --cac 500 --ltv 2000 --json
```

## Attribution note

PLG: product analytics (Mixpanel/Amplitude) for activation.  
Sales-led: CRM stage timestamps for pipeline conversion.
