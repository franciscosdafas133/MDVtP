#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if ! curl -fsS --max-time 1 http://127.0.0.1:8765/api/salud >/dev/null 2>&1; then
  setsid -f /usr/bin/python3 "$ROOT/standalone_server.py" </dev/null >/tmp/i01-standalone.out 2>/tmp/i01-standalone.err
  for i in 1 2 3 4 5 6 7 8 9 10; do
    curl -fsS --max-time 1 http://127.0.0.1:8765/api/salud >/dev/null 2>&1 && break
    sleep 0.3
  done
fi
xdg-open "http://127.0.0.1:8765/" >/dev/null 2>&1 || true
echo "Editor: http://127.0.0.1:8765/"
