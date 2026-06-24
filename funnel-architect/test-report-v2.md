# Funnel Architect — Round-2 Test Report

**Run date:** 2026-06-23 (immediately after round-1 fixes)  
**Goal:** (1) regression-check that round-1 fixes worked, (2) probe edge cases not covered in round-1.

**Fixes applied since round 1:**

- Fix 1 — Code execution rule tightened (system prompt + principles)
- Fix 2 — Pre-traction DTC section added to channel-playbooks
- Fix 3 — Marketplaces reference (280 lines) created in funnel-frameworks
- Fix 4 — Referral channel section added to channel-playbooks

**Test method:** same as round 1 — read each SKILL.md, respond to each prompt following system prompt + skill instructions. Each test is short and diagnostic.

---

## Test R2-1 — Multi-product company

**Prompt:** _"We're a B2B SaaS with three products: a project management tool ($15/seat/mo), an HR product ($25/seat/mo), and a sales CRM ($90/seat/mo). One website. We sell to small businesses. Help me build a funnel."_

**Probing:** the "one funnel, one job" principle from `funnel-frameworks`. Should agent propose multiple funnels rather than one Frankenstein?

**Diagnostic:** ✅ **The "one funnel, one job" principle fired correctly.** Agent rejected the implicit "build one funnel" framing, asked diagnostic questions, and proposed parallel acquisition + unified expansion. No changes needed.

---

## Test R2-2 — Pivot scenario

**Prompt:** _"We've been selling our scheduling tool to law firms for 2 years. It's not growing. We just realized real-estate agents have the same problem and bigger budgets. We want to pivot. Our existing funnel doesn't really work for real estate. What should I do?"_

**Probing:** does the agent handle audience-pivot work specifically, or treat this as a fresh build?

**Diagnostic:** ✅ Handled pivot well — transfers vs doesn't, parallel funnel, audience research first, premature-rebrand warning. ⚠️ **Minor:** lacked structured pivot playbook.

**Action taken:** pivot section added to `audience-mapping` SKILL.md (v1.1.2).

---

## Test R2-3 — Negative result diagnosis

**Prompt:** _"We spent $30K on LinkedIn Ads over 3 months for our B2B SaaS ($12K ACV). Got 47 leads, 4 demos, 0 closed. Was LinkedIn the wrong channel or did we run it wrong?"_

**Diagnostic:** ✅ Excellent structural diagnosis. code_execution fired (Fix 1). Benchmark comparison, ranked hypotheses, refused to kill channel on thin evidence. No changes needed.

---

## Test R2-4 — Hybrid PLG + sales-assisted B2B

**Prompt:** _"Our B2B SaaS has self-serve (mostly individual users at $20/mo) and enterprise contracts ($50K-$200K). Both convert through the same funnel today. It's a mess. How do we split?"_

**Diagnostic:** ✅ Two funnels + graduation threshold per `funnel-frameworks` hybrid guidance. No changes needed.

---

## Test R2-5 — Mature business optimization

**Prompt:** _"Our funnel works. $8M ARR, growing 60% YoY, profitable. CEO wants me to find a 10% improvement somewhere. Where would you look?"_

**Diagnostic:** ✅ Surgical optimization, not redesign. Retention/expansion prioritized. Velocity vs conversion distinguished. No changes needed.

---

# Round-2 synthesis

## What the fixes accomplished

| Fix | Verified in | Result |
|-----|-------------|--------|
| Fix 1: code_execution rule tightening | R2-3 | ✅ Math through code; no head-math in R2 |
| Fix 2: Pre-traction DTC section | not probed in R2 | Re-run R1 Test 2 recommended |
| Fix 3: Marketplaces reference | not probed in R2 | Re-run R1 Test 5 recommended |
| Fix 4: Referral channel section | not probed in R2 | Re-run R1 Test 3 recommended |

**Action:** Re-run R1 Tests 2, 3, and 5 to close regression loop before declaring v1.1 fully validated.

## Patterns that held across rounds

1. Discovery gates fire reliably
2. Math through code_execution (post Fix 1)
3. Honest diagnosis on negative results
4. Architecture-level thinking (R2-1, R2-4, R2-5)
5. Anti-patterns explicitly named

## Verdict

**v1.1 is ship-ready for testing with real users.** No round-2 issue blocking. Pivot playbook gap addressed in audience-mapping v1.1.2.

## Recommended path from here

1. Close regression loop — re-run R1 Tests 2, 3, 5
2. Run 5–10 real user sessions
3. Capture observability per `observability/trace-schema.json`
4. Populate remaining references (priority: email-sequences depth, meta-ads, cold-outbound, benchmarks-saas)
5. ~~Add pivot section to audience-mapping~~ ✅ Done (v1.1.2)

## What NOT to do next

- Don't refactor working SKILL.md files for style
- Don't add new skills (six is right for v1)
- Don't graduate to multi-agent yet (>50 funnels/month gate)
- Don't over-build observability before real sessions

---

_See also: [test-report-v1.md](test-report-v1.md) · [test-prompts.md](test-prompts.md) · 15 total prompts across two rounds._
