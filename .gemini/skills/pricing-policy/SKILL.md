---
name: pricing-policy
description: Apply the company's pricing policy — rate cards, segment
  discounts, volume tiers, strategic adders, approval thresholds, and
  floor prices. Use whenever building, validating, or revising priced
  line items in a customer-facing offer, or when explaining a price
  internally. Includes the discount decision tree, approval matrix,
  floor prices per SKU family, and worked examples of edge cases
  (stacking, renewals, floor violations). Do not use for one-off custom
  quotes outside the standard rate-card structure — those require manual
  desk-pricing review.
---

# Hard rules (non-negotiable)

1. **Never go below floor_price[SKU].** Floors are in `floor-prices.csv`,
   pulled fresh per offer (never cached). Floors protect gross margin and
   don't bend for any deal.
2. **Aggregate discount > 25% requires VP-Sales approval.**
3. **Aggregate discount > 40% requires CRO approval.**
4. **Strategic-logo discount and multi-year discount do NOT stack.** Pick
   the one that gives the customer the larger benefit; record both as
   eligible, the chosen one as selected.
5. **Volume discount applies AFTER segment discount, BEFORE strategic
   adders.** Order matters and is enforced by `pricing_engine.apply_discount`.
6. **Every applied discount must record: amount, rule_id, justification.**
   Anything else is a policy violation regardless of math.
7. **Currency follows customer billing region** unless a documented
   override exists in the dossier.
8. **Strategic-logo adder always escalates to at least VP-Sales**,
   regardless of aggregate.
9. **Renewal uplift runs before all discount steps**, against the
   uplifted list price.

# When to use this skill

- Building a new offer
- Validating a discount a rep has requested
- Renewing an account (apply renewal-uplift rules)
- Explaining a price to a customer or internal stakeholder

# When NOT to use this skill

- Desk-pricing requests outside the standard rate card → manual review
- Marketplace/partner-sourced deals → `partner-pricing` skill applies first
- Non-revenue swaps (e.g. service-for-equity) → out of scope, escalate

# Discount decision tree

See [`discount-tree.md`](discount-tree.md) for the step-by-step. Summary:

```
START
  └─ (renewals only) renewal-uplift
  └─ segment discount (automatic, table lookup)
  └─ volume discount (automatic, tier table)
  └─ strategic adder (≤ 1: competitive XOR multi-year XOR strategic-logo)
  └─ floor check (hard stop on violation)
  └─ aggregate threshold check → Director sets approval
  └─ emit pricing
```

# Approval matrix

See [`approval-matrix.csv`](approval-matrix.csv). Summary:

| Aggregate discount     | Approver        | SLA              |
|------------------------|-----------------|------------------|
| 0 – 10%                | none (auto)     | n/a              |
| 10 – 25%               | Sales Manager   | 4 business hrs   |
| 25 – 40%               | VP Sales        | 1 business day   |
| > 40%                  | CRO             | 2 business days  |
| any floor violation    | BLOCKED         | n/a              |
| strategic-logo adder   | min VP Sales    | 1 business day   |
| renewal uplift > 7%    | min Sales Mgr   | 4 business hrs   |

Approver roles in offer output use schema enums: `sales_manager`, `vp_sales`, `cro`, `legal`.

# Floor prices

Pulled fresh per offer via `pricing_engine.check_floor(sku, unit_price_net)`.
Never cached. Source: Finance (`floor-prices.csv`), refreshed quarterly.

# Renewal uplift

Renewal uplift rates live in `uplift-table.csv` (Finance-owned). Applied in
step 0 of the discount tree before segment/volume/strategic steps.

# Worked examples

See [`examples/`](examples/):

- `01-standard-new-logo.md` — mid-market, segment + volume only
- `02-competitive-multi-year.md` — strategic-adder pick-one decision
- `03-renewal-with-uplift.md` — renewal uplift mechanics
- `04-stack-violation.md` — what NOT to do, and how policy catches it
