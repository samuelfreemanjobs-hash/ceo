# Funnel Architect

**An AI agent that audits, designs, builds, and optimizes marketing & sales funnels end-to-end.**

Codename: `funnel-architect-v1` · Architecture: **Single agent + Skills** (see _Building Effective AI Agents_, Anthropic 2025)

## What it does

1. **Discover** — audience, offer, goals, current state
2. **Map** — stage-by-stage funnel with channels, assets, KPIs
3. **Build** — copy, sequences, page structures, ad angles
4. **Measure** — metrics, benchmarks, instrumentation
5. **Optimize** — ICE-scored tests, leak identification

**Output:** Funnel Spec + modular artifacts → `docs/marketing/funnels/`

## Package layout

```
funnel-architect/
├── README.md
├── funnel-architect-agent.md    Full blueprint + worked example
├── prompts/system.md            API system parameter (canonical)
├── CLAUDE.md                    Claude Code auto-load
├── AGENTS.md                    @ mention card
├── test-report-v1.md
├── test-report-v1.1.md
└── skills/
    ├── funnel-frameworks/
    ├── audience-mapping/
    ├── channel-playbooks/
    ├── conversion-copywriting/
    ├── funnel-metrics/          (+ Python scripts)
    └── funnel-visualization/
```

## Deploy

| Surface | How |
|---------|-----|
| **CEO / Morgan** | Task tool → `subagent_type: funnel-architect` |
| **Cursor** | `@funnel-architect/AGENTS.md` + brief |
| **API** | `prompts/system.md` + enable web_search, code_execution |

## Skills (6)

| Skill | Phase |
|-------|-------|
| `audience-mapping` | Discovery |
| `funnel-frameworks` | Frame + map |
| `funnel-visualization` | Map |
| `channel-playbooks` | Map + build |
| `conversion-copywriting` | Build |
| `funnel-metrics` | Measure + optimize |

## Metrics scripts

```bash
python funnel-architect/skills/funnel-metrics/scripts/funnel_projection.py --json
python funnel-architect/skills/funnel-metrics/scripts/cac_ltv_calculator.py --cac 500 --ltv 2000 --json
```

## Handoffs

- **From** `competition-analyzer` — GTM teardown, funnel patterns
- **To** `compliance-agent` — external copy publish
- See `docs/marketing/HANDOFFS.md`

## Evolution

Phase 1: single agent (here) → Phase 2: MCP audit data → Phase 4: multi-agent only if volume > ~50 funnels/month.

Full blueprint: [`funnel-architect-agent.md`](funnel-architect-agent.md)
