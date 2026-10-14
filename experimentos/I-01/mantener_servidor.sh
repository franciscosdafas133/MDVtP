#!/usr/bin/env bash
# Mantiene el HTML aparte en http://127.0.0.1:8765/ (reinicia si se cae).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONUNBUFFERED=1
while true; do
  echo "[$(date -Is)] arrancando standalone_server.py" >&2
  python3 standalone_server.py >>/tmp/i01-standalone.out 2>>/tmp/i01-standalone.err || true
  echo "[$(date -Is)] se detuvo; reinicio en 1s" >&2
  sleep 1
done
