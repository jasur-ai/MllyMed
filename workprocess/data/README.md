# DATA — O'RINDOR ma'lumot bo'limi

Hamma yig'ilgan ma'lumot **shu yerda**, ishlatsa bo'ladigan ko'rinishda.
Manba: ochiq davlat API'lari + ochiq dorixona saytlari. Sana: **2026-11-18**.

```
json  — ilova uchun (to'g'ridan-to'g'ri o'qiladi)
csv   — Excel / Google Sheets uchun
xlsx  — rasmiy nusxa (qo'lda ko'rish uchun)
```

---

## 1. Fayllar

| Fayl | Yozuv | Hajm | Nima |
|---|---|---|---|
| **`reyestr_dori.json`** | **46 079** | 25 MB | davlat dori reyestri — to'liq |
| `reyestr_dori.xlsx` | 40 000 | 2.7 MB | o'sha reyestr, rasmiy Excel |
| **`referent_narx.json`** | **12 612** | 5.0 MB | 3735 bo'yicha chegaraviy narxlar |
| `referent_narx.csv` | 12 612 | 2.7 MB | o'sha, jadval |
| `tafsilot.json` | 538 | 441 KB | chegara narx (`maxSalePrice`) + tarkib |
| `tafsilot.csv` | 538 | 191 KB | o'sha, jadval |
| `mini_apteka_katalog.json` | 48 | 18 KB | 12 kategoriya × 4, mahalliy+import juftligi |
| `arzon_vitrina.json` | 20 | 4.6 KB | ArzonApteka bosh sahifasi |
| `atx_guruhlari.json` | 15 | 5.8 KB | ATX guruhlari + dori soni |
| `dori_shakllari.json` | 104 | 3.2 KB | dori shakllari ro'yxati |
| `faktlar.json` | 17 | 9.5 KB | lex.uz dan tekshirilgan huquqiy faktlar |
| `hisob.json` | — | 46 B | 46 079 dori · 400 tibbiyot tashkiloti |
| `index.json` | — | 2.8 KB | manifest: har fayl, manba, sana, hajm |

Jami: **~36 MB**. `index.json` — mashina o'qiydigan manifest.

---

## 2. `reyestr_dori.json` — asosiy jadval

```json
{
  "drugId": 1010000,
  "shortName": "АНЗИБЕЛ®",
  "fullName": "АNZIBEL® sprey 0,2 % 30ml flakonlar",
  "mnn": "xlorgeksidin",                  ← XPN (INN) — kirill yoki lotin
  "dosageForm": "спрей",
  "strength": "30 миллилитр",
  "country": "Узбекистан",
  "manufacturer": "ИП ООО NOBEL PHARMSANOAT MCHJ Узбекистан",
  "registrationCode": "DV/M 04121/05/22",  ← reyestr raqami (100% to'ldirilgan)
  "local": true,                           ← rasmiy bayroq: mahalliy/import
  "atxCode": "A01AD",
  "icps": "03004999025001005",             ← soliq/bojxona kodi
  "tnved": "3004900002",                   ← bojxona kodi
  "dispensingConditions": "Retseptsiz",
  "prescriptionRequired": false
}
```

Taqsimot: **27 620 mahalliy · 18 459 import · 2 958 XPN turi**.

---

## 3. `referent_narx.json` — narx chegarasi

```json
{
  "drugId": 1570451,
  "trademark": "5-ФТОРУРАЦИЛ-ЭБЕВЕ",
  "innName": "фторурацил",
  "manufacturer": "GmbH Fareva Unterach GmbH Австрия",
  "registrationNumber": "DV/X 03682/11/17",
  "price": 91467.43,
  "wholesalePrice": 105187.54,   ← ulgurji
  "retailPrice": 126225.05,      ← chakana (so'm)
  "basePrice": 6.57,             ← bazaviy (valyutada)
  "currency": "dollar",
  "vatEnabled": "с НДС",
  "prescription": "По рецепту",
  "uploadedAt": "2026-11-16"
}
```

---

## 4. `tafsilot.json` — eng muhim yangi maydon

```json
{
  "id": 1010000,
  "maxSalePrice": 6.57,          ← ★ QONUNIY CHEGARA NARX (asl valyutada)
  "currency": "Доллар США",
  "retailPrice": 126225.05,      ← so'mdagi chakana
  "priceDate": "2026-11-16",
  "substanceNames": ["поливинилпирролидон", "глицерин", "..."],  ← tarkib
  "imgCount": 5                  ← qadoq rasmlari soni
}
```

**Diqqat:** `maxSalePrice` — 3735-son qaror bo'yicha ruxsat etilgan chegara.
Asl valyutada berilgan; so'mga o'girish kursi (hisoblangan): **19 267 so'm/USD**
(`retailPrice / maxSalePrice` medianasi). Valyuta: USD 216 · so'm 269 · yevro 30 · rubl 5.

---

## 5. Qanday ishlatish

```python
import json

reyestr = json.load(open("data/reyestr_dori.json", encoding="utf-8"))

# 1) XPN bo'yicha barcha variantlar (almashtirish guruhi)
guruh = [d for d in reyestr if d["mnn"] == "flukonazol"]
print(len(guruh), "ta variant;", sum(d["local"] for d in guruh), "tasi mahalliy")

# 2) import ulushi
import_ = sum(1 for d in reyestr if d["local"] is False)
print(f"import: {100*import_/len(reyestr):.0f}%")
```

```javascript
// Node / brauzer
const reyestr = await (await fetch('data/reyestr_dori.json')).json();
const guruh = reyestr.filter(d => d.mnn === 'flukonazol');
```

⚠️ **25 MB** faylni telefon ilovasiga to'liq yuklash og'ir. Amaliy yo'l:
kerakli XPN larni oldindan tanlab, kichik indeks yasash (masalan 200 eng ko'p
yoziladigan XPN) — `mini_apteka_katalog.json` shunday qilingan, 18 KB.

---

## 6. Nima YO'Q (va nega)

| Maydon | Holat | Sabab |
|---|---|---|
| GTIN / shtrix-kod | ❌ | Excel da yo'q, qadoq rasmlarida yo'q, API'da yo'q |
| Asl Belgisi kod tekshiruvi | ❌ | `xtrace.aslbelgisi.uz` → 401, to'liq auth |
| GMP / GDP / GPP sertifikatlari | ❌ | `api.mpa.uz/.../gmp-registry` → 401, E-IMZO kerak |
| Bioekvivalentlik hisoboti | ❌ | ochiq manbada yo'q, faqat yozma so'rov |
| Dorixona qoldig'i (real vaqt) | ❌ | `arzonapteka.uz` API yopiq (`/api/partners/` rasmiy yo'l) |
| Dori yo'riqnomasi | ❌ | `instruction/detail` → 401 |

Bu ro'yxat **reliz uchun to'siq emas**: `tafsilot.maxSalePrice` va
`reyestr.registrationCode` borligi kartani to'liq ishlatishga yetadi.
"Ma'lum emas" — mahsulotning xususiyati, xato emas.

---

## 7. Qayta yig'ish

```bash
python3 orindor/tools/harvest_mpa.py         # reyestr + referent narx (60 so'rov, ~3 daq)
python3 orindor/tools/harvest_mpa_extra.py   # tafsilot + Excel + ATX (davom etadigan)
python3 orindor/tools/build_data.py          # hammasini data/ ga yig'ish
```

Xom yig'ish `orindor/data/uz_registry/` ga tushadi (staging), `build_data.py`
uni `data/` dagi toza JSON/CSV ga aylantiradi.
