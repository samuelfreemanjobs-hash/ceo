# Example 3 — Renewal with annual price uplift

The interesting case: uplift runs BEFORE all discount steps, and net effect
to customer can still be a price decrease if discounts more than absorb it.

## Dossier extract
- segment: mid-market
- deal_type: renewal
- prior_acv: $180,000

## Scope
- Same as prior year: ProductA × 300 seats, 12 months

## Walk-through

Step 0 — Renewal uplift
  Standard annual uplift          = 5%
  new_list_subtotal               = $189,000
  uplift_pct                      = 5%  (not > 7%, no extra approver)

(Steps 1-5 now run against the uplifted list)

Step 1 — Segment: mid-market → 5%
  $189,000 × 0.05               = $9,450
  subtotal_after_segment        = $179,550

Step 2 — Volume: 300 seats → T3 → 7%
  $179,550 × 0.07               = $12,569
  subtotal_after_volume         = $166,981

Step 3 — Strategic adder: none eligible

Step 4 — Floor check: PASS

Step 5 — Aggregate
  vs uplifted list: 1 − (166,981 / 189,000)  = 11.65% → sales_manager
  vs prior ACV:     166,981 / 180,000 − 1    = −7.2%
  (Customer pays 7.2% LESS than last year despite the uplift.)

## Approval logic
  Aggregate band (10-25%)   → sales_manager
  Uplift > 7%?  No (5%)     → no extra approver
  Net effect to customer    → −7.2% YoY (strong renewal story)

## What the Copywriter must do
- Explain the uplift (5% standard annual)
- Show the offset from segment + volume discount
- Frame the net cost change honestly: customer pays less than last year
