"""
Marketing Director — test harness.

Three layers of testing, each with a different cost/coverage trade-off:

  1. MOCKED  — no real API calls. Tests routing/dispatch logic by replacing
              specialists with MockSpecialist. Fast (<1s/case), free, deterministic.
              Catches: routing failures, escalation rule bugs, schema validation.

  2. SMOKE   — real API calls on 2-3 canonical cases. Verifies end-to-end
              integration. ~30s, <$1.

  3. FULL    — real API calls on all eval cases + LLM judges. Real evaluation.
              ~5-10 min, ~$5-15 depending on case mix.

Usage:
    python test_harness.py --mode mocked
    python test_harness.py --mode smoke
    python test_harness.py --mode full --report report.html
    python test_harness.py --case copy_subject_lines

JSONL traces are written to ./traces/<run_id>.jsonl in the same format as
your orchestration-log.jsonl, so they're queryable with the same tools.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

from marketing_director import (
    MarketingDirector,
    BaseSpecialist,
    SpecialistResult,
)

from eval_cases import EVAL_CASES, EvalCase

logger = logging.getLogger("test_harness")


@dataclass
class TraceEvent:
    ts: float
    kind: str
    tool: str = ""
    input: dict = field(default_factory=dict)
    output: dict = field(default_factory=dict)
    duration_ms: float = 0
    note: str = ""


class TraceRecorder:
    """Captures every dispatch event for assertions and replay."""

    def __init__(self, trace_id: str = ""):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.events: list[TraceEvent] = []
        self.started_at = time.time()

    def record(self, kind: str, **kwargs) -> None:
        self.events.append(TraceEvent(ts=time.time() - self.started_at, kind=kind, **kwargs))

    def specialists_called(self) -> list[str]:
        return [
            e.tool for e in self.events
            if e.kind == "dispatch_start" and e.tool.endswith("_agent")
        ]

    def unique_specialists(self) -> set[str]:
        return set(self.specialists_called())

    def was_escalated(self) -> bool:
        return any(e.kind == "escalation" for e in self.events)

    def call_count(self, tool: str) -> int:
        return sum(1 for e in self.events if e.kind == "dispatch_start" and e.tool == tool)

    def to_jsonl(self) -> str:
        return "\n".join(
            json.dumps({"trace_id": self.trace_id, **asdict(e)}) for e in self.events
        )


class InstrumentedDirector(MarketingDirector):
    """Subclass that hooks dispatch to record events. Use in tests only."""

    def __init__(self, *args, recorder: Optional[TraceRecorder] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.recorder = recorder or TraceRecorder(trace_id=self.trace_id)

    def _dispatch(self, tool_name: str, tool_input: dict) -> dict:
        start = time.time()
        self.recorder.record("dispatch_start", tool=tool_name, input=tool_input)
        try:
            result = super()._dispatch(tool_name, tool_input)
        except Exception as e:
            self.recorder.record("dispatch_error", tool=tool_name, note=str(e))
            raise
        self.recorder.record(
            "dispatch_end",
            tool=tool_name,
            output={"status": result.get("status", "?")},
            duration_ms=(time.time() - start) * 1000,
        )
        if tool_name == "request_human_review":
            self.recorder.record("escalation", tool=tool_name, input=tool_input)
        return result


class MockSpecialist(BaseSpecialist):
    """Returns canned output without calling the API."""

    def __init__(self, canned_output: dict, status: str = "ok"):
        self.canned_output = canned_output
        self.status = status
        self.calls: list[dict] = []

    def run(self, input_data: dict) -> SpecialistResult:
        self.calls.append(input_data)
        return SpecialistResult(
            status=self.status,
            output=self.canned_output,
            tokens_used=0,
            loops_used=1,
        )


def install_mocks(director: MarketingDirector, canned: dict[str, dict]) -> None:
    for name in list(director.specialists.keys()):
        output = canned.get(name, {"_mocked": True})
        director.specialists[name] = MockSpecialist(output)


DEFAULT_CANNED_OUTPUTS: dict[str, dict] = {
    "research_agent": {
        "summary": "Mock research summary.",
        "findings": [{"claim": "mock", "source": "mock://", "confidence": "medium"}],
        "gaps": [],
        "recommendations": [],
    },
    "creative_agent": {
        "concepts": [{
            "name": "Concept A",
            "core_idea": "mock",
            "visual_direction": "mock",
            "emotional_arc": "mock",
            "channel_adaptations": {},
            "rationale": "mock",
        }],
        "recommended": "Concept A",
        "trade_offs": "mock",
    },
    "copy_agent": {
        "variants": [
            {"copy": "Subject 1", "character_count": 9, "hypothesis": "mock", "suggested_visual_pair": ""},
            {"copy": "Subject 2", "character_count": 9, "hypothesis": "mock", "suggested_visual_pair": ""},
            {"copy": "Subject 3", "character_count": 9, "hypothesis": "mock", "suggested_visual_pair": ""},
        ],
        "recommended_variant": 0,
        "notes": "mock",
    },
    "media_agent": {
        "channel_mix": [{
            "channel": "email",
            "budget_usd": 5000,
            "percentage": 100,
            "expected_reach": 0,
            "expected_cpa_or_cpc": 0,
            "rationale": "mock",
        }],
        "total_budget_check": "ok",
        "kpi_targets": {},
        "risk_notes": "mock",
    },
    "analytics_agent": {
        "findings": [{"claim": "mock", "evidence": "mock", "confidence": "medium"}],
        "methodology": "mock",
        "recommendations": [],
        "data_gaps": [],
    },
    "compliance_agent": {
        "severity": "NONE",
        "issues": [],
        "required_disclaimers": [],
        "ready_to_publish": True,
    },
}


@dataclass
class AssertionResult:
    name: str
    passed: bool
    detail: str = ""


class Assertions:
    @staticmethod
    def specialists_include(recorder: TraceRecorder, required: list[str]) -> AssertionResult:
        called = recorder.unique_specialists()
        missing = set(required) - called
        return AssertionResult(
            name=f"specialists_include({required})",
            passed=not missing,
            detail=f"missing: {missing}" if missing else f"called: {sorted(called)}",
        )

    @staticmethod
    def specialists_exclude(recorder: TraceRecorder, forbidden: list[str]) -> AssertionResult:
        called = recorder.unique_specialists()
        accidentally_called = set(forbidden) & called
        return AssertionResult(
            name=f"specialists_exclude({forbidden})",
            passed=not accidentally_called,
            detail=f"unexpectedly called: {accidentally_called}" if accidentally_called else "ok",
        )

    @staticmethod
    def escalated(recorder: TraceRecorder, should: bool = True) -> AssertionResult:
        actual = recorder.was_escalated()
        return AssertionResult(
            name=f"escalated={should}",
            passed=actual == should,
            detail=f"actual: {actual}",
        )

    @staticmethod
    def specialist_called_at_most(recorder: TraceRecorder, tool: str, n: int) -> AssertionResult:
        count = recorder.call_count(tool)
        return AssertionResult(
            name=f"{tool}_called_<={n}",
            passed=count <= n,
            detail=f"called {count} times",
        )

    @staticmethod
    def deliverable_nonempty(result: dict) -> AssertionResult:
        deliverable = result.get("deliverable", "")
        return AssertionResult(
            name="deliverable_nonempty",
            passed=bool(deliverable and len(deliverable.strip()) > 20),
            detail=f"length: {len(deliverable)}",
        )

    @staticmethod
    def tokens_under(result: dict, limit: int) -> AssertionResult:
        used = result.get("tokens_used", 0)
        return AssertionResult(
            name=f"tokens_under({limit})",
            passed=used < limit,
            detail=f"used: {used}",
        )

    @staticmethod
    def compliance_was_called_if_external(recorder: TraceRecorder, is_external: bool) -> AssertionResult:
        if not is_external:
            return AssertionResult(name="compliance_check_if_external", passed=True, detail="n/a")
        called = "compliance_agent" in recorder.unique_specialists()
        return AssertionResult(
            name="compliance_check_if_external",
            passed=called,
            detail="compliance_agent called" if called else "MISSING — external content without compliance",
        )


class LLMJudge:
    JUDGE_PROMPT: str = ""
    JUDGE_MODEL: str = "claude-sonnet-4-6"

    def __init__(self, client):
        self.client = client

    def evaluate(self, content_under_review: str, context: dict | None = None) -> dict:
        prompt = self._build_prompt(content_under_review, context or {})
        response = self.client.messages.create(
            model=self.JUDGE_MODEL,
            max_tokens=1024,
            system=self.JUDGE_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in response.content if getattr(b, "type", "") == "text")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"_parse_error": True, "raw": text, "overall_pass": False, "pass": False}

    def _build_prompt(self, content: str, context: dict) -> str:
        return f"Content to evaluate:\n---\n{content}\n---"


class BrandVoiceJudge(LLMJudge):
    JUDGE_PROMPT = """\
