#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIMESTAMP="$(date +"%Y%m%d-%H%M%S")"
OUTPUT_DIR="$REPO_ROOT/sqls"
OUTPUT_FILE="$OUTPUT_DIR/db_seed_${TIMESTAMP}.sql"
LATEST_SYMLINK="$OUTPUT_DIR/db_seed_latest.sql"

mkdir -p "$OUTPUT_DIR"

echo "[backup-db] Dumping backend_db into $OUTPUT_FILE"
docker compose -f "$REPO_ROOT/docker-compose.yml" exec -T csci3100_db_server \
  pg_dump -U django_user -d backend_db \
  --format=plain --no-owner --no-acl \
  > "$OUTPUT_FILE"

echo "[backup-db] Updating latest symlink -> $LATEST_SYMLINK"
ln -sf "$(basename "$OUTPUT_FILE")" "$LATEST_SYMLINK"

echo "[backup-db] Done"
