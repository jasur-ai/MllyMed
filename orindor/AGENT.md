# O'RINDOR AGENT — dori ishonch kartasi + xavfsiz yo'naltirish

**№17 · mahalliy dori vositalariga ishonch.** Agent ikki ishni qiladi:

| Rejim | Kirish | Chiqish |
|---|---|---|
| **A. Karta (yadro)** | dori nomi yoki XPN | davlat reyestri + referent narx + guruh taqqoslash + dalil holati |
| **B. Triaj (ikkinchi)** | shikoyat | mutaxassis + muddat, favqulodda qoidalar va skrining bilan |

Uch qat'iy chegara kodda majburlangan:

1. **Tashxis yo'q** — kasallik nomi aytilmaydi, da'vo qilinmaydi.
2. **Dori maslahati yo'q** — triajda dori nomi/doza chiqmaydi. Kartadagi nom —
   reyestr ma'lumoti, tavsiya emas.
3. **Navbat tasdiqlanmaydi** — faqat `my.gov.uz` havolasi; bron sahnalashtirilmaydi.

---

## 1. Nega bu LLM wrapper emas

| | LLM wrapper | O'RINDOR |
|---|---|---|
| Qaror | model "o'ylaydi" | qat'iy qoidalar + izohlanadigan ballash |
| Favqulodda | modelga ishonch | `FLAGS` modeldan **oldin**, har rejimda |
| Raqam | model to'qishi mumkin | faqat `data/` va `facts.json` dan |
| "Nega?" | izohsiz | har signal, har raqam, har fakt raqami ko'rsatiladi |
| Internet yo'q | ishlamaydi | hammasi qurilmada; 0 tarmoq chaqiruvi |
| Xato | bilinmaydi | `eval_agent.py` raqam beradi |

Til modeli hozir **ulanmagan** — bu ataylab. LLM qo'shilsa faqat matnni
yumshatadi va **validator** (`safety.validate_triage` / `validate_card`) dan
o'tishi shart: faktda yo'q raqam, dori nomi, doza yoki tashxis da'vosi
chiqsa — rad etiladi. Validator hozir ham har chiqishda ishlaydi.

---

## 2. Ma'lumot — real, demo emas

`data/` `tools/build_core_data.py` bilan xom manbadan yig'iladi
(`workprocess/data/` → `orindor/data/`).

| Fayl | Yozuv | Manba |
|---|---|---|
| `drugs.json` | **46 079** dori | `api.mpa.uz/.../drugs/portal/search` |
| `inn.json` | **2 941** XPN guruhi | shu reyestr, guruhlangan |
| `refprice.json` | **12 423** referent narx | `.../referent-price/all` (3735-son) |
| `detail.json` | **538** chegara narx + tarkib | `.../drugs/{id}` (`maxSalePrice`) |
| `mini.json` | 48 dorixona mahsuloti | apteka.uz (ochiq sahifalar) |
| `facts.json` | **17** huquqiy fakt | lex.uz, so'zma-so'z iqtibos |

Taqsimot: **27 620 mahalliy · 18 459 import**. Narx qamrovi **26.6%**
(12 240 yozuv) — qolgani uchun karta halol tarzda «ma'lum emas» deydi.

Yig'ish: `python3 orindor/tools/build_core_data.py` (~60 s).

---

## 3. Ishonch kartasi — har raqam ortida manba

```
💊 PARATSETAMOL — 500 мг, tabletka
   XPN, ishlab chiqaruvchi, davlat, reyestr raqami, ATX, retsept holati

💰 NARX (3735-son, 25.12.2025)
   Referent chakana / ulgurji / bazaviy valyuta / sana
   Chegara narx (maxSalePrice) — bo'lsa

📊 GURUH — 417 yozuv (312 mahalliy · 105 import)
   Bir xil shakl/doza ichida: mahalliy min · import min · farq %
   ⚠️ Bu CHEGARA narx; dorixonadagi real narx emas

🧪 DALIL (A2): BE hisoboti — MA'LUM EMAS (dosye yopiq)
   2029-01-01 ICH majburiy (738), 80% qoidasi (3735)
   GMP: TEKSHIRILMADI — reyestr ochiq, DNS yo'q (taxmin emas)

🔐 HAQIQIYLIK (A1): ASL BELGISI 2027-07-01 (149)
   QR/kod tekshiruvi — TEKSHIRILMADI (Operator API yopiq)

📚 Manbalar + «tibbiy maslahat emas»
```

