# Offer Builder — JSON Schemas

**Canonical assembled offer:** [`offer-schema.json`](offer-schema.json) (`schema_version: 1.0.0`) — produced by **Offer Director** for CRM, docgen, approval, observability.

## Assembled offer (`offer-schema.json`)

| Block | Source agent | Notes |
|-------|--------------|-------|
| `dossier_ref` | offer-discovery | Full dossier in `dossier-schema.json`; offer stores ref + confidence |
| `scope` | solution-architect | Extended agent output may include `quantity_basis`, `addresses` — Director normalizes |
| `pricing` | offer-pricing | See `pricing-schema.json` (agent emit shape) |
| `risk` | offer-risk-compliance | See `risk-schema.json` |
| `narrative` | offer-copywriter | See `narrative-schema.json` |
| `approval` | offer-director | From pricing thresholds + risk flags |
| `evaluator_result` | offer-evaluator | See `evaluator-result-schema.json` |
| `audit_log` | offer-director | See `audit-log-schema.json` |

## Agent emit schemas

| Schema | Agent |
|--------|-------|
| [`dossier-schema.json`](dossier-schema.json) | offer-discovery |
| [`scope-agent-schema.json`](scope-agent-schema.json) | solution-architect (pre-normalization) |
| [`pricing-schema.json`](pricing-schema.json) | offer-pricing |
| [`risk-schema.json`](risk-schema.json) | offer-risk-compliance |
| [`narrative-schema.json`](narrative-schema.json) | offer-copywriter |
| [`evaluator-result-schema.json`](evaluator-result-schema.json) | offer-evaluator |
| [`audit-log-schema.json`](audit-log-schema.json) | `offer.audit_log` shape |
| [`brief.v1.json`](brief.v1.json) | offer-builder Playbook v1.2 ingest |

## Legacy aliases

- `copy-schema.json` → same as `narrative-schema.json`
- `evaluation-schema.json` → same as `evaluator-result-schema.json`
