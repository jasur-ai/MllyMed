# Davlat reyestri va referent narxlar — TOPILDI

**Sana:** 2026-11-18 · **Holat:** ✅ uchta "yopiq" maydon aslida **ochiq**

---

## 1. Nima topildi

Butun davlat dori tizimining API'si — **`api.mpa.uz/drug-catalog-api/`** — autentifikatsiyasiz ishlaydi.
Manba: `pharm.gov.uz` ("Medpharm portal", Tarmoqni rivojlantirish agentligi) sahifasining
ochiq JavaScript fayli.

| Endpoint | Nima beradi | Hajm |
|---|---|---|
| `GET /v2/drugs/portal/search?search=&page=&size=` | **davlat reyestri** | **46 079 dori** |
| `GET /v1/referent-price/all?page=&size=` | **referent narxlar** | **12 612 yozuv** |
| `/v1/referent-price/excel` | narxlar Excel | tekshirilmagan |
| `/v1/drugs/download-excel` | reyestr Excel | 500 xato (parametr kerak) |
| `/v1/gmp-registry` · `gdp` · `gpp` · `gcp` · `glp` · `gsp` | GMP/GDP/GPP sertifikat registrlari | tekshirilmagan |
| `/v1/foreign-drug-gmp-registry` | xorijiy GMP | tekshirilmagan |

---

## 2. Yig'ilgan ma'lumot (workspace'da)

```
orindor/data/uz_registry/
  drugs.jsonl       46 079 yozuv · 26 MB
  referent.jsonl    12 612 yozuv · 5.3 MB
  join_sample.json     25 guruh (mini apteka XPN lari bo'yicha bog'langan)
  meta.json            yig'ilgan vaqt + sahifa holati
```

Qayta yig'ish: `python3 orindor/tools/harvest_mpa.py` (60 so'rov, ~3 daqiqa, davom etadigan).

### Reyestr maydonlari (har birida 100%)
```
drugId · shortName · fullName · mnn (XPN) · dosageForm · strength ·
country · manufacturer · registrationCode · local (rasmiy bayroq) ·
atxCode · icps · tnved · dispensingConditions · prescriptionRequired
```

### Referent narx maydonlari
```
trademark · innName · manufacturer · registrationNumber ·
price · wholesalePrice · retailPrice · basePrice · currency ·
vatEnabled · prescription · uploadedAt
```

---

## 3. Bu nima o'zgartirdi

Oldin "yopiq, yozma so'rov kerak" deb hisoblangan maydonlar:

| Maydon | Oldin | Endi |
|---|---|---|
| Reyestr raqami | ❌ yopiq | ✅ **46 079 / 46 079 (100%)** |
| XPN (INN) | ❌ faqat qidiruvda | ✅ **2 958 tur** |
| Mahalliy / import | ⚠️ taxmin (nom bo'yicha) | ✅ **rasmiy bayroq**: 27 620 mahalliy · 18 459 import |
| Referent narx (3735) | ❌ yopiq → proxy ishlatilgan | ✅ **12 612 yozuv**, chakana + ulgurji |
| ATX kodi | ❌ | ✅ |
| TNVED (bojxona) kodi | ❌ | ✅ |
| Bioekvivalentlik (BE) | ❌ | ❌ hali ham yo'q |
| GTIN / Asl belgisi | ❌ | ❌ hali ham yo'q (faqat ilova orqali skan) |
| Dorixona qoldig'i | ❌ | ❌ (faqat `arzonapteka` / `apteka.uz` ko'rsatadi) |

---

## 4. Kutilmagan topilma — bu №17 ni qayta o'qiydi

