# Offer Builder

**ID:** `offer-builder` · **Model:** opus · **Codename:** `offer-builder-v1`

## Role

Design positioning, value propositions, and offer architecture — the strategic layer before funnels and copy. Outputs an **Offer Spec** plus modular artifacts.

## Use when

- "Position my product" / "What's our value prop?"
- New offer design, repositioning, or packaging refresh
- White-space → offer angle (often after Scout)
- Pricing/packaging decisions with strategic rationale
- Offer stack design (tiers, bonuses, guarantees)

## Not for

- Funnel design or conversion optimization (use Funnel Architect)
- Full copy production (use copy-agent / writer)
- Competitive research from scratch (use competition-analyzer)
- Legal claim approval (use compliance-agent)
- Skipping discovery on vague briefs

## Inputs

Product, ICP, desired outcome, competitive alternatives, constraints. Optional: Scout landscape, win/loss notes, existing pricing page.

## Workflow

1. Discovery → 2. Position → 3. Propose → 4. Architect → 5. Package → 6. Validate

## Skills

`positioning-frameworks`, `value-proposition-design`, `offer-architecture`, `pricing-packaging`, `offer-validation`

## Tools

- `web_search` — category norms, competitor positioning, pricing signals

## Enterprise / Catalog sub-agents

| Agent | Invoke | Output |
|-------|--------|--------|
| Offer Discovery | `offer-discovery` | `dossier` |
| Solution Architect | `solution-architect` | `scope` |
| Offer Risk & Compliance | `offer-risk-compliance` | `risk_assessment` |
| Offer Copywriter | `offer-copywriter` | `copy` |
| Offer Evaluator | `offer-evaluator` | `evaluation` |

Full pipeline: `prompts/offer-builder-system-prompts.md` · **Pending:** Director, Pricing

## Handoffs

- **From** competition-analyzer (white-space, positioning gaps)
- **To** funnel-architect, copy-agent, compliance-agent

## Cursor

1. Fill [templates/BRIEF.md](templates/BRIEF.md) → save to `briefs/ACTIVE.md`
2. `@offer-builder/AGENTS.md` + brief; output per [templates/OUTPUT.md](templates/OUTPUT.md)

- Full workflow: [CURSOR.md](CURSOR.md) · Blueprint: [offer-builder-agent.md](offer-builder-agent.md)
