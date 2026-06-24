---
name: legal-terms
description: Approved clause library for B2B offers. Use when Risk & Compliance selects T&Cs, SLA tiers, IP indemnity, termination, auto-renewal, or data-residency language. Clauses ONLY from clm.clauses.search — never compose new legal text. Triggers on "clause", "terms", "SLA", "indemnity", "termination", "data residency", "contract language".
---

# Legal Terms

Used by **Offer Risk & Compliance** (`offer-risk-compliance`). Custom language → automatic legal escalation.

## Hard rules

- Output clauses **only** from `clm.clauses.search`
- Every clause: `clause_id`, `version`, `source: clm.clauses.search:...`
- Never disable clauses marked `non-negotiable` for deal type
- Conservative default when borderline

## Clause categories

| Category | When to use | When NOT to use |
|----------|-------------|-----------------|
| Standard MSA | New-logo, expansion | Pilot (use pilot agreement) |
| Data residency addendum | EU/UK/APAC residency required | US-only, no residency ask |
| SLA tier — standard | SMB / mid-market | Enterprise with custom SLA ask |
| SLA tier — enterprise | Enterprise segment | Below exposure threshold |
| Mutual indemnity | Default | — |
| Uncapped IP indemnity | Strategic logo + deal size threshold | All other deals |
| Evergreen / auto-renewal | Multi-year, renewal | Pilot |
| Pilot off-ramp | `deal_type = pilot` | Production deals |

## Deviation handling

If customer precedent (`clm.precedent.search`) shows prior deviation:
- Surface in `precedent_findings`
- Do not auto-apply deviation — flag `open_questions_for_legal`

## References

- `references/clause-index.md` — category → search query hints
- Data residency variants per region (load on demand)

## Handoffs

- `blocking_scope_conflict` → Solution Architect (SKU lacks regional offering)
- `jurisdiction_status = blocked` → Director STOP → Legal
