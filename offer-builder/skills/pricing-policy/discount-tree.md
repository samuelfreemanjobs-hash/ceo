# Discount decision tree

Pricing Agent must follow these steps in order. Each step has an input,
a tool call, and an output. Do not skip, reorder, or short-circuit.

## Step 0 — Renewal uplift (renewals only)

INPUT: deal_type, prior_acv, scope
TOOL:  pricing_engine.renewal_uplift(prior_acv, scope, uplift_policy)
OUTPUT: uplifted_list_subtotal, uplift_pct, uplift_rule_id

If deal_type ≠ renewal, skip to step 1 with list_subtotal from rate card.

If uplift_pct > 7%, set requires_approval ≥ sales_manager regardless of
where aggregate lands later. The rep needs visibility before sending.

## Step 1 — Segment discount

INPUT:  dossier.account.segment ∈ {enterprise, mid-market, SMB, startup}
TOOL:   pricing_engine.segment_discount(segment, list_subtotal)
OUTPUT: segment_discount_amount, rule_id

Standard table (source of truth: pricing_engine, not this doc):

| Segment    | Standard discount |
|------------|-------------------|
| enterprise | 10%               |
| mid-market | 5%                |
| SMB        | 0%                |
| startup    | 15% (program flag required) |

Startup discount requires `startup_program_flag = true` in CRM. If absent,
fall back to SMB or mid-market by `size_employees`.

## Step 2 — Volume discount

INPUT:  subtotal_after_segment, volume_metric (typically total_seat_count)
TOOL:   pricing_engine.volume_discount(subtotal, volume)
OUTPUT: volume_discount_amount, tier_id

Tier table (per product family — full map in `floor-prices.csv`):

| Tier | Threshold       | Additional discount |
|------|-----------------|---------------------|
| T1   | < 50 units      | 0%                  |
| T2   | 50 – 250        | 3%                  |
| T3   | 250 – 1,000     | 7%                  |
| T4   | 1,000 – 5,000   | 10%                 |
| T5   | > 5,000         | 12%                 |

## Step 3 — Strategic adder (pick ZERO or ONE)

Strategic adders do NOT stack. Record all eligible; select the one with
largest customer benefit; mark unused as `eligible: true, selected: false`.

### 3a. Competitive displacement adder
Eligible if:
- dossier.competitors_mentioned contains a competitor on the
  approved-competitive-list, AND
- rep_brief or call transcripts indicate active displacement
Adder: up to 5%.

### 3b. Multi-year commitment adder
Eligible if scope.term_months ≥ 24.
- 24–35 months → 5%
- 36+ months  → 8%

### 3c. Strategic-logo adder
Eligible if CRM.account.strategic_logo_flag = true.
Adder: up to 10%. Always escalates to ≥ vp_sales regardless of aggregate.

Selection rule: pick the adder yielding the largest dollar benefit to the
customer. Tie → prefer multi-year (lower approval friction).

## Step 4 — Floor check

For every line item:
TOOL: pricing_engine.check_floor(sku, unit_price_net)

If any line item violates its floor:
- BLOCK. Do not emit pricing.
- Return error: { type: "floor_violation", sku, list_price,
                  attempted_net, floor }

This is a hard policy stop. The agent does NOT get to retry with a
different discount mix to work around the floor — that's exactly what
the floor exists to prevent.

## Step 5 — Aggregate threshold check

aggregate_discount_pct = 1 − (final_net / list_subtotal_after_uplift)

| Aggregate range | Action                        |
|-----------------|-------------------------------|
| ≤ 10%           | auto-approve                  |
| 10 – 25%        | requires_approval=sales_manager |
| 25 – 40%        | requires_approval=vp_sales    |
| > 40%           | requires_approval=cro         |

Overrides (escalate to the higher of the two):
- strategic-logo adder used → at least vp_sales
- renewal uplift > 7%       → at least sales_manager

Director maps these into `offer.approval` using schema enum values.

## Output (Pricing Agent JSON)

Output must include — in this order — for the Director and Evaluator
to verify policy compliance:

1. list_subtotal (after uplift if renewal)
2. discounts[] with type segment, volume, and strategic adder entries
3. strategic_adder_eligibility_log: [{type, eligible, would_yield, selected}]
4. aggregate_discount_pct
5. floor_check_passed: true (must be true to emit; otherwise return error)
6. renewal_uplift_pct or null

Approval (`requires_approval`, `approver_role`) is assembled by the Director
from aggregate bands and override rules in [`approval-matrix.csv`](approval-matrix.csv).
