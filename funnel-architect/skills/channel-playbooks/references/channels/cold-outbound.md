# Cold outbound playbook

Alias / deep dive for `outbound.md`. Load when user says "cold email", "SDR", "outbound sequence", "cold outbound".

## When it works

- ACV $15K+ (or clear enterprise path)
- List of accounts matching ICP
- Articulable pain in 1 sentence
- Sales capacity to run discovery calls

## When it doesn't

- Self-serve $9–$99/mo — economics fail
- No ICP definition — fix `audience-mapping` first
- Product needs trial before conversation (PLG)

## Sequence architecture

| Touch | Channel | Content |
|-------|---------|---------|
| 1 | Email | Problem + insight, no pitch |
| 2 | Email | Micro-case or data point |
| 3 | LinkedIn | Connect + context |
| 4 | Email | Direct ask (15 min) |
| 5 | Call | Optional |

**3–5 touches** over 10–14 days typical. Stop on reply.

## Message rules

- ≤100 words per email
- Personalized first line (real research, not `{company}` fluff)
- One question per email
- No deck attachment on touch 1

## Math

| Metric | Heuristic | Confidence |
|--------|-----------|------------|
| Reply rate | 1–5% | Likely |
| Positive reply | 0.5–2% of sends | Likely |
| Meeting rate | 0.3–1% of sends | Likely |
| CAC | Fully loaded SDR+AE / closed deals | Required |

Run CAC via `funnel-metrics` + code_execution.

## KPIs

| Primary | Guardrail |
|---------|-----------|
| Meetings booked | Bounce rate, spam reports |
| SQL from outbound | Pipeline $ created |

## Failure modes

- Buying lists without fit scoring
- Pitching on touch 1
- No CRM logging → can't attribute
- Same copy to inbound and outbound leads

## Handoff

- Message **angles** → `conversion-copywriting` for full draft
- Pipeline stages → `funnel-frameworks` sales-led map

See also: `outbound.md`
