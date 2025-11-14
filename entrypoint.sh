#!/bin/bash
set -e

echo "⏳ Waiting for DB"
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done
echo "📦 Applying migrations"
alembic upgrade head

echo "🚀 Start App"
exec "$@"