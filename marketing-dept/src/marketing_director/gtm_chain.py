"""
gtm_chain.py — read marketing GTM artifacts from docs/marketing/.

Wires the Python marketing-dept runtime to the same artifact paths
used by Cursor agents (offer-builder → proposal-agent → lp-agent).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .integrations import find_repo_root

ARTIFACT_DIRS = {
    "offers": "docs/marketing/offers",
    "proposals": "docs/marketing/proposals",
    "landing_pages": "docs/marketing/landing-pages",
    "research": "docs/marketing/research",
    "funnels": "docs/marketing/funnels",
    "campaigns": "docs/marketing/campaigns",
}


def list_gtm_artifacts(
    artifact_type: str = "all",
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = repo_root or find_repo_root()
    if root is None:
        return {"error": "repo root not found", "artifacts": []}

    types = list(ARTIFACT_DIRS.keys()) if artifact_type == "all" else [artifact_type]
    results: list[dict[str, str]] = []

    for atype in types:
        rel = ARTIFACT_DIRS.get(atype)
        if not rel:
            continue
        dir_path = root / rel
        if not dir_path.is_dir():
            continue
        for p in sorted(dir_path.glob("*.md")):
            if p.name.upper() == "README.MD":
                continue
            results.append({
                "type": atype,
                "path": str(p.relative_to(root)),
                "name": p.stem,
            })

    return {"artifact_type": artifact_type, "count": len(results), "artifacts": results}


def read_gtm_artifact(
    path: str,
    repo_root: Path | None = None,
    max_chars: int = 50_000,
) -> dict[str, Any]:
    root = repo_root or find_repo_root()
    if root is None:
        return {"error": "repo root not found"}

    file_path = (root / path).resolve()
    try:
        file_path.relative_to(root.resolve())
    except ValueError:
        return {"error": "path outside repo", "path": path}

    if not file_path.is_file():
        return {"error": "file not found", "path": path}

    content = file_path.read_text(encoding="utf-8")
    truncated = len(content) > max_chars
    if truncated:
        content = content[:max_chars] + "\n\n...[truncated]"

    return {
        "path": path,
        "size": file_path.stat().st_size,
        "truncated": truncated,
        "content": content,
    }
