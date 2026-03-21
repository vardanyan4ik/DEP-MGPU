#!/usr/bin/env python3
"""Generate synthetic liquidity dataset."""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ASSETS = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOT", "MATIC"]


def main() -> None:
    random.seed(42)
    output = Path("data/liquidity_metrics.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    start = date(2025, 1, 1)
    days = 120

    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "report_date",
                "asset",
                "avg_liquidity_ratio",
                "turnover_usd",
                "volatility_index",
            ]
        )

        for i in range(days):
            current = start + timedelta(days=i)
            for asset in ASSETS:
                ratio = round(random.uniform(0.8, 2.4), 4)
                turnover = round(random.uniform(3_000_000, 45_000_000), 2)
                vol = round(random.uniform(0.1, 0.8), 4)
                writer.writerow([current.isoformat(), asset, ratio, turnover, vol])

    print(f"Generated: {output} | rows={days * len(ASSETS)}")


if __name__ == "__main__":
    main()
