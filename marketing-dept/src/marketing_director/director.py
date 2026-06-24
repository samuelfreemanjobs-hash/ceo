"""
Marketing Director — multi-agent orchestrator.

Architecture: Hierarchical / Supervisory (see Building Effective AI Agents, Ch. 3).
Specialists are exposed to the Director as tools; each specialist makes its own
Claude API calls with its own system prompt and (optionally) its own tools —
the recursion described in the agent guide.

Usage:
    from anthropic import Anthropic
    from marketing_director import MarketingDirector

    client = Anthropic()
    director = MarketingDirector(client)
    result = director.handle_request(
        "Write three subject lines for our Mother's Day skincare email."
    )
    print(result["deliverable"])

Dependencies:
    pip install anthropic
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from anthropic import Anthropic
from anthropic.types import Message

logger = logging.getLogger(__name__)


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class ModelConfig:
    """Model selection per role. Revisit quarterly — capabilities and costs shift."""
    director: str = "claude-opus-4-7"
    creative: str = "claude-opus-4-7"
    research: str = "claude-sonnet-4-6"
    copy: str = "claude-sonnet-4-6"
    media: str = "claude-sonnet-4-6"
    analytics: str = "claude-sonnet-4-6"
    compliance: str = "claude-haiku-4-5-20251001"


@dataclass
class LoopBudget:
    """Max tool-use cycles per specialist invocation. Hard cap on runaway loops."""
    director: int = 12       # Director can call several specialists per campaign
    research: int = 8
    creative: int = 6
    copy: int = 5
    media: int = 5
    analytics: int = 6
    compliance: int = 4


@dataclass
class CostThresholds:
    """Trigger human review when these are exceeded."""
    budget_commit_usd: float = 25_000
    estimated_token_cost_usd: float = 50
    repeated_calls_to_same_specialist: int = 3


# =============================================================================
# Specialist tool schemas — what the Director sees
# =============================================================================

SPECIALIST_TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "research_agent",
        "description": (
            "Conduct market research, competitive analysis, audience insights, "
            "or trend analysis. Use this when the campaign or content brief "
            "depends on external information you don't already have — market "
            "size, competitor positioning, audience attitudes, category "
            "benchmarks. Returns a structured report with sourced findings."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The research question. Be specific.",
                },
                "scope": {
                    "type": "string",
                    "description": "Boundaries — geos, time period, audience segment.",
                },
                "depth": {
                    "type": "string",
                    "enum": ["quick", "standard", "deep"],
                    "description": (
                        "quick = <2 min sanity check; standard = <10 min "
                        "primary research pass; deep = full report with multiple sources."
                    ),
                },
                "deadline_minutes": {
                    "type": "integer",
                    "description": "Soft deadline; specialist may return partial if exceeded.",
                },
            },
            "required": ["question", "depth"],
        },
    },
    {
        "name": "creative_agent",
        "description": (
            "Develop creative concepts, visual direction, and brand expression "
            "for a campaign or asset. Use when the request needs more than just "
            "copy — when there's a visual idea, mood, or campaign concept to "
            "develop. Returns 2-3 concepts with rationale and channel adaptations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "The creative brief."},
                "audience": {"type": "string", "description": "Who is this for."},
                "channels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Channels the concept must work across.",
                },
                "mood": {"type": "string", "description": "Emotional tone."},
                "must_include": {"type": "array", "items": {"type": "string"}},
                "must_avoid": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["brief", "audience", "channels"],
        },
    },
    {
        "name": "copy_agent",
        "description": (
            "Write or revise messaging — ad copy, email, landing page, social, "
            "long-form. Use when the deliverable is text that will reach a "
            "customer or prospect. Returns variants (default 3+) with character "
            "counts and A/B hypotheses."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string"},
                "channel": {
                    "type": "string",
                    "description": "Channel context (email subject, IG caption, etc.)",
                },
                "variants": {
                    "type": "integer",
                    "description": "Number of variants to produce.",
                    "default": 3,
                },
                "tone": {"type": "string"},
                "must_include": {"type": "array", "items": {"type": "string"}},
                "constraints": {
                    "type": "object",
                    "description": "e.g., {'max_chars': 60, 'no_emoji': true}",
                },
            },
            "required": ["brief", "channel"],
        },
    },
    {
        "name": "media_agent",
        "description": (
            "Plan media mix, channel allocation, and budget split for a campaign. "
            "Use when there's spend to allocate and channels to choose. Returns "
            "a channel mix with rationale, budget per channel, expected reach, "
            "and KPI targets."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_usd": {"type": "number"},
                "audience": {"type": "string"},
                "channels_available": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Channels to consider (empty = all).",
                },
                "flight_days": {"type": "integer"},
                "kpi_priority": {
                    "type": "string",
                    "enum": ["reach", "engagement", "conversion", "retention"],
                },
                "constraints": {"type": "object"},
            },
            "required": ["budget_usd", "audience", "flight_days", "kpi_priority"],
        },
    },
    {
        "name": "analytics_agent",
        "description": (
            "Analyze performance data, design experiments, or investigate "
            "anomalies. Use for any question that requires querying actual data — "
            "spend pacing, CPL trends, attribution, cohort analysis, A/B test "
            "design. Returns findings with statistical confidence and recommended "
            "actions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "metric_focus": {"type": "array", "items": {"type": "string"}},
                "time_range": {
                    "type": "string",
                    "description": "ISO date range or relative ('last_30d').",
                },
                "segments": {"type": "array", "items": {"type": "string"}},
                "analysis_type": {
                    "type": "string",
                    "enum": ["descriptive", "diagnostic", "predictive", "experiment_design"],
                },
            },
            "required": ["question", "analysis_type"],
        },
    },
    {
        "name": "compliance_agent",
        "description": (
            "Review content for legal, regulatory, and brand-safety issues. "
            "MUST be called before any external-facing content is finalized — "
            "no exceptions. Returns a structured verdict with severity "
            "(NONE/LOW/MEDIUM/HIGH/CRITICAL); HIGH and CRITICAL are hard blocks "
            "that you cannot override by re-prompting."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Full text of content to review.",
                },
                "content_type": {
                    "type": "string",
                    "enum": ["ad", "email", "landing_page", "social", "press", "blog", "deck", "other"],
                },
                "claims_made": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Explicit list of factual or comparative claims.",
                },
                "regulated_category": {
                    "type": "string",
                    "description": "If applicable: health, finance, legal, etc.",
                },
            },
            "required": ["content", "content_type"],
        },
    },
    {
        "name": "brand_memory_read",
        "description": (
            "Retrieve brand guidelines, voice rules, prohibited claims, prior "
            "campaign performance, or active campaign list. Always consult this "
            "BEFORE delegating to specialists on new campaigns."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": (
                        "What to retrieve: 'brand_voice', 'active_campaigns', "
                        "'prohibited_claims', 'marketing_plan', or a specific query."
                    ),
                },
            },
            "required": ["topic"],
        },
    },
    {
        "name": "request_human_review",
        "description": (
            "Escalate to a human reviewer. Use when: budget exceeds threshold, "
            "compliance flags HIGH/CRITICAL, new brand territory, strategic "
            "uncertainty, or any condition listed in your system prompt. "
            "Pauses the workflow."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string", "description": "Why human review is needed."},
                "urgency": {
                    "type": "string",
                    "enum": ["routine", "elevated", "urgent"],
                },
                "context": {"type": "string", "description": "What the human needs to know."},
                "draft_deliverable": {
                    "type": "string",
                    "description": "What you've produced so far, for the human to review.",
                },
            },
            "required": ["reason", "urgency", "context"],
        },
    },
]


DIRECTOR_SYSTEM_PROMPT = """\
You are the Marketing Director — an autonomous orchestrator responsible for \
planning, delegating, and synthesizing marketing work for [COMPANY NAME].

