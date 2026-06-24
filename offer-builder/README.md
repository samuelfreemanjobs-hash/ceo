# Offer Builder

**Dual-mode offer system:** Enterprise B2B commercial offers + Marketing GTM positioning.

| Mode | Entry | Package |
|------|-------|---------|
| **Enterprise** | `offer-director` | [`OFFER-BUILDER-SPEC.md`](OFFER-BUILDER-SPEC.md) |
| **Marketing** | `offer-builder` | [`offer-builder-agent.md`](offer-builder-agent.md) |

---

## Enterprise — full pipeline (7/7 agents installed)

```
offer-director → offer-discovery → [solution-architect ∥ offer-risk-compliance]
              → offer-pricing → offer-copywriter → offer-evaluator → rep review
```

```
Task → subagent_type: offer-director   # opportunity_id + rep_brief
```

**Schemas:** [`schemas/`](schemas/) · **Prompts:** [`prompts/offer-builder-system-prompts.md`](prompts/offer-builder-system-prompts.md)

---

## Marketing — Playbook v1.2

Package services into **specific, executable offers** (programs, sprints, retainers).

```
Task → subagent_type: offer-builder
Modes: flagship | stack | audit
```

Output: `docs/marketing/offers/` · Card: [`AGENTS.md`](AGENTS.md) · Standards: [`STANDARDS.md`](../STANDARDS.md)

---

## Package layout

```
offer-builder/
├── OFFER-BUILDER-SPEC.md      Enterprise architecture (canonical)
├── ROADMAP.md · METRICS.md
├── prompts/
│   ├── system.md              Marketing mode
│   ├── offer-builder-system-prompts.md
│   └── agents/                All 7 enterprise sub-agents
├── schemas/                   dossier, scope, pricing, risk, copy, eval, audit
├── skills/                    Enterprise + marketing skills
├── observability/
└── templates/                 Marketing BRIEF/OUTPUT
```

---

## Implementation status

| Component | Status |
|-----------|--------|
| All 7 enterprise agents + prompts | Installed |
| Enterprise skills (6) | Installed |
| Marketing skills (5) | Installed |
| MCP tool integrations | Pending wiring |
| docgen.render, approval.route | Pending |

See [`ROADMAP.md`](ROADMAP.md).
