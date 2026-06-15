#!/usr/bin/env python3
"""Optional linter: check agent rules/*.yaml syntax and required keys."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PLATFORMS = [".claude", ".github", ".codex", ".gemini"]
REQUIRED_KEYS = {"id", "description"}


def lint_rules() -> list[str]:
    errors: list[str] = []
    for platform in PLATFORMS:
        rules_root = REPO_ROOT / platform / "agents"
        if not rules_root.exists():
            continue
        for rules_dir in rules_root.glob("*/rules"):
            for f in rules_dir.glob("*.yaml"):
                if f.name == "README.md":
                    continue
                try:
                    data = yaml.safe_load(f.read_text(encoding="utf-8"))
                except yaml.YAMLError as e:
                    errors.append(f"{f.relative_to(REPO_ROOT)}: YAML error {e}")
                    continue
                if not isinstance(data, dict):
                    errors.append(f"{f.relative_to(REPO_ROOT)}: expected mapping")
                    continue
                missing = REQUIRED_KEYS - set(data.keys())
                if missing:
                    errors.append(f"{f.relative_to(REPO_ROOT)}: missing {missing}")
    return errors


def main() -> int:
    errors = lint_rules()
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("OK: rules linter passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
