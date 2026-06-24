# Funnel Architect — Skills Bundle

This directory contains the six SKILL.md files that power the Funnel Architect agent. Each follows the Anthropic Skill spec: YAML frontmatter (`name` + `description` as the trigger mechanism) plus a markdown body of operational instructions.

## What's in here

```
skills/
├── funnel-frameworks/SKILL.md        — Picks the right funnel shape for the business
├── audience-mapping/SKILL.md         — Forces specific audience definition before any build
├── channel-playbooks/SKILL.md        — Matches channels to business stage, ACV, and audience
├── conversion-copywriting/SKILL.md   — Writes stage-appropriate copy with evaluator loop
├── funnel-metrics/SKILL.md           — Defines, computes, and benchmarks numbers
└── funnel-visualization/SKILL.md     — Produces Mermaid diagrams and stage tables
```

Each skill has a `references/` folder for deep dives. References load on-demand (Progressive Disclosure) — SKILL.md bodies stay operational; depth lives in references.

**Bundled scripts:** `funnel-metrics/scripts/` — `funnel_projection.py`, `cac_ltv_calculator.py`, `cohort_retention.py`

## How the skills coordinate

```
Discovery   → audience-mapping (forces specifics)
Frame       → funnel-frameworks (picks shape)
Map         → funnel-visualization (renders structure)
Build       → conversion-copywriting (generates assets)
Measure     → funnel-metrics (defines KPIs, computes math)
Optimize    → funnel-metrics + audience-mapping (re-validates assumptions)
```

Skills are independently composable. `conversion-copywriting` checks that `audience-mapping` has run before generating. `funnel-frameworks` hands buyer-state stage names to `funnel-visualization`. `funnel-metrics` runs any time numbers appear, regardless of phase.

## Deployment

### Option 1: Claude.ai Project (fastest, v1)

1. Create a new Project
2. Paste system prompt from `../prompts/system.md` into Project instructions
3. Upload all six SKILL.md files to Project knowledge
4. Enable web search and code execution
5. Describe a business to start

### Option 2: API integration

1. System prompt as `system` parameter
2. Load skill bodies conditionally (descriptions = trigger criteria)
3. Enable `tool_use` for web_search and code_execution
4. Persist conversation state across turns

### Option 3: Claude Code / CEO orchestration

1. Skills at `funnel-architect/skills/` (canonical) or mirrored `.claude/skills/`
2. YAML frontmatter loads into discovery; bodies load on intent match
3. CEO: `Task → subagent_type: funnel-architect`

## Iteration loop

After deployment, run evaluation criteria from `../funnel-architect-agent.md` §7. Watch for:

1. **Undertriggering** — Fix: add trigger phrases to description; emphasize when to use
2. **Overtriggering** — Fix: add explicit "do not use when" guidance
3. **Generic output** — Fix: tighten operational instructions; add anti-patterns
4. **Missing reference depth** — Fix: populate `references/` files

Plan ~15–30 minutes per skill iteration. Most skills converge within 3–5 iterations against real prompts.

## Versioning

- `CHANGELOG.md` per skill — what changed and why
- Tag deployments (`v1.0`, `v1.1`)
- A/B test description changes — the description is the trigger

## See also

- Main blueprint: `../funnel-architect-agent.md`
- Cursor workflow: `../CURSOR.md`
- Test suite: `../test-prompts.md`
- Observability: `../observability/trace-schema.json`
