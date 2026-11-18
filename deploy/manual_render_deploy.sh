#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# MllyMed — Render.com'ga bir buyruqda deploy (internetli istalgan mashinada).
# GitHub Actions ishlamasa yoki secret qo'shish imkoni bo'lmasa — shu skriptni ishga
# tushiring. HECH QANDAY token kodda emas — hammasi muhit o'zgaruvchilaridan olinadi.
#
#   export RENDER_API_KEY="rnd_..."            # Render → Account Settings → API Keys
#   export TELEGRAM_BOT_TOKEN="123:AA..."      # BotFather (bot uchun)
#   export CF_API_TOKEN="cfat_..."             # Cloudflare API token (R2 backup uchun, ixtiyoriy)
#   export CF_ACCOUNT_ID="..."                 # Cloudflare Account ID (ixtiyoriy)
#   export R2_ACCESS_KEY_ID="..."              # R2 kaliti (ixtiyoriy)
#   export R2_SECRET_ACCESS_KEY="..."          # R2 siri (ixtiyoriy)
#   ./deploy/manual_render_deploy.sh
#
# Talab: bash, curl, jq. (aws-cli faqat R2 backup uchun.)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/jasur-ai/MllyMed}"
BRANCH="${BRANCH:-arena/bbba9f48-mllymed}"
REGION="${REGION:-frankfurt}"
WEB_NAME="${WEB_NAME:-mllymed}"
BOT_NAME="${BOT_NAME:-mllymed-bot}"
API="https://api.render.com/v1"

