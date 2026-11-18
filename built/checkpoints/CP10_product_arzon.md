# CP10 — bitta sayqallangan mahsulot + Arzon apteka bo'limi

**Sana:** 2026-11-18 · **Holat:** ✅ yopilgan

## Maqsad

`built/` ni bitta tushunarli veb-mahsulotga yig'ish va alohida **Arzon apteka**
bo'limini qo'shish: har XPN uchun eng past taklif, tejamkorlik va vitrina
yozuvlarini bir-biridan aniq ajratib ko'rsatish.

## Nima qilindi

| Qism | O'zgarish |
|---|---|
| `src/apteka.py` | `arzon()` — XPN guruhi bo'yicha eng past taklif, mediana, tejamkorlik %, vitrina ro'yxati, filtrlar |
| `src/bridge.py` | `Bridge.arzon()` — faqat katalogdan hisoblaydi, taxmin qo'shmaydi |
| `src/web/server.py` | `GET /api/arzon?limit=&category=&local=` |
| `src/web/static/index.html` | To'liq yangi interfeys: yorug' tibbiy dizayn, 5 bo'lim (Dorilar, Arzon apteka, Maslahat, Kabinet, Xodimlar) |
| `build.py --check` | O'zgarmadi — vendor core va manifest tegilmagan |

## Raqamlar (o'lchangan)

```
arzon guruhlari        54 (≥2 narxli taklif)
narxli takliflar       284
eng katta farq         −89% (guruh medianasiga nisbatan)
median farq            −24.5%
eng past taklif        2 500 so'm
vitrina yozuvlari      19 (XPN siz, almashtirishga kirmaydi)
```

## Qarorlar

- **A9. Tejamkorlik guruh medianasiga nisbatan hisoblanadi** — «kassa narxi»
  yoki «kafolatlangan tejash» deb nomlanmaydi; izoh UI da ochiq.
- **A10. Vitrina alohida jadvalda** — XPN yo'qligi `badge` bilan ko'rsatiladi,
  `has_inn=false` invariantiga tayanadi.
- **R11. Paket/doza bo'yicha normallashtirish** — hozircha qilinmadi: katalogda
  doza alohida maydon emas, shuning uchun katta foizlar bo'lishi mumkin.
  Keyingi qadam: nomdan doza va paket ajratish.

## Dalil

```bash
cd built
python -m unittest discover -s tests    # 17/17 OK
python sim/run.py                       # 12/12
python build.py --check                 # CHECK OK
python -m src.web.server --port 8200    # 5 bo'lim
```

E2E: `GET /api/arzon` 54 guruh · `local=local&category=Antibiotiklar` → 1 ·
`POST /api/prescriptions` → sign (doctor) → queue (pharmacist) → dispense;
patient roli bilan sign **403**, queue **403**.

## Ochiq

- Vizual tekshiruv brauzerda o'tkazilmadi (bu hostda Chrome yo'q) — faqat
  HTML/JS sintaksisi (`node --check`) va HTTP javoblari tekshirildi.
- ArzonApteka vitrinasida 20 yozuvdan 19 tasida narx bor.

## Qo'shimcha (o'sha kuni): milliy ustuvorlik

- `apteka.by_inn()` va `Bridge.catalog()` mahalliy takliflarni ro'yxat boshiga
  qo'yadi; ichida narx bo'yicha.
- UI kartada «Milliy ustuvorlik: mahalliy muqobillar ro'yxat boshida» izohi,
  eng past narx alohida `badge` bilan (tartib narxni yashirmaydi).
- Bu **tartib**, sifat da'vosi emas: `local=None` taxmin qilinmaydi.
- Tekshiruv: `by_inn("paratsetamol")` → 3 mahalliy, keyin import; 17/17 test,
  12/12 sim, `CHECK OK`.
