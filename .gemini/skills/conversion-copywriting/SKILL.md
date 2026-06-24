---
name: conversion-copywriting
description: Use this skill whenever the user needs to write or improve any funnel asset headlines, hero sections, landing pages, ad copy, email subject lines, email bodies, CTAs, lead magnet titles, sales pages, pricing pages, onboarding flows. Triggers on "write copy", "headline", "subject line", "landing page", "ad copy", "email sequence", "rewrite this", "make this convert better", "CTA", "hero section". Applies PAS, BAB, AIDA, 4Ps, FAB to the user's specific audience and offer. Always runs evaluator-optimizer loop on high-stakes copy (hero, primary email, main ad). Do NOT use without audience context — run audience-mapping first if missing. Do NOT use for channel selection or funnel structure.
---

# Conversion Copywriting

**Phase:** Build (4) · **Requires:** `audience-mapping` output (objections, voice, buyer vs user)

## Purpose

Generate **stage-appropriate, audience-specific** copy. Run evaluator-optimizer on high-stakes assets. Route external publish to compliance.

## Preconditions check

Before writing, confirm you have:

- [ ] Economic buyer vs user (who is the hero?)
- [ ] Top objection to pre-empt
- [ ] Specific promise / outcome
- [ ] Voice reference OR extracted voice from assets
- [ ] Funnel stage this asset serves

If missing → invoke `audience-mapping` or ask user. **Do not generate generic copy.**

## Copy formulas

| Formula | Structure | Best for |
|---------|-----------|----------|
| **PAS** | Problem → Agitate → Solve | Pain-aware audiences |
| **BAB** | Before → After → Bridge | Transformation offers |
| **AIDA** | Attention → Interest → Desire → Action | Broad awareness |
| **4Ps** | Promise → Picture → Proof → Push | Direct response BOFU |
| **FAB** | Features → Advantages → Benefits | Technical products |

Match formula to **awareness level** (see `audience-mapping` / b2c-psychographics).

## Headline archetypes (8)

1. Specific outcome + timeframe
2. Audience call-out + promise
3. Contrarian / pattern interrupt
4. Social proof lead
5. Question that names the pain
6. Number + mechanism
7. Before/after contrast
8. Risk reversal lead

Generate **3 variants** for hero/primary email using different archetypes.

## Email sequence architectures

| Sequence | Emails | Trigger | Load reference |
|----------|--------|---------|----------------|
| Welcome | 5 | Signup | `references/email-sequences.md` |
| Activation | 5–7 | Trial start | PLG critical path |
| Nurture | 7 | Lead magnet | MOFU education |
| Sales | 4 | BOFU segment | Close push |
| Re-engagement | 3 | 30d inactive | Win-back |
| Abandoned cart | 3 | Cart abandon | DTC |

One **primary CTA** per email. Plain-text founder voice often wins for activation.

## Landing page structure

```
Hero (headline + subhead + CTA + proof snippet)
→ Problem (customer words)
→ Solution (mechanism)
→ How it works (≤3 steps)
→ Proof (logos, testimonials, metrics)
→ Objection handling (FAQ)
→ Final CTA
```

See `references/landing-page-patterns.md` for BOFU comparison pages and pricing.

## CTA patterns

| Weak | Strong |
|------|--------|
| Learn more | Start 14-day trial — no card |
| Submit | Book 15-min fit call |
| Get started | Invite your team in Slack |

**Specificity wins.** Match CTA to stage (soft MOFU vs hard BOFU).

## Evaluator-optimizer loop (mandatory for high-stakes)

Applies to: **hero headline**, **primary activation email**, **main ad concept**.

### Step 1 — Generate 3 variants

Different headline archetypes or angles. Same facts, different framing.

### Step 2 — Critique each

| Criterion | Question |
|-----------|----------|
| Audience hero | Is the buyer/user the subject, not the product? |
| Specific promise | Is there a concrete outcome or behavior? |
| Objection | Does it pre-empt #1 objection from inventory? |
| CTA clarity | One obvious next action? |

Score ✅/❌ per variant.

### Step 3 — Refine strongest

Merge best elements. Remove unsubstantiated claims.

### Step 4 — Flag for compliance

- Stats (78% vs 12%) — must be verified or removed
- Competitor names — substantiation required
- Before/after, income, health claims

Handoff: Morgan → `compliance-agent` before external publish.

## Voice calibration

1. Ask for 2–3 examples (URLs, emails, tweets)
2. Extract: sentence length, jargon level, humor, formality
3. Mirror — don't parody
4. If repo has `brand-voice` skill, load it

## Ad creative (angles only in build table)

Full patterns: `references/ad-creative-patterns.md`. Output angles + hook lines; not 20 variants unless asked.

## Output format per asset

```markdown
### [Asset name] — [Stage]
**Formula:** PAS
**Variant selected:** v3 (evaluator pass)

**Copy:**
[final copy]

**Evaluator notes:**
- ✅ Audience hero (EM not product)
- ✅ Specific promise (3 posters in 48h)
- ⚠️ Verify cohort stat before send
```

## Do not use when

- No audience/objection context and user won't answer → discovery only
- User wants channel strategy → `channel-playbooks`
- User wants funnel diagram → `funnel-visualization`
- Brand positioning narrative only → different agent

## Anti-patterns

| Mistake | Fix |
|---------|-----|
| Feature-first hero | Lead with buyer outcome |
| Three equal CTAs | One primary |
| Fake urgency | Flag for compliance |
| Competitor bash without proof | Factual comparison only |
| Skipping evaluator on hero | Always 3 variants |

## Coordination

- **From audience-mapping:** Objections, voice, buyer hero
- **From channel-playbooks:** Format constraints (LinkedIn vs email)
- **From funnel-frameworks:** Stage awareness level
- **To compliance:** All external-facing copy
- **To funnel-metrics:** Claims that need cohort data

## References

- `references/email-sequences.md`
- `references/landing-page-patterns.md`
- `references/ad-creative-patterns.md`

## Quality checklist

- [ ] audience-mapping context used
- [ ] 3 variants + evaluator for high-stakes assets
- [ ] One CTA per email/section
- [ ] Claims flagged for verification
- [ ] Voice matched or user warned
