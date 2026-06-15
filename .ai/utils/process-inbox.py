#!/usr/bin/env python3
"""Process inbox items into specs or archive."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INBOX = REPO_ROOT / "inbox"
SPECS = REPO_ROOT / "specs"
ARCHIVE = INBOX / "archive"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "item"


def list_inbox() -> list[Path]:
    if not INBOX.exists():
        return []
    return sorted(
        p for p in INBOX.glob("*.md")
        if p.is_file() and p.name != "README.md"
    )


def cmd_list() -> int:
    items = list_inbox()
    if not items:
        print("Inbox empty.")
        return 0
    for p in items:
        print(p.name)
    return 0


def cmd_promote(path: Path, title: str | None) -> int:
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        return 1
    content = path.read_text(encoding="utf-8")
    first_line = content.splitlines()[0] if content else ""
    derived = title or first_line.lstrip("# ").strip() or path.stem
    cycle_id = f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-{slugify(derived)}"
    cycle_dir = SPECS / cycle_id
    cycle_dir.mkdir(parents=True, exist_ok=True)
    (cycle_dir / "00-brief.md").write_text(
        f"# Brief: {derived}\n\n"
        f"**Promoted from:** `{path.relative_to(REPO_ROOT)}`\n"
        f"**Created:** {datetime.now(timezone.utc).isoformat()}\n\n"
        f"## Source\n\n{content}\n",
        encoding="utf-8",
    )
    (cycle_dir / "01-research.md").write_text(
        f"# Research: {derived}\n\n_Pending — assign Ana or manual research._\n",
        encoding="utf-8",
    )
    (cycle_dir / "02-spec.md").write_text(
        f"# Spec: {derived}\n\n## Problem\n\n## Requirements\n\n## Acceptance criteria\n\n",
        encoding="utf-8",
    )
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(ARCHIVE / path.name))
    print(f"Promoted to specs/{cycle_id}/")
    return 0


def cmd_archive(path: Path) -> int:
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        return 1
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(ARCHIVE / path.name))
    print(f"Archived {path.name}")
    return 0


def cmd_process_all(dry_run: bool) -> int:
    items = list_inbox()
    if not items:
        print("Nothing to process.")
        return 0
    promoted = 0
    for p in items:
        if dry_run:
            print(f"[dry-run] would promote {p.name}")
            continue
        if cmd_promote(p, None) == 0:
            promoted += 1
    print(f"Promoted {promoted} item(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inbox processor for team-brain")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List inbox items")

    promote = sub.add_parser("promote", help="Promote inbox item to spec cycle")
    promote.add_argument("file", type=Path)
    promote.add_argument("--title", default=None)

    archive = sub.add_parser("archive", help="Archive inbox item")
    archive.add_argument("file", type=Path)

    proc = sub.add_parser("process-all", help="Promote all inbox items")
    proc.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "promote":
        f = args.file if args.file.is_absolute() else INBOX / args.file
        return cmd_promote(f, args.title)
    if args.cmd == "archive":
        f = args.file if args.file.is_absolute() else INBOX / args.file
        return cmd_archive(f)
    if args.cmd == "process-all":
        return cmd_process_all(args.dry_run)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
