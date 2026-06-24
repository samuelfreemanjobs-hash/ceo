#!/usr/bin/env python3
"""CAC / LTV / payback calculator with simple verdicts."""

from __future__ import annotations

import argparse
import json
from typing import Any


def calculate(
    cac: float,
    ltv: float,
    gross_margin: float = 0.8,
    monthly_churn: float | None = None,
) -> dict[str, Any]:
    ltv_gross = ltv * gross_margin
    ratio = ltv_gross / cac if cac > 0 else float("inf")
    payback_months = cac / (ltv * gross_margin / 12) if ltv > 0 else float("inf")

    if ratio >= 3:
        verdict = "healthy"
    elif ratio >= 1:
        verdict = "marginal"
    else:
        verdict = "unsustainable"

    out: dict[str, Any] = {
        "cac": cac,
        "ltv": ltv,
        "ltv_gross": round(ltv_gross, 2),
        "ltv_cac_ratio": round(ratio, 2),
        "payback_months": round(payback_months, 1),
        "verdict": verdict,
    }
    if monthly_churn is not None and monthly_churn > 0:
        implied_ltv = 1 / monthly_churn
        out["implied_ltv_from_churn"] = round(implied_ltv, 2)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cac", type=float, required=True)
    parser.add_argument("--ltv", type=float, required=True)
    parser.add_argument("--margin", type=float, default=0.8)
    parser.add_argument("--churn", type=float, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = calculate(args.cac, args.ltv, args.margin, args.churn)
    print(json.dumps(result, indent=2) if args.json else result)


if __name__ == "__main__":
    main()
