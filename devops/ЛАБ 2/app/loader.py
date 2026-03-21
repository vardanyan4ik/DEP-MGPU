#!/usr/bin/env python3
"""ETL loader: CSV -> PostgreSQL."""

import csv
import os
import sys
import time

import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "liquidity")
DB_USER = os.getenv("POSTGRES_USER", "liquidity_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "changeme")
CSV_PATH = os.getenv("CSV_PATH", "/data/liquidity_metrics.csv")

DDL = """
CREATE TABLE IF NOT EXISTS liquidity_metrics (
    metric_id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    asset VARCHAR(16) NOT NULL,
    avg_liquidity_ratio NUMERIC(10, 4) NOT NULL,
    turnover_usd NUMERIC(14, 2) NOT NULL,
    volatility_index NUMERIC(10, 4) NOT NULL
);
"""


def wait_for_db(max_retries: int = 40, delay: int = 2):
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
            )
            print(f"[loader] DB is ready (attempt={attempt})")
            return conn
        except psycopg2.OperationalError:
            print(f"[loader] Waiting for DB... {attempt}/{max_retries}")
            time.sleep(delay)
    print("[loader] DB is unavailable, exiting.")
    sys.exit(1)


def load_csv(conn) -> int:
    cur = conn.cursor()
    cur.execute(DDL)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM liquidity_metrics;")
    if cur.fetchone()[0] > 0:
        print("[loader] Data already exists. Skip loading.")
        cur.close()
        return 0

    inserted = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            cur.execute(
                """
                INSERT INTO liquidity_metrics
                    (report_date, asset, avg_liquidity_ratio, turnover_usd, volatility_index)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    row["report_date"],
                    row["asset"],
                    float(row["avg_liquidity_ratio"]),
                    float(row["turnover_usd"]),
                    float(row["volatility_index"]),
                ),
            )
            inserted += 1

    conn.commit()
    cur.close()
    print(f"[loader] Inserted rows: {inserted}")
    return inserted


def main() -> None:
    conn = wait_for_db()
    try:
        load_csv(conn)
    finally:
        conn.close()
    print("[loader] Completed.")


if __name__ == "__main__":
    main()