You do not execute specialist work yourself. You decompose requests, route \
them to specialist agents (available as tools), synthesize their outputs into \
a coherent deliverable, and own the final result.

# Your specialists (call as tools)
- research_agent: market research, competitive analysis, audience insights
- creative_agent: visual concepts, brand expression, creative direction
- copy_agent: messaging strategy, ad copy, long-form content
- media_agent: channel selection, budget allocation, media planning
- analytics_agent: performance analysis, A/B test design, attribution
- compliance_agent: brand-safety, legal/regulatory, claim verification

# How to handle every request

1. CLASSIFY: campaign | content_request | analysis_request | ideation | ops
2. PLAN before delegating. State your plan briefly inside <plan></plan> tags.
3. DELEGATE with full context — specialists do NOT see the original user request \
   unless you pass it.
4. PARALLELIZE when sub-tasks are independent (e.g., research + initial \
   competitive scan).
5. NEVER skip compliance for external-facing content.
6. ESCALATE via request_human_review when: budget exceeds $25,000, compliance \
   flags HIGH/CRITICAL, claims involve competitors or regulated categories, \
   crisis comms, new brand territory, or strategic uncertainty.
7. SYNTHESIZE — don't concatenate. Resolve specialist disagreements yourself \
   and document the trade-off.

# Operating principles
- Start simple. If one specialist can handle the request fully, call only that one.
- Cap iteration. If you've called the same specialist 3 times without converging, \
  escalate.
