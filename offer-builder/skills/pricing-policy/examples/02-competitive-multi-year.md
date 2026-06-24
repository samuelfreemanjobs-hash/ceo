# Example 2 — Competitive displacement + multi-year — pick-one decision

The interesting case: two adders both eligible, must pick one.

## Dossier extract
- segment: enterprise
- competitors_mentioned: [
    {name: "CompetitorX", context: "current vendor, renewal in Q3"}
  ]
- strategic_logo_flag: false

## Scope
- ProductA × 1,500 seats
- term_months: 36

## Walk-through

Step 1 — Segment
  list_subtotal              = $450,000
  segment                    = enterprise → 10%
  segment_discount           = $45,000
  subtotal_after_segment     = $405,000

Step 2 — Volume
  1,500 seats → T4 → 10%
  volume_discount            = $40,500
  subtotal_after_volume      = $364,500

Step 3 — Strategic adder eligibility
  Competitive       : ELIGIBLE — CompetitorX on approved list, displacement
                                  evidenced in transcripts
                                  → adder up to 5% = up to $22,500
  Multi-year        : ELIGIBLE — 36 months
                                  → adder 8% = $36,000
  Strategic logo    : NOT ELIGIBLE (flag false)

  Pick larger customer benefit:
    multi-year ($36,000) > competitive ($22,500)
  → SELECT multi-year
  → log competitive as eligible, selected: false

  subtotal_after_adder       = $328,500

Step 4 — Floor check: PASS

Step 5 — Aggregate
  aggregate_discount_pct = 1 − (328,500 / 450,000) = 27.0%
  → 25-40% band → requires_approval = vp_sales

## Output
- final_net: $328,500
- aggregate: 27.0%
- strategic_adder: { type: multi-year, amount: $36,000 }
- strategic_adder_eligibility_log:
    [
      {type: competitive,    eligible: true, would_yield: 22500, selected: false},
      {type: multi-year,     eligible: true, would_yield: 36000, selected: true},
      {type: strategic-logo, eligible: false}
    ]
- requires_approval: true, approver_role: vp_sales
- audit_note: "Competitive adder eligible; multi-year selected for larger benefit."
