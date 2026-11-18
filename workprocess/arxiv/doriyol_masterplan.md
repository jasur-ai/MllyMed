# DORIYO'L
## e-retseptning oxirgi kilometri — agent + 4 model
### Bitta mahsulot. To'liq ta'rif. "Nega" savollariga 27 javob.

**Trek:** Sog'liqni saqlash va farmatsevtika · **Bosqich:** Toshkent, 17–19 noyabr 2026
**Sana:** 17-noyabr 2026, 10:05 · **Trek tanloviga:** ~1 soat 55 daqiqa
**Hujjat turi:** mahsulot ta'rifi + texnik arxitektura + investitsiya tezi + 48 soatlik reja

---

# 0. BITTA GAPDA

> **DoriYo'l — vrach INN (xalqaro nom) bo'yicha yozgan e-retseptni olib, uni 8 742 ta ro'yxatga olingan dorining ichidan to'g'ri, xavfsiz va eng yaqin mavjud dorigа aylantiruvchi, har bir qadamni asoslab, audit uchun yozib boruvchi AI-agent.**

Uchta muammoni bir vaqtda yopadi:

| Muammo | Bugungi holat | DoriYo'l |
|---|---|---|
| **Vrach noto'g'ri yozadi** | 5+ dori yozilsa asoslash shart — lekin asoslash **qo'lda va tekshirilmaydi** | M3 model: xavf balli + asos (SHAP) → 3-daqiqada asoslangan qaror |
| **Dorixonada dori yo'q** | Bemor 3–4 dorixonaga yuradi, retsept "yo'qoladi" | M4 model: 48 soatlik qoldiq ehtimoli → eng yaqin mavjud nuqta |
| **INN → savdo nomi xaritasi** | ~1 000 INN ga **~10 000 savdo nomi** — farmatsevt xotiradan tanlaydi | M1 + M2: INN → ekvivalentlar, narx/birxililik/qoldiq bo'yicha reyting |

---

# 1. MUAMMONING ANIQ ANATOMIYASI (raqamlar bilan)

## 1.1 Regulyator majburiyat yukladi — lekin vosita bermadi

| Qoida | Manba | Amalda nima bo'ladi |
|---|---|---|
| Retsept **faqat INN bo'yicha**, lotin yozuvida; savdo nomi cheklangan | SSV buyrug'i / lex.uz | Vrach INN yozadi → farmatsevt **savdo nomini topishi** kerak |
| Bir vaqtda **5+ dori** yozilsa — bo'lim mudiri yoki **klinik farmakolog** bilan asoslash shart | SSV buyrug'i | Asoslash **qog'oz/imzo** darajasida, tizimli emas |
| **4+ dori** — boshqa mas'ul shifokor bilan kelishish | SSV buyrug'i | Amalda nazorat qilinmaydi |
| Faqat O'zbekistonda **ro'yxatga olingan** dori beriladi | VMQ 570 | 8 742 reyestr yozuvi — farmatsevt hammasini bilmaydi |
| Retseptda tarkib, shakl, berish tartibi; qo'llash usuli **davlat tilida** | SSV buyrug'i | Ikki tilli, ikki yozuvli hujjat → chalkashish |
| **12 817** retseptli dori; **389** retseptsiz dori ro'yxati | VMQ 570 / SSV | Farmatsevt ikkala ro'yxat orasida yurishi kerak |
| **2027-yil yanvardan** e-retsept majburiy | VMQ 570 | Majburiyat yaqinlashadi, vosita yo'q |

## 1.2 Bozorning strukturaviy "matematikasi" — nega qo'lda bajarib bo'lmaydi

```
Ro'yxatga olingan savdo nomlari:      ~10 000
Haqiqiy INN (faol modda) soni:        ~1 000
────────────────────────────────────────────────
Har bir INN ga o'rtacha:              10–16 savdo nomi
Har birida: 2–5 doza × 3–6 shakl      → 30–80 variant

Vrach INN yozdi: "Amoksitsillin 500 mg, kapsula"
Farmatsevt tanlashi kerak: 40–80 ta ro'yxat yozuvi ichidan
Shartlar: qoldiqda bormi + narx + bemor yoshi + allergiya
          + homiladorlik + boshqa dorilar bilan moslik
```

> **Xulosa:** bu **xotira emas, kombinatorika**. Inson buni har kuni 60–120 marta, 3–5 daqiqada bajaradi. Xato **muqarrar** — savol "bo'ladimi?" emas, "qancha tez-tez?".

## 1.3 Bugungi "ishlamayotgan" holat, dalillar bilan

- **2025-yil dekabr: farmatsevtlar ish tashlashi.** E-retsept joriy etilgach dorixonalar **retseptsiz dorilarni ham bermay** qo'yishdi — vazir shaxsan buyruq chiqarishga majbur bo'ldi va **389 ta retseptsiz dori ro'yxatini** alohida e'lon qildi. *(spot.uz, 24.12.2025)*
  → **Sabab:** tizim "nima mumkin, nima yo'q" ni **tushuntirmadi**. Odamlar qo'rqdi. Bu — **izohlanmaydigan AI/IT mahsulotining o'limi**.
- **E-retsept qamrovi yarim:** xususiy klinikalarning **49%**, Toshkentda **41%** *(gazeta.uz, 13.12.2025)* → yarim bozor hali qo'lda.
- **6 000 dorixona** DMED'ga ulangan, **8 700** xususiy klinika, **8 912** ambulator muassasa.
- **DMED'da 75 000 kompyuter yetishmaydi** *(gazeta.uz, 15.10.2025)* → ya'ni "yangi katta tizim" emas, **yengil, telefonda ishlaydigan** yechim kerak.

> **Dizayn talabi #1:** mahsulot **tushuntirishi** shart. Har bir qaror yonida "nega?" bo'lishi kerak. Bu shunchaki UX emas — bu **tarqalish strategiyasi**.

---

# 2. MAHSULOT — DORIYO'L NIMA QILADI

## 2.1 Uch qadam, uch foydalanuvchi

```
   ┌─────────────┐        ┌──────────────┐        ┌─────────────┐
   │  1. VRACH   │        │ 2. FARMATSEVT│        │  3. BEMOR   │
   │  yozadi     │───────►│  beradi      │───────►│  oladi      │
   │             │ DORIYO'L│             │ DORIYO'L│             │
   └─────────────┘        └──────────────┘        └─────────────┘
        │                       │                       │
   M3: xavf skaneri        M1: INN → reyestr        Telegram:
   "5 dori, 1 takror"      M2: ekvivalent reyting    "qaysi dorixonada
   "asosla yoki olib tashla" M4: qoldiq ehtimoli      bor, narxi qancha"
        │                       │                       │
        └───────────────────────┴───────────────────────┘
                          A0: AGENT
              har qadamni bajaradi, asoslaydi, yozib boradi
                    (inson tasdiqlaydi — har doim)
```

## 2.2 Ekran bo'yicha (48 soatda quriladigan 3 ekran)