- Always check brand_memory before starting campaign work.
- Final output: (a) the deliverable, (b) a one-paragraph rationale, \
  (c) decisions made with reasoning, (d) suggested next steps.

# What you will not do
- Invent statistics, customer quotes, or research findings.
- Approve work that compliance has flagged HIGH or CRITICAL.
- Commit budget without explicit authorization.
- Make competitor claims that research_agent has not verified.
"""


@dataclass
class SpecialistResult:
    """Structured return from any specialist."""
    status: str  # "ok" | "incomplete" | "error"
    output: dict[str, Any] = field(default_factory=dict)
    notes: str = ""
    tokens_used: int = 0
    loops_used: int = 0


class BaseSpecialist:
    """Base class for all specialist agents."""

    SYSTEM_PROMPT: str = ""
    TOOLS: list[dict[str, Any]] = []

    def __init__(
        self,
        client: Anthropic,
        model: str,
        max_loops: int,
        tool_executor: Optional[Callable[[str, dict], Any]] = None,
        trace_id: str = "",
    ):
        self.client = client
        self.model = model
        self.max_loops = max_loops
        self.tool_executor = tool_executor or (lambda name, inp: {"error": f"no executor for {name}"})
        self.trace_id = trace_id

    def _build_user_message(self, input_data: dict) -> str:
        return json.dumps(input_data, indent=2)

    def _extract_output(self, response: Message) -> dict[str, Any]:
        text = "".join(
            block.text for block in response.content if getattr(block, "type", "") == "text"
        )
        return {"text": text}

    def run(self, input_data: dict) -> SpecialistResult:
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": self._build_user_message(input_data)}
        ]
        total_tokens = 0

        for loop_n in range(self.max_loops):
            logger.info(
                "specialist=%s loop=%d trace=%s",
                self.__class__.__name__, loop_n, self.trace_id,
            )

            kwargs: dict[str, Any] = dict(
                model=self.model,
                max_tokens=2048,
                system=self.SYSTEM_PROMPT,
                messages=messages,
            )
            if self.TOOLS:
                kwargs["tools"] = self.TOOLS

            response = self.client.messages.create(**kwargs)
            total_tokens += response.usage.input_tokens + response.usage.output_tokens

            if response.stop_reason == "end_turn":
                return SpecialistResult(
                    status="ok",
                    output=self._extract_output(response),
                    tokens_used=total_tokens,
                    loops_used=loop_n + 1,
                )

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})

                tool_results = []
                for block in response.content:
                    if getattr(block, "type", "") == "tool_use":
                        try:
                            result = self.tool_executor(block.name, block.input)
                        except Exception as e:
                            logger.exception("tool execution failed")
                            result = {"error": str(e)}
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        })

                messages.append({"role": "user", "content": tool_results})
                continue

            logger.warning("unexpected stop_reason=%s", response.stop_reason)
            break

        return SpecialistResult(
            status="incomplete",
            notes=f"loop budget {self.max_loops} exhausted",
            tokens_used=total_tokens,
            loops_used=self.max_loops,
        )


class ResearchAgent(BaseSpecialist):
    SYSTEM_PROMPT = """\
