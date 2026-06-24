# Funnel Architect — v1 test prompts

Run weekly on a sample; score against §7 evaluation criteria in `funnel-architect-agent.md`.

| # | Prompt | Expected behavior |
|---|--------|-------------------|
| 1 | **B2B SaaS PLG** — See [worked-example.md](worked-example.md) | Full 6 phases; activation focus; AARRR |
| 2 | **DTC skincare** — "$45 serum, 80% Meta traffic, 1.2% purchase rate, want 2%" | DTC framework; Meta + PDP funnel; unit economics |
| 3 | **Services agency** — "B2B marketing agency, $8K/mo retainers, inbound only, need more qualified calls" | Qualify → discovery → proposal; no Meta scale advice |
| 4 | **Info product** — " $497 course, webinar → cart, 3% webinar-to-purchase" | AIDCAS or webinar funnel; email sequence |
| 5 | **Marketplace** — "Two-sided local services marketplace, supply side thin" | Two-sided funnel; supply-first sequencing |
| 6 | **Audit** — "Here's our funnel: [paste stage table]. Where's the leak?" | Delta recommendations; no full rewrite unless broken |
| 7 | **Copy refresh** — "Rewrite hero for [URL], audience = [ICP], objection = price" | 3 variants + evaluator; asks voice if missing |
| 8 | **Metrics only** — "Model 10K visits, 5% signup, 30% activate, 50% pay, $99/mo, 3 seats avg" | code_execution only; sensitivity band |
| 9 | **Single channel** — "Should we do LinkedIn ads or outbound for $40K ACV enterprise HR software?" | channel-playbooks; honest fit; one recommendation |
| 10 | **Ambiguous brief** — "Help me grow" | Discovery only; refuses to build until minimum inputs |

## Scoring rubric (1–5)

| Dimension | Target |
|-----------|--------|
| Specificity | ≥4.0 avg |
| Math correctness | 100% spot-check |
| Channel-fit | No obvious mismatches |
| Actionability | ≥85% executable |
| Discovery completeness | 100% for prompts 1–5, 10 |

## Log results

Record in [test-report-v1.md](test-report-v1.md) and [learnings/OUTCOMES-LOG.md](learnings/OUTCOMES-LOG.md).
