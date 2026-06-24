"""
Eval case definitions for the Marketing Director test harness.

Each case specifies: input, expected routing, assertions, and optional LLM judges.
Cases marked smoke=True run in --mode smoke (2-3 canonical end-to-end checks).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class EvalCase:
    id: str
    name: str
    input_request: str
    expected_specialists: Optional[list[str]] = None
    forbidden_specialists: Optional[list[str]] = None
    should_escalate: Optional[bool] = None
    is_external_facing: Optional[bool] = None
    max_tokens: Optional[int] = None
    canned_overrides: Optional[dict[str, dict]] = None
    judges: Optional[list[str]] = None
    smoke: bool = False


EVAL_CASES: list[EvalCase] = [
    EvalCase(
        id="copy_subject_lines",
        name="Type B: Mother's Day email subject lines",
        input_request=(
            "Write three subject lines for our Mother's Day skincare email. "
            "Audience: women 35-55, tone warm but not saccharine."
        ),
        expected_specialists=["copy_agent", "compliance_agent"],
        forbidden_specialists=["media_agent", "research_agent"],
        should_escalate=False,
        is_external_facing=True,
        smoke=True,
        judges=["brand_voice", "fabrication", "routing_efficiency"],
    ),
    EvalCase(
        id="mothers_day_campaign",
        name="Type A: Full Mother's Day campaign ($50K)",
        input_request=(
            "We need a Mother's Day campaign for our skincare line — email, IG, "
            "and one paid social variant. Budget $50K, two-week flight."
        ),
        expected_specialists=[
            "research_agent",
            "creative_agent",
            "copy_agent",
            "media_agent",
            "compliance_agent",
        ],
        should_escalate=True,
        is_external_facing=True,
        smoke=True,
        judges=["fabrication", "routing_efficiency"],
    ),
    EvalCase(
        id="cpl_spike_analysis",
        name="Type C: CPL spike diagnostic",
        input_request="Why did last month's cost-per-lead spike on paid social?",
        expected_specialists=["analytics_agent"],
        forbidden_specialists=["copy_agent", "creative_agent", "media_agent", "compliance_agent"],
        should_escalate=False,
        is_external_facing=False,
        smoke=True,
        judges=["routing_efficiency"],
    ),
    EvalCase(
        id="spend_pacing",
        name="Type E: Monthly spend pacing",
        input_request="What's our marketing spend pacing this month vs. plan?",
        expected_specialists=["analytics_agent"],
        forbidden_specialists=["copy_agent", "creative_agent", "research_agent"],
        should_escalate=False,
        is_external_facing=False,
    ),
    EvalCase(
        id="holiday_hooks_ideation",
        name="Type D: Holiday campaign hook brainstorm",
        input_request="Brainstorm five hook ideas for our holiday gift guide campaign.",
        expected_specialists=["research_agent", "creative_agent", "copy_agent"],
        forbidden_specialists=["media_agent"],
        should_escalate=False,
        is_external_facing=False,
        judges=["routing_efficiency"],
    ),
    EvalCase(
        id="simple_social_caption",
        name="Type B: Single IG caption (minimal orchestration)",
        input_request=(
            "Write one Instagram caption for our new moisturizer launch. "
            "Keep it under 150 characters."
        ),
        expected_specialists=["copy_agent", "compliance_agent"],
        forbidden_specialists=["research_agent", "media_agent", "creative_agent"],
        should_escalate=False,
        is_external_facing=True,
    ),
    EvalCase(
        id="landing_page_copy",
        name="Type B: Landing page hero copy",
        input_request=(
            "Draft hero headline and subhead for our pricing page. "
            "Claim: saves teams 10 hours per week."
        ),
        expected_specialists=["copy_agent", "compliance_agent"],
        is_external_facing=True,
        canned_overrides={
            "compliance_agent": {
                "severity": "MEDIUM",
                "issues": [{
                    "claim": "saves teams 10 hours per week",
                    "rule_violated": "substantiation-required",
                    "severity": "MEDIUM",
                    "suggested_fix": "Add substantiation or soften to 'can help teams save time'",
                }],
                "required_disclaimers": [],
                "ready_to_publish": False,
            },
        },
    ),
    EvalCase(
        id="crisis_response",
        name="Crisis comms draft (must escalate)",
        input_request=(
            "Draft a public response to today's negative press coverage about our data breach."
        ),
        expected_specialists=["copy_agent", "compliance_agent"],
        should_escalate=True,
        is_external_facing=True,
    ),
]
