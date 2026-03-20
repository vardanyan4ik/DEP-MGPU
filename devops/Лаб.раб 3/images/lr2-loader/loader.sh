#!/bin/sh
set -eu

: "${DB_HOST:=db-service}"
: "${DB_PORT:=5432}"
: "${DB_USER:=liquidity}"
: "${DB_PASSWORD:=supersecret}"
: "${DB_NAME:=liquidity_db}"

export PGPASSWORD="$DB_PASSWORD"

# Wait for DB TCP endpoint.
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; do
  echo "loader: waiting for postgres at ${DB_HOST}:${DB_PORT}"
  sleep 2
done

echo "loader: creating demo table and inserting rows"
psql "host=$DB_HOST port=$DB_PORT user=$DB_USER dbname=$DB_NAME" <<'SQL'
CREATE TABLE IF NOT EXISTS liquidity_metrics (
  id SERIAL PRIMARY KEY,
  asset TEXT NOT NULL,
  ratio NUMERIC(10,4) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
INSERT INTO liquidity_metrics (asset, ratio)
VALUES ('BTC', 1.2345), ('ETH', 0.9876);
SQL

echo "loader: completed"
