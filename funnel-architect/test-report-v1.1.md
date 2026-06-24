# Funnel Architect — Test Report v1.1

**Round 2:** 5 prompts · regression check + new edge cases

## Regression prompts

| # | Retest | v1 issue | Expected |
|---|--------|----------|----------|
| 1 | Ambiguous brief | #1 discovery skip | Agent asks minimum 5 inputs |
| 2 | PLG activation | #4 generic output | Specific email + ICE tests |
| 3 | Funnel projection | #2 head-math | code_execution or script output |

## New edge cases

| # | Case | Expected behavior |
|---|------|-------------------|
| 4 | $9/mo consumer app + outbound request | Decline outbound; recommend PLG channels |
| 5 | Multi-goal brief (signup + expansion + referral) | Propose 2–3 funnels, not one Frankenstein |

## Results

_To be filled on live eval run._

## Scripts verified

```bash
python funnel-architect/skills/funnel-metrics/scripts/funnel_projection.py --json
python funnel-architect/skills/funnel-metrics/scripts/cac_ltv_calculator.py --cac 500 --ltv 2000 --json
python funnel-architect/skills/funnel-metrics/scripts/cohort_retention.py --actual 1.0,0.85,0.72 --json
```
