# 15 MEZON BO'YICHA QAYTA TEKSHIRUV
## `T1–T5` · `B1–B5` · `S1–S5` — har biriga dalil, ball va bo'shliq

**Sana:** 17-noyabr 2026 · **Mahsulot:** JUFT · **Muammo:** №17
**Formula:** `T_Ball = (T1+…+T5)/5` · `B_Ball = (B1+…+B5)/5` · `S_Ball = (S1+…+S5)/5` · har biri 1–10

> **Bu hujjat nima uchun.** Ilgari biz ishni *"muammo to'g'ri tanlanganmi"* bo'yicha qurgan edik. Mezonlar chiqqandan keyin savol o'zgardi: **hakam qaysi 15 nuqtaga qaraydi va bizda har biriga dalil bormi.** Quyida 15 ta mezon, har biriga: mentor nimani qidiradi → bizda nima bor → ball → bo'shliq → harakat.

---

# 1. XARITA — 15 mezon, bir jadvalda

| # | Mezon | Mentor nimani qidiradi | Bizda bor dalil | Ball | Holat |
|---|---|---|---|---|---|
| **T1** | Texnik amalga oshirilish | Ishga tushadigan narsa bormi | `app/server.py` — HTTP API, 7 endpoint, `0.0.0.0:8000` da ishlaydi | **8** | 🟢 |
| **T2** | Kod tayyorligi | Kod sifati, testlar, tuzilma | Dvigatel + eval + server + UI; 4 test to'plami; 16/16 adversarial | **8** | 🟢 |
| **T3** | Yechimning innovatsionligi | Yangi nima bor | **Negativ dalil** va **abstention** birinchi darajali; 5 xil qaror; izohli model | **8** | 🟢 |
| **T4** | Jamoa bilim darajasi | Har a'zo o'z qismini tushuntira oladimi | **Himoya varaqasi** (§6): 12 qiyin savol + aniq javob | **7** | 🟡 |
| **T5** | Texnologiyalar to'plami | Stek ongli tanlanganmi | Qoida + ML + GS1 + HTTP API + UI; har biri **sabab bilan** tanlangan | **7** | 🟡 |
| **B1** | G'oya va muammoning dolzarbligi | Muammo rasmiymi, o'tkirmi | Rasmiy **№17**, so'zma-so'z iqtibos; og'riq bir gapda | **9** | 🟢 |
| **B2** | Biznes modeli / monetizatsiya | Kim to'laydi, qancha | 3 liniya + **`moliyaviy_model.xlsx`** (LTV/CAC = 5.0) | **7** | 🟡 |
| **B3** | Raqobatdagi ustunlik | Nega biz, nega himoyalangan | Moat = **standart**, mahsulot emas; 6 ta global yechim tahlil qilindi | **8** | 🟢 |
| **B4** | Moliyaviy barqarorlik | Pul yetadimi, qachon foyda | 3 yillik model + 4 ssenariy + break-even Y3-Q1 | **7** | 🟡 |
| **B5** | O'sish imkoniyati | Keyingi qadam bormi | 20 → 120 → 480 dorixona; MDH va boshqa toifalar | **7** | 🟡 |
| **S1** | Muammoning dolzarbligi | Sohaga tegishlimi | №17 ning 4 talabi → 4 javob (§2) | **9** | 🟢 |
| **S2** | Sohani tushunish chuqurligi | Terminlarni to'g'ri ishlatadimi | 738-son, ICH 2029, BCS bioveyver, NTI 90–111%, referent narx | **9** | 🟢 |
| **S3** | Amaliy qo'llanilishi | Ertaga ishlatib bo'ladimi | 30 soniyalik ish oqimi; dorixona POS integratsiyasi | **8** | 🟢 |
| **S4** | Qonunchilikka muvofiqligi | Qonun buzilmaydimi | Reyestr ustiga qurilgan; yangi majburiyat yo'q; Juft Pass audit | **8** | 🟢 |
| **S5** | Ta'sir ko'lami | Raqamlar ishonchlimi | 6 000 dorixona · 38 mln bemor · 69% tejam | **7** | 🟡 |

