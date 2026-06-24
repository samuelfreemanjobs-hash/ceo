---
name: pricing-teardown
description: Use when analyzing a competitor's pricing model, packaging, and monetization signals — tier structure, enterprise opacity, PLG mechanics, and pricing-led positioning. Invoke for pricing intelligence, battle card pricing sections, and move alerts on price changes.
---

# Pricing Teardown

**Used by:** Competition Analyzer (primary), Marketing Director (when competitive pricing claims are needed)

## When to invoke

- User asks about competitor pricing, tiers, or packaging
- Building or updating a battle card pricing section
- Investigating a suspected pricing change (move alert)
- Comparing monetization models across a landscape

Do **not** invoke for general profiling when pricing is a single row in the profile — run a full teardown when pricing is the focus or when enterprise/custom pricing opacity blocks a profile conclusion.

## Investigation sequence

### 1. Locate primary sources

| Source | What to capture |
|--------|-----------------|
| Pricing page (live) | Tier names, list prices, billing period, seat/user limits |
| Product docs | Feature gates per tier, add-ons, usage limits |
| Checkout flow (if accessible) | Trial length, credit card requirement, downgrade path |
| Enterprise / contact-sales page | Signals of opaque pricing, minimum deal size language |
| Changelog / blog | Announced pricing or packaging changes |

Always `web_fetch` the live pricing page. Screenshots in third-party articles are not sufficient — verify live.

### 2. Build the tier map

For each tier, record as **observations** (quote exact numbers from source):

```
| Tier | Price | Billing | Unit | Key limits | Notable inclusions |
|------|-------|---------|------|------------|-------------------|
```

Tag confidence per cell. If a number is inferred (e.g., "≈$X based on review"), label **Unverified**.

### 3. Packaging mechanics

Document:

- **Seat model:** per-user, per-workspace, flat, usage-based, hybrid
- **Free tier:** exists? limits? conversion hooks?
- **Trial:** duration, feature scope, credit card required?
- **Add-ons:** support, SSO, audit logs, API, storage — priced separately?
- **Annual discount:** published % if visible
- **Minimum commitment:** monthly only vs. annual push

### 4. Enterprise / opaque pricing

When public pricing stops at "Contact sales":

- Record as observation: "Self-serve tiers end at [tier]; enterprise pricing not published"
- Note signals: "Teams of 50+", "SSO required", "custom SLA" on higher tiers
- Check G2/review sites for **anecdotal** deal sizes — tag **Unverified**, never Confirmed from reviews alone
- Check job postings for "deal size", "ACV", "enterprise AE" — **Likely** strategy signal, not pricing fact

### 5. Positioning inference (label explicitly)

Only after tier map is complete, draw **inferences**:

- "Price anchoring suggests upmarket focus" — cite which tier is hero / default
- "PLG motion" — cite free tier + self-serve checkout evidence
- "Land-and-expand" — cite seat model + tier jump mechanics

Each inference links to specific observations.

### 6. Historical comparison (if prior intel exists)

- Check internal prior profiles in `docs/marketing/research/`
- If price changed: produce move-alert fields (what changed, when verified, implications)
- If no prior intel: note "no baseline for comparison"

## Output formats

### Pricing snapshot (inline)

```markdown
## Pricing snapshot — {competitor}

**Last verified:** YYYY-MM-DD

### Published tiers
[table]

### Packaging mechanics
- ...

### Enterprise visibility
- ...

### Inferences (labeled)
- **Likely:** ...

### Open questions
- ...

### Sources
- ...
```

### Battle card pricing block

≤5 bullets: their price position, where we're cheaper/expensive, landmines (claims we can't make), discovery question to expose gap.

## Staleness

Pricing goes stale in **30 days**. Re-fetch live page before any external-facing deliverable.

## Anti-patterns

- Don't report tier prices from a blog roundup without verifying the live page
- Don't treat "starts at" language as exact without checking checkout
- Don't Confirmed-label enterprise ACV from a single Reddit thread
- Don't conflate "they're expensive" (opinion) with tier comparison (observation)

## Handoff

Feed tier map and inferences into `competitor-profiling` (section 3) or `strategic-synthesis` (battle card / landscape).
