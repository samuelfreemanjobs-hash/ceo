---
name: lp-validation
description: Validate landing page copy against source offer and proposal — scope fidelity, price accuracy, proof honesty, guarantee rules, CTA clarity. Use before saving LP output or routing to compliance.
---

# LP Validation

Run after draft, before save. Fail closed on price/scope violations.

## Checks

### 1. Scope fidelity
- Every deliverable in LP ⊆ offer §3 included items
- Out-of-scope items match offer §3 boundaries
- No timelines or deliverables invented

### 2. Price fidelity
- Primary tier price **exact match** to offer §6
- Tier table (if present) matches offer tier table row-for-row
- No rounding, "starting at" unless offer uses it

### 3. Proof honesty
- Stats and logos only from offer §5 substantiated list
- Gaps not upgraded to verified claims
- Testimonials carry same caveats as offer

### 4. Guarantees
- Guarantee text ⊆ offer §7
- No new risk reversal or money-back terms

### 5. CTA
- Exactly one primary CTA label + URL in brief
- CTA action matches offer stage (don't say "Buy" for high-touch service)

### 6. Compliance
- YMYL flags from offer §7 listed in metadata
- Quantitative claims flagged for `compliance-agent`

## Verdict format

```json
{
  "pass": true,
  "failures": [],
  "warnings": ["proof section thin — consider minimal format"],
  "ready_for_compliance": false
}
```

Set `ready_for_compliance: true` only when `pass: true` and brief has no open compliance flags.
