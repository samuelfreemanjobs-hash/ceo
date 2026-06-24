"""Integrations between the Python runtime and the CEO orchestration repo."""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any, Callable
from urllib import error, request

import yaml

logger = logging.getLogger(__name__)


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


def load_skill(skill_id: str, repo_root: Path | None = None) -> dict[str, Any]:
    """Load a skill markdown file from the orchestration repo."""
    root = repo_root or find_repo_root()
    if root is None:
        return {"skill": skill_id, "status": "not_found", "content": None}

    for platform in (".github", ".claude", ".gemini"):
        skill_path = root / platform / "skills" / skill_id / "SKILL.md"
        if skill_path.exists():
            return {
                "skill": skill_id,
                "status": "loaded",
                "path": str(skill_path.relative_to(root)),
                "content": skill_path.read_text(encoding="utf-8"),
            }

    return {"skill": skill_id, "status": "not_found", "content": None}


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

    if topic in {"marketing_plan", "marketing-plan-current-quarter", "active_campaigns"}:
        payload["content"] = load_skill("marketing-plan-current-quarter", root)
        payload["skill_status"] = director_cfg.get("skills", {}).get(
            "marketing-plan-current-quarter", {}
        )
    elif topic in {"brand_voice", "brand-voice"}:
        payload["content"] = load_skill("brand-voice", root)
        payload["skill_status"] = director_cfg.get("skills", {}).get("brand-voice", {})
    elif topic in {"prohibited_claims", "prohibited-claims", "prohibited-claims-and-disclaimers"}:
        payload["content"] = load_skill("prohibited-claims-and-disclaimers", root)
        payload["skill_status"] = director_cfg.get("skills", {}).get(
            "prohibited-claims-and-disclaimers", {}
        )
    elif topic in {"active_campaigns"}:
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
            "skills": director_cfg.get("skills", {}),
        }

    return payload


def load_phase1_skills(repo_root: Path | None = None) -> dict[str, str]:
    """Load P0 skill content for Phase 1 copy + compliance wiring."""
    root = repo_root or find_repo_root()
    skills: dict[str, str] = {}
    for skill_id, key in (
        ("brand-voice", "brand_voice"),
        ("prohibited-claims-and-disclaimers", "prohibited_claims"),
    ):
        loaded = load_skill(skill_id, root)
        if loaded.get("status") == "loaded" and loaded.get("content"):
            skills[key] = loaded["content"]
    return skills


def make_repo_specialist_tool_executor(
    brand_memory_loader: Callable[[str], dict],
) -> Callable[[str, dict], dict]:
    """Wire copy/compliance specialist tools to repo-backed brand memory."""

    def executor(tool_name: str, tool_input: dict) -> dict:
        if tool_name == "style_guide_lookup":
            topic = tool_input.get("topic", "brand_voice")
            return brand_memory_loader(topic if topic != "brand_voice" else "brand-voice")
        if tool_name == "rules_engine":
            return brand_memory_loader("prohibited-claims-and-disclaimers")
        if tool_name == "previous_copy_search":
            root = find_repo_root()
            content_dir = (root / "docs/marketing/content") if root else None
            if content_dir and content_dir.is_dir():
                files = [p.name for p in content_dir.glob("*.md")][:10]
                return {"results": files, "source": str(content_dir), "query": tool_input.get("query")}
            return {"results": [], "note": "No prior copy archive — save outputs to docs/marketing/content/"}
        if tool_name == "web_search":
            return {"results": [], "_stub": True, "query": tool_input.get("query")}
        if tool_name == "internal_db_query":
            return {"rows": [], "_stub": True, "source": tool_input.get("source")}
        if tool_name == "analytics_query":
            return {"data": [], "_stub": True, "metric": tool_input.get("metric")}
        return {"error": f"no executor for {tool_name}"}

    return executor


def create_human_review_handler(
    repo_root: Path | None = None,
    slack_webhook_url: str | None = None,
) -> Callable[[dict], dict]:
    """
    Queue human reviews to docs/marketing/decisions/ and optionally notify Slack.

    Set SLACK_WEBHOOK_URL env var or pass slack_webhook_url explicitly.
    """
    root = repo_root or find_repo_root()
    webhook = slack_webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    decisions_dir = (root / "docs/marketing/decisions") if root else Path("reviews")
    decisions_dir.mkdir(parents=True, exist_ok=True)

    def handler(review_request: dict) -> dict:
        review_id = str(uuid.uuid4())
        record = {
            "review_id": review_id,
            "status": "queued",
            "created_at": time.time(),
            **review_request,
        }
        path = decisions_dir / f"review-{review_id}.json"
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        logger.warning("Human review queued: %s → %s", review_id, path)

        if webhook:
            urgency = review_request.get("urgency", "routine")
            reason = review_request.get("reason", "Review required")
            context = review_request.get("context", "")[:500]
            payload = {
                "text": (
                    f":warning: *Marketing review [{urgency}]*\n"
                    f"*Reason:* {reason}\n"
                    f"*Context:* {context}\n"
                    f"*Review ID:* `{review_id}`"
                ),
            }
            try:
                req = request.Request(
                    webhook,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with request.urlopen(req, timeout=10) as resp:
                    record["slack_status"] = resp.status
            except (error.URLError, error.HTTPError) as exc:
                logger.exception("Slack notification failed")
                record["slack_error"] = str(exc)

        record["path"] = str(path)
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        return {
            "review_id": review_id,
            "status": "queued",
            "path": str(path),
            "message": "Review queued for human approval before external publication.",
        }

    return handler


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
