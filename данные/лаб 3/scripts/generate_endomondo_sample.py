#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from pathlib import Path
import random


random.seed(42)

sports = ["running", "cycling", "gym", "walking"]

records = []
start = datetime(2026, 2, 1, 6, 0, 0)

for i in range(180):
    sport = random.choices(
        population=sports,
        weights=[0.35, 0.25, 0.20, 0.20],
        k=1,
    )[0]

    # Паттерны времени по спорту (для варианта 9)
    if sport == "running":
        hour = random.choice([6, 7, 8, 9])
    elif sport == "gym":
        hour = random.choice([18, 19, 20, 21])
    elif sport == "cycling":
        hour = random.choice([7, 8, 17, 18])
    else:
        hour = random.choice([12, 13, 19, 20])

    day_offset = random.randint(0, 59)
    date_base = start + timedelta(days=day_offset)
    ts_start = date_base.replace(hour=hour, minute=random.randint(0, 59), second=0)

    duration = random.randint(20, 120)
    ts_end = ts_start + timedelta(minutes=duration)

    hr_base = {
        "running": 152,
        "cycling": 146,
        "gym": 138,
        "walking": 118,
    }[sport]

    hr_len = max(12, duration)
    hr = [int(max(90, random.gauss(hr_base, 8))) for _ in range(hr_len)]

    records.append(
        {
            "user_id": i + 1,
            "sport": sport,
            "gender": random.choice(["male", "female"]),
            "timestamp_start": ts_start.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp_end": ts_end.strftime("%Y-%m-%d %H:%M:%S"),
            "heart_rate": hr,
        }
    )

out = Path(__file__).resolve().parents[1] / "data" / "endomondo_sample.json"
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"Wrote {len(records)} rows to {out}")
