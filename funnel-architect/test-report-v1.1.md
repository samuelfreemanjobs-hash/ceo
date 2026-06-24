# Funnel Architect — test report v1.1

**Follow-up to:** [test-report-v1.md](test-report-v1.md)  
**Round 2:** [test-report-v2.md](test-report-v2.md)  
**Date:** 2026-06-23

## Changes since v1

- Fix 1: code_execution rule tightened (system prompt + principles)
- Fix 2: Pre-traction DTC section in channel-playbooks
- Fix 3: Full marketplaces reference (funnel-frameworks)
- Fix 4: Referral channel section in channel-playbooks
- All 6 SKILL.md files replaced with authoritative v1.1 bodies
- Round 2: pivot playbook added to audience-mapping (v1.1.2)

## Re-run results

| Dimension | v1 | v1.1 | Target | R2 notes |
|-----------|----|------|--------|----------|
| Specificity | — | ✅ | ≥4.0 | Architecture-level thinking in R2-1, R2-4, R2-5 |
| Math correctness | — | ✅ | 100% | code_execution in R2-3; no head-math in R2 |
| Discovery completeness | — | ✅ | 100% | Gates fired on all edge cases |
| Channel-fit | — | ✅ | 100% | R2-3 structural diagnosis |
| Actionability | — | ✅ | ≥85% | Graduation threshold, parallel funnels |

## Regression loop (pending)

- [ ] Re-run R1 Test 2 (DTC) — validates Fix 2
- [ ] Re-run R1 Test 3 (services) — validates Fix 4
- [ ] Re-run R1 Test 5 (marketplace) — validates Fix 3

## Ship readiness

- [x] 6 authoritative SKILL.md files
- [x] Round-2 edge cases (5/5 pass)
- [x] Pivot playbook (audience-mapping v1.1.2)
- [ ] R1 regression re-run (Tests 2, 3, 5)
- [ ] 5–10 real user sessions
- [ ] Observability traces from live use

**Verdict:** **Ship-ready for real-user testing.** No blocking issues from round 2. Close R1 regression loop before declaring v1.1 fully validated.