You are the Research specialist for [COMPANY NAME]'s marketing team. Conduct \
focused, sourced research on the questions the Marketing Director hands you.

Output contract — return your final answer as a JSON object with these fields:
- summary: 2-3 sentence executive summary
- findings: list of {claim, source, confidence: "high"|"medium"|"low"}
- gaps: list of things you couldn't determine from available data
- recommendations: list of next research steps if any

Never fabricate sources. If you cannot find data, say so in `gaps`. Cite the \
source URL or internal system for every finding.
"""
    TOOLS = [
        {
            "name": "web_search",
            "description": "Search the public web for market data, competitor info, etc.",
            "input_schema": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
        {
            "name": "internal_db_query",
            "description": "Query internal data (CRM, customer surveys, past research).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "enum": ["crm", "surveys", "past_research"]},
                    "query": {"type": "string"},
                },
                "required": ["source", "query"],
            },
        },
    ]

    def _build_user_message(self, input_data: dict) -> str:
        return (
            f"Research question: {input_data.get('question')}\n"
            f"Scope: {input_data.get('scope', 'not specified')}\n"
            f"Depth required: {input_data.get('depth')}\n"
            f"Deadline (minutes): {input_data.get('deadline_minutes', 'flexible')}\n\n"
            "Conduct the research and return the JSON object specified in your "
            "system prompt."
        )

    def _extract_output(self, response: Message) -> dict[str, Any]:
        text = "".join(b.text for b in response.content if getattr(b, "type", "") == "text")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text, "_parse_warning": "could not parse JSON"}


class CreativeAgent(BaseSpecialist):
    SYSTEM_PROMPT = """\
You are the Creative Director specialist. Develop campaign concepts that are \
on-brand, emotionally resonant, and adaptable across channels.

Consult the brand-voice skill before generating concepts.

Output contract — JSON:
- concepts: list of {name, core_idea, visual_direction, emotional_arc, \
  channel_adaptations: {channel: adaptation_notes}, rationale}
- recommended: name of your top pick with one-sentence justification
- trade_offs: explicit comparison between concepts
"""

    def _build_user_message(self, input_data: dict) -> str:
        return (
            f"Brief: {input_data['brief']}\n"
            f"Audience: {input_data['audience']}\n"
            f"Channels: {', '.join(input_data['channels'])}\n"
            f"Mood: {input_data.get('mood', 'open')}\n"
            f"Must include: {input_data.get('must_include', [])}\n"
            f"Must avoid: {input_data.get('must_avoid', [])}\n\n"
            "Develop 2-3 distinct creative concepts. Return the JSON object "
            "from your system prompt."
        )


class CopyAgent(BaseSpecialist):
    SYSTEM_PROMPT = """\
You are the Copywriter specialist. Write copy that lands — on-brand, \
channel-appropriate, and clear about what action you want the reader to take.

Always produce at least 3 variants unless instructed otherwise. Each variant \
should test a meaningfully different hypothesis (different hook, different \
benefit, different tone) — don't just rephrase.

Output contract — JSON:
- variants: list of {copy, character_count, hypothesis, suggested_visual_pair}
- recommended_variant: index of your top pick
- notes: anything the Director should know
"""
    TOOLS = [
        {
            "name": "style_guide_lookup",
            "description": "Load brand voice rules and vocabulary from brand memory.",
            "input_schema": {
                "type": "object",
                "properties": {"topic": {"type": "string", "default": "brand_voice"}},
            },
        },
        {
            "name": "previous_copy_search",
            "description": "Search prior copy that performed well (wire to DAM or archive).",
            "input_schema": {
                "type": "object",
                "properties": {"query": {"type": "string"}, "channel": {"type": "string"}},
                "required": ["query"],
            },
        },
    ]

    def _build_user_message(self, input_data: dict) -> str:
        return (
            f"Brief: {input_data['brief']}\n"
            f"Channel: {input_data['channel']}\n"
            f"Tone: {input_data.get('tone', 'on-brand default')}\n"
            f"Variants requested: {input_data.get('variants', 3)}\n"
            f"Must include: {input_data.get('must_include', [])}\n"
            f"Constraints: {input_data.get('constraints', {})}\n\n"
            "Write the copy. Return the JSON object from your system prompt."
        )


class MediaAgent(BaseSpecialist):
    SYSTEM_PROMPT = """\
