# Marketing Department — Agent Handoffs

Cross-agent handoff contracts for the Marketing Dept and adjacent GTM workflows.

**See also:** [Marketing README](./README.md) · [Competition Analyzer package](../competition-analyzer/README.md)

---

## Competition Analyzer (Scout) → downstream

| Trigger | Hand off to | Payload |
|---------|-------------|---------|
| White space identified in GTM landscape | **Offer Builder** *(pending)* | Landscape excerpt, white-space hypothesis, confidence tags, open questions |
| Funnel pattern worth mapping or countering | **Funnel Map** *(pending)* | GTM teardown funnel section, competitor URLs, P0 verification gaps |
| Positioning / offer angle from landscape | **Offer Builder** *(pending)* | White-space section, implications for us |
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
| GTM landscape, funnel teardown, white space, monitoring | `competition-analyzer` (GTM mode — `gtm-competitor-analysis` skill) |
| Full profile, M&A, pricing deep dive, move alert | `competition-analyzer` (Scout — full skills) |
| Copy / content | `copy-agent` (interim: `writer`) |
| External publish | `compliance-agent` |

---

## Pending agents (not yet installed)

| Agent | Receives from Scout |
|-------|---------------------|
| **Offer Builder** | White-space analysis, positioning gaps |
| **Funnel Map** | Public funnel teardowns, CTA patterns |
| **LP** | Competitor LP URLs, positioning contrast |
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
| Full marketing campaign | `marketing-director` |
