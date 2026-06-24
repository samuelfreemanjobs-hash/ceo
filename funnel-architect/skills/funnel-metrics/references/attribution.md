# Attribution models

When recommending instrumentation, explain **what each model optimizes for** and how it lies.

## Models

| Model | Credits | Best when | Lies when |
|-------|---------|-----------|-----------|
| First-touch | First interaction | Brand awareness ROI | Ignores nurture |
| Last-touch | Last interaction | Simple BOFU | Ignores awareness |
| Linear | Equal all touches | Long consideration | Treats spam clicks equal |
| Time-decay | More to recent | Short cycles | Wrong for early influencer |
| Data-driven | ML-weighted | Volume + clean data | Black box, needs scale |
| Product-led (internal) | Activation events | PLG | Misses paid assist |

## Recommendations by motion

| Motion | Primary | Secondary |
|--------|---------|-----------|
| PLG | Product analytics cohorts | Paid channel assisted signup |
| Sales-led | CRM opportunity source + influence fields | Marketing influenced pipeline |
| DTC | MER + platform ROAS | Post-purchase survey |

## Instrumentation minimum

| Tool | Track |
|------|-------|
| GA4 | Sessions, key events, source/medium |
| Product analytics | Activation, retention cohorts |
| CRM | Stage timestamps, source |
| Ads platforms | Conversions (with off-line import for B2B) |

## Funnel Spec output

Include one paragraph: **"For your motion, we recommend X as primary because Y. Do not use Z alone because..."**

## Common failure

Reporting last-touch Facebook ROAS while SEO + email did the education — cuts wrong channel.
