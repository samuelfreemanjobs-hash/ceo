# Proposal Agent — guide

**Role:** Convert an internal **offer one-pager** into a **client-facing proposal** the rep can send.

**Chain:** Offer Builder → **Proposal** → LP

---

## Quick start

1. Finish Offer Builder → artifact at `docs/marketing/offers/{slug}-offer-{date}.md`
2. Fill [`templates/BRIEF.md`](templates/BRIEF.md) — offer path, client name, format, personalization
3. `@proposal-agent/AGENTS.md` + brief
4. Save → `docs/marketing/proposals/{slug}-proposal-{date}.md`

---

## What changes from offer → proposal

| Offer (internal) | Proposal (client-facing) |
|------------------|--------------------------|
| For who / not for | "Your situation" + fit framing |
| What's included | "Proposed solution" + deliverables table |
| How it works | Timeline with client responsibilities |
| Pricing + logic | "Investment" — clear, confident, same numbers |
| Objection handling | FAQ or "Common questions" section |
| Implementation checklist | "Next steps" + signature block |

---

## Formats

- **`standard`** — full 9-section proposal (default)
- **`short`** — 2–3 pages: summary, scope, investment, next steps
- **`executive`** — 1 page: outcome, investment, decision ask

---

## Downstream

| Agent | When |
|-------|------|
| **LP** *(pending)* | Offer + proposal ready for landing page |
| **compliance-agent** | YMYL, guarantees, regulated claims |
| **writer** | Cover email to accompany PDF |

---

## Not for

- Enterprise B2B catalog quotes → `offer-director`
- Changing price or scope → back to `offer-builder`
