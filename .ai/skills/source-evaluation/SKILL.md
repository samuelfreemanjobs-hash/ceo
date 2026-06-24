---
name: source-evaluation
description: Use when assessing the reliability, recency, or bias of competitive intelligence sources before incorporating findings into any analysis. Apply continuously in the background of any research task; surface explicit source ratings when reliability is low, when sources conflict, when a finding will materially affect a recommendation, or when the user asks about confidence. Triggers include conflicting sources, suspiciously precise numbers from anonymous sources, claims about private companies' internals, and any time a finding feels "too clean". Do NOT use as a substitute for actually gathering sources — this skill evaluates, it doesn't replace research.
---

# Source Evaluation

Competitive intelligence is only as good as its sources. This skill is the quality filter applied to every input before it earns a confidence label.

**Used by:** Competition Analyzer (every investigation)

## The three-axis model

Evaluate every source on three axes. A source can be strong on one and weak on another — that's important to track.

### Axis 1: Reliability (is this source likely to be correct?)

**Tier S — Primary, authoritative**

- The competitor's own current published material (for facts about themselves)
- Regulatory filings (10-K, 10-Q, S-1, 8-K, prospectuses)
- Direct first-party data from your own organization (sales call notes, win/loss interviews, customer references)
- Court filings, M&A disclosures

**Tier A — Strong secondary**

- Reputable analyst reports (Gartner MQ, Forrester Wave, IDC)
- Earnings call transcripts (the _transcript_, not press coverage of it)
- Reputable industry trade press with named authors
- Investor decks shared by the company

**Tier B — Useful but noisy**

- General business press
- Aggregated review sites (G2, Capterra, TrustRadius, Trustpilot)
- LinkedIn data (headcount estimates, hiring patterns)
- Crunchbase, Pitchbook (good for funding, weaker for revenue)
- Conference talks, podcasts, public interviews

**Tier C — Signal but treat with care**

- Forums (Reddit, Hacker News, niche communities)
- Glassdoor, Blind
- Twitter/X, LinkedIn posts (non-official)
- Anonymous "insider" claims

**Tier D — Do not cite as evidence**

- Unsourced rumors
- Competitor-bashing content from rivals
- Auto-generated SEO content
- AI-generated content masquerading as analysis

A finding only earns **Confirmed** with at least one Tier S or two Tier A sources. **Likely** can rest on one Tier A or two triangulating Tier B. **Unverified** is anything resting on Tier C alone.

### Axis 2: Recency

How fresh does this need to be to be useful?

| Topic | Half-life |
|-------|-----------|
| Pricing list | 30–60 days |
| Product features | 60–90 days |
| Leadership | 90 days |
| Funding / financials | Next earnings or next round |
| Headcount | 90 days |
| Strategic positioning | 6–12 months |
| Company history | Indefinite |

If a source is past the half-life for its topic, downgrade reliability by one tier or flag for re-verification.

### Axis 3: Bias

Every source has a built-in slant. Track it explicitly.

| Source | Built-in bias |
|--------|---------------|
| Competitor's own marketing | Maximally favorable to themselves |
| Their press releases | Timed for narrative, not for completeness |
| Earnings calls | Public-company performance theater; read the Q&A, not the prepared remarks |
| Analyst reports | Pay-to-play sensitivity varies; check who the analyst's clients are |
| Reviews | Self-selection — angry and very happy users overrepresented |
| Glassdoor | Skews to ex-employees with grievances |
| Trade press | Access journalism is real; check whether the outlet routinely critiques the company |
| Customers as references | Selected and prepped by the vendor |
| Ex-employees | May have non-disparagement obligations; may also have axes to grind |
| Forums / Reddit | Loud minority effects; brigading; sometimes salted by the company |
| Your own sales team | Loss bias — they remember losses more vividly than wins |

Bias doesn't invalidate a source; it shapes how you read it. A pricing page is biased _toward_ listing list prices, not actual deal prices — useful for one and not the other.

## Triangulation rules

A claim earns higher confidence only if multiple sources agree _and the sources are independent_. Two trade-press articles citing the same press release are not independent — they're one source.

Independence tests:

- Do they cite each other?
- Do they cite the same single primary?
- Are they downstream of the same PR cycle?

If yes to any, they count as one source for triangulation purposes.

## Red flags

Treat any of these as reasons to drop confidence:

- **Suspicious precision** — a private company's revenue stated to three significant figures by an anonymous source.
- **Single-source strong claims** — a strategic pivot reported by exactly one outlet and not corroborated.
- **Timing coincidences** — favorable coverage clustering around fundraising or sales cycles.
- **Off-narrative silence** — a competitor that usually announces launches loudly suddenly going quiet on a known initiative. (Not necessarily disconfirming — but worth flagging.)
- **AI-summarized content cited as evidence** — including content from other AI systems. Don't cite AI summaries; cite the underlying source.

## Confidence mapping

| Evidence pattern | Label |
|------------------|-------|
| Tier S + independent Tier A agree | Confirmed |
| One Tier S (competitor claim on themselves) | Likely (note bias) |
| One Tier A | Likely |
| Two+ independent Tier B triangulating | Likely |
| Single Tier B | Likely at best — often Unverified for quantitative claims |
| Tier C alone | Unverified |
| Inference without direct evidence | Unverified (label as hypothesis) |

## Citation format

```
[short label] — [URL] — [retrieval date] — Tier: S|A|B|C — Note: one-line reliability/bias
```

Example: `Acme pricing page — https://acme.com/pricing — 2026-06-14 — Tier: S — Primary; list prices only, enterprise not shown.`

## How to surface source quality in outputs

Source quality is always recorded, not always displayed. Display when:

- Reliability changes the conclusion ("This is Likely, not Confirmed, because all sources trace to one press release")
- Sources conflict materially (then explain the conflict and your resolution)
- The user explicitly asks
- A finding will drive a high-stakes decision

In other cases, the **Sources** section at the end of the output carries the reliability notes per source, and the **Confidence summary** carries the aggregated picture. Inline noise about source quality on every sentence destroys readability.

## Anti-patterns

- **False precision laundering.** Citing a source doesn't make the underlying number more reliable than the source allows.
- **Reliability inflation through repetition.** If three articles repeat the same dubious claim, the claim isn't more reliable — the noise floor is just higher.
- **Authority transfer.** Citing a reputable outlet for a claim that outlet itself sourced weakly. Always check what the outlet's source actually was.
- **Recency worship.** Newer isn't always better. The official 10-K is more reliable than yesterday's trade-press recap of it.
- **Cynicism as substitute for analysis.** Every source has bias; that doesn't mean every source is equally unreliable. Calibrate, don't dismiss.
