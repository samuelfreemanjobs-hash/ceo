# Competitor Analysis Agent — instructions (Cursor)

**Agent:** Scout (`competition-analyzer`) · **Package:** `competition-analyzer/`

Compare **public** GTM: positioning, funnels, pricing *signals*, and **user-supplied** ad evidence. Output **landscape**, **teardown**, or **monitoring checklist** with **P0/P1** priorities and explicit unknowns.

---

## 1. Prep

1. **Optional:** [USER_PROFILE.md](USER_PROFILE.md) — your offer, ICP, and comparison frame (how you want competitors evaluated against *you*).
2. **Fill** [templates/BRIEF.md](templates/BRIEF.md) — competitor list + URLs; paste ad/landing evidence if you have it.
3. **Choose mode** in the brief: `teardown` | `landscape` | `monitoring`.

Save an active brief to [briefs/ACTIVE.md](briefs/ACTIVE.md) when running repeat passes.

---

## 2. Run

In Cursor chat:

- `@competition-analyzer/AGENTS.md` (or `@.github/agents/competition-analyzer.md`) **+** paste your filled brief (or reference `briefs/ACTIVE.md`).
- **Ads:** attach screenshots, exports, or state you'll use Ad Library **manually** — do *not* ask the model to invent ad copy.

**Example prompt:**

```
@competition-analyzer/AGENTS.md + my brief in briefs/ACTIVE.md.
Mode: landscape.
Output using templates/OUTPUT.md structure.
Tag P0/P1. Unknowns must be explicit.
```

**CEO orchestration alternative:** Task tool → `subagent_type: competition-analyzer` with brief content in the prompt.

---

## 3. After

- Move strong insights to **Offer** / **LP** / **Ad** agents per [docs/marketing/HANDOFFS.md](../docs/marketing/HANDOFFS.md).
- Log outcomes: [learnings/OUTCOMES-LOG.md](learnings/OUTCOMES-LOG.md).
- Save deliverable under `docs/marketing/research/` (agent does this when asked or via `*doc-out`).

---

## 4. API

- **System:** [prompts/system.md](prompts/system.md)
- **User message:** filled brief + any pasted public content / ad artifacts
- Load skills from `competition-analyzer/skills/*/SKILL.md` or use platform Skills mechanism

---

## 5. Trouble

| Problem | Fix |
|---------|-----|
| **Thin on proof** | Add one competitor LP URL + your landing outline for contrast |
| **Too many players** | Ask to shortlist **4** active + **3** on watch list for later |
| **Invented ad claims** | Attach artifacts or remove ad section from brief |
| **Same-name companies** | Add disambiguation line per competitor in brief |

---

## See also

- [AGENTS.md](AGENTS.md) — agent card for `@` mention
- [README.md](README.md) — architecture and deploy options
- [templates/BRIEF.md](templates/BRIEF.md) · [templates/OUTPUT.md](templates/OUTPUT.md)
