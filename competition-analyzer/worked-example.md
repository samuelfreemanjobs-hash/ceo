# Worked Example — Competitor Profile Trace (Linear)

**Purpose:** Demonstrate end-to-end investigation flow, skill invocation order, and evidence tagging — not a live intelligence product. **Re-verify all observations at investigation time.**

**Task:** Build a threat-lens profile of Linear for a B2B project-management competitive landscape.

**Lens:** threat  
**Date of trace:** 2025-06-24 (methodology demo)

---

## Step 0 — Classify and decompose

| Sub-investigation | Independent? | Skill |
|-------------------|--------------|-------|
| Identity & product baseline | Yes | competitor-profiling §1–2 |
| Pricing & packaging | Yes | pricing-teardown |
| Positioning & homepage messaging | Yes | competitor-profiling §4 |
| GTM & hiring signals | Yes | competitor-profiling §5–6 |
| Synthesis | Sequential (after above) | strategic-synthesis |

**Parallel batch 1:** pricing teardown + homepage fetch + job board search (if tool available)

---

## Step 1 — Identity (observations)

| Claim | Type | Confidence | Last verified |
|-------|------|------------|---------------|
| Linear is a project/issue tracking product aimed at software teams | Observation | Confirmed | 2025-06-24 |
| HQ in San Francisco; founded 2019 | Observation | Likely | 2025-06-24 |
| Category: dev-centric project management / issue tracking | Observation | Confirmed | 2025-06-24 |

**Sources:**
- [linear.app](https://linear.app) — retrieved 2025-06-24 — Tier: Primary — Self-narrative; verify claims independently

---

## Step 2 — Pricing teardown (skill: `pricing-teardown`)

**Actions taken:**
1. `web_fetch` live pricing page (required — do not trust roundup blogs)
2. Map tiers: name, price, billing period, seat limits
3. Note enterprise opacity if "Contact sales" appears

**Example tier map structure** (populate with live fetches — numbers below are illustrative placeholders):

| Tier | Price | Billing | Unit | Limits | Notes |
|------|-------|---------|------|--------|-------|
| Free | $0 | — | per user | [verify limits] | Observation |
| [Tier name] | [verify live] | monthly/annual | per user | [verify] | Observation |
| Enterprise | Not published | — | — | SSO, audit, etc. | Observation |

**Packaging mechanics (template):**
- Seat model: [per-user / hybrid — verify]
- Trial: [verify checkout flow]
- Annual discount: [verify if published]

**Inference (labeled):**
- **Likely:** PLG motion if free tier + self-serve upgrade path confirmed on live site — *evidence: [link to pricing + signup flow]*

**Open questions:**
- Enterprise ACV and minimum deal size — not on public pricing page
- Would resolve with: CRM win/loss notes, 2+ sales call transcripts mentioning Linear deals

---

## Step 3 — Positioning (observations)

| Claim | Type | Confidence | Last verified |
|-------|------|------------|---------------|
| Homepage headline emphasizes speed / craft for product teams | Observation | Confirmed | 2025-06-24 |
| "Built for modern software teams" (or similar) persona language | Observation | Likely | 2025-06-24 |
| Differentiation vs. Jira: less enterprise baggage, faster UX | Inference | Unverified | — |

**Bias flag:** Homepage copy is Primary tier — Likely at best for differentiation claims; triangulate with G2 reviews and win/loss notes.

---

## Step 4 — GTM & scale signals

| Signal | Type | Confidence | Source tier |
|--------|------|------------|-------------|
| Content marketing + changelog cadence suggests product-led growth | Inference | Likely | Primary (blog/changelog) |
| Hiring for enterprise AE roles | Observation | Likely | Tertiary (job boards) — strategy signal, not revenue fact |
| ARR / revenue | — | Unverified | Do not cite without filing or credible press |

---

## Step 5 — Source evaluation (skill: `source-evaluation`, applied silently)

- Pricing page: Primary, re-verify every 30 days
- G2 comparison pages: Secondary, both sides biased — triangulate only
- Reddit "we switched from Jira to Linear": Tertiary — anecdote, not Confirmed trend

---

## Step 6 — Strategic synthesis (skill: `strategic-synthesis`)

### SWOT excerpt (threat lens)

| | Item | Tag |
|---|------|-----|
| **Strength** | Strong UX reputation among eng teams | Likely |
| **Weakness** | Enterprise depth vs. incumbent PM tools | Unverified — needs win/loss |
| **Opportunity** | Win accounts where Linear lacks [our strength] | Inference — needs our positioning fit |
| **Threat** | Land-and-expand from eng team into broader org | Hypothesis |

### Battle card bullets (draft)

- **Their pitch:** [quote homepage — Observation]
- **Where we win:** [requires our product context — human input]
- **Landmine:** Do not claim specific Linear pricing without live verification

---

## Step 7 — Deliverable assembly

**Output file:** `docs/marketing/research/profiles/linear-profile-2025-06-24.md`

**Required closing sections:**

```markdown
## Sources
[full citation list per source-evaluation format]

## Confidence summary
- **Confirmed:** ...
- **Likely:** ...
- **Unverified:** ...

## Open questions
- Enterprise pricing and ACV
- Win/loss patterns vs. us (needs CRM)
```

---

## Handoff to Marketing Director (if orchestrated)

```json
{
  "summary": "Linear is a dev-centric PM tool with PLG signals and opaque enterprise pricing. Strong UX positioning; enterprise depth unverified without internal win/loss.",
  "artifact_path": "docs/marketing/research/profiles/linear-profile-2025-06-24.md",
  "confidence_highlights": [
    "Confirmed: category and primary ICP from linear.app",
    "Unverified: enterprise ACV, head-to-head win rates"
  ],
  "open_questions": [
    "CRM win/loss data for deals involving Linear",
    "Live pricing tier verification before external battle card use"
  ]
}
```

---

## What this example teaches

1. **Decompose → parallelize → synthesize last** — pricing and positioning run in parallel; SWOT comes after evidence table is built.
2. **Skills chain** — `pricing-teardown` feeds `competitor-profiling` §3; `strategic-synthesis` consumes the full profile.
3. **Confidence is structural** — every row tagged; Unverified is an acceptable terminal state.
4. **No fabrication** — enterprise ACV left open rather than invented.
5. **Re-verify** — this trace is methodology, not a cached intelligence product.
