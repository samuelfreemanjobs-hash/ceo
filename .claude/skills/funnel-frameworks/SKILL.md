---
name: funnel-frameworks
description: Use this skill whenever the user wants to design, audit, or discuss the structure of a marketing or sales funnel. Triggers on phrases like "build a funnel", "map my customer journey", "design a sales process", "AARRR", "TOFU/MOFU/BOFU", "AIDA", "conversion funnel", "customer lifecycle", "acquisition funnel", "what framework should I use", "PLG funnel", "sales pipeline". Loads canonical frameworks and decision logic for picking the right one based on business model (SaaS, DTC, marketplace, services, info product, enterprise) and motion (PLG, sales-led, hybrid). Do NOT use for writing copy, channel tactics, or computing metrics — route those to conversion-copywriting, channel-playbooks, or funnel-metrics.
---

# Funnel Frameworks

**Phase:** Frame (2), Map (3) · **Pairs with:** `audience-mapping` (before), `funnel-visualization` (after)

## Purpose

Select the **simplest framework and shape** that fits the business. Output: funnel TYPE, primary GOAL metric, SHAPE, and named buyer-state stages — not channel tactics.

## Preconditions

- Minimum from discovery: business model, motion (if B2B), primary conversion goal
- If audience is vague, invoke `audience-mapping` first — framework choice depends on buyer

## Decision tree

| Business model | Primary motion | Default framework | Default shape |
|----------------|----------------|-------------------|---------------|
| B2B SaaS | PLG | AARRR | Looped |
| B2B SaaS | Sales-led | TOFU/MOFU/BOFU + MQL→SQL→Opp→Close | Multi-entry |
| B2B SaaS | Hybrid | Bow Tie or parallel entry | Multi-entry |
| DTC ecommerce | — | Awareness → Consideration → Purchase → Retention → Advocacy | Linear + retention loop |
| Marketplace | Two-sided | Supply + demand funnels | Parallel (two funnels) |
| Services / agency | High-touch | Lead-gen → qualify → propose → close | Linear |
| Info product | — | AIDCAS or webinar → cart | Linear |
| Enterprise | Sales-led | Forrester 5-stage + pipeline | Multi-entry |

**Rule:** One funnel, one job. Multiple unrelated goals → propose multiple funnels.

## Canonical frameworks (when to use)

### AIDA
- **Use:** Simple linear, single offer, short cycle
- **Stages:** Attention → Interest → Desire → Action
- **Avoid:** PLG with activation choke point (too shallow)

### AIDCAS
- **Use:** Info products, courses, high-consideration digital offers
- **Adds:** Conviction, Satisfaction after Action

### AARRR (Pirate metrics)
- **Use:** PLG SaaS, freemium/trial
- **Stages:** Acquisition → Activation → Retention → Revenue → Referral
- **Critical:** Define **activation** explicitly — often the real lever

### TOFU / MOFU / BOFU
- **Use:** Content-led B2B, inbound-heavy
- **Map to buyer states:** Unaware/Aware → Considering → Decided

### Bow Tie (Winning by Design)
- **Use:** Land-and-expand B2B, NRR-focused
- **Stages:** Acquire → Adopt → Expand (both sides of the tie)

### See-Think-Do-Care
- **Use:** SEO/content mapping to intent
- **Pairs with:** channel-playbooks for SEO

### Forrester 5-stage
- **Use:** Enterprise, long cycle, multiple stakeholders
- **Stages:** Discover → Explore → Buy → Engage → Advocate

## Funnel shapes

| Shape | Definition | When |
|-------|------------|------|
| **Linear** | Single path, one entry | Simple acquisition, DTC, services |
| **Looped** | Exit connects back to entry | PLG, retention/referral matter |
| **Multi-entry** | Several TOFU paths, shared BOFU | Inbound + outbound + partners |
| **Parallel** | Independent funnels (same company) | Multi-product, marketplace sides |

Hand **stage names** to `funnel-visualization` — use buyer states, not channel names.

## Anti-patterns (call these out)

| Anti-pattern | What it looks like | Fix |
|--------------|-------------------|-----|
| Flywheel labeled funnel | No discrete conversion goal | Name the metric or split funnels |
| Frankenstein funnel | Acquire + hire + fundraise in one map | One funnel per goal |
| Channels as stages | "Facebook → Email → Sales" | Reframe as buyer states |
| Over-staging | 12 micro-steps | Collapse to 4–7 decision-relevant stages |
| Wrong framework | AIDA for PLG with 35% activation | Switch to AARRR, focus activation |

## Operational workflow

1. **Restate** business model + motion + goal in one sentence
2. **Run decision tree** — pick default framework; note if hybrid needed
3. **Name 4–7 stages** as buyer states (Unaware → … → Advocate)
4. **Assign shape** — linear, looped, multi-entry, parallel
5. **Flag anti-patterns** in user's current description
6. **Confirm with user** before map/build (interactive sessions)
7. **Hand off** stage list + shape to `funnel-visualization`

## Output format (Frame phase)

```markdown
## Funnel frame
- **Type:** acquisition | activation | expansion | win-back | partner
- **Primary metric:** [one KPI]
- **Framework:** [name]
- **Shape:** linear | looped | multi-entry | parallel
- **Stages:** 1. [buyer state] → 2. … → n.
- **Notes:** [hybrid, second funnel if needed]
```

## Do not use when

- User only wants headline rewrite → `conversion-copywriting`
- User asks "what's a good CPC on Meta" → `channel-playbooks`
- User asks to model CAC/LTV numbers only → `funnel-metrics`
- User already has agreed framework and wants diagram only → `funnel-visualization`

## References (load on demand)

| File | Load when |
|------|-----------|
| `references/saas-plg.md` | PLG, trial, activation leak |
| `references/saas-sales-led.md` | MQL/SQL, enterprise pipeline |
| `references/dtc-ecommerce.md` | DTC, ecommerce lifecycle |
| `references/services.md` | Agency, consultancy, high-touch |
| `references/marketplaces.md` | Two-sided, supply/demand |

## Coordination

- **From audience-mapping:** ICP, buyer vs user, trigger events inform stage emphasis
- **To funnel-visualization:** Stage names, shape, leak hypothesis
- **To channel-playbooks:** After stages defined — assign channels per stage
- **To funnel-metrics:** Stage definitions become KPI boundaries

## Quality checklist

- [ ] Framework matches business model + motion
- [ ] Stages are buyer states, not channels
- [ ] Single primary metric stated
- [ ] ≤7 stages on main path
- [ ] User confirmed frame (if interactive)