You are evaluating marketing copy against the brand-voice rewrite test for \
[YOUR_BRAND]. For each of the 5 checks below, answer pass=true or pass=false \
with a one-sentence reason.

The 5 checks:
1. GENERIC: Could a generic competitor have written this? If yes, fail.
2. VOCABULARY: Does it use specific words from our vocabulary, or marketing-speak?
3. YOU_WE: Is there a "you" or only "we" / company-centric language?
4. SPECIFICITY: Are claims specific enough to be checkable?
5. READ_ALOUD: Does it sound like a person, or like a brochure?

Return ONLY a JSON object:
{
  "checks": {
    "generic":     {"pass": bool, "reason": str},
    "vocabulary":  {"pass": bool, "reason": str},
    "you_we":      {"pass": bool, "reason": str},
    "specificity": {"pass": bool, "reason": str},
    "read_aloud":  {"pass": bool, "reason": str}
  },
  "score": int (0-5),
  "overall_pass": bool (true if score >= 4),
  "rewrite_suggestion": str (only if overall_pass is false)
}
"""


class FabricationJudge(LLMJudge):
    JUDGE_PROMPT = """\
You are auditing marketing output for fabricated claims. A claim is fabricated \
if it asserts a specific statistic, customer quote, ranking, comparison, or \
fact that is not clearly sourced or attributed.

