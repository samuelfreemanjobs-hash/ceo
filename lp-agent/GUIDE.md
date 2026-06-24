# LP Agent — guide

**Role:** Convert **offer + proposal** artifacts into **landing page copy** ready for your CMS or static site.

**Chain:** Offer Builder → Proposal → **LP**

---

## Quick start

1. Finish offer → `docs/marketing/offers/{slug}-offer-{date}.md`
2. Finish proposal → `docs/marketing/proposals/{slug}-proposal-{date}.md`
3. Fill [`templates/BRIEF.md`](templates/BRIEF.md) — paths, primary CTA, format
4. `@lp-agent/AGENTS.md` + brief
5. Save → `docs/marketing/landing-pages/{slug}-lp-{date}.md`

---

## What changes from proposal → LP

| Proposal (document) | LP (web page) |
|---------------------|---------------|
| Executive summary | Hero headline + subhead |
| Your situation | Problem section (short) |
| Proposed solution | Solution + what's included |
| Investment | Pricing block (primary tier) |
| FAQ / objections | FAQ accordion copy |
| Next steps | Primary + secondary CTA |

---

## Formats

- **`full`** — hero, problem, solution, proof, pricing, FAQ, CTA (default)
- **`minimal`** — hero, 3 proof bullets, single CTA
- **`tiered`** — tier comparison table when offer mode = `stack`

---

## Downstream

| Agent | When |
|-------|------|
| **compliance-agent** | Before publish — guarantees, YMYL, stats |
| **writer** | Ad/email hooks from hero |
| **funnel-architect** | Page fits in multi-step funnel |

---

## Not for

- Enterprise B2B catalog quotes → `offer-director`
- Changing price or scope → back to `offer-builder`
- Full site IA → `funnel-architect` first