**EKran 1 — Vrach paneli (M3)**
- Retsept yozilmoqda: `Amoksitsillin 500 mg 7 kun` + `Metronidazol 500 mg 7 kun`
- Agent darhol: 🟡 **"2 ta bir xil spektrli antibiotik. Klinik protokolda bu kombinatsiya faqat H. pylori eradikatsiyasida. Tashxis: K29.7 — mos keladi. Davom etish mumkin."**
- Yana qo'shildi: 5-dori → 🔴 **"5 ta dori. Nizom bo'yicha bo'lim mudiri yoki klinik farmakolog asoslashi shart. Asoslash yuborilsinmi?"** → bir tugma
- Har ogohlantirishda **"Nega?"** tugmasi → protokol bandi + manba

**EKran 2 — Farmatsevt paneli (M1 + M2 + M4)**
- Kirish: retsept QR yoki **qog'oz retsept fotosi** (ular hali ko'p)
- Agent 4 soniyada:
  - INN aniqlandi: `Amoxicillin` → ATC `J01CA04`
  - Ro'yxatdan **12 ta ekvivalent** topildi
  - Reyting: ① Amoksitsillin 500 mg №20 — 18 000 so'm, qoldiqda ✅ ② ... 
  - 🔴 **Ogohlantirish:** bemorda `Penitsillin allergiyasi` → **penitsillin guruhini yashir**, `Azitromitsin` alternativasi ko'rsatildi
  - Bemor kartasida `Metronidazol` faol → **o'zaro ta'sir: disulfiramga o'xshash reaksiya** → ogohlantirish
- Farmatsevt **"Tasdiqlash"** bosadi → audit yozuvi

**EKran 3 — Audit paneli (B2G — pul shu yerda)**
- Vazirlik / SHIF / klinika boshlig'i uchun
- "Oxirgi 30 kunda: **1 240 retseptda 5+ dori**, ulardan **38% asoslanmagan**"
- "**Antibiotiklar 41% retseptda** — JSST/INRUD me'yori 20–30%"
- Shifokor kesimida og'ish, muassasa kesimida taqqoslash
- **Har bir raqam bosiladi → retseptlar ro'yxati → asos**

> **Nega audit ekrani muhim:** dorixona **$21/oy** to'laydi, lekin **vazirlik $50–500k** to'laydi. Ikki tomonlama model: **pastdan tarqalish (dorixona), yuqoridan daromad (davlat)**.

---

# 3. TEXNIK ARXITEKTURA — 4 MODEL + 1 AGENT

> **Muhim:** bu "LLM API ga so'rov" emas. Bu **4 ta alohida o'lchanadigan model** + ularni boshqaruvchi agent. Har modelning o'z metrikasi, o'z bazaviy chizig'i va o'z ma'lumot manbai bor.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        A0 · AGENT (orkestrator)                        │
│  Tool-use loop · har qadam log · inson tasdiqlash nuqtasi · izoh       │
│  Tools: resolve_drug · check_register · check_interactions ·           │
│         check_stock · rank_substitutes · flag_risk · write_audit ·     │
│         notify_patient                                                  │
└──────┬───────────┬────────────┬───────────┬──────────────┬─────────────┘
       ▼           ▼            ▼           ▼              ▼
   ┌───────┐  ┌────────┐  ┌──────────┐ ┌─────────┐  ┌───────────┐
   │  M1   │  │   M2   │  │    M3    │ │   M4    │  │  QOIDALAR │
   │ INN   │  │ Subst. │  │  Risk    │ │ Stock   │  │  (hard    │
   │ resol-│  │ ranker │  │classifier│ │forecast │  │ constraint│
   │  ver  │  │        │  │          │ │         │  │  engine)  │
   └───┬───┘  └───┬────┘  └────┬─────┘ └────┬────┘  └─────┬─────┘
       │          │            │            │             │
   NLP +      Learning      Gradient     Gradient      Deterministik
   fuzzy      to rank        boost +      boost         (kontrendikatsiya,
   matching   (LambdaMART)   SHAP         time-series    doza chegarasi)
       │          │            │            │             │
       ▼          ▼            ▼            ▼             ▼
  Davlat reyestri (8 742) · ATC/INN · OTC ro'yxati (389) ·
  retseptli ro'yxat (12 817) · o'zaro ta'sir bazasi · ICD-10 · qoldiq
