#!/usr/bin/env python3
"""Append and summarize orchestration log entries (JSONL)."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = ROOT / ".ai" / "data" / "orchestration-log.jsonl"


def append_entry(
    tier: int,
    pattern: str,
    agents: list[str],
    rationale: str,
    outcome: str = "pending",
    cycles: int = 0,
    est_tokens: int = 1,
    human_review: bool = False,
    request_id: str | None = None,
) -> dict:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id or str(uuid.uuid4())[:8],
        "tier": tier,
        "pattern": pattern,
        "agents": agents,
        "rationale": rationale,
        "outcome": outcome,
        "cycles": cycles,
        "est_tokens": est_tokens,
        "human_review": human_review,
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def read_entries(limit: int | None = None) -> list[dict]:
    if not LOG_PATH.exists():
        return []
    lines = LOG_PATH.read_text(encoding="utf-8").strip().splitlines()
    entries = [json.loads(ln) for ln in lines if ln.strip()]
    return entries[-limit:] if limit else entries


def summarize() -> dict:
    entries = read_entries()
    if not entries:
        return {"count": 0}
    tiers: dict[int, int] = {}
    agents: dict[str, int] = {}
    for e in entries:
        tiers[e.get("tier", 0)] = tiers.get(e.get("tier", 0), 0) + 1
        for a in e.get("agents", []):
            agents[a] = agents.get(a, 0) + 1
    return {
        "count": len(entries),
        "by_tier": tiers,
        "by_agent": agents,
        "human_review_pending": sum(
            1 for e in entries if e.get("human_review") and e.get("outcome") == "pending"
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Orchestration log utility")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("append", help="Append log entry")
    a.add_argument("--tier", type=int, required=True)
    a.add_argument("--pattern", required=True)
    a.add_argument("--agents", default="", help="Comma-separated agent ids")
    a.add_argument("--rationale", required=True)
    a.add_argument("--outcome", default="success")
    a.add_argument("--est-tokens", type=int, default=1)

    sub.add_parser("tail", help="Last 10 entries")
    sub.add_parser("summary", help="Aggregate stats")

    args = p.parse_args()
    if args.cmd == "append":
        entry = append_entry(
            tier=args.tier,
            pattern=args.pattern,
            agents=[x.strip() for x in args.agents.split(",") if x.strip()],
            rationale=args.rationale,
            outcome=args.outcome,
            est_tokens=args.est_tokens,
        )
        print(json.dumps(entry, indent=2))
    elif args.cmd == "tail":
        for e in read_entries(10):
            print(json.dumps(e))
    elif args.cmd == "summary":
        print(json.dumps(summarize(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
