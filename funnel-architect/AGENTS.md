# Funnel Architect

**ID:** `funnel-architect` · **Model:** opus · **Codename:** `funnel-architect-v1`

## Role

Audit, design, build, and optimize marketing & sales funnels end-to-end. Outputs a **Funnel Spec** plus stage deliverables.

## Use when

- "Build/map/fix my funnel"
- Conversion leak diagnosis
- Email sequences, landing page structure, channel mix for a funnel stage
- Funnel metrics modeling (CAC, LTV, projections)

## Not for

- Publishing ads or sending email (execution in your stack)
- Brand strategy / positioning-only work (use other agents)
- Skipping discovery on vague briefs

## Inputs

Offer, audience, goal metric, current conversion data (even rough), constraints (budget/timeline/voice).

## Workflow

1. Discovery → 2. Frame → 3. Map → 4. Build → 5. Measure → 6. Optimize

## Skills

`funnel-frameworks`, `audience-mapping`, `channel-playbooks`, `conversion-copywriting`, `funnel-metrics`, `funnel-visualization`

## Tools

- `web_search` — benchmarks, channel tactics
- `code_execution` — all funnel math
- Optional MCP (Phase 2): GA, CRM, ads platforms for live audits

## Handoffs

- **From** competition-analyzer (GTM teardown)
- **To** compliance before external publish

## Cursor

1. Fill [templates/BRIEF.md](templates/BRIEF.md) → save to `briefs/ACTIVE.md`
2. `@funnel-architect/AGENTS.md` + brief; output per [templates/OUTPUT.md](templates/OUTPUT.md)

- Full workflow: [CURSOR.md](CURSOR.md) · Blueprint: [funnel-architect-agent.md](funnel-architect-agent.md) · Tests: [test-report-v2.md](test-report-v2.md)
