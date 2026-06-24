---
name: offer-validation
description: Use when prioritizing tests to validate positioning, messaging, pricing, or offer structure. Triggers on "test this offer", "validate", "how do we know", "experiments", "ICE", "assumptions", "message testing". Run after Offer Spec draft. ALWAYS produces top 3 ICE-scored tests and explicit assumption log. Prefer cheapest test that falsifies the riskiest assumption.
---

# Offer Validation

An offer spec is a **hypothesis bundle**. This skill turns it into a test plan before you build funnels or spend media budget.

## Assumption log (extract from spec)

| Assumption | Risk if wrong | Evidence today | Test type |
|------------|---------------|----------------|-----------|
| ICP will self-identify with category label | Positioning fails | | Message test |
| Price anchor works | Conversion / ARPU miss | | Pricing page A/B |
| Proof ladder sufficient | Trust gap | | Sales call / LP test |
| Bonus increases conversion | Complexity without lift | | Offer stack A/B |

## ICE scoring

| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| **Impact** | Nice to know | Meaningful metric move | Changes go/no-go |
| **Confidence** | Pure guess | Some analog evidence | Strong prior |
| **Ease** | Weeks + budget | Days + moderate effort | Hours + existing traffic |

**ICE = (I + C + E) / 3** — rank tests; run highest first.

## Test menu (by assumption type)

| Assumption | Fast test | Better test |
|------------|-----------|-------------|
| Positioning resonance | 5 ICP interviews with statement | Landing headline A/B |
| Category literacy | LinkedIn poll / community post | Paid traffic to two LP variants |
| Price acceptance | Sales calls with two anchors | Pricing page split test |
| Offer stack value | Email split (with vs without bonus) | Closed pilot cohort |
| Guarantee impact | Remove/add on pricing page | Cohort refund rate tracking |

## Output: top 3 tests

For each test specify:
1. **Hypothesis** — "If X, then Y metric moves because Z"
2. **Method** — channel, sample, duration
3. **Success criteria** — numeric threshold where possible
4. **Kill criteria** — when to abandon positioning/offer angle

## Sequencing rules

1. Test **positioning/message** before **price** (wrong message invalidates price tests)
2. Test **ICP fit** before **scale** (don't amplify misfit)
3. **Qualitative before quantitative** when n < 100 conversions/month

## Handoffs

- **To funnel-architect:** winning tests become funnel optimization backlog
- **To analytics:** experiment design for tracked tests
- **To Morgan:** campaign-scale validation needs coordinated specialists

## Anti-patterns

- Building full funnel before message test
- Testing 10 things at once
- No kill criteria (sunk cost on dead positioning)
- Declaring victory on vanity metrics (clicks without conversion)
