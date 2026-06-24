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

- **One-line promise** — qualified, delivery-honest
- **In / out of scope** — explicit; out-of-scope builds trust
- **Client inputs required** — boring ops detail included
- **One primary tier** — recommended with rationale
- **Objection pre-empts** — price, time, fit, trust
- **Self-audit** passed (see [AGENTS.md](AGENTS.md))

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
