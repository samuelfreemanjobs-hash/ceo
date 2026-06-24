---
name: competitor-profiling
description: Use when building a full structured profile of a named competitor — product, pricing, positioning, GTM, financials, and strategic signals. Invoke for competitor profiles, due diligence, and landscape entry research before battle cards or SWOT.
---

# Competitor Profiling

**Used by:** Competition Analyzer (primary), Marketing Director (delegation context)

## Profile structure

Build profiles in this order:

### 1. Identity & scope

- Company name, HQ, founded, funding stage / public ticker
- Primary product category and ICP they claim
- Geographic focus
- **Lens:** threat | acquisition target | partner | adjacent — state which lens applies

### 2. Product & roadmap signals

| Dimension | Observation | Confidence | Last verified |
|-----------|-------------|------------|---------------|
| Core offering | | | |
| Key features vs. us | | | |
| Recent launches | | | |
| Tech stack (if public) | | | |

Tag each row: observation vs. inference.

### 3. Pricing & packaging

- Published tiers (quote exact numbers from source)
- Enterprise / custom pricing visibility
- Free trial / freemium mechanics
- **Open questions** for anything not on public pages

### 4. Positioning & messaging

- Homepage headline and primary value prop (quote)
- Target persona language
- Differentiation claims they make
- Channels where messaging appears (site, ads, social)

### 5. Go-to-market

- Primary acquisition channels (evidence-based)
- Sales motion: PLG, sales-led, hybrid
- Partner ecosystem
- Content / SEO presence (high level)

### 6. Financial & scale signals

- Revenue / ARR if public or credibly reported
- Employee count trend (LinkedIn, job postings)
- Funding rounds or public filings
- Customer logos / case studies cited

### 7. Strategic synthesis

- **Strengths** (evidence-tagged)
- **Weaknesses** (evidence-tagged)
- **Likely next moves** (hypothesis — label explicitly)
- **Implications for us** (recommendation with confidence)

## Required sections in every profile

1. Executive summary (≤150 words)
2. Full profile body (sections above)
3. Sources (URL, date, reliability note)
4. Confidence summary (Confirmed / Likely / Unverified lists)
5. Open questions

## Output path

`docs/marketing/research/profiles/{competitor-name}-profile-{date}.md`