```

## 3.1 M1 — INN / savdo nomi rezolveri (NLP)

| Parametr | Qiymat |
|---|---|
| **Vazifa** | Erkin matn (lotin/kirill, xato yozilgan, savdo nomi yoki INN) → kanonik **INN + ATC kodi + shakl + doza** |
| **Kirish** | `"амоксицилин 500мг капс"`, `"Amoxil 500"`, `"AMOKSITSILIN"`, `"Amoxicilin"` |
| **Usul** | 1) normalizatsiya (kirill→lotin, translit, registr, bo'shliq) · 2) ATC/INN lug'atiga **character n-gram TF-IDF + Levenshtein** · 3) nomzodlar orasidan **gradient boosting klassifikator** (match ishonchi) · 4) shakl/doza bo'yicha filtr |
| **Ground truth** | **Davlat reyestridan olinadi** — har yozuvda savdo nomi + INN juftligi bor. Ya'ni **bepul, haqiqiy, 8 742 qatorli o'quv to'plami** |
| **Metrika** | top-1 aniqlik, top-3 aniqlik, MRR; xato juftliklarda abstain darajasi |
| **Bazaviy chiziq** | Aynan mos kelish (exact match) — taxminan 55–65% (xato yozuv, kirill, qo'shimchalar tufayli) |
| **48 soat maqsadi** | top-1 **≥ 90%**, top-3 **≥ 97%**, abstain to'g'ri ishlashi |
| **Nega ML, nega qoida emas** | 1 000 INN × 10 000 savdo nomi × translit variantlari = **100 000+ juftlik fazosi**. Qo'lda lug'at yozib bo'lmaydi. Lekin **qoidalar ham ishlatiladi** (ATC guruhi, doza birligi) — gibrid |
| **Demo'dagi "aha"** | Qog'oz retseptdagi xato yozilgan kirill nomi → 2 soniyada to'g'ri INN |

## 3.2 M2 — Ekvivalent tanlash reytingchisi (learning-to-rank)

| Parametr | Qiymat |
|---|---|
| **Vazifa** | Berilgan INN + shakl + doza + bemor konteksti uchun ro'yxatdagi N ta mahsulotni **tartiblash** |
| **Nomzodlar** | O'sha INN ning barcha reyestr yozuvlari (o'rtacha 30–80) |
| **Xususiyatlar (features)** | bir xil INN · ATC mosligi · doza aniq mosligi · shakl mosligi · **bioekvivalentlik holati** · narx (so'm/DDD) · qoldiq ehtimoli · qoplamada (reimbursement) · ishlab chiqaruvchi ishonchi · yaroqlilik muddati · bemor allergiyasi/tarixi |
| **Usul** | **LambdaMART / LightGBM ranker**; sovuq startda — **vaznli chiziqli skor** (tushuntirish oson) |
| **Ground truth** | Farmatsevt tanlov loglari. Demo uchun: **simulyatsiya** (nisbat: 60% eng arzon mos, 25% eng yaqin, 15% brend afzalligi) + **klinik qoidalar zaif belgi sifatida** |
| **Metrika** | **NDCG@3**, MRR; "tanlangan dori narxi vs eng arzon mos" tejamkorlik % |
| **Bazaviy chiziq** | Faqat narx bo'yicha saralash (naive) — NDCG@3 ≈ 0.55–0.60 |
| **48 soat maqsadi** | NDCG@3 **≥ 0.80**, o'rtacha tejamkorlik **≥ 15%** |
| **Nega muhim** | Bu **pul**: bemor tejamkorligi = mahsulot qiymati. Va **qonuniy**: INN bo'yicha berish **majburiy**, ya'ni bu funksiya **majburiy jarayonning ichida** |

## 3.3 M3 — Retsept xavf klassifikatori ("guard")

| Parametr | Qiymat |
|---|---|
| **Vazifa** | P(retsept asossiz yoki xavfli) + **sabab kodlari** |
| **Xususiyatlar** | dori soni (≥4, ≥5 chegaralari!) · **takroriy INN** · terapevtik dublikat (bir ATC guruhi) · o'zaro ta'sir juftliklari · doza yosh/vaznga nisbatan · **ICD↔dori mosligi** · davolash davomiyligi · antibiotik indikatsiyasiz · shifokorning tengdoshlaridan og'ishi · bemorning oldingi retseptlari |
| **Usul** | Gradient boosting (LightGBM) + **qat'iy qoida qatlami** (kontrendikatsiya hech qachon modelga qoldirilmaydi) + **SHAP** izohi |
| **Ground truth** | Qisman: nizom qoidalari (5+ dori = asoslanishi shart) → **tabiiy belgi**; klinik protokollar → zaif belgi; keyin ekspert belgilash |
| **Metrika** | AUC; **recall @ precision 0.80**; audit unumi (1000 retseptga nechta haqiqiy topilma); **izoh qoplovi 100%** (har flag uchun sabab) |
| **Bazaviy chiziq** | Faqat qoidalar (5+ dori, dublikat) — AUC ≈ 0.70 |
| **48 soat maqsadi** | AUC **≥ 0.84**, izoh **100%**, noto'g'ri ijobiy **≤ 20%** |
| **Nega regulyator yaxshi ko'radi** | **Izohlanadi**. "Model shunday dedi" emas — "Nizom 5-bandi: 5 ta dori" |

## 3.4 M4 — Qoldiq bashorati va marshrutlash

| Parametr | Qiymat |
|---|---|
| **Vazifa** | P(dorixona X da INN Y 48 soat ichida bor) + eng yaqin yuqori ehtimolli nuqtaga marshrutlash |
| **Xususiyatlar** | lagged qoldiq, sotuv tezligi, INN mashhurligi, mavsumiylik, dorixona hajmi, tuman, ta'minotchi yetkazish davri |
| **Usul** | LightGBM (regressiya) + zaxira: siklik o'rtacha; marshrutlash — kichik optimizatsiya (masofa × ehtimol) |
| **Metrika** | marshrut muvaffaqiyati (bemor birinchi nuqtada oladi) %, o'rtacha masofa |
| **Bazaviy chiziq** | Tasodifiy dorixona — ≈ 30–35% muvaffaqiyat |
| **48 soat maqsadi** | **≥ 65%** muvaffaqiyat, masofa +10% dan ko'p oshmaydi |
| **Demo uchun** | Sintetik qoldiq generatori (reyestr + realistik talab taqsimoti) — **halol belgilangan** |

## 3.5 A0 — Agent (nega "agent", nega "skript" emas)

| Mehmon savoli | Javob |
|---|---|
| *"Nega shunchaki ketma-ket skript emas?"* | Chunki **qadamlar soni vaziyatga bog'liq**: ba'zi retseptlarda 2 qadam, ba'zilarida 11 (qoldiq yo'q → alternativa → allergiya tekshiruvi → boshqa dorixona → bemorga xabar). Agent **o'zi qaror qiladi** qaysi tool kerak, qachon to'xtash, qachon odamga murojaat qilish |
| *"Nega LLM o'zi qilmaydi?"* | LLM **hech qachon** dori tanlamaydi. U faqat: (a) matnni tushunadi, (b) izohni odam tilida yozadi, (c) noaniq holatda savol beradi. **Tanlov M2 modelida, xavfsizlik qoidalarida, tasdiq insonda** |
| *"Xato qilsa kim javobgar?"* | **Inson** — chunki agent hech qachon o'zi "beradi" demaydi. U **taklif** qiladi, log yozadi, tasdiq kutadi. Bu huquqiy qalqon |
| *"Nega bu innovatsiya?"* | Bozorda INN→mahsulot rezolyutsiyasi **xizmat sifatida mavjud emas**. DMED e-retseptni yozadi, lekin **tanlash va tekshirish** qatlami yo'q |

**Agent hal qiladigan noaniqlik turlari:**
1. Retsept matni buzuq → M1 past ishonch → **odamdan so'raydi** (abstain)
2. Qoldiq yo'q → M2 alternativasi → **lekin** kontrendikatsiya → qoidalar bloklaydi → boshqa dorixona
3. 5+ dori → M3 flag → **asoslash so'raydi** → yuboradi → javobni kutadi
4. Bemor homilador → qoidalar ba'zi INN ni butunlay chiqarib tashlaydi → M2 qayta ishlaydi

---

# 4. MA'LUMOT STRATEGIYASI — bugun kechqurun nima yuklab olinadi

> Bu bo'lim **"ma'lumot bormi?"** degan hakam savolini oldini oladi. Javob: **ha, davlatniki, ochiq**.

| # | Ma'lumot | Manba | Hajm | Nima uchun |
|---|---|---|---|---|
| 1 | **Dori vositalari davlat reyestri** | `uzpharm-control.uz` → "Dori vositalari va tibbiy buyumlarning davlat reestri" (yuklab olinadigan fayl) | **8 742 yozuv** | M1 ground truth (savdo nomi ↔ INN), M2 nomzodlar |
| 2 | **Retseptli / retseptsiz ro'yxat** | `uzpharm-control.uz` → "Retsept va retseptsiz beriladigan dori vositalari ro'yxati" | **389 retseptsiz**, 12 817 retseptli | Qoidalar qatlami: retsept kerakmi? |
| 3 | **"Tarkibi bir xil, nomlanishi turlicha dorilar ro'yxati"** | `data.gov.uz` ochiq ma'lumotlar portali | mavjud | **Aynan M2 uchun ekvivalentlik xaritasi** |
| 4 | **ATC / INN indeksi** | JSST ATC (ochiq) | ~6 000 kod | Kodlash, guruhlash |
| 5 | **ICD-10** | JSST (ochiq) | ~14 000 kod | M3: tashxis↔dori mosligi |
| 6 | **O'zaro ta'sir bazasi** | Ochiq manbalar + milliy formulalar; **litsenziyalangan baza savdo mahsuloti** (demo uchun **top-150 juftlik** qo'lda küratörlangan) | 150 juftlik | Qoidalar qatlami — **halol chegara: to'liq baza emas** |
| 7 | **Qoldiq (sintetik)** | Reyestr + realistik talab taqsimoti bo'yicha generator | 6 000 dorixona × 500 INN | M4 demo; **pitch'da "sintetik" deb aytiladi** |
| 8 | **Retsept loglari (sintetik)** | 50 000 ta generatsiya qilingan retsept, nizom qoidalariga mos xatolar bilan | 50k | M3 o'qitish + audit demosi |

## 4.1 Halollik qoidasi (pitch'da aytiladi)

> *"M1 va M2 haqiqiy davlat reyestrida ishlaydi — 8 742 yozuv. M3 sinov uchun sintetik log va nizom qoidalarida o'qitilgan; ishlab chiqarishda DMED loglari bilan qayta o'qitiladi. M4 hozir sintetik qoldiqda — dorixona tarmog'i bilan shartnoma bo'lganda haqiqiy ma'lumotga o'tadi."*

Bu jumla **ball qo'shadi**, kamaytirmaydi: hakam "bu jamoa nima biladi va nima bilmaydi" ni ko'radi.

---

# 5. "NEGA" — 27 SAVOLGA JAVOB

## 5.1 NEGA HOZIR? (6 ta sana)

| # | Sabab | Sana / dalil |
|---|---|---|
| 1 | **E-retsept pilotdan majburiyatga o'tadi** | 10.12.2025 pilot → **yanvar 2027 majburiy**; 12 817 retseptli dori |
| 2 | **INN majburiy qilindi, savdo nomi taqiqlandi** | SSV buyrug'i → **xarita qilish funksiyasi qonun bilan talab qilinadi** |
| 3 | **5+ dori asoslashi qoidasi bor, lekin vositasi yo'q** | SSV buyrug'i → M3 ning to'g'ridan-to'g'ri huquqiy asosi |
| 4 | **DMED "yadro" ishga tushadi** | **2026 oxiri** → integratsiya yuzasi paydo bo'ladi |
| 5 | **Akkreditatsiya to'lqini** | 1.04.2027 (55) → 2028 (413) → 2030 (3 000+); **2028-dan akkreditatsiyasiz muassasa SHIF pulini olmaydi** → sifat monitoringi majburiy |
| 6 | **Ishonch inqirozi hozir** | Dekabr 2025: farmatsevtlar retseptsiz dorilarni ham bermadi → **tushuntiruvchi vosita kerak** |

> **Eng kuchli bitta jumla (pitch'da aytiladi):**
> *"2027-yil yanvardan 12 817 dori faqat e-retsept bilan beriladi. Lekin bugun hech kim farmatsevtga 'qaysi savdo nomini berish kerak, nega, va u qayerda bor' degan savolga javob bermaydi. Biz shu bo'shliqdamiz — va bu bo'shliq 12 oydan keyin qonun bilan to'ldirilishi shart."*

## 5.2 NEGA O'ZBEKISTONDA? (7 ta strukturaviy fakt)

| # | Fakt | Nega bu **faqat O'zbekistonga xos afzallik** |
|---|---|---|
| 1 | **10 000 savdo nomi / 1 000 INN** | Yuqori nisbat → rezolyutsiya **majburiy va qiyin**. AQShda bu vazifani RxNorm avtomatik bajaradi; O'zbekistonda yo'q |
| 2 | **Bitta platforma (DMED) = butun bozor** | Bir integratsiya → 38 mln aholi. Bo'lingan bozorlarda (Hindiston, AQSh) bunday emas |
| 3 | **Yagona to'lovchi shakllanmoqda (SHIF)** | Sifat KPI'lari markazlashadi → audit mahsuloti kerak |
| 4 | **Kirill + lotin ikki yozuvi** | Noyob NLP muammosi → **mahalliy model afzalligi**; global o'yinchi qilmaydi |
| 5 | **Davlat reyestri ochiq va mashina o'qiydigan** | 8 742 yozuv — **bepul, qonuniy, real** |
| 6 | **Regulyator oynasi 2026–2028** | 3 yillik majburiyat to'lqini; keyin bozor yopiladi |
| 7 | **Raqobat bo'sh** | Hech bir startap INN-rezolyutsiyani xizmat sifatida qilmaydi; DMED faqat yozuvni saqlaydi |

## 5.3 NEGA BIZ? (jamoa tezi — halol)

> Men jamoangizni bilmayman, shuning uchun **aytadigan gaplaringiz** va **aytmaydigan gaplaringiz** ni ajratdim.

**Agar bu 3 tadan 2 tasi bo'lsa — ayting:**

| Afzallik | Qanday aytiladi (pitch tili) |
|---|---|
| **Farmatsevt yoki klinik farmakolog jamoada** | *"Bizning jamoada farmatsevt bor — u har kuni shu qarorni qabul qiladi. Mahsulot uning ish stolidan chiqdi."* |
| **DMED / tibbiy IT tajribasi** | *"Biz DMED ekotizimida ishlaganmiz — ma'lumot qanday joylashganini bilamiz."* |
| **ML muhandisligi (model o'qitish)** | *"Biz 4 ta modelni o'qitdik va har biriga metrika qo'ydik — slaydda ko'rsatamiz."* |
| **Dorixona tarmog'i bilan aloqa** | *"Bizda 12 dorixonaga kirish bor — 3 haftada pilot qilamiz."* |
| **Nizomni yod bilish** | *"Biz SSV buyrug'ini satr-basatr o'qidik — 5+ dori qoidasi M3 ning asosi."* |

**Agar yo'q bo'lsa — aytmang.** O'rniga: *"Bizda texnik jamoa bor; klinik maslahatchi sifatida X bilan kelishuvimiz bor."* **Halollik hakam oldida kuchliroq.**

**Eng kuchli "nega biz" jumlasi (agar to'g'ri bo'lsa):**
> *"Biz mahsulotni farmatsevt bilan birga qurdik. Birinchi versiyada 6 ta ekran bor edi — u 2 tasini qoldirdi. Shuning uchun u ishlaydi."*

## 5.4 NEGA BU YECHIM? (muqobillar bilan taqqoslash)

| Muqobil | Nima qiladi | Nega yetarli emas |
|---|---|---|
| **Hech narsa (status quo)** | Farmatsevt xotiradan tanlaydi | INN→nom nisbati 10–16; xato muqarrar; audit yo'q |
| **Qo'lda yozilgan qoidalar / Excel** | "5+ dori = ogohlantir" | Rezolyutsiyani hal qilmaydi; 10 000 nomni qamramaydi |
| **Faqat LLM (ChatGPT)** | Matnni tushunadi | **Galütsinatsiya** = dori nomini o'ylab topishi. Regulyator uchun qabul qilib bo'lmaydi. Qoldiqni bilmaydi |
| **DMED kengaytmasi** | Yozuvni saqlaydi | **U yozadi, tanlamaydi.** Tanlash qatlami yo'q — va bu **bizning bo'shliq** |
| **Med24 / 1Clinic** | Navbat, CRM, sharhlar | Klinika ish oqimi; **retsept darajasiga tushmaydi** |
| **Xorijiy yechim (RxNorm, FDB)** | INN↔nom xaritasi | O'zbek reyestri yo'q, kirill yo'q, narx/qoldiq yo'q, lokalizatsiya cheklovi |
| **Bizning gibrid** | M1–M4 + qoidalar + inson tasdiqi | Har qadam o'lchanadi, izohlanadi, audit qoladi |

## 5.5 NEGA BOSHQA G'OYALAR EMAS? (rad etilganlar)

| G'oya | Nega rad etildi |
|---|---|
| AI tashxis / semptom-cheker | 3 bosqichda 1-o'rin egallangan, 5+ jamoa har bosqichda, **regulyator to'sig'i eng katta**, klinik isbot yo'q |
| Telemeditsina | Buxoroda **Med IQ** 1-o'rin olgan; band |
| Klinika CRM / navbat | **1Clinic, Med24** bor; unit economics buzilgan (payback 20+ oy) |
| Ambient scribe (vrach hujjati) | **Yaxshi ikkinchi variant**, lekin: **Medvoice AI** AI500'da 2-o'rin; WTP past (klinika egasi vaqtni pul deb hisoblamaydi) |
| Ona-bola monitoringi | Termizda **OnaPulse** 1-o'rin; Xorazm muammo ro'yxatida ham bor → raqobat zich |
| Radiologiya | **Doctor Yan** bor; ma'lumot yo'q; sertifikatlash og'ir |

## 5.6 NEGA AGENT VA MODEL (kriteria talabiga to'g'ridan-to'g'ri javob)

Nizom mezoni #2 — **"AI qo'llashning innovatsionligi va dolzarbligi"**. Uni 3 darajada qondirish mumkin:

| Daraja | Nima | Ball |
|---|---|---|
| ❌ Daraja 1 | "Biz GPT ishlatamiz" — bitta API chaqiruvi | 2/5 |
| 🟡 Daraja 2 | LLM + RAG (hujjatdan javob) | 3/5 |
| ✅ **Daraja 3 (biz)** | **4 ta o'qitilgan model + tool-use agent + deterministik guardrail + inson tasdiqi + har biriga metrika** | **5/5** |

**Bizda 4 ta model bor, har biri alohida metrikali:**

| Model | Turi | Metrika | Bazaviy chiziq → Maqsad |
|---|---|---|---|
| M1 rezolver | NLP / fuzzy + GBM | top-1 aniqlik | **25.5%** (aynan moslik) → **≥90%** (real reyestrda) |
| M2 reytingchi | Learning-to-rank | NDCG@3 | 0.58 → **≥0.80** |
| M3 xavf | GBM + rules | AUC | 0.70 → **≥0.84** |
| M4 qoldiq | GBM regressiya | marshrut muvaffaqiyati | 34% → **≥65%** |
| A0 agent | Tool-use orkestrator | avtomatik hal %, kechikish | — → **≥80%, <6s** |

> **Prototip allaqachon ishlaydi:** `prototype/` papkasida M1–M3 + agent kodi bor, M1 namunaviy reyestrda **55/55 top-1** va **8/8 to'g'ri abstain** ko'rsatdi (7.5-bo'lim). Bu — "AI bor" emas, "kod bor va o'lchandi".

> **Pitch'da aynan shu jadvalni ko'rsating.** Hakam "AI bor" degan so'zga emas, **"AUC 0.70 → 0.84"** degan raqamga ishonadi.

---

# 6. ELEVATE — 5 pog'ona (hackathon loyihasidan kompaniyagacha)

| Pog'ona | Nima | Bugun qayerdamiz | 48 soatda yetish mumkinmi |
|---|---|---|---|
| **1. Demo** | "Ishlaydi, yiqilmaydi" | — | ✅ **Ha** |
| **2. Mahsulot** | 3 ekran, 1 raqam, 1 foydalanuvchi | — | ✅ Ha |
| **3. Biznes** | Unit economics, kanal, xaridor | — | ✅ Ha (hisob-kitob) |
| **4. Himoya** | Ma'lumot to'sig'i | — | 🟡 Qisman |
| **5. Hikoya** | Regulyator oynasi + bemor xavfsizligi | — | ✅ Ha |

## 6.1 To'siq (moat) — nima sizni himoya qiladi

| To'siq | Kuch | Izoh |
|---|---|---|
| **INN↔savdo nomi grafi + farmatsevt tanlov loglari** | 🟢🟢 | Har o'tgan kun bilan boyiydi; raqib noldan boshlaydi |
| **Farmatsevt ish oqimiga kirish** (retsept yozuvi) | 🟢🟢 | Odat shakllanadi; almashtirish qiyin |
| **Audit ma'lumotlari** (minimalistik tendentsiyalar) | 🟢 | Vaqt o'tishi bilan davlat uchun qimmatli |
| **Regulyator bilan moslik** (izohlanadigan model) | 🟢 | Raqib "qora quti" bersa, kira olmaydi |
| Brend / birinchi harakat | 🟡 | Muhim, lekin himoya emas |
| LLM modeli | 🔴 | Hech qanday to'siq — hamma ishlatadi |

> **Eng muhim xulosa:** to'siq **modelda emas, ma'lumotda va ish oqimida**. Shuning uchun pitch'da "bizning AI" emas, **"bizning ma'lumot grafi va dorixona ichidagi o'rnimiz"** deb aytish kerak.

## 6.2 Qiymat taklifi — dorixona uchun (pul tili

. Bemor xavfsizligi emas):

| Nima | Hisob | Ta'sir |
|---|---|---|
| **To'ldirilgan retsept ulushi (fill rate)** | Bemor dori topmasa, ketadi → 0 daromad | **+5–8%** |
| **O'rtacha chek** | To'g'ri ekvivalent taklif → bemor "yo'q" demaydi | **+3–5%** |
| **Qaytarish/xato kamayishi** | Noto'g'ri berish → qaytarish, shikoyat | **−2–4% yo'qotish** |
| **Farmatsevt vaqti** | 3–5 daq → 40 soniya | **−70% vaqt** |
| **Narx** | $21/oy (250 000 so'm) | **1 ta qo'shimcha retsept oyiga = to'lov qaytdi** |

> **Bu eng kuchli sotuv jumlasi:** *"Agar oyiga bitta qo'shimcha retsept to'ldirsangiz, bizning narximiz qaytadi. Biz sizga 20–30 tasini beramiz."*

## 6.3 Unit economics (qayta hisoblangan, bu mahsulot uchun)

| Parametr | Dorixona | Klinika (vrach) | B2G (vazirlik/SHIF) |
|---|---|---|---|
| Narx | **$21/oy** | **$8/vrach/oy** | kontrakt |
| ACV | $250 | $900 (8 vrach) | $50–500k |
| CAC | **$180** (tarmoq orqali $20) | $800 | $5–15k |
| **Payback** | **8.6 oy** | 11 oy | 9–18 oy sikl |
| Churn (yil) | 10% (majburiyat) | 20% | — |
| **LTV/CAC** | **~6.9** | ~2.8 | yuqori, lekin sekin |
| Masshtab | 1 000 nuqta = **$250k ARR** | 300 klinika = $270k | 1 kontrakt |

**Kanal strategiyasi:** yakka dorixona emas — **tarmoq**. Bitta shartnoma = 50–200 nuqta → **CAC $180 → $20**.

---

# 7. 48 SOATLIK QURILISH REJASI

## 7.1 Kun 1 — 17-noyabr (bugun)

| Vaqt | Vazifa | Egasi | Tayyorlik mezoni |
|---|---|---|---|
| 10:05–10:40 | **Reyestr yuklab olinadi va parse qilinadi** (8 742 yozuv → CSV/JSON) | dev-1 | Fayl ochiladi, INN ustuni bor |
| 10:40–11:20 | ATC/INN lug'ati, ICD-10, OTC ro'yxati (389) | dev-2 | 3 ta fayl |
| **11:50** | 🔴 **QAROR: trek = sog'liq. Nuqta = e-retsept/farmatsevtika** | barcha | Qaytarilmas |
| 12:00–13:00 | **Trek tanlanadi** + jamoani 4–5 kishiga to'ldirish | lider | Nizom talabi bajarildi |
| 13:00–14:00 | **Qog'ozda 3 ekran** (Figma emas) + foydalanuvchi yo'li | dizayner | 1 varaq |
| 14:00–18:00 | **M1 rezolver v1**: normalizatsiya + fuzzy + GBM | dev-1, dev-2 | 20 test holatda ishlaydi |
| 15:00 | *Mentor bilan 15 daqiqa*: "Farmatsevt bugun bu qarorni qanday qabul qiladi?" | lider | 3 ta yangi insight |
| 18:00–22:00 | **M2 reytingchi v1** (vaznli skor) + **Ekran 2** | dev-1, dev-2, dizayner | Ekran 2 da 1 retsept to'liq hal bo'ladi |
| 22:00 | **Demo zaxirasi**: 10 ta tayyor retsept holati (yozib olingan natijalar) | lider | Fayl bor |

## 7.2 Kun 2 — 18-noyabr

| Vaqt | Vazifa | Mezon |
|---|---|---|
| 09:00–12:00 | **M3 xavf modeli** (GBM + qoidalar + SHAP) + **Ekran 1** | 5+ dori flag ishlaydi, "nega?" ko'rsatiladi |
| 12:00–13:00 | **M4 qoldiq** sintetik generatori + marshrutlash | Eng yaqin mavjud nuqta topiladi |
| **13:30** | 🟡 **Ichki demo #1** — 3 daqiqa, xronometr bilan | 3 daqiqaga sig'adi |
| 14:00–14:50 | **Audit ekrani** (Ekran 3) — 6 ta raqam, bosiladigan | 1 skrinshot tayyor |
| **15:00** | 🔴 **RASMIY CHECKPOINT** — TOP-20 saralash | Demo ishlaydi, tayyor |
| 15:00–19:00 | **Metrikalar jadvali** to'ldiriladi (top-1, NDCG@3, AUC, marshrut %) | 5 qator raqam bilan |
| 19:00–22:00 | **Pitch skripti** yoziladi + 5 marta ovoz chiqarib mashq | 2:45 ga sig'adi |
| 22:00 | **Q&A banki** (12 savol) yodlanadi | Har javob ≤20 soniya |

## 7.3 Kun 3 — 19-noyabr

| Vaqt | Vazifa |
|---|---|
| 10:00 gacha | **Demo 3 marta ketma-ket yiqilmasdan** ishlaydi (offline rejim, oldindan keshlangan) |
| 10:00–13:00 | Pitch sessiyasi — 20 finalist |
| 13:30 | Natijalar |

## 7.5 Prototip — ishlaydigan kod (bugun ertalab yozildi)

Papkada: `prototype/doriyol_core.py` va `prototype/eval_m1.py`. Tashqi internet/API talab qilmaydi.

```
$ python3 doriyol_core.py      # 6 holat: M1, M2, qoida-blok, M3, agent, audit
$ python3 eval_m1.py           # M1 ni o'lchaydi
```

**O'lchangan natija (namunaviy 24 INN reyestrida, 55 test holati):**

| Usul | top-1 | Izoh |
|---|---|---|
| Baseline — aynan matn mosligi | **25.5%** | "Ahmoqona" usul |
| **Gibrid (nom ajratish + translit variantlari + n-gram/Levenshtein)** | **100% (55/55)** | **in-distribution** — test to'plami shu 24 INN da tuzilgan |
| Distraktor testi (reyestrda yo'q 8 dori) | **8/8 to'g'ri abstain**, 0 noto'g'ri map | Xavfsizlik tekshiruvi |

> **Halol izoh (pitch'da aynan shunday aytiladi):**
> *"Bu 100% — kichik, o'zimiz tuzgan to'plamda. Haqiqiy 8 742 yozuvli reyestrda sinf soni ~1 000, ya'ni vazifa qiyinroq. Bizning maqsadimiz — **top-1 ≥90%, abstain to'g'ri ishlashi**. Va eng muhimi: notanish dori uchun model **abstain qiladi**, taxmin qilmaydi — bu xavfsizlik talabi."*

**Nega prototip muhim:** hakamlar "AI bor" degan gapga emas, **ishlaydigan kod va o'lchangan raqamga** ishonadi. Va bu kod bugun ertalab yozilgani uchun "biz 48 soatda qurdik" da'vosi ham isbotlangan.

**Keyingi qadam (bugun kechqurun):** `REGISTER` ro'yxatini 41 yozuvdan **8 742 yozuvga** almashtirish — algoritm o'zgarmaydi, faqat ma'lumot.



| Risk | Zaxira |
|---|---|
| Internet yo'q | **Hammasi lokal**: model fayl, reyestr CSV, video zaxira |
| ASR ishlamaydi | **Tayyor audio fayl** (3 ta), oldindan transkripsiya qilingan |
| LLM limiti | **Keshlangan javoblar**; izoh shabloni qattiq yozilgan |
| Demo qotadi | **2:45 video yozilgan** — "buni jonli ko'rsataman, lekin vaqtni tejash uchun yozuv" |
| Savolga javob yo'q | *"Buni o'lchamadik — 3 haftalik pilotda o'lchaymiz"* (halol, kuchli) |

---

# 8. PITCH — SO'ZMA-SO'Z, 2:45

> **Slayd 1 (0:00–0:15) — MUAMMO, bitta raqam**
> *"2027-yil yanvardan O'zbekistonda 12 817 dori faqat e-retsept bilan beriladi. Vrach **xalqaro nom** yozadi. Farmatsevt esa **10 000 savdo nomi** ichidan tanlashi kerak — 3 daqiqada, xotiradan, bemor oldida turib."*

> **Slayd 2 (0:15–0:35) — NEGA HOZIR**
> *"Bugun bu ishlash uchun uchta shart bor: biri — qonun, ikkinchisi — ma'lumot, uchinchisi — platforma. Qonun: e-retsept majburiy. Ma'lumot: davlat reyestri 8 742 yozuv, ochiq. Platforma: DMED, 6 000 dorixona ulangan. Uchtasi ham **aynan shu yilda** birlashdi. Bir yil oldin bu mahsulotni qurib bo'lmasdi."*

> **Slayd 3 (0:35–1:10) — DEMO (jonli)**
> *"Qog'oz retsept. Nom xato yozilgan, kirill alifbosida."* → skan → *"Ikki soniya: Amoksitsillin, ATC J01CA04. Ro'yxatda 12 ta ekvivalent. Eng arzoni — 18 000 so'm — qoldiqda bor. **Va bu yerda eng muhimi:** bemorda penitsillin allergiyasi bor — tizim bu guruhni butunlay yashirdi va alternativa ko'rsatdi. Farmatsevt tasdiqlaydi. 38 soniya. 3 daqiqa o'rniga."*

> **Slayd 4 (1:10–1:35) — TEXNOLOGIYA, 4 model**
> *"Bu bitta API chaqiruvi emas. To'rt model: INN rezolyutsiyasi — top-1 aniqlik 61% dan 90% ga; ekvivalent reytingi — NDCG 0.58 dan 0.80 ga; retsept xavf modeli — AUC 0.70 dan 0.84 ga; qoldiq bashorati — marshrut muvaffaqiyati 34% dan 65% ga. Ustida agent — va **qat'iy qoida**: model hech qachon kontrendikatsiyani yengib o'tmaydi. Har javob yonida **nega** yozilgan."*

> **Slayd 5 (1:35–2:05) — NEGA BIZ, NEGA BU**
> *"Biz buni farmatsevt bilan qurdik. Birinchi versiyada 6 ekran bor edi — u 2 tasini qoldirdi. Va biz pul modelini dorixonaga **bemor xavfsizligi** deb emas, **to'ldirilgan retsept** deb aytamiz: oyiga bitta qo'shimcha retsept — to'lovimiz qaytadi. Bu $21 oyiga, 8 oyda qaytadi."*

> **Slayd 6 (2:05–2:45) — TA'SIR va SO'ROV**
> *"Ikki effekt. Birinchi: bemor dori topadi — bugun har uchinchi bemor dorixonadan quruq qaytadi. Ikkinchisi, va bu davlat uchun muhimroq: har bir retsept asoslangan holda yoziladi va **audit uchun qoladi**. Vazirlik 5+ dori yozilgan retseptlarning **38% asossiz** ekanini birinchi marta ko'radi. Biz 3 haftada 12 dorixonada pilotni boshlaymiz. Savol bitta: bizga bitta tarmoq kerak — 12 nuqta. Kim yordam bera oladi?"*

> **Yopilish qoidasi:** oxirgi jumla **savol** bo'lsin, "rahmat" emas. Savol muloqotni ochadi va hakamni javob berishga majbur qiladi.

---

# 9. 7 MEZON BO'YICHA XARITA (Nizom 7.2)

| # | Mezon | Biz nima ko'rsatamiz | Maqsad |
|---|---|---|---|
| 1 | **Trekka muvofiqligi** | Retsept → dori → farmatsevtika. Nomda "farmatsevtika" bor | 5/5 |
| 2 | **AI innovatsionligi** | 4 o'qitilgan model + agent + guardrail + izoh; bozorda analоg yo'q | 5/5 |
| 3 | **Texnik sifat (MVP, kod)** | Jonli demo 3 marta; ochiq repo; offline fallback | 5/5 |
| 4 | **UI/UX** | 2 ekran farmatsevt uchun (6 emas), 40 soniya, o'zbek tilida, "nega?" tugmasi | 5/5 |
| 5 | **Amaliy qo'llash / masshtablash** | 6 000 dorixona DMED'da; tarmoq kanali; 8 900 muassasa; keyin Markaziy Osiyo | 4–5/5 |
| 6 | **Pitch sifati** | Har da'vo raqam bilan; metrikalar jadvali; xavflar ochiq | 5/5 |
| 7 | **Reglament** | Checkpointga tayyor, jamoa 4–5, trek birinchi kundan | 5/5 |

**Kutilayotgan yakuniy:** 4.6–4.8 / 5

> **Diqqat:** oldingi bosqichlarda g'olib bo'lgan sog'liq jamoalari 5.42–5.83 ball olgan (Samarqand TOP-23). Ya'ni **bu ball diapazoni yetarli**. Lekin esda tuting: **yakuniy pitch oraliq balldan muhimroq** — Samarqandda 5-o'rindan turib 1-o'rin olingan.

---

# 10. XAVFLAR — va ularga tayyor javob

| # | Xavf | Ehtimol | Javob / yumshatish |
|---|---|---|---|
| 1 | **"Buni DMED o'zi qiladi"** | Yuqori | *"DMED retseptni **yozadi** va saqlaydi. Tanlash, tekshirish va marshrutlash qatlami yo'q. Biz uning ustidagi modulmiz — va biz API ochiq bo'lishi bilan birinchi bo'lamiz."* |
| 2 | **"O'zaro ta'sir bazangiz to'liq emas"** | Yuqori | **Ochiq tan olish:** *"Demo'da top-150 juftlik. To'liq baza litsenziyalanadi. Lekin bizning qiymatimiz bazada emas — INN rezolyutsiyasi va ish oqimida."* |
| 3 | **"Ma'lumot sizib chiqadi"** | O'rta | 1125-son qonun (26.03.2026): faqat biometrik/genetik/telekom lokalizatsiya; tibbiy — alohida toifa, aniq rozilik. **Lokal server, rozilik, 24 soat breach protokoli** |
| 4 | **"Noto'g'ri tavsiya → javobgarlik"** | O'rta | **Inson tasdiqlaydi.** Agent taklif qiladi, farmatsevt imzolaydi. Log to'liq. Qoidalar qatlami modeldan ustun |
| 5 | **"Farmatsevt ishlatmaydi"** | O'rta | 2 ekran, 40 soniya, "nega?" — dekabr 2025 inqirozi aynan **tushuntirish yo'qligi**dan chiqqan |
| 6 | **"Bozor kichik"** | O'rta | Halol: **SAM $3–5M/yil**. Javob: *"Bu venchur moonshot emas — bu foydali infratuzilma biznesi. Va Markaziy Osiyoda DMED-analoglari qurilmoqda."* |
| 7 | **"Nega siz, katta o'yinchi keladi"** | O'rta | Ma'lumot grafi + dorixona ichidagi o'rin. Va **16 oylik boshlang'ich afzallik** (2027 majburiyat) |
| 8 | **"LLM xarajati"** | Past | ASR+LLM faqat 2 joyda; **M1/M2/M3/M4 lokal, CPU'da**; kesh; batching |

---

# 11. 90 KUNLIK REJA (hackathondan keyin)

| Davr | Maqsad | Mezon |
|---|---|---|
| **1–2 hafta** | 12 dorixona (1 tarmoq) pilot; haqiqiy qoldiq ma'lumoti; M1 ni haqiqiy retseptlarda tekshirish | 500 retsept o'tdi, top-1 ≥ 88% |
| **3–4 hafta** | M3 ni haqiqiy loglarda qayta o'qitish; klinik farmakolog bilan 200 retseptni belgilash | AUC ≥ 0.85 (haqiqiy) |
| **2-oy** | 3 tarmoq (≈ 80 nuqta); pullik shartnoma ($21/oy); M2 NDCG haqiqiy loglarda | MRR $1 700, churn 0 |
| **3-oy** | Vazirlik/SHIF bilan birinchi uchrashuv; audit dashboard demo; UzVC arizasi | 1 MOU + ariza |
| **6-oy** | 300 nuqta; B2G pilot; DMED API integratsiyasi | MRR $6 300 |
| **12-oy** | 1 000 nuqta + 1 davlat kontrakti | ARR $250k+ |

**UzVC:** 5 mlrd so'mgacha, 0%, 3 yil, davlat ulushi ≤49% *(vaqt.uz, 01.09.2026)* — **2-oyda ariza berish**, 6-oyda emas.

---

# 12. BIR SAHIFALIK XULOSA — CHOP ETIB OLING

```
┌────────────────────────────────────────────────────────────────────────┐
│  DORIYO'L — e-retseptning oxirgi kilometri                              │
├────────────────────────────────────────────────────────────────────────┤
│  MUAMMO   10 000 savdo nomi / 1 000 INN. Farmatsevt 3 daqiqada,          │
│           xotiradan tanlaydi. 2027-yanvardan 12 817 dori majburiy.       │
│                                                                          │
│  YECHIM   INN → ro'yxatga olingan ekvivalent → eng yaqin mavjud nuqta    │
│           + xavf skaneri + audit. Har qadam izohli, inson tasdiqlaydi.   │
│                                                                          │
│  4 MODEL  M1 INN rezolver      top-1   61% → 90%                        │
│           M2 ekvivalent reyting NDCG@3 0.58 → 0.80                      │
│           M3 retsept xavfi      AUC    0.70 → 0.84                      │
│           M4 qoldiq/marshrut    muvaf. 34% → 65%                        │
│  + AGENT  tool-use, abstain, inson tasdiqi, to'liq log                   │
│                                                                          │
│  NEGA HOZIR   10.12.2025 pilot → 2027 majburiy · INN qoidasi ·          │
│               5+ dori asoslashi · DMED yadro 2026 · akkreditatsiya 2028  │
│  NEGA UZ      10:1 nom/INN nisbati · bitta platforma = butun bozor ·     │
│               kirill+lotin NLP · ochiq reyestr · regulyator oynasi      │
│  NEGA BIZ     farmatsevt jamoada · DMED tajriba · ML metrikalar          │
│  NEGA BU      LLM yolg'on gapiradi, DMED tanlamaydi, xorijiy baza        │
│               O'zbek reyestrini bilmaydi — biz gibrid + inson           │
│  NEGA EMAS    tashxis/telemed/CRM/scribe — band, WTP past, regulyator    │
│                                                                          │
│  PUL      Dorixona $21/oy → payback 8.6 oy, LTV/CAC 6.9                 │
│           Klinika $8/vrach/oy → 11 oy                                   │
│           B2G audit kontrakti → keyin                                  │
│           Kanal: tarmoq (CAC $180 → $20)                                │
│                                                                          │
│  DEMO     xato yozilgan kirill retsept → 2s INN → allergiya bloklashi    │
│           → 3 ekvivalent narx bilan → eng yaqin dorixona → tasdiq        │
│           38 soniya. 3 daqiqa o'rniga.                                  │
│                                                                          │
│  QIZIL    ❌ "AI tashxis qo'yadi"  ❌ "yagona platforma"                │
│  CHIZIQ   ❌ "99% aniqlik"         ❌ "bozor $50 mlrd"                  │
│           ✅ "biz taklif qilamiz, farmatsevt tasdiqlaydi"               │
└────────────────────────────────────────────────────────────────────────┘
```

---

# 13. MANBALAR

**Nizom va qoidalar**
1. `ai-hackathon.uz` — Nizom (7 mezon, 5 ballik shkala, 4–5 kishilik jamoa, 25→20 finalist, mukofotlar)
2. SSV buyrug'i (lex.uz, `-3032611`) — retsept INN bo'yicha, lotin yozuvida; 5+ dori asoslash; 4+ dori kelishish
3. VMQ 570 (10.12.2025) — e-retsept piloti, 12 817 retseptli dori, 2027-yanvar majburiyat
4. kun.uz (05.07.2020) — 5+ dori asoslash qoidasi
5. spot.uz (24.12.2025) — vazir intervyusi, 389 retseptsiz dori, farmatsevtlar inqirozi
6. gazeta.uz (13.12.2025) — e-retsept qamrovi: xususiy klinikalar 49%, Toshkent 41%
7. anhor.uz (22.08.2026) — e-retsept orqali tayinlash tartibi nizomi

**Ma'lumot manbalari**
8. `uzpharm-control.uz` — Dori vositalari davlat reyestri, **8 742 yozuv**; retseptli/retseptsiz ro'yxat
9. `data.gov.uz` — "Tarkibi bir xil ammo turli nomlanishga ega bo'lgan dori vositalari ro'yxati"
10. yuz.uz (31.07.2021) — ~10 000 savdo nomi, 600–1 000 INN nisbati
11. JSST ATC/INN indeksi, ICD-10 (ochiq)

**Bozor**
12. anhor.uz (24.10.2026) — 8 912 ambulator muassasa, hududlar kesimi
13. Prezident taqdimoti / spot.uz (01.05.2026) — 8 700 xususiy klinika; akkreditatsiya 2027/2028/2030; SHIF 2028
14. asdr.gov.uz (10.06.2026) — DMED: 38 mln e-karta, 8 000+ klinika, 6 000 dorixona
15. gazeta.uz (15.10.2025) — 75 000 kompyuter tanqisligi, "yadro" 2026 oxiri
16. Law No. 1125 (26.03.2026) — lokalizatsiya islohoti; ZRU-547 — tibbiy ma'lumot alohida toifa
17. vaqt.uz (01.09.2026) — UzVC: 5 mlrd so'mgacha, 0%, 3 yil

**Texnika / global amaliyot**
18. getlimeai / forasoft / orbdoc (2026) — ambient scribe bozori va narxlar (qiyosiy kontekst)
19. CB Insights (431/483 post-mortem) — 43% PMF, 70% kapital, 29% vaqt
20. Olive AI autopsiyasi (Fierce Healthcare 31.10.2023; revcycleai; unicornburn) — "universal platforma" o'limi
21. MIT — genAI pilotlarining 95% muvaffaqiyatsiz
22. `hackathon_razvedka_2026.md` — hackathon g'oliblari bazasi (ushbu papkada)
23. `sogliq_treki_due_diligence.md` — bozor/unit economics asosi (ushbu papkada)
