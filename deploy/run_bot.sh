#!/bin/bash
# MllyMed Telegram bot — Render FREE web service sifatida ishga tushirish.
# Free worker yo'q, shuning uchun: health HTTP endpoint (0.0.0.0:$PORT, statik)
# + uzoq so'rov bot (fon jarayon emas, ASOSIY jarayon — u yiqilsa konteyner yiqiladi).
# Kod o'zgarmaydi: backend ham, agent ham tegilmagan.
set -euo pipefail

APP_DIR="${APP_DIR:-/app}"
PORT="${PORT:-10000}"

cd "${APP_DIR}"

# Health/status sahifa (Render health check "/" → 200)
python3 -m http.server "${PORT}" --bind 0.0.0.0 --directory deploy/bot_health &
HEALTH_PID=$!
trap 'kill -TERM "${HEALTH_PID}" 2>/dev/null || true' TERM INT

# Bot ASOSIY jarayon: yiqilsa docker konteyneri to'xtaydi → Render avtomatik qayta ko'taradi
exec python3 deploy/telegram_bot.py
