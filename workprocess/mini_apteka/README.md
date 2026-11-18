# Mini apteka — O'RINDOR integratsiyasi ko'rgazmasi

**Vazifasi:** O'RINDOR kartasi dorixona oqimida qanday ko'rinishini ko'rsatish.
Sotuvchi emas, **tekshiruvchi**.

```
XPN qidiruvi → shu XPN ostidagi mahalliy/import variantlar → O'RINDOR tekshiruvi
                                                              ├ narx (3735, F09) ✔ hisoblanadi
                                                              ├ reyestr          ✖ ma'lum emas
                                                              └ Asl belgisi      ✖ ma'lum emas
```

## Ishga tushirish

```bash
python3 mini_apteka/server.py        # → http://0.0.0.0:8100
```

API (hammasi `GET`, keyless):

| Yo'l | Nima beradi |
|---|---|
| `/api/stats` | hajm, mahsulot, XPN, mahalliy/import kesimi |
| `/api/search?q=` | nom / XPN / ishlab chiqaruvchi bo'yicha qidiruv **+ o'sha XPN ning boshqa variantlari** |
| `/api/inn/<xpn>` | guruh + O'RINDOR tekshiruvi + dalil (F09, F12) |
| `/api/catalog` | butun katalog (oflayn kesh uchun, 34 KB) |

## Ma'lumot — nima real, nima yo'q

| Maydon | Holat | Manba |
|---|---|---|
| Savdo nomi | ✅ 48/48 | apteka.uz |
| **XPN (INN)** | ✅ 48/48 | apteka.uz (`/uz/products/active-…`) |
| Ishlab chiqaruvchi | ✅ 44/48 | apteka.uz |
| **Davlat (mahalliy/import)** | ✅ 42/48 | kartadagi davlat nomi |
| Narx («X so'mdan») | ✅ 48/48 | apteka.uz |
| Dorixonalar soni | ✅ | «N ta dorixonada bor» |
| ~~Reyestr raqami~~ | ❌ | yopiq |
| ~~Asl belgisi / GTIN~~ | ❌ | yopiq (CRPT Turon) |
| ~~Referent narx~~ | ❌ | yopiq — shuning uchun narx tekshiruvi **proxy** |
| ~~Bioekvivalentlik~~ | ❌ | hech qayerda ochiq emas |

**Tanlov qoidasi:** har kategoriyadan 4 ta, lekin tasodifiy emas — bir XPN ostida
mahalliy va import juftligi bo'lgani birinchi. Sabab: O'RINDOR ning butun ishi shu juftlikda.

Natija: **48 mahsulot · 25 XPN · 8 juftlik · 12 kategoriya · 34 KB**.

## Integratsiya shartnomasi (agent uchun)

O'RINDOR agenti dorixonaga o'tishda shu JSON ni oladi:

```json
{
  "inn": "Ezomeprazol",
  "products": [ { "name": "...", "local": true, "manufacturer": "...",
                  "country": "O'zbekiston", "price_from_som": 56000,
                  "pharmacies": 12, "url": "..." } ],
  "orindor": {
    "narx_tekshiruv": { "holat": "80% dan qimmat", "mahalliy_eng_arzon": 56000,
                        "import_eng_arzon": 65000, "chegara_80": 52000, "farq_foiz": 13.8 },
    "reyestr":     { "holat": "ma'lum emas", "sabab": "..." },
    "asl_belgisi": { "holat": "ma'lum emas", "sabab": "..." },
    "dalil": [ { "id": "F09", "quote": "...", "doc": "3735", "url": "https://lex.uz/..." } ]
  }
}
```

Agent bu javobni **aynan shu shaklda** o'qiydi: `holat` uch xil bo'lishi mumkin —
`mos` · `80% dan qimmat` · `tekshirib bo'lmadi`. «Ma'lum emas» — xato emas,
**mahsulot xususiyati**.

## Halol cheklovlar

1. **Narx tekshiruvi — proxy.** Qonun (3735, F09) *referent narx* haqida: jenerik
   referent narxi originalning 80% idan oshmasligi kerak. Bizda referent narx yo'q,
   shuning uchun chakana narxni olamiz. Bu **ishora**, hukm emas — ilovada ham shunday yozilgan.
2. **Faqat birinchi sahifa.** Har kategoriyadan 18 tadan faqat 4 tasi olinadi (sizning
   talabingiz: ko'p bo'lsa og'ir bo'ladi). Katalog kichik, shuning uchun tez va oflayn.
3. **ArzonApteka vitrinasi 20 ta yozuv — XPN siz.** Ularning bosh sahifasida XPN
   ko'rsatilmaydi, shuning uchun bu yozuvlar almashtirishga yaroqsiz. Ilova buni ochiq aytadi.
4. **`/api/` ga tegmadik.** Ikkala saytning `robots.txt` ida `/api/` taqiqlangan.
   Barcha ma'lumot ochiq, server-render sahifalardan.

## Keyingi qadam

- Rasmiy sheriklik: **+998 71 207-08-08**, **info@fom.group** (`/api/partners/` mavjud).
- Reyestr va Asl belgisi uchun yozma so'rov — bu ikkisi bo'lmasa kartaning yarmi «ma'lum emas».
- Agent bilan ulash: `agent.py` ga `--apteka http://127.0.0.1:8100` rejimi.
