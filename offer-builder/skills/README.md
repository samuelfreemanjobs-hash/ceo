# Offer Builder — Skills Bundle

Five SKILL.md files power the Offer Builder agent. Each follows the Anthropic Skill spec: YAML frontmatter (`name` + `description` as trigger) plus operational markdown body.

## Coordination

```
Discovery   → positioning-frameworks (forces competitive frame)
Position    → positioning-frameworks (category + differentiation)
Propose     → value-proposition-design (claims + proof ladder)
Architect   → offer-architecture (stack, tiers, guarantees)
Package     → pricing-packaging (model, anchor, packaging)
Validate    → offer-validation (ICE tests, assumptions)
```

### Enterprise / Catalog (Solution Architect)

```
Discovery dossier → solution-catalog (need→family) → catalog.product.search
                 → catalog.dependencies.check → offer-templates (milestones)
                 → scope JSON → Pricing
```

Skills: `solution-catalog`, `offer-templates` — see `prompts/agents/solution-architect.md`

### Enterprise / Catalog (full pipeline)

```
offer-discovery → dossier
              → [solution-architect ∥ offer-risk-compliance]
              → scope + risk_assessment → pricing (pending)
              → offer-copywriter → offer-evaluator
```

Skills: `solution-catalog`, `offer-templates`, `competitive-positioning`

## Deployment

Mirror to `.github/skills/`, `.claude/skills/`, `.gemini/skills/`, `.ai/skills/` for platform discovery.

CEO: `Task → subagent_type: offer-builder`
