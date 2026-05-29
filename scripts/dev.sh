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

docker compose -f "$ROOT_DIR/infra/docker/docker-compose.yml" up -d postgres
cd "$ROOT_DIR/backend"

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

"$PYTHON_BIN" -m pip install --user ".[dev]"
"$PYTHON_BIN" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
