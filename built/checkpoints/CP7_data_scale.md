# CP7 — masshtab: 48 → 308 mahsulot

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

Demo uchun 48 mahsulot yetarli emas edi. Katta mahsulotga real katalog
kerak — lekin qonuniy va takrorlanadigan yo'l bilan.

## Qilindi

`pipeline/harvest_apteka.py`:

- 16 kategoriya (antibiotiklar → vitaminlar), har biri `?page=N` bilan;
- ochiq server-render sahifalar; **`/api/` ga tegilmagan** (robots.txt);
- har yozuvda manba URL, yig'ilgan vaqt, XPN, ishlab chiqaruvchi, davlat,
  sotuvchi, narx, dorixonalar soni, kategoriya;
- dedupe `offer id` bo'yicha; sahifa yangi yozuv bermasa — to'xtaydi.

`build.py` endi `data/raw_apteka.json` bo'lsa o'shandan, bo'lmasa eski
48 talik mini katalogdan yig'adi (fallback saqlanadi).

## Natija

```
288 yangi mahsulot · 285 XPN bilan · 158 XPN guruhi · 69 sotuvchi
53 mahalliy · 211 import · 24 kelib chiqishi noma'lum
build: 308 mahsulot (288 + 20 ArzonApteka vitrinasi)
narx bor: 284/285 · 16 kategoriya
```

XPN ↔ reyestr: **95/156 guruh (60.1%)** — `exact 132`, `fuzzy 55`,
`none 92` (mahsulot darajasida).

## Qarorlar

- **Tasdiq:** har kategoriyadan barcha mavjud kartalar (18 tadan), sahifalar
  tugaguncha — "4 tadan" cheklovi olib tashlandi.
- **Tasdiq:** ArzonApteka 20 yozuvi katalogda qoldi, lekin `has_inn=false`.
- **Rad:** `/api/` orqali to'liq katalog — `robots.txt` taqiqlaydi, auth 401.
- **Rad:** sahifa raqami ishlamasa ham cheksiz urinish — yangi yozuv
  bo'lmasa to'xtaydi (takror yuklamaslik uchun).

## Dalil

```bash
cd built && python pipeline/harvest_apteka.py --max-pages 4
# mahsulot 288 · XPN 285 · narx 287 · mahalliy 53 · import 211
cd built && python build.py
# apteka: {'products': 308, 'with_inn': 285, 'without_inn': 23, ...}
```

## Keyingi qadam

CP8: domenni SQLite'ga o'tkazish va rollarni kiritish.
