# Offer Builder

**An AI agent that designs positioning, value propositions, and offer architecture — the strategic layer before funnels and copy.**

Codename: `offer-builder-v1` · Architecture: **Single agent + Skills** (see _Building Effective AI Agents_, Anthropic 2025)

## What it does

1. **Discover** — product, audience, competitive context, constraints
2. **Position** — category, differentiation, who it's for / not for
3. **Propose** — value proposition, proof ladder, messaging hierarchy
4. **Architect** — offer stack, tiers, bonuses, guarantees, risk reversal
5. **Package** — pricing model, anchoring, packaging decisions
6. **Validate** — ICE-scored tests, message experiments, open assumptions

**Output:** Offer Spec + modular artifacts → `docs/marketing/offers/`

## Package layout

```
offer-builder/
├── README.md
├── offer-builder-agent.md    Full blueprint
├── prompts/system.md         API system parameter (canonical)
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
    └── offer-validation/
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