## Prognoz (o'z-o'zini baholash — hakam bahosi emas)

| Mentor | O'rtacha | Izoh |
|---|---|---|
| **Texnik (T)** | **7.6** | Eng past — T4 (jamoa) va T5 (stek). Ikkisi ham tuzatiladi |
| **Biznes (B)** | **7.6** | B2/B4 endi model bilan; B5 zaif |
| **Soha (S)** | **8.2** | Eng kuchli tomonimiz — №17 talabiga 1:1 moslik |

> **Muhim:** eng past ball — **T4 (jamoa bilim darajasi)**. Buni kod bilan tuzatib bo'lmaydi, lekin **himoya varaqasi** bilan "har a'zo javob bera oladi" holatiga keltirish mumkin. §6 shu uchun.

---

# 2. BU TURDA NIMA O'ZGARDI — uchta aniq harakat

Mezonlar chiqqandan keyin **uchta** ish qilindi, chunki aynan shu uchtasi eng zaif joy edi:

| # | Mezon | Ilgari | Endi |
|---|---|---|---|
| **1** | **T1 + T2 + T5** | Statik HTML, ma'lumot ichiga qotirilgan JSON | **Jonli HTTP API** — `app/server.py`, 7 endpoint, POST bilan o'z qutingizni tekshirasiz |
| **2** | **B2 + B4** | Matnda "3 liniya" deyilgan, raqam yo'q | **`moliyaviy_model.xlsx`** — 5 varaq, LTV/CAC, 3 yillik model, 4 ssenariy |
| **3** | **T4 + S2** | "Jamoani bilmayman" degan bo'shliq | **Himoya varaqasi** — 12 qiyin savol va aniq javoblar (§6) |

---

# 3. TEXNIK MEZONLAR (T)

## T1 — Texnik amalga oshirilish · **8/10**

**Mentor nima qiladi:** "Ko'rsating, ishlayaptimi?" — va o'zi tugma bosadi.

**Bizda:**

```
$ python3 app/server.py
JUFT API → http://0.0.0.0:8000
  12 mahsulot · 6 INN guruhi · 4 QR holati
```

| Endpoint | Nima qaytaradi |
|---|---|
| `GET /api/health` | `{"ok":true,"problem":17,"products":12}` |
| `GET /api/groups` | 6 INN guruhi × ishonch kartalari |
| `GET /api/trust?inn=&mg=` | Bitta INN bo'yicha solishtirish |
| `GET /api/scan-cases` | 4 QR holati |
| `POST /api/scan` | **O'z qutingizni tekshirish** — hakam maydonlarni o'zi o'zgartiradi |
| `GET /api/eval` | Xavfsizlik ko'rsatkichlari |

**Nega 8, 10 emas:** ma'lumot hali **sintetik**. Real davlat reyestriga ulanish — keyingi bosqich (W0).

**Demo skripti (30 soniya):** `POST /api/scan` → GTIN ni oxirgi raqamini o'zgartiring → 🟢 YASHIL dan 🔴 QIZIL ga o'tadi. Jonli, oldindan yozilmagan.

## T2 — Kod tayyorligi · **8/10**

| Fayl | Satr | Nima |
|---|---|---|
| `prototype/juft17_core.py` | ~700 | Dvigatel: dalil darajalari, 8 qat'iy qoida, M3 modeli, 5 qaror, 3 renderer |
| `prototype/eval_juft17.py` | ~430 | 4 test to'plami, 16 adversarial holat, shovqin testi |
| `app/server.py` | ~280 | HTTP API, 7 endpoint, faqat standart kutubxona |
| `app/index.html` | ~600 | UI, 3 rol, jonli API |

**Testlar:**

```
A. Haqiqiylik      600 sinov qutisi              → 99.8% aniqlash, 0.0% yolg'on ayblov
A2. Shovqin        400 qonuniy "shubhali" quti    → 0.0% ayblov
B. Da'vo xavfsizligi 12 mahsulot, 8 da'vo         → 0/8 asossiz
C. Adversarial     16 qiyin holat                 → 16/16
D. Halollik        import yo'q → narx da'vosi     → 2/2
```

