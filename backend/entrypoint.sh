#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head

echo "Running seeds..."
SYNC_URL=$(echo "$DATABASE_URL" | sed 's/+asyncpg//')
psql "$SYNC_URL" -f /seeds/seed_categories.sql 2>/dev/null || true
psql "$SYNC_URL" -f /seeds/seed_muscle_groups.sql 2>/dev/null || true

echo "Starting server..."
exec "$@"
