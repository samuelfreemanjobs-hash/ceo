# Marketing Department

**Status:** Initializing  
**Director:** Morgan (`marketing-director`)  
**Last updated:** 2025-06-24

The Marketing Dept is a hierarchical multi-agent team orchestrated by the Marketing Director. Specialists are installed progressively; the Director routes work and synthesizes final deliverables.

## Org chart

```
Marketing Director (Morgan)
├── Research Agent          [pending]
├── Brand & Creative Agent  [pending]
├── Copywriter Agent        [pending]
├── Media Planner Agent     [pending]
├── Analytics (Ana)         [installed]
└── Compliance Agent        [pending]
```

## Routing

| Request type | Entry point | Workflow |
|--------------|-------------|----------|
| Full campaign | Marketing Director | Full orchestration |
| Content / copy | Marketing Director → Copy | Specialist + compliance |
| Performance analysis | Marketing Director → Analytics | Direct |
| Ideation | Marketing Director | Collaborative → synthesize |
| Ops / status | Marketing Director → Analytics | Direct lookup |

## Output directories

- `docs/marketing/campaigns/` — Campaign decks and briefs
- `docs/marketing/content/` — Copy packs and content assets
- `docs/marketing/reports/` — Analysis and performance reports
- `docs/marketing/decisions/` — Decision logs and trade-off records

## Configuration

- Agent definition: `.github/agents/marketing-director.md`
- Orchestration config: `.github/data/marketing-director-config.yaml`
- Campaign brief template: `.github/templates/campaign-brief-tmpl.yaml`
- **Python runtime:** [`marketing-dept/`](../marketing-dept/README.md) — Anthropic API orchestrator with built-in specialists

## Rollout phases

1. **Phase 1** — Director + Copy + Compliance (content requests)
2. **Phase 2** — Add Research + Analytics (analysis, ideation, ops)
3. **Phase 3** — Add Creative + Media (full campaigns)
4. **Phase 4** — Optimization and evaluator agents

## Skills installed

| Skill | Status | Path |
|-------|--------|------|
| `brand-voice` | Template (fill in placeholders) | `.github/skills/brand-voice/SKILL.md` |
| `prohibited-claims-and-disclaimers` | Template (legal sign-off required) | `.github/skills/prohibited-claims-and-disclaimers/SKILL.md` |
| `marketing-plan-current-quarter` | Pending | — |
