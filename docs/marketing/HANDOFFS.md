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
| LP or ad creative direction | **LP** / **Ad** agents *(pending)* | Teardown positioning, competitor LP URLs, user contrast pages |
| Battle card ready for external use | **Compliance** *(pending)* / Morgan | Artifact path, claims requiring substantiation, landmines list |
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
| Full profile, M&A, pricing deep dive, move alert | `competition-analyzer` (Scout — full skills) |
| Copy / content | `copy-agent` (interim: `writer`) |
| External publish | `compliance-agent` |

---

## Offer Builder → Enterprise pipeline

| Step | Agent | Output |
|------|-------|--------|
| Discovery | Discovery *(pending)* | `dossier` |
| Scope | **Solution Architect** (`solution-architect`) | `scope` → Pricing |
| Risk | Risk & Compliance *(pending)* | `risk_assessment` |

Schema: `offer-builder/schemas/offer-schema.json` · Prompts: `offer-builder/prompts/offer-builder-system-prompts.md`

---

## Offer Builder → downstream (Marketing)

| Trigger | Hand off to | Payload |
|---------|-------------|---------|
| Offer Spec complete, need funnel | **Funnel Architect** | Offer Spec path, ICP, primary conversion goal |
| Messaging hierarchy ready for assets | **Copywriter** (`copy-agent` / `writer`) | Messaging hierarchy, voice constraints, proof ladder |
| Claims need legal review | **Compliance** | Proof ladder rows marked Unverified; guarantee terms |
| Pricing intel gaps | **Scout** (`competition-analyzer`) | Competitor list, pricing-teardown request |

### Handoff JSON (from Scout → Offer Builder)

Already defined above (`from: competition-analyzer`, `to: offer-builder`).

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

## Pending agents (not yet installed)

| Agent | Receives from Scout / Offer Builder |
|-------|-------------------------------------|
| **Funnel Architect** | GTM teardown, funnel patterns *(installed)* |
| **Offer Builder** | White-space analysis, positioning gaps *(installed)* |
| **LP** | Competitor LP URLs, positioning contrast, Offer Spec |
| **Ad** | User-supplied ad artifacts + pattern analysis |

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
