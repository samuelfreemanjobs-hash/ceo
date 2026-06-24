---
name: competitor-profiling
description: Use when building or updating a comprehensive profile of a specific named competitor. Covers identity, offerings, pricing, ICP, positioning, GTM, financials, people signals, recent moves, and a strengths/weaknesses synthesis. Triggers include "profile [company]", "tell me about [company] as a competitor", "research [competitor]", "what does [company] do", "build a competitor profile". Do NOT use for market sizing without a named competitor, customer/persona research, or analyses that don't center on a specific competitor. Do NOT use to generate a one-page battle card — use strategic-synthesis for that.
---

# Competitor Profiling

A profile is the **baseline view** of a competitor. Everything else — battle cards, SWOTs, move alerts — is derived from it. Build the profile first; derive second.

**Used by:** Competition Analyzer (primary), Marketing Director (delegation context)

## When this skill applies

- New competitor entering scope
- Periodic refresh (quarterly is a reasonable default for active competitors)
- Major triggering event that warrants a full re-profile (acquisition, leadership change, pivot)

For a _single dimension_ question ("what's their pricing?") you don't need the full skill — use **pricing-teardown** for pricing depth, or the relevant section below.

## The ten sections of a profile

Build them in this order. Earlier sections constrain later ones (you can't assess positioning without knowing the offering).

### 1. Identity and context

- Legal name, common name, parent company, ownership status (public / private / PE-owned / subsidiary)
- Founded, HQ, key offices
- Headcount (most recent verifiable estimate, with source)
- Funding history if private, market cap range if public
- **Lens:** threat | acquisition target | partner | benchmark | adjacent — state which applies

_Sources:_ company "About" page, LinkedIn company page, Crunchbase/Pitchbook, SEC filings if public.

_Common pitfalls:_ Conflating subsidiaries with parents, using stale headcount, missing recent ownership changes.

### 2. Offerings

- Product/service lines with one-sentence descriptions each
- Categorize by use case, not by their marketing taxonomy
- Note recently launched, recently sunset, and visibly de-emphasized lines

_Sources:_ product pages, docs, changelog/release notes, press releases.

_Common pitfalls:_ Taking the marketing taxonomy at face value; missing the gap between what's marketed and what's documented.

### 3. Pricing and packaging

- List all visible tiers with prices
- Note what's gated where (features, seats, volume, support)
- Identify hidden tiers (enterprise / custom / contact-sales)
- Note pricing model (per-seat, usage, flat, hybrid) and any recent model changes

Use **pricing-teardown** when pricing is strategic, opaque, or the focus of the request.

_Sources:_ pricing page (primary), reviews mentioning prices, third-party pricing trackers.

_Common pitfalls:_ Assuming the pricing page is complete; missing regional pricing variations; missing the gap between list and actual deal pricing (only sales call data fixes this).

### 4. Target customers / ICP

- Stated ICP (from their marketing)
- Apparent ICP (from case studies, logos, integrations they prioritize)
- Note discrepancies between stated and apparent — these are revealing

_Sources:_ customer page, case studies, integration partners, testimonials, "who uses this" review data.

_Common pitfalls:_ Trusting the marketed ICP over the lived one; missing segment shifts.

### 5. Positioning and messaging

- Hero claim (the one sentence on the homepage)
- Three to five key differentiation points they emphasize
- The category they place themselves in
- Notable absences — what they conspicuously _don't_ mention

_Sources:_ homepage, category landing pages, recent keynote / launch material, CEO public talks.

_Common pitfalls:_ Confusing positioning (how they want to be seen) with capability (what they actually do).

### 6. Go-to-market and channels

- Sales motion (PLG / sales-led / hybrid)
- Channel partners, reseller programs
- Notable marketing surfaces (events, podcasts, content programs)
- Pricing presence on procurement marketplaces (AWS, GCP, Azure)

_Sources:_ careers page (sales-team hiring is a signal), partner pages, conference sponsor lists, marketplace listings.

_Common pitfalls:_ Reading the sales motion from public surface only; missing channel-led revenue if they don't market it.

### 7. Financials (where available)

- Public: latest 10-K/10-Q headline figures, revenue trajectory, segment breakdown if disclosed
- Private: most recent funding round (size, lead, date, post-money), reported revenue ranges, burn signals
- Layoff / hiring net position from the last 6 months

_Sources:_ SEC filings, Crunchbase, Pitchbook, news, layoffs trackers, job-posting deltas.

_Common pitfalls:_ Treating press-released revenue figures as audited; missing that a funding round at flat valuation is a signal too.

### 8. People and culture signals

- Key leadership (CEO, CRO, CPO, CTO) — names, tenure, prior roles
- Recent senior departures or hires
- Glassdoor / Blind signal if relevant (with caveats — these skew)
- Open roles concentration (where are they investing headcount?)

_Sources:_ leadership page, LinkedIn, news, Glassdoor (with care), job board with role-type aggregation.

_Common pitfalls:_ Overweighting Glassdoor; missing the "ghost departure" where someone is removed from the leadership page but no announcement was made.

### 9. Recent moves (last 6–12 months)

- Product launches and major updates
- Pricing changes
- Leadership changes
- Funding / M&A activity
- Notable customer wins and losses
- Public strategic statements (earnings calls, keynote announcements, investor decks)

_Sources:_ changelog, press, earnings transcripts (for public), industry trade press.

_Common pitfalls:_ Listing everything chronologically and missing the pattern; treating launches and updates as equally significant.

### 10. Strengths / weaknesses synthesis

- Three to five real strengths (evidence-tagged)
- Three to five real weaknesses (evidence-tagged, including weaknesses they themselves wouldn't acknowledge)
- One or two open questions where the answer would change your assessment

_This section is your assessment, not their marketing._ Strengths your customer wouldn't agree with aren't strengths. Weaknesses without evidence aren't weaknesses, they're wishes.

---

## Profile output structure

```markdown
# [Competitor name] — Profile
*Last updated: [date] · Refresh recommended: [date]*

**Position summary (one sentence):** [...]

## 1. Identity and context
...

## 2. Offerings
...

[sections 3–10]

---

## Sources
[list with URL, retrieval date, reliability note]

## Confidence summary
- Confirmed: [...]
- Likely: [...]
- Unverified: [...]

## Open questions
- [What you couldn't determine and what would resolve it]
```

**Output path:** `docs/marketing/research/profiles/{competitor-name}-profile-{date}.md`

## Anti-patterns

- **Profile-as-press-release.** A profile that reads like their marketing is a failed profile.
- **Profile-as-attack.** A profile that catalogs only weaknesses is also a failed profile. The point is accuracy, not advocacy.
- **Profile-as-snapshot-only.** A profile without "recent moves" is a baseline view stripped of velocity. Always include momentum.
- **Profile-as-everything-equal.** Don't give equal column-inches to every section. Sections with high relevance to the user's lens should be deeper.

## Handoff

Derive battle cards, SWOT, move alerts, and strategic briefs via **strategic-synthesis** after the profile baseline is complete.