You are the Media Planner specialist. Allocate budget across channels based on \
audience reach, channel economics, and the priority KPI.

Output contract — JSON:
- channel_mix: list of {channel, budget_usd, percentage, expected_reach, \
  expected_cpa_or_cpc, rationale}
- total_budget_check: confirm the sum equals the input budget
- kpi_targets: dict of channel → expected KPI values
- risk_notes: anything that could blow up the plan
"""

    def _build_user_message(self, input_data: dict) -> str:
        return (
            f"Budget: ${input_data['budget_usd']:,.0f}\n"
            f"Audience: {input_data['audience']}\n"
            f"Flight: {input_data['flight_days']} days\n"
            f"Channels available: {input_data.get('channels_available', 'all')}\n"
            f"KPI priority: {input_data['kpi_priority']}\n"
            f"Constraints: {input_data.get('constraints', {})}\n\n"
            "Produce the media plan. Return the JSON object from your system prompt."
        )


class AnalyticsAgent(BaseSpecialist):
    SYSTEM_PROMPT = """\
You are the Analytics specialist. Investigate performance data, design \
experiments, and answer diagnostic questions with rigor.

Output contract — JSON:
- findings: list of {claim, evidence, confidence: "high"|"medium"|"low"}
- methodology: brief description of how you analyzed
- recommendations: list of actions with expected impact
- data_gaps: anything you couldn't determine
"""
    TOOLS = [
        {
            "name": "analytics_query",
            "description": "Query the analytics platform (GA4, Mixpanel, etc.).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "metric": {"type": "string"},
                    "dimensions": {"type": "array", "items": {"type": "string"}},
                    "time_range": {"type": "string"},
                    "filters": {"type": "object"},
                },
                "required": ["metric"],
            },
        },
    ]

    def _build_user_message(self, input_data: dict) -> str:
        return (
            f"Question: {input_data['question']}\n"
            f"Metrics: {input_data.get('metric_focus', [])}\n"
            f"Time range: {input_data.get('time_range', 'last_30d')}\n"
            f"Segments: {input_data.get('segments', [])}\n"
            f"Analysis type: {input_data['analysis_type']}\n\n"
            "Analyze and return the JSON object from your system prompt."
        )


class ComplianceAgent(BaseSpecialist):
    SYSTEM_PROMPT = """\
You are the Compliance & Brand Safety specialist. Review content against the \
prohibited-claims-and-disclaimers skill.

You MUST return a JSON object with this exact structure:
{
  "severity": "NONE" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  "issues": [
    {
      "claim": "exact text from content",
      "rule_violated": "rule reference",
      "severity": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
      "suggested_fix": "specific revision"
    }
  ],
  "required_disclaimers": ["disclaimer text"],
  "ready_to_publish": true | false
}

Rules:
- Any unsubstantiated comparative claim → MEDIUM minimum.
- Any claim in a regulated category (health/finance/legal) without proper \
  disclaimer → HIGH minimum.
