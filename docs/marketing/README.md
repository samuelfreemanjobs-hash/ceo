# Marketing Department

**Status:** Initializing  
**Director:** Morgan (`marketing-director`)  
**Last updated:** 2025-06-24

The Marketing Dept is a hierarchical multi-agent team orchestrated by the Marketing Director. Specialists are installed progressively; the Director routes work and synthesizes final deliverables.

## Org chart

```
Marketing Director (Morgan)
├── Competition Analyzer (Scout)  [installed]
├── Funnel Architect              [installed]
├── Offer Director                [installed]  Enterprise B2B
├── Offer Builder                 [installed]  Marketing GTM
├── Research Agent              [pending]
├── Brand & Creative Agent      [pending]
├── Copywriter Agent            [pending]
├── Media Planner Agent         [pending]
├── Analytics (Ana)             [installed]
└── Compliance Agent            [pending]
```

## Routing

| Request type | Entry point | Workflow |
|--------------|-------------|----------|
| Full campaign | Marketing Director | Full orchestration |
| Content / copy | Marketing Director → Copy | Specialist + compliance |
| Competitive intelligence | Competition Analyzer (Scout) or Marketing Director | Profiles, battle cards, SWOT, landscape |
| Funnel design / audit / optimize | Funnel Architect or Marketing Director | Funnel Spec, stage copy, metrics |
| Positioning / offer / packaging | Offer Builder or Marketing Director | Offer Spec, proof ladder, pricing |
| Performance analysis | Marketing Director → Analytics | Direct |
| Ideation | Marketing Director | Collaborative → synthesize |
| Ops / status | Marketing Director → Analytics | Direct lookup |

## Output directories

- `docs/marketing/campaigns/` — Campaign decks and briefs
- `docs/marketing/content/` — Copy packs and content assets
- `docs/marketing/reports/` — Analysis and performance reports
- `docs/marketing/decisions/` — Decision logs and trade-off records
- `docs/marketing/research/profiles/` — Competitor profiles
- `docs/marketing/research/battle-cards/` — Sales battle cards
- `docs/marketing/research/alerts/` — Competitive move alerts
- `docs/marketing/funnels/` — Funnel Specs and funnel artifacts
- `docs/marketing/offers/` — Offer Specs and positioning artifacts

## Configuration

- Agent definitions: `.github/agents/marketing-director.md`, `.github/agents/competition-analyzer.md`, `.github/agents/funnel-architect.md`, `.github/agents/offer-builder.md`
- Orchestration config: `.github/data/marketing-director-config.yaml`
- Campaign brief template: `.github/templates/campaign-brief-tmpl.yaml`
- Battle card template: `.github/templates/battle-card-tmpl.yaml`
- **Python runtime:** [`marketing-dept/`](../marketing-dept/README.md) — Anthropic API orchestrator with built-in specialists

## Rollout phases

1. **Phase 1** — Director + Copy + Compliance (content requests)
2. **Phase 2** — Add Competition Analyzer + Funnel Architect + Research + Analytics (analysis, ideation, ops)
3. **Phase 3** — Add Creative + Media (full campaigns)
4. **Phase 4** — Optimization and evaluator agents

## Skills installed

| Skill | Status | Path |
|-------|--------|------|
| `brand-voice` | Template (fill in placeholders) | `.github/skills/brand-voice/SKILL.md` |
| `prohibited-claims-and-disclaimers` | Template (legal sign-off required) | `.github/skills/prohibited-claims-and-disclaimers/SKILL.md` |
| `marketing-plan-current-quarter` | Template (refresh each quarter) | `.github/skills/marketing-plan-current-quarter/SKILL.md` |
| `gtm-competitor-analysis` | Installed | `competition-analyzer/skills/gtm-competitor-analysis/SKILL.md` |
| `competitor-profiling` | Installed | `competition-analyzer/skills/competitor-profiling/SKILL.md` |
| `pricing-teardown` | Installed | `competition-analyzer/skills/pricing-teardown/SKILL.md` |
| `source-evaluation` | Installed | `competition-analyzer/skills/source-evaluation/SKILL.md` |
| `strategic-synthesis` | Installed | `competition-analyzer/skills/strategic-synthesis/SKILL.md` |
| `funnel-frameworks` | Installed | `funnel-architect/skills/funnel-frameworks/SKILL.md` |
| `audience-mapping` | Installed | `funnel-architect/skills/audience-mapping/SKILL.md` |
| `channel-playbooks` | Installed | `funnel-architect/skills/channel-playbooks/SKILL.md` |
| `conversion-copywriting` | Installed | `funnel-architect/skills/conversion-copywriting/SKILL.md` |
| `funnel-metrics` | Installed | `funnel-architect/skills/funnel-metrics/SKILL.md` |
| `funnel-visualization` | Installed | `funnel-architect/skills/funnel-visualization/SKILL.md` |
| `positioning-frameworks` | Installed | `offer-builder/skills/positioning-frameworks/SKILL.md` |
| `value-proposition-design` | Installed | `offer-builder/skills/value-proposition-design/SKILL.md` |
| `offer-architecture` | Installed | `offer-builder/skills/offer-architecture/SKILL.md` |
| `pricing-packaging` | Installed | `offer-builder/skills/pricing-packaging/SKILL.md` |
| `offer-validation` | Installed | `offer-builder/skills/offer-validation/SKILL.md` |
| `solution-catalog` | Installed | `offer-builder/skills/solution-catalog/SKILL.md` |
| `offer-templates` | Installed | `offer-builder/skills/offer-templates/SKILL.md` |

## Enterprise sub-agents (Offer Director)

| Agent | Status | Prompt |
|-------|--------|--------|
| **Offer Director** | Installed | `offer-builder/prompts/agents/director.md` |
| Offer Discovery | Installed | `offer-builder/prompts/agents/discovery.md` |
| Solution Architect | Installed | `offer-builder/prompts/agents/solution-architect.md` |
| Offer Risk & Compliance | Installed | `offer-builder/prompts/agents/risk-compliance.md` |
| **Offer Pricing** | Installed | `offer-builder/prompts/agents/pricing.md` |
| Offer Copywriter | Installed | `offer-builder/prompts/agents/copywriter.md` |
| Offer Evaluator | Installed | `offer-builder/prompts/agents/evaluator.md` |

Architecture: [`offer-builder/OFFER-BUILDER-SPEC.md`](../offer-builder/OFFER-BUILDER-SPEC.md)

## Offer Builder package (Marketing mode)

[`offer-builder/`](../offer-builder/README.md) — positioning, value props, offer architecture. Blueprint: `offer-builder-agent.md`.

## Funnel Architect package

[`funnel-architect/`](../funnel-architect/README.md) — audit, design, build, optimize funnels. Blueprint: `funnel-architect-agent.md` · Metrics scripts in `skills/funnel-metrics/scripts/`.

## Competition Analyzer package

Standalone deployable package: [`competition-analyzer/`](../competition-analyzer/README.md)

- `system-prompt.md` — API / Project instructions
- `CLAUDE.md` — Claude Code auto-load
- `worked-example.md` — methodology trace (Linear)
- `HANDOFFS.md` — cross-agent handoffs (Funnel Architect, Offer Builder, LP, Ad)
- **Cursor workflow:** `competition-analyzer/CURSOR.md` (brief → run → log)
