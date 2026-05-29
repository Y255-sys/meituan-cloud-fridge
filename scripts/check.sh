#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if command -v python3.13 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3.13)"
elif [ -x /opt/miniconda3/bin/python3.13 ]; then
  PYTHON_BIN="/opt/miniconda3/bin/python3.13"
else
  PYTHON_BIN="$(command -v python3)"
fi

cd "$ROOT_DIR/backend"
"$PYTHON_BIN" -m compileall app scripts
PYTHONPATH="$ROOT_DIR/backend" DATABASE_URL=sqlite+pysqlite:////private/tmp/meituan_cloud_fridge_check.db AUTO_CREATE_TABLES=true AUTO_SEED_DEMO_DATA=true "$PYTHON_BIN" -m pytest
