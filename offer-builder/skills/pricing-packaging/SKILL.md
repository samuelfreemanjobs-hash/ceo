---
name: pricing-packaging
description: Use when setting price points, pricing models, anchoring, packaging decisions, annual vs monthly, minimum commitment, or "what should we charge". Triggers on "pricing", "price point", "how much to charge", "packaging", "anchor", "tiers pricing", "freemium", "per seat". Requires offer-architecture stack defined. ALWAYS states anchoring rationale and competitor price frame. Use web_search for public pricing signals when competitors named.
---

# Pricing & Packaging

Price is a **signal**, not just a number. Packaging determines who self-selects and how deals expand.

## Prerequisites

- Offer stack and tiers (from offer-architecture)
- ACV/AOV target or range
- Competitive alternatives with known or researchable pricing
- Business model (SaaS, DTC, services, etc.)

## Pricing model selection

| Model | Fits when | Watch out |
|-------|-----------|-----------|
| Flat subscription | Predictable value, single user type | Under-monetizes power users |
| Per seat / user | Collaboration products | Seat hoarding, shelfware |
| Usage / consumption | Variable value delivery | Bill shock, unpredictable revenue |
| Tiered (good/better/best) | Clear feature or support steps | Middle tier neglect |
| Freemium | PLG, viral, low marginal cost | Free tier too generous |
| One-time + maintenance | Hardware, licenses | Expansion revenue plan needed |
| Project / package | Services, agencies | Scope creep |

## Anchoring protocol

1. **Identify reference prices** — competitor public pricing, status quo cost (DIY hours × rate), previous vendor spend
2. **Set anchor** — higher reference that makes sell price feel reasonable (decoy tier, annual vs monthly, "full value" stack)
3. **State sell price** — primary price you'll lead with
4. **Document rationale** — one paragraph: why this frame for this ICP

Use `web_search` for competitor pricing pages when not in Scout artifact. Tag: Confirmed (public page) / Likely (third-party) / Unverified.

## Packaging decisions checklist

- [ ] Minimum commitment (seats, term, contract)
- [ ] Annual discount % and why
- [ ] What's sold separately (implementation, premium support)
- [ ] Expansion path (usage, seats, modules)
- [ ] Discount policy (never / sales-only / promo windows)

## Price sensitivity heuristics

| ACV / AOV | Typical motion | Pricing page needs |
|-----------|----------------|------------------|
| < $500/yr | Self-serve | Clear tiers, instant buy |
| $500–$5K | Hybrid | Trial or demo + transparent starter |
| $5K–$50K | Sales-assisted | "Starting at" + qualification |
| > $50K | Enterprise | Custom; publish framework not final price |

## Anti-patterns

- Price without anchor context ("$49" means nothing alone)
- Race to bottom vs. commodity competitors
- Annual discount so deep it trains monthly churn
- Hiding price when ICP expects transparency
- Same price for segments with 10× different value received

## Handoffs

- **To offer-validation:** price tests (A/B tier order, anchor placement)
- **To funnel-architect:** trial vs. paid entry, pricing page stage in funnel
- **To competition-analyzer:** if pricing intel missing — request pricing-teardown
