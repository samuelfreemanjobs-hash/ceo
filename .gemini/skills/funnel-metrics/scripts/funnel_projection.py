#!/usr/bin/env python3
"""Funnel volume projection with sensitivity bands."""

from __future__ import annotations

import argparse
import json
import random
from typing import Any


def project(visits: float, rates: dict[str, float], seats_per_customer: float = 1.0, price_per_seat: float = 0.0) -> dict[str, Any]:
    signup = visits * rates.get("signup", 0.0)
    activate = signup * rates.get("activate", 0.0)
    pay = activate * rates.get("pay", 0.0)
    mrr_added = pay * seats_per_customer * price_per_seat
    return {
        "visits": visits,
        "signup": round(signup, 2),
        "activate": round(activate, 2),
        "pay": round(pay, 2),
        "mrr_added": round(mrr_added, 2),
    }


def sensitivity(
    visits: float,
    base_rates: dict[str, float],
    vary_stage: str,
    low: float,
    high: float,
    steps: int = 5,
    **kwargs: float,
) -> list[dict[str, Any]]:
    results = []
    step = (high - low) / max(steps - 1, 1)
    for i in range(steps):
        rate = low + step * i
        rates = dict(base_rates)
        rates[vary_stage] = rate
        row = project(visits, rates, **kwargs)
        row["varied_stage"] = vary_stage
        row["varied_rate"] = round(rate, 4)
        results.append(row)
    return results


def monte_carlo(
    visits: float,
    rate_ranges: dict[str, tuple[float, float]],
    iterations: int = 1000,
    **kwargs: float,
) -> dict[str, Any]:
    pays: list[float] = []
    for _ in range(iterations):
        rates = {k: random.uniform(lo, hi) for k, (lo, hi) in rate_ranges.items()}
        pays.append(project(visits, rates, **kwargs)["pay"])
    pays.sort()
    return {
        "iterations": iterations,
        "pay_p10": round(pays[int(0.10 * len(pays))], 2),
        "pay_p50": round(pays[int(0.50 * len(pays))], 2),
        "pay_p90": round(pays[int(0.90 * len(pays))], 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Funnel projection calculator")
    parser.add_argument("--visits", type=float, default=12000)
    parser.add_argument("--signup", type=float, default=0.08)
    parser.add_argument("--activate", type=float, default=0.35)
    parser.add_argument("--pay", type=float, default=0.55)
    parser.add_argument("--seats", type=float, default=5)
    parser.add_argument("--price", type=float, default=29)
    parser.add_argument("--monte-carlo", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rates = {"signup": args.signup, "activate": args.activate, "pay": args.pay}
    base = project(args.visits, rates, args.seats, args.price)
    out: dict[str, Any] = {"base": base}

    if args.monte_carlo:
        out["monte_carlo"] = monte_carlo(
            args.visits,
            {
                "signup": (args.signup * 0.8, args.signup * 1.2),
                "activate": (args.activate * 0.8, args.activate * 1.2),
                "pay": (args.pay * 0.8, args.pay * 1.2),
            },
            seats_per_customer=args.seats,
            price_per_seat=args.price,
        )

    out["sensitivity_activate"] = sensitivity(
        args.visits, rates, "activate", args.activate * 0.5, min(args.activate * 1.5, 1.0),
        seats_per_customer=args.seats, price_per_seat=args.price,
    )

    print(json.dumps(out, indent=2) if args.json else out)


if __name__ == "__main__":
    main()
