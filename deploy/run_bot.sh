#!/bin/bash
# MllyMed Telegram bot — Render FREE web service sifatida ishga tushirish.
# Botning o'zi: /app/bot.py → backend/bot.py (Mini App + reply/inline keyboard + agent).
# Free worker yo'q, shuning uchun: health HTTP endpoint (0.0.0.0:$PORT, statik)
# + long polling ASOSIY jarayon sifatida (u yiqilsa konteyner yiqiladi → Render qayta ko'taradi).
# Kod o'zgarmaydi: backend ham, agent ham tegilmagan (faqat xavfsizlik tuzatlari backend/bot.py da).
set -euo pipefail

APP_DIR="${APP_DIR:-/app}"
PORT="${PORT:-10000}"

cd "${APP_DIR}"

# Health/status sahifa (Render health check "/" → 200)
python3 -m http.server "${PORT}" --bind 0.0.0.0 --directory deploy/bot_health &
HEALTH_PID=$!
trap 'kill -TERM "${HEALTH_PID}" 2>/dev/null || true' TERM INT

# Bot ASOSIY jarayon
exec python3 "${APP_DIR}/bot.py"
