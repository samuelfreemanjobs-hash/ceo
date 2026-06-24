---
name: proposal-validation
description: Validate a client proposal draft against its source Offer Builder artifact before delivery. Use as final gate before saving to docs/marketing/proposals. Checks scope fidelity, price match, proof honesty, guarantee parity, and compliance flag preservation. Failures must be fixed — do not ship with drift.
---

# Validation checklist

Run after draft, before output.

## 1. Scope fidelity

- [ ] Every deliverable in proposal §3 appears in offer §3 included list
- [ ] Every out-of-scope item in proposal matches offer §3 boundaries
- [ ] Timeline phases ⊆ offer §4 steps
- [ ] Client responsibilities = offer §4 (no new asks)

**Fail →** Remove invented items or route back to `offer-builder` if scope wrong.

## 2. Price fidelity

- [ ] Primary investment = offer §6 primary tier price (exact)
- [ ] Alternate tiers match offer §6 table row-for-row
- [ ] Payment terms = offer §7 (no new net-30 if offer says upfront)

**Fail →** Fix numbers. Never "approximate" or round up.

## 3. Proof honesty

- [ ] No claim in §5 stronger than offer §5
- [ ] Gaps from offer explicitly stated if proof thin
- [ ] No fabricated testimonials or metrics

## 4. Guarantee parity

- [ ] Guarantee in §7 = offer §7 only (or omitted if offer had none)
- [ ] No new risk reversal invented for persuasion

## 5. Compliance preservation

- [ ] YMYL / must-not-say / substantiation flags copied to §7 internal block
- [ ] Regulated claims not added in client sections

## 6. Format compliance

- [ ] Sections match brief format (`standard` | `short` | `executive`)
- [ ] Header includes offer artifact reference path
- [ ] Valid-until date from brief if provided

# Severity

| Issue | Action |
|-------|--------|
| Scope or price drift | Block — fix before ship |
| Tone / wording only | Fix in place |
| Missing personalization | Ask 1 clarifying question max |
| Structural offer problem | Hand back to `offer-builder` |
