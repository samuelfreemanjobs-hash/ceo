# Offer Builder — Implementation Roadmap

Aligned with architecture spec §10.

## Phase 0 — Foundations

- Single agent + `offer-templates` + `pricing-policy`
- Tools: CRM read, catalog read, pricing engine, docgen
- Manual rep edit expected
- **Goal:** prove time savings on simple deals

## Phase 1 — Skills, not agents

- Add `legal-terms`, `competitive-positioning`, `customer-discovery` to single agent
- Evaluator as second call (not separate role yet)
- Observability + metrics pipeline + outcome linkage

## Phase 2 — Decompose

- Split **Pricing** and **Risk & Compliance** as specialists *(installed in this repo)*
- Parallel execution where independent
- Simple deals stay on single-agent path for cost

## Phase 3 — Full hierarchy *(current target)*

- All six specialists + Evaluator + Director *(installed)*
- Front-door router: simple → single path; complex/strategic → full hierarchy
- Outcome-linked eval drives prompt + skill iteration

## Phase 4 — Optimization

- MCP live integrations (CRM, CPQ, CLM)
- Model tier routing per agent
- Automated eval set regression on prompt changes

---

**This repo status:** Phase 3 structure installed; tool integrations pending MCP wiring.
