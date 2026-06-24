---
name: offer-templates
description: Use when defining deal milestones and pacing in Enterprise / Catalog offer builds. Required by Solution Architect agent. Triggers on "milestones", "implementation timeline", "deal_type template", "expected_close", "milestone owner". Provides default milestone templates by deal_type — adjust for urgency_signals but never below implementation_minimum from solution-catalog.
---

# Offer Templates

Default **milestone templates** for Solution Architect. Anchor all dates to `opportunity.expected_close` and respect `implementation_minimum` from `solution-catalog`.

## Date anchoring

1. Read `opportunity.expected_close` (YYYY-MM-DD)
2. Work backward for pre-close milestones (contract, security review)
3. Work forward from expected close for post-close implementation
4. Adjust pacing for `dossier.urgency_signals` — compress only within implementation_minimum

## Templates by deal_type

### new_business

| Order | Milestone | Typical offset from close | Owner |
|-------|-----------|---------------------------|-------|
| 1 | Contract executed | 0 (close date) | Sales |
| 2 | Kickoff / discovery | +1 week | CSM / Implementation |
| 3 | Configuration complete | +implementation_minimum × 0.5 | Implementation |
| 4 | Go-live | +implementation_minimum | Implementation |
| 5 | Success review | +implementation_minimum + 30 days | CSM |

### expansion

| Order | Milestone | Typical offset | Owner |
|-------|-----------|----------------|-------|
| 1 | Amendment executed | 0 | Sales |
| 2 | Provisioning | +1 week | Ops |
| 3 | Enablement session | +2 weeks | CSM |
| 4 | Adoption checkpoint | +30 days | CSM |

### renewal

| Order | Milestone | Typical offset | Owner |
|-------|-----------|----------------|-------|
| 1 | Renewal executed | 0 | Sales |
| 2 | QBR / success review | +14 days | CSM |
| 3 | Expansion review (optional) | +90 days | Account Manager |

### pilot

| Order | Milestone | Typical offset | Owner |
|-------|-----------|----------------|-------|
| 1 | Pilot agreement | 0 | Sales |
| 2 | Pilot kickoff | +3 days | Implementation |
| 3 | Mid-pilot check-in | +50% of pilot term | CSM |
| 4 | Pilot readout / conversion decision | End of pilot term | Sales + CSM |

## Urgency adjustments

| Signal | Allowed adjustment | Not allowed |
|--------|-------------------|-------------|
| Executive sponsor engaged | Pull kickoff earlier (min +3 business days post-close) | Go-live before implementation_minimum |
| Competitive displacement deadline | Flag `flags_to_director` for exec approval | Invent faster SKU |
| "Need it next week" on enterprise bundle | `non_standard=true` → SE | Compress milestones |

## Owner roster (defaults)

- **Sales** — contract, commercial milestones
- **Implementation** — technical delivery, go-live
- **CSM** — enablement, success review, adoption
- **Ops** — provisioning, seat adds
- **Account Manager** — expansion, renewal strategy

Override owners only when `rep_brief` names a specific owner.

## Success criteria pairing

Each `dossier.pain` addressed in scope should have exactly one measurable `success_criteria` entry in scope output. Template examples:

| Pain theme | Measurable criterion example |
|------------|------------------------------|
| Slow onboarding | "Reduce time-to-first-value from X to Y weeks by go-live + 30d" |
| Manual reporting | "Automate Z reports; eliminate N hours/week by day 60" |
| Tool sprawl | "Consolidate N tools to single platform for team of M by go-live" |

Reject: "Improve onboarding", "Better reporting", "Increase efficiency"

## Anti-patterns

- Same milestone template for pilot and enterprise rollout
- Milestones with no owner
- target_date before expected_close for post-sale implementation (unless pilot)
- Copying competitor timeline promises from rep_brief without implementation_minimum check