Return ONLY a JSON object:
{
  "fabricated_claims": [
    {"claim": str, "why_suspect": str, "severity": "low"|"medium"|"high"}
  ],
  "overall_pass": bool (true if no high-severity fabrications),
  "notes": str
}
"""


class RoutingEfficiencyJudge(LLMJudge):
    JUDGE_PROMPT = """\
You are evaluating whether a marketing orchestrator used the right amount of \
agent coordination for a given request.

You will see: the original user request, the list of specialists called, and \
the final deliverable. Return a JSON object:

{
  "appropriate_specialists": bool,
  "over_engineered": bool (called more specialists than needed?),
  "under_engineered": bool (skipped specialists that were needed?),
  "ideal_specialist_set": [list of specialist names],
  "verdict": "efficient" | "wasteful" | "insufficient",
  "explanation": str
}
"""

    def _build_prompt(self, content: str, context: dict) -> str:
        return (
            f"USER REQUEST:\n{context.get('request', '')}\n\n"
            f"SPECIALISTS CALLED:\n{context.get('specialists', [])}\n\n"
            f"FINAL DELIVERABLE:\n{content}\n"
        )


@dataclass
class CaseOutcome:
    case_id: str
    case_name: str
    passed: bool
    assertions: list[AssertionResult]
    judge_results: dict[str, dict]
    tokens_used: int
    wall_time_sec: float
    escalated: bool
    specialists_called: list[str]
    deliverable: str
    trace_path: str = ""


class Runner:
    def __init__(self, mode: str, client=None, traces_dir: str = "./traces"):
        self.mode = mode
        self.client = client
        self.traces_dir = Path(traces_dir)
        self.traces_dir.mkdir(parents=True, exist_ok=True)
        self.run_id = time.strftime("%Y%m%d-%H%M%S")

    def run(self, cases: list[EvalCase]) -> list[CaseOutcome]:
        outcomes = []
        for i, case in enumerate(cases):
            logger.info("[%d/%d] %s — %s", i + 1, len(cases), case.id, case.name)
            try:
                outcome = self._run_case(case)
            except Exception as e:
                logger.exception("case %s crashed", case.id)
                outcome = CaseOutcome(
                    case_id=case.id,
                    case_name=case.name,
                    passed=False,
                    assertions=[AssertionResult("crashed", False, str(e))],
                    judge_results={},
                    tokens_used=0,
                    wall_time_sec=0,
                    escalated=False,
                    specialists_called=[],
                    deliverable="",
                )
            outcomes.append(outcome)
            logger.info(
                "  → %s (tokens=%d, time=%.1fs)",
                "PASS" if outcome.passed else "FAIL",
                outcome.tokens_used,
                outcome.wall_time_sec,
            )
        return outcomes

    def _run_case(self, case: EvalCase) -> CaseOutcome:
        recorder = TraceRecorder()

        if self.mode == "mocked":
            from unittest.mock import MagicMock

            client = MagicMock()
            director = InstrumentedDirector(
                client=client,
                recorder=recorder,
                brand_memory_loader=lambda topic: {"topic": topic, "_mocked": True},
                human_review_handler=lambda req: {"_mocked": True, "review_id": "mock"},
            )
            install_mocks(director, DEFAULT_CANNED_OUTPUTS | (case.canned_overrides or {}))
            self._install_director_script(director, case)
        else:
            director = InstrumentedDirector(client=self.client, recorder=recorder)

        result = director.handle_request(case.input_request)
        assertions = self._run_assertions(case, recorder, result)

        judge_results = {}
        if self.mode == "full" and case.judges:
            judge_results = self._run_judges(case, result, recorder)

        trace_path = self.traces_dir / f"{self.run_id}_{case.id}.jsonl"
        trace_path.write_text(recorder.to_jsonl())

        all_passed = all(a.passed for a in assertions) and all(
            j.get("overall_pass", False) for j in judge_results.values()
        )

        return CaseOutcome(
            case_id=case.id,
            case_name=case.name,
            passed=all_passed,
            assertions=assertions,
            judge_results=judge_results,
            tokens_used=result.get("tokens_used", 0),
            wall_time_sec=result.get("wall_time_sec", 0),
            escalated=result.get("escalated", False),
            specialists_called=recorder.specialists_called(),
            deliverable=result.get("deliverable", ""),
            trace_path=str(trace_path),
        )

    def _install_director_script(self, director: InstrumentedDirector, case: EvalCase) -> None:
        from unittest.mock import MagicMock

        def make_response(content_blocks, stop_reason):
            r = MagicMock()
            r.content = content_blocks
            r.stop_reason = stop_reason
            r.usage = MagicMock(input_tokens=100, output_tokens=100)
            return r

        def make_tool_use(name: str, input_data: dict):
            b = MagicMock()
            b.type = "tool_use"
            b.name = name
            b.input = input_data
            b.id = f"toolu_{uuid.uuid4().hex[:8]}"
            return b

        def make_text(text: str):
            b = MagicMock()
            b.type = "text"
            b.text = text
            return b

        script = []
        for sp in case.expected_specialists or []:
            script.append(make_response([make_tool_use(sp, {"_test": True})], "tool_use"))
        if case.should_escalate:
            script.append(make_response(
                [make_tool_use(
                    "request_human_review",
                    {"reason": "test", "urgency": "routine", "context": "test"},
                )],
                "tool_use",
            ))
        script.append(make_response(
            [make_text(f"Final deliverable for case {case.id}: [mocked output with enough length]")],
            "end_turn",
        ))

        director.client.messages.create.side_effect = script

    def _run_assertions(
        self, case: EvalCase, recorder: TraceRecorder, result: dict
    ) -> list[AssertionResult]:
        out: list[AssertionResult] = []

        if case.expected_specialists is not None:
            out.append(Assertions.specialists_include(recorder, case.expected_specialists))
        if case.forbidden_specialists is not None:
            out.append(Assertions.specialists_exclude(recorder, case.forbidden_specialists))
        if case.should_escalate is not None:
            out.append(Assertions.escalated(recorder, should=case.should_escalate))
        if case.is_external_facing is not None:
            out.append(Assertions.compliance_was_called_if_external(
                recorder, case.is_external_facing
            ))
        if case.max_tokens is not None:
            out.append(Assertions.tokens_under(result, case.max_tokens))

        out.append(Assertions.deliverable_nonempty(result))

        for sp in recorder.unique_specialists():
            out.append(Assertions.specialist_called_at_most(recorder, sp, 3))

        return out

    def _run_judges(
        self, case: EvalCase, result: dict, recorder: TraceRecorder
    ) -> dict[str, dict]:
        judge_results: dict[str, dict] = {}
        deliverable = result.get("deliverable", "")

        if "brand_voice" in case.judges:
            judge_results["brand_voice"] = BrandVoiceJudge(self.client).evaluate(deliverable)
        if "fabrication" in case.judges:
            judge_results["fabrication"] = FabricationJudge(self.client).evaluate(deliverable)
        if "routing_efficiency" in case.judges:
            judge_results["routing_efficiency"] = RoutingEfficiencyJudge(self.client).evaluate(
                deliverable,
                context={
                    "request": case.input_request,
                    "specialists": recorder.specialists_called(),
                },
            )
        return judge_results


def render_text_report(outcomes: list[CaseOutcome]) -> str:
    lines = []
    passed = sum(1 for o in outcomes if o.passed)
    total_tokens = sum(o.tokens_used for o in outcomes)
    total_time = sum(o.wall_time_sec for o in outcomes)

    lines.append("=" * 72)
    lines.append(f"EVAL RESULTS: {passed}/{len(outcomes)} passed")
    lines.append(f"Total tokens: {total_tokens:,}   Total time: {total_time:.1f}s")
    lines.append("=" * 72)

    for o in outcomes:
        marker = "PASS" if o.passed else "FAIL"
        lines.append(f"\n{marker} [{o.case_id}] {o.case_name}")
        lines.append(
            f"    tokens={o.tokens_used}  time={o.wall_time_sec:.1f}s  "
            f"escalated={o.escalated}  specialists={o.specialists_called}"
        )
        for a in o.assertions:
            am = "  ok" if a.passed else "  FAIL"
            lines.append(f"    {am} {a.name}: {a.detail}")
        for jname, jres in o.judge_results.items():
            jm = "  ok" if jres.get("overall_pass") else "  FAIL"
            score = jres.get("score", "n/a")
            lines.append(f"    {jm} judge[{jname}]: pass={jres.get('overall_pass')} score={score}")

    return "\n".join(lines)


def render_html_report(outcomes: list[CaseOutcome], run_id: str) -> str:
    rows = []
    for o in outcomes:
        status = "PASS" if o.passed else "FAIL"
        color = "#1a7f37" if o.passed else "#cf222e"
        assertion_rows = "".join(
            f"<li style='color:{'#1a7f37' if a.passed else '#cf222e'}'>"
            f"{'ok' if a.passed else 'FAIL'} <b>{a.name}</b>: {a.detail}</li>"
            for a in o.assertions
        )
        judge_rows = "".join(
            f"<li><b>{name}</b>: pass={r.get('overall_pass')} — {json.dumps(r)[:300]}</li>"
            for name, r in o.judge_results.items()
        )
        rows.append(f"""
        <tr>
          <td><b>{o.case_id}</b><br><small>{o.case_name}</small></td>
          <td style='color:{color};font-weight:bold'>{status}</td>
          <td>{o.tokens_used:,}</td>
          <td>{o.wall_time_sec:.1f}s</td>
          <td>{', '.join(o.specialists_called)}</td>
          <td><ul style='margin:0;padding-left:18px'>{assertion_rows}</ul></td>
          <td><ul style='margin:0;padding-left:18px'>{judge_rows or '<i>n/a</i>'}</ul></td>
        </tr>
        """)
    passed = sum(1 for o in outcomes if o.passed)
    return f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Eval {run_id}</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; margin: 20px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; text-align: left; }}
  th {{ background: #f6f8fa; }}
</style></head>
<body>
  <h1>Marketing Director Eval — {run_id}</h1>
  <p><b>{passed}/{len(outcomes)} passed</b></p>
  <table>
    <thead><tr><th>Case</th><th>Result</th><th>Tokens</th><th>Time</th>
    <th>Specialists</th><th>Assertions</th><th>Judges</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</body></html>"""


