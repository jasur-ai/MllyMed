#!/bin/bash
# MllyMed konteyner entrypoint: backend (127.0.0.1:INTERNAL_PORT) + socat (0.0.0.0:PUBLIC_PORT)
# Kod o'zgarmaydi — "python3 -m backend.server" hech qanday parametrsiz ishga tushadi.
set -euo pipefail

APP_DIR="${APP_DIR:-/app}"
INTERNAL_PORT="${INTERNAL_PORT:-9000}"
PUBLIC_PORT="${PUBLIC_PORT:-8200}"

cd "${APP_DIR}"

python3 -m backend.server --port "${INTERNAL_PORT}" &
BACK_PID=$!

socat "TCP-LISTEN:${PUBLIC_PORT},fork,reuseaddr" "TCP:127.0.0.1:${INTERNAL_PORT}" &
SOCAT_PID=$!

term() {
  kill -TERM "${BACK_PID}" "${SOCAT_PID}" 2>/dev/null || true
}
trap term TERM INT

# Ikkalasidan biri yiqilsa — konteyner ham yiqiladi (orkestrator qayta ko'taradi)
wait -n "${BACK_PID}" "${SOCAT_PID}"
EXIT_CODE=$?
term
wait "${BACK_PID}" "${SOCAT_PID}" 2>/dev/null || true
exit "${EXIT_CODE}"
