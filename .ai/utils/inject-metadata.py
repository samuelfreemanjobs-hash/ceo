#!/usr/bin/env python3
"""Inject GitAgent layer frontmatter: last_modified, modified_by, git_commit, checksum."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAYER_NAMES = ("SOUL.md", "SKILLS.md", "SUBAGENTS.md", "DUTIES.md")
AGENT_ROOTS = [
    ROOT / ".claude" / "agents",
    ROOT / ".github" / "agents",
    ROOT / ".codex" / "agents",
    ROOT / ".gemini" / "agents",
]

META_KEYS = ("last_modified", "modified_by", "git_commit", "checksum")


def git_commit() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=ROOT,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


def git_user() -> str:
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"{name} <{email}>" if name and email else name or "unknown"
    except Exception:
        return "unknown"


def body_checksum(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def inject_file(path: Path, dry_run: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return False
    match = re.match(r"---\n.*?\n---\n", text, re.DOTALL)
    if not match:
        return False
    fm = match.group(0)
    body = text[match.end() :]
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    commit = git_commit()
    user = git_user()
    chk = body_checksum(body)
    new_fm = fm
    for key, val in [
        ("last_modified", ts),
        ("modified_by", user),
        ("git_commit", commit),
        ("checksum", chk),
    ]:
        pattern = rf"^{key}:.*$"
        repl = f"{key}: {val}"
        if re.search(pattern, new_fm, re.MULTILINE):
            new_fm = re.sub(pattern, repl, new_fm, count=1, flags=re.MULTILINE)
        else:
            new_fm = new_fm.rstrip("---\n") + f"\n{repl}\n---\n"
    new_text = new_fm + body
    if new_text != text:
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")
        return True
    return False


def iter_layers() -> list[Path]:
    files: list[Path] = []
    for root in AGENT_ROOTS:
        if not root.exists():
            continue
        for name in LAYER_NAMES:
            files.extend(root.glob(f"*/{name}"))
    return sorted(set(files))


def staged_layer_files() -> list[Path]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        ).decode().splitlines()
    except Exception:
        return []
    files: list[Path] = []
    for line in out:
        p = ROOT / line.strip()
        if p.name in LAYER_NAMES and p.parent.parent.name == "agents":
            files.append(p)
    return files


def main() -> int:
    dry = "--dry-run" in sys.argv
    if "--staged" in sys.argv:
        targets = staged_layer_files()
    else:
        paths = [Path(p) for p in sys.argv[1:] if not p.startswith("-")]
        targets = paths if paths else iter_layers()
    changed = sum(1 for p in targets if p.exists() and inject_file(p, dry_run=dry))
    print(f"{'Would update' if dry else 'Updated'} {changed} layer file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
