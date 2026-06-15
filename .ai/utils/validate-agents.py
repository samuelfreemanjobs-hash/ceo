#!/usr/bin/env python3
"""Validate GitAgent layer completeness and index parity."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENT_IDS = [
    "ceo", "analytics", "developer", "pm", "qa",
    "marketer", "ux-expert", "writer", "prepper",
]
REQUIRED_FILES = ["{id}.md", "SOUL.md", "SKILLS.md", "SUBAGENTS.md", "DUTIES.md"]
REQUIRED_DIRS = ["rules", "memory"]


def validate_agent_dir(base: Path, agent_id: str) -> list[str]:
    errors: list[str] = []
    agent_dir = base / agent_id
    if not agent_dir.is_dir():
        return [f"Missing agent directory: {agent_dir.relative_to(REPO_ROOT)}"]
    for pattern in REQUIRED_FILES:
        f = agent_dir / pattern.format(id=agent_id)
        if not f.is_file():
            errors.append(f"Missing file: {f.relative_to(REPO_ROOT)}")
    for d in REQUIRED_DIRS:
        p = agent_dir / d
        if not p.is_dir():
            errors.append(f"Missing directory: {p.relative_to(REPO_ROOT)}")
        elif d == "memory" and not (p / "session-state.yaml").is_file():
            errors.append(f"Missing memory/session-state.yaml for {agent_id}")
    spec = agent_dir / f"{agent_id}.md"
    if spec.is_file():
        text = spec.read_text(encoding="utf-8")
        if "Activation Protocol" not in text:
            errors.append(f"Missing Activation Protocol in {spec.relative_to(REPO_ROOT)}")
    return errors


def validate_index(index_path: Path, platform: str) -> list[str]:
    errors: list[str] = []
    if not index_path.is_file():
        return [f"Missing index: {index_path.relative_to(REPO_ROOT)}"]
    data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    agents = data.get("agents", [])
    ids = {a["id"] for a in agents}
    for aid in AGENT_IDS:
        if aid not in ids:
            errors.append(f"Index missing agent: {aid} in {index_path.name}")
    platform_root = REPO_ROOT / f".{platform}"
    for a in agents:
        spec_rel = a.get("spec_path") or a.get("path", "")
        if not spec_rel:
            errors.append(f"Index missing path for agent in {index_path.name}")
            continue
        spec = platform_root / spec_rel
        if not spec.is_file():
            errors.append(f"Index path missing: {spec_rel}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", default="claude", choices=["claude", "github", "codex", "gemini"])
    args = parser.parse_args()

    if args.platform in ("claude", "github"):
        base = REPO_ROOT / f".{args.platform}" / "agents"
        index = REPO_ROOT / f".{args.platform}" / "agents.index.yaml"
    else:
        base = REPO_ROOT / f".{args.platform}" / "agents"
        index = REPO_ROOT / f".{args.platform}" / "agents.index.yaml"

    errors: list[str] = []
    for aid in AGENT_IDS:
        errors.extend(validate_agent_dir(base, aid))
    errors.extend(validate_index(index, args.platform))

    team_brain = [
        REPO_ROOT / "context" / "how-we-operate.md",
        REPO_ROOT / "inbox" / "README.md",
        REPO_ROOT / "specs" / "README.md",
    ]
    for p in team_brain:
        if not p.is_file():
            errors.append(f"Missing team-brain file: {p.relative_to(REPO_ROOT)}")

    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: {args.platform} agents + team-brain validated ({len(AGENT_IDS)} agents)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
