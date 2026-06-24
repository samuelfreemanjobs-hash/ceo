#!/usr/bin/env python3
"""Cohort retention: naive constant-churn vs month-by-month actuals."""

from __future__ import annotations

import argparse
import json
from typing import Any


def naive_retention(months: int, monthly_retention: float) -> list[float]:
    cohort = [1.0]
    for _ in range(months - 1):
        cohort.append(cohort[-1] * monthly_retention)
    return [round(x, 4) for x in cohort]


def compare(actual: list[float], naive_rate: float) -> dict[str, Any]:
    projected = naive_retention(len(actual), naive_rate)
    deltas = [round(a - p, 4) for a, p in zip(actual, projected)]
    return {
        "actual": actual,
        "naive_projected": projected,
        "delta_actual_minus_naive": deltas,
        "avg_delta": round(sum(deltas) / len(deltas), 4) if deltas else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--retention", type=float, default=0.9, help="Naive monthly retention rate")
    parser.add_argument("--actual", type=str, default="", help="Comma-separated retention by month, e.g. 1.0,0.85,0.72")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.actual:
        actual = [float(x.strip()) for x in args.actual.split(",")]
        out = compare(actual, args.retention)
    else:
        out = {"naive": naive_retention(args.months, args.retention)}

    print(json.dumps(out, indent=2) if args.json else out)


if __name__ == "__main__":
    main()
