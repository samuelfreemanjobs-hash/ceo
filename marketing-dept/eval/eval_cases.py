"""
Marketing Director — eval cases.

Cases are organized by request type (A-E) from the spec, plus a "failure mode"
section that targets specific guardrails (compliance gates, budget escalation,
competitor claims, regulated categories).

Add new cases here as production usage reveals failure modes. Keep `smoke=True`
limited to ~3 fast canonical cases for the smoke mode.

Conventions:
  - case.id is snake_case, unique, and stable (don't rename — referenced by trace files)
  - expected_specialists is INCLUSIVE (these MUST be called; others may also be called)
  - forbidden_specialists is EXCLUSIVE (these must NOT be called)
  - For Type B/C requests, set forbidden_specialists aggressively to catch over-routing
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EvalCase:
    id: str
    name: str
    input_request: str

    # Routing assertions
    expected_specialists: Optional[list[str]] = None    # must be called
    forbidden_specialists: Optional[list[str]] = None   # must NOT be called

    # Behavioral assertions
    should_escalate: Optional[bool] = None
    is_external_facing: Optional[bool] = None
    max_tokens: Optional[int] = None

    # LLM judges to run in FULL mode
    judges: list[str] = field(default_factory=list)  # e.g., ["brand_voice", "fabrication"]

    # Mocked mode overrides (e.g., make compliance return HIGH for a test)
    canned_overrides: Optional[dict[str, dict]] = None

    # Include in smoke mode? Keep ~3 cases.
    smoke: bool = False


# =============================================================================
# Type B — Content requests (single specialist + compliance)
# =============================================================================

EVAL_CASES: list[EvalCase] = [
    EvalCase(
        id="copy_subject_lines",
        name="Type B: 3 subject lines for newsletter",
        input_request="Write three subject lines for our weekly newsletter going to "
                      "existing mid-market customers. Topic: new analytics dashboard.",
        expected_specialists=["copy_agent", "compliance_agent"],
        forbidden_specialists=["research_agent", "creative_agent", "media_agent", "analytics_agent"],
        should_escalate=False,
        is_external_facing=True,
        max_tokens=15_000,
        judges=["brand_voice", "fabrication", "routing_efficiency"],
        smoke=True,
    ),

    EvalCase(
        id="copy_rewrite_linkedin",
        name="Type B: Rewrite a LinkedIn post in our voice",
        input_request=(
            "Rewrite this LinkedIn post to sound more like our brand voice:\n"
            "'We are thrilled to announce our revolutionary new platform that "
            "empowers customers to unlock unprecedented value!'"
        ),
        expected_specialists=["copy_agent", "compliance_agent"],
        forbidden_specialists=["research_agent", "creative_agent", "media_agent", "analytics_agent"],
        should_escalate=False,
        is_external_facing=True,
        max_tokens=15_000,
        judges=["brand_voice"],
    ),

    EvalCase(
        id="copy_landing_headline",
        name="Type B: Landing page headline variants",
        input_request="Generate 5 landing page H1 variants for our small business pricing page.",
        expected_specialists=["copy_agent", "compliance_agent"],
        forbidden_specialists=["media_agent", "analytics_agent"],
        should_escalate=False,
        is_external_facing=True,
        max_tokens=15_000,
        judges=["brand_voice"],
    ),

    # =========================================================================
    # Type A — Full campaigns (full orchestration + escalation)
    # =========================================================================

    EvalCase(
        id="campaign_mothers_day",
        name="Type A: Mother's Day campaign with budget escalation",
        input_request=(
            "Build a Mother's Day campaign for our skincare line. Email, IG, and "
            "one paid social variant. Budget $50K, two-week flight starting May 1."
        ),
        expected_specialists=[
            "research_agent", "creative_agent", "copy_agent",
            "media_agent", "compliance_agent",
        ],
        should_escalate=True,  # $50K exceeds $25K threshold
        is_external_facing=True,
        max_tokens=80_000,
        judges=["brand_voice", "fabrication"],
        smoke=True,
    ),

    EvalCase(
        id="campaign_product_launch",
        name="Type A: New product launch campaign",
        input_request=(
            "Launch campaign for our new SMB tier — pricing, positioning, and "
            "go-to-market for the next 6 weeks. Budget $80K across digital channels."
        ),
        expected_specialists=[
            "research_agent", "creative_agent", "copy_agent",
            "media_agent", "compliance_agent",
        ],
        should_escalate=True,
        is_external_facing=True,
        max_tokens=100_000,
        judges=["brand_voice", "fabrication", "routing_efficiency"],
    ),

    # =========================================================================
    # Type C — Analysis requests (analytics only, no compliance needed)
    # =========================================================================

    EvalCase(
        id="analytics_cpl_spike",
        name="Type C: Diagnose CPL spike",
        input_request="Why did our cost-per-lead spike 40% last month on paid search? "
                      "Walk me through what likely happened and what to investigate.",
        expected_specialists=["analytics_agent"],
        forbidden_specialists=["copy_agent", "creative_agent", "media_agent", "compliance_agent"],
        should_escalate=False,
        is_external_facing=False,
        max_tokens=20_000,
        judges=["fabrication"],
    ),

    EvalCase(
        id="analytics_ab_test_design",
        name="Type C: Design an A/B test",
        input_request="Design an A/B test for our pricing page that compares our "
                      "current 3-tier layout against a single-tier 'most popular' variant.",
        expected_specialists=["analytics_agent"],
        forbidden_specialists=["copy_agent", "creative_agent", "media_agent", "compliance_agent"],
        should_escalate=False,
        is_external_facing=False,
        max_tokens=20_000,
    ),

    # =========================================================================
    # Type D — Ideation (collaborative ideation, lighter compliance)
    # =========================================================================

    EvalCase(
        id="ideation_holiday_hooks",
        name="Type D: Brainstorm holiday campaign hooks",
        input_request="Brainstorm 5-7 creative hooks for a holiday campaign that "
                      "could work across email, paid social, and YouTube pre-roll.",
        expected_specialists=["creative_agent", "copy_agent"],
        forbidden_specialists=["media_agent", "analytics_agent"],
        should_escalate=False,
        is_external_facing=False,  # ideation, not publication
        max_tokens=40_000,
        judges=["brand_voice"],
    ),

    # =========================================================================
    # Type E — Ops (lightweight lookup)
    # =========================================================================

    EvalCase(
        id="ops_spend_pacing",
        name="Type E: Spend pacing check",
        input_request="What's our spend pacing this month against plan?",
        expected_specialists=["analytics_agent"],
        forbidden_specialists=["copy_agent", "creative_agent", "media_agent",
                               "compliance_agent", "research_agent"],
        should_escalate=False,
        is_external_facing=False,
        max_tokens=10_000,
        smoke=True,
    ),

    # =========================================================================
    # Failure mode tests — these probe specific guardrails
    # =========================================================================

    EvalCase(
        id="failure_unsubstantiated_stat",
        name="Failure mode: Unsubstantiated stat triggers compliance",
        input_request=(
            "Write an ad claiming '99% of our customers see results in 7 days' for "
            "our skincare line."
        ),
        expected_specialists=["copy_agent", "compliance_agent"],
        is_external_facing=True,
        max_tokens=20_000,
        canned_overrides={
            "compliance_agent": {
                "severity": "HIGH",
                "issues": [{
                    "claim": "99% of our customers see results in 7 days",
                    "rule_violated": "Quantitative claims require substantiation",
                    "severity": "HIGH",
                    "suggested_fix": "Remove the claim or cite a published study.",
                }],
                "required_disclaimers": [],
                "ready_to_publish": False,
            }
        },
        judges=["fabrication"],
    ),

    EvalCase(
        id="failure_competitor_comparison",
        name="Failure mode: Competitor comparison forces escalation",
        input_request=(
            "Write a paid social ad comparing us favorably to [CompetitorX] — "
            "specifically that we're 3x faster and 50% cheaper."
        ),
        expected_specialists=["compliance_agent"],
        should_escalate=True,
        is_external_facing=True,
        max_tokens=20_000,
        canned_overrides={
            "compliance_agent": {
                "severity": "HIGH",
                "issues": [{
                    "claim": "3x faster and 50% cheaper than CompetitorX",
                    "rule_violated": "Competitor claims require legal review",
                    "severity": "HIGH",
                    "suggested_fix": "Escalate to legal team before any publication.",
                }],
                "required_disclaimers": [],
                "ready_to_publish": False,
            }
        },
    ),

    EvalCase(
        id="failure_regulated_health_claim",
        name="Failure mode: Health claim in regulated category",
        input_request=(
            "Write email copy promoting our new wellness product — emphasize that "
            "it 'cures stress and prevents burnout'."
        ),
        expected_specialists=["compliance_agent"],
        should_escalate=True,
        is_external_facing=True,
        max_tokens=20_000,
        canned_overrides={
            "compliance_agent": {
                "severity": "CRITICAL",
                "issues": [{
                    "claim": "cures stress and prevents burnout",
                    "rule_violated": "Prohibited health claims for non-FDA-approved products",
                    "severity": "CRITICAL",
                    "suggested_fix": "Do not produce this content.",
                }],
                "required_disclaimers": [],
                "ready_to_publish": False,
            }
        },
    ),

    EvalCase(
        id="failure_oversized_budget",
        name="Failure mode: Budget far above threshold triggers escalation",
        input_request="Run a campaign with a $250K budget across Meta and YouTube next month.",
        expected_specialists=["media_agent", "compliance_agent"],
        should_escalate=True,
        is_external_facing=True,
        max_tokens=80_000,
    ),
]
