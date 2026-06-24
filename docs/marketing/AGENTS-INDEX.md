# Marketing Department — Agents Index

*Which agent when* — full orchestration map.

**Standards:** [STANDARDS.md](../STANDARDS.md) · **Handoffs:** [HANDOFFS.md](HANDOFFS.md)

---

## Entry points

| User intent | Agent | `subagent_type` |
|-------------|-------|-----------------|
| Full marketing campaign | Marketing Director (Morgan) | `marketing-director` |
| Competitive intel / GTM / battlecards | Scout | `competition-analyzer` |
| Funnel design / audit / optimize | Funnel Architect | `funnel-architect` |
| **Services offer / productized package** | **Offer Builder** | `offer-builder` |
| B2B commercial quote (CRM) | Offer Director | `offer-director` |
| Performance analysis | Analytics (Ana) | `analytics` |

---

## Offer Builder (marketing) — Playbook v1.2

**Package:** [`offer-builder/`](../offer-builder/)  
**When:** Programs, sprints, retainers, productized services — **offer one-pager**, tier stack, messaging  
**Modes:** `flagship` · `stack` · `audit`  
**Not for:** Enterprise catalog quoting (use `offer-director`)

---

## Offer Director (enterprise)

**Package:** [`offer-builder/OFFER-BUILDER-SPEC.md`](../offer-builder/OFFER-BUILDER-SPEC.md)  
**When:** CRM opportunity → scope + pricing + terms + narrative  
**Sub-agents:** discovery, solution-architect, risk, pricing, copywriter, evaluator

---

## Supporting agents (pending / interim)

| Agent | Status | Interim |
|-------|--------|---------|
| Copywriter | Pending | `writer` (Casey) |
| Compliance | Pending | self-review vs `prohibited-claims-and-disclaimers` |
| Media Planner | Pending | `marketer` (Mark) |
| Research | Pending | Scout for competitive; general TBD |

---

## Package quick links

| Package | Agent card | Output path |
|---------|------------|-------------|
| competition-analyzer | `competition-analyzer/AGENTS.md` | `docs/marketing/research/` |
| funnel-architect | `funnel-architect/AGENTS.md` | `docs/marketing/funnels/` |
| offer-builder | `offer-builder/AGENTS.md` | `docs/marketing/offers/` |
| marketing-director | `.github/agents/marketing-director.md` | `docs/marketing/campaigns/` |
