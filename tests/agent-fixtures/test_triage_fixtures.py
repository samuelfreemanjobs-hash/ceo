#!/usr/bin/env python3
"""Lightweight agent behavior fixtures — triage keyword expectations."""

from __future__ import annotations

import sys
from pathlib import Path

# Heuristic tier expectations for regression testing (not LLM calls)
FIXTURES = [
    ("What agents are available?", 0, "direct-response"),
    ("List tasks from the index", 1, "augmented-single"),
    ("Analyze last week's campaign performance", 2, "route-single-agent"),
    ("Plan and implement user notifications", 3, "orchestrator-workers"),
    ("Ship payment processing to production with PCI compliance", 4, "evaluator-optimizer"),
]


def classify_heuristic(text: str) -> tuple[int, str]:
    lower = text.lower()
    if any(k in lower for k in ("ship", "production", "pci", "compliance", "security audit")):
        return 4, "evaluator-optimizer"
    if any(k in lower for k in ("plan and implement", "research and create", "pm → dev")):
        return 3, "orchestrator-workers"
    if any(k in lower for k in ("analyze", "campaign", "implement", "fix bug", "write spec", "ux review")):
        return 2, "route-single-agent"
    if any(k in lower for k in ("list", "read", "grep", "index", "file")):
        return 1, "augmented-single"
    if any(k in lower for k in ("what", "help", "agents available", "how does")):
        return 0, "direct-response"
    return 1, "augmented-single"


def test_fixtures() -> None:
    for text, expected_tier, expected_pattern in FIXTURES:
        tier, pattern = classify_heuristic(text)
        assert tier == expected_tier, f"{text!r}: tier {tier} != {expected_tier}"
        assert pattern == expected_pattern, f"{text!r}: pattern {pattern} != {expected_pattern}"


def test_repo_structure() -> None:
    root = Path(__file__).resolve().parents[2]
    required = [
        root / "context" / "how-we-operate.md",
        root / ".ai" / "utils" / "validate-agents.py",
        root / ".githooks" / "pre-commit",
    ]
    for p in required:
        assert p.is_file(), f"Missing: {p.relative_to(root)}"


if __name__ == "__main__":
    test_fixtures()
    test_repo_structure()
    print("OK: agent behavior fixtures passed")
    sys.exit(0)
