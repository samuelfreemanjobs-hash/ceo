# Ecommerce funnel benchmarks

Verify category via `web_search` — fashion, consumables, and electronics differ widely.

## Standard ecommerce funnel

| Stage | Heuristic CVR | Confidence |
|-------|---------------|------------|
| Session → PDP | 40–70% | Likely |
| PDP → add to cart | 8–15% | Likely |
| Cart → purchase | 50–70% | Likely |
| 90-day repeat | 15–35% | Varies |

## Paid social (DTC)

| Metric | Range | Confidence |
|--------|-------|------------|
| ROAS (mature account) | 2–4× | Varies |
| CPA vs AOV | CPA < 30–40% AOV early target | Heuristic |
| MER (total revenue / total ad spend) | Track blended | Best practice |

## Email

| Metric | Range |
|--------|-------|
| Welcome series revenue | 20–40% of email revenue |
| Abandoned cart recovery | 5–15% of abandoned carts |

## Subscription add-on

| Metric | Heuristic |
|--------|-----------|
| Subscribe rate at checkout | 10–25% |
| Subscription churn monthly | 5–10% early |

## Scripts

Use `funnel_projection.py` with custom stage names: `session, pdp, atc, purchase`.

## Guardrails

- Contribution margin after returns/shipping
- Don't optimize ROAS while LTV data is immature