**Nega 8, 10 emas:** CI, Docker, real DB va API autentifikatsiyasi yo'q. Hackathon uchun ortiqcha, lekin hakam so'rasa: *"W0 da SQLite + Docker, 2 kunlik ish"*.

## T3 — Yechimning innovatsionligi · **8/10**

**Mentor qidiradi:** "Bu yana bir chatbot emasmi?"

**To'rt haqiqiy yangilik — har biri himoya qilinadi:**

| # | Yangilik | Nega bu yangilik |
|---|---|---|
| **1** | **Negativ dalil — birinchi darajali javob** | Bozordagi barcha "ishonch" mahsulotlari **maqtaydi**. Bizda "hujjat yo'q" — bu **to'liq huquqli natija**, xato emas. Natija: 8 ta "ha", 4 ta "yo'q" |
| **2** | **Abstention — o'lchanadigan mezon** | Over-claim rate = 0 ni **dizayn talabi** qildik va o'lchadik. Ko'pchilik tizimda bu ko'rsatkich umuman yo'q |
| **3** | **Bitta zaif signal — tekshiruv, ayblov emas** | Narx signali yolg'iz: 0.25 🟡. Ikki mustaqil signal: 0.67 🔴. Bu — **ayblov huquqiy madaniyati**, kodda |
| **4** | **Dalil darajasi = hujjat turi** | E3 faqat NTI + 90–111% bo'lsa. Keng indeksga E3 berish **yaxshi ko'rinadi, lekin yolg'on** — biz bermaymiz |

> **Eng kuchli jumla hakam uchun:** *"Biz ishonchni o'stirmaymiz — biz ishonchni **tekshirsa bo'ladigan** qilib qo'yamiz."*

## T4 — Jamoa bilim darajasi · **7/10**

**Bu — eng zaif mezon**, chunki kod bilan tuzatilmaydi. Lekin tuzatiladigan qismi bor: **har a'zo o'z qismini tushuntira olishi**.

**Nima qilindi:** §6 da **12 qiyin savol** va aniq javob. Har bir a'zoga o'z bo'limi biriktiriladi:

| A'zo | Bo'lim | Majburiy javob |
|---|---|---|
| 1 | Muammo + №17 mosligi | S1, S3, B1 — *"nega aynan №17"* |
| 2 | Dalil darajalari + 738-son | S2, S4 — *"E3 nima uchun faqat NTI"* |
| 3 | M3 modeli + eval | T2, T3 — *"98% qayerdan"* |
| 4 | Biznes model | B2, B4, B5 — *"kim to'laydi"* |

**Qoida:** hech kim *"buni boshqasi qildi"* demaydi. Har kim **o'z raqamini** ayta oladi.

## T5 — Texnologiyalar to'plami · **7/10**

| Texnologiya | Nega aynan shu | Nega boshqasi emas |
|---|---|---|
| **Python 3.12** | Ma'lumot qatlami; 48 soatda eng tez | JS/TS — og'irroq, model qatlami zaif |
| **Qoida dvigateli (8 ta)** | Regulyator **tushunishi** shart | Sof ML — qora quti, o'tmaydi |
| **Logistik regressiya (M3)** | **Izohlanadi** — har koeffitsiyent aytiladi | Neyron tarmoq — 12 mahsulotda o'zini oqlamaydi |
| **GS1 mod-10** | Xalqaro standart, hisoblash arzon | Maxsus hash — hech kim tanimaydi |
| **HTTP API (stdlib)** | 0 bog'liqlik, istalgan joyda ishlaydi | FastAPI — yaxshiroq, lekin demo uchun ortiqcha |
| **LLM (keyingi)** | Faqat **til**: nom variantlari, tushuntirish matni | LLM dori tanlasa — **xavfsizlik halokati** |

**Asosiy texnik qaror:** **qoida > model > LLM > inson tasdiqlashi.** Bu — arxitektura, did emas: regulyator talab qiladigan **izohlanuvchanlik**.

---

# 4. BIZNES MEZONLAR (B)

## B1 — G'oya va muammoning dolzarbligi · **9/10**

**Mentor qidiradi:** "Bu muammo haqiqatan bormi yoki siz o'ylab topdingizmi?"

