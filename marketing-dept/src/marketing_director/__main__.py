"""CLI entry point for the Marketing Director runtime."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from anthropic import Anthropic

from marketing_director import MarketingDirector, create_phase1_director
from marketing_director.integrations import (
    create_human_review_handler,
    repo_brand_memory_loader,
    thresholds_from_config,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Marketing Director — hierarchical marketing orchestrator",
    )
    parser.add_argument(
        "request",
        nargs="?",
        help="Marketing request to handle (or pass via stdin)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full result JSON instead of deliverable only",
    )
    parser.add_argument(
        "--phase1",
        action="store_true",
        help="Phase 1 mode: copy + compliance + repo brand memory only (recommended to start)",
    )
    parser.add_argument(
        "--use-repo-config",
        action="store_true",
        help="Load thresholds and brand memory from the CEO orchestration repo",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    user_request = args.request
    if not user_request and not sys.stdin.isatty():
        user_request = sys.stdin.read().strip()
    if not user_request:
        parser.error("Provide a request as an argument or via stdin")

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if args.phase1:
        director = create_phase1_director(client)
    else:
        kwargs: dict = {"client": client}
        if args.use_repo_config:
            kwargs["thresholds"] = thresholds_from_config()
            kwargs["brand_memory_loader"] = repo_brand_memory_loader
            kwargs["human_review_handler"] = create_human_review_handler()
        director = MarketingDirector(**kwargs)

    result = director.handle_request(user_request)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("status") == "ok":
            print(result.get("deliverable", ""))
        else:
            print(json.dumps(result, indent=2))
            sys.exit(1)


if __name__ == "__main__":
    main()
