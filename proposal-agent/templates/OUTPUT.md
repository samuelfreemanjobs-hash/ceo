# Client proposal — output template

Agent fills this structure. Save to: `docs/marketing/proposals/{slug}-proposal-{YYYY-MM-DD}.md`

Playbook v1.0 · Validate against offer artifact before delivery.

**Formats:** `standard` (full) · `short` (sections 1, 4–6, 9) · `executive` (sections 1, 6, 9 only)

---

## Document header

- **Prepared for:** {client name / company}
- **Prepared by:** {your company}
- **Date:** {YYYY-MM-DD}
- **Valid until:** {date from brief}
- **Reference:** {link or path to source offer artifact}

---

## 1. Executive summary

2–4 short paragraphs:
- Restate the client's situation in their language (from brief personalization + offer "for who")
- One-line promise (from offer §1 — do not strengthen)
- Recommended path and primary investment (from offer §6)
- Clear ask / next step preview

---

## 2. Your situation & goals

**What we understand:**
- (Pains, goals, constraints — from brief notes and offer §2)

**Why now:**
- (Optional — only if supported by brief notes)

**Fit:**
- Who this is for / not for (from offer §2 — client-friendly framing)

---

## 3. Proposed solution

**Overview:**
- (Offer §1 promise + mechanism from offer §4)

**What's included:**
- (Offer §3 — bullets, client-facing language)

**Out of scope:**
- (Offer §3 boundaries — builds trust)

---

## 4. How we'll work together

| Phase | What happens | Timing |
|-------|--------------|--------|
| | | |

**What we need from you:**
- (Offer §4 client inputs)

---

## 5. Proof & credibility

**Relevant results:**
- (Offer §5 — only verified or honestly labeled)

**If proof is still building:**
- (Carry gaps from offer §5 — do not invent)

---

## 6. Investment

**Recommended option:** (primary tier from offer §6 if applicable)

| | |
|--|--|
| **Investment** | {exact price/band from offer — no rounding up} |
| **Payment terms** | {from offer §7} |
| **What's included** | {summary} |

**Other options** (if offer had tiers):

| Option | Investment | Best for |
|--------|------------|----------|
| | | |

**Why this pricing:** (offer §6 logic — plain language)

---

## 7. Terms & assumptions

- **Guarantee / risk reversal:** (offer §7 only — omit if none)
- **Assumptions:** (client inputs, access, timelines depend on...)
- **Boundaries:** revisions, scope, pauses (offer §7)

*Internal compliance flags (do not delete — for compliance handoff):*
- YMYL / regulated:
- Must not say:
- Claims needing substantiation:

---

## 8. Common questions

| Question | Answer |
|----------|--------|
| | |

*(From offer §8 objection handling — 3–5 rows, client phrasing)*

---

## 9. Next steps

1. **Review** this proposal and confirm scope fits
2. **{Action}** — e.g. schedule kickoff, sign agreement, pay deposit
3. **{Contact}** — rep name, email, calendar link

**Signature block** (if brief requests):

| | |
|--|--|
| Client | _________________________ Date: _________ |
| Provider | _________________________ Date: _________ |

---

## Agent validation (complete before delivery)

- [ ] Every deliverable traces to offer §3
- [ ] Prices match offer §6 exactly
- [ ] No new guarantees vs offer §7
- [ ] Proof gaps disclosed per offer §5
- [ ] Compliance flags copied to §7
- [ ] Format matches brief (`standard` | `short` | `executive`)

## Downstream handoffs

| To | Payload |
|----|---------|
| lp-agent | §1 summary, §5 proof, §6 primary tier, §9 CTA |
| compliance-agent | §7 flags |
| writer | §1 + §9 for cover email |

## Open questions

-
