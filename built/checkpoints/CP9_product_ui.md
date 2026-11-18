# CP9 — katta mahsulot UI + analitika

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

Bitta chat oynasi emas — to'rt rol uchun bitta mahsulot: bemor, shifokor,
dorixona, admin. Har rol faqat o'z ishini ko'radi.

## Analitika (`src/analytics.py`, `/api/analytics`)

| Ko'rsatkich | Qiymat |
|---|---|
| Mahsulot | 308 (285 XPN bilan, 23 siz) |
| XPN guruhi · sotuvchi · kategoriya | 156 · 69 · 16 |
| Narx bor | 284 |
| Mahalliy / import / noma'lum | 53 / 208 / 24 |
| Reyestr bog'lanishi | 95/156 (60.1%) |
| Paritet juftliklari | 14 · 10 tasi «80% dan qimmat» · median farq 0.5% |
| Ma'lumot sifati | narx yo'q 0.4% · XPN yo'q 7.5% · kelib chiqishi noma'lum 8.4% |

`analytics.checks()` — 6 ta ichki izchillik testi (yig'indi, qamrov,
reyestr soni); hammasi `True`.

## API rollar bilan

`X-Role`: `patient | doctor | pharmacist | admin`. Ruxsatlar serverda:

- `POST /api/prescriptions*` → faqat `doctor`;
- `POST /api/prescriptions/dispense` va `GET /queue` → faqat `pharmacist`;
- `GET /api/audit` → faqat `admin`;
- qolganlari `patient`.

## UI (`src/web/static/index.html`)

| Portal | Nima ko'rsatadi |
|---|---|
| Bemor | agent chat, karta, dorixona takliflari, shifokor/vaqt, «mening holatim» |
| Shifokor | navbatlar, XPN tekshirish, qoralama, imzo |
| Dorixona | imzolangan retseptlar navbati, takliflar, «Berish» |
| Admin | metrikalar, paritet jadvali, sifat, audit |

Sarlavhada `DMED: SIMULYATSIYA` doimiy belgi.

## Qarorlar

- **Tasdiq:** analitika ham mahsulot — raqamlar hisoblanadi, yozilmaydi.
- **Tasdiq:** rol tekshiruvi serverda (UI'ga ishonilmaydi).
- **Rad:** alohida 4 HTML fayl — bitta sahifa, rol almashtirish (demo tezligi).
- **Rad:** Chart.js/CDN — 0 tashqi bog'liqlik.

## Dalil

```bash
GET /api/analytics → 200 · 308 mahsulot
GET /api/card?q=ezomeprazol → 200 · ok · DV/M 02386/12/18
UI / → 200
E2E: draft→sign→dispense (403 bemor, 200 farmatsevt), audit 3
```

## Keyingi qadam

CP10 (kelajak): GMP qatlami, qoldiq, autentifikatsiya, 40 stsenariy.
