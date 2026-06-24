# Marketing Department — Agents Index

*Which agent when* — full orchestration map.

**Standards:** [STANDARDS.md](../STANDARDS.md) · **Handoffs:** [HANDOFFS.md](HANDOFFS.md) · **Getting started:** [GETTING-STARTED.md](GETTING-STARTED.md)

---

## Entry points

| User intent | Agent | `subagent_type` |
|-------------|-------|-----------------|
| Full marketing campaign | Marketing Director (Morgan) | `marketing-director` |
| Competitive intel / GTM / battlecards | Scout | `competition-analyzer` |
| Funnel design / audit / optimize | Funnel Architect | `funnel-architect` |
| **Services offer / productized package** | **Offer Builder** | `offer-builder` |
| **Client proposal from offer** | **Proposal Agent** | `proposal-agent` |
| **Landing page from offer + proposal** | **LP Agent** | `lp-agent` |
| B2B commercial quote (CRM) | Offer Director | `offer-director` |
| Performance analysis | Analytics (Ana) | `analytics` |
| Copy / content | Copywriter | `copy-agent` (interim: `writer`) |
| Pre-publish review | Compliance | `compliance-agent` |

---

## GTM chain (services)

```
Scout → Offer Builder → Proposal → LP → Compliance → Publish
```

| Step | Package | Output path |
|------|---------|-------------|
| Offer | `offer-builder/` | `docs/marketing/offers/` |
| Proposal | `proposal-agent/` | `docs/marketing/proposals/` |
| Landing page | `lp-agent/` | `docs/marketing/landing-pages/` |

**Example offer:** [offers/example-discovery-sprint-offer-2026-06-24.md](offers/example-discovery-sprint-offer-2026-06-24.md)

---

## Proposal Agent (marketing) — Playbook v1.0

**Package:** [`proposal-agent/`](../proposal-agent/)  
**When:** Offer one-pager ready → **client-facing proposal**  
**Formats:** `standard` · `short` · `executive`  
**Upstream:** `offer-builder` · **Downstream:** `lp-agent`

---

## LP Agent — Playbook v1.0

**Package:** [`lp-agent/`](../lp-agent/)  
**When:** Offer + proposal ready → **landing page copy**  
**Formats:** `full` · `minimal` · `tiered`  
**Upstream:** `offer-builder` + `proposal-agent` · **Downstream:** `compliance-agent`

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

## Supporting agents

| Agent | Status | Notes |
|-------|--------|-------|
| Proposal | **Installed** | — |
| LP | **Installed** | — |
| Copywriter | **Installed** | Card + `marketing-dept --phase1` |
| Compliance | **Installed** | Card + `marketing-dept --phase1` |
| Media Planner | Pending | `marketer` (Mark) |
| Research | Pending | Scout for competitive |
| Creative | Pending | — |
| Ad | Pending | — |

---

## Package quick links

| Package | Agent card | Guide | Output path |
|---------|------------|-------|-------------|
| lp-agent | `lp-agent/AGENTS.md` | `lp-agent/GUIDE.md` | `docs/marketing/landing-pages/` |
| proposal-agent | `proposal-agent/AGENTS.md` | `proposal-agent/GUIDE.md` | `docs/marketing/proposals/` |
| competition-analyzer | `competition-analyzer/AGENTS.md` | — | `docs/marketing/research/` |
| funnel-architect | `funnel-architect/AGENTS.md` | — | `docs/marketing/funnels/` |
| offer-builder | `offer-builder/AGENTS.md` | `offer-builder/GUIDE.md` | `docs/marketing/offers/` |
| marketing-director | `.github/agents/marketing-director.md` | — | `docs/marketing/campaigns/` |
