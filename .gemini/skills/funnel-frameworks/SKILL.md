---
name: funnel-frameworks
description: Use this skill whenever the user wants to design, audit, or discuss the structure of a marketing or sales funnel. Triggers on phrases like "build a funnel", "map my customer journey", "design a sales process", "AARRR", "TOFU/MOFU/BOFU", "AIDA", "conversion funnel", "customer lifecycle", "acquisition funnel", and on any conversation about moving prospects through a buying process. Loads the canonical frameworks and the decision logic for picking the right one based on business model (SaaS, DTC, marketplace, services, info product, enterprise) and motion (PLG, sales-led, hybrid). ALWAYS invoke this skill before designing any funnel — picking the wrong framework wastes hours of downstream work.
---

# Funnel Frameworks

The job of this skill is to pick the **right shape** for the funnel before any building begins. Most bad funnels are bad because they used the wrong framework — a linear AIDA flow imposed on a PLG product, or a TOFU/MOFU/BOFU content funnel imposed on a transactional ecommerce business.

## When to invoke

- The user is starting a new funnel from scratch
- The user has an existing funnel but is unsure if its shape is right
- The user references a framework by name and you need to validate it fits
- The user describes a business but hasn't named a framework — you must pick one for them

## Decision logic: pick the framework

Run through these questions IN ORDER. Stop at the first match.

### Question 1: What is the business model?

| Business model | Default framework | Funnel shape |
|----------------|-------------------|--------------|
| **PLG SaaS** (self-serve, freemium or low-friction trial, in-product activation matters) | **AARRR** (Pirate Metrics) | Looped — activation and retention are stages, not afterthoughts |
| **Sales-led SaaS / Enterprise** (long cycle, multiple stakeholders, demos required) | **MQL → SQL → Opp → Closed-Won** + post-sale expansion | Linear with multi-stakeholder branching; "Bow Tie" if expansion matters |
| **DTC ecommerce** (transactional, one-time or subscription purchase) | **Awareness → Consideration → Purchase → Retention → Advocacy** | Linear with strong retention loop |
| **Marketplace** (two-sided) | **Two parallel funnels** (supply + demand) joined at the transaction | Parallel; supply-side often the constraint |
| **Services / agencies** (high-touch, project-based) | **Lead → Qualify → Proposal → Close** | Linear, low-volume, high-value |
| **Info products / courses** (content + community) | **Awareness → Lead Magnet → Nurture → Tripwire → Core Offer → Upsell** | Linear with ascending offer ladder |
| **Mobile app / consumer** (free, ad-supported or IAP) | **AARRR** but Activation = "habit formation" | Looped, heavy on retention metrics |

### Question 2: What is the motion?

| Motion | What it means | Key implication |
|--------|---------------|-----------------|
| **PLG** (Product-Led Growth) | Users find value before talking to sales (or never talk to sales) | Activation is the choke point. Build the funnel around in-product behavior. |
| **Sales-led** | Humans qualify and close deals | The funnel runs through CRM stages, not page views. Time-in-stage matters as much as conversion. |
| **Marketing-led** | Marketing generates leads, hands to sales OR self-serve | Need clear handoff criteria. Lead scoring matters. |
| **Hybrid** (most common) | Mix of PLG entry + sales-assist on larger deals | Two funnels with a "graduation" criterion. Don't try to model as one. |

If hybrid: design TWO funnels. PLG funnel for self-serve under threshold (e.g., <$X ACV); sales-assisted funnel for above. Set the threshold explicitly.

### Question 3: What is the funnel SHAPE?

Even within a framework, the shape matters:

- **Linear**: stages flow one direction. Default for transactional businesses. Easiest to instrument.
- **Looped**: customers re-enter earlier stages (re-engagement, expansion, referral). Default for subscription businesses.
- **Multi-entry**: prospects enter at different stages (warm referral starts at "Consideration", cold inbound starts at "Aware"). Common in enterprise.
- **Parallel**: two or more funnels run alongside each other (marketplace supply/demand; B2B2C company selling to both businesses and end users).
- **Bow Tie**: pre-sale funnel + post-sale expansion funnel, mirror images. The standard for modern SaaS where NRR > new-logo growth.

Ask: "Does revenue from existing customers matter more than revenue from new ones?" If yes → Bow Tie. If new logos dominate → linear or AARRR.

## The frameworks themselves

Brief reference — invoke the relevant `references/` file for full templates.

### AIDA (and variants: AIDCAS, AIDCA)

**Attention → Interest → Desire → Action** (sometimes + Conviction, Satisfaction)

