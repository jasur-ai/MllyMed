# CP4 — bridge + veb

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

Agent, dorixona va mini DMED ni bitta foydalanuvchi oqimiga yig'ish; bitta
stdlib server va bitta sahifa bilan ko'rsatish.

## Bridge shartnomasi

`POST /api/chat {sid, text}` →

```json
{
  "reply": "…yadro agentining matni (validatordan o'tgan)…",
  "stage": "card | emergency | routed | age | screening | idle",
  "mode": "card | triage",
  "card": { "reg": "…", "inn": "…", "price": {…}, "group": {…} },
  "apteka": { "count": 4, "offers": […], "check": {…}, "link": {…} },
  "triage": { "specialist": "kardiolog", "urgency": "BUGUN" },
  "dmed": { "doctors": […], "synthetic": true }
}
```

**Muhim:** `reply` o'zgartirilmaydi. Bridge faqat yoniga JSON qo'shadi —
validator natijasi va xavfsizlik matni buzilmaydi.

## API

| Metod | Yo'l | Vazifa |
|---|---|---|
| GET | `/api/health` · `/api/stats` | holat |
| GET | `/api/search?q=` · `/api/apteka/inn/<inn>` | dorixona |
| GET | `/api/dmed/doctors?specialist=` · `/api/dmed/slots?doctor=` | DMED |
| GET | `/api/state?sid=` | navbat/retseptlar |
| POST | `/api/chat` | agent |
| POST | `/api/dmed/book` · `/confirm` · `/cancel` | navbat (user) |
| POST | `/api/dmed/prescribe` · `/sign` | retsept (shifokor sim) |

Xatolar: `ValueError` → 400, `PermissionError` → 403, boshqa → 500.

## UI

Bir sahifa: suhbat (karta + dorixona + shifokorlar), "Dorixona" qidiruvi,
"Mini DMED" va "Retsept" paneli. Sarlavhada ikkita belgi:
`agent: qoidalar + validator` va `DMED: SIMULYATSIYA`.

## Qarorlar

- **Tasdiq:** bridge agent matnini tahrirlamaydi (yagona haqiqat — yadro).
- **Tasdiq:** navbat tugmasi ikki bosqichli: «Tanlash» → «Tasdiqlash».
- **Rad:** chat javobida navbat vaqtini avtomatik taklif qilib "bron" qilish.
- **Rad:** tashqi CDN/freymvork — stdlib + 0 bog'liqlik.

## Dalil

```bash
cd built && python -m src.web.server --port 8211
curl /api/health → {"ok": true, ...}
curl /api/card?q=… → card + apteka
```
(Smoke natijalari `CP6_handoff.md` da.)

## Keyingi qadam

CP5: virtual tajriba.
