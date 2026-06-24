"""Marketing Director — hierarchical multi-agent orchestrator."""

from marketing_director.director import (
    AnalyticsAgent,
    BaseSpecialist,
    ComplianceAgent,
    CopyAgent,
    CostThresholds,
    CreativeAgent,
    LoopBudget,
    MarketingDirector,
    MediaAgent,
    ModelConfig,
    ResearchAgent,
    SpecialistResult,
    example_usage,
)
from marketing_director.phase1 import create_phase1_director

__all__ = [
    "AnalyticsAgent",
    "BaseSpecialist",
    "ComplianceAgent",
    "CopyAgent",
    "CostThresholds",
    "CreativeAgent",
    "LoopBudget",
    "MarketingDirector",
    "MediaAgent",
    "ModelConfig",
    "ResearchAgent",
    "SpecialistResult",
    "create_phase1_director",
    "example_usage",
]
