# CP0 — doira va arxitektura

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

`built/` ichida bitta professional yig'indi: agent (karta + triaj), dorixona
konnektori (arzon_apteka mini + apteka.uz), mini DMED, virtual tajriba va
keyingi AI davom ettira oladigan hujjatlar.

## Kirish sharti (o'qilgan)

- `critic.md` — P0–P3 bandlari; asosiy xavf: yangi iborada favqulodda
  o'tkazib yuborilishi va "bajarilmagan narsani bajarilgandek" ko'rsatish.
- `orindor/AGENT.md` — 10-suite eval, 3 chegara, GMP `UNRESOLVED`.
- `workprocess/tadqiqot/arzon_apteka_tekshiruv.md` — 20 yozuv, XPN yo'q,
  `/api/` taqiqlangan.
- `workprocess/mini_apteka/README.md` — 48 mahsulot, integratsiya shartnomasi.
- `arxiv/*` — DMED bilan raqobat emas, ustiga modul qurish.

## Ko'rib chiqilgan variantlar

| Variant | Qaror | Sabab |
|---|---|---|
| A. Yadro kodini `built/` da qayta yozish | ❌ rad | ikki nusxa, drift, eval bilan uzilish |
| B. `built/` dan `../orindor` ni import qilish | ⚠️ vaqtincha | ishlaydi, lekin papka ko'chirilganda buziladi |
| C. `build.py` bilan yadroni vendorga ko'chirish | ✅ tanlandi | bitta manba + ko'chirsa bo'ladigan papka + SHA256 manifest |
| D. Haqiqiy DMED API integratsiyasi | ❌ rad | ochiq API yo'q, ruxsat yo'q, demo bloklanadi |
| E. DMED ni "raqib" sifatida qurish | ❌ rad | `arxiv/sogliq_treki_due_diligence.md`: parallel EHR = o'lim |
| F. Navbatni agent "band qilishi" | ❌ rad | critic P2: bajarilmagan narsani ko'rsatish |
| G. ArzonApteka `/api/` dan katalog yig'ish | ❌ rad | `robots.txt` taqiqlaydi, 401 auth |

## Tanlangan arxitektura

```
built/
  build.py → vendor/orindor (yadro) + data/apteka_catalog.json + manifest
  src/apteka.py  — katalog va 80% proxy
  src/dmed.py    — sintetik mini DMED, qat'iy ruxsatlar
  src/bridge.py  — agent javobi + yonidagi JSON (matn o'zgarmaydi)
  src/web/       — stdlib API + bir sahifa UI
  sim/           — 12 stsenariy, invariantlar
  tests/         — 12 unit test
```

## Dalil

- `python build.py` → `✅ CHECK OK`, 20 fayl, manifest SHA256.
- `python -m unittest discover -s tests` → 12/12.
- `python sim/run.py` → 12/12.

## Keyingi qadam

CP1: ma'lumot yig'ish va manifestni muzlatish.
