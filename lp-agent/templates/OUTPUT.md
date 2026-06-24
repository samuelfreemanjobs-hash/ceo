# Landing page — output template

Agent fills this structure. Save to: `docs/marketing/landing-pages/{slug}-lp-{YYYY-MM-DD}.md`

Playbook v1.0 · Validate against offer + proposal before delivery.

**Formats:** `full` (default) · `minimal` · `tiered`

---

## Page metadata

- **Offer reference:** {path to offer artifact}
- **Proposal reference:** {path to proposal artifact}
- **Primary CTA:** {label} → {URL}
- **Compliance flags:** {from offer §7 / brief}
- **Format:** {full | minimal | tiered}

---

## Hero

**Headline:** (offer §1 promise — specific, no fluff)

**Subhead:** (who it's for + outcome — from offer §2)

**Primary CTA:** [{label}]({url})

**Secondary CTA:** (optional)

**Trust strip:** (logos, stats, or proof bullets — only substantiated items from offer §5)

---

## Problem (full / tiered only)

2–3 short paragraphs or bullets — pains from proposal §2 / offer §2.

---

## Solution

**Overview:** (offer §1 + mechanism from offer §4)

**What's included:**
- (offer §3 bullets — client-facing)

**Out of scope:**
- (offer §3 boundaries — builds trust)

---

## Proof

**Social proof / results:**
- (offer §5 — honest; note gaps if thin)

**Gaps:** (if any — internal note or omit section)

---

## Pricing (full / tiered)

**Primary recommendation:** {tier name} — **{price}** (exact from offer §6)

**What's included at this tier:**
- (bullets)

### Tier comparison (tiered format only)

| Tier | Best for | Price | Includes |
|------|----------|-------|----------|
| | | | |

**Payment / terms:** (from offer §7 — brief)

---

## FAQ (full / tiered)

| Question | Answer |
|----------|--------|
| (from offer §8 objections) | |

---

## Final CTA

**Headline:** (restated outcome)

**Body:** (1–2 sentences — urgency without hype)

**Button:** [{primary CTA label}]({url})

---

## Implementation notes (for dev / CMS)

- **Suggested URL slug:**
- **SEO title:** (≤60 chars)
- **Meta description:** (≤155 chars)
- **Open Graph headline:**

---

## Pre-publish checklist

- [ ] Scope ⊆ offer §3
- [ ] Price = offer §6 primary tier
- [ ] No new guarantees
- [ ] Compliance review if YMYL or flagged claims
- [ ] CTA URL confirmed
