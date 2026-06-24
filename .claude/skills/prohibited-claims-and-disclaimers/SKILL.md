---
name: prohibited-claims-and-disclaimers
description: Verify that any external-facing marketing content complies with legal restrictions, substantiation requirements, regulatory disclosures, and the company's prohibited claims list. Use this skill before publishing or approving ANY content that will be seen by customers, prospects, regulators, or the public — including ads, emails, landing pages, social posts, press materials, sales decks, and product copy. Also use when reviewing competitor comparisons, performance claims, health/finance/safety statements, or any content making quantitative assertions. The Compliance Agent should treat this as its primary rulebook.
---

# Prohibited Claims and Required Disclaimers

> **Canonical rules:** [`docs/marketing/BRAND-PROFILE.md`](../../docs/marketing/BRAND-PROFILE.md) — Compliance section.  
> **Status:** Operational with B2B services defaults. Legal review recommended for regulated industries.  
> **Owner:** Legal + Brand · **Used by:** Compliance Agent (primary)

## How the Compliance Agent uses this skill

For every piece of content reviewed, the agent must produce a verdict with the following structure:

```json
{
  "severity": "NONE | LOW | MEDIUM | HIGH | CRITICAL",
  "issues": [
    {
      "claim": "exact text from the content",
      "rule_violated": "section reference from this skill",
      "severity": "LOW | MEDIUM | HIGH | CRITICAL",
      "suggested_fix": "specific revision or required disclaimer"
    }
  ],
  "required_disclaimers": ["list of required disclaimer text"],
  "ready_to_publish": true | false
}
```

## Severity rubric

| Level | Meaning | Director's required response |
|-------|---------|------------------------------|
| NONE | No issues found | Proceed |
| LOW | Minor — recommend revision, not required | Note in output, proceed |
| MEDIUM | Should fix before publishing | Director MUST revise and re-run compliance |
| HIGH | Must fix — significant legal/brand risk | Director MUST block; escalate to human |
| CRITICAL | Hard stop — regulatory, lawsuit, or brand-existential risk | Director MUST refuse to produce content; escalate immediately to Legal + CMO |

The Director is configured to treat HIGH and CRITICAL as hard blocks. The agent cannot override these by re-prompting.

## Hard prohibitions (always CRITICAL)

The following are **never permissible** in any external content, regardless of context, audience, or framing:

- [Example — fintech: "Guaranteed returns" or "risk-free" in any investment context]
- [Example — health: "Cures", "treats", "prevents" for any non-FDA-approved condition]
- [Example — universal: Claims about competitor financial health, executive personal lives, or litigation outcomes]
- [Example — universal: Any claim implying endorsement by a regulatory body that has not endorsed us]
- [Example — universal: Statements about pricing/availability that are not current as of publication]
- [Fill in industry-specific items...]

## Substantiation required (MEDIUM if missing, HIGH if false)

These claim types require documented proof on file before the content is approved. Compliance agent verifies substantiation exists by checking the substantiation database; if no record found, default to MEDIUM and request from author.

| Claim type | What's required | Source location |
|------------|-----------------|-----------------|
| "X% improvement" / "Up to X%" | Study with sample size, methodology, dated within 24 months | `/legal/substantiation/performance/` |
| "#1 in [category]" | Third-party ranking with citable source and date | `/legal/substantiation/rankings/` |
| "Faster than [competitor]" | Benchmark methodology that's replicable on request | `/legal/substantiation/benchmarks/` |
| "Trusted by [N] customers" | Verifiable count from CRM or billing system as of date | `/legal/substantiation/customer-counts/` |
| "Award-winning" | Award named with year and granting body | `/legal/substantiation/awards/` |
| Customer testimonial | Signed release on file; "results not typical" disclaimer if applicable | `/legal/releases/` |
| Security/uptime claim ("99.9%") | Measured methodology, time window, public status page | `/legal/substantiation/sla/` |
| Cost savings claim | Methodology document including comparison baseline | `/legal/substantiation/savings/` |
| [Industry-specific] | [Fill in] | [...] |

## Required disclaimers by category

When content falls into one of these categories, the disclaimer text below must appear adjacent to the claim (not buried in the footer unless explicitly noted).

### Financial / investment content

- **Required text:** [Specific disclaimer language from legal]
- **Placement:** Adjacent to claim
- **Font size minimum:** [Specify — often 10pt or equivalent on web]

