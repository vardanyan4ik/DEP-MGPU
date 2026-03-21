#!/usr/bin/env python3
"""FastAPI service for liquidity metrics."""

import logging
import os
from typing import Any

import psycopg2
from fastapi import FastAPI

APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "liquidity")
DB_USER = os.getenv("POSTGRES_USER", "liquidity_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "changeme")

app = FastAPI(title="Liquidity FastAPI", version=APP_VERSION)
logger = logging.getLogger("uvicorn.error")


@app.on_event("startup")
def startup_log() -> None:
    logger.info("Starting Liquidity FastAPI | version=%s", APP_VERSION)


def db_connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "analytics_app"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"app_version": APP_VERSION}


@app.get("/")
def root() -> dict[str, Any]:
    conn = db_connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM liquidity_metrics;")
    rows_count = cur.fetchone()[0]

    cur.execute(
        """
        SELECT asset, avg_liquidity_ratio, report_date
        FROM liquidity_metrics
        ORDER BY report_date DESC
        LIMIT 5;
        """
    )
    latest = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "project": "Liquidity App",
        "app_version": APP_VERSION,
        "rows_in_db": rows_count,
        "latest_records": [
            {"asset": r[0], "avg_liquidity_ratio": float(r[1]), "report_date": str(r[2])}
            for r in latest
        ],
    }
