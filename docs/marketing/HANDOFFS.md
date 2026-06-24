# Marketing Department — Agent Handoffs

Cross-agent handoff contracts for the Marketing Dept and adjacent GTM workflows.

**See also:** [Marketing README](./README.md) · [Competition Analyzer package](../competition-analyzer/README.md)

---

## Competition Analyzer (Scout) → downstream

| Trigger | Hand off to | Payload |
|---------|-------------|---------|
| White space identified in GTM landscape | **Offer Builder** (`offer-builder`) | Landscape excerpt, white-space hypothesis, confidence tags, open questions |
| Funnel pattern worth mapping or countering | **Funnel Architect** (`funnel-architect`) | GTM teardown funnel section, competitor URLs, stage rates, P0 verification gaps |
| Positioning / offer angle from landscape | **Offer Builder** (`offer-builder`) | White-space section, implications for us |
| LP or ad creative direction | **LP** (`lp-agent`) / **Ad** (`ad-agent`) | Teardown positioning, competitor LP URLs, user contrast pages |
| Battle card ready for external use | **Compliance** (`compliance-agent`) / Morgan | Artifact path, claims requiring substantiation, landmines list |
| Deep profile needed after GTM pass | Scout (same agent, different skill) | Load `competitor-profiling` + `pricing-teardown` |

### Handoff JSON (to Morgan or future agents)

```json
{
  "from": "competition-analyzer",
  "to": "offer-builder",
  "summary": "2-3 sentences",
  "artifact_path": "docs/marketing/research/...",
  "p0_items": ["..."],
  "open_questions": ["..."],
  "confidence_highlights": ["Confirmed: ...", "Unverified: ..."]
}
```

---

## Morgan (Marketing Director) → specialists

| Request signal | Route to |
|----------------|----------|
| GTM landscape, funnel teardown, white space, monitoring | `competition-analyzer` (GTM mode) |
| Funnel design, audit, build, optimize | `funnel-architect` |
| Positioning, value prop, offer stack, packaging | `offer-builder` |
| Services offer → proposal → landing page | `offer-builder` → `proposal-agent` → `lp-agent` |
| Full profile, M&A, pricing deep dive, move alert | `competition-analyzer` (Scout — full skills) |
| Copy / content | `copy-agent` (interim: `writer`; Python: `marketing-dept --phase1`) |
| External publish | `compliance-agent` (Python: `marketing-dept --phase1`) |

---

## Enterprise Offer Builder — full pipeline

Entry: **`offer-director`** with `opportunity_id` + `rep_brief`

| Step | Agent | `subagent_type` |
|------|-------|-----------------|
| Supervisor | Offer Director | `offer-director` |
| Discovery | Offer Discovery | `offer-discovery` |
| Scope | Solution Architect | `solution-architect` |
| Risk | Offer Risk & Compliance | `offer-risk-compliance` |
| Pricing | Offer Pricing | `offer-pricing` |
| Copy | Offer Copywriter | `offer-copywriter` |
| QA | Offer Evaluator | `offer-evaluator` |

Spec: `offer-builder/OFFER-BUILDER-SPEC.md` · **7/7 agents installed** · MCP tool wiring pending

---

## Offer Builder → downstream (Marketing)

Typical chain: **Offer Builder → Proposal → LP**.

| Trigger | Hand off to | Payload |
|---------|-------------|---------|
| Offer one-pager complete, need client proposal | **Proposal** (`proposal-agent`) | `docs/marketing/offers/...`, scope, tiers, price logic, objection pre-empts |
| Offer + proposal ready for web | **LP** (`lp-agent`) | Offer artifact, proposal §1/§5/§6/§9, headline/proof bullets, primary tier, CTA |
| Need funnel / channel fit | **Funnel Architect** | Offer path, ICP, primary conversion goal |
| Messaging ready for assets | **Copywriter** (`copy-agent` / `writer`) | Headline direction, proof bullets, voice constraints |
| Claims need legal review | **Compliance** | Unverified claims, guarantee terms, YMYL flags |
| Pricing intel gaps | **Scout** (`competition-analyzer`) | Competitor list, pricing-teardown request |

### Handoff JSON (from Scout → Offer Builder)

Already defined above (`from: competition-analyzer`, `to: offer-builder`).

### Handoff JSON (from Offer Builder → Proposal)

```json
{
  "from": "offer-builder",
  "to": "proposal-agent",
  "summary": "2-3 sentences",
  "artifact_path": "docs/marketing/offers/...",
  "recommended_format": "standard",
  "client_context": {
    "company": "...",
    "personalization_notes": "..."
  },
  "compliance_flags": ["..."]
}
```

### Handoff JSON (from Offer Builder → Funnel Architect)

```json
{
  "from": "offer-builder",
  "to": "funnel-architect",
  "summary": "2-3 sentences",
  "artifact_path": "docs/marketing/offers/...",
  "icp": "...",
  "primary_conversion_goal": "...",
  "positioning_statement": "...",
  "open_questions": ["..."]
}
```

---

### Handoff JSON (from Proposal → LP)

```json
{
  "from": "proposal-agent",
  "to": "lp-agent",
  "summary": "2-3 sentences",
  "offer_path": "docs/marketing/offers/...",
  "proposal_path": "docs/marketing/proposals/...",
  "primary_cta": { "label": "Book a call", "url": "https://..." },
  "format": "full",
  "compliance_flags": ["..."]
}
```

---

## Agent status

| Agent | Status |
|-------|--------|
| Funnel Architect | **Installed** |
| Offer Builder | **Installed** |
| Proposal | **Installed** |
| LP | **Installed** |
| Copywriter | **Installed** (card + Python Phase 1) |
| Compliance | **Installed** (card + Python Phase 1) |
| Ad | **Installed** | `ad-agent` |

---

## After a run (Cursor workflow)

Log outcomes: `competition-analyzer/learnings/OUTCOMES-LOG.md`  
Brief template: `competition-analyzer/templates/BRIEF.md`  
Cursor instructions: `competition-analyzer/CURSOR.md`

---

## CEO (Cleo) routing

| User intent | Entry point |
|-------------|-------------|
| Competitive GTM / battlecard / white space | `competition-analyzer` directly, or Morgan if part of campaign |
| Funnel design, audit, build, optimize | `funnel-architect` directly, or Morgan for coordinated work |
| Positioning, value prop, offer design, packaging | `offer-builder` directly, or Morgan for coordinated work |
| Full marketing campaign | `marketing-director` |
