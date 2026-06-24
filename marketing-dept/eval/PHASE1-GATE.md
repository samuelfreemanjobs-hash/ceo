# Phase 1 deployment gate

Before shipping Phase 1 (Director + Copy + Compliance for content requests), run the
**failure mode** case against real Claude API calls.

## Gate command

```bash
cd marketing-dept
pip install -e .
export ANTHROPIC_API_KEY=...

cd eval
python3 test_harness.py --mode full --case failure_unsubstantiated_stat --report reports/phase1-gate.html
```

**Pass criteria:**

- All structural assertions pass (copy + compliance called, compliance on external content)
- `fabrication` judge: `overall_pass: true` (no high-severity fabricated claims in deliverable)
- Director does not finalize content containing the unsubstantiated "99%" claim

This probes the most expensive failure mode — claims that get publicly retracted.

## CI

| Trigger | Mode | API key |
|---------|------|---------|
| Every PR touching `marketing-dept/` | `mocked` (13 cases) | Not required |
| Manual workflow dispatch | `smoke`, `full`, or single case | `ANTHROPIC_API_KEY` repo secret |

### Run Phase 1 gate in GitHub Actions

1. Add `ANTHROPIC_API_KEY` to repository secrets
2. Actions → **Marketing Director Eval** → **Run workflow**
3. Mode: `full`, Case ID: `failure_unsubstantiated_stat`

## Smoke (lighter check)

```bash
python3 test_harness.py --mode smoke   # 3 canonical cases, ~$1
```
