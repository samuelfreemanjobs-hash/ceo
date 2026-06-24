# Offer Builder — instructions (Cursor)

**Agent:** Offer Builder · **Playbook:** v1.2 · **Package:** `offer-builder/`

Package services/products into **specific offers** — outcome, scope, terms, proof. For **CRM catalog quotes** use `offer-director` instead.

**Standards:** [STANDARDS.md](../STANDARDS.md)

---

## 1. Prep

1. Optional: [USER_PROFILE.md](USER_PROFILE.md)
2. Fill [templates/BRIEF.md](templates/BRIEF.md) — mode: `flagship` | `stack` | `audit`
3. Save to [briefs/ACTIVE.md](briefs/ACTIVE.md)

---

## 2. Run

```
@offer-builder/AGENTS.md + my brief in briefs/ACTIVE.md.
Mode: flagship (or: stack | audit).
Output using templates/OUTPUT.md.
Max 3 questions if needed.
```

**CEO:** `Task → subagent_type: offer-builder`

---

## 3. After

- Save → `docs/marketing/offers/{slug}-offer-{date}.md`
- Log: [learnings/OUTCOMES-LOG.md](learnings/OUTCOMES-LOG.md)
- Handoffs: [HANDOFFS.md](../docs/marketing/HANDOFFS.md)

**Second pass (optional):** sales one-pager · landing outline · email pitch

---

## 4. Trouble

| Problem | Fix |
|---------|-----|
| Vague "we help everyone" | Narrow ICP in Context; use Exclusions for who/what is out |
| Unrealistic timeline | Fill Outcomes (time to first value + client inputs) and Context (capacity) |
| Price feels arbitrary | Require price logic section in output |
| Guarantee overreach | Self-audit + compliance flag |

---

## See also

[GUIDE.md](GUIDE.md) · [AGENTS-INDEX.md](../docs/marketing/AGENTS-INDEX.md) · [AGENTS.md](AGENTS.md)
