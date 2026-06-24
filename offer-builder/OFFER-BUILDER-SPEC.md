# Offer Builder — Architecture & Implementation Spec

> Hierarchical multi-agent system that turns a sales opportunity into a defensible, policy-compliant, customer-ready commercial offer.

**Codename:** `offer-builder-enterprise-v1`  
**Canonical prompts:** [`prompts/offer-builder-system-prompts.md`](prompts/offer-builder-system-prompts.md)  
**Schemas:** [`schemas/`](schemas/)

---

## 0. Scope

**B2B commercial offer (proposal/quote) builder:** customer + opportunity → customized scope + pricing + terms + narrative, ready for rep review and delivery.

Domain-agnostic architecture — Skills, tools, and prompts swap for job offers, real-estate, RFP responses, etc.

**Dual deployment in this repo:**

| Mode | Entry | Use case |
|------|-------|----------|
| **Enterprise** | `offer-director` | B2B deal desk — CRM, catalog, pricing engine |
| **Marketing** | `offer-builder` | GTM positioning, value props, offer stacks |

---

## 1. Architecture decision

| Dimension | Assessment | Implication |
|-----------|------------|-------------|
| Control | Moderate-high; legal/financial commitment | Hierarchical + audit trail + human-in-loop |
| Complexity | Multi-domain, predictable structure | Multi-agent justified |
| Resources | High-value deals; minutes OK | Specialist agents + evaluator |
| Failure cost | Errors → contracts | Hard policy in code/skills; mandatory evaluator |

**Pattern:** Hierarchical multi-agent, sequential workflow with parallel Discovery tail ‖ SA ‖ Risk, evaluator-optimizer loop (max 3), mandatory human review before send.

**MVP path:** Single agent + Skills → decompose when metrics plateau (Phases 0–3 in [`ROADMAP.md`](ROADMAP.md)).

---

## 2. Workflow

```
TRIGGER: opportunity_id + rep_brief
    → Offer Director (supervisor)
    → Discovery → dossier
    → [Solution Architect ∥ Risk & Compliance]  (parallel)
    → Pricing (needs scope)
    → Copywriter (synthesizes)
    → Evaluator (loop ≤3 → escalate_human)
    → HUMAN: rep + manager/legal if thresholds
    → docgen.render → PDF + DOCX + CRM
```

See mermaid in [`prompts/offer-builder-system-prompts.md`](prompts/offer-builder-system-prompts.md).

---

## 3. Agent roster

| Agent | `subagent_type` | Output | Model |
|-------|-----------------|--------|-------|
| Offer Director | `offer-director` | offer + audit_log | opus |
| Discovery | `offer-discovery` | dossier | sonnet |
| Solution Architect | `solution-architect` | scope | opus |
| Pricing | `offer-pricing` | pricing | opus |
| Risk & Compliance | `offer-risk-compliance` | `risk` | opus |
| Copywriter | `offer-copywriter` | `narrative` | sonnet |
| Evaluator | `offer-evaluator` | `evaluator_result` | sonnet |

**No generative authority:** Pricing (numbers), Solution Architect (SKUs), Discovery (facts), Risk (clauses).

---

## 4. Skills (Enterprise)

| Skill | Used by |
|-------|---------|
| `customer-discovery` | Discovery, Director |
| `solution-catalog` | Solution Architect |
| `pricing-policy` | Pricing, Director |
| `legal-terms` | Risk & Compliance |
| `offer-templates` | Director, SA, Copywriter |
| `competitive-positioning` | Copywriter, Pricing (strategic discount) |

Marketing skills (`positioning-frameworks`, etc.) remain on `offer-builder` only.

---

## 5. Tools / MCP

| Tool | Used by |
|------|---------|
| `crm.opportunity.get`, `crm.account.get`, `crm.activity.search` | Discovery, Director |
| `gong.transcript.search`, `email.thread.read` | Discovery |
| `catalog.product.search`, `catalog.dependencies.check` | Solution Architect |
| `pricing_engine.get_rates`, `.segment_discount`, `.apply_discount` | Pricing |
| `clm.clauses.search`, `clm.precedent.search` | Risk |
| `compliance.jurisdiction.check` | Risk |
| `deals.history.search` | Pricing, SA, Director |
| `docgen.render` | Director (terminal) |
| `approval.route` | Director |

Tool rules: structured JSON, pagination, ~25K cap per response, args+results logged.

---

## 6. Evaluator rubric

Six dimensions, 0–3 each, minimum pass = 2. See [`prompts/agents/evaluator.md`](prompts/agents/evaluator.md).

1. Completeness  
2. Internal consistency  
3. Policy compliance  
4. Factual grounding  
5. Tone fit  
6. Differentiation  

Max 3 cycles → `escalate_human` with `diff_summary`.

---

## 7. Observability

Per offer: per-agent traces, decision events (discounts, escalations, evaluator routes), cross-agent parent span, outcome linkage `offer_id → CRM → close/loss`.

See [`observability/`](observability/) · [`METRICS.md`](METRICS.md).

---

## 8. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Fabricated price/SKU | Engine + catalog tools only; schemas enforce traceability |
| Discount drift | pricing_engine SOT; aggregate discount metric |
| Legal exposure | clm.clauses.search only; custom → legal |
| Claim hallucination | dossier sources; evaluator dimension 4 |
| Token cost | Router: simple → single agent; 25K tool cap |
| Bad auto-send | **Never auto-send** — rep review mandatory |

---

## 9. Open design choices (Appendix A)

1. Launch deal types: **new-logo + renewal** first; RFP + pilot Phase 2  
2. CRM SOR: Salesforce vs HubSpot — drives Discovery tools  
3. CLM + pricing engine: existing vs build — Phase 0 scope  
4. Approval routing: Slack vs CRM vs dedicated  
5. Output: PDF + DOCX; DocuSign-ready TBD  
6. Model tiers: sonnet Discovery/Copy; opus Director/Pricing/Risk/SA  
7. Auto-send floor: **default never**

---

## 10. Explicitly not in design

- Swarm/peer-to-peer (audit needs favor supervisor)  
- Dynamic agent generation (experimental)  
- Agent-to-customer direct interaction (internal drafts only)

---

_Full implementation phases: [`ROADMAP.md`](ROADMAP.md) · Metrics: [`METRICS.md`](METRICS.md)_
