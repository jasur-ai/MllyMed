# MllyMed — Deploy qo'llanmasi (professional runbook)

**Mahsulot:** MllyMed — Milliy dori vositalariga ishonch ekotizimi (Track №17)
**Arxitektura:** bitta Python 3.11 jarayoni — statik frontend + JSON API + O'RINDOR agent.
DB: SQLite (`built/data/runtime/dmed.db`, simulyatsiya). Tashqi servisga bog'liq emas.
**Mahsulot kodi o'zgartirilmagan** — `deploy/` papkasidagi yangi fayllardan tashqari bitta satr ham tegilmagan.

```
foydalanuvchi ──► [nginx / socat] ──► python3 -m backend.server (127.0.0.1:8200/9000)
                                          ├── frontend/      (statik)
                                          ├── /api/*         (B2C/B2B)
                                          ├── built/src/*    (apteka · analytics · dmed·sqlite)
                                          └── orindor/agent  (O'RINDOR agent — triaj + karta)
Telegram ──► deploy/run_bot.sh → /app/bot.py → backend/bot.py ─┘
             (long polling; Mini App tugmasi → https://jasur-ai.github.io/MllyMed/)
```

---

## 0. Sifat darvozasi (deploydan oldin — hammasi yashil ✅)

```bash
python3 run.py --test          # 17/17 invariant + 12/12 stsenariy + 10/10 agent eval
python3 agent/eval.py          # Mustaqil Halol Eval (RED FLAG 32/32, FALSE ALARM 100/100 …)
python3 -m backend.server --port 8200 &
curl -s localhost:8200/api/health   # {"ok": true, ...}
```

Tekshirilgan holat (2026-11-18, Python 3.11.2): **barcha testlar va eval 0 xato bilan o'tdi**,
`/`, `/api/b2c/catalog`, `/api/b2c/card`, `/api/b2c/chat` (triaj + favqulodda/103) — barchasi 200.

---

## 1. Yo'l A — Docker (tavsiya, 20 daqiqa)

