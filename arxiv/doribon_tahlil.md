# DORIBON
## Retseptdan qo'liga — 40 soniyada
### MUAMMO → YECHIM → QANDAY → ISHLAYDI

**Sana:** 17-noyabr 2026 · **Trek:** Sog'liqni saqlash va farmatsevtika
**Format:** Nizom mezoni #1 (trekka muvofiqlik) va #2 (AI innovatsionligi) bo'yicha **to'liq asoslangan yechim hujjati**
**Tuzilish:** talab qilingan tartibda — **PROBLEM → SOLUTION → HOW → WORKING**

---

# QISM 0 · NOM — nega aynan "DORIBON"

## 0.1 Nomning ma'nosi

> **DORIBON = "dori" + "-bon"** (qo'riqchi, parvarish qiluvchi)
> O'zbek tilidagi **bog'bon** so'zi bilan bir qolipda: *bog'bon — bog'ni parvarish qiladi; **doribon — dorini parvarish qiladi.***

Nom uch xil ma'noni bir vaqtda beradi:

| Qatlam | Ma'no | Nega muhim |
|---|---|---|
| **To'g'ridan-to'g'ri** | Dori + qo'riqchi = **dori qo'riqchisi** | Mahsulot nima qilishini bir so'zda aytadi |
| **Kultural** | **bog'bon** qolipi — o'zbek tiliga xos, samimiy, esda qoladigan | "Sun'iy" texnik nom emas; tilga singib ketadi |
| **Vazifaviy** | **Qo'riqlash** = xavfsizlikni tekshirish, xatoni to'sish, iz qoldirish | Mahsulotning butun mantiqi shu so'zda |

## 0.2 Pitch'da aytiladigan bir jumla

> *"**Bog'bon** o'z bog'idagi har bir ko'chatni taniydi — qaysi biri suv talab qiladi, qaysi biri kasal. **Doribon** — 8 742 dori ichidan bemorga kerakli bittasini taniydi va xato qilishga yo'l qo'ymaydi."*

Bu jumla 8 soniyada aytiladi va hakam eslab qoladi. **Nom — pitch'ning eng qisqa qismi, lekin eng ko'p esda qoladigan qismi.**

## 0.3 Nega boshqa nomlar emas — rad etilgan 6 variant

| Variant | Ma'nosi | Nega rad etildi |
|---|---|---|
| ~~DoriYo'l~~ | "dorining yo'li" | Chiroyli, lekin **passiv** — "yo'l" hech narsa qilmaydi. Mahsulot esa **faol qo'riqchi** |
| ~~Shifo~~ | shifo, tuzalish | **Band** (`shifo.uz` mavjud, tibbiy portal) |
| ~~Tabib~~ | tabib, davolovchi | **Vrach** ma'nosini beradi → mahsulot **farmatsevt** uchun; pozitsiya chalkashadi |
| ~~Davo~~ | davo, dori | Juda umumiy; brend kuchi nolga teng; qidiruvda yo'qoladi |
| ~~Tarozi~~ | tarozi (tanlash/tortish metaforasi) | Chiroyli, lekin **3 bo'g'in**, talaffuzda og'ir; rus tilida ham qiyin |
| ~~Zirak / Zukko~~ | ziyrak, aqlli | **ZukkoMind AI** allaqachon bor (Jizzax bosqichi g'olibi) — chalkashlik |
| ~~KinesteX, MedIQ, DARDLASHAI~~ | — | Bosqich g'oliblari **allaqachon egallagan** — takrorlash = "ko'rilgan" taassurot |

## 0.4 Brend arxitekturasi

```
DORIBON
├── tagline      "Retseptdan qo'liga — 40 soniyada"
├── shior (UZ)   "Har bir dori o'z qo'liga"
├── shior (RU)   "От рецепта до руки — за 40 секунд"
├── ovoz ohangi   xotirjam, ishonchli, ortiqcha emotsiyasiz
│                (tibbiy mahsulot — "vau", "super", "inqilobiy" YO'Q)
└── vizual        yashil (xavfsizlik) + oq (aniqlik)
                  belgi: qalqon ichida dori kapsulasi
```

**Bitta qoida:** barcha ekranlarda, pitch'da, kodda, fayl nomlarida — **faqat "Doribon"**. Nom izchilligi professional taassurotning yarmi.

---

# QISM I · PROBLEM (muammo aniq nimada)

## 1.1 Muammo bir gapda — va u nima EMAS

> **Muammo:** Vrach e-retseptni faqat **xalqaro nom (INN)** bo'yicha yozadi. Farmatsevt esa shu INN ni O'zbekistonda ro'yxatga olingan **~10 000 savdo nomi** ichidan haqiqiy mahsulotga aylantirishi kerak — 3 daqiqada, xotiradan, bemor oldida turib, qoldiq/narx/allergiya/tashxisni hisobga olib. Buning uchun **hech qanday vosita yo'q**.

**Muammo nima EMAS** (bu chegara juda muhim, chunki noto'g'ri chegara = noto'g'ri mahsulot):

| ❌ Bu muammo emas | Nega |
|---|---|
| "Shifokorlar kam" | Kadr masalasi — bizning mahsulot emas |
| "Bemorlar o'zini o'zi davolaydi" | Xulq-atvor masalasi — tizimli yechim talab qiladi |
| "Dorilar qimmat" | Narx siyosati — referens narx tizimi bor |
| "Klinikada navbat" | Boshqa bozor, boshqa o'yinchilar (Med24, 1Clinic) |
| "AI tashxis qo'yishi kerak" | Regulyator to'sig'i eng katta, klinik isbot yo'q, 3 bosqichda band |

## 1.2 Muammoning ildiz sabablari (root cause) — 5 ta

| # | Ildiz sabab | Mexanizm | Dalil |
|---|---|---|---|
| **R1** | **Nomlar ko'pligi (nomenclature explosion)** | 1 INN → o'rtacha **10–16 savdo nomi**; har birida 2–5 doza × 3–6 shakl = **30–80 variant** | ~10 000 savdo nomi, 600–1 000 INN *(yuz.uz; davlat reyestri 8 742 yozuv)* |
| **R2** | **Majburiy INN qoidasi, vositasiz** | Retsept faqat INN bo'yicha, lotin yozuvida; savdo nomi taqiqlangan. Lekin INN→mahsulot xaritasi **xizmat sifatida mavjud emas** | SSV buyrug'i (lex.uz) |
| **R3** | **Ikki alifbo, ikki til** | Nom kirill va lotin yozuvida; qo'llash usuli davlat tilida; xato imlo odatiy | SSV buyrug'i |
| **R4** | **Qoldiq va narx ko'rinmas** | Bemor 3–4 dorixonaga yuradi; qaysi dorixonada bor — hech kim bilmaydi | 6 000 dorixona DMED'da, lekin **qoldiq moduli yo'q** |
| **R5** | **Nazorat qog'ozda** | 5+ dori asoslashi shart, lekin asoslash **tekshirilmaydi va yozilmaydi** | SSV buyrug'i; xususiy klinikalarning 49% e-retseptda |

**Muhim:** R1–R5 — **texnik** sabablar. Ular **siyosiy emas, muhandislik** masalalari. Ya'ni **yechiladi**.

## 1.3 Muammo kim uchun qanchalik og'riqli — 3 foydalanuvchi

| Foydalanuvchi | Bugungi harakat | Vaqt | Xato narxi |
|---|---|---|---|
| **Farmatsevt** | INN o'qiydi → xotiradan 3–5 nomzod → qoldiqni qidiradi → narxni aytadi → tekshiradi | **3–5 daqiqa**, kuniga **60–120 marta** | Noto'g'ri ekvivalent → qaytarish, shikoyat, **farmakonazorat tekshiruvi** |
| **Vrach** | INN yozadi → 5+ dori bo'lsa asoslaydi → bemorni dorixonaga yuboradi | **1–2 daqiqa** + asoslash | Asossiz antibiotik → **rezistentlik**, keyin tekshiruv |
| **Bemor** | Retsept oladi → dorixonalarga yuradi | **20–60 daqiqa**, **1–3 dorixona** | Dori topmaydi → **davolash uziladi**; pul va ishonch yo'qoladi |

**Oqibat (makro):** antibiotiklarni nazoratsiz qo'llash → rezistentlik; surunkali kasallikda davolash uzilishi → asorat → **davlat xarajati o'sadi**. Bu **pul masalasi**, "qulaylik" masalasi emas.

## 1.4 "Shu paytgacha nima qilindi" — rasmiy urinishlar xronologiyasi

| Sana | Nima qilindi | Nima uchun yetarli bo'lmadi |
|---|---|---|
| **2019** | "Shaxsga doir ma'lumotlar" qonuni (ZRU-547) | Ma'lumot uchun asos yaratdi, lekin **vosita emas** |
| **2021** | Lokalizatsiya talabi (ZRU-666) | Infratuzilma cheklovi qo'shildi (2026-da yumshatildi) |
| **2020** | INN bo'yicha retsept qoidasi | **Qoida** berildi, **vosita** berilmadi |
| **2022** | Reimbursement piloti (Sirdaryo, 5 NCD) | To'lov mexanizmi, tanlash emas |
| **2023** | Dori reyestri raqamlashtirildi | **PDF/veb reyestr** — mashina o'qiydigan xizmat emas |
| **2024** | Reimbursement kengaytirildi (WHO bahosi) | Xaridor yaratildi, vosita yo'q |
| **10.12.2025** | **E-retsept piloti** (Toshkent + 15 tuman, 12 817 dori) | Farmatsevtga **yangi yuk**, vosita bermadi |
| **dek 2025** | **Inqiroz:** farmatsevtlar retseptsiz dorilarni ham bermadi; vazir shaxsan aralashdi, 389 retseptsiz dori ro'yxati e'lon qilindi | Tizim **tushuntirmadi** → odamlar qo'rqdi |
| **2025** | Referens narx tizimi: bir ishlab chiqaruvchining bir xil tarkibli dorilariga **eng past narx** qo'llanadi | Narx bosimi yaratildi, **tanlash vositasi yo'q** |
| **24.11.2025** | Ro'yxatga olish tartibi yangilandi (738-son) | Reyestr sifati oshdi — **xizmat qatlami yo'q** |
| **2026 oxiri** | DMED "elektron sog'liqni saqlash yadrosi" rejalashtirilgan | **Yadro = ulanish**, tanlash emas |
| **yanvar 2027** | **E-retsept majburiy** | Deadline yaqinlashadi, vosita yo'q |

> **Xulosa:** davlat **qoidani, to'lovni, reyestrni va platformani** qurdi. **Uchta bo'g'in yetishmayapti:** (1) INN→mahsulot rezolyutsiyasi, (2) xavfsizlik tekshiruvi, (3) qoldiq bo'yicha marshrutlash. **Aynan shu uchtasi — mahsulotimiz.**

---

# QISM II · OLDINGI YECHIMLAR — TO'LIQ AUDIT

> Uch toifa: **(A)** eski/meros yechimlar, **(B)** eski lekin innovatsion standartlar, **(C)** hozirgi startup va vendor yechimlari. Har biri: nima qiladi → nimani hal qilmaydi → nega O'zbekistonda ishlamaydi.

## 2.1 (A) ESKI / MEROS YECHIMLAR

| # | Yechim | Nima qiladi | Nimani hal qilmaydi | O'zbekistonda holat |
|---|---|---|---|---|
| A1 | **Qo'lyozma retsept** | Vrach yozadi | INN→nom, qoldiq, xavfsizlik, audit — **hech biri** | 2027-dan yo'qoladi |
| A2 | **Farmakopeya / davlat reyestri (qog'oz)** | Ro'yxatni beradi | Qidiruv, moslashtirish, narx — **yo'q** | 8 742 yozuv veb/PDF'da |
| A3 | **Vidal / RLS / "Tibbiyot qo'llanmasi" (kitob)** | Dori tavsifi, doza, ta'sir | INN→mahalliy savdo nomi xaritasi **yo'q**; yangilanmaydi | Keng ishlatiladi, lekin **qoldiqni bilmaydi** |
| A4 | **Klinik protokollar (qog'oz)** | Nima yozish kerakligini aytadi | **Yozilganini tekshirmaydi** | Mavjud, lekin retseptga ulanmagan |
| A5 | **Formulyar ro'yxat** | Muassasa dorilari | Muassasa ichida qoladi; dorixonaga chiqmaydi | Qisman |
| A6 | **Excel / daftar (dorixona qoldig'i)** | Qoldiq hisobi | INN bilan bog'lanmagan; real vaqt emas | **Asosiy amaliyot** |
| A7 | **Telefon qo'ng'irog'i** ("bor-yo'qini so'rash") | Qoldiqni aniqlaydi | Vaqt, xato, masshtablanmaydi | **Eng ko'p ishlatiladigan "yechim"** |

> **A-toifa xulosasi:** meros yechimlarning hammasi **"ma'lumot beradi, xizmat bermaydi"**. Ular INN ni biladi yoki qoldiqni biladi — **ikkalasini bir vaqtda bilmaydi**.

## 2.2 (B) ESKI LEKIN INNOVATSION STANDARTLAR — bu eng muhim bo'lim

> Bular **20–50 yil oldin** yaratilgan, lekin hanuz dunyoning eng yaxshi amaliyoti. Ular **bizning poydevorimiz** — noldan ixtiro qilmaymiz.

### B1 · ATC/INN tizimi (JSST, 1970-yillar)

| Parametr | Ma'lumot |
|---|---|
| Nima | Dorilarni **anatomik-terapevtik-kimyoviy** ierarxiyaga joylashtiruvchi xalqaro tasnif + xalqaro patentlanmagan nom |
| Qamrov | ~6 000 kod, 5 daraja (A → A02 → A02B → A02BC → A02BC01) |
| Nimani hal qiladi | **"Bu dorilar bir xilmi?"** degan savolga rasmiy javob. INN — qonuniy nom |
| Nimani hal qilmaydi | **Mahalliy ro'yxatga olingan mahsulotga bog'lamaydi**; doza/shakl/narx/qoldiq yo'q |
| O'zbekistonda | INN qonun bilan majburiy qilindi — **lekin ATC kodi retseptda talab qilinmaydi** va tizimli ishlatilmaydi |

### B2 · RxNorm (AQSh NLM, 2005) — **eng yaqin analog**

| Parametr | Ma'lumot |
|---|---|
| Nima | **Normallashtirilgan dori nomenklaturasi.** Har kontseptga `RxCUI` identifikatori |
| Tuzilma | Grafik: `Ingredient (IN)` → `Ingredient+Strength (SCDC)` → `Ingredient+Form (SCDF)` → `Ingredient+Strength+Form (SCD)` → `Branded (SBD)` |
| Isbot | 19 743 real e-retseptda **qamrov 99.995%**; avtomatik bog'lash **98.8%**; 6 oyda kontseptlarning 8.1% i yangilangan |
| API | Bepul REST: `getApproximateMatch` (fuzzy qidiruv), `getRelatedByType` (ierarxiya), `getNDCProperties` (billing) |
| Hal qiladi | **Aynan bizning R1 va R3** — nom ko'pligi va imlo varianti |
| Hal qilmaydi | **Narx, qoldiq, qonuniy qoplam** — RxNorm'da **yo'q** (aniq hujjatlashtirilgan chegara). Faqat AQSh dorilari |
| O'zbekistonda | **YO'Q.** Eng katta bo'shliq. RxNorm O'zbek reyestrini bilmaydi |

> **Strategik xulosa:** RxNorm — **arxitektura namunasi**, mahsulot emas. Biz xuddi shu g'oyani **O'zbek reyestri + narx + qoldiq** ustida qurmoqchimiz. Bu "ixtiro" emas — **ko'chirilgan eng yaxshi amaliyot**, mahalliy ma'lumot bilan. Va bu **kuchli "nega ishlaydi" dalili**.

### B3 · Generik almashtirish siyosati (Yevropa, 1990–2000-yillar)

| Parametr | Ma'lumot |
|---|---|
| Nima | Farmatsevtga **arzon ekvivalent berish huquqi/majburiyati**; ba'zi mamlakatlarda — **majburiy almashtirish** |
| Nimani hal qiladi | Narx bosimi: bemor va davlat tejamkorligi |
| Nimani hal qilmaydi | **"Qaysi ekvivalent?"** degan savolni farmatsevtdan olib tashlamaydi — faqat huquq beradi |
| O'zbekistonda | **Referens narx tizimi** (2025): bir ishlab chiqaruvchining bir xil tarkibli dorilari uchun **eng past narx** qo'llanadi → **almashtirish iqtisodiy jihatdan majburiy** |
| Xulosa | Siyosat bor, **vosita yo'q** |

### B4 · E-retsept infratuzilmasi (Surescripts, AQSh, 2001–)

| Parametr | Ma'lumot |
|---|---|
| Nima | Retseptni vrach → dorixona → to'lovchi orasida uzatuvchi **milliy tarmoq** |
| Nimani hal qiladi | Uzatish va **eligibility** (qoplama) tekshiruvi |
| Nimani hal qilmaydi | **INN→mahsulot tanlashni**; bu alohida qatlam (RxNorm + vendor baza) |
| O'zbekistonda | **DMED** xuddi shu rolni o'ynaydi — lekin **tanlash qatlami yo'q** |

### B5 · Klinik qaror qo'llab-quvvatlash (CDSS) — **va uning mashhur muvaffaqiyatsizligi**

| Parametr | Ma'lumot |
|---|---|
| Nima | Dori o'zaro ta'siri, allergiya, doza ogohlantirishlari |
| **Halokatli dalil** | Ogohlantirishlar **49–96% hollarda e'tiborsiz qoldiriladi / bekor qilinadi**; jamlangan ko'rsatkich **96.2%**; ba'zi tadqiqotlarda **98%** |
| Sabab | **Past spetsifiklik** (ko'p noto'g'ri signal), noaniq matn, ish oqimini buzish → **"alert fatigue"** |
| Eng yomoni | Bir tadqiqotda bekor qilingan ogohlantirishlarning **96.8% i klinik farmakolog tomonidan "asosli" deb topilgan** — ya'ni **tizim noto'g'ri signal bergan, vrach emas** |
| **Biz uchun saboq** | **Interruptiv (to'xtatuvchi) ogohlantirish yasash = o'lim.** M3 modelini **boshqacha** qurish shart |

> **B5 — bu hujjatning eng muhim topilmasi.** Ko'p jamoalar "AI ogohlantiradi" deb chiqadi. 20 yillik global ma'lumot: **bunday ogohlantirishlar 96% e'tiborsiz qoladi**. Bizning arxitektura shu sababli **butunlay boshqacha** — 4.3-bo'lim.

## 2.3 (C) HOZIRGI STARTUP VA VENDOR YECHIMLARI

### C1 · Global — to'g'ridan-to'g'ri raqobatchi mantiq

| Kompaniya | Mamlakat | Yig'ilgan | Nima qiladi | Biz uchun ma'nosi |
|---|---|---|---|---|
| **Truemeds** | Hindiston | — | Retseptni AI bilan **generik almashtiruvchilarga** moslashtiradi, 50 000+ dorixona, **72% gacha tejamkorlik** | 🟢 **Model isbotlangan** — lekin Hindiston bozori, O'zbek reyestri yo'q |
| **Synapse Medicine (MedGPT)** | Fransiya | **$39M** | Retsept xavfsizligi AI: o'zaro ta'sir, kontrendikatsiya, doza, personalizatsiya | 🟢 Texnik yo'nalish to'g'ri; 🇺🇿 reyestr, INN, narx, qoldiq yo'q |
| **Latent** | AQSh | **$80M Series A, ~$600M baho**, $20M+ ARR, 45 sog'liq tizimi | **Agent** — oldindan ruxsat (prior auth) va hujjat jarayonini avtomatlashtiradi | 🟢🟢 **Agent arxitekturasi venture tomonidan tasdiqlangan** ($600M baho) |
| **Queue** | AQSh | **$12.6M seed** | To'liq avtonom robot dorixona: 600 tabletka/daqiqa, **dispens narxini 96% ga kamaytirish** | 🟠 Hardware, kapital talab qiladi; **regulyator to'sig'i** (shtat qonuni farmatsevtni talab qiladi) |
| **DoseMe / DoseMeRx** | Avstraliya | — | Farmakokinetik **doza optimizatsiyasi** (Bayesian PK), $3 500/oy | 🟢 Tor, chuqur, klinik jihatdan qimmatli; bizning keyingi modul |
| **DrFirst / Surescripts** | AQSh | $79M / infratuzilma | E-retsept, medication history, eligibility | 🟠 Infratuzilma — **biz DMED bilan raqobatlashmaymiz** |
| **Waltz Health** | AQSh | $55.5M | Dori narxini solishtiruvchi qidiruv | 🟢 Narx qatlami; lekin klinik tekshiruv yo'q |
| **Alto / Capsule / Truepill** | AQSh | ~$2 mlrd (birgalikda) | Raqamli dorixona + yetkazish | 🔴 **"Dorixona bo'lish" — yutqazilgan model.** "Digital pharmacy shakeout": CVS/Walgreens bilan raqobat, kapital yondi |

### C2 · O'zbekiston — mavjud o'yinchilar

| O'yinchi | Nima qiladi | Nimani **qilmaydi** (bizning bo'shliq) |
|---|---|---|
| **DMED (Uzinfocom)** | E-karta, e-poliklinika, **e-retsept moduli**, 38 mln aholi, 6 000 dorixona | **Tanlamaydi.** Retseptni saqlaydi va uzatadi — INN→mahsulot, xavfsizlik, qoldiq yo'q |
| **uzpharm-control.uz** | Davlat reyestri (8 742 yozuv), retseptli/retseptsiz ro'yxat | **Fayl/veb** — API emas, xizmat emas |
| **data.gov.uz** | "Tarkibi bir xil, nomlanishi turlicha dorilar ro'yxati" | **Statik ro'yxat** — jonli tanlash, narx, qoldiq yo'q |
| **Med24.uz** | Klinika/shifokor agregatori, onlayn navbat, sharhlar | **Retsept darajasiga tushmaydi** |
| **1Clinic** | Xususiy klinika CRM/ERP | Klinika ichida; **dorixonaga chiqmaydi** |
| **Doctor Yan** | Tibbiy tasvirlash XAI (saraton) | Radiologiya — boshqa muammo |
| **Medvoice AI (AI500 2-o'rin)** | Tibbiy hujjatlashtirish | Hujjat, retsept emas |

> **C-toifa xulosasi:** O'zbekistonda **hech kim INN→mahsulot→qoldiq zanjirini** qilmayapti. DMED **birinchi yarmini** (yozish) qildi, **ikkinchi yarmi** (tanlash) bo'sh.

## 2.4 YAKUNIY AUDIT JADVALI — hamma yechim bir jadvalda

| Yechim | R1 nom ko'pligi | R2 INN majburiyati | R3 kirill/lotin | R4 qoldiq | R5 nazorat | O'zbek reyestri | Jonli | Narx |
|---|---|---|---|---|---|---|---|---|
| Qo'lyozma retsept | ❌ | ❌ | ❌ | ❌ | ❌ | — | — | — |
| Qog'oz reyestr / Vidal | 🟡 | 🟡 | 🟡 | ❌ | ❌ | 🟡 | ❌ | ✅ |
| Excel qoldiq | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | 🟡 | ✅ |
| Telefon qo'ng'irog'i | ❌ | ❌ | — | 🟡 | ❌ | — | ✅ | ✅ |
| ATC/INN (JSST) | 🟡 | ✅ | ❌ | ❌ | ❌ | ❌ | — | ✅ |
| **RxNorm** | ✅ | 🟡 | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Generik almashtirish siyosati | ❌ | ✅ | — | ❌ | ❌ | 🟡 | — | ✅ |
| Surescripts / e-retsept tarmog'i | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| CDSS ogohlantirishlari | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ✅ | ✅ |
| Truemeds | ✅ | 🟡 | ❌ | 🟡 | ❌ | ❌ | ✅ | ✅ |
| Synapse Medicine | 🟡 | 🟡 | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Latent | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ✅ | ✅ |
| DMED | ❌ | ✅ | 🟡 | ❌ | ❌ | ✅ | ✅ | ✅ |
| **DORIBON** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**O'qish qoidasi:** hech bir ustun "hamma yashil" emas. **Biz — birinchi "hamma yashil" qator.**

---

# QISM III · TALABGA JAVOB BERMAYDIGAN QISMLARNI OLIB TASHLASH

> Bu bo'lim **ataylab** yozilgan. Ko'p jamoalar hamma narsani va'da qiladi va shu bilan ishonchni yo'qotadi. Biz **nimani qilmasligimizni** aniq aytamiz.

## 3.1 OLIB TASHLANDI — 9 ta qaror va sabablari

| # | Olib tashlandi | Nega olib tashlandi | Dalil |
|---|---|---|---|
| **X1** | **"AI tashxis qo'yadi" funksiyasi** | Regulyator nuqtai nazaridan bu **tibbiy xizmat** → litsenziya, klinik sinov, mas'uliyat. Va bozorda band | Babylon bankrotligi; 3 bosqichda 1-o'rin egallangan; hakamlar orasida SSV vakili |
| **X2** | **Interruptiv (to'xtatuvchi) ogohlantirishlar** | **49–96% e'tiborsiz**; jamlangan 96.2%. Pop-up oynalar mahsulotni o'ldiradi | van der Sijs 2006; Weingart 2003; 2022 DDI CDSS tadqiqoti |
| **X3** | **To'liq o'zaro ta'sir bazasi (bizniki)** | Uni qurish 10+ yil va litsenziya talab qiladi; bizning qiymatimiz u yerda emas | FDB/Micromedex/Wolters Kluwer bozori. Demo'da top-150 juftlik, **halol aytiladi** |
| **X4** | **Bemorlar uchun B2C ilova (mustaqil)** | ARPU $2–5/oy, CAC yuqori, to'lash odati past. Bemor — **kanal**, xaridor emas | O'zbekistonda B2C monetizatsiya isbotlanmagan |
| **X5** | **Dorixona bo'lish / yetkazib berish** | Kapital yondiradi, CVS bilan raqobat. "Digital pharmacy shakeout" | Alto/Capsule/Truepill ~$2 mlrd, muammoli model |
| **X6** | **Parallel EHR / klinika CRM** | **DMED egasi davlat**, 1Clinic mavjud. Raqobat emas — **o'lim** | Olive AI: "universal platforma" → $902M yondi |
| **X7** | **Hardware (skaner, qurilma)** | 48 soatda ishonchli apparat qurilmaydi; sertifikatlash 6–12 oy | Forward Health: 3 200 va'da → **5** yetkazildi |
| **X8** | **ASR/ovoz (vrach nutqini yozish)** | Medvoice AI shu yo'nalishda; ASR xatosi o'zbek tibbiy nutqida yuqori; **WTP past** | AI500 2-o'rin; global scribe narxi $99–600, bizda to'lov yo'q |
| **X9** | **"Yagona AI tibbiy platforma" pozitsiyasi** | DMED shu. Bu jumla hakamlar uchun chiroyli, investor uchun o'lik | Olive autopsiyasi: "vision mahsulotdan uzilib ketdi" |

## 3.2 NIMA QOLDI — qat'iy qamrov (scope lock)

### ✅ QAMROVGA KIRADI (5 ta, boshqa hech narsa)

| # | Funksiya | Nega bu |
|---|---|---|
| **S1** | **INN → mahalliy mahsulot rezolyutsiyasi** (kirill/lotin, xato imlo) | R1, R2, R3 — qonun bilan majburiy, busiz jarayon to'xtaydi |
| **S2** | **Ekvivalent reytingi** (doza, shakl, bioekvivalentlik, narx, qoldiq) | Almashtirish iqtisodiy jihatdan majburiy (referens narx) |
| **S3** | **Xavfsizlik qatlami** — qoidalar + model, **lekin interruptiv emas** | R5; B5 saboqlari bilan qayta dizayn |
| **S4** | **Qoldiq ehtimoli va marshrutlash** | R4 — bemor 3 dorixona bo'ylab yurmasin |
| **S5** | **Audit yozuvi** (har qaror asoslangan, izohli) | R5 — vazirlik/SHIF uchun; **B2G daromad manbai** |

### ❌ QAMROVGA KIRMAYDI
Diagnostika · davolash tavsiyasi · klinika CRM · navbat · yetkazib berish · EHR · hardware · tibbiy turizm · sug'urta underwriting

> **Bu "scope lock" ni pitch'ning birinchi slaydida ayting.** Hakam "bu jamoa nima qilmasligini biladi" deb o'ylaydi — bu **ishonch belgisi**.

---

# QISM IV · SOLUTION (yechim aniq nima)

## 4.1 Yechim bir gapda

> **Doribon — DMED ustidagi bitta modul: INN bo'yicha yozilgan e-retseptni ro'yxatga olingan mahalliy mahsulotga aylantiradi, xavfsizlikni tekshiradi, eng yaqin mavjud dorixonani ko'rsatadi va har bir qarorni asoslab yozib qo'yadi — hammasi 40 soniyada, inson tasdig'i bilan.**

## 4.2 Uch qavatli qiymat (kim nimani oladi)

| Qavat | Kim | Nima oladi | To'lov |
|---|---|---|---|
| **L1** | **Farmatsevt** | 3–5 daqiqa → **40 soniya**; to'g'ri ekvivalent; qoldiq ko'rinadi | Dorixona: **$21/oy** |
| **L2** | **Vrach / klinika** | Asoslangan retsept; 5+ dori avtomatik asoslash; himoya | Klinika: **$8/vrach/oy** |
| **L3** | **Vazirlik / SHIF** | Retsept sifati paneli; asossiz antibiotik; akkreditatsiya dalili | Kontrakt |

## 4.3 XAVFSIZLIK QATLAMI — B5 saboqlari bilan qayta dizayn (eng muhim texnik qaror)

**Global xato (biz takrorlamaymiz):** pop-up ogohlantirish → 96% e'tiborsiz.

**Bizning dizayn — 4 ta farq:**

| # | Global amaliyot (buzuq) | Bizning yechim | Nega ishlaydi |
|---|---|---|---|
| 1 | **Interruptiv** pop-up | **Non-interruptiv**, natija ichida ko'rsatiladi | Ish oqimini buzmaydi → e'tiborsiz qoldirishga sabab yo'q |
| 2 | **Past spetsifiklik** (ko'p yolg'on signal) | **Precision-first**: faqat harakat talab qiladigan signallar. "Eslatma" darajasi **alohida**, aralashmaydi | 96% shovqin yo'qoladi |
| 3 | **"Model shunday dedi"** | **Har signal uchun huquqiy yoki klinik asos** ko'rsatiladi | Vrach nima uchun ogohlantirilayotganini biladi |
| 4 | **Bekor qilish sababi yozilmaydi** | **Har bekor qilish sababi majburiy + log** → model shundan o'rganadi | Tizim vaqt o'tishi bilan **spetsifiklashadi** — global tizimlar buni qilmaydi |

> **Pitch jumlasi:** *"Biz ogohlantirish tizimi qurmadik. Biz **qaror yozuvi** qurdik. Farqi shu: 20 yillik ma'lumot shuni ko'rsatadi — to'xtatuvchi ogohlantirishlarning 96 foizi e'tiborsiz qoladi. Bizning yondashuvda signal ish oqimini buzmaydi, lekin **iz qoldiradi** — va izni o'chirib bo'lmaydi."*

## 4.4 Chegara (halollik deklaratsiyasi)

| Da'vo | Haqiqat |
|---|---|
| "Tashxis qo'ymaymiz" | ✅ Faqat retsept darajasidagi mantiqiy/klinik tekshiruv |
| "O'zaro ta'sir bazamiz to'liq" | ❌ Demo: top-150 juftlik. To'liq baza — litsenziya |
| "Model 100% aniq" | ❌ Namuna reyestrda 100%, real reyestrda maqsad **≥90%** |
| "Qoldiq real vaqtda" | ❌ Hozir sintetik; tarmoq shartnomasidan keyin real |
| "Bemor ma'lumoti xavfsiz" | ✅ Aniq rozilik, lokal server, 24 soat breach protokoli (ZRU-547) |

---

# QISM V · HOW (qanday ishlaydi — mexanizm)

## 5.1 Jarayon — 7 qadam, har biri o'lchanadi

```
FARMATSEVT: retseptni skanlaydi / INN ni kiritadi
        │
        ▼
[1] M1 · REZOLYUTSIYA ──────────────── 0.8 s
    normalizatsiya (kirill→lotin, diakritika)
    → nom ajratish (doza/shakl tokenlarini olib tashlash)
    → translit variantlari (max 60)
    → n-gram kosinus + Levenshtein + prefix bonusi
    → INN + ATC + ishonch darajasi
    ├── ishonch < 0.72 → ⛔ ABSTAIN (odamdan so'raladi)   ← xavfsizlik
    └── ishonch ≥ 0.72 → davom
        │
        ▼
[2] HARD QOIDALAR ─────────────────── <0.1 s
    bemor allergiyasi (ATC guruh darajasida)
    homiladorlik / yosh cheklovi
    retseptli/retseptsiz (389 ro'yxat)
    ro'yxatga olinganmi (8 742)
    → bloklangan variantlar CHIQARIB TASHLANADI (modeldan ustun)
        │
        ▼
[3] M2 · EKVIVALENT REYTINGI ──────── 1.2 s
    nomzodlar = shu INN, qoidalardan o'tganlar
    skor = doza mosligi + shakl + bioekvivalentlik + qoplam
           + qoldiq ehtimoli + narx (referens narx bilan)
    → top-3, har biri "nega" bilan
        │
        ▼
[4] M3 · XAVF QATLAMI ─────────────── 0.6 s
    non-interruptiv: natija yonida ko'rsatiladi
    qoidalar (5+ dori, dublikat, ICD↔dori, ATC dublikat)
    + model balli
    → har signal: kod + asos + tavsiya
        │
        ▼
[5] M4 · QOLDIQ VA MARSHRUT ───────── 0.9 s
    P(dorixona X da bor, 48 soat)
    → birinchi muvaffaqiyat ehtimoli eng yuqori nuqta
    → masofa × ehtimol optimizatsiyasi
        │
        ▼
[6] A0 · AGENT ORKESTRATSIYASI
    qadamlar soni 2–9 (vaziyatga qarab)
    abstain, qayta urinish, alternativa, inson chaqiruvi
    har qadam LOG (audit uchun)
        │
        ▼
[7] INSON TASDIG'I ─────────────────── MAJBURIY
    farmatsevt ko'radi → tasdiqlaydi → yozuv yakunlanadi
    (agent hech qachon o'zi "beradi" demaydi)
```

**Umumiy vaqt:** **~4 soniya** kompyuter + **~35 soniya** inson o'qishi = **40 soniya** (3–5 daqiqa o'rniga).

## 5.2 Ustuvorlik ierarxiyasi — nega bu xavfsiz

```
   1. QAT'IY QOIDALAR   ← hech qachon yengilmaydi
      (allergiya, kontrendikatsiya, ro'yxat, yosh)
              │
   2. MODEL BALLARI     ← faqat tartiblaydi, taqiqlamaydi
      (M1, M2, M3, M4)
              │
   3. LLM               ← faqat TIL: matn tushunish, izoh yozish
      hech qachon dori tanlamaydi
              │
   4. INSON TASDIG'I    ← javobgarlik shu yerda
```

> **Nega LLM pastda:** LLM **galütsinatsiya** qiladi — dori nomini o'ylab topishi mumkin. Farmatsevtika regulyatori buni qabul qilmaydi. Shuning uchun LLM **faqat til qatlami**, qaror qatlami emas. Bu bitta jumla hakamlarda katta ishonch yaratadi.

## 5.3 4 model — har biri alohida o'lchanadi

| Model | Turi | Kirish | Chiqish | Metrika | Chiziq → Maqsad |
|---|---|---|---|---|---|
| **M1** rezolver | NLP: translit + n-gram + Levenshtein (+ GBM ishlab chiqarishda) | erkin matn | INN + ATC + ishonch | top-1 aniqlik | **25.5%** → **≥90%** |
| **M2** reytingchi | Learning-to-rank (LightGBM LambdaMART) | INN + kontekst | tartiblangan top-3 | NDCG@3 | 0.58 → **≥0.80** |
| **M3** xavf | GBM + SHAP + hard rules | retsept + tashxis + bemor | ball + sabab kodlari | AUC, **izoh 100%** | 0.70 → **≥0.84** |
| **M4** qoldiq | GBM regressiya + zaxira | dorixona × INN | P(mavjud) | marshrut muvaffaqiyati | 34% → **≥65%** |
| **A0** agent | Tool-use orkestrator | retsept | qarorlar ketma-ketligi | avtomatik hal %, kechikish | — → **≥80%, <6 s** |

## 5.4 Ma'lumot — bugun kechqurun nima ishlatiladi

| Ma'lumot | Manba | Hajm | Qaysi model |
|---|---|---|---|
| Davlat reyestri | uzpharm-control.uz | **8 742 yozuv** | M1 ground truth, M2 nomzodlar |
| Retseptli/retseptsiz | uzpharm-control.uz | 389 + 12 817 | Hard qoidalar |
| "Tarkibi bir xil" ro'yxati | data.gov.uz | statik | M2 ekvivalentlik |
| ATC/INN | JSST (ochiq) | ~6 000 | Kodlash |
| ICD-10 | JSST (ochiq) | ~14 000 | M3 ICD↔dori |
| O'zaro ta'sir | Ochiq + küratörlangan **top-150** | 150 juftlik | Hard qoidalar |
| Qoldiq (sintetik) | Generator | 6 000 × 500 | M4 |
| Retsept loglari (sintetik) | Nizom qoidalariga mos generator | 50 000 | M3 o'qitish |

## 5.5 Pul mexanizmi — qanday to'lanadi

| Mijoz | Narx | CAC | **Payback** | LTV/CAC |
|---|---|---|---|---|
| Dorixona | **$21/oy** ($250/yil) | $180 → **$20 (tarmoq)** | **8.6 oy** | **6.9** |
| Klinika | $8/vrach/oy ($900/yil) | $800 | 11 oy | 2.8 |
| Vazirlik/SHIF | kontrakt | $5–15k | 9–18 oy sikl | yuqori |

**Sotuv mantig'i (dorixona tilida):** *"Oyiga bitta qo'shimcha retsept to'ldirsangiz, narximiz qaytadi. Biz 20–30 tasini beramiz."*

---

# QISM VI · WORKING (ishlaydi — isbot)

## 6.1 Kod yozildi va ishladi (bugun, 17-noyabr)

**Fayllar:** `prototype/doribon_core.py`, `prototype/eval_m1.py`. Tashqi API/internet **talab qilmaydi**.

```
$ python3 eval_m1.py
========================================================================
  M1 REZOLVERI — O'LCHOV NATIJALARI
========================================================================
  Test to'plami: 55 ta holat

  BASELINE (aynan moslik)          :  14/55  =  25.5%
  BIZNING USUL  top-1              :  55/55  = 100.0%
  BIZNING USUL  top-3              :  55/55  = 100.0%
  Abstain (ishonch < 0.72)         :   1  =   1.8%

  ➜ YAXSHILANISH: +74.5 punkt (baseline'dan)

  DISTRAKTOR (reyestrda yo'q 8 dori):
    to'g'ri abstain                : 8/8
    noto'g'ri map (XAVFLI)         : 0/8
========================================================================
```

**Halol izoh:** 100% — kichik, o'zimiz tuzgan to'plamda (in-distribution). Haqiqiy 8 742 yozuvli reyestrda sinf soni ~1 000 → maqsad **≥90%**. Lekin **distraktor testi** muhimroq: model **notanish dori uchun taxmin qilmaydi** — abstain qiladi.

## 6.2 Ishlaydigan oqim — konsol chiqishi (haqiqiy)

```
[A0] retsept qabul qilindi: 'амоксицилин 500мг капс'
[M1] rezolyutsiya: amoxicillin (ATC J01CA04, ishonch 0.92)
[M2] 5 ta ekvivalent topildi, eng yaxshisi: Amoxil
[M2] tanlangan variant eng arzonidan 7,000 so'm qimmat (qoldiq/moslik uchun)
[A0] natija tayyor -> INSON TASDIQ'I kutilmoqda

➜ TAKLIF: Amoxil · 500 mg · 18,000 so'm · qoldiq 82%
   HOLAT: awaiting_human_approval
```

Va xavfsizlik qatlami:
```
INN: amoxicillin · bemor allergiyasi: penitsillin
Natija: 0 ta variant (qoida barchasini blokladi)
Agent alternativasi: Azitromitsin (25,000 so'm, qoldiq 80%)
```

Va M3 (non-interruptiv, izohli):
```
Xavf balli: 0.805   Asoslash shart: HA
 • [YUQORI] 5 ta dori bir vaqtda yozilgan
            asos: SSV buyrug'i: 5+ dori — bo'lim mudiri yoki klinik farmakolog asoslashi shart
 • [ORTA  ] Bir ATC guruhida 2 ta dori: amoxicillin, azithromycin
            asos: ATC J01 — terapevtik dublikat ehtimoli
 • [YUQORI] Antibiotik (amoxicillin, azithromycin) tashxis J45.9 bilan mos emas
            asos: Klinik protokol: bu tashxislarda antibiotik ko'rsatilmagan
```

> **Diqqat:** hech biri **pop-up emas**. Hammasi **natija ichida**, **asos bilan**. Bu B5 (alert fatigue) saboqlarining kodga ko'chirilishi.

## 6.3 "Ishlaydi" ning 4 darajasi — har biriga mezon

| Daraja | Nima | Mezon | Holat |
|---|---|---|---|
| **W1** Deterministik | M1 + qoidalar ishlaydi | 20 test holat o'tadi | ✅ **Bajarildi** |
| **W2** O'lchangan | Har modelda metrika | 5 qator raqamli jadval | 🟡 M1 tayyor, M2–M4 bugun |
| **W3** Jonli demo | 3 marta ketma-ket yiqilmaydi | Offline rejim + zaxira video | 🔴 18-noy 10:00 |
| **W4** Foydalanuvchi tasdiqladi | Farmatsevt ishlatdi | 1 farmatsevt "ha, tezroq" dedi | 🔴 19-noy gacha |

## 6.4 Qabul mezonlari (acceptance criteria) — bitim sifatida

| # | Mezon | Maqsad | Tekshirish usuli |
|---|---|---|---|
| AC1 | M1 top-1 | ≥90% (real reyestrda) | `eval_m1.py` |
| AC2 | M1 abstain to'g'riligi | notanish dori → **100% abstain** | distraktor testi |
| AC3 | M2 NDCG@3 | ≥0.80 | farmatsevt tanlovi bilan taqqoslash |
| AC4 | M3 AUC | ≥0.84 | belgilangan 200 retsept |
| AC5 | M3 izoh qoplovi | **100%** | har flag'da asos matni bor |
| AC6 | M4 marshrut muvaffaqiyati | ≥65% | sintetik → real |
| AC7 | Uchdan-uchgacha kechikish | **<6 s** | xronometr |
| AC8 | Demo barqarorligi | 3/3 ketma-ket | jonli |

## 6.5 Riskli taxmin testi (RAT) — eng katta noaniqlik nima

| Taxmin | Nega riskli | Qanday 48 soatda tekshiriladi |
|---|---|---|
| **Farmatsevt ishlatadi** | Dekabr 2025 inqirozi shuni ko'rsatdiki, vosita "tushuntirmasa" rad etiladi | 1 farmatsevtga ko'rsatish, **vaqtni o'lchash** |
| **Dorixona $21/oy to'laydi** | O'zbekistonda SaaS to'lov odati past | 5 dorixonaga savol: *"sinov uchun qancha to'laysiz?"* |
| **INN→mahsulot xaritasi reyestrdan chiqadi** | Reyestr formati noma'lum | **Bugun reyestrni yuklab, parse qilish** — 30 daqiqalik ish |
| **Qoldiqni olish mumkin** | Qoldiq DMED'da emas, dorixonada | M4 ni sintetik bilan qoldirish **va ochiq aytish** |

---

# QISM VII · PROBLEM–SOLUTION FIT (talabga muvofiqlik isboti)

## 7.1 Nizomning 7 mezoni bo'yicha xarita

| # | Mezon | Qanday qondiriladi | Dalil |
|---|---|---|---|
| 1 | **Trekka muvofiqlik** | Retsept → dori → farmatsevtika. Trek nomida "farmatsevtika" bor | QISM I |
| 2 | **AI innovatsionligi** | 4 o'qitilgan model + agent + guardrail + izoh; mahalliy analоg yo'q | QISM V.3, VI.1 |
| 3 | **Texnik sifat (MVP, kod)** | Kod yozilgan, o'lchangan, offline ishlaydi | QISM VI.1 |
| 4 | **UI/UX** | 2 ekran, 40 soniya, o'zbekcha, non-interruptiv | QISM V.1, IV.3 |
| 5 | **Amaliy qo'llash/masshtablash** | 6 000 dorixona DMED'da; tarmoq kanali; 8 912 muassasa | QISM V.5 |
| 6 | **Pitch sifati** | Har da'vo raqamli, chegaralar ochiq, 27 savolga javob | ushbu hujjat |
| 7 | **Reglament** | Checkpoint 18-noy 15:00; jamoa 4–5; trek 1-kundan | 48 soat reja |

## 7.2 Besh fit testi

| # | Test | Savol | Javob |
|---|---|---|---|
| 1 | **Muammo fiti** | Muammo haqiqiymi, og'riqlimi? | ✅ Qonun bilan majburiy; dekabr 2025 inqirozi bilan isbotlangan |
| 2 | **Yechim fiti** | Bizning yechim muammoni **to'liq** yopadimi? | ✅ S1–S5 → R1–R5, 1:1 xarita |
| 3 | **Kanal fiti** | Yetib borish mumkinmi? | ✅ 6 000 dorixona bitta platformada (DMED) |
| 4 | **Model fiti** | To'laydimi? | 🟡 Payback 8.6 oy — **hisoblandi, lekin real mijozda tasdiqlanmagan** |
| 5 | **Vaqt fiti** | Nega hozir? | ✅ 2027-yanvar majburiyati = **qaytarilmas deadline** |

---

# QISM VIII · HALOL QOLDIQLAR (nima hali isbotlanmagan)

| # | Isbotlanmagan | Halol holat | Qachon yopiladi |
|---|---|---|---|
| 1 | **Real reyestrda M1 aniqligi** | 100% faqat namunada | Bugun kechqurun |
| 2 | **M2 ning real farmatsevt tanloviga mosligi** | Hozir evristik vaznlar | 3 haftalik pilot |
| 3 | **M3 ning real AUC si** | Sintetik log + nizom qoidalari | 200 retseptni belgilash |
| 4 | **M4 real qoldiq** | Sintetik | Tarmoq shartnomasi |
| 5 | **To'liq o'zaro ta'sir bazasi** | Top-150 juftlik | Litsenziya |
| 6 | **To'lov irodasi** | Hisoblangan, tasdiqlanmagan | 5 dorixona suhbati |
| 7 | **Farmatsevtning qabul qilishi** | Dizayn tamoyili, real test yo'q | 19-noy |

> **Bu ro'yxatni pitch'da ko'rsatish — kuchsizlik emas, kuch.** Hakam "bu jamoa o'z chegarasini biladi" deb baholaydi. Olive AI'ning o'limi aynan **chegarani bilmaslikdan** bo'lgan.

---

# QISM IX · 10 QATORDA XULOSA

1. **Muammo:** INN majburiy, INN→mahsulot xaritasi yo'q. 10 000 savdo nomi, 1 000 INN, 3 daqiqa, xotiradan.
2. **Ildiz:** R1 nom ko'pligi · R2 vositasiz qoida · R3 kirill/lotin · R4 qoldiq ko'rinmas · R5 nazorat qog'ozda.
3. **Nima qilindi:** davlat **qoida, to'lov, reyestr, platforma** qurdi. **Uchta bo'g'in** — rezolyutsiya, xavfsizlik, marshrut — bo'sh.
4. **Eski innovatsiya:** ATC/INN (1970-yillar) va **RxNorm (2005, 99.995% qamrov)** — arxitektura namunasi, O'zbek reyestri bilan ishlamaydi.
5. **Global startup:** Truemeds (72% tejash), Synapse ($39M), **Latent ($600M baho — agent modeli isbotlangan)**, Queue ($12.6M).
6. **Global o'lim:** CDSS ogohlantirishlarining **49–96% i e'tiborsiz** (jamlangan 96.2%) → **biz interruptiv ogohlantirish qurmaymiz**.
7. **Olib tashlandi (9):** tashxis, pop-up, to'liq interaksiya bazasi, B2C, yetkazish, EHR, hardware, ASR, "platforma".
8. **Qoldi (5):** rezolyutsiya · reyting · xavfsizlik (non-interruptiv) · marshrut · audit.
9. **Qanday:** 7 qadam, 4 soniya mashina + 35 soniya inson. Ustuvorlik: **qoidalar > model > LLM > inson**.
10. **Ishlaydi:** kod yozilgan, M1 **55/55** va distraktor **8/8 abstain**; maqsad real reyestrda **≥90%**; 8 qabul mezoni qog'ozda.

---

# QISM X · MANBALAR

**Muammo va qoidalar**
1. SSV buyrug'i (lex.uz `-3032611`) — retsept INN bo'yicha, lotin yozuvida; 5+ dori asoslash; 4+ dori kelishish
2. VMQ 570 (10.12.2025) — e-retsept piloti, 12 817 retseptli dori, 2027-yanvar majburiyat
3. kun.uz (05.07.2020) — 5+ dori asoslash qoidasi
4. spot.uz (24.12.2025) — dekabr inqirozi, 389 retseptsiz dori ro'yxati
5. gazeta.uz (13.12.2025) — e-retsept qamrovi: xususiy klinikalar 49%, Toshkent 41%
6. **738-son (24.11.2025)** — dori vositalarini ro'yxatga olish tartibi
7. "Dori vositalari va farmatsevtika faoliyati to'g'risida" qonuni (lex.uz `-2856464`)
8. **gazeta.uz (29.01.2025)** — referens narx: bir ishlab chiqaruvchining bir xil tarkibli dorilariga **eng past narx**; ulgurji 15%, chakana 20%

**Eski lekin innovatsion standartlar**
9. **JSST ATC/INN** tasnifi (~6 000 kod, 5 daraja)
10. **RxNorm (NLM, 2005):** qamrov **99.995%**, avtomatik bog'lash 98.8%, `getApproximateMatch` API — *Evaluation of RxNorm for Representing Ambulatory Prescriptions*, PMC3041423
11. *Normalized names for clinical drugs: RxNorm at 6 years*, PMC3128404 — TTY ierarxiyasi (IN/SCDC/SCDF/SCD/SBD)
12. RxNorm chegarsi: narx/formulyar **yo'q** — inferensys, firestarterpro, casrai hujjatlari
13. Generik almashtirish siyosati (Yevropa) — umumiy amaliyot
14. Surescripts / e-retsept infratuzilmasi (AQSh)

**CDSS muvaffaqiyatsizligi (eng muhim dalil)**
15. **van der Sijs et al., 2006** — *Overriding of Drug Safety Alerts in CPOE*, PMC1447540: **49–96%** override
16. Weingart et al., 2003 — 94% umumiy, **96% o'rta darajali interaksiya**
17. Nightingale et al., 2000 — 87 789 order, **90%** override
18. 2022 DDI CDSS tadqiqoti (BMC Med Inform Decis Mak) — **96.8%** override asosli deb topilgan
19. *Medication safety alert fatigue...* systematic review — jamlangan **96.2%**
20. KevinMD (04.11.2026) — "alert fatigue is a design problem"

**Global startup va vendor**
21. **Truemeds** (Hindiston) — AI retsept→generik moslashtirish, **72% gacha tejash**
22. **Synapse Medicine** — $39M, MedGPT (Dealroom)
23. **Latent** — $80M Series A, ~$600M baho, $20M+ ARR, 45 sog'liq tizimi (Forbes, 18.03.2026)
24. **Queue** — $12.6M seed, avtonom robot dorixona (TNW, 01.07.2026)
25. **DoseMe / DoseMeRx** — Bayesian PK dozalash, $3 500/oy
26. Alto / Capsule / Truepill — ~$2 mlrd, "digital pharmacy shakeout" (Business Insider, 31.03.2023; multias.vc)
27. DrFirst, Waltz Health, Surescripts — e-retsept/narx infratuzilmasi

**O'zbekiston bozori**
28. uzpharm-control.uz — davlat reyestri **8 742 yozuv**; retseptli/retseptsiz ro'yxat
29. data.gov.uz — "Tarkibi bir xil ammo turli nomlanishga ega bo'lgan dori vositalari ro'yxati"
30. yuz.uz (31.07.2021) — ~10 000 savdo nomi vs 600–1 000 INN
31. asdr.gov.uz (10.06.2026) — DMED: 38 mln e-karta, 8 000+ klinika, 6 000 dorixona
32. anhor.uz (24.10.2026) — 8 912 ambulator muassasa
33. Law No. 1125 (26.03.2026) — lokalizatsiya islohoti; ZRU-547 — tibbiy ma'lumot alohida toifa
34. `hackathon_razvedka_2026.md`, `sogliq_treki_due_diligence.md`, `doriyol_masterplan.md` (eski nom bilan) — ushbu papkadagi oldingi hujjatlar
