---
name: pricing-teardown
description: Use when conducting detailed pricing analysis of a competitor — extracting tiers, inferring hidden pricing, classifying the pricing model, mapping packaging-as-pricing, identifying recent pricing changes, and reading pricing strategy. Triggers include "what does [competitor] charge", "how do they price", "build a pricing teardown", "compare pricing", any question about enterprise / custom / contact-sales tiers, or any request involving discounting, packaging, or pricing changes. Apply after or alongside competitor-profiling when pricing is the focus or a significant component. Do NOT use for pure feature comparison without a pricing dimension — use competitor-profiling section 2 for that.
---

# Pricing Teardown

Pricing is the most concentrated expression of a competitor's strategy. A teardown done well reveals not just what they charge but who they're for, what they think they're worth, and where they think the market is going.

**Used by:** Competition Analyzer (primary), Marketing Director (when competitive pricing claims are needed)

## Why pricing analysis is uniquely hard

- Pricing pages show **list prices**, not deal prices. The gap is often 20–50% and only your sales team can close it.
- **Hidden tiers** are intentional. "Contact sales" is itself a signal — about ACV, sales motion, and what they don't want self-serve customers to see.
- **Packaging is pricing.** What's gated where matters as much as the dollar figure.
- **Pricing pages change quietly.** Re-verify; don't rely on memory or stale snapshots.
- **Regional variations exist** and are usually undocumented publicly.

Treat pricing data with extra rigor on source-evaluation. The recency half-life is 30–60 days, not "indefinite."

## The seven-step teardown

### 1. Visible tier extraction

Pull every visible tier with:

- Tier name
- Headline price (monthly and annual where both shown)
- Billing unit (per-seat, per-thousand-events, flat, per-GB, etc.)
- Included quantities (seats, projects, requests, storage)
- "Starting at" prefixes — note them; they always mean something costs more

Get this from the live pricing page via `web_fetch`. Search snippets are not enough — pricing pages have specific structure that snippets flatten.

### 2. Hidden tier inference

If the pricing page ends with "Enterprise — Contact us," that's a tier. Infer what you can:

- **Estimated ACV** — from job postings (enterprise AE seniority and OTE imply deal sizes), from press-released customer logos, from public earnings if available
- **Likely included capabilities** — what's listed as "Enterprise-only" or "talk to us" elsewhere in their docs
- **Likely sales process length** — from their RFP responses, security questionnaires, and procurement marketplace listings
- **Floor and ceiling** — the lowest believable enterprise deal and the highest

Tag every enterprise-tier inference as **Likely** or **Unverified** unless you have first-party sales data confirming.

### 3. Pricing model classification

Classify on these axes:

| Axis | Options |
|------|---------|
| **Unit** | Per-seat / per-usage / flat / hybrid |
| **Commitment** | Month-to-month / annual / multi-year required |
| **Expansion vector** | Seats / volume / features / all of the above |
| **Free tier** | None / time-limited / feature-limited / seat-limited / forever-free |
| **Self-serve ceiling** | Where does the credit card stop working? |

The combination tells you the sales motion. Per-seat + month-to-month + forever-free is PLG. Per-usage + annual + no free tier is enterprise sales. Hybrid models are increasingly common and reveal where the company is in transition.

### 4. Packaging-as-pricing map

For each tier, list what's _gated_. Pay attention to:

- **Features that exist but are tier-gated** — reveals what they think is high-willingness-to-pay
- **Quotas / quantities** — reveals their cost structure and target customer size
- **Support level** — reveals where they invest CS attention
- **Compliance / governance** (SSO, SCIM, audit logs) — usually the enterprise gate, and the _price_ of SSO is a famous tell ("SSO tax" — note as signal, not moralize)
- **API and integration access** — gating these signals platform aspirations or lack thereof

Build a matrix: rows = features/quotas, columns = tiers, cells = included / gated / quantity.

### 5. Discount and commitment discipline

From the pricing page, billing FAQs, and review sites, look for:

- Annual discount magnitude (typical: 15–25%)
- Multi-year discount existence and magnitude
- Volume discount tiers (if disclosed)
- Nonprofit, education, startup-program discounts
- Whether month-to-month is offered at all on higher tiers
- Whether per-seat pricing has minimums

Discount discipline reveals sales pressure. A flexible discount stack signals deals being negotiated; rigid public pricing signals confidence in willingness-to-pay.

### 6. Pricing change history

Use the Wayback Machine, public announcements, and customer complaints in forums to reconstruct:

- Last list-price change (direction, magnitude, date)
- Packaging changes (what moved between tiers)
- New tiers added or sunset
- Free-tier changes (these usually signal strategy shifts)

Pricing changes are strategic signals. Re-organizing the free tier almost always means the funnel is being tuned. Adding an enterprise tier means moving upmarket. Raising list while quietly expanding discount means margin pressure.

Tag historical claims **Unverified** unless primary or archived source confirms.

### 7. Pricing strategy interpretation

Synthesize. The pricing strategy is usually one of:

| Strategy | Signals |
|----------|---------|
| **Penetration** | Aggressive entry pricing, generous free tier, expansion-via-usage |
| **Skim** | High list prices, premium positioning, weak free tier, enterprise focus |
| **Value-based** | Pricing varies sharply by use case or customer size; willingness-to-pay segmentation visible |
| **Cost-plus** | Pricing tracks infrastructure cost (common for usage-based dev tools) |
| **Anchor-and-discount** | High list prices with routine large discounts; the headline is for negotiation |

Tag your interpretation with confidence. Strategy interpretations are inferences and should be labeled as such.

## Output format

```markdown
# [Competitor] — Pricing Teardown
*Last verified: [date]*

## Visible tiers
| Tier | Price | Unit | Included | Notes |
| ... |

## Hidden tier (Enterprise)
- Estimated ACV: [range, confidence]
- Likely capabilities: [...]
- Sales process: [...]
- Evidence: [...]

## Model classification
- Unit: [...]
- Commitment: [...]
- Free tier: [...]
- Self-serve ceiling: [...]

## Packaging matrix
[features × tiers table]

## Discount discipline
[...]

## Pricing change history (last 12 months)
[...]

## Strategy interpretation
**Most likely:** [strategy] — confidence: [level]
**Evidence:** [...]
**Alternative interpretation:** [...]
**What would change my read:** [...]

## Sources
[...]

## Confidence summary
[...]

## Open questions
[...]
```

**Output path:** `docs/marketing/research/{competitor}-pricing-teardown-{date}.md`

## Anti-patterns

- **List-price worship.** Treating list prices as deal prices. Without sales data, every list price is an upper bound for the segment that doesn't negotiate.
- **Tier-count theater.** Counting tiers is not analysis. What's in them and what's gated is.
- **Free-tier dismissal.** "They have a free tier" is not a finding. _Why_ and _how generous_ is the finding.
- **The SSO tax confusion.** Don't moralize about SSO being gated to enterprise — note it as a signal (it usually means enterprise-positioning) and move on.
- **Currency / region confusion.** Pricing pages default to one region. Don't assume the price you see is the price everyone sees.
- **Confusing pricing page with pricing strategy.** The page is an artifact; the strategy is the intent behind it. Don't conflate them.

## When this skill yields the most value

- Before a price/packaging change of your own
- Before entering a new segment where the competitor already plays
- When sales is losing deals on price and you need to know if it's real
- During a pricing audit or M&A diligence
- When a competitor visibly changes their pricing and you need to read the signal

## Handoff

Feed tier map, packaging matrix, and strategy interpretation into `competitor-profiling` (§3) or `strategic-synthesis` (battle card pricing block, move alerts).
