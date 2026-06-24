"""
Phase 1 Marketing Director — copy + compliance + repo brand memory.

Ship this before enabling the full multi-agent pipeline. Handles Type B
content requests: subject lines, captions, landing headlines, rewrites.

Usage:
    from anthropic import Anthropic
    from marketing_director.phase1 import create_phase1_director

    director = create_phase1_director(Anthropic())
    result = director.handle_request(
        "Write three subject lines for our weekly newsletter about the new dashboard."
    )
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from marketing_director.director import MarketingDirector, SPECIALIST_TOOL_SCHEMAS
from marketing_director.integrations import (
    create_human_review_handler,
    find_repo_root,
    load_phase1_skills,
    make_repo_specialist_tool_executor,
    repo_brand_memory_loader,
    thresholds_from_config,
)

if TYPE_CHECKING:
    from anthropic import Anthropic

PHASE1_TOOL_NAMES = [
    "copy_agent",
    "compliance_agent",
    "brand_memory_read",
    "request_human_review",
]

PHASE1_SPECIALIST_NAMES = ["copy_agent", "compliance_agent"]

PHASE1_DIRECTOR_SYSTEM_PROMPT = """\
You are the Marketing Director running in **Phase 1** mode — content requests only.

You have two specialists:
- copy_agent: writes messaging, ad copy, email subject lines, social captions
- compliance_agent: reviews external-facing content against legal/brand rules

Utility tools:
- brand_memory_read: load brand voice, prohibited claims, or quarterly plan BEFORE writing
- request_human_review: escalate when compliance flags HIGH/CRITICAL or topic is sensitive

# Phase 1 workflow (Type B content requests)

1. CLASSIFY as content_request unless clearly out of scope.
2. Call brand_memory_read(topic="brand_voice") before delegating to copy_agent.
3. Delegate to copy_agent with full brief, channel, tone, and constraints.
4. ALWAYS call compliance_agent on the copy before finalizing.
5. If compliance returns HIGH or CRITICAL — do NOT approve. Revise or escalate.
6. SYNTHESIZE: deliverable + rationale + decisions + next steps.

# Out of scope in Phase 1

Campaign planning, media budgets, research, analytics — respond:
"This request needs Phase 2+ specialists. I can handle copy/content requests only."

# Operating rules

- Start simple: copy → compliance → done.
- Never skip compliance for external-facing content.
- Never invent statistics or customer quotes.
- Escalate crisis comms, competitor claims, and regulated categories immediately.
"""


def _inject_skills(director: MarketingDirector, repo_root: Path | None) -> None:
    """Prepend loaded skill content to copy and compliance system prompts."""
    skills = load_phase1_skills(repo_root)
    if skills.get("brand_voice") and "copy_agent" in director.specialists:
        agent = director.specialists["copy_agent"]
        agent.SYSTEM_PROMPT = (
            f"{agent.SYSTEM_PROMPT}\n\n# Brand voice skill (loaded from repo)\n"
            f"{skills['brand_voice']}"
        )
    if skills.get("prohibited_claims") and "compliance_agent" in director.specialists:
        agent = director.specialists["compliance_agent"]
        agent.SYSTEM_PROMPT = (
            f"{agent.SYSTEM_PROMPT}\n\n# Prohibited claims skill (loaded from repo)\n"
            f"{skills['prohibited_claims']}"
        )


def create_phase1_director(
    client: "Anthropic",
    repo_root: Path | None = None,
) -> MarketingDirector:
    """
    Production-ready Phase 1 director: copy + compliance + repo skills.

    Wires:
    - brand_memory_loader → skills in .github/skills/ (or .claude/.gemini)
    - copy/compliance specialist tools → brand memory + copy archive
    - human_review_handler → docs/marketing/decisions/ + optional Slack webhook
    """
    root = repo_root or find_repo_root()
    loader = lambda topic: repo_brand_memory_loader(topic, root)
    tool_executor = make_repo_specialist_tool_executor(loader)

    director = MarketingDirector(
        client=client,
        thresholds=thresholds_from_config(root),
        brand_memory_loader=loader,
        human_review_handler=create_human_review_handler(root),
        enabled_specialists=PHASE1_SPECIALIST_NAMES,
        enabled_tools=PHASE1_TOOL_NAMES,
        system_prompt=PHASE1_DIRECTOR_SYSTEM_PROMPT,
    )

    for name in PHASE1_SPECIALIST_NAMES:
        director.specialists[name].tool_executor = tool_executor

    _inject_skills(director, root)
    return director


def phase1_tool_schemas() -> list[dict]:
    """Director tool schemas exposed in Phase 1."""
    names = set(PHASE1_TOOL_NAMES)
    return [t for t in SPECIALIST_TOOL_SCHEMAS if t["name"] in names]
