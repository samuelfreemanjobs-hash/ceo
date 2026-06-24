# Observability — Funnel Architect

Log one JSON object per session (or per phase in long sessions). Store in your analytics pipeline, Langfuse, or `docs/marketing/funnels/traces/` if file-based.

## Trace schema

See [trace-schema.json](trace-schema.json).

## Required fields

| Field | Description |
|-------|-------------|
| `trace_id` | `fa_{date}_{shortid}` |
| `phase` | discovery \| frame \| map \| build \| measure \| optimize |
| `skills_invoked` | Skill names loaded |
| `tools_called` | web_search, code_execution, mcp, etc. |
| `model` | e.g. claude-opus-4-7 |
| `latency_ms` | Wall clock |

## Optional fields

| Field | Use |
|-------|-----|
| `user_rating` | 1–5 post-session |
| `user_edits` | % copy changed before ship |
| `tokens_in` / `tokens_out` | Cost tracking |

## Failure modes to tag

- `skipped_discovery`
- `channel_misfit`
- `invented_benchmark`
- `voice_mismatch`
- `channels_as_stages`

## Weekly eval

Sample 20 traces; score against [test-prompts.md](../test-prompts.md) rubric.

## Example

```json
{
  "trace_id": "fa_2026-06-12_a3f9",
  "user_id": "redacted",
  "phase": "build",
  "skills_invoked": ["conversion-copywriting", "funnel-metrics"],
  "tools_called": [
    {"name": "web_search", "query": "B2B SaaS activation benchmarks 2026"},
    {"name": "code_execution", "purpose": "funnel_projection"}
  ],
  "tokens_in": 8420,
  "tokens_out": 3210,
  "model": "claude-opus-4-7",
  "latency_ms": 12400,
  "user_rating": null,
  "user_edits": null
}
```
