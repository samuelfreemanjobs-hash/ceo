#!/usr/bin/env python3
"""Ensure Activation Protocol exists in all agent operational specs."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS = [
    "ceo", "analytics", "developer", "pm", "qa",
    "marketer", "ux-expert", "writer", "prepper",
]

ACTIVATION = """

## Activation Protocol

On every session start, before responding:

1. Read `SOUL.md`, `SKILLS.md`, `SUBAGENTS.md`, `DUTIES.md` in this directory.
2. Load applicable files from `rules/` (highest severity first).
3. Hydrate from `memory/session-state.yaml` (goals, blockers, last actions).
4. Read repo `context/how-we-operate.md` and `context/rules-for-ai.md`.
5. Log material decisions to `memory/session-state.yaml` at session end.

Commands: `*status` (emit hydration summary), `*remember <note>` (append to session-state).
"""


def patch_file(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if "Activation Protocol" in text:
        return False
    # Insert before first ## Commands or at end
    marker = "\n## Commands"
    if marker in text:
        text = text.replace(marker, ACTIVATION + marker, 1)
    else:
        text = text.rstrip() + ACTIVATION + "\n"
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    for platform in (".claude", ".github"):
        for aid in AGENTS:
            p = REPO_ROOT / platform / "agents" / aid / f"{aid}.md"
            if patch_file(p):
                print(f"Patched {p.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
