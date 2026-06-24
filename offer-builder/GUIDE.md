# Offer Builder Agent — guide

**Role:** Turn skills into a **packaged offer**: scope, **honest** promise, tiers, **objection** coverage — aligned to delivery capacity.

**Use when** creating new programs, sprints, or fixing a fuzzy "we do everything."

**Not for:** legal contract drafting; unbounded "results guaranteed."

**Tips:** The **out-of-scope** list sells trust. One **recommended** tier with why.

---

## Quick start

1. Fill [`templates/BRIEF.md`](templates/BRIEF.md) — Context, Outcomes, Proof, Business rules, Mode, Exclusions
2. `@offer-builder/AGENTS.md` + brief
3. Output → [`templates/OUTPUT.md`](templates/OUTPUT.md) → save under `docs/marketing/offers/`
4. Log ship: [`learnings/OUTCOMES-LOG.md`](learnings/OUTCOMES-LOG.md)

---

## Typical downstream chain

```
Offer Builder → Proposal → LP
```

| Step | Agent | When |
|------|-------|------|
| **Offer** (you are here) | `offer-builder` | Scope, promise, tiers, objections, price logic |
| **Proposal** *(pending)* | `proposal-agent` | Client-facing proposal doc from offer one-pager |
| **LP** *(pending)* | `lp-agent` | Landing page from offer + proposal messaging |

Alternate paths: **Funnel Architect** (funnel fit) · **Copywriter** / `writer` (assets) · **Compliance** (claims).

Full contracts: [HANDOFFS.md](../docs/marketing/HANDOFFS.md)

---

## Modes

| Mode | Best for |
|------|----------|
| `flagship` | One deep offer — new program or sprint |
| `stack` | Flagship + upsells / ladder |
| `audit` | Sharpen existing offer without full rewrite |

---

## What good output looks like

Matches [`templates/OUTPUT.md`](templates/OUTPUT.md):

1. **Name & one-line promise** — honest scope
2. **For who / not for** — ICP fit explicit
3. **What's included** — bullets + boundaries
4. **How it works** — steps + timeline + client inputs
5. **Proof** — or honest gap + what to collect next
6. **Pricing** — logic stated; tiers with one primary if stack mode
7. **Guarantee / terms** — only if defensible
8. **Objection handling** — 3–5
9. **Implementation checklist** — sales + delivery handoff

---

## Enterprise vs marketing

| Need | Agent |
|------|-------|
| Services / productized offer (this guide) | `offer-builder` |
| CRM commercial quote (SKUs, CLM, pricing engine) | `offer-director` |

---

## See also

- [AGENTS.md](AGENTS.md) — full Playbook v1.2 card
- [CURSOR.md](CURSOR.md) — Cursor workflow
- [STANDARDS.md](../STANDARDS.md) — proof, YMYL, guarantees
- [AGENTS-INDEX.md](../docs/marketing/AGENTS-INDEX.md) — which agent when
