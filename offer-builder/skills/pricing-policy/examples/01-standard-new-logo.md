# Example 1 — Standard new-logo mid-market deal

## Dossier extract
- segment: mid-market
- size_employees: 350
- deal_type: new-logo
- competitors_mentioned: []
- strategic_logo_flag: false

## Scope
- ProductA × 200 seats
- ProductB × 200 seats
- term_months: 12

## Walk-through

Step 0 — Renewal uplift: N/A (new-logo)

Step 1 — Segment discount
  list_subtotal              = $240,000
  segment                    = mid-market → 5%
  segment_discount           = $12,000
  subtotal_after_segment     = $228,000

Step 2 — Volume discount
  volume                     = 400 seats → T3 (250-1000) → 7%
  volume_discount            = $15,960
  subtotal_after_volume      = $212,040

Step 3 — Strategic adder
  Competitive?  No (empty competitors_mentioned)
  Multi-year?   No (term = 12 months)
  Strategic logo? No
  → no adder applied

Step 4 — Floor check
  All line items above floor → PASS

Step 5 — Aggregate
  aggregate_discount_pct = 1 − (212,040 / 240,000) = 11.65%
  → 10-25% band → requires_approval = sales_manager

## Output
- final_net: $212,040
- aggregate_discount: 11.65%
- requires_approval: true
- approver_role: sales_manager
- All discounts recorded with rule_ids
- floor_check_passed: true