### Health / wellness content

- **Required text:** [Specific disclaimer]
- **"Results not typical" rule:** Required when testimonial includes specific outcome metrics

### Performance / comparative claims

- **Required text:** [Disclaimer]
- **Source citation:** Must include date of comparison and source URL

### Beta / preview / early-access features

- **Required text:** "Feature in beta; functionality may change before general availability."
- **Placement:** First mention of the feature on each page

### [Industry-specific category]

- **Required text:** [...]

## Competitor claims rules

These rules apply whenever content references a competitor by name OR by clear implication (e.g., "the leading platform with the blue logo"):

1. **Never** state a competitor "fails to" or "can't" do something. Frame as "we do X" not "they don't do X."
2. **Side-by-side comparisons** require:
   - Same data point being compared (apples to apples)
   - Date of comparison stated
   - Source of competitor data (public sources only — never internal speculation)
   - Disclaimer: "[Exact required text from legal]"
3. **Never** use a competitor's trademark in headlines, H1s, or paid search ad copy without explicit legal clearance.
4. **Never** imply endorsement, partnership, or affiliation by a competitor.
5. **Escalate to legal review** before ANY content naming a top-3 competitor by name — even content that seems positive about the comparison.

## Quantitative claim review checklist

When the content makes a number-based claim, the Compliance Agent must verify all of the following:

- [ ] Number is sourced and citation is current (<24 months unless evergreen)
- [ ] Methodology is documented and available on request
- [ ] No rounding that misrepresents (e.g., "98%" when actual is 78%)
- [ ] Time frame is specified ("in 2024" not just "annually")
- [ ] Population is specified ("of surveyed users" not "of all users")
- [ ] Comparison baseline is fair (not cherry-picked)
- [ ] If a range is given, both endpoints are accurate (no "up to X" where X is the max ever seen)

Any unchecked item triggers MEDIUM minimum.

## Common patterns that auto-trigger MEDIUM or higher

The Compliance Agent should flag these on sight and verify substantiation:

| Pattern | Severity if unsubstantiated | Why |
|---------|----------------------------|-----|
| "The best" / "the only" / "the most" | MEDIUM | Superlatives require #1 substantiation |
| "Save money" / "free" / "no cost" | MEDIUM | Must define exactly what's free/saved |
| "AI" claims | MEDIUM | Must describe what the AI actually does (FTC guidance) |
| "Eco-friendly" / "sustainable" / "green" | MEDIUM | FTC Green Guides require specificity |
| "Limited time" / "ending soon" | HIGH | Must actually be time-limited; deceptive if perpetual |
| Implied scarcity ("only 3 left") | HIGH | Must be actually true at time of impression |
| Customer story / testimonial | MEDIUM until release verified | Must have signed release on file |
| Statistics without citation | MEDIUM | Always cite |
| "Doctors recommend" / "experts say" | HIGH | Must name source; FTC requires substantiation |
| "Patented" / "proprietary" | MEDIUM | Verify patent exists and is granted (not pending) |

## Escalation paths

| Trigger | Path | SLA |
|---------|------|-----|
| CRITICAL flag | Legal team + CMO | Same business day |
| HIGH flag | Legal team | Within 24 hours |
| Repeated MEDIUM flags from same source (3+ in a week) | Brand team retraining session | Within 1 week |
| Entering new regulatory category (e.g., new product launch into healthcare) | Legal review BEFORE any content produced | Pre-launch |
| Competitor names a comparison claim that could trigger response | Legal review | Within 48 hours |
| Crisis or breaking news referencing the brand | Legal + Comms + CMO | Within 2 hours |

## What this skill does NOT cover

These are handled by other skills or processes — the Compliance Agent should not attempt to assess them:

- **Trademark/IP review for visual assets** — separate process owned by Legal
- **Privacy / GDPR / CCPA review for data collection** — owned by Data team
- **Accessibility (WCAG)** — owned by Design QA
- **Localization legal review** — separate skill per market
- **Securities disclosures (10-K, 10-Q references)** — owned by Finance + Legal directly, never automated

If a piece of content needs review in any of these areas, flag MEDIUM with note "out of scope for automated compliance — route to [appropriate team]."

## Versioning

`v[X].[Y] — [DATE]` — [changes]
