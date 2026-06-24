# Example 4 — Attempted strategic-adder stacking — policy stop

## Scenario
Pricing Agent receives a scope eligible for BOTH multi-year AND
strategic-logo adders. A naive (or pressured) agent might try to stack
them. This example shows what must happen instead, and what the policy
check catches if it doesn't.

## What the agent MUST do

- Identify both as eligible
- Record both in `strategic_adder_eligibility_log`
- Pick the larger benefit (or, if strategic-logo, accept its approval cost)
- DO NOT add them together
- DO NOT switch adders mid-offer to maximize discount across line items

## Correct output

eligibility_log:
  - {type: multi-year,     eligible: true, would_yield: 8%,  selected: false}
  - {type: strategic-logo, eligible: true, would_yield: 10%, selected: true}

strategic_adder: { type: strategic-logo, amount: 10% of subtotal }

requires_approval: true
approver_role: cro
approver_role_reason: |
  "strategic-logo adder applied → minimum vp_sales per hard rule 8;
   aggregate also in 25-40% band → escalates further to cro."

## What a policy violation would look like

If the output contained:
  strategic_adder: { type: "multi-year + strategic-logo", amount: 18% }

→ Evaluator dimension 3 (policy compliance) fails immediately
→ Routed back to Pricing with specific_issue:
    "strategic_adder.type combines two adders; hard rule 4 prohibits stacking"
→ After 3 such cycles, escalate to human

## Why the hard rule exists

Strategic adders represent margin concessions made for STRATEGIC reasons.
Stacking them means conceding margin for the same strategic story twice.
The rule exists because historical analysis showed reps doing exactly this
under quota pressure. The policy is structural, not negotiable, and not
adjustable per deal.
