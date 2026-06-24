---
name: solution-catalog
description: Use when mapping customer needs to product families, checking implementation minimums, tier limits, segment defaults, or integration coverage in Enterprise / Catalog offer builds. Required by Solution Architect agent. Triggers on "product family", "SKU mapping", "implementation minimum", "tier max", "catalog match", "integration coverage". Load BEFORE catalog.product.search calls — defines family→pain mapping heuristics and constraints.
---

# Solution Catalog

Operational reference for the **Solution Architect** agent. This skill does NOT replace `catalog.product.search` — it guides need→family mapping and enforces constraints before and after catalog calls.

## Product family mapping

Map each `dossier.pain` or `from_rep_brief_only` ask to **one primary family** first. Do not multi-map unless pain genuinely spans families.

| Pain pattern | Typical family | Verify via catalog |
|--------------|----------------|-------------------|
| Onboarding / time-to-value | Implementation services, onboarding package | `catalog.product.search(family=implementation)` |
| Seat / user expansion | Platform licenses | `catalog.product.search(family=platform)` |
| Integration / data sync | Connectors, integration services | `catalog.integrations` + search |
| Support / SLA | Support tiers | `catalog.product.search(family=support)` |
| Training / enablement | Training SKUs | `catalog.product.search(family=training)` |
| Security / compliance | Security add-ons | `catalog.product.search(family=security)` |
| Custom workflow | **No catalog match** → `non_standard=true` | Do not invent |

**Rule:** If pain maps to zero families after search, set `non_standard=true` and emit SE question — never guess a SKU.

## Segment defaults

| Segment | Default `term_months` | Notes |
|---------|----------------------|-------|
| SMB | 12 | Month-to-month only if rep_brief explicitly requests |
| Mid-market | 12 | 24 if ACV > segment threshold in catalog |
| Enterprise | 24 | Shorter only with `customer_preference` citation |

Set `term_basis = "default_applied"` when using table defaults.

## Implementation minimums

Each SKU family carries `implementation_minimum_weeks` in catalog metadata. Solution Architect MUST:

1. Sum critical-path implementation weeks for bundled services
2. Set earliest milestone dates ≥ `today + implementation_minimum`
3. If `dossier.urgency_signals` demand faster delivery → flag `flags_to_director`, do NOT compress below minimum

**Never commit to delivery inside implementation_minimum without SE sign-off** (`non_standard=true`).

## Tier and volume limits

- `tier_max` per SKU — if proposed `quantity` exceeds `tier_max`, set `non_standard=true` and flag capacity planning
- Quantity sources (in priority order):
  1. `dossier.account.size_employees` (for seat-based SKUs)
  2. Named team size from `transcript:<id>`
  3. Explicit volume in `rep_brief:<excerpt>`
  4. `estimate_from_<source>` — document assumption; never round up silently

## Integration coverage

Before adding integration-related SKUs:

1. Call `catalog.integrations` with customer system name
2. If not listed → `non_standard=true`, SE question with `estimated_complexity`
3. Do not substitute a "similar" integration SKU

## Dependency rules (post-search)

After `catalog.product.search` assembles candidates:

1. Call `catalog.dependencies.check` on full bundle
2. Missing required dependency → add SKU, `added_by_dependency_rule = true`
3. Incompatible SKUs → keep better pain-fit, drop other with rationale in `flags_to_director`
4. Check fails → **do not emit scope**; return clarification to Director

## Precedent check

Call `deals.history.search` with:
- `segment`, `deal_type`, similar `line_items` SKUs
- Note `deviations_from_precedent` when scope shape differs materially (term, bundle composition, quantity ratios)

## Anti-patterns

- Kitchen-sink bundles without pain mapping
- "Common attach" SKUs without `addresses`
- Paraphrased SKU names (must be verbatim from catalog)
- Aspirational quantities exceeding dossier facts
- Milestones inside implementation_minimum
