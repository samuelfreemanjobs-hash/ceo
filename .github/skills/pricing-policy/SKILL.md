---
name: pricing-policy
description: Apply the company's pricing policy — rate cards, segment discounts, strategic adders, approval thresholds, and floor prices. Use whenever building, validating, or revising priced line items in a customer-facing offer, or when explaining a price to internal stakeholders. Includes the discount decision tree and the approval matrix.
---

# Pricing Policy

Used by **Pricing Agent** (`offer-pricing`) and **Offer Director** for approval decisions.

## When to use

- Building offers, renewals, expansions, one-off quotes
- Validating a rep-requested discount
- Explaining a price to a customer or internal stakeholder

## Hard rules

- Never go below `floor_price[SKU]`
- Aggregate discount > 25% requires VP approval (`VP-Sales`)
- Aggregate discount > 40% requires CRO approval
- Strategic-logo and multi-year discounts **do not stack**
- All numbers from `pricing_engine` — agent assembles only

## Tools

- `pricing_engine.get_rates(scope)`
- `pricing_engine.segment_discount(segment, sku)`
- `pricing_engine.apply_discount(sku, rule, justification)`
- `deals.history.search` — precedent for strategic discounts

## Discount decision tree

See [`references/discount-tree.md`](references/discount-tree.md)

## Approval matrix

See [`references/approval-matrix.md`](references/approval-matrix.md)

## Strategic adder eligibility

| Adder | Requires |
|-------|----------|
| Competitive displacement | Named competitor in `dossier.competitors_mentioned` |
| Multi-year | `scope.term_months` ≥ 24 |
| Strategic logo | CRM `strategic_logo_flag = true` |
| Volume | Quantity ≥ `volume_threshold[SKU]` per rate card |

Only one strategic adder per SKU unless policy explicitly allows stacking (standard: no stack).

## Output requirements

Every priced line item: `list_price`, `discount_amount`, `net_price`, `source: pricing_engine.*`

Set `floor_check_passed = false` if any SKU net < floor — Director must not proceed to customer-facing output.
