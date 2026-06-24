# Offer Builder

**An AI agent that designs positioning, value propositions, and offer architecture — plus an Enterprise / Catalog pipeline for deal-desk quoting.**

Codename: `offer-builder-v1` · **Dual mode:** Marketing (single agent + Skills) · Enterprise (multi-agent + catalog tools)

## What it does

1. **Discover** — product, audience, competitive context, constraints
2. **Position** — category, differentiation, who it's for / not for
3. **Propose** — value proposition, proof ladder, messaging hierarchy
4. **Architect** — offer stack, tiers, bonuses, guarantees, risk reversal
5. **Package** — pricing model, anchoring, packaging decisions
6. **Validate** — ICE-scored tests, message experiments, open assumptions

**Output:** Offer Spec + modular artifacts → `docs/marketing/offers/`

## Enterprise / Catalog mode

Director-orchestrated pipeline for rep-driven deals:

1. **Discovery** → `dossier`
2. **Solution Architect** + Risk & Compliance (parallel) → `scope` + `risk_assessment`
3. **Pricing** → `pricing` (consumes `scope`)
4. **Copywriter** + **Evaluator** → approved offer

- Sub-agent prompts: [`prompts/offer-builder-system-prompts.md`](prompts/offer-builder-system-prompts.md)
- Solution Architect: [`prompts/agents/solution-architect.md`](prompts/agents/solution-architect.md)
- Schema: [`schemas/offer-schema.json`](schemas/offer-schema.json)
- Invoke SA: `Task → subagent_type: solution-architect`
- Invoke Discovery: `Task → subagent_type: offer-discovery`
- Invoke Risk: `Task → subagent_type: offer-risk-compliance`
- Invoke Copy: `Task → subagent_type: offer-copywriter`
- Invoke Evaluator: `Task → subagent_type: offer-evaluator`

**Pending:** Director, Pricing

## Package layout

```
offer-builder/
├── README.md
├── offer-builder-agent.md    Full blueprint
├── prompts/
│   ├── system.md                 Marketing mode (canonical)
│   ├── offer-builder-system-prompts.md   Enterprise sub-agent index
│   └── agents/
│       └── solution-architect.md
├── schemas/offer-schema.json
├── CURSOR.md                   Cursor operational workflow
├── CLAUDE.md                   Claude Code auto-load
├── AGENTS.md                   @ mention card
├── USER_PROFILE.md
├── worked-example.md
├── test-prompts.md
├── templates/BRIEF.md · OUTPUT.md
├── briefs/ACTIVE.md
├── learnings/OUTCOMES-LOG.md
├── observability/              trace schema + README
└── skills/
    ├── README.md
    ├── positioning-frameworks/
    ├── value-proposition-design/
    ├── offer-architecture/
    ├── pricing-packaging/
    ├── offer-validation/
    ├── solution-catalog/         Enterprise — SA agent
    └── offer-templates/        Enterprise — SA agent
```

## Deploy

| Surface | How |
|---------|-----|
| **CEO / Morgan** | Task tool → `subagent_type: offer-builder` |
| **Cursor** | [CURSOR.md](CURSOR.md) — `@offer-builder/AGENTS.md` + [templates/BRIEF.md](templates/BRIEF.md) |
| **API** | `prompts/system.md` + enable web_search |

## Skills (5)

| Skill | Phase |
|-------|-------|
| `positioning-frameworks` | Discover + position |
| `value-proposition-design` | Propose |
| `offer-architecture` | Architect |
| `pricing-packaging` | Package |
| `offer-validation` | Validate |

## Handoffs

- **From** `competition-analyzer` — white-space analysis, positioning gaps, GTM landscape
- **To** `funnel-architect` — offer + positioning for funnel design
- **To** `copy-agent` / `writer` — messaging hierarchy for asset production
- **To** `compliance-agent` — claims requiring substantiation
- See `docs/marketing/HANDOFFS.md`

## Evolution

Phase 1: single agent (here) → Phase 2: MCP pricing/CRM data → Phase 4: multi-agent only if volume > ~30 offer builds/month.

Full blueprint: [`offer-builder-agent.md`](offer-builder-agent.md)