**Bizning javob:** muammo **rasmiy ro'yxatda**, **№17**, va PDF **yechimni ham yozib bergan**:

> "sifat sertifikatlari va laboratoriya natijalarini **shaffof ko'rsatuvchi**, dori **haqiqiyligini tekshirish** imkonini beruvchi hamda bemorlar, tibbiyot xodimlari va dorixonalarni mahalliy mahsulotni **tanlashga rag'batlantiruvchi** raqamli yechim."

**To'rt talab → to'rt javob:** sertifikat shaffofligi → A2 · haqiqiylik → A1 · rag'batlantirish → A3 · 3 aktor → 3 ekran.

**Og'riq bir gapda:** *"Dorixonada importning 69% arzon jufti turadi, farmatsevt taklif qilmaydi — qo'lida isbot yo'q."*

**Nega 9, 10 emas:** muammoning **miqdoriy** o'lchami (mahalliy dori ulushi necha foiz) hali rasmiy statistikadan olinmagan.

## B2 — Biznes modeli / monetizatsiya · **7/10**

**Kim to'laydi — uch liniya:**

| Liniya | Kim | Narx | Nega to'laydi |
|---|---|---|---|
| **Dorixona SaaS** | 6 000 dorixona | 200 000 so'm/oy | Dalil + javobgarlikdan himoya |
| **Ishlab chiqaruvchi dosye** | ~200 zavod | 10 mln so'm/yil | Hujjati bor, ko'rinmaydi → sotuv |
| **B2G / integratsiya** | Agentlik, SSV | Yillik kontrakt | Referent narx siyosati ishlashi uchun |

**Birlik iqtisodi (model fayldan):**

