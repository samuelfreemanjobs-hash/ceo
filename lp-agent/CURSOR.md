# LP Agent — instructions (Cursor)

**Agent:** LP Agent · **Package:** `lp-agent/`

Turn offer + proposal artifacts into **landing page copy**. Requires completed offer and proposal.

**Standards:** [STANDARDS.md](../STANDARDS.md)

---

## 1. Prep

1. Confirm offer at `docs/marketing/offers/...`
2. Confirm proposal at `docs/marketing/proposals/...`
3. Fill [templates/BRIEF.md](templates/BRIEF.md) — CTA URL, format, brand notes
4. Save to [briefs/ACTIVE.md](briefs/ACTIVE.md)

---

## 2. Run

```
@lp-agent/AGENTS.md + brief in briefs/ACTIVE.md.
Offer: docs/marketing/offers/{path}.
Proposal: docs/marketing/proposals/{path}.
Format: full (or: minimal | tiered).
Output using templates/OUTPUT.md.
```

**CEO / Morgan:** `Task → subagent_type: lp-agent`

---

## 3. After

- Save → `docs/marketing/landing-pages/{slug}-lp-{date}.md`
- Log: [learnings/OUTCOMES-LOG.md](learnings/OUTCOMES-LOG.md)
- Route to compliance before publish
- Optional: ad variants via `writer`

---

## 4. Trouble

| Problem | Fix |
|---------|-----|
| Hero too vague | Pull exact promise from offer §1 |
| Price mismatch | Offer §6 is source of truth |
| Too much text | Switch to `minimal` format |
| Tier confusion | Use `tiered` only when offer has tier table |

---

## See also

[GUIDE.md](GUIDE.md) · [proposal-agent/CURSOR.md](../proposal-agent/CURSOR.md) · [AGENTS-INDEX.md](../docs/marketing/AGENTS-INDEX.md)