Referent narxlar bo'yicha **344 ta XPN** da bir vaqtda mahalliy ham, import ham bor.
Har biri uchun eng arzon mahalliy va eng arzon import narxi solishtirildi
(doza bo'yicha guruhlangan, paket birligiga keltirilgan):

```
mahalliy / import birlik narxi nisbati — mediana  1.10
  mahalliy arzonroq (≤1.0)         162 / 344   (47%)
  mahalliy 80% qoidasida (≤0.8)    122 / 344   (35%)
  mahalliy 2 baravar qimmat (>2)    92 / 344   (27%)
```

**Ya'ni:** har ikkinchi holatda eng arzon mahalliy dori importdan **qimmat**.
Qonundagi 80% qoidasi (F09) mavjud, lekin referent narxlarda u **ko'p hollarda bajarilmagan**.

Eng katta farqlar (tekshirish kerak — birlik hisobi evristik):

| XPN | nisbat | mahalliy | import |
|---|---|---|---|
| стрептомицин | 19.8× | 55 200 | 2 783 |
| домперидон | 17.6× | 77 280 | 4 386 |
| орнидазол | 13.4× | 40 186 | 3 005 |
| амоксициллин + клавулановая | 12.9× | 37 871 | 2 927 |

**Diqqat:** bu raqamlar **referent narx reyestridan**, ya'ni rasmiy. Lekin paket birligiga
keltirish evristik (N10/N30 ni matndan o'qish) — ba'zi qatorlar qo'lda tekshirilishi shart.

**Nima uchun bu muhim:** "mahalliy = arzon" degan taxmin ma'lumotda **tasdiqlanmadi**.
Demak O'RINDOR ning ishi targ'ibot emas, **aniq ko'rsatish**: qaysi mahalliy dori haqiqatan
arzon, qaysi biri emas. Bu mahsulotning eng kuchli tomoni bo'lishi mumkin — raqobatchilarda
bunday qatlam yo'q.

---

## 5. Hali yopiq (va nima qilish kerak)

| Nima | Holat | Yo'l |
|---|---|---|
| Bioekvivalentlik (BE) hisobotlari | ❌ | yozma so'rov — Markazda bor, ochiq emas |
| GTIN / Asl belgisi kodlari | ❌ | `xtrace.aslbelgisi.uz` faqat a'zolar uchun; `abelgi.uz` — tijoriy |
| Dorixona qoldig'i va real narx | ❌ | `arzonapteka.uz` (`/api/partners/`) · `apteka.uz` |
| Referent narx Excel | ⚠️ | `referent-price/excel` — parametrlari aniqlanmagan |

---

## 6. Texnik eslatmalar

- **XPN tili:** reyestr va referent narxlar **kirillcha** (`эзомепразол`), mini apteka esa lotin.
  Bog'lash uchun transliteratsiya + imlo kaliti (`ts→s`, `ph→f`) ishlatildi → 25 tadan 9 tasi mos.
  Qolgan 16 tasi — o'simlik ekstraktlari va kombinatsiyalar (ular XPN sifatida ro'yxatga olinmagan).
- **Sahifa hajmi:** `size=1000` ishlaydi (46 079 → 47 so'rov).
- **`search=` bo'sh** bo'lsa ham butun ro'yxat qaytadi — alohida "list all" endpointi kerak emas.
- **`mb-referent-price/analogs`** bo'sh qaytadi (analog bog'lanishi to'ldirilmagan);
  ishlaydigan yo'l — `referent-price/all` va XPN bo'yicha o'zimiz guruhlash.
- **`referent-price/rcm-by-drug-name`** 500 beradi — server tomonidagi SQL xatosi (bizning aybimiz emas).
- `pharm.gov.uz` ga **E-IMZO** bilan kirish fuqaro uchun; API esa ochiq.

---

# QO'SHIMCHA: ikkinchi qidiruv bosqichi (2026-11-18)

"Parcha qism bo'lsa ham" degan so'rov bo'yicha davom etdim. Natija: **yana 5 ta manba topildi**,
1 tasi eng muhimi.

## 7. Yangi topilgan endpointlar

| Endpoint | Nima beradi | Holat |
|---|---|---|
| `/v2/drugs/download-excel` | butun reyestr Excel | ✅ **2.8 MB · 40 000 qator · 11 ustun** |
| `/v2/drugs/{drugId}` | dori tafsiloti | ✅ **eng muhim** (quyida) |
| `/v1/atc-groups/all` | 15 ATX guruhi + dori soni | ✅ 45 199 dori |
| `/v1/analysis/counts` | 46 079 dori · **400 tibbiyot tashkiloti** | ✅ |
| `/v1/drugs/rec-drug-dosage-form` | 104 dori shakli | ✅ |
| `/file-api/v1/drugs/{uuid}.jpg` | **qadoq rasmlari** | ✅ ochiq (JPEG) |

Excel ustunlari: `ID · short Name · full Name · mnn · dosage Form · strength · country ·
manufacturer · registration Code · prescription · **pharma Cotherapeutic Group**`
(farmakoterapevtik guruh — yangi maydon).

## 8. ★ `maxSalePrice` — 3735 chegara narxi, proxy emas

`/v2/drugs/{id}` har bir dori uchun qaytaradi:

```
retailPrice     126 225.05   (so'm)
wholeSalePrice  ...
maxSalePrice    6.57         ← QONUNIY CHEGARA NARX, asl valyutada
currency        "Доллар США"
priceDate       2026-11-16
```

Ya'ni oldingi bosqichda "referent narx yopiq → chakana narxni proxy qilamiz" degan
majburiy taxmin **bekor bo'ldi**: chegara narx to'g'ridan-to'g'ri keladi.

Valyuta taqsimoti (520 yozuvda): **USD 216 · so'm 269 · yevro 30 · rubl 5**.
Kurs hisoblandi: `retail / maxSalePrice` medianasi = **19 267 so'm/USD** (2026-11-16 holatiga).
So'mdagi yozuvlarda nisbat 1.38 (chakana = chegara × ustamalar).

**Bu nima beradi:** 3735 (F09, 80% qoidasi) endi haqiqiy chegara narx ustida tekshiriladi —
taxminiy emas. `facts.json` dagi `price_model` bloki shu bilan almashtirilishi mumkin.

## 9. Yana ikkita parchа

- **Tarkib (`substanceNames`)** — har dorining yordamchi moddalari ro'yxati (520/520 da bor).
  Bioekvivalentlik **o'rnini bosmaydi**, lekin tarkibni solishtirish imkonini beradi.
- **Qadoq rasmlari** — har doriga 0–6 ta rasm (oldi, orqasi, yoni). Ochik yuklanadi.
  Tekshirildi: rasmlar faqat **qadoq dizayni**, shtrix-kod/Data Matrix **yo'q**.

## 10. Yopiq qolgani (qayta tekshirildi — 401)

| Endpoint / manba | Javob |
|---|---|
| `registry/gmp-registry` · `gdp` · `gpp` · `gcp` · `glp` · `gsp` | **401 UNAUTHORIZED** |
| `instruction/detail` (yo'riqnoma) | **401** |
| Asl Belgisi `xtrace.aslbelgisi.uz` → `/api/cod/public/code` | **401** "Full authentication is required" |
| GTIN / shtrix-kod | Excel da **yo'q**, rasmlarda **yo'q**, API'da **yo'q** |
| Bioekvivalentlik hisoboti | hech qayerda yo'q |

GMP registrlari uchun **E-IMZO** kerak (`eimzo/auth`, `eimzo/challenge` endpointlari bor) —
ya'ni yuridik shaxs sifatida kirish talab qilinadi. Bu **yozma so'rov** yo'li, texnik yo'l emas.

## 11. Yig'ilgan fayllar (qo'shimcha)

```
orindor/data/uz_registry/
  drugs_registry.xlsx   2.8 MB · 40 000 qator · oflayn ishlash uchun
  details.jsonl         520+ yozuv · maxSalePrice, tarkib, rasm soni
  atc_groups.json       15 ATX guruhi · 45 199 dori
  dosage_forms.json     104 dori shakli
  counts.json           46 079 dori · 400 tibbiyot tashkiloti
```

Qayta yig'ish: `python3 orindor/tools/harvest_mpa_extra.py` (davom etadigan — qolgan joyidan).