Use for: traditional advertising flows, content-driven sales pages, info products. Avoid for: PLG, complex B2B, anything with significant post-sale work. Why it's overused: simple to teach, but treats buyers as linear when they often aren't.

### TOFU / MOFU / BOFU

**Top of Funnel** (awareness) → **Middle of Funnel** (consideration) → **Bottom of Funnel** (decision).

Use for: content-marketing-driven businesses (B2B SaaS, services). Maps cleanly to content types: TOFU=blog/social, MOFU=guides/webinars, BOFU=demos/case studies. Avoid for: anything where the funnel isn't content-driven. Don't bolt this onto a paid-acquisition DTC funnel.

### AARRR (Pirate Metrics — Dave McClure)

**Acquisition → Activation → Retention → Revenue → Referral**

Use for: PLG SaaS, mobile apps, consumer products. The default if the user has a product people interact with directly. Why it's the modern default for SaaS: it treats activation and retention as first-class stages, which a linear "MQL → Closed-Won" funnel hides. Trap: don't confuse Activation (user got value) with Sign-up (user gave email). Define activation as behavior, not registration.

### Bow Tie (Winning by Design)

**Acquisition → Engagement → Exploration → Evaluation → Purchase → Adoption → Usage → Value → Expansion → Advocacy**

Use for: modern SaaS where NRR matters as much as new-logo. Forces you to design post-sale stages with the same rigor as pre-sale. Avoid for: businesses where customers buy once (most DTC, info products, services).

### See–Think–Do–Care (Avinash Kaushik)

**See** (broad audience) → **Think** (commercial intent emerges) → **Do** (ready to buy) → **Care** (post-purchase).

Use for: content + paid hybrid funnels where you want to clearly separate audience-targeting from intent-targeting. Particularly good for digital advertising mix design.

### Forrester's 5-stage (B2B)

**Discover → Explore → Buy → Use → Ask**

Use for: enterprise B2B with long, committee-driven cycles. Less common in startup contexts but useful when modeling complex buying groups.

## Funnel anti-patterns

When you spot these, redesign before building:

1. **The "Frankenstein funnel"**: trying to serve multiple primary goals with one funnel. Symptom: stages have conflicting CTAs (book a demo AND start a free trial AND download an ebook on the same page). Fix: split into multiple funnels with one primary CTA each.

2. **The "channel masquerading as a stage"**: "Email" is not a stage. "Webinar" is not a stage. Stages are _buyer states_; channels move buyers between states. If the user's funnel has channel names as stages, redraw it.

3. **The "activation gap"**: PLG funnel that goes Acquisition → Revenue with no Activation stage. Always the cause of bad trial-to-paid conversion. Insert activation explicitly.

4. **The "post-sale void"**: subscription business with no stages after first purchase. If NRR matters, you need expansion/retention stages explicitly mapped.

5. **The "20-stage funnel"**: more stages ≠ better funnel. If you have more than 7 stages, you've conflated stages with sub-steps. Compress.

6. **The "flywheel mislabeled as a funnel"**: if customer success drives new acquisition (referrals, word-of-mouth, community), you may be looking at a flywheel, not a funnel. Acknowledge this and design accordingly — the metrics differ.

## Output checklist

Before handing off to other skills, this skill must produce:

- [ ] Selected framework, named and justified
- [ ] Selected shape (linear / looped / multi-entry / parallel / bow tie)
- [ ] Stage list (3–7 stages, named in buyer-state language)
- [ ] Primary conversion goal (ONE)
- [ ] Whether there's a meaningful post-sale funnel and what it looks like
- [ ] Flags for any anti-patterns you spotted in the user's brief

## Reference files

Read these on demand for deep templates:

- `references/saas-plg.md` — PLG-specific funnel patterns: activation definition, time-to-value, expansion loops
- `references/saas-sales-led.md` — Enterprise MQL→SQL→Opp→Close with lead-scoring and stage-exit criteria
- `references/dtc-ecommerce.md` — Acquisition → Consideration → Purchase → Retention → Advocacy with retention focus
- `references/services.md` — Lead-gen funnels for high-touch services (consulting, agencies, professional services)
- `references/marketplaces.md` — Two-sided funnel design and the "chicken-and-egg" supply problem

## Final guidance to the agent

If the user pushes back on your framework choice, _engage with their reasoning_. They may know something about their business you don't. Frameworks are guidance, not law. But don't capitulate to a clearly wrong choice — if they insist on TOFU/MOFU/BOFU for a transactional DTC business, surface the cost of that choice (you'll undermeasure retention, you'll over-invest in content, etc.) and let them decide.