die() { echo "❌ $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null || die "$1 topilmadi — o'rnating (apt install $1)"; }
need curl; need jq
[ -n "${RENDER_API_KEY:-}" ] || die "RENDER_API_KEY muhit o'zgaruvchisi berilmagan"

rq() {  # rq METHOD PATH [JSON]
  local method="$1" path="$2" data="${3:-}"
  if [ -n "$data" ]; then
    curl -sS -X "$method" -H "Authorization: Bearer $RENDER_API_KEY" \
         -H 'Content-Type: application/json' -d "$data" "$API$path"
  else
    curl -sS -X "$method" -H "Authorization: Bearer $RENDER_API_KEY" "$API$path"
  fi
}

echo "▶ 1/6 Render workspace aniqlanmoqda…"
OID=$(rq GET "/owners?limit=5" | jq -r '.[0].owner.id // .[0].id // empty')
[ -n "$OID" ] || die "ownerId olinmadi — token yaroqlimi?"
echo "   owner: $OID"

find_service() { rq GET "/services?name=$1&limit=20" | jq -r '[.[].service | select(.name=="'"$1"'")][0].id // empty'; }
service_url() { rq GET "/services/$1" | jq -r '.service.serviceDetails.url // .serviceDetails.url // empty'; }

echo "▶ 2/6 Web servis: $WEB_NAME (docker · free · $REGION)…"
SID=$(find_service "$WEB_NAME")
if [ -z "$SID" ]; then
  P=$(jq -nc --arg o "$OID" --arg r "$REPO_URL" --arg b "$BRANCH" --arg n "$WEB_NAME" --arg reg "$REGION" '
    {type:"web_service", name:$n, ownerId:$o, repo:$r, branch:$b, autoDeploy:"yes",
     serviceDetails:{runtime:"docker", plan:"free", region:$reg,
       envSpecificDetails:{dockerfilePath:"./deploy/Dockerfile", dockerContext:"."}}}')
  RESP=$(rq POST "/services" "$P")
  SID=$(echo "$RESP" | jq -r '.service.id // .id // empty')
  [ -n "$SID" ] || die "web servis yaratilmadi: $(echo "$RESP" | head -c 300)"
  echo "   yaratildi: $SID (autoDeploy=yes — ilk deploy boshlandi)"
else
  echo "   mavjud: $SID — deploy trigger…"
  rq POST "/services/$SID/deploys" '{}' | jq -c '{deploy:(.deploy.id // .id), status:(.deploy.status // .status // "triggered")}'
fi
WEB_URL=$(service_url "$SID"); [ -z "$WEB_URL" ] && WEB_URL="https://$WEB_NAME.onrender.com"
echo "   URL: $WEB_URL"

echo "▶ 3/6 Telegram bot servis: $BOT_NAME (free · health + long polling)…"
if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "   ⚠️  TELEGRAM_BOT_TOKEN berilmagan — bot servisi O'TKAZILIB YUBORILDI"
  BOT_URL="(yaratilmadi)"
else
  BID=$(find_service "$BOT_NAME")
  if [ -z "$BID" ]; then
    P=$(jq -nc --arg o "$OID" --arg r "$REPO_URL" --arg b "$BRANCH" --arg n "$BOT_NAME" --arg reg "$REGION" '
      {type:"web_service", name:$n, ownerId:$o, repo:$r, branch:$b, autoDeploy:"no",
       serviceDetails:{runtime:"docker", plan:"free", region:$reg,
         envSpecificDetails:{dockerfilePath:"./deploy/Dockerfile", dockerContext:".",
                             dockerCommand:"bash /app/deploy/run_bot.sh"}}}')
    RESP=$(rq POST "/services" "$P")
    BID=$(echo "$RESP" | jq -r '.service.id // .id // empty')
    [ -n "$BID" ] || die "bot servisi yaratilmadi: $(echo "$RESP" | head -c 300)"
    echo "   yaratildi: $BID"
  else
    echo "   mavjud: $BID"
  fi
  ENV_P=$(jq -nc --arg t "$TELEGRAM_BOT_TOKEN" --arg u "$WEB_URL" \
    '[{key:"TELEGRAM_BOT_TOKEN", value:$t}, {key:"MLLYMED_API", value:$u}]')
  CODE=$(curl -sS -o /dev/null -w '%{http_code}' -X PUT -H "Authorization: Bearer $RENDER_API_KEY" \
         -H 'Content-Type: application/json' -d "$ENV_P" "$API/services/$BID/env-vars")
  [ "$CODE" -lt 300 ] || die "env-vars o‘rnatilmadi (HTTP $CODE)"
  echo "   env varlar o‘rnatildi (token logga chiqarilmadi)"
  rq POST "/services/$BID/deploys" '{}' | jq -c '{deploy:(.deploy.id // .id), status:(.deploy.status // .status // "triggered")}'
  BOT_URL=$(service_url "$BID"); [ -z "$BOT_URL" ] && BOT_URL="https://mllymed-bot.onrender.com"
  echo "   URL: $BOT_URL"
fi

echo "▶ 4/6 Web servis jonli bo'lguncha kutilmoqda (build ~3–8 daqiqa)…"
ok=0
for i in $(seq 1 48); do
  code=$(curl -s -o /dev/null -w '%{http_code}' "$WEB_URL/api/health" || true)
  printf '\r   urinish %d/48: HTTP %s   ' "$i" "$code"
  [ "$code" = "200" ] && { ok=1; echo; break; }
  sleep 15
done
[ "$ok" = "1" ] || die "web servis 12 daqiqada ko‘tarilmadi — Render → Logs"
echo "   ✅ $WEB_URL/api/health → 200"

echo "▶ 5/6 Smoke test…"
curl -sS -o /dev/null -w '   GET /           → %{http_code}\n' "$WEB_URL/"
BODY=$(curl -sS -X POST "$WEB_URL/api/b2c/chat" -H 'Content-Type: application/json' \
             -d '{"sid":"manual-smoke","text":"Qon qusdim"}')
echo "   chat(emergency) → $(echo "$BODY" | jq -r '.reply' | head -1)"
echo "$BODY" | jq -e '.reply | contains("103")' >/dev/null && echo "   ✅ favqulodda yo‘l (103) ishlayapti"

if [ -n "${R2_ACCESS_KEY_ID:-}" ] && [ -n "${R2_SECRET_ACCESS_KEY:-}" ] && [ -n "${CF_API_TOKEN:-}" ] && [ -n "${CF_ACCOUNT_ID:-}" ]; then
  echo "▶ 6/6 R2 backup (data/ → mllymed-backup)…"
  curl -sS -o /dev/null -w '   bucket create HTTP %{http_code} (mavjud bo‘lsa — muammo emas)\n' \
       -X POST -H "Authorization: Bearer $CF_API_TOKEN" -H 'Content-Type: application/json' \
       -d '{"name":"mllymed-backup"}' "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT_ID/r2/buckets"
  if command -v aws >/dev/null; then
    EP="https://$CF_ACCOUNT_ID.r2.cloudflarestorage.com"
    AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID" AWS_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY" AWS_DEFAULT_REGION=auto \
      aws s3 sync ./data "s3://mllymed-backup/data" --endpoint-url "$EP" --only-show-errors
    AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID" AWS_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY" AWS_DEFAULT_REGION=auto \
      aws s3 sync ./orindor/data "s3://mllymed-backup/orindor-data" --endpoint-url "$EP" --only-show-errors
    echo "   ✅ R2 backup tugadi"
  else
    echo "   ⚠️  aws-cli yo‘q — backup o‘tkazib yuborildi (pip install awscli)"
  fi
else
  echo "▶ 6/6 R2 (ixtiyoriy) — kalitlar berilmagani uchun o‘tkazib yuborildi"
fi

echo
echo "═══════════════════════════════════════════════"
echo "✅ Web:      $WEB_URL"
echo "✅ Health:   $WEB_URL/api/health"
echo "✅ Bot:      https://t.me/MllyMed_bot  ($BOT_URL)"
echo "   (Botga /start yozing — javob berishi kerak)"
echo "═══════════════════════════════════════════════"