| Ko'rsatkich | Qiymat |
|---|---|
| LTV | 6.0 mln so'm |
| CAC | 1.2 mln so'm |
| **LTV / CAC** | **5.0** (≥3 — sog'lom) |
| Qaytish | 6 oy |
| Yalpi marja | 85% |

**Nega 7, 10 emas:** narx **bitta** dorixona bilan tasdiqlanmagan. Hakam "kim va'da berdi?" desa — halol javob: *"hech kim hali; W0 da 1 tarmoq bilan tasdiqlaymiz."*

## B3 — Raqobatdagi ustunlik · **8/10**

| Raqobatchi | Nima qiladi | Bizda ortiqcha |
|---|---|---|
| RxNorm (AQSh) | Nomlar grafi | BE, sertifikat, narx, QR |
| Orange Book | Ekvivalentlik bahosi | O'zbek reyestri |
| Synapse ($39M) | Retsept xavfsizligi | Reyestr, QR |
| Truemeds | 72% tejam | **Ishonch qatlami** |
| GS1 / TraceLink | Treysing | **Ekvivalentlik** |
| Davlat reyestri | Ro'yxat | **Solishtirish + qaror** |

> **Moat — mahsulot emas, STANDART.** Agar JUFT "sertifikat shaffofligi formati" ga aylansa, raqobat mazmunsiz qoladi. Ikkinchi moat: **skanerlash tarmog'i** — qancha dorixona, shuncha yaxshi aniqlash.

## B4 — Moliyaviy barqarorlik · **7/10**

`moliyaviy_model.xlsx` — 5 varaq: Xulosa · Birlik iqtisodi · 3 yillik model · Xarajatlar · Ssenariylar

| | 1-yil | 2-yil | 3-yil |
|---|---|---|---|
| Daromad | 78 | 808 | 2 352 |
| Xarajat | 620 | 1 100 | 1 700 |
| **Foyda** | **−542** | **−292** | **+652** |

**Break-even:** Yil-3, 1-chorak (480 dorixona + 30 zavod).
**Kerakli mablag':** ~850 mln so'm (yoki asoschilar minimal maosh bilan — ~420 mln).

**To'rt ssenariy — B4 ning asl savoli "yashaydimi?"**

| Ssenariy | 3-yil daromad | Foyda | Xulosa |
|---|---|---|---|
| Optimistik | 2 352 | +652 | O'zini qoplaydi |
| Bazaviy | 1 500 | +240 | Yashaydi |
| **Pessimistik** | **300** | **−480** | **Kichik jamoa bilan yashaydi** |
| Halokat (ruxsat yo'q) | 0 | −620 | B2B sifatida qoladi |

> **Eng muhim jumla:** *"Pessimistik ssenariyda ham xarajat 480 mln ga tushadi — ya'ni mahsulot o'lmaydi, sekinlashadi."*

## B5 — O'sish imkoniyati · **7/10**

| Bosqich | Muddat | Ko'rsatkich |
|---|---|---|
| Pilot | 0–2 oy | 1 tarmoq, 200 dori kartasi |
| Toshkent | 3–9 oy | 120 dorixona |
| Respublika | 12–24 oy | 480 dorixona + 30 zavod |
| **Kengayish** | 24+ | (1) boshqa toifalar (medtexnika), (2) MDH — Qozog'iston reyestri, (3) **eksport**: "sertifikat shaffofligi" formati boshqa mamlakatlarga |

**Nega 7, 10 emas:** kengayish rejasi **taxminiy** — Qozog'iston reyestri bilan solishtirilmagan.

---

# 5. SOHA MEZONLAR (S)

## S1 — Muammoning dolzarbligi · **9/10**
Rasmiy №17 + 738-son nizom + ICH 2029 oynasi. Muammo **o'zi o'tkir**: referent narx siyosati ishlashi uchun ishonch kerak.

## S2 — Sohani tushunish chuqurligi · **9/10**
Mentor terminlarni tekshiradi. Biz aniq aytamiz:

| Termin | Bizning javob |
|---|---|
| **Bioekvivalentlik** | Referens dori bilan qon plazmasidagi AUC/Cmax nisbati 80–125% ichida |
| **E3 nima uchun faqat NTI** | NTI uchun oraliq 90–111% ga toraytiriladi; keng indeksga E3 berish — yolg'on |
| **Bioxveyver** | BCS I/III uchun in vitro; 738-son ruxsat beradi |
| **Nega parenteral EX** | Eritma to'g'ridan-to'g'ri qonga — so'rilish bosqichi yo'q, BE talab qilinmaydi |
| **Referent narx** | Bir xil tarkibli nomlar orasidagi eng past narx |
| **Nega warfarin xavfli** | INR 10 kunda 2.5 → 4.8 siljishi mumkin |

## S3 — Amaliy qo'llanilishi · **8/10**
**30 soniyalik ish oqimi:** farmatsevt INN ni kiritadi → karta ochiladi → bemorga ko'rsatadi → Juft Pass'ga yoziladi.
**Integratsiya:** dorixona POS'iga 2 ta tugma (yoki QR skan). Yangi qurilma kerak emas.

## S4 — Qonunchilikka muvofiqligi · **8/10**

| Savol | Javob |
|---|---|
| Davlat tizimini almashtiradimi? | ❌ Ustiga quriladi — reyestr, sertifikat, BE davlatniki |
| Yangi majburiyat? | ❌ Mavjud hujjatlarni ko'rinadigan qiladi |
| Tibbiy qaror qabul qiladimi? | ❌ Faqat **ko'rsatadi**. Qaror — vrach/farmatsevt |
| Shaxsiy ma'lumot? | Bemor kartasi **saqlanmaydi** — faqat dori ma'lumoti |
| Audit? | ✅ Juft Pass: kim, qachon, nimaga asoslanib |

**Nega 8, 10 emas:** regulyator bilan **yozma** kelishuv yo'q — hali taklif bosqichida.

## S5 — Ta'sir ko'lami · **7/10**

| Ko'rsatkich | Qiymat | Holat |
|---|---|---|
| Dorixonalar | ~6 000 | ⚠️ manba tekshirilishi kerak |
| Bemorlar | 38 mln (bozor) | ✅ |
| Bitta o'ramdagi tejam | 14 500 so'm (parasetamol) | ✅ demo |
| Mahalliy dori ulushi o'sishi | **o'lchanmagan** | ❌ W1 A/B test |

**Nega 7, 10 emas:** ta'sir **potensial**, o'lchangan natija emas. Buni ochiq aytamiz — hakam yolg'ondan ko'ra abstentionni qadrlaydi (bu bizning mahsulot falsafasi ham).

---

# 6. HIMOYA VARAQASI — 12 qiyin savol

> T4 va S2 uchun. Har bir jamoa a'zosi **o'z** savolini yod bilishi kerak. Javoblar **qisqa** — 15 sekunddan oshmasin.

**1. "Sizning 99.8% qayerdan?"**
→ Sintetik 600 qalbaki qutida. Real skanerlash oqimida pastroq bo'ladi — M3 koeffitsiyentlari real ma'lumotda kalibrlanadi. Bu **chegara**, prognoz emas.

**2. "Yolg'on ayblov bo'lsa nima bo'ladi?"**
→ Qonuniy qutida ayblov **0.0%** — bu dizayn talabi. Model yakka o'zi ayblamaydi: bitta zaif signal = 🟡 tekshiruv. Ayblov faqat qat'iy qoida yoki 2+ mustaqil signaldan keyin.

**3. "Bu shunchaki QR tekshiruv emasmi?"**
→ Yo'q. QR A1 ni yechadi — **haqiqiylik**. №17 ning qolgan ikki qismi (ekvivalentlik, tanlov) QR da yo'q. Bizda uch qavat.

**4. "Nega AI? Qoidalar yetarli-ku."**
→ Qoidalar **ustun** — 8 tasi bor va modeldan yuqori turadi. AI **nozik signallarda** (M3) va **tilda** (nom normalizatsiyasi) ishlaydi. Ikkisi ham izohlanadi.

**5. "Nega mahalliy dori ishonchsiz bo'lsa ham tavsiya qilasiz?"**
→ Qilmaymiz. 12 mahsulotdan 4 tasi "yo'q" oldi. Levotiroksin 69% arzon — **tavsiya qilinmadi**.

**6. "Bu farmatsevtni sotuvchiga aylantiradi-ku?"**
→ Aksincha: farmatsevt **rad etish uchun ham asos** oladi. Mahsulot savdoni emas, **filtrni** ko'paytiradi.

**7. "Kim to'laydi — dorixona 200 ming so'mni nega beradi?"**
→ Javobgarlikdan himoya uchun. Bitta noto'g'ri almashinuvning huquqiy narxi bundan yuqori. LTV/CAC = 5.

**8. "Regulyator ruxsat bermasa?"**
→ Mahsulot B2B sifatida qoladi: zavodlar o'z dosyesini ko'rsatish uchun. Ya'ni halokat ssenariysida ham o'lmaydi.

**9. "Ma'lumotni qayerdan olasiz?"**
→ Davlat reyestri (ochiq), sertifikatlar, ishlab chiqaruvchi partiya ro'yxatlari, referent narx. Sintez faqat demo uchun.

**10. "Nega aynan №17, №16 emas?"**
→ №17 — 29/30: 48 soatda demo (5), ma'lumot bor (5), bizning tayyor aktiv (5), kam raqobat (5). №16 faqat narx haqida, ishonch emas.

**11. "Jamoa bu ishni qila oladimi?"** *(T4 ning asl savoli)*
→ Har a'zo o'z raqamini aytadi: dvigatel, model, moliya, muammo. Boshqasiga havola yo'q.

**12. "48 soatdan keyin nima bo'ladi?"**
→ W0: 1 tarmoq, 200 ta haqiqiy dori kartasi, A/B test. Asosiy KPI — **mahalliy dori ulushi**, va'da emas.

---

# 7. QOLGAN BO'SHLIQLAR — halol ro'yxat

| # | Bo'shliq | Mezon | 60 daqiqada tuzatiladimi |
|---|---|---|---|
| 1 | Real reyestrga ulanmagan (sintetik ma'lumot) | T1, S5 | ❌ — W0 ishi, 1 hafta |
| 2 | Dorixona bilan narx tasdiqlanmagan | B2, B4 | ❌ — mijoz kerak |
| 3 | Ta'sir o'lchanmagan (A/B) | S5, B5 | ❌ — pilot kerak |
| 4 | Jamoa tarkibi hujjatlashtirilmagan | T4 | ✅ — 10 daqiqa, slaydga qo'shish |
| 5 | Regulyator bilan yozma aloqa yo'q | S4 | ❌ — uchrashuv kerak |
| 6 | CI / Docker / DB yo'q | T2 | ✅ — 40 daqiqa, lekin demo uchun shart emas |

> **Birinchi 3 ta — halol cheklov.** Ularni yashirmaymiz; hakam baribir so'raydi. Tayyor javob: *"Bu W0 ning vazifasi — va biz aynan shu 3 raqamni o'lchash uchun pilot so'rayapmiz."*

---

# 8. PITCH — mezonlarga moslab qayta tartiblandi

Mezonlar ma'lum bo'lgach, **tartib** ham o'zgardi: ilgari muammodan boshlardik, endi **har slayd bitta mezon klasteriga** javob beradi.

| Slayd | Nima | Qaysi mezonga |
|---|---|---|
| 1 | Muammo — №17 so'zma-so'z + og'riq bir gapda | **B1, S1** |
| 2 | Uchta savol (A1/A2/A3) — PDF 4 talabi | **S1, S2** |
| 3 | **Jonli demo** — API, hakam o'zi bosadi | **T1, T2, T3** |
| 4 | "Ammo hamma joyda 'ha' demaymiz" — 4 ta "yo'q" | **T3, S2** |
| 5 | 99.8% / 0.0% / over-claim 0 | **T2, T3** |
| 6 | Kim to'laydi + 3 yillik model + LTV/CAC | **B2, B4, B5** |
| 7 | Raqobat: uchtasi bor, bir joyda yo'q | **B3** |
| 8 | Qonunchilik: ustiga qurilgan, yangi majburiyat yo'q | **S4** |
| 9 | Ta'sir + keyingi qadam (W0 pilot) | **S5, B5** |
| 10 | Jamoa — har a'zo bir qator | **T4** |

---

# 9. BIR SAHIFA

```
┌──────────────────────────────────────────────────────────────────────────┐
│  15 MEZON → HOLAT                           JUFT · №17                   │
├──────────────────────────────────────────────────────────────────────────┤
│  T1 texnik amalga oshirish   8   jonli API, hakam o'zi bosadi            │
│  T2 kod tayyorligi           8   4 test to'plami, 16/16 adversarial      │
│  T3 innovatsionlik           8   negativ dalil + abstention = mezon      │
│  T4 jamoa bilim              7   himoya varaqasi: 12 savol               │
│  T5 texnologiyalar           7   qoida > model > LLM (sabab bilan)       │
│                                                                          │
│  B1 dolzarblik               9   rasmiy №17, so'zma-so'z                 │
│  B2 monetizatsiya            7   3 liniya · LTV/CAC 5.0                  │
│  B3 ustunlik                 8   moat = STANDART                         │
│  B4 moliyaviy barqarorlik    7   xlsx: 3 yil, 4 ssenariy, BE Y3-Q1       │
│  B5 o'sish                   7   20 → 120 → 480 → MDH                    │
│                                                                          │
│  S1 dolzarblik               9   PDF 4 talabi → 4 javob                  │
│  S2 soha chuqurligi          9   738 · ICH 2029 · NTI · bioveyver        │
│  S3 amaliy qo'llanilish      8   30 soniya, POS integratsiyasi           │
│  S4 qonunchilik              8   ustiga qurilgan, audit, javobgarlik     │
│  S5 ta'sir                   7   potensial, o'lchanmagan (halol)         │
│                                                                          │
│  O'RTACHA:  T 7.6  ·  B 7.6  ·  S 8.2                                    │
│  ENG ZAIF:  T4 (jamoa)  —  kod bilan emas, HIMOYA bilan tuzatiladi       │
└──────────────────────────────────────────────────────────────────────────┘
```

---

*Har bir ball — o'z-o'zini baholash, hakam bahosi emas. Bo'shliqlar §7 da ochiq yozilgan: yashirilgan kamchilik birinchi savolda ochiladi, tan olingan kamchilik esa reja bo'lib ko'rinadi.*