**Halollik qoidalari (kodda):**

- narxlar faqat **bir xil shakl + doza** ichida solishtiriladi; aks holda
  «turli doza — to'g'ridan-to'g'ri solishtirib bo'lmaydi»;
- BE, GTIN, QR — ochiq bo'lmagani uchun **«ma'lum emas / tekshirilmadi»**;
- GMP endi qo'lda yozilmaydi: **ochiq HTML reyestr bor** (`uzpharm-gxp.uz`),
  holat `data/source_status.json` dan olinadi (quyida 9-bo'lim);
- `why_text` dagi hisob-misol **«MISOL»** yorlig'i bilan, real dorixona narxi
  sifatida ko'rsatilmaydi.

---

## 4. Xavfsizlik — critic.md P0 bandlari

| Muammo (eski) | Yechim (hozir) |
|---|---|
| 2–3 harfli skelet: `qon≈kun`, `gap≈ko'p` | moslik ≥4 harf, undosh-sinf prefiksi, 3 harfli o'zakda faqat qo'shimcha whitelist |
| «Qon qusdim» → oftalmolog | `QON_QUS` qoidasi modeldan oldin → 103 |
| «Ko'krak og'riyapti» → «1 hafta» | majburiy skrining savoli; javobsiz/noaniq → **BUGUN**, «ha» → 103 |
| «Yuzimning yarmi qimirlamayapti» → dermatolog | `STROKE_FACE/ARM/SPEECH/TONGUE` qoidalari |
| «Bolam tutqanoq tutdi» → terapevt | `SEIZURE` qoidasi |
| «2 yil» yosh deb olinadi | yosh faqat «N yosh» / «N oylik»; «yil» — davomiylik |
| «bolam» → yosh = 4 | yosh **so'raladi**, taxmin qilinmaydi |
| ruscha/kirill qatlami yo'q | kirill→lotin + ruscha qoida iboralari (`рвота с кровью`, `не могу дышать`…) |
| inkor: «og'rimayapti» signal bo'ladi | inkor faqat signal o'zagiga bog'langanda hisoblanadi |
| «Ko'p kunlardan beri holsizman» → 103 | yolg'on signal 0; umumiy holsizlik → terapevt |

Darajalar: **NOW** (103, navbat yo'q) → **TODAY** (bugun) → **SOON** →
**ROUTINE** → **LATER**. Shubha bo'lsa — yuqoriroq daraja.

---

## 5. O'lchov — `python3 orindor/eval_agent.py`

```
1) RED FLAG RECALL      32/32  100%     (yangi iboralar, UZ/RU/kirill)
2) FALSE ALARM         100/100 100%     (100 oddiy gap)
3) MUTAXASSIS top-1     26/26  100%     top-3 26/26
4) XAVFSIZ DEFAULT       4/4   100%     (javobsiz → «1 hafta» chiqmaydi)
5) YOSH AJRATISH         4/4   100%
6) KARTA (xom manba)    30/30  100%     30 haqiqiy reyestr yozuvi
6b) QIDIRUV              8/8   100%     savdo nomi + kirill
7) XAVFSIZLIK           30/30  100%     tashxis/dori/doza/maslahat yo'q
8) IQTIBOS               7/7   100%
9) DATA INTEGRITY         ✅
10) MANBA HALOLLIGI      1/1   100%     GMP holati fayldan, da'vo qo'lda emas
```

**Muhim:** testlar ham shu jamoa yozgan — bu **regression to'ri**, klinik
validatsiya emas. 100% — shu to'plamda xato yo'qligi, dunyoda xato yo'qligi
emas. Shifokor ko'rigi hali o'tkazilmagan (quyida).

---

## 6. Demo halolligi (P2)

| Eski da'vo | Hozir |
|---|---|
| «Navbat tayyor … 09:30» | «Men tasdiqlamayman» + `my.gov.uz` havolasi; vaqtni foydalanuvchi tanlaydi |
| Eslatma faqat javobda | foydalanuvchi bergan **haqiqiy vaqt**; due bo'lganda ko'rsatiladi (CLI/web), push emas |
| Offline = xotiradagi ro'yxat | `data/runtime/outbox_pending.json` — **diskda**; `flush` → `outbox_sent.json` (lokal eksport, tarmoqqa emas) |
| «Bordim» → narx kartasi (misol) | «Bordim» → eslatma to'xtaydi; dori nomini so'raydi |

---

## 7. Fayllar

```
orindor/
├── agent.py                 CLI + demo + rejim mantiqi
├── eval_agent.py            10 ta o'lchov, raqam + xato ro'yxati
├── core/
│   ├── text.py              norm, kirill→lotin, qat'iy moslik, inkor
│   ├── safety.py            FLAGS, skrining, chiqish validatori
│   ├── triage.py            mutaxassis ballash, yosh, urgency
│   ├── registry.py          qidiruv, karta, guruh narxlari
│   ├── sources.py           manba holati (GMP: ochiq/yopiq/DNS yo'q)
│   ├── evidence.py          lex.uz faktlari, manba URL
│   ├── render.py            matn shablonlari
│   └── session.py           holat, eslatma, offline (disk)
├── web/server.py            stdlib HTTP API (0 bog'liqlik)
├── web/index.html           brauzer demo (karta + chat)
├── data/                    yig'ilgan real ma'lumot + facts.json
└── tools/
    ├── build_core_data.py     xom manba → data/
    └── sources.py             19 manbani jonli tekshiradi → source_status.json
```

---

## 8. Ishga tushirish

```bash
python3 orindor/agent.py                  # jonli suhbat
python3 orindor/agent.py --demo            # karta + triaj + offline demo
python3 orindor/agent.py --card paratsetamol
python3 orindor/agent.py --ask "qon qusdim"
python3 orindor/agent.py --stats
python3 orindor/eval_agent.py              # o'lchov (10 suite)
python3 orindor/tools/sources.py           # manbalarni jonli tekshirish
python3 orindor/web/server.py --port 8000  # brauzer demo
```

API: `POST /api/chat` · `GET /api/card?q=` · `GET /api/stats` ·
`GET /api/reminders?sid=` · `GET /api/health`.

---

## 9. Qo'shimcha ochiq manbalar — 2026-11-18 tekshiruvi

Ikkinchi qidiruv bosqichi: `api.mpa.uz` dan tashqarida nima ochiq?
Har bir manba **jonli probe** qilindi (`python3 orindor/tools/sources.py`),
natija `data/source_status.json` da.

| Manba | Holat | Nima beradi / nega ulanmadi |
|---|---|---|
| `uzpharm-gxp.uz/registry2` — GMP, mahalliy | 🌐 **OCHIQ HTML**, bu muhitda DNS yo'q | sertifikat egasi, obyekt, soha, raqam, berilgan/amal muddati, `Active/Inactive`, oxirgi inspeksiya; sahifalash `?page=N` |
| `uzpharm-gxp.uz/registry6` — GMP, xorijiy | 🌐 OCHIQ HTML, DNS yo'q | `GMP_UZ – NN:YYYY` xorijiy zavodlar uchun |
| `api.mpa.uz/.../gmp-registry` | ⛔ 401 | E-IMZO talab qiladi; HTML reyestr — muqobil |
| `api.mpa.uz/.../instruction/detail` | ⛔ 400/500 | `certificateNumber` talab qiladi, haqiqiy raqam bilan ham topilmadi |
| `api.mpa.uz/.../referent-price/analogs` | ✅ 200 (hozircha bo'sh) | INN bo'yicha rasmiy analoglar; `paratsetamol`, `aspirin`, `ftoruratsil` — 0 yozuv |
| `mpa.uz/uz/open-data` | ✅ 200 (SPA) | katalog, `certificates-verification`, tibbiy buyumlar, moliyaviy hisobot |
| `data.egov.uz/datasets` | ✅ 200 | «Tarkibi bir xil, nomi turlicha» — hali **so'rov** (363 ovoz), dataset emas |
| `pharmagency.uz/en/service/manufacturers` | 🌐 DNS yo'q | 59 ishlab chiqaruvchi + STIR (nom normalizatsiyasi uchun) |

### Nima o'zgardi (kodda)

1. **Xato da'vo tuzatildi.** Ilgari karta «GMP: ochiq reyestr E-IMZO talab
   qiladi» deb yozardi — bu **noto'g'ri**: `registry2/6` ochiq HTML jadval.
   401 faqat `api.mpa.uz` JSON endpointida.
2. **`core/sources.py`** — `source_status.json` ni o'qiydi; karta va «ishonch»
   javobidagi GMP qatori shu yerdan olinadi, qo'lda yozilmaydi.
3. **Yangi holat: `UNRESOLVED`.** «Manba yopiq» va «manba ochiq, lekin bu
   qurilmada DNS yo'q» — bir xil narsa emas. Endi matnda shu farq bor:
   *«sertifikat yo'q» emas — hujjat bor, biz hozir ko'ra olmadik*.
4. **`tools/sources.py`** — 13 T0 manba (19 jami), har biri HTTP kod + tur
   bilan; probe sanasi faylga yoziladi.
5. **Eval 10-suite:** `MANBA HALOLLIGI` — GMP yozuvi faylda borligi, holati
   ma'lum ro'yxatdan ekani, kartada «TEKSHIRILMADI» chiqishi va eski
   «E-IMZO talab qiladi» da'vosi qaytib kelmaganini tekshiradi.

### Keyingi qadam (tarmoq bo'lsa — 1 soatlik ish)

`registry2`/`registry6` HTML jadvalini yig'ish → `data/gmp.json`:

```
{ "holder_norm": { "name", "cert", "issued", "valid_to", "active", "scope" } }
```

Kartada: `GMP: Active · GMP–07:2025 · 06.02.2028` yoki
`GMP: bog'lanmadi (nom mos kelmadi)` — **taxmin qilinmaydi**. Risklar:
reyestr egasi (`LLC JV «REMEDY GROUP»`) va reyestrdagi `manufacturer`
(`OOO «REMEDY GROUP»`) yozilishi farq qiladi; moslik ≥4 harf + qavs/`LLC`
tozalash bilan, mos kelmasa — «bog'lanmadi».

---

## 10. Nima hali YO'Q (yashirmaymiz)

- **Bioekvivalentlik hisoboti ochiq emas** — bitta ham mahsulot uchun BE
  dalili yo'q; karta buni «ma'lum emas» deb aytadi.
- **Shifokor ko'rigi yo'q** — 21 qoida va signal xaritasi adabiyotga asoslangan,
  ammo klinik tasdiqlanmagan. Reliz oldidan 2 shifokor ko'rigi shart.
- **GMP sertifikati kartada yo'q** — reyestr ochiq, lekin bu muhitda domen
  DNS'da topilmadi; shuning uchun karta «TEKSHIRILMADI» deydi, «yo'q» demaydi.
  Yig'ish rejasi 9-bo'limda.
- **QR/GTIN tekshiruvi** — Operator API 401; kod tekshirilmaydi.
- **Navbat API yo'q** — `my.gov.uz` da ochiq API topilmadi (404/403); faqat
  deep-link.
- **Eslatma push emas** — ilova ochiq bo'lganda due tekshiriladi.
- **Yuridik matn** — «tibbiy maslahat emas» bor, ammo javobgarlik chegarasi
  yurist tomonidan yozilmagan.
- **LLM ulanmagan** — ataylab; til qatlami keyingi qadam, validator tayyor.

---

*Manba: `api.mpa.uz` (ochiq, kalitsiz) · `lex.uz` (17 hujjat). Har iqtibosning
to'liq matni `data/uz/` da.*
