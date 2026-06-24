---
name: lp-structure
description: Map Offer Builder and Proposal artifacts to landing page sections — hero, proof, pricing, FAQ, CTA. Use when drafting or restructuring LP copy from offer/proposal inputs. Ensures scannable web format and single primary conversion action.
---

# LP Structure — Offer + Proposal → Landing Page

## Section mapping

| LP block | Primary source | Secondary source |
|----------|----------------|------------------|
| Hero headline | Offer §1 promise | Proposal §1 (tone) |
| Hero subhead | Offer §2 for who | Proposal situation |
| Problem | Offer §2 pains | Proposal §2 |
| Solution overview | Offer §1 + §4 | Proposal §3 |
| What's included | Offer §3 | Proposal §3 |
| Proof | Offer §5 | Proposal proof callouts |
| Pricing | Offer §6 primary tier | Proposal §6 investment |
| FAQ | Offer §8 objections | Proposal FAQ if present |
| Final CTA | Brief primary CTA | Proposal §9 next steps |

## Hero patterns

**Do:**
- Lead with specific outcome + qualifier ("for B2B teams with 10–50 employees")
- One idea per headline line
- CTA verb matches stage: "Book" / "Apply" / "Get started" / "Join waitlist"

**Don't:**
- Clever wordplay without clarity
- Multiple CTAs above the fold
- Stronger promise than offer §1

## Format rules

### `full`
Hero → Problem → Solution → Proof → Pricing → FAQ → Final CTA

### `minimal`
Hero (headline + subhead + CTA) → 3 proof bullets → repeat CTA

### `tiered`
`full` + tier comparison table copied from offer §6 (exact prices)

## Voice

Load `brand-voice` skill. Web copy: shorter sentences than proposal; more bullets; active voice.

## Handoff metadata

Include in page metadata block:
- `offer_ref`, `proposal_ref`, `primary_cta`, `compliance_flags`
