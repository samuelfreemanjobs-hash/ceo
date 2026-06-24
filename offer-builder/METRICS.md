# Offer Builder — Metrics

Track from Phase 1 (evaluator as second call).

| Metric | Why |
|--------|-----|
| Time-to-offer (request → reviewable draft) | Core productivity gain |
| % offers requiring <10% rep edits before send | Quality proxy |
| % discounts auto-approved vs escalated | Policy-fit signal |
| Evaluator pass rate on first cycle | Generator quality |
| Win rate: agent-built vs human control | Business value |
| Token cost per offer | Unit economics |
| % deals where agent flagged risk legal later confirmed | Risk-catch value |
| Evaluator-loop count distribution | Where to focus prompt/skill work |

## Outcome linkage (required Phase 1)

```
offer_id → CRM opportunity_id → close/loss → revenue
```

This join builds the eval set that matters.

## Per-agent SLOs (targets — tune in production)

| Agent | Latency target | Quality signal |
|-------|----------------|----------------|
| Discovery | <60s | dossier_confidence distribution |
| Solution Architect | <90s | dependency check pass rate |
| Pricing | <45s | floor_check_passed rate |
| Risk | <60s | blocking issue precision |
| Copywriter | <45s | grounding score on eval |
| Evaluator | <30s | revision fix rate cycle 2 |
