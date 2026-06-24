---
name: funnel-frameworks
description: Use whenever the user wants to design, audit, or discuss the structure of a marketing or sales funnel. Triggers on "build a funnel", "map my customer journey", "design a sales process", "AARRR", "TOFU/MOFU/BOFU", "AIDA", "conversion funnel", "customer lifecycle", "acquisition funnel". Loads canonical frameworks and decision logic for picking the right one by business model and motion.
---

# Funnel Frameworks

**Used by:** Funnel Architect (Phase 2 — Frame, Phase 3 — Map)

## Framework selection decision tree

| Business model | Primary motion | Default framework |
|----------------|----------------|-------------------|
| B2B SaaS | PLG | AARRR (activation often > acquisition) |
| B2B SaaS | Sales-led | TOFU/MOFU/BOFU + MQL→SQL→Opp→Close |
| B2B SaaS | Hybrid | Bow Tie or parallel entry |
| DTC ecommerce | — | Awareness → Consideration → Purchase → Retention → Advocacy |
| Marketplace | Two-sided | Supply + demand funnels (see references/marketplaces.md) |
| Services / agency | High-touch | Lead-gen → qualify → propose → close |
| Info product | — | AIDCAS or webinar → cart |

## Canonical frameworks

- **AIDA** — Attention, Interest, Desire, Action (simple linear)
- **AIDCAS** — adds Conviction, Satisfaction (info products)
- **AARRR** — Acquisition, Activation, Retention, Revenue, Referral (PLG)
- **TOFU/MOFU/BOFU** — content-led B2B
- **Bow Tie** (Winning by Design) — land → adopt → expand
- **See-Think-Do-Care** — Google content mapping
- **Forrester 5-stage** — discover → explore → buy → engage → advocate

## Funnel shapes

| Shape | When |
|-------|------|
| Linear | Simple acquisition, single entry |
| Looped | PLG with re-activation and expansion |
| Multi-entry | Enterprise (inbound + outbound + partner) |
| Parallel | Multi-product or multi-ICP |

## Anti-patterns

- Calling a **flywheel** a funnel when there's no discrete conversion goal
- One funnel for multiple unrelated products
- Conflating **channels** with **stages**

## References (load on demand)

- `references/marketplaces.md` — two-sided funnel design
- `references/saas-plg.md` — PLG patterns (activation focus)
- `references/saas-sales-led.md` — enterprise pipeline
- `references/dtc-ecommerce.md` — DTC lifecycle
- `references/services.md` — high-touch lead gen