def main():
    parser = argparse.ArgumentParser(description="Marketing Director eval harness")
    parser.add_argument("--mode", choices=["mocked", "smoke", "full"], default="mocked")
    parser.add_argument("--case", help="Run a single case by ID")
    parser.add_argument("--report", help="Path to write report (.txt or .html)")
    parser.add_argument("--traces-dir", default="./traces")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    cases = EVAL_CASES
    if args.case:
        cases = [c for c in cases if c.id == args.case]
        if not cases:
            print(f"No case with id={args.case}", file=sys.stderr)
            sys.exit(2)
    if args.mode == "smoke":
        cases = [c for c in cases if c.smoke]

    client = None
    if args.mode in {"smoke", "full"}:
        try:
            from anthropic import Anthropic
        except ImportError:
            print("anthropic SDK not installed: pip install anthropic", file=sys.stderr)
            sys.exit(2)
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ANTHROPIC_API_KEY not set", file=sys.stderr)
            sys.exit(2)
        client = Anthropic()

    runner = Runner(mode=args.mode, client=client, traces_dir=args.traces_dir)
    outcomes = runner.run(cases)

    print(render_text_report(outcomes))
    if args.report:
        report_path = Path(args.report)
        if report_path.suffix == ".html":
            report_path.write_text(render_html_report(outcomes, runner.run_id))
        else:
            report_path.write_text(render_text_report(outcomes))
        print(f"\nReport written to {report_path}")

    sys.exit(0 if all(o.passed for o in outcomes) else 1)


if __name__ == "__main__":
    main()
