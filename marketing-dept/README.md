# Marketing Director — Python Runtime

Production Python implementation of the Marketing Director hierarchical orchestrator. This is the **programmatic runtime** that complements the agent persona definitions in `.github/agents/marketing-director.md`, `.claude/agents/`, and `.gemini/agents/`.

**Architecture:** Hierarchical / Supervisory (Building Effective AI Agents, Ch. 3)  
Each specialist is exposed to the Director as a tool and makes its own Claude API calls with its own system prompt.

## Install

```bash
cd marketing-dept
pip install -e .
```

Requires `ANTHROPIC_API_KEY` in the environment.

## Quick start

```python
from anthropic import Anthropic
from marketing_director import MarketingDirector

client = Anthropic()
director = MarketingDirector(client)

result = director.handle_request(
    "Write three subject lines for our Mother's Day skincare email."
)
print(result["deliverable"])
```

## CLI

```bash
# From repo root (with package installed)
marketing-director "Write three subject lines for our Mother's Day skincare email."

# Use CEO repo config for thresholds + brand memory
marketing-director --use-repo-config "Plan a Q1 launch campaign for product X"

# Full JSON output (trace ID, token usage, escalation flags)
marketing-director --json "Why did last month's CPL spike?"
```

## Repo integration

When run from within this repository, pass `--use-repo-config` to load:

- Budget and iteration thresholds from `marketing-director-config.yaml`
- Brand memory topics from marketing data files

```python
from anthropic import Anthropic
from marketing_director import MarketingDirector
from marketing_director.integrations import repo_brand_memory_loader, thresholds_from_config

director = MarketingDirector(
    client=Anthropic(),
    thresholds=thresholds_from_config(),
    brand_memory_loader=repo_brand_memory_loader,
)
```

## Specialists (built-in)

| Tool | Class | Model (default) |
|------|-------|-----------------|
| `research_agent` | ResearchAgent | Sonnet 4.6 |
| `creative_agent` | CreativeAgent | Opus 4.7 |
| `copy_agent` | CopyAgent | Sonnet 4.6 |
| `media_agent` | MediaAgent | Sonnet 4.6 |
| `analytics_agent` | AnalyticsAgent | Sonnet 4.6 |
| `compliance_agent` | ComplianceAgent | Haiku 4.5 |

Director utility tools: `brand_memory_read`, `request_human_review`

## Production wiring (stubs → real)

Replace stub tool executors in `director.py`:

| Stub | Wire to |
|------|---------|
| `web_search` | Search provider / MCP |
| `internal_db_query` | CRM, surveys, past research |
| `analytics_query` | GA4, Mixpanel, Amplitude |
| `brand_memory_loader` | Notion, Drive, vector store |
| `human_review_handler` | Slack, ticketing system |

**Never auto-write** to customer-facing systems without human-in-the-loop.

## Observability

Every `handle_request()` returns:

```json
{
  "status": "ok",
  "trace_id": "...",
  "deliverable": "...",
  "tokens_used": 1234,
  "wall_time_sec": 11.2,
  "escalated": false,
  "specialist_call_counts": {"copy_agent": 1, "compliance_agent": 1}
}
```

Propagate `trace_id` through your logging pipeline for end-to-end replay.

## Related files

| Asset | Path |
|-------|------|
| Agent persona (Cursor/Claude/Gemini) | `.github/agents/marketing-director.md` |
| Orchestration config | `.github/data/marketing-director-config.yaml` |
| Output directories | `docs/marketing/` |

Keep `DIRECTOR_SYSTEM_PROMPT` in `director.py` in sync with the agent markdown when you update either.

## Testing

Three-layer eval harness in `eval/`:

| Mode | API calls | Cost | Use for |
|------|-----------|------|---------|
| `mocked` | None | Free | Routing, escalation, compliance gates |
| `smoke` | 3 canonical cases | ~$1 | End-to-end integration check |
| `full` | All cases + LLM judges | ~$5-15 | Pre-release evaluation |

```bash
cd marketing-dept
pip install -e .

# Fast deterministic tests (no API key needed)
cd eval && python3 test_harness.py --mode mocked   # 13 cases

# Single case
python3 test_harness.py --mode mocked --case copy_subject_lines

# Smoke test (requires ANTHROPIC_API_KEY)
python3 test_harness.py --mode smoke

# Full eval with HTML report
python3 test_harness.py --mode full --report reports/eval.html
```

Traces are written to `eval/traces/<run_id>_<case>.jsonl` for replay and debugging.

Eval cases live in `eval/eval_cases.py` — add cases there without modifying the harness.

## Phase 1 deployment gate

Before shipping Phase 1, run the failure-mode case against real Claude:

```bash
cd eval
python3 test_harness.py --mode full --case failure_unsubstantiated_stat --report reports/phase1-gate.html
```

See [`eval/PHASE1-GATE.md`](eval/PHASE1-GATE.md) for pass criteria and CI instructions.