Talab: serverda `docker`. Image ichida hamma narsa bor (ma'lumotlar, frontend, agent) — internet shart emas.

```bash
git clone <repo-url> mllymed && cd mllymed
docker build -f deploy/Dockerfile -t mllymed:latest .
docker run -d --name mllymed --restart unless-stopped \
    -p 8200:8200 mllymed:latest

curl -s http://127.0.0.1:8200/api/health        # {"ok": true}
curl -s -X POST http://127.0.0.1:8200/api/b2c/chat \
     -H 'Content-Type: application/json' \
     -d '{"sid":"smoke","text":"Qon qusdim"}'   # ⛔ SHOSHILINCH — 103
docker logs -f mllymed
```

Izoh: backend kodda ataylab `127.0.0.1` ga bog'langan. Konteynerda `socat`
`0.0.0.0:8200` → `127.0.0.1:9000` ni yo'naltiradi (kodga tegilmadi). Healthcheck
`/api/health` ni har 30s da tekshiradi; yiqilsa `--restart unless-stopped` ko'taradi.

Resurs: **512 MB RAM** yetadi (ma'lumotlar yuklangach ~300 MB), 1 vCPU, ~250 MB disk.

---

## 2. Yo'l B — Dockersiz (VPS + systemd + nginx)

```bash
sudo useradd -r -s /usr/sbin/nologin mllymed
sudo mkdir -p /opt/mllymed && sudo chown mllymed:mllymed /opt/mllymed
sudo -u mllymed git clone <repo-url> /opt/mllymed

sudo cp /opt/mllymed/deploy/systemd/mllymed.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now mllymed

sudo cp /opt/mllymed/deploy/nginx.conf /etc/nginx/sites-available/mllymed
# nginx.conf ichida server_name ni domeningizga almashtiring
sudo ln -sf /etc/nginx/sites-available/mllymed /etc/nginx/sites-enabled/
sudo certbot --nginx -d mllymed.uz                       # bepul TLS
sudo nginx -t && sudo systemctl reload nginx
```

---

## 3. Cloudflare — siz bergan tokenlar bilan (muhim, o'qing)

**Aniq haqiqat:** bu muhitdan (sandbox) `api.cloudflare.com`, `*.r2.cloudflarestorage.com`
va `api.telegram.org` **tarmoq darajasida yopiq** (ulanish rad etiladi). Shuning uchun
deploy'ning o'zi shu mashinadan bajarilmadi — quyidagi qadamlarni istalgan
internetli mashinada (serveringiz, noutbukingiz) 5 daqiqada bajarasiz. Tokenlar
chatda oshkor bo'lgani uchun **rotsiya qilishni tavsiya qilamiz** (§6).

### 3.1 Tavsiya: VPS + Cloudflare CDN/WAF/TLS (eng ishonchli)
Backend statik emas (Python + SQLite) — Cloudflare **Pages** uni ishga sola
olmaydi. To'g'ri sxema: app VPS'da (Yo'l A yoki B), Cloudflare oldida:

1. Cloudflare Dashboard → DNS → `A` yozuvi: `mllymed.uz` → VPS IP, **Proxied** (to'q sariq bulut)
2. SSL/TLS → mode: **Full (strict)**; Edge Certificates → «Always Use HTTPS» **ON**
3. Security → WAF → Managed rules **ON**; `/api/*` ga rate-limit (10 r/s, nginx bilan juft)
4. Tekshirish: `curl -s https://mllymed.uz/api/health`

### 3.2 Cloudflare Containers (Workers Paid, beta) — «Cloudflare'da to'liq»
`deploy/Dockerfile` to'g'ridan-to'g'ri ishlaydi (Python 3.11 + ma'lumotlar image ichida).
Talab: Workers **Paid** reja ($5/oy). Mashinada:

```bash
npm i -g wrangler && wrangler login     # yoki CLOUDFLARE_API_TOKEN=… wrangler …
# wrangler.toml (containers) — Cloudflare docs dagi joriy sintaksis bilan:
#   [containers]  image = "./deploy/Dockerfile",  va HTTPS Worker (fetch → container)
wrangler deploy
```
Batafsil: https://developers.cloudflare.com/containers/ (sintaksis beta'da o'zgarib turadi — docs dagi joriy namuna bo'yicha `wrangler.toml` yoziladi).

### 3.3 R2 — ma'lumot zaxirasi (backup)
46 079 dori regyestri va INN/referent narxlarini off-site saqlang:

```bash
# aws-cli yoki rclone bilan, S3-mos endpoint:
aws s3 sync ./data s3://mllymed-backup/data \
  --endpoint-url https://<ACCOUNT_ID>.r2.cloudflarestorage.com   # ACCOUNT_ID — Cloudflare dashboard → R2
# wrangler bilan bucket yaratish:
npx wrangler r2 bucket create mllymed-backup
```
(R2'dagi fayllarni ilova o'qimaydi — ilova lokal fayllarni o'qiydi; R2 = zaxira.)

### 3.4 ❌ Qilmang: «faqat statikni Pages'ga yuklash»
API o'chadi (katalog qidiruv, karta, chat, DMED — hammasi 404/501). Yarim-yalay deploy
professional emas.

---

## 4. Telegram bot — @MllyMed_bot (develop'dagi to'liq bot)

Bot **repo ichida allaqachon bor**: `bot.py` → `backend/bot.py` — long polling,
reply/inline keyboard, Mini App ochish tugmasi (`WEBAPP_URL`, default
`https://jasur-ai.github.io/MllyMed/` — gh-pages), agent bilan to'g'ridan-to'g'ri
suhbat (`/api/b2c/chat` emas, bevosita `Agent.respond`). Deploy'da `run_bot.sh`
uni foreground'da ko'taradi + `/` ga health sahifa beradi (Render free health check).

**Tuzatilgan kamchiliklar** (develop'da bor edi):
- `Session(f"tg_{chat_id}")` → `Session()` — Session'ning birinchi pozitsiyali
  argumenti `mode=` edi: "tg_*" mode sifatida o'rnatilib, agent intent tanlashni
  PYTHONATLAB O'TKAZIB YUBORARDI → **dori kartalari hech qachon chiqmasdi**.
- `TELEGRAM_BOT_TOKEN` uchun kodda **hardcoded default** bor edi (public repo!) —
  olib tashlandi; endi faqat muhit o'zgaruvchisi, aks holda bot aniq xato bilan chiqadi.
- `requests` imajga qo'shildi (`deploy/Dockerfile`), aks holda bot ImportError bilan yiqilardi.

**TOKENNI ALBATTA ROTATSIYA QILING** — eski token public repo'da ochiq qolgan:
t.me/BotFather → `/revoke` → yangi token. Keyin uni faqat Render dashboard'ga /
`deploy/.env` ga yozing (hech qachon commitga).

```bash
# Lokal sinov (toza muhit):
pip install "requests>=2.31,<3"
export TELEGRAM_BOT_TOKEN="<yangi token>"
python3 bot.py                        # «MllyMed Telegram Bot faol!»
# Telegram → t.me/MllyMed_bot → /start → «paratsetamol» → karta ✅
```

Render'da ikkinchi servis sifatida ishlaydi: dockerCommand `bash /app/deploy/run_bot.sh`
(health `/` + `python3 bot.py`), env: `TELEGRAM_BOT_TOKEN`. Bitta poller ishlasin —
ikkita jarayon bir token bilan `getUpdates` qilsa xabarlar bo'linadi (409 Conflict).

systemd orqali: `deploy/systemd/mllymed-bot.service` (ExecStart=`python3 bot.py`,
EnvironmentFile bilan). `deploy/.env` ichida `TELEGRAM_BOT_TOKEN=…`.

BotFather sozlamalari (bir marta, t.me/BotFather):
- `/setdescription` — «Milliy dori vositalari reyestri: dori kartasi, narx, INN analog,
  xavfsiz yo'naltirish. Tashxis yo'q, maslahat yo'q — ma'lumot va 103.»
- `/setabouttext` — «O'zbekiston dori vositalari reyestri asosidagi rasmiy-ma'lumot boti.»
- `/setuserpic` — `frontend/shared/assets/logo.svg` dan eksport qilingan PNG
- `/setcommands` — `start — Boshlash`, `help — Yordam`, `reset — Suhbatni tozalash`

## 5. Tekshiruv ro'yxati (go-live checklist)

- [ ] `python3 run.py --test` — yashil
- [ ] `curl .../api/health` — `{"ok": true}`
- [ ] `/` brauzerda ochiladi, katalog qidiruv ishlaydi («para» → 15 ta natija)
- [ ] Chat: «Qon qusdim» → ⛔ 103; «ko'kragim og'riyapti» → majburiy savol; «nurofen» → karta
- [ ] `docker ps` / `systemctl status mllymed` — `active (running)`
- [ ] TLS (https) — yashil qulf, `curl -I` da 301→200
- [ ] Telegram: `/start` → salom+tugmalar; «paratsetamol» → **karta**; «ko'kragim qattiq og'riyapti» → ⛔ 103; Mini App tugmasi ochiladi
- [ ] Monitoring: UptimeRobot/Healthchecks.io → `https://domen/api/health` har 5 daqiqa
- [ ] Zaxira: `built/data/runtime/dmed.db` (sqlite) kunlik nusxa; `data/` R2 ga (§3.3)
- [ ] Loglar: `docker logs` / `journalctl -u mllymed -f` — xatosiz

Rollback: `docker rm -f mllymed && docker run … mllymed:previous` yoki
`git checkout <oldingi-commit>` + qayta build. Runtime holat faqat `built/data/runtime/`
da — zaxiradan tiklanadi.

---

## 6. Xavfsizlik

1. **Tokenni rotsiya qiling** — Telegram tokeni va Cloudflare API tokeni
   maxfiy chatda oshkor bo'ldi. BotFather → `/revoke`; Cloudflare → API Tokens → Roll.
   R2 kalitlari uchun ham yangi juft yarating. (`deploy/.env` — gitignore'da; commit qilinmaydi.)
2. **API'da autentifikatsiya yo'q** — `X-Role`/`X-User` sarlavhalari faqat *simulyatsiya*
   (demo rollar), haqiqiy himoya emas. Ilovani ochiq internetga qo'yishdan oldin:
   nginx darajasida rate-limit (§2) + basic-auth yoki Cloudflare Access (Zero Trust,
   bepul 50 foydalanuvchigacha) bilan yoping. §2 dagi `limit_req` allaqachon bor.
3. **SQLite** bitta jarayonli; yozish `timeout=10` bilan. Yuqori yuklamada
   `built/data/runtime/` ni tmpfs emas, oddiy disk ustida saqlang.
4. Ma'lumotlar ochiq davlat regyestridan (api.mpa.uz) — PII yo'q. Baribir
   `.env`, loglar va chat_id'lar gitga tushmasin.
5. Healthcheck va xatolar `/api/health` ga ichki tafsilot oshkor qilmaydi — to'g'ri.

---

## 7. Ma'lum cheklovlar (yashirilmaydi)

- Agent eval 100% (32/32, 100/100, …), lekin klinik ko'rikdan o'tmagan — **tibbiy maslahat emas**.
- DMED (navbat, shifokor, retsept) — **simulyatsiya**; haqiqiy DMED API ga ulanmagan.
- Eslatmalar — push emas; ilova ochiq bo'lganda ko'rsatiladi.
- GMP reyestri holati: UNRESOLVED (`uzpharm-gxp.uz/registry2` ochiq, lekin tekshirilmagan).
- Narx qamrovi karta evalda 26.6% — «ma'lum emas» deb ko'rsatiladi, taxmin qilinmaydi.
- Bitta ishchi jarayoni; horizontal scale uchun SQLite → Postgres kerak bo'ladi.

## 8. Muammolar

| Belgilari | Yechim |
|---|---|
| `permission denied` (runtime) | `chown -R mllymed:mllymed built/data/runtime orindor/data/runtime` |
| 502 nginx | `systemctl status mllymed`; `journalctl -u mllymed -n 100` |
| Health FAIL | `docker ps`; xotira yetarli emasligini `dmesg` da tekshiring |
| Bot javob bermayapti | `systemctl status mllymed-bot`; token rotatsiyadan keyin yangilanganini tekshiring; `python3 bot.py` lokal ishga tushirib ko'ring; poller bittami? |
| Port band | `PUBLIC_PORT=8080` (env) yoki `docker run -p 8080:8200` |
