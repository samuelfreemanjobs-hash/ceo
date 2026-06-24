# Offer Builder — instructions (Cursor)

**Agent:** Offer Builder (`offer-builder-v1`) · **Package:** `offer-builder/`

Design positioning, value propositions, and offer architecture. Output an **Offer Spec** with proof ladder, offer stack, and ICE-scored validation tests.

---

## 1. Prep

1. **Optional:** [USER_PROFILE.md](USER_PROFILE.md) — standing context (product, ICP, voice, constraints).
2. **Fill** [templates/BRIEF.md](templates/BRIEF.md) — product, audience, outcome, alternatives, constraints.
3. Save active brief to [briefs/ACTIVE.md](briefs/ACTIVE.md) for repeat sessions.

**From Scout:** If you have a competitive landscape or white-space analysis, attach or link `docs/marketing/research/` output — see [HANDOFFS.md](../docs/marketing/HANDOFFS.md).

---

## 2. Run

In Cursor chat:

```
@offer-builder/AGENTS.md + my brief in briefs/ACTIVE.md.
Mode: full build (or: reposition only | packaging only | validate only).
Output using templates/OUTPUT.md (Offer Spec).
Confirm each phase before proceeding.
```

**CEO orchestration:** Task tool → `subagent_type: offer-builder` with brief in prompt.

**Modes**

| Mode | Phases run |
|------|------------|
| `full` | 1–6 (default) |
| `reposition` | 1–3 (discovery + position + value prop) |
| `packaging` | 1, 4–5 (needs existing positioning) |
| `validate` | 1, 6 (assumption log + ICE tests) |

---

## 3. After

- Save Offer Spec → `docs/marketing/offers/{slug}-offer-spec-{date}.md`
- Funnel design → `funnel-architect` with Offer Spec attached
- Copy production → Morgan → `copy-agent` / `writer`
- Claims review → `compliance-agent` before external publish
- Log outcomes: [learnings/OUTCOMES-LOG.md](learnings/OUTCOMES-LOG.md)

---

## 4. API

- **System:** [prompts/system.md](prompts/system.md)
- **User message:** filled brief + Scout artifacts or pricing page URLs
- **Skills:** `offer-builder/skills/*/SKILL.md`

---

## 5. Trouble

| Problem | Fix |
|---------|-----|
| Generic "we help businesses" output | Re-run Phase 1 — add ICP, alternatives, switching trigger |
| No differentiation | Attach Scout landscape or list 3 named competitors |
| Pricing feels arbitrary | Require anchoring rationale and competitor price frame |
| Too many segments | Pick one primary ICP; note secondary as future spec |
| Claims without proof | Require proof ladder with Verified / Unverified tags |

---

## See also

- [AGENTS.md](AGENTS.md) — agent card for `@` mention
- [worked-example.md](worked-example.md) — B2B SaaS reposition trace
- [test-prompts.md](test-prompts.md) — eval suite
- [templates/BRIEF.md](templates/BRIEF.md) · [templates/OUTPUT.md](templates/OUTPUT.md)
