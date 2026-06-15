#!/usr/bin/env python3
"""Sync GitAgent agent trees from .claude to .codex and .gemini."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / ".claude" / "agents"
TARGETS = {
    ".codex": ROOT / ".codex" / "agents",
    ".gemini": ROOT / ".gemini" / "agents",
}


def sync_tree(target_platform: str, target_root: Path) -> None:
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True, exist_ok=True)

    for agent_dir in sorted(SOURCE.iterdir()):
        if not agent_dir.is_dir():
            continue
        agent_id = agent_dir.name
        dest = target_root / agent_id
        shutil.copytree(agent_dir, dest)
        for path in dest.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
                text = path.read_text(encoding="utf-8")
                text = text.replace(".claude/", f"{target_platform}/")
                path.write_text(text, encoding="utf-8")
        print(f"  ✓ {target_platform}/agents/{agent_id}/")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Source not found: {SOURCE}")
    print("Syncing GitAgent trees from .claude ...")
    for platform, target in TARGETS.items():
        sync_tree(platform, target)
    print("Done. Run generate-indexes in each platform folder if needed.")


if __name__ == "__main__":
    main()
