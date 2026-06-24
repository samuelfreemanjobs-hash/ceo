# Proposal Agent — instructions (Cursor)

**Agent:** Proposal Agent · **Package:** `proposal-agent/`

Turn Offer Builder artifacts into **client-facing proposals**. Requires a completed offer at `docs/marketing/offers/`.

**Standards:** [STANDARDS.md](../STANDARDS.md)

---

## 1. Prep

1. Confirm offer artifact exists (`docs/marketing/offers/...`)
2. Fill [templates/BRIEF.md](templates/BRIEF.md) — client, format, personalization
3. Save to [briefs/ACTIVE.md](briefs/ACTIVE.md)

---

## 2. Run

```
@proposal-agent/AGENTS.md + brief in briefs/ACTIVE.md.
Offer artifact: docs/marketing/offers/{path}.
Format: standard (or: short | executive).
Output using templates/OUTPUT.md.
```

**CEO / Morgan:** `Task → subagent_type: proposal-agent`

---

## 3. After

- Save → `docs/marketing/proposals/{slug}-proposal-{date}.md`
- Log: [learnings/OUTCOMES-LOG.md](learnings/OUTCOMES-LOG.md)
- YMYL or guarantees → route to compliance before send
- LP handoff: [HANDOFFS.md](../docs/marketing/HANDOFFS.md)

**Second pass (optional):** cover email via `writer`

---

## 4. Trouble

| Problem | Fix |
|---------|-----|
| Scope creep in draft | Re-read offer section 3; run proposal-validation |
| Price mismatch | Offer section 6 is source of truth — do not round or upsell |
| Thin personalization | Add discovery notes to brief; max 2 clarifying questions |
| Too long for buyer | Switch format to `short` or `executive` |

---

## See also

[GUIDE.md](GUIDE.md) · [offer-builder/GUIDE.md](../offer-builder/GUIDE.md) · [AGENTS-INDEX.md](../docs/marketing/AGENTS-INDEX.md)
