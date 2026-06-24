# Funnel Architect — instructions (Cursor)

**Agent:** Funnel Architect (`funnel-architect-v1`) · **Package:** `funnel-architect/`

Audit, design, build, and optimize marketing & sales funnels. Output a **Funnel Spec** with stage copy, metrics, and ICE-scored tests.

---

## 1. Prep

1. **Optional:** [USER_PROFILE.md](USER_PROFILE.md) — standing context (offer, ICP, voice, constraints).
2. **Fill** [templates/BRIEF.md](templates/BRIEF.md) — offer, audience, goal, current rates, constraints.
3. Save active brief to [briefs/ACTIVE.md](briefs/ACTIVE.md) for repeat sessions.

**From Scout:** If you have a competitive GTM teardown, attach or link `docs/marketing/research/` output — see [HANDOFFS.md](../docs/marketing/HANDOFFS.md).

---

## 2. Run

In Cursor chat:

```
@funnel-architect/AGENTS.md + my brief in briefs/ACTIVE.md.
Mode: full build (or: audit only | map only | copy refresh | metrics only).
Output using templates/OUTPUT.md (Funnel Spec).
Confirm each phase before proceeding.
Use code_execution for all funnel math.
```

**CEO orchestration:** Task tool → `subagent_type: funnel-architect` with brief in prompt.

**Modes**

| Mode | Phases run |
|------|------------|
| `full` | 1–6 (default) |
| `audit` | 1–2, 5–6 (existing funnel + leaks) |
| `map` | 1–3 |
| `copy` | 1, 4 (needs voice references) |
| `metrics` | 1, 5–6 |

---

## 3. After

- Save Funnel Spec → `docs/marketing/funnels/{slug}-funnel-spec-{date}.md`
- External copy → Morgan → `compliance-agent` before publish
- Log outcomes: [learnings/OUTCOMES-LOG.md](learnings/OUTCOMES-LOG.md)
- Append observability trace per [observability/README.md](observability/README.md) (if instrumented)

---

## 4. API

- **System:** [prompts/system.md](prompts/system.md)
- **User message:** filled brief + any analytics screenshots or CRM exports
- **Skills:** `funnel-architect/skills/*/SKILL.md` + `references/` on demand

---

## 5. Trouble

| Problem | Fix |
|---------|-----|
| Generic AIDA output | Re-run Phase 1 — add ICP, rates, competitor |
| Wrong channels | Specify ACV, motion (PLG vs sales-led), timeline |
| Math doesn't match | Require agent to rerun `funnel_projection.py` |
| Copy feels off-brand | Paste 2–3 voice examples in brief |
| Too long | Ask for `map only` or single-stage build |

---

## See also

- [AGENTS.md](AGENTS.md) — agent card for `@` mention
- [worked-example.md](worked-example.md) — B2B SaaS PLG session trace
- [test-prompts.md](test-prompts.md) — v1 eval suite (10 prompts)
- [templates/BRIEF.md](templates/BRIEF.md) · [templates/OUTPUT.md](templates/OUTPUT.md)
