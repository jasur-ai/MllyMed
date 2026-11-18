# CP1 — ma'lumot: vendor core + apteka katalogi

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

`built/` ni ma'lumot jihatidan o'z-o'ziga yetarli qilish: yadro JSON'lari,
ikkita dorixona manbasi, provenance va SHA256 manifest.

## Nima qilindi

1. `build.py` `../orindor` dan `agent.py`, `core/`, 9 ta data JSON ni
   `vendor/orindor/` ga ko'chiradi (`VENDORED.md` ogohlantirishi bilan).
2. Ikki manba bitta katalogga birlashtirildi:
   - `workprocess/data/mini_apteka_katalog.json` — 48 yozuv, XPN bor;
   - `workprocess/data/arzon_vitrina.json` — 20 yozuv, XPN **yo'q**.
3. Har yozuvga `source`, `has_inn`, `inn_key`, `local` qo'yildi;
   ArzonApteka uchun `has_inn=false`, `local=null`.
4. `data/build_manifest.json` — har faylning SHA256, o'lchami, yadro
   statistikasi, apteka sonlari.

## Natija

```
core:   46 079 dori · 2 941 XPN · 12 423 referent narx · qamrov 26.6%
apteka: 68 mahsulot · 48 XPN bilan · 20 XPN siz · 25 XPN guruhi
        (15 mahalliy · 27 import · 26 noma'lum)
fayllar: 20 · CHECK OK
```

## Qarorlar

- **Tasdiq:** ikki manbani ajratib saqlash (`source` maydoni) — keyin
  qaysi yozuv qayerdan kelganini bilish uchun.
- **Tasdiq:** ArzonApteka `local=null` — ishlab chiqaruvchi nomidan davlat
  taxmin qilinmaydi.
- **Rad:** ArzonApteka yozuvlariga XPN qo'lda yozish — noto'g'ri
  almashtirish xavfi (README: "almashtirishga yaroqsiz").
- **Rad:** `openFDA` yozuvlarini katalogga qo'shish — AQSh bozori, UZ kartasi
  uchun yaroqsiz.

## Dalil

```bash
cd built && python build.py
# → ✅ CHECK OK; 20 fayl; apteka {'products': 68, ...}
```

## Keyingi qadam

CP2: katalog ustida XPN bog'lash va 80% tekshiruvini yozish.
