---
name: proposal-structure
description: Map Offer Builder output sections to client-facing proposal structure. Use when drafting a proposal from an offer artifact — section order, tone, personalization hooks, and format variants (standard, short, executive). Ensures internal offer semantics translate to sendable client language without scope or price drift.
---

# Offer → proposal mapping

| Offer section | Proposal section | Transform |
|---------------|------------------|-----------|
| §1 Name & promise | §1 Executive summary + §3 opening | Client language; do not strengthen promise |
| §2 For who / not for | §2 Situation & fit | "We understand..." framing |
| §3 What's included | §3 Proposed solution | Bullets → deliverables; keep boundaries |
| §4 How it works | §4 How we'll work together | Table + client responsibilities |
| §5 Proof | §5 Proof & credibility | Honest gaps preserved |
| §6 Pricing | §6 Investment | Same numbers; explain logic plainly |
| §7 Guarantee / terms | §7 Terms & assumptions | Copy flags for compliance |
| §8 Objections | §8 Common questions | Rephrase as client questions |
| §9 Implementation | §9 Next steps | Sales CTA + optional signature |

# Tone calibration

| Brief tone | Guidance |
|------------|----------|
| formal | Third person acceptable; complete sentences; minimal contractions |
| consultative | "We recommend..."; partnership language |
| technical | Name deliverables precisely; keep jargon only if buyer is technical |
| warm | First person plural; conversational but still precise on scope |

# Personalization (§2)

Use brief `personalization_notes` only. Do not invent:
- Client quotes
- Budget figures not in offer
- Competitor names unless in offer/brief
- Urgency without brief evidence

# Format compression

**short:** Merge §3+§4 if needed; drop §5 if no proof; keep §7 one line unless guarantee exists.

**executive:** §1 = 1 paragraph; §6 = table only; §9 = numbered steps (max 3).

# Anti-patterns

- "World-class", "best-in-class", unverifiable superlatives
- Padding with generic agency boilerplate
- Hiding out-of-scope in footnotes
- Rounding prices up for "clean" numbers
