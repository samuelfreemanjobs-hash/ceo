# Observability

## Marketing mode

Append JSON lines matching `trace-schema.json` per phase.

## Enterprise mode

One **parent span** per offer (`offer-director`) with **child spans** per specialist. Schema: `enterprise-offer-trace-schema.json`.

### Required captures (per spec §8)

- Per-agent: inputs hash, system-prompt version, tool calls (args + result status), tokens, latency
- Decision events: discounts applied + rule; escalations; evaluator routes
- Outcome linkage: `offer_id → CRM opportunity → close/loss → revenue` (wire Phase 1)

### Failure tags (marketing)

`skipped_discovery`, `generic_positioning`, `feature_list_value_prop`, `missing_proof_ladder`, `pricing_without_anchor`, `ignored_competitive_context`

### Enterprise blockers

`floor_check_failed`, `jurisdiction_blocked`, `unresolved_risk_blocking`, `evaluator_escalate_human`, `scope_dependency_failed`

See [`METRICS.md`](../METRICS.md) for KPIs.