- Any prohibited claim from the skill → CRITICAL.
- If you are uncertain, escalate severity, do not lower it.
- ready_to_publish must be `false` if ANY issue is MEDIUM or higher.
"""
    TOOLS = [
        {
            "name": "rules_engine",
            "description": "Load prohibited claims and required disclaimers rulebook.",
            "input_schema": {
                "type": "object",
                "properties": {"topic": {"type": "string", "default": "prohibited_claims"}},
            },
        },
    ]

    def _build_user_message(self, input_data: dict) -> str:
        return (
            f"Content type: {input_data['content_type']}\n"
            f"Regulated category: {input_data.get('regulated_category', 'none')}\n"
            f"Explicit claims made: {input_data.get('claims_made', [])}\n\n"
            f"Content to review:\n---\n{input_data['content']}\n---\n\n"
            "Review and return the JSON verdict per your system prompt."
        )

    def _extract_output(self, response: Message) -> dict[str, Any]:
        text = "".join(b.text for b in response.content if getattr(b, "type", "") == "text")
        try:
            verdict = json.loads(text)
        except json.JSONDecodeError:
            logger.error("Compliance agent returned unparseable verdict: %s", text[:500])
            return {
                "severity": "HIGH",
                "issues": [{
                    "claim": "n/a",
                    "rule_violated": "agent_output_unparseable",
                    "severity": "HIGH",
                    "suggested_fix": "Re-run review",
                }],
                "required_disclaimers": [],
                "ready_to_publish": False,
                "_parse_error": True,
            }

        sev = verdict.get("severity", "HIGH")
        if sev not in {"NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            verdict["severity"] = "HIGH"
        if verdict["severity"] in {"MEDIUM", "HIGH", "CRITICAL"}:
            verdict["ready_to_publish"] = False
        return verdict


class MarketingDirector:
    """The orchestrator. Maintains campaign context, calls specialists, synthesizes output."""

    def __init__(
        self,
        client: Anthropic,
        models: Optional[ModelConfig] = None,
        budgets: Optional[LoopBudget] = None,
        thresholds: Optional[CostThresholds] = None,
        brand_memory_loader: Optional[Callable[[str], dict]] = None,
        human_review_handler: Optional[Callable[[dict], dict]] = None,
        enabled_specialists: Optional[list[str]] = None,
        enabled_tools: Optional[list[str]] = None,
        system_prompt: Optional[str] = None,
    ):
        self.client = client
        self.models = models or ModelConfig()
        self.budgets = budgets or LoopBudget()
        self.thresholds = thresholds or CostThresholds()

        self.brand_memory_loader = brand_memory_loader or self._default_brand_memory
        self.human_review_handler = human_review_handler or self._default_human_review

        self._director_system = system_prompt or DIRECTOR_SYSTEM_PROMPT
        if enabled_tools:
            names = set(enabled_tools)
            self._director_tools = [t for t in SPECIALIST_TOOL_SCHEMAS if t["name"] in names]
        else:
            self._director_tools = SPECIALIST_TOOL_SCHEMAS

        self.trace_id = str(uuid.uuid4())

        all_specialists: dict[str, BaseSpecialist] = {
            "research_agent": ResearchAgent(
                client, self.models.research, self.budgets.research,
                tool_executor=self._specialist_tool_executor, trace_id=self.trace_id,
            ),
            "creative_agent": CreativeAgent(
                client, self.models.creative, self.budgets.creative,
                tool_executor=self._specialist_tool_executor, trace_id=self.trace_id,
            ),
            "copy_agent": CopyAgent(
                client, self.models.copy, self.budgets.copy,
                tool_executor=self._specialist_tool_executor, trace_id=self.trace_id,
            ),
            "media_agent": MediaAgent(
                client, self.models.media, self.budgets.media,
                tool_executor=self._specialist_tool_executor, trace_id=self.trace_id,
            ),
            "analytics_agent": AnalyticsAgent(
                client, self.models.analytics, self.budgets.analytics,
                tool_executor=self._specialist_tool_executor, trace_id=self.trace_id,
            ),
            "compliance_agent": ComplianceAgent(
                client, self.models.compliance, self.budgets.compliance,
                tool_executor=self._specialist_tool_executor, trace_id=self.trace_id,
            ),
        }

        if enabled_specialists:
            allowed = set(enabled_specialists)
            self.specialists = {k: v for k, v in all_specialists.items() if k in allowed}
        else:
            self.specialists = all_specialists

        self._call_counts: dict[str, int] = {}

    def handle_request(self, user_request: str) -> dict[str, Any]:
        """Main entry point. Returns the final deliverable as a dict."""
        logger.info("director starting trace=%s request=%s", self.trace_id, user_request[:120])
        start = time.time()
        total_tokens = 0

        messages: list[dict[str, Any]] = [{"role": "user", "content": user_request}]
        escalated = False

        for loop_n in range(self.budgets.director):
            response = self.client.messages.create(
                model=self.models.director,
                max_tokens=4096,
                system=self._director_system,
                tools=self._director_tools,
                messages=messages,
            )
            total_tokens += response.usage.input_tokens + response.usage.output_tokens
            logger.info(
                "director loop=%d stop=%s tokens=%d",
                loop_n, response.stop_reason, total_tokens,
            )

            if response.stop_reason == "end_turn":
                return self._finalize(response, total_tokens, time.time() - start, escalated)

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if getattr(block, "type", "") == "tool_use":
                        self._call_counts[block.name] = self._call_counts.get(block.name, 0) + 1
                        if self._call_counts[block.name] > self.thresholds.repeated_calls_to_same_specialist:
                            logger.warning(
                                "specialist %s called too many times — forcing escalation",
                                block.name,
                            )
                            result = self._force_escalate(block.name)
                            escalated = True
                        else:
                            result = self._dispatch(block.name, block.input)
                            if block.name == "request_human_review":
                                escalated = True

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        })
                messages.append({"role": "user", "content": tool_results})
                continue

            logger.warning("director unexpected stop_reason=%s", response.stop_reason)
            break

        return {
            "status": "incomplete",
            "reason": "director loop budget exhausted",
            "trace_id": self.trace_id,
            "tokens_used": total_tokens,
            "wall_time_sec": time.time() - start,
        }

    def _dispatch(self, tool_name: str, tool_input: dict) -> dict:
        if tool_name in self.specialists:
            result = self.specialists[tool_name].run(tool_input)
            return {
                "status": result.status,
                "output": result.output,
                "notes": result.notes,
                "loops_used": result.loops_used,
            }

        if tool_name == "brand_memory_read":
            return self.brand_memory_loader(tool_input.get("topic", ""))

        if tool_name == "request_human_review":
            return self.human_review_handler(tool_input)

        return {"error": f"unknown tool: {tool_name}"}

    def _specialist_tool_executor(self, tool_name: str, tool_input: dict) -> dict:
        if tool_name == "web_search":
            return {"results": [], "_stub": True, "query": tool_input.get("query")}
        if tool_name == "internal_db_query":
            return {"rows": [], "_stub": True, "source": tool_input.get("source")}
        if tool_name == "analytics_query":
            return {"data": [], "_stub": True, "metric": tool_input.get("metric")}
        return {"error": f"no executor for {tool_name}"}

    def _force_escalate(self, tool_name: str) -> dict:
        return self.human_review_handler({
            "reason": (
                f"Repeated calls to {tool_name} ({self._call_counts[tool_name]} times) "
                "— likely stuck in a loop"
            ),
            "urgency": "elevated",
            "context": f"Director kept calling {tool_name} without converging.",
            "draft_deliverable": "",
        })

    def _default_brand_memory(self, topic: str) -> dict:
        return {
            "_stub": True,
            "topic": topic,
            "message": "brand_memory_loader not configured — wire to your knowledge base",
        }

    def _default_human_review(self, request: dict) -> dict:
        logger.warning("HUMAN REVIEW REQUESTED: %s", request)
        return {
            "_stub": True,
            "review_id": str(uuid.uuid4()),
            "status": "queued",
            "message": "Stub: human_review_handler not configured. Wire to Slack/ticketing.",
        }

    def _finalize(
        self, response: Message, tokens: int, wall_time: float, escalated: bool
    ) -> dict[str, Any]:
        deliverable = "".join(
            b.text for b in response.content if getattr(b, "type", "") == "text"
        )
        return {
            "status": "ok",
            "trace_id": self.trace_id,
            "deliverable": deliverable,
            "tokens_used": tokens,
            "wall_time_sec": round(wall_time, 2),
            "escalated": escalated,
            "specialist_call_counts": dict(self._call_counts),
        }


def example_usage() -> None:
    """Wire-up example. Replace stubs with real implementations in production."""
    import os

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    director = MarketingDirector(client=client)
    result = director.handle_request(
        "We need a Mother's Day campaign for our skincare line — "
        "email, IG, and one paid social variant. Budget $50K, two-week flight."
    )

    print(json.dumps(result, indent=2))
