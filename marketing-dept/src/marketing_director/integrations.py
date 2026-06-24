"""Integrations between the Python runtime and the CEO orchestration repo."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def find_repo_root(start: Path | None = None) -> Path | None:
    """Walk upward looking for marketing-director-config.yaml."""
    current = (start or Path.cwd()).resolve()
    for path in [current, *current.parents]:
        if (path / ".github/data/marketing-director-config.yaml").exists():
            return path
        if (path / ".claude/data/marketing-director-config.yaml").exists():
            return path
    return None


def load_marketing_config(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root or find_repo_root()
    if root is None:
        return {}

    for rel in (
        ".github/data/marketing-director-config.yaml",
        ".claude/data/marketing-director-config.yaml",
    ):
        config_path = root / rel
        if config_path.exists():
            with config_path.open(encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    return {}


def repo_brand_memory_loader(topic: str, repo_root: Path | None = None) -> dict[str, Any]:
    """
    Load brand memory topics from the orchestration repo.

    Wire this as `brand_memory_loader` when constructing MarketingDirector.
    """
    root = repo_root or find_repo_root()
    config = load_marketing_config(root)
    director_cfg = config.get("marketing_director", {})

    payload: dict[str, Any] = {
        "topic": topic,
        "source": "repo",
        "repo_root": str(root) if root else None,
    }

    if topic in {"marketing_plan", "marketing-plan-current-quarter"}:
        payload["content"] = {
            "note": "Load marketing-plan skill when installed",
            "skills_priority": director_cfg.get("skills_priority", {}),
        }
    elif topic in {"prohibited_claims", "brand_voice", "active_campaigns"}:
        data_paths = []
        if root:
            for rel in (
                ".github/data/marketing-frameworks.yaml",
                ".github/data/channel-best-practices.yaml",
                ".claude/data/marketing-frameworks.yaml",
            ):
                path = root / rel
                if path.exists():
                    with path.open(encoding="utf-8") as f:
                        data_paths.append({"path": rel, "data": yaml.safe_load(f)})
        payload["content"] = data_paths
    else:
        payload["content"] = {
            "persona": director_cfg.get("persona", {}),
            "thresholds": director_cfg.get("thresholds", {}),
            "specialists": director_cfg.get("specialists", {}),
            "request_types": director_cfg.get("request_types", {}),
        }

    return payload


def thresholds_from_config(repo_root: Path | None = None):
    """Build CostThresholds from marketing-director-config.yaml."""
    from marketing_director.director import CostThresholds

    config = load_marketing_config(repo_root)
    thresholds = config.get("marketing_director", {}).get("thresholds", {})
    return CostThresholds(
        budget_commit_usd=float(thresholds.get("budget_escalation_usd", 25_000)),
        estimated_token_cost_usd=float(thresholds.get("token_cost_confirm_usd", 50)),
        repeated_calls_to_same_specialist=int(thresholds.get("max_specialist_iterations", 3)),
    )
