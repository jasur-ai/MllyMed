# 300 BOSQICHLI TADQIQOT MASTERPLAN
## National AI Hackathon Tashkent 2026 — 3 g'oya, 3×100 bosqich, 1 qaror

**Sana:** 17-noyabr 2026, 08:00 (Toshkent) · **Event:** 17–19-noyabr, Youth Creativity Centre
**Trekler:** Sog'liqni saqlash va farmatsevtika · Ta'lim ("Formation") · Tadbirkor
**Tayyorlagan:** strategik tadqiqot hujjati (ochiq manbalar + bozor tahlili)
**Versiya:** 1.0 · **Til:** o'zbek (lotin), texnik atamalar ingliz tilida

---

# 0. TL;DR — 60 SONIYADA QAROR

> **Birinchi o'qiladigan qism. Qolgan 250 sahifa shu 6 qatorni isbotlaydi.**

| # | G'oya | Trek | Bir qatorda | 100 bosqichli baho |
|---|-------|------|-------------|--------------------|
| **1** | **MEDSI** | Sog'liq | O'zbek tilida gapiradigan "vrach kotibi": qabulni eshitadi → DMED formatida hujjat yozadi → tashxis bo'yicha protokol eslatadi | **73.2 / 100** |
| **2** | **USTOZ AI** | Ta'lim | 5–11-sinf o'quv dasturiga bog'langan, javob bermaydigan (hint-first) repetitor + o'qituvchi paneli | **74.0 / 100** |
| **3** | **HISOB AI** | Tadbirkor | Telegram'dagi "buxgalter": faktura/pdf/ovoz → soliq xulosasi, risk-skor izohi, deklaratsiya tayyorlash | **92.8 / 100** |

### QAROR: **G'OYA №3 — HISOB AI** (Tadbirkor treki)

**Uch sabab, uch raqam:**
1. **Bozor bor va to'laydi:** O'zbekistonda **1,236,100** faol kichik biznes subyekti, **357,883** YaTT, kichik biznes YaIMning **52.2%**i va bandlikning **~74%**i. Ular allaqachon buxgalterga oyiga pul to'laydi — biz yangi xarajat emas, **arzonroq o'rinbosar** sotamiz.
2. **Regulyativ "deraza" hozir ochildi va yopiladi:** 2026-yil 1-yanvardan **ZRU-1108** (avtomatik deklaratsiya + o'zini-o'zi band qilganlarga e-faktura), **UP-153** (real-time AI soliq risk-skor), **UP-100** (26.05.2026: 6% VIP, 12 000 BRV chegarasi, deklaratsiyasiz rejim), **PP-247** (1% aylanma solig'i). Natija: 600 000+ tadbirkor qoidani tushunmay qoldi → **tushuntirishga bo'lgan talab portladi**, taklif esa yo'q.
3. **48 soatda ko'rsatib bo'ladi:** faktura/chek rasmi → OCR → soliq xulosasi → Telegram javobi. Jonli demo, real hujjat bilan, internetsiz ham ishlaydigan fallback bilan.

**Nima uchun №1 va №2 emas:** ikkalasi ham kuchli (73–74 ball), lekin (a) ma'lumotga kirish yopiq (DMED), (b) 36 soatda ishonchli klinik demo qurish xavfli, (c) ta'limda raqobat allaqachon zich (EduBaza, Mohirdev, bepul ChatGPT) va **engagement** — asosiy o'lim sababi. Batafsil: 7-bo'lim.

**Bugun, T−4 soatda nima qilish kerak:** 10-bo'limdagi "72 soatlik playbook" ning **BLOK 0** (4 ta vazifa, 90 daqiqa).

---

# 1. KONTEKST: BIZ NIMA UCHUN MUSOBAQAGA KIRYAPMIZ

## 1.1 Event anatomiyasi

| Parametr | Fakt | Strategik xulosa |
|---|---|---|
| Format | 17–19-noyabr, 3 kun | 1-kun: jamoa + trek tanlash. 2-kun: mentorlik + **checkpoint 15:00** + **20 finalist 19:00**. 3-kun: faqat pitch |
| Trekler | Sog'liq · Ta'lim · Tadbirkor | Uchala g'oya ham mos — tanlov erkin, ya'ni **qaror raqobatga qarab** qilinadi, mavzuga qarab emas |
| Mukofot | 1-o'rin: MacBook Air; 2-o'rin: 20 mln so'm; 3-o'rin: 10 mln so'm | Pul kichik. **Asl qiymat — mentorlar, IT Park aloqasi, Demo Day investorlari, prezident dasturlari (PQ-59) yo'li** |
| Nominatsiyalar | "Eng qiziqarli prezentatsiya", "Eng dolzarb ijtimoiy loyiha" | Ikkita qo'shimcha yutish yo'li bor → pitch dizayni ikkalasiga ham "tegishi" kerak |
| Cheklov | 16+, Toshkent/Toshkent viloyati, ro'yxatdan o'tganlar | Raqobat = Toshkent yoshlari, ya'ni texnik saviyasi o'rtacha-yuqori, **biznes saviyasi past**. Bu bizning ustunligimiz |

### Tanlov mexanikasi (ehtimoliy, tekshiriladi)
Eventflow sahifasida mezonlar e'lon qilinmagan → **10-bo'lim, 11-bosqichda** tashkilotchidan so'raladi. Benchmark sifatida Toshkentdagi o'xshash hackathon mezoni (Hack Tashkent 2026):

| Mezon | Vazn |
|---|---|
| **Ishlaydi (works)** | **30%** |
| Innovatsiya | 20% |
| Amaliy qiymat | 20% |
| Mavzuga moslik | 10% |
| Pitch sifati | 10% |
| Jamoa | 10% |

> **Strategik xulosa:** "Ishlaydi" 30% — ya'ni **yarim ishlaydigan aqlli g'oya emas, to'liq ishlaydigan oddiy narsa yutadi**. Bu HISOB AI ni yana oldinga chiqaradi: uning demo'si 100% barqaror (fayl kirish → matn chiqish), klinik demo esa tashqi tizimga bog'liq.

## 1.2 Raqobat manzarasi: kim bizga qarshi turadi

**Bukhara bosqichi natijalari (aprel 2026) — eng muhim razvedka ma'lumoti:**

| Trek | 1-o'rin | 2-o'rin | 3-o'rin |
|---|---|---|---|
| Healthcare | **Med IQ** | Med AI | Neuro X |
| Education | **Robots and Me** | Feba | Monday |
| Entrepreneur | **Databek** | Ko'k Choy | Protocol X |

**Tahlil:**
- Sog'liqda **uchala g'olib ham "Med/Neuro"** — ya'ni hakamlar tashxis/simptom-cheker tipidagi loyihalarni allaqachon 3 marta ko'rgan. **Differensiatsiya qiyin.**
- Ta'limda "Robots and Me" — robototexnika/hardware, ya'ni **AI-tutor hali g'olib bo'lmagan** (lekin demak bo'shliq ham, isbotsizlik ham bor).
- Tadbirkorda "Databek" — data/analitika. Ya'ni **buxgalteriya–soliq janri hali egallanmagan**.
- Nomlarning o'zi "startup nomi" emas, "jamoa nomi" — Demak hakamlar **nomdan emas, demo'dan** baholaydi.

> **Xulosa:** Toshkentda klinik-tashxis g'oyalari to'lib-toshgan (Med IQ, Med AI, Neuro X, symptom checker'lar), soliq/buxgalteriya esa **bo'sh**. Bu 3-g'oyaning eng katta "asan" ustunligi.

## 1.3 Nima uchun hackathon emas, "post-hackathon" muhim

Hackathon — bu **tarqatish kanali**, mahsulot emas:
- PQ-59 (11.02.2026): 2030-yilga qadar **5 000 startap**, **$2 mlrd venchur**, 500 ta $1 mln+ kompaniya, 100 ta $10 mln+, 25 ta $100 mln+. Dastur ishtirokchilari **avtomatik IT Park rezidenti** (01.04.2026 dan).
- IT Park rezidenti = **0% foyda solig'i, 0% QQS**, IT-visa, 2 800+ kompaniya tarmog'i.
- IT Park Ventures: $10k (idea) → $1 mln (Seed/Series A), o'rtacha $150k.
- Prezident AI Award: **$1 mln** mukofot jamg'armasi (2026 dan).

> **Ya'ni:** 1-o'rinni olishning moliyaviy qiymati MacBook emas — **keyingi 12 oyda jalb qilinadigan $150k–$500k grant/venchur va soliq imtiyozining kirish eshigi**. Shu sabab pitch "biz hackathon yutdik" emas, **"biz PQ-59 o'lchovlariga to'g'ri kelamiz"** tilida qurilishi kerak.

---

# 2. MAKRO: O'ZBEKISTON 2026 — RAQAMLAR BILAN

> Har bir raqam qarorga ta'sir qiladi. Manbalar 15-bo'limda.

## 2.1 Demografiya va raqamli infratuzilma

| Ko'rsatkich | Qiymat | Sana | "Why now" ga ta'siri |
|---|---|---|---|
| Aholi | **38.2 mln** (MDHda 1-o'rin) | 01.2026 | Bozor hajmi yetarli; ichki bozor bilan startup qurish mumkin |
| Median yosh | **27** | 2025 oxiri | Raqamli mahsulotga tayyor auditoriya |
| 14–30 yosh | **9.6 mln** (~25%) | 2026 | Ta'lim va ish mahsulotlari uchun yadro |
| Internet foydalanuvchilari | **33.9 mln / 89.5%** | 10.2026 | Tarqatish muammosi deyarli yo'q |
| Mobil qurilmalar | 33.9 mln ulanish, **97.5% broadband** | 10.2026 | Mobile-first majburiy |
| Telegram | **~25 mln foydalanuvchi (~85%)** | 2026 | **Birinchi kanal Telegram, Instagram emas** (Instagram ~16%) |
| To'lovlar | **Click 12 mln+**, **Payme 8 mln+** | 2026 | Onlayn to'lov infra tayyor → B2C monetizatsiya mumkin |
| Uzum | **$2.3 mlrd baho** (birinchi "unicorn") | 03.2025 | Investorlar uchun "bu yerda exit bo'ladi" isboti |

## 2.2 Iqtisodiyot va IT sektori

| Ko'rsatkich | Qiymat | Manba |
|---|---|---|
| IT xizmatlari eksporti | **<$1 mln (2017) → ~$1 mlrd (2026)** | Raqamli texnologiyalar vazirligi |
| Maqsad | **$5 mlrd IT+AI eksporti (2030)** | Sherzod Shermatov |
| IT Park eksporti | **$191.8 mln / Q1 2026, +25% YoY** | IT Park |
| IT Park xizmatlari | **9.4 trln so'm / Q1 2026** | IT Park |
| AKT ulushi | **YaIMning 2.7%** (2025), qo'shilgan qiymat **+23.9%** | Statkom |
| Startap moliyalash | $0.3 mln (2020) → **$69.5 mln (2024)**; jami **$618 mln+** | Stanbase/Pivot |
| Kichik biznes YaIMdagi ulushi | **52.2%** (2025) → 50.5% (1-yarim 2026) | Statkom |
| Kichik biznes bandlikdagi ulushi | **~74% (10.5 mln kishi)** | Statkom |
| Raqamli savdo ulushi (SME) | **<30%** | Jahon banki |
| Venchur kapital talabi vs taklifi | **$20–30 mlrd vs ~$2 mlrd** | Jahon banki |

> **"Why now" ning iqtisodiy yadrosi:** mamlakatda **kapital ko'p, mahsulot kam**. IT eksporti 1000× o'sdi, lekin bu asosan **autsorsing** — o'z IP'si bo'lgan mahsulot kompaniyalari hali kam. Davlat aynan shu bo'shliqni pul bilan to'ldirmoqchi (PQ-59, AI Award). Demak: **hozir mahalliy bozorga mos, IP'li AI mahsulot quruvchilar eng katta rag'batni oladi.**

## 2.3 Davlat siyosati: to'liq xronologiya (bu sizning "tailwind"ingiz)

| Sana | Hujjat | Mazmuni | Bizga ahamiyati |
|---|---|---|---|
| 05.10.2020 | PF-6079 | "Raqamli O'zbekiston — 2030" | Asosiy ramka |
| 14.10.2024 | **PQ-358** | AI strategiyasi 2030: AI mahsulot/xizmatlar hajmi **$1.5 mlrd**, Gov AI Readiness **top-50**, IT Park'da AI markazi | Bozorning "rasmiy" hajmi |
| 14.10.2024 | PQ-357 | "Digital Startup" dasturi, IT Park Ventures | Bizning moliyalashish yo'limiz |
| 22.10.2025 | **UP-189** | 2026 oxirigacha **100 ta AI loyihasi**, 2030 gacha **$1 mlrd AI infra**, **15 ta AI laboratoriya**, `ai.gov.uz`, **Prezident AI Award ($1 mln)**, "5 Million AI Leaders" | **Byudjet egasi = davlat.** Davlat xaridi = birinchi mijoz |
| 25.12.2025 | **ZRU-1108** | 2026 soliq islohoti: avtomatik deklaratsiya, o'zini-o'zi band qilganlarga e-faktura | ⚡ **3-g'oyaning portlash nuqtasi** |
| 01.01.2026 | UP-153 amalda | **Real-time AI QQS-faktura risk-skor** tizimi | ⚡ Tadbirkor "nima uchun flag qilindi?" deb tushunmaydi → tushuntirish mahsuloti kerak |
| 11.02.2026 | **PQ-59** | 2030: 5 000 startap, $2 mlrd venchur, 4 bosqichli ekotizim; Digital Startups → avtomatik IT Park rezidentligi (01.04.2026) | Bizning scaling yo'li |
| 26.05.2026 | **UP-100** | Kichik biznes: **6% ixtiyoriy QQS** (01.06.2026–01.01.2030), **12 000 BRV (~4.94 mlrd so'm → 5.28 mlrd, 01.09.2026)** chegarasi, importerlar uchun majburiy QQS bekor, riski 500 mln so'mgacha bo'lsa tekshiruv yo'q | ⚡ **600 000+ subyekt** rejim tanlash bosimida → maslahat talabi |
| 24.07.2026 | **PF-141** | AI "Raqamli O'zbekiston 2030" ga kirdi; KPI: **200 tarmoq AI loyihasi**, **250 AI rezident IT Park**, top-50, **3 000 AI mutaxassisi**; etika qoidalari va standartlar | Trek mavzusi = davlat prioriteti. Hakamlar buni biladi |

**Xulosa:** hukumat **AI'ni byudjet, KPI va mukofot bilan** majburiy yo'nalishga aylantirgan. Bu — "bozor o'zi yetiladi" degan 5 yillik kutishni **0 yilga** tushirgan. Lekin diqqat: PF-141 **xususiy sektorga majburiyat yuklamaydi** — ya'ni davlat puli bor, ammo **majburiy talab yo'q**. Demak **B2G kanali — tez, B2B — barqaror**.

## 2.4 Uch trek bo'yicha bozor faktlari (qisqa karta)

### Sog'liqni saqlash
- NCD (yuqumli bo'lmagan kasalliklar) — **o'limlarning ~80%**i; qon aylanish tizimi **61.1%** (2023).
- Qandli diabet: **7% (2021, ~1.35 mln) → 7.5% (2024)**.
- **27 vrach / 10 000** aholi (AQSh, UK, Finlyandiya darajasi) — *lekin* qishloqda oilaviy vrach yetishmaydi.
- Sog'liq xarajati: **42 trln so'm (~$3.2 mlrd), 2025**; 2021–25 da **€16.3 mlrd** investitsiya.
- NCD iqtisodiy zarari: **~$1 mlrd/yil**; 35% aholi surunkali kasallik bilan; tez yordam chaqiruvlarining **1/4** — surunkali bemorlar.
- **DMED**: 37 mln fuqaro ma'lumoti, MED-ID, 20+ modul, 400+ diagnostika protokoli, **8 000+ dorixona (66%)**, e-retsept, "ortiqcha retsept −40%", vrach yuki **−30%**.
- Xususiy klinikalar: **3 000–3 500 (2017) → 9 000+ (2025)**.
- Farmatsevtika ishlab chiqarish: **4.4 trln so'm (8 oy, 2026), +24.9%**; paketlarning **60% import / 40% mahalliy** (Q1 2025).
- Tibbiy turizm: **86 199 kishi (2025)**, 1-yarim 2026 — **35 401** (Tojikiston 19 096).

### Ta'lim
- **11 118 maktab**, **6.87 mln o'quvchi**, **577 700 o'qituvchi** (72.5% ayol), 1-sinfga **725 300** (2025/26), 2026/27 da **795 000** kutilmoqda.
- Xususiy maktablar: **551** (+21.1%); Toshkentda 145.
- Bir maktabga o'rtacha **619 o'quvchi**.
- **PISA 2025** (birinchi marta to'liq ishtirok): 8 652 o'quvchi / 233 maktab. **49% o'quvchi haftada kamida bir marta AI chatbot ishlatadi** (OECD 46%); 43% mavzuni o'rganish uchun (OECD 31%).
- **TALIS 2024**: o'qituvchilarning **62%** ishida AI ishlatgan (OECD 36%); 54% maktabda infra yo'qligini aytadi.
- Global repetitorlik bozori: **$143 mlrd (2026)**; AI-tutor bozori **$2.7 mlrd → $17.7 mlrd (2033)**.
- Mahalliy edtech: Mohirdev 50 000+ o'quvchi, Najot Ta'lim 12 000+ bitiruvchi, **EduBaza** ($50k, $1 mln baho, 2026-yil yanvar), Lerna.uz 793 kurs.

### Tadbirkorlik
- Faol kichik biznes: **1 201 600** (01.01.2026) → **1 236 100** (01.07.2026).
- YaTT: **357 883** (01.10.2026); Toshkent sh. 56 858.
- Operatsion korxonalar: **474 900**, shundan **403 800 (85%)** — kichik.
- Soliq rejimlari 2026: foyda **15%**, QQS **12%** (ixtiyoriy **6%**), JShDS **12%**, ijtimoiy **12%**, aylanma **4%**, YaTT/o'zini band qilganlar uchun **1%** (1 mlrd so'mgacha).
- 2026: SME'larga **140 trln so'm** kredit ajratilishi rejalashtirilgan.
- Global: Intuit QuickBooks **8.5 mln obunachi**, **7.5 mln** AI funksiyalardan foydalanadi; AQShda kichik bizneslarning **45%** AI-buxgalteriya ishlatadi, oyiga **10 soat** tejaydi, xarajat **40–50%** past.

---

# 3. G'OYA №1 — **MEDSI**
## O'zbek tilida ishlaydigan klinik "kotib" + oilaviy vrach yordamchisi

**Trek:** Sog'liqni saqlash va farmatsevtika
**Bir qatorda:** Vrach qabulni ovoz bilan olib boradi → MEDSI uni eshitadi → tuzilgan hujjat (shikoyat, anamnez, obyektiv holat, tashxis, retsept) tayyorlaydi → protokol bo'yicha ogohlantiradi → DMED'ga yuborishga tayyor holatda beradi.
**Kimga:** Toshkentdagi xususiy klinikalar (9 000+) → keyin davlat oilaviy poliklinikalari.
**Nima uchun kerak:** Vrachning vaqtining katta qismi **hujjatga** ketadi; DMED 70+ turdagi qog'oz jurnalni bekor qildi va yukni 30% ga tushirdi — ya'ni **hujjatni raqamli yozish majburiy bo'lib qoldi**, lekin yozishning o'zi hali ham qo'l bilan.

> **Halol ogohlantirish:** Bu eng "olijanob" va eng **xavfli** g'oya. Klinik xato = javobgarlik. Shuning uchun arxitektura "AI qaror qabul qilmaydi, AI **yozadi** va **eslatadi**" tamoyiliga qurilgan.

---

## FAZA A (1–10). Muammo va mijoz anatomiyasi

1. **Kimning og'rig'i eng o'tkir?** Savol: vrachmi, klinika direktori mi, bemormi? → **Topilma:** og'riq pul egasida (direktor) va vaqt egasida (vrach). Direktor "navbat va NPS" haqida, vrach "kechqurun uyda hujjat yozish" haqida gapiradi. → **Qaror:** xaridor = klinika direktori, foydalanuvchi = vrach, foyda dalili = "qabul soni +20%" yoki "vrach qo'shimcha 1 soat bo'sh".
2. **Hujjatga ketadigan vaqt ulushi qancha?** Savol: real o'lchov kerak → **Topilma (global):** Ispaniya tarmog'ida ambient scribe **qabul vaqtini 21.8% qisqartirdi**, hujjat sifati oshdi; Erasmus MC'da hujjatlashtirish vaqti **~30% kamaydi** (300 000+ qabul). → **Qaror:** O'zbekistonda ham xuddi shu o'lchovni 5 klinikada o'tkazish (3-bosqich vazifasi).
3. **O'zbekistonda hujjat yuki qanday o'zgardi?** Savol: raqamlashtirish yukni kamaytirdimi? → **Topilma:** DMED 70+ turdagi qog'oz jurnal/formani bekor qildi, vrach yuki **30% ga tushdi**, laboratoriya natijalari 3–5 daqiqada. → **Qaror:** "Raqamlashtirish muammoni qisman hal qildi, lekin **kirish (data entry) hali qo'lda**" — bu bizning aniq pozitsiya.
4. **Vrachlar soni yetarlimi?** → **Topilma:** **27 vrach / 10 000** (AQSh/UK/Finlyandiya darajasi), lekin **qishloqda oilaviy vrach tanqisligi** va mutaxassis taqsimoti notekis; 9 000 reproduktiv yoshdagi ayolga 1.5 ginekolog. → **Qaror:** "Vrach yetishmayapti" — zaif argument. Kuchli argument: **"vrach bor, lekin vaqti hujjatga ketyapti"**.
5. **Surunkali kasallik yuki qanday?** → **Topilma:** aholining **35%** surunkali kasallik bilan; tez yordam chaqiruvlarining **1/4**; NCD iqtisodiy zarari **$1 mlrd/yil**. → **Qaror:** uzoq muddatli yo'l — **surunkali bemorni kuzatish (follow-up)**, lekin hackathon uchun emas (uzoq sotuv tsikli).
6. **Xususiy sektor qanchalik katta?** → **Topilma:** klinikalar **3 000–3 500 (2017) → 9 000+ (2025)**, ya'ni 8 yilda ~3×. → **Qaror:** B2B xaridorlar bazasi yetarli; raqobat ham shu yerda (klinikalar o'zaro kurashadi → samaradorlik sotib oladi).
7. **Bemor oqimi qanday?** Savol: o'rtacha qabul davomiyligi → **Topilma:** DMED joriy etilgandan keyin Toshkent Yunusobodda maksimal konsultatsiya vaqti **30 → 17 daqiqa**ga tushdi. → **Qaror:** 17 daqiqada yozish — real vaqt bosimi; demo'da shu 17 daqiqani ko'rsatish.
8. **Muammoning "push" kuchi bormi (majburiymi)?** → **Topilma:** e-retsept va DMED 2026 oxirigacha barcha shifoxona/dorixonalarga majburiy, 2027-yil yanvardan umumiy rejim. → **Qaror:** Ha — **majburiy o'tish** bor. Lekin u bizning mahsulotga emas, DMED'ga majburiyat. Biz "DMED bilan birga yashash" mahsulotimiz.
9. **Vrachning haqiqiy ish oqimi (workflow) qanday?** Savol: qabul → yozuv → retsept → lab → qayd; qayerda uzilish? → **Topilma:** e-retsept oqimi 5 qadam (vrach → QR+E-IMZO → dorixona → tekshiruv → qayd). → **Qaror:** bizning integratsiya nuqtasi = **1-qadam oldi**: qabuldan matn chiqarish.
10. **Bitta jumlada muammo bayoni (muammo statement).** → **Yakuniy formulirovka:** *"Toshkentdagi xususiy klinika vrach o'rtacha 17 daqiqalik qabulning 6–9 daqiqasini klaviaturaga sarflaydi va bemorga qaramaydi; bu ham sifatni, ham kuniga qabul sonini cheklaydi."* → **Qaror:** pitch shu jumla bilan boshlanadi.

## FAZA B (11–20). Regulyatsiya, ma'lumot va huquqiy chegara

11. **DMED'ga kirish huquqi bormi?** Savol: ochiq API bormi, integratsiya kim orqali? → **Topilma:** DMED yagona integrator **UZINFOCOM** (PQ-415, 28.12.2023), 20+ modul, tibbiy ma'lumot davlat tizimida. Ochiq API e'lon qilinmagan. ⏳ **Tekshirish:** `dmed.uz` / UZINFOCOM'dan integratsiya reglamenti va hamkorlik sharti. → **Qaror:** 🔴 **Hackathon demo'si DMED API'siga bog'lanmasligi kerak.** Demo = fayl → matn. Integratsiya — 2-bosqich (90 kun).
12. **Shaxsiy ma'lumotlar rejimi qanday?** → **Topilma:** O'zbekistonda "Shaxsiy ma'lumotlar to'g'risida" qonuni va ma'lumotlarni **mahalliy serverlarda saqlash (data localization)** talabi amalda. ⏳ **Tekshirish:** 2019-yilgi qonun + 2026 holatiga o'zgartirishlar, tibbiy ma'lumot = maxsus toifa. → **Qaror:** arxitektura **mahalliy (O'zbekiston ichida) hosting** + "audio saqlanmaydi" rejimi bilan quriladi. Bu ham huquqiy, ham marketing argumenti.
13. **Bemor roziligi (informed consent) qanday olinadi?** → **Gipoteza:** yozib olish uchun og'zaki + ilovada rozilik kerak. ⏳ **Tekshirish:** Sog'liqni saqlash vazirligi talablari. → **Qaror:** demo'da "consent toggle" ko'rsatish — hakamlarda ishonch uyg'otadigan kichik, lekin hal qiluvchi detal.
14. **Tibbiy hujjatning majburiy shakli bormi?** → **Topilma:** 400+ diagnostika protokoli va davolash standarti 40 klinik yo'nalishda joriy etilgan. → **Qaror:** mahsulot **shu protokollar formatiga** mos chiqarishi kerak — bu bizning "moat"imiz (format bilimi).
15. **Retsept yozish tartibi nima?** → **Topilma:** e-retsept Xalqaro nom (INN) bo'yicha yoziladi, QR + ERI bilan, faqat O'zbekistonda ro'yxatdan o'tgan dorilar, ba'zi toifalar chiqarilmaydi. → **Qaror:** AI faqat **INN taklif qiladi**, savdo nomini emas → korrupsiya/farmakompaniya manipulatsiyasi xavfini yo'q qiladi (hakamlar uchun kuchli etika argumenti).
16. **Tibbiy qurilma (medical device) deb hisoblanadimi?** Savol: AI hujjat yozsa — bu dasturiy tibbiy qurilmi? → **Topilma:** O'zbekistonda alohida "AI tibbiy qurilma" regulyatsiyasi hali shakllanmagan; PF-141 faqat **etika qoidalari va standartlar tayyorlashni** buyurgan (ya'ni hali yo'q). → **Qaror:** ✅ **"Clinical documentation assistance" pozitsiyasi** (qaror qabul qilmaydi) — regulyatsiyadan chiqib ketishning eng qonuniy yo'li. Bu javob 15-bo'limdagi Q&A'da ham kerak.
17. **Xato uchun javobgarlik kimda?** → **Topilma:** global amaliyot: hujjatni **vrach imzolaydi**, ya'ni javobgarlik vrachda; AI "qoralama" beradi. → **Qaror:** mahsulot nomi ham shundan: **"qoralama"**, "tashxis" emas. Har bir chiqishda "tekshirildi" tugmasi + audit-log.
18. **Audit-log nima uchun kerak?** → **Topilma:** ambient scribe adabiyotida asosiy xavf — **audio-only tizimlarda xato 36× ko'p** (358 vs 10 missed errors) va "data drift" bilan model jimgina buziladi. → **Qaror:** har bir hujjat versiyasi, model versiyasi, vrach tahriri foizi saqlanadi → klinikaga "sifat hisoboti" sotamiz (ikkinchi daromad liniyasi).
19. **Ma'lumotni qayerdan olamiz (o'quv to'plami)?** → **Topilma:** tibbiy audio datasetlar O'zbekistonda **ochiq emas**. Ochiq Uzbek ASR korpuslari bor (Common Voice, FLEURS, USC 96 soat, UzbekVoice 594 soat) — lekin **tibbiy emas**. → **Qaror:** 🔴 ma'lumot = eng katta to'siq → strategiya: **sintetik dialoglar + 5 klinika bilan 40 soatlik real yozuv** (kelishuv asosida).
20. **Faza B yakuni (Go/No-Go).** → **Xulosa:** Texnik jihatdan mumkin, huquqiy jihatdan **ehtiyotkor dizayn bilan** mumkin; ammo **eng katta risk — ma'lumot va integratsiya**, hackathonda ularni yechib bo'lmaydi. → **Qaror:** hackathon demo'si "vertikal kesim" (bitta kasallik: **gipertoniya + qandli diabet** qabuli), to'liq klinika emas.

## FAZA C (21–30). Bozor hajmi: TAM / SAM / SOM

21. **TAM (jami bozor) — vrachlar soni.** → **Topilma:** 560 000+ tibbiyot xodimi DMED'da hisobga olingan; vrachlar ulushi ~30% deb olsak ≈ **150–170 ming vrach**. ⏳ **Tekshirish:** aniq statistika (Statkom/Sog'liq vazirligi).
22. **TAM — pulda.** → **Hisob:** 160 000 vrach × 100 000 so'm/oy × 12 = **192 mlrd so'm/yil (~$16 mln)**. → **Qaror:** bu kichik bozor; demak **sof SaaS bilan $10 mln+ kompaniya bo'lmaydi**. Kerak: (a) klinika-darajadagi shartnoma, (b) farma/insurance ma'lumot mahsuloti, (c) eksport.
23. **SAM (xizmat ko'rsatiladigan bozor) — xususiy klinikalar.** → **Topilma:** 9 000+ xususiy klinika, o'rtacha 8–15 vrach. → **Hisob:** Toshkentdagi 2 000 klinika × 10 vrach × 150 000 so'm = **3.6 mlrd so'm/oy ($300k/oy)**. → **Qaror:** SAM yetarli, agar ARPU klinika darajasida bo'lsa.
24. **SOM (real 24 oylik maqsad).** → **Hisob:** 120 klinika (Toshkentning ~6%) × o'rtacha 3 mln so'm/oy = **360 mln so'm/oy (~$30k/oy)** = yiliga $360k ARR. → **Qaror:** bu seed uchun ishonchli raqam; VC'ga "katta" ko'rinmaydi, lekin **IT Park Ventures bosqichiga mos** ($150k–$1 mln).
25. **Ikkinchi daromad liniyasi: farma.** → **Topilma:** farma ishlab chiqarish **4.4 trln so'm (8 oy 2026)**; bozor 60% import; brendlar INN raqobatiga o'tmoqda. → **Qaror:** **retsept analitikasi** (qaysi INN qayerda ko'p yoziladi) — farma uchun qimmatli, lekin **etik jihatdan xavfli** (manipulyatsiya). → **Chegara:** faqat agregat, anonim, sotuvga ta'sir qilmaydigan hisobot.
26. **Uchinchi liniya: sug'urta.** → **Topilma:** Davlat sog'liq sug'urtasi jamg'armasi bilan integratsiya rejalashtirilgan (National Health Compact, 12.2026 gacha). → **Qaror:** sug'urta uchun "hujjat sifati" = to'lov asosi → bizning audit-log mahsuloti.
27. **To'rtinchi liniya: tibbiy turizm.** → **Topilma:** 2025 da **86 199** chet ellik bemor; 1-yarim 2026 da 35 401 (54% Tojikiston). → **Qaror:** chet ellik bemor uchun **tarjima qilingan tibbiy xulosa** — kichik, lekin tez pul keltiradigan xizmat (qo'shimcha modul).
28. **To'lov qobiliyati testi.** Savol: klinika oyiga qancha to'lashga tayyor? → **Topilma:** xususiy klinika o'rtacha vrachdan qabul uchun 100–200 ming so'm oladi; bitta vrach oyiga ~$1 500–3 000 daromad keltiradi. → **Qaror:** ARPU vrach boshiga **oyiga $15–25** (200–300 ming so'm) real; 10 vrachli klinika = **$150–250/oy**. Bu "bir xodim maoshining 10%" — sotiladigan narx.
29. **Byudjet kimda?** → **Topilma:** klinika direktori CAPEX emas, **oylik OPEX**ni yaxshi ko'radi; davlat esa aksincha — tender va CAPEX. → **Qaror:** xususiy sektorda **oylik obuna**, davlatda **loyiha/tender** (2 xil pitch, 2 xil narx).
30. **Bozor xulosasi.** → **Xulosa:** "Kichik lekin och bozor". $16 mln TAM bilan venchur shkalasidagi kompaniya **faqat eksport yoki ma'lumot mahsuloti** bilan bo'ladi. → **Qaror:** hackathonda bu gapirilmaydi, lekin **slides 9 (vision)** da "Central Asia + Turkic languages" ko'rsatiladi.

## FAZA D (31–40). Global ilmiy dalillar: nima ishlaydi, nima o'ldiradi

31. **Ambient scribe haqiqatan ishlaydimi?** → **Topilma:** Ispaniya tarmog'i, 48 ta shoshilinch bo'lim, **1.03 mln konsultatsiya**, 12 oy: qabul vaqti **−21.8%**, transkripsiya aniqligi **93.9%**, hujjat sifati yuqori, shifokor tajribasi yaxshilandi. → **Qaror:** ✅ asosiy dalil shu; pitch'da bitta slayd.
32. **Lekin samaradorlik har joyda bir xilmi?** → **Topilma:** Mass General Brigham — **−5.6 daqiqa** EHR vaqti; Permanente — faqat **−18 soniya**; Intermountain — **statistik ahamiyatsiz**. → **Qaror:** ⚠️ halollik: "vaqt tejash kafolatlangan emas; **barqaror natija — kognitiv yuk va burnout kamayishi**". Bu halollik hakamlarda ishonch oshiradi.
33. **Xato manbalari qayerda?** → **Topilma:** audio-only tizimlar **358 xato**, vision-enabled **10 xato**; aksent, ko'p tilli qabul, shovqin, dorilar nomi — eng zaif joylar. → **Qaror:** bizning dizayn: **audio + kontekst** (vrach kiritgan tashxis/INN ro'yxati) → xatoni kamaytirish.
34. **Tashxis qo'yuvchi symptom checker ishlaydimi?** → **Topilma:** diagnostik aniqlik **19–38%**, triage **49–90%**; LLM'larning umumiy diagnostik aniqligi **52.1%**, ekspert vrachdan **15.8 p.p. past**. → **Qaror:** 🔴 **biz symptom checker qurmaymiz**. Bu bozor "o'lik" va xavfli.
35. **Nima uchun symptom checker'lar O'zbekistonda baribir quriladi?** → **Topilma:** chunki demo qilish oson va hakamlar "AI" ni ko'radi. Bukhara bosqichida 3 ta shunday loyiha g'olib bo'lgan. → **Qaror:** biz **ataylab qarshi** pozitsiya olamiz: "hamma tashxis qo'ymoqchi, biz **hujjat**ni yechamiz" — differensiatsiya bir jumlada.
36. **Hujjat sifati o'lchanadimi?** → **Topilma:** auditlarda AI-hujjatlar **yuqori ball** oldi; Wisconsin tadqiqoti: o'zgartirilgan so'zlar medianasi **9.0%**, **14.9%** hujjat umuman tahrirsiz qabul qilindi. → **Qaror:** bizning KPI: **tahrir foizi <15%** (o'zbek tili uchun realist maqsad 25–35% birinchi versiyada).
37. **Audio-only yetarlimi yoki video kerakmi?** → **Topilma:** vision-enabled 98% vs audio-only 81% (dori tarixi). → **Qaror:** hackathon'da audio; yo'l xaritasi: kamera ixtiyoriy (retsept/analiz qog'ozini ko'rish).
38. **Klinik natijalar (patient outcomes) isbotlanganmi?** → **Topilma:** ❌ **yo'q** — hozircha faqat samaradorlik, qulaylik, xarajat o'lchangan. → **Qaror:** biz "natijani yaxshilaydi" demaymiz; "**vaqtni bo'shatadi**" deymiz. Bu halollik — hakamlar oldida kuchli.
39. **Til muammosi qanchalik katta?** → **Topilma:** barcha yirik tadqiqotlar ingliz/ispan/niderland tilida; o'zbek tili uchun **nol dalil**. → **Qaror:** ✅ **bu bizning imkoniyat**: "dunyo buni isbotladi, O'zbekistonda hech kim qilmagan — chunki o'zbek tili uchun tibbiy ASR yo'q".
40. **Global bozor konteksti (investor uchun).** → **Topilma:** agentic AI bozori **$9.14 mlrd (2026) → $139 mlrd (2034)**; sog'liq vertikali eng tez o'suvchi (**48.4% CAGR**); agentik loyihalarning **40%+** 2027 oxirigacha bekor qilinadi (Gartner) → "hype emas, ish" pozitsiyasi kerak. → **Qaror:** pitch'da "48.4% CAGR" + "biz 40% bekor qilinadiganlarga kirmaymiz, chunki aniq ROI metriko'miz bor".

## FAZA E (41–50). Raqobat va alternativa

41. **Hozir vrach nima ishlatadi?** → **Topilma:** DMED (majburiy), qog'oz daftar (amalda hali), Telegram (konsultatsiya), MedElement/EMERGENCY.uz (ma'lumotnoma/telemeditsina). → **Qaror:** bizning raqobatchi — **qog'oz va odat**, dastur emas.
42. **MedElement nima qiladi?** → **Topilma:** tibbiy ma'lumotnoma + masofaviy konsultatsiya platformasi. → **Qaror:** u **reference**, biz **workflow** — to'qnashuv yo'q, potensial hamkor.
43. **Xalqaro scribe kompaniyalari kirib keladimi?** → **Topilma:** Nuance/Abridge/Suki globalda bor, lekin o'zbek tili va mahalliy protokol yo'q; kirish narxi yuqori. → **Qaror:** **til + protokol + narx** = himoya devori.
44. **Nega hozirgacha hech kim qilmagan?** → **Topilma:** Uzbek ASR faqat 2026 da yetuk bo'ldi (NavAI Whisper: medium model WER 9.73 makro, 753 soat inson transkripti). → **Qaror:** ✅ texnologik " enabling" 12 oy ichida paydo bo'ldi → **why now** juda aniq.
45. **Ochiq model bilan raqobat qilish mumkinmi?** Savol: vrach shunchaki ChatGPT'ga yozsa bo'lmaydimi? → **Topilma:** PISA ma'lumotlari ham AI chatbotlar ommalashganini ko'rsatadi (o'quvchilarning 49% haftalik); vrachlar ham ishlatadi. → **Qaror:** raqobat = **"ChatGPT + nusxalash"**. Bizning javob: **integratsiya + audit + protokol + mas'uliyat**, ya'ni "bitta tugma" qulayligi.
46. **Raqobat xaritasi (2x2).** → O'qlar: *Workflow chuqurligi* × *Til/mahalliy moslik*. → Lavozim: DMED (workflow bor, AI yo'q), ChatGPT (AI bor, workflow yo'q), xalqaro scribe (AI bor, til yo'q), **biz (ikkalasi)**. → **Qaror:** slayd 5 shu 2×2 bo'ladi.
47. **Hamkor bo'lish imkoniyati bormi?** → **Topilma:** DMED integratori UZINFOCOM; IT Park rezidentlari orasida tibbiy IT kompaniyalar bor. → **Qaror:** 90 kunlik reja: **UZINFOCOM bilan texnik uchrashuv** — raqobat emas, modul sifatida kirish.
48. **Dorixonalar kanal bo'la oladimi?** → **Topilma:** **8 000+ dorixona (66%)** tizimga ulangan; e-retsept bilan retsept sifati markazlashgan. → **Qaror:** dorixona — keyingi mahsulot (retseptni o'qish + INN almashtirish), hozir emas.
49. **Kim bizni birinchi bo'lib "sotib yuboradi"?** → **Topilma:** klinika direktori o'z vrachlarining shikoyatiga javob beradi; eng tez qaror — **yangi ochilgan klinika** (yangi xodim, yangi tizim). → **Qaror:** ICP = *Toshkentda 2024–2026 da ochilgan, 10–40 vrachli xususiy klinika*.
50. **Faza E xulosasi.** → **Xulosa:** raqobat **past**, lekin talab ham **uyg'otilmagan** (bu "blue ocean" emas, "education market"). → **Qaror:** sotuv tsikli 3–6 oy; hackathon'dan keyin **pilot** so'zi asosiy mahsulot bo'ladi.

## FAZA F (51–60). Texnologiya va ma'lumot

51. **Uzbek ASR bugungi holati.** → **Topilma:** NavAI Whisper (753 soat, medium WER 9.73%); USC 96 soat, UzbekVoice 594 soat ochiq. → **Qaror:** ✅ **fine-tune qilish uchun baza bor**; tibbiy lug'at qo'shish kerak.
52. **Lug'at muammosi qanchalik katta?** → **Gipoteza:** 400+ protokol, 3 100+ dori nomi (DARMON). → **Qaror:** **custom vocabulary biasing** (ASR'ga dori nomlari ro'yxatini berish) — arzon va samarali texnika; hackathon'da ko'rsatiladi.
53. **Arxitektura (demo uchun).** → Oqim: `audio → ASR (Whisper uz, lokal) → diarization (vrach/bemor) → LLM structured extraction → JSON (shikoyat/anamnez/obyektiv/tashxis/retsept) → hujjat` → **Qaror:** hamma narsa **lokal ishlaydigan** fallback bilan (internet uzilsa demo buzilmaydi).
54. **Nima uchun lokal?** → **Topilma:** ma'lumot lokalizatsiyasi talabi + tibbiy maxfiylik + klinika interneti beqaror. → **Qaror:** "offline-first" — kuchli sotuv argumenti.
55. **LLM tanlovi.** → **Topilma:** LLM API narxlari 2025→2026 da **~80% tushdi**; SLM-first arxitektura compute'ni **60–70%** tejaydi. → **Qaror:** kichik model (lokal, 7–8B) asosiy, katta model faqat murakkab holatlar uchun.
56. **Xatoni qanday ushlaymiz?** → Texnika: (a) **confidence** har bir maydon bo'yicha, (b) "aniqlanmadi" deb bo'sh qoldirish huquqi, (c) vrach tahriri → feedback loop, (d) **red-flag check** (allergiya, homiladorlik, yosh chegarasi). → **Qaror:** ✅ **"bo'sh qoldirish"** — eng muhim dizayn qarori: model taxmin qilmasligi kerak.
57. **Evaluation qanday bo'ladi?** → Metrikalar: WER, **entity F1** (tashxis, doza, INN), **tahrir foizi**, "xavfli xato" soni (0 bo'lishi shart). → **Qaror:** demo'da 5 ta oldindan tayyorlangan holat + jonli 1 ta.
58. **Xavfsizlik.** → **Topilma:** 78% hisobchilar/shifokorlar ma'lumot maxfiyligini asosiy xavf deb aytadi (Thomson Reuters). → **Qaror:** shifrlash, rol-asosli kirish, audit-log, "audio 24 soatdan keyin o'chiriladi".
59. **Integratsiya yo'li (90 kun).** → UZINFOCOM → DMED modul → HL7/FHIR moslashuvi → klinika HIS'lari (masalan, lokal tizimlar). ⏳ **Tekshirish:** klinikalarda qaysi HIS ishlatiladi (5 klinika so'rovi). → **Qaror:** birinchi integratsiya — **PDF/DOCX eksport** (bugun ham ishlaydi, ruxsat talab qilmaydi).
60. **Texnik Go/No-Go.** → **Xulosa:** 36 soatda "audio → tuzilgan hujjat" ishlaydigan prototip **mumkin** (ochiq Whisper + LLM + 20 ta sintetik dialog). Klinik aniqlik isbotlanmaydi, lekin **yo'nalish** ko'rsatiladi. → **Qaror:** demo ambitsiyasi **to'g'ri kalibrlanadi**: "bu prototip, bu 3 oylik pilot".

## FAZA G (61–70). Monetizatsiya va unit economics

61. **Narx modeli 1: vrach boshiga obuna.** → 200–300 ming so'm/oy. → **Kamchilik:** vrach almashsa churn.
62. **Narx modeli 2: klinika obunasi (10+ vrach).** → 2–4 mln so'm/oy. → **Afzallik:** barqaror, yillik shartnoma, bitta hisob-faktura. → **Qaror:** ✅ **asosiy model**.
63. **Narx modeli 3: "per document".** → 1 000 so'm/hujjat. → **Afzallik:** oson sotiladi ("sinab ko'ring"). → **Qaror:** kirish taklifi (entry offer) sifatida.
64. **Narx modeli 4: davlat tenderi.** → **Topilma:** 2026 da 100 ta AI loyihasi rejalashtirilgan; "Eng yaxshi AI loyihasi" tanlovi yiliga 2 marta. → **Qaror:** B2G alohida biznes-liniya, lekin **hackathon'dan keyin**.
65. **COGS (bir hujjat tannarxi).** → Hisob: 5 daqiqa audio → ASR ~$0.002 + LLM ~$0.003 + server ~$0.002 = **~$0.007/hujjat**. 1 vrach kuniga 20 hujjat = **$0.14/kun = ~$4/oy** → 250 ming so'm (~$20) ARPU bilan **gross margin ~80%**. → **Qaror:** ✅ model ishlaydi.
66. **CAC.** → Kanal: shifokorlar Telegram guruhlari, tibbiyot universitetlari, klinika assotsiatsiyalari, konferensiyalar. → **Gipoteza:** $300–600/klinika; LTV 24 oy × $200 = $4 800 → **LTV/CAC ~8–16×**. → **Qaror:** sog'lom.
67. **Churn riski.** → Sabab: vrach o'rganmasa tashlab qo'yadi (engagement muammosi). → **Qaror:** onboarding = klinikada **1 hafta joyida** o'qitish; KPI "3-kunda 10 hujjat" (activation).
68. **Expansion revenue.** → Modullar: audit/sifat hisoboti, tibbiy turizm tarjimasi, dorixona moduli, sug'urta hisoboti. → **Qaror:** NRR maqsadi **120%**.
69. **Moliyaviy model (24 oy).** → 120 klinika × 3 mln so'm/oy = **360 mln so'm/oy** ≈ $30k/oy; jamoa 8 kishi ($12k/oy) → **breakeven 6–9 oyda** mumkin. → **Qaror:** ✅ **kapitalga chanqoq emas** — bu IT Park Ventures uchun ideal profil.
70. **Faza G xulosasi.** → **Xulosa:** yaxshi unit economics, lekin **kichik baza** → o'sish **klinika zanjirlari** orqali (bir zanjir = 1 bitim, 20 klinika).

## FAZA H (71–80). GTM: kimga, qanday, qaysi so'zlar bilan

71. **Birinchi 10 mijoz qayerdan?** → Ro'yxat: Toshkentdagi yangi xususiy klinikalar, stomatologiya emas (hujjat oddiy) → **terapevtik/multiprofıl klinikalar**. → **Qaror:** 30 ta nomdan iborat ro'yxat **bugun** tuziladi.
72. **Sotuv suhbati qanday boshlanadi?** → ❌ "Bizda AI bor" → ✅ "Kuningizda nechta hujjat yozasiz? Kechqurun uyda qancha vaqt ishlaysiz?" → **Qaror:** **og'riq savoli** birinchi.
73. **Demo'da nima ko'rsatiladi?** → 90 sekund: vrach gapiradi (jonli), ekranda matn o'sadi, hujjat tayyor, "imzolash" tugmasi. → **Qaror:** ⚠️ jonli ovoz xavfli (shovqin) → 2 ta tayyor audio + 1 jonli.
74. **Narxni qachon aytish kerak?** → **Qoida:** qiymatdan keyin. "Bir vrach kuniga 1 soat tejasa, oyiga 20 soat — bu 250 ming so'mdan qimmatmi?"
75. **Kim "chempion" bo'ladi?** → Klinika ichida: **bosh vrach (zavuch)** yoki **bosh hamshira**. → **Qaror:** direktor emas, **bosh vrach** bilan ishlash.
76. **Ijtimoiy isbot.** → Hackathon natijasi + 3 pilot klinika + 1 tibbiyot universiteti. → **Qaror:** universitet (TMA, ToshPTI) — **talabalar orqali tarqatish** + ilmiy hamkorlik.
77. **Nima uchun vrach ishonadi?** → 3 narsa: (1) o'zbek tilida gapiradi, (2) "sen imzolaysan" — AI mas'uliyat olmaydi, (3) protokolga havola beradi. → **Qaror:** har bir tavsiya yonida **manba** (protokol raqami) ko'rsatiladi.
78. **Nima uchun klinika direktori to'laydi?** → ROI kalkulyatori: 10 vrach × 1 soat/kun × 250 kun = **2 500 soat/yil** ≈ 1.5 vrach ish yuki. → **Qaror:** pitch'da **aynan shu kalkulyator** ko'rsatiladi.
79. **Tarqatish kanallari ro'yxati.** → (a) tibbiyot konferensiyalari, (b) klinika egasi Telegram guruhlari, (c) TMA/Halqaro tibbiyot universiteti, (d) IT Park/GBC tadbirlari, (e) Sog'liq vazirligi pilotlari. → **Qaror:** 1-kanal eng arzon.
80. **Faza H xulosasi.** → **Xulosa:** GTM **inson-mi, marketing-mi**? → **inson** (founder-led sales). → **Qaror:** jamoada **sotuvchi-medik** bo'lishi shart; bo'lmasa — maslahat kengashi.

## FAZA I (81–90). Risklar, etika, javobgarlik

81. **R1 — klinik xato.** → Ehtimol: o'rtacha; Ta'sir: halokatli. → **Mitigatsiya:** hujjat = qoralama, vrach imzosi, red-flag check, "bo'sh qoldirish" huquqi.
82. **R2 — ma'lumot sizib chiqishi.** → Mitigatsiya: lokal hosting, shifrlash, audio o'chirish, DPIA hujjati, shartnomada javobgarlik chegarasi.
83. **R3 — DMED integratsiyasi rad etilishi.** → Mitigatsiya: PDF eksport bilan ishlash, UZINFOCOM bilan erta aloqa, "raqib emas, modul" pozitsiyasi.
84. **R4 — vrach o'rganmasligi (engagement).** → **Topilma:** ambient scribe'da qabul 7.7% → 57.8% ga o'sgan, lekin **enterprise rollout + workflow integratsiyasi** bilan. → **Qaror:** integratsiyasiz sotmaslik.
85. **R5 — til/dialekt xatolari.** → Mitigatsiya: 3 dialekt (Toshkent, Farg'ona, Xorazm) bo'yicha test; xato foizini ochiq e'lon qilish (halollik = brend).
86. **R6 — katta o'yinchi kirib kelishi.** → Mitigatsiya: hujjat formatini mahalliy protokolga bog'lash (o'tish narxi), klinikalar bilan 2 yillik shartnoma.
87. **R7 — regulyatsiya keskin o'zgarishi.** → Mitigatsiya: PF-141 etika qoidalari loyihasida **ishtirok etish** (ochiq muhokama) — kichik kompaniya uchun eng katta leverage.
88. **R8 — noto'g'ri "tashxis" da'vosi.** → **Qaror:** marketingda "diagnosis" so'zi **taqiqlanadi**; faqat "documentation", "recall", "safety check".
89. **Etika: to'lov modeli.** → Farmakompaniya pul to'lab, INN tanlanishiga ta'sir qilmasligi shart. → **Qaror:** **yozma siyosat** e'lon qilinadi (hakamlar uchun kuchli signal).
90. **Faza I xulosasi.** → **Xulosa:** risklar boshqariladi, lekin **R3 va R4** hackathon'dan keyin ham eng qiyin. → **Qaror:** 90 kunlik reja **aynan shu 2 riskni** yechishga bag'ishlanadi.

## FAZA J (91–100). Hackathon sintezi (agar shu g'oya tanlansa)

91. **Demo 1 (asosiy):** 90 sekundlik audio → tuzilgan hujjat, ekranda real vaqtda.
92. **Demo 2 (xavfsizlik):** ataylab xato qilingan audio (noto'g'ri doza) → AI **bayroq** ko'taradi, "bo'sh qoldiradi".
93. **Demo 3 (iqtisod):** 1 hujjat → 4 daqiqa; qo'l bilan → 12 daqiqa; kalkulyator.
94. **Metrika ekrani:** WER, entity F1, tahrir foizi — 5 test holati bo'yicha.
95. **Arxitektura slaydi:** offline-first, lokal, audit-log.
96. **Bozor slaydi:** 9 000+ klinika, 27 vrach/10k, DMED 37 mln.
97. **Why now slaydi:** NavAI Whisper 2026 + DMED majburiy + e-retsept 2027.
98. **Pitch hook:** "Vrach 17 daqiqaning yarmini klaviaturaga sarflaydi. Bemor esa qarab turibdi."
99. **Hakam savoliga tayyor javob:** "Bu tashxis qo'yadimi?" → "Yo'q. Va bu **ataylab** shunday."
100. **Yakuniy baho: 73.2/100.** Kuchli: ijtimoiy ta'sir, hikoya, davlat prioriteti. Zaif: ma'lumotga kirish, demo barqarorligi, uzun sotuv tsikli, klinik javobgarlik.

---

# 4. G'OYA №2 — **USTOZ AI**
## O'quv dasturiga bog'langan, javob bermaydigan repetitor + o'qituvchi paneli

**Trek:** Ta'lim ("Formation")
**Bir qatorda:** 5–11-sinf o'quvchisi uchun o'zbek tilidagi AI-repetitor: mavzuni **tushuntiradi**, **savol beradi**, **javobni bermaydi**, xatosini topadi, o'qituvchiga **har bir o'quvchining zaif nuqtalari xaritasini** beradi.
**Kimga:** B2C — ota-onalar (repetitorga pul to'layotganlar); B2B2C — xususiy o'quv markazlari (551 xususiy maktab, minglab kurslar); B2G — maktablar.
**Nima uchun kerak:** O'zbekistonda 6.87 mln o'quvchi, 577 700 o'qituvchi, o'qituvchi **72.5% ayol** va sinfda 30+ o'quvchi. Har bir o'quvchiga individual yondashish **fizik jihatdan imkonsiz** — bu bo'shliqni repetitorlar to'ldiradi, lekin ular **qimmat va shaharda**.

---

## FAZA A (1–10). Muammo va mijoz anatomiyasi

1. **Muammo kimda?** → Uch tomon: o'quvchi (tushunmaydi), ota-ona (repetitor qimmat), o'qituvchi (30 o'quvchi). → **Qaror:** pul to'lovchi = **ota-ona**, foydalanuvchi = **o'quvchi**, ta'sirchan = **o'qituvchi** → pitch'da 3 rol, 3 foyda.
2. **Repetitor bozori qanchalik katta?** → **Topilma:** global repetitorlik bozori **$143 mlrd (2026)**, Osiyo-Tinch okeani 54.5%; AI-tutor segmenti **$2.7 mlrd → $17.7 mlrd (2033), 30.5% CAGR**. → **Qaror:** bozor bor; O'zbekiston ulushi kichik, lekin **o'sish sur'ati** muhim.
3. **O'zbekistonda "repetitor" narxi qancha?** ⏳ **Tekshirish:** Toshkentda guruh darsi 150–400 ming so'm/oy, individual 600 ming–1.5 mln so'm/oy (bozor kuzatuvi). → **Qaror:** B2C narx **29–49 ming so'm/oy** = repetitordan **10× arzon** → aniq qiymat taklifi.
4. **Ota-ona nimaga pul to'laydi?** → **Gipoteza:** imtihon natijasi (DTM/milliy sertifikat), baho, "boshqa bolalar olayapti" bosimi. → **Qaror:** marketing **natija**ga, mahsulot **odat**ga quriladi.
5. **O'qituvchi nimadan shikoyat qiladi?** → **Topilma (TALIS 2024):** o'qituvchilarning **62%** ishida AI ishlatgan (OECD 36%) — ya'ni **talab allaqachon bor**; 54% maktabda infra yo'qligini aytadi; 46% "AI bilan dars berish ko'nikmasi yo'q" demaydi (OECD 75%) — ya'ni **o'qituvchi tayyor, qurol yo'q**. → **Qaror:** ✅ eng kuchli insight: "o'qituvchi AI'ni allaqachon ishlatyapti, lekin **nazoratsiz**".
6. **O'quvchi nimadan charchaydi?** → **Topilma (PISA 2025):** 49% o'quvchi haftada kamida bir marta AI chatbot ishlatadi; 43% mavzuni o'rganish uchun; 37% matn yozish uchun. → **Qaror:** ⚠️ **raqobatchi — ChatGPT, bepul**. Biz "yaxshiroq ChatGPT" emas, **"dastur + odat + nazorat"** sotamiz.
7. **Dasturga bog'lanish muhimmi?** → **Gipoteza:** ota-ona "maktab dasturiga mos" so'zini qidiradi. → **Qaror:** ✅ **curriculum alignment = asosiy differensiator** (ChatGPT bilmaydi qaysi sinfda nima o'tiladi).
8. **Sinflar soni va yuk.** → **Topilma:** 11 118 maktab, bir maktabga o'rtacha **619 o'quvchi**; 2026/27 da 1-sinfga **795 000** bola keladi. → **Qaror:** kontent hajmi katta → **AI bilan generatsiya + o'qituvchi tekshiruvi** gibrid modeli.
9. **Eng og'riqli nuqta qayerda?** → **Gipoteza:** 9-sinf (imtihon tanlovi), 11-sinf (DTM), 5-sinf (o'tish). → **Qaror:** **wedge = 9-sinf matematika + ingliz tili** (eng ko'p repetitor olinadigan fanlar).
10. **Muammo bayoni.** → *"O'zbekistonda 6.87 mln o'quvchi bor, o'qituvchi boshiga 12 o'quvchi, lekin individual tushuntirish faqat Toshkentda va faqat to'lovchi oilalar uchun mavjud. Qishloqdagi bola uchun 'tushunmagani'ni so'raydigan odam yo'q."*

## FAZA B (11–20). Regulyatsiya, kontent huquqi, ma'lumot

11. **Darsliklar huquqi kimda?** → **Topilma:** darsliklar davlat tomonidan nashr etiladi (Respublika ta'lim markazi). ⏳ **Tekshirish:** matn va topshiriqlardan foydalanish sharti, ochiq litsenziya bormi. → **Qaror:** 🔴 **darslik matnini ko'chirmaslik**; **dastur mavzulari ro'yxatiga** (topic list) tayanish — bu huquqiy jihatdan xavfsiz.
12. **Mavzular ro'yxati ochiqmi?** → ⏳ **Tekshirish:** Davlat ta'lim standarti (DTM) va fan dasturlari. → **Qaror:** dastur ro'yxati — mahsulotning "skeleti"; 2 hafta ichida qo'lda kiritiladi.
13. **Bolalar ma'lumoti (COPPA/GDPR-K analogi).** → **Topilma:** O'zbekistonda shaxsiy ma'lumotlar qonuni; 18 yoshgacha — ota-ona roziligi talabi. ⏳ **Tekshirish:** aniq yosh chegarasi. → **Qaror:** **ota-ona akkaunti** orqali ro'yxatdan o'tish, minimal ma'lumot (ism/telefon).
14. **Ta'lim vazirligi bilan ishlash tartibi.** → **Topilma:** UP-189: 2026/2027 o'quv yilidan **AI fanlari o'quv dasturlariga kiritiladi**; 15 ta AI laboratoriyasi universitetlarda. → **Qaror:** ✅ **hukumat bizning mahsulotni "infratuzilma" deb qabul qilishga tayyor** — B2G yo'li ochiq.
15. **Maktab infratuzilmasi tayyormi?** → **Topilma (TALIS):** 54% o'qituvchi maktabda AI uchun infra yo'q deydi; PISA: 69% o'quvchi telefon taqiqlangan maktabda. → **Qaror:** 🔴 B2G mahsuloti **offline/arzon qurilma** bilan ishlashi kerak; B2C esa **ota-ona telefoni** (bu to'g'ri yo'l).
16. **Telefon taqiqi muammomi?** → **Topilma:** 69% o'quvchi taqiq ostida (OECD 49%). → **Qaror:** maktabda ishlatish modeli **o'qituvchi proyektori orqali** (sinf ekrani), o'quvchi uyda.
17. **Imtihon tizimi (DTM) formati.** ⏳ **Tekshirish:** 2026 holatiga test formati, milliy sertifikat talablari. → **Qaror:** **test-generator** moduli (mavzu → 20 savol → tushuntirish) eng tez quriladigan qiymat.
18. **Til siyosati.** → **Topilma:** ta'lim o'zbek va rus tillarida; qoraqalpoq ham. → **Qaror:** **2 til (uz/ru)** birinchi versiyada — bu ham mahsulot, ham bozor 2×.
19. **O'qituvchi malakasi.** → **Topilma:** TALIS: 62% AI ishlatadi; eng ko'p **dars rejasi (91%)**, mavzuni o'rganish (92%), o'quvchi natijalarini ko'rish (86%). → **Qaror:** ✅ **o'qituvchi uchun eng kerakli funksiya — dars rejasi va natija tahlili**, tutor emas. Ikki xil mahsulot!
20. **Faza B xulosasi.** → **Go:** huquqiy jihatdan yurish mumkin (darsliksiz, dastur asosida). **Risk:** ma'lumot himoyasi va B2G infra. → **Qaror:** hackathon demo **B2C mobil/Telegram** yo'nalishida.

## FAZA C (21–30). Bozor hajmi: TAM / SAM / SOM

21. **TAM — o'quvchilar.** → 6.87 mln maktab o'quvchisi; 5–11 sinf ≈ **4.4 mln**. → **Qaror:** 1% penetratsiya = 44 000 foydalanuvchi.
22. **TAM — pulda (B2C).** → 4.4 mln × 30 000 so'm/oy × 12 = **1.58 trln so'm/yil (~$130 mln)**. → **Qaror:** nazariy jihatdan katta; real penetratsiya 1–3%.
23. **To'lov qobiliyati.** → **Topilma:** o'rtacha ish haqi va oila byudjeti; repetitor xarajati oila uchun katta ulush. ⏳ **Tekshirish:** o'rtacha oylik ish haqi 2026 (Statkom). → **Qaror:** narx **29 000 so'm/oy** (bir kishi kuniga ~1000 so'm) — "bir non narxi" pozitsiyasi.
24. **SAM — repetitor olinadigan oilalar.** → **Gipoteza:** shahar aholisining 25–35% repetitor to'laydi ≈ **500–700 ming oila**. → **Hisob:** 100 000 obunachi × 30 000 = **3 mlrd so'm/oy ($250k/oy)** → **$3 mln ARR**.
25. **SOM (24 oy).** → 60 000 obunachi → **$1.8 mln ARR**; B2B2C qo'shilsa **+$400k**. → **Qaror:** seed uchun yetarli hikoya.
26. **B2B2C — o'quv markazlari.** → **Topilma:** 551 xususiy maktab (+21.1%); Toshkentda 145. Minglab o'quv kurslari (Lerna 793 kurs ro'yxatga olgan). → **Qaror:** o'quv markazi uchun "AI yordamchi o'qituvchi" = xarajatni kamaytirish → **yuqori ARPU ($100–300/oy)**.
27. **B2G — maktablar.** → 11 118 maktab; davlat byudjeti bor, lekin tender uzoq. → **Qaror:** B2G **2-bosqich** (12+ oy), pilot orqali.
28. **Ikkinchi mahsulot: o'qituvchi copilot.** → **Topilma:** EduBaza (2026-yil yanvarda, $50k, $1 mln baho) aynan shu bozorda. → **Qaror:** ⚠️ **to'g'ridan-to'g'ri raqobat**; lekin EduBaza — veb, biz **o'quvchi natijalari** bilan bog'lansak differensiatsiya bor.
29. **Eksport salohiyati.** → Turkiy tillar: Ozarbayjon, Qozog'iston (lotin alifbosi), Qirg'iziston. → **Topilma:** global AI-tutor kompaniyalari mahalliy dasturga moslashmaydi. → **Qaror:** **"curriculum-as-a-service"** — uzoq muddatli moat.
30. **Bozor xulosasi.** → **Xulosa:** eng katta bozor, eng qiyin monetizatsiya (past ARPU, yuqori CAC, o'chib ketish). → **Qaror:** hackathon uchun jozibali, **biznes uchun qiyin**.

## FAZA D (31–40). Ilmiy dalillar: AI-tutor ishlaydimi yoki zararmi?

31. **Eng katta RCT nima dedi?** → **Topilma:** Khanmigo, 18 maktab, 2 yil, 6 900 o'quvchi-davr: **+1.26 persentil/chorak ≈ 0.06–0.08 SD/yil**, "AI'siz Khan Academy mashqi bilan o'xshash", narxi **$15/o'quvchi/yil**. → **Qaror:** ⚠️ ta'sir **kichik**, lekin **musbat va arzon**.
32. **Nega ta'sir kichik?** → **Topilma:** median o'quvchi AI bilan **mashq kunlarining faqat 1/3**ida gaplashgan; xato qilgan sessiyalarning **17%**ida. → **Qaror:** ✅ **asosiy muammo — model emas, ENGAGEMENT.** Bizning mahsulot shu muammoni yechishga qurilishi kerak.
33. **Eng katta ta'sir qayerda olingan?** → **Topilma:** Garvard fizika RCT: maxsus qurilgan tutor **0.63 SD** (4.5 vs 3.5 ball), **49 vs 60 daqiqa**. → **Qaror:** ✅ "yaxshi qurilgan tutor" 10× kuchliroq → **pedagogik dizayn** = mahsulotning yadrosi.
34. **Javob beruvchi AI nima qiladi?** → **Topilma:** ~1 000 o'quvchi bilan tajriba: javob beruvchi AI mashq natijasini **+48%**, keyin AI olinganda imtihonni **−17%**; hint-first versiya mashqni **+127%**, imtihon **o'zgarmagan**. → **Qaror:** 🔴 **javob berish taqiqlanadi**. Bu eng muhim texnik qaror.
35. **Inson repetitor bilan solishtirsa?** → **Topilma:** inson repetitor o'rtacha **0.288 SD** (PreK-12 RCT meta). → **Qaror:** bizning maqsad **0.10–0.15 SD** — real va sotiladigan.
36. **AI o'qituvchiga yordam bersa?** → **Topilma:** Tutor CoPilot RCT (900 repetitor, 1 800 o'quvchi): AI maslahati olgan repetitorlar **+4 p.p.** mavzuni o'zlashtirish; **eng katta foyda — zaif repetitorlarga**. → **Qaror:** ✅ **B2B2C strategiyasi ilmiy asoslangan**: repetitorni kuchaytirish, uni almashtirish emas.
37. **Struktura muhimmi?** → **Topilma:** AI + mastery practice: amaliyotdan keyingi urinishda **+3.1 p.p.**; "gains come with structure or a person". → **Qaror:** mahsulot **mastery-based** bo'lishi shart (o'zlashtirmaguncha keyingi mavzuga o'tmaydi).
38. **Motivatsiya.** → **Topilma:** Sal Khan: "motivation matters more than anyone expected". → **Qaror:** o'zbek madaniyatiga mos **o'yinlashtirish**: reyting, kunlik seriya (streak), ota-onaga haftalik hisobot.
39. **PISA mahalliy konteksti.** → **Topilma:** O'zbekistonda raqamli chalg'ish kuchli: chalg'igan o'quvchilar fanda **28 ball past** (OECD 11). → **Qaror:** ⚠️ telefon = chalg'ish manbai → mahsulot **qisqa sessiya (7–12 daqiqa)** va **bildirishnoma gigienasi** bilan.
40. **Xulosa: ilmiy asos bormi?** → **Ha, lekin shartli:** (a) hint-first, (b) struktura/mastery, (c) engagement dizayni, (d) inson ustidan nazorat, (e) past narx. → **Qaror:** ✅ bularning **5/5** bajarilishi pitch'da ko'rsatiladi — bu hakamlarni hayratlantiradigan "ilmiy slayd".

## FAZA E (41–50). Raqobat va alternativa

41. **Asosiy raqobatchi kim?** → **ChatGPT/Gemini — bepul**. → **Qaror:** biz "aqlliroq" emas, **"dasturga mos + nazoratli + o'zbekcha"** bo'lamiz.
42. **Mahalliy o'yinchilar.** → **Topilma:** EduBaza (AI dars rejasi, $50k), Mohirdev (IT kurslari, 50k+ o'quvchi), Najot Ta'lim (12k bitiruvchi), Lerna.uz (793 kurs marketplace), Prep.uz (rus tili). → **Qaror:** **maktab dasturi segmenti** bo'sh; IT-kurslar segmenti to'la — u yerga kirmaymiz.
43. **Xalqaro o'yinchilar.** → Khan Academy, Duolingo, Byju's, ChatGPT Study Mode (bepul). → **Topilma:** ChatGPT "Study Mode" bepul va guardrailed. → **Qaror:** 🔴 narx bosimi juda katta → **bepul qatlam shart** (freemium).
44. **O'quv markazlari o'z yechimini qurmoqda?** → **Gipoteza:** yo'q, ular CRM ishlatadi. → **Qaror:** B2B2C bo'sh.
45. **Nega o'qituvchilar hali AI'dan foydalanmaydi?** → **Topilma:** TALIS: faqat 46% "ko'nikma yo'q" deydi — ya'ni **asosiy to'siq ko'nikma emas, infratuzilma va ishonch**. → **Qaror:** mahsulot **"tushuntirib beradigan"** bo'lishi kerak (prompt yozish shart emas).
46. **Nima uchun ota-onalar allaqachon to'laydi?** → chunki natija ko'rinadi (baho, imtihon). → **Qaror:** bizning metrika ham **ko'rinadigan** bo'lishi kerak: haftalik "nechta mavzu o'zlashtirildi".
47. **Raqobat 2×2.** → O'qlar: *Dasturga moslik* × *Nazorat/natija*. → Lavozim: ChatGPT (0,0), Khan Academy (1,0, ingliz), EduBaza (o'qituvchi, 0), **biz (1,1)**.
48. **O'qituvchi bizni raqib deb ko'radimi?** → **Xavf:** ha, agar "o'qituvchini almashtiradi" desak. → **Qaror:** pozitsiya: **"o'qituvchining yordamchisi"** — TALIS ma'lumotiga tayangan holda.
49. **Kim birinchi sotib oladi?** → ICP: Toshkent, 8–10-sinf, matematika/ingliz, ota-ona allaqachon repetitor to'laydi. → **Qaror:** 200 ta shunday oila topish = 2 hafta.
50. **Faza E xulosasi.** → **Xulosa:** raqobat **juda kuchli va bepul**. Faqat 2 himoya: **dastur + til + nazorat**. → **Qaror:** hackathon hakamlari uchun bu yetarli, investor uchun **yetarli emas**.

## FAZA F (51–60). Texnologiya va kontent

51. **Asosiy texnik qiyinchilik nima?** → **Kontent**, model emas. → **Qaror:** 5-sinf matematika (1 fan, 1 sinf) = 120–160 mavzu; AI bilan generatsiya + o'qituvchi tekshiruvi.
52. **Hint-first qanday amalga oshiriladi?** → Texnika: Socratic prompting + **javob detektori** (model javobni aytmoqchi bo'lsa bloklaydi) + **step-checker** (har qadamni tekshiradi). → **Qaror:** ✅ **"answer-guard"** — demo'da ko'rsatiladigan eng ta'sirli detal.
53. **Matematikani qanday tekshiradi?** → SymPy/Wolfram kabi **ramziy hisoblash** moduli → LLM'ning matematik xatosi yo'qoladi. → **Qaror:** ✅ gibrid: LLM tushuntiradi, **SymPy tekshiradi**.
54. **Ovoz kerakmi?** → **Topilma:** O'zbek ASR endi yetuk (NavAI Whisper, WER ~9.7%); TTS ham mavjud. → **Qaror:** 2-versiyada **ovozli tutor** (qishloqda klaviatura sekin yozadigan bolalar uchun) — kuchli differensiator.
55. **Platforma tanlovi.** → **Topilma:** Telegram **25 mln foydalanuvchi (85%)**; Click/Payme to'lov. → **Qaror:** ✅ **Telegram Mini App** birinchi kanal (CAC eng past), keyin iOS/Android.
56. **Ma'lumot yig'ish va maxfiylik.** → Minimal: ism, sinf, javoblar. → **Qaror:** ota-ona panelida **nima saqlanayotgani** ochiq ko'rsatiladi (ishonch).
57. **Adaptivlik.** → Algoritm: **knowledge tracing** (BKT/DKT) — qaysi mavzuda zaif. → **Qaror:** oddiy versiya: mavzu bo'yicha masteriy foizi; demo uchun yetarli.
58. **O'qituvchi paneli.** → Funksiya: 30 o'quvchining zaif mavzulari issiqlik xaritasi + avtomatik guruhlash ("5 o'quvchi kasrlarda zaif → ularga alohida topshiriq"). → **Qaror:** ✅ bu **B2B sotuvning kaliti**.
59. **Evaluation.** → Metrikalar: mavzu bo'yicha pre/post test, **engagement** (kunlik faol daqiqa), **tugatish foizi**, ota-ona hisobotini ochish foizi. → **Qaror:** A/B test: hint-first vs oddiy LLM — 2 haftalik pilot.
60. **Texnik Go/No-Go.** → 36 soatda: 1 fan × 1 sinf × 20 mavzu + hint-guard + Telegram bot = **mumkin**. → **Qaror:** demo tayyor.

## FAZA G (61–70). Monetizatsiya va unit economics

61. **Narx.** → Freemium: kuniga 5 savol bepul; **29 000 so'm/oy** cheksiz. → **Qaror:** ota-ona uchun "bir repetitor darsining yarmi".
62. **To'lov infra.** → Click/Payme (**80% onlayn to'lov**). → **Qaror:** Telegram ichida to'lov — ishqalanish minimal.
63. **CAC.** → Kanal: ota-onalar Telegram guruhlari, Instagram reels, maktab o'qituvchilari orqali tavsiya, mikro-influencerlar. → **Gipoteza:** CAC **$3–8**; ARPU $3/oy; LTV (6 oy) $18 → **LTV/CAC ~2.5–6×**. → **Qaror:** ⚠️ chegarada; **churn** hal qiluvchi.
64. **Churn.** → **Topilma:** Khanmigo tajribasida engagement pastligi asosiy muammo. → **Qaror:** 30 kunlik retention KPI **>35%** bo'lmasa, model buziladi.
65. **COGS.** → LLM + hosting: 1 faol o'quvchi/oy ~$0.30–0.60 → ARPU $3 da **margin 80–90%**. → **Qaror:** ✅ yaxshi.
66. **B2B2C narx.** → O'quv markazi: **$150–300/oy** (50–150 o'quvchi) → ARPU 10× yuqori, CAC past. → **Qaror:** ✅ **fokus B2B2C** (bu muhim strategik burilish).
67. **B2G.** → Maktab litsenziyasi: 11 118 maktab; bitta maktab $200–500/yil → **$2–5 mln TAM**. → **Qaror:** tender 12+ oy.
68. **Moliyaviy model 24 oy.** → 100 o'quv markazi ($200) = $20k/oy + 20 000 B2C ($3) = $60k/oy → **$80k/oy = ~$1 mln ARR**. → **Qaror:** ishonchli.
69. **Kapital talabi.** → Kontent + sotuv + 6 kishi = **$25–40k/oy** burn → seed $400–600k. → **Qaror:** IT Park Ventures + angel.
70. **Faza G xulosasi.** → **Xulosa:** model ishlaydi, **agar B2B2C** bo'lsa. B2C-only = o'lim.

## FAZA H (71–80). GTM

71. **Birinchi kanal.** → O'qituvchilar (ular 62% allaqachon AI ishlatadi) → ular o'quvchilarga tavsiya qiladi. → **Qaror:** "teacher-led growth".
72. **Ikkinchi kanal.** → Ota-onalar Telegram guruhlari (har bir sinfda 1–3 guruh). → **Qaror:** 50 guruhga kirish = 25 000 ota-ona.
73. **Uchinchi kanal.** → Xususiy maktablar (551) — direktorga "differensiatsiya" sifatida sotish.
74. **Demo skript.** → 60 sekund: "Menga kasrlarni tushuntir" → AI tushuntiradi → savol beradi → bola xato qiladi → AI **javobni aytmaydi**, qadam bilan olib boradi → o'qituvchi panelida zaif nuqta paydo bo'ladi.
75. **Nima ko'rsatilmaydi?** → "Biz 1 mln o'quvchi olamiz" — ishonchsizlik. → **Qaror:** faqat **o'lchangan** narsalar.
76. **Ijtimoiy ta'sir hikoyasi.** → Qishloq maktabi, 30 o'quvchi, 1 o'qituvchi → "bu bola uchun repetitor yo'q edi". → **Qaror:** ✅ "Eng dolzarb ijtimoiy loyiha" nominatsiyasi uchun aynan shu.
77. **Nima uchun o'qituvchi qo'rqmaydi?** → "Biz sizni almashtirmaymiz — biz sizning 30 o'quvchingizni ko'radigan ko'zingiz bo'lamiz".
78. **Nima uchun ota-ona ishonadi?** → haftalik hisobot: "farzandingiz 3 mavzuni o'zlashtirdi, 2 tasida qiynaldi" — **ko'rinadigan natija**.
79. **Tarqatish bo'yicha xulosa.** → B2B2C → B2C → B2G tartibi. → **Qaror:** hackathon'da **B2C demo**, lekin **pitch'da B2B2C biznes-model**.
80. **Faza H xulosasi.** → **Xulosa:** GTM ishlaydi, lekin **sekin** va **qimmat**.

## FAZA I (81–90). Risklar, etika

81. **R1 — engagement/churn.** → Eng katta risk. → Mitigatsiya: 7-daqiqalik sessiya, streak, ota-ona hisoboti, o'qituvchi bosimi.
82. **R2 — bepul raqobat (ChatGPT).** → Mitigatsiya: dastur, til, nazorat, ota-ona paneli.
83. **R3 — akademik halollik.** → **Topilma:** javob beruvchi AI imtihon natijasini **17% pasaytiradi**. → **Qaror:** answer-guard + "imtihon rejimi" (AI faqat savol beradi).
84. **R4 — kontent xatosi.** → Mitigatsiya: inson tekshiruvi (fan o'qituvchisi), "xato xabar berish" tugmasi.
85. **R5 — bolalar maxfiyligi.** → Mitigatsiya: minimal ma'lumot, ota-ona akkaunti, o'chirish huquqi.
86. **R6 — o'qituvchilar qarshiligi.** → Mitigatsiya: kasaba uyushmalari/mintaqaviy metodbirlashmalar bilan ishlash.
87. **R7 — monetizatsiya sekinligi.** → Mitigatsiya: B2B2C birinchi.
88. **R8 — "yana bir AI tutor" charchog'i.** → **Topilma:** global bozorda 10+ tutor bor; hakamlar ham charchagan. → **Qaror:** **pozitsiya "natija hisoboti"** bo'lishi kerak, "chat" emas.
89. **Etika: neyro-xilma-xillik.** → Zaif o'quvchilarni yorliqlashdan saqlanish; o'qituvchi panelida "zaif" emas, **"qo'shimcha mashq kerak"** deyiladi.
90. **Faza I xulosasi.** → Risklar **boshqariladigan**, lekin **biznes-risk (churn + bepul raqobat)** texnik riskdan kattaroq.

## FAZA J (91–100). Hackathon sintezi

91. **Demo 1:** matematika, hint-first, jonli.
92. **Demo 2:** o'qituvchi paneli — 30 o'quvchi issiqlik xaritasi.
93. **Demo 3:** "answer-guard" — AI javobni aytishga urinadi, bloklaydi.
94. **Ilmiy slayd:** Khanmigo 0.06–0.08 SD, Garvard 0.63 SD, +48%/−17% tajribasi.
95. **Bozor slayd:** 6.87 mln o'quvchi, 577.7k o'qituvchi, 49% allaqachon AI ishlatadi.
96. **Why now:** PISA 2025 natijalari + UP-189 (AI fan sifatida 2026/27) + Telegram 25 mln.
97. **Pitch hook:** "Qishloqdagi bolaning 'tushunmadim' deb so'raydigan odami yo'q."
98. **Hakam savoli:** "Bu ChatGPT'dan nimasi bilan farq qiladi?" → "U dasturni bilmaydi, javobni beradi va ota-onaga hisobot bermaydi."
99. **Asosiy zaiflik:** engagement va monetizatsiya.
100. **Yakuniy baho: 74.0/100.** Kuchli: bozor hajmi, ijtimoiy ta'sir, ilmiy baza, demo osonligi. Zaif: bepul raqobat, churn, past ARPU, kontent huquqi.

---

# 5. G'OYA №3 — **HISOB AI**
## Telegram'dagi "AI-buxgalter": 1.24 mln kichik biznes uchun soliq va moliya yordamchisi

**Trek:** Tadbirkor
**Bir qatorda:** Tadbirkor rasm/PDF/ovoz yuboradi (faktura, chek, kvitansiya) → HISOB AI uni o'qiydi, tasniflaydi, soliq oqibatini aytadi, qaysi rejim foydali ekanini hisoblaydi, deklaratsiyaga tayyor fayl beradi va "sizni nima uchun risk-skor flag qildi" ni **o'zbek tilida tushuntiradi**.
**Kimga:** 1 236 100 mikrofirma/YaTT/o'zini band qilganlar; keyin ularga xizmat ko'rsatuvchi buxgalterlar va buxgalteriya firmalari (B2B2C).
**Nima uchun kerak:** 2026-yil boshidan soliq tizimi **bir vaqtning o'zida 4 ta katta o'zgarish**ni boshdan kechirdi. Tadbirkor qoidani tushunmaydi, buxgalter esa qimmat. Natija: jarima qo'rquvi, hisobotni kechiktirish, "soya"ga qaytish.

---

## FAZA A (1–10). Muammo va mijoz anatomiyasi

1. **Mijoz kim va nechta?** → **Topilma:** 01.01.2026 holatiga **1 201 600** faol kichik biznes subyekti; 01.07.2026 da **1 236 100** (526 700 mikrofirma, 375 100 YaTT, 334 400 dehqon xo'jaligi, 23 200 hunarmand). Alohida: **357 883** faol YaTT (01.10.2026), Toshkent sh. 56 858. → **Qaror:** yadro mijoz = **mikrofirma + YaTT ≈ 900 000**. Bu yetarli, hatto 1% = 9 000 to'lovchi.
2. **Ular iqtisodiyotda qanchalik muhim?** → **Topilma:** kichik biznes **YaIMning 52.2%** (2025), 1-yarim 2026 — **50.5%**; bandlikning **~74% (10.5 mln kishi)**. → **Qaror:** ✅ **"ijtimoiy ta'sir" argumenti ham shu yerda**: biznesni rasmiylashtirish = davlat uchun milliardlab soliq bazasi.
3. **Og'riq aniq nima?** → 5 ta: (a) qaysi soliq rejimi foydali? (b) qanday qilib jarimaga tushmaslik? (c) buxgalter qimmat; (d) deklaratsiya muddati; (e) "nima uchun mening hisob-fakturam flag qilindi?" → **Qaror:** mahsulot **5 modul** = 5 og'riq.
4. **Tadbirkor bugun buxgalterga qancha to'laydi?** ⏳ **Tekshirish (bozor kuzatuvi):** kichik biznes uchun autsorsing buxgalteriya **500 ming – 2 mln so'm/oy**; Toshkentda 800 ming – 1.5 mln so'm odatiy. → **Qaror:** bizning narx **99–199 ming so'm/oy** = **5–10× arzonroq** → aniq qiymat taklifi.
5. **Buxgalter o'rnini bosa olamizmi?** → **Yo'q, va bu yaxshi.** → **Topilma:** Intuit tadqiqoti: "AI where it counts, human when it matters"; AI buxgalterni **almashtirmaydi**, uning **bir mijozga sarflagan vaqtini 50–60% qisqartiradi**. → **Qaror:** ✅ ikki tomonlama model: **tadbirkorga AI**, **buxgalterga super-qurol** (B2B2C).
6. **Tadbirkor nima qilishdan qo'rqadi?** → **Jarima va tekshiruv.** → **Topilma (UP-100):** risk **500 mln so'mgacha** bo'lsa soliq tekshiruvi o'tkazilmaydi, **100 mln so'mgacha** bo'lsa joyida tekshiruv yo'q; tadbirkor xatoni **o'zi tuzatishi** mumkin. → **Qaror:** ✅ mahsulot "jarimasiz o'zini tuzatish" vositasiga aylanadi — **davlat siyosatiga to'liq mos**.
7. **2026 da nima o'zgardi — bir jadvalda?** → (1) **ZRU-1108** (25.12.2025): avtomatik tayyorlangan deklaratsiyalar + o'zini band qilganlarga e-faktura majburiyati; (2) **UP-153**: real-time **AI QQS faktura risk-skor**; (3) **UP-100** (26.05.2026): **6% ixtiyoriy QQS**, chegara **1 mlrd → 12 000 BRV (~4.94 mlrd; 01.09.2026 dan ~5.28 mlrd)**, 6% rejimda **foyda solig'i 0% va deklaratsiya yo'q**, lekin **kirim QQS hisobga olinmaydi**; (4) **PP-247** (12.08.2025): YaTT/o'zini band qilganlar uchun **1% aylanma** (1 mlrd so'mgacha). → **Qaror:** ⚡ **bu 4 ta o'zgarish = 4 ta mahsulot moduli**, va ular **2026-yil ichida** kuchga kirdi → "why now" mutlaqo aniq.
8. **Kim eng ko'p zarar ko'radi?** → **Topilma:** UP-100 bo'yicha **600 000+** kichik subyekt yangi imtiyozlardan foydalanadi; lekin 6% rejimda **kirim QQS yo'q** — ya'ni noto'g'ri tanlov **foyda solig'ini yo'qotib, QQS'ni ko'paytirishi** mumkin. → **Qaror:** ✅ **"rejim simulyatori" eng ko'p qiymat beradigan bitta funksiya**.
9. **Muammo bayoni (pitch uchun).** → *"2026-yil 1-yanvardan O'zbekistonda 1.2 mln tadbirkor bir vaqtda yangi soliq qoidalari, avtomatik deklaratsiya va AI risk-skor bilan yuzlashdi. Ular qoidani tushunmaydi, buxgalter esa oyiga 1 mln so'm turadi. Natija — jarima qo'rquvi va yana soyaga qaytish."*
10. **Bitta jumlada yechim.** → *"HISOB AI — Telegram'dagi buxgalter: fakturani rasmga oling, soliq oqibatini o'zbek tilida bilib oling."*

## FAZA B (11–20). Regulyatsiya, ma'lumot, huquqiy chegara

11. **E-faktura tizimi qanday ishlaydi?** → **Topilma:** EHF (elektron hisob-faktura) 2020-yildan majburiy; 2026 dan **o'zini band qilganlar ham** chiqaradi; QQS 12% (2023 dan). → **Qaror:** ✅ bizning asosiy kirish nuqtasi — **EHF** (u hamma uchun majburiy va raqamli).
12. **EHF ma'lumotiga kirish mumkinmi?** → ⏳ **Tekshirish:** `didox.uz`, `faktura.uz`, `my.soliq.uz` API'lari va tadbirkorning o'z kabinetidan eksport imkoniyati. → **Qaror:** eng qonuniy yo'l — **foydalanuvchi o'z hisobidan eksport qiladi** (biz hisobini saqlamaymiz). Bu huquqiy riskni nolga tushiradi.
13. **Soliq API'lari ochiqmi?** → ⏳ **Tekshirish:** soliq.uz / my.soliq.uz ochiq API, "Elektron hukumat" integratsiya reglamenti. → **Qaror:** birinchi versiyada **fayl yuklash** (Excel/PDF/rasm) — API'siz ham to'liq ishlaydi.
14. **AI risk-skor qanday ishlaydi?** → **Topilma:** UP-153 bilan **real vaqtda QQS faktura risk-tahlili** joriy etilgan; aniq algoritm ochiq emas. → **Qaror:** 🔴 biz "skoringni takrorlaymiz" demaymiz; **"flag sabablarini tushuntiramiz"** deymiz (qoidaga asoslangan checklist + LLM izohi).
15. **Buxgalteriya faoliyati litsenziyalanadimi?** → ⏳ **Tekshirish:** buxgalteriya xizmati litsenziya talab qiladimi (O'zbekistonda odatda yo'q, audit esa litsenziyali). → **Qaror:** ✅ **"maslahat va avtomatlashtirish"** pozitsiyasi — **audit emas**, **buxgalteriya xizmati emas**, **dasturiy vosita**. Shartnomada aniq yoziladi.
16. **Javobgarlik chegarasi.** → **Qaror:** foydalanuvchi shartnomasida: "vosita ma'lumot beradi, yakuniy qaror va deklaratsiya javobgarligi tadbirkorda/buxgalterda". Har bir javobda "manba: Soliq kodeksi moddasi" havolasi.
17. **Shaxsiy ma'lumotlar va tijorat siri.** → Moliyaviy ma'lumot = maxfiy; raqobatchi ko'rmasligi kerak. → **Qaror:** mahalliy hosting, shifrlash, agregat statistikadan boshqa narsa **sotilmaydi** (bank/CRM'ga lead sotish — **taqiqlanadi**, siyosatda yoziladi).
18. **E-IMZO.** → **Topilma:** e-retsept ham, EHF ham **ERI (E-IMZO)** bilan imzolanadi. → **Qaror:** demo'da E-IMZO'ni **simulyatsiya** qilamiz (haqiqiy imzo yo'q), lekin yo'l xaritasida integratsiya bor.
19. **Buxgalterlar uyushmasi/hamkorlik.** → ⏳ **Tekshirish:** O'zbekistonda buxgalterlar palatasi/assotsiatsiyasi, ularning a'zolari soni. → **Qaror:** **B2B2C kanal** — 1 buxgalter = 10–30 mijoz.
20. **Faza B xulosasi.** → **Go:** huquqiy jihatdan **eng toza** uch g'oyadan. Ma'lumot **foydalanuvchi tomonidan** beriladi, javobgarlik chegaralangan, davlat siyosatiga mos. → **Qaror:** ✅ hackathon uchun eng xavfsiz va eng tez demo.

## FAZA C (21–30). Bozor hajmi: TAM / SAM / SOM

21. **TAM (B2C, YaTT/mikrofirma).** → 900 000 subyekt × 150 000 so'm/oy × 12 = **1.62 trln so'm/yil (~$135 mln)**. → **Qaror:** bu **haqiqiy** raqam (Intuit modeli bilan solishtirsa: 8.5 mln obunachi × ~$30/oy).
22. **SAM.** → Faol, raqamli, bank hisobiga ega, e-faktura chiqaradigan subyektlar ≈ **350 000** → 350 000 × 150 000 × 12 = **630 mlrd so'm (~$52 mln)**.
23. **SOM (24 oy).** → 25 000 to'lovchi × 150 000 so'm = **3.75 mlrd so'm/oy (~$310k/oy)** = **$3.7 mln ARR**. → **Qaror:** seed/Series A uchun ishonchli.
24. **B2B2C (buxgalteriya firmalari).** → ⏳ **Tekshirish:** Toshkentda buxgalteriya autsorsing firmalari soni (ehtimol 1 000+). → **Hisob:** 300 firma × $100/oy = $30k/oy, lekin **CAC juda past** va har firma **o'z mijozlarini** olib keladi.
25. **B2G.** → **Topilma:** 2026 oxirigacha **100 ta AI loyihasi** davlat sektorida rejalashtirilgan; "Eng yaxshi AI loyihasi" tanlovi yiliga 2 marta. → **Qaror:** davlat **o'z xodimlariga** ham shunday vosita kerak (soliq inspektorlari tushuntirishga vaqt sarflaydi) — B2G moduli.
26. **Eksport: nega aynan shu mahsulot eksport bo'ladi?** → **Topilma:** Qozog'iston, Ozarbayjon, Gruziya, Qirg'iziston **o'xshash raqamli soliq islohotlarini** o'tkazmoqda (e-faktura + risk-skor global trend). → **Qaror:** ✅ mahsulot **"soliq qoidalari dvigateli"** bo'lsa, yangi davlat = yangi qoidalar fayli. Bu **haqiqiy skalalanuvchi arxitektura**.
27. **Nima uchun eksport oson?** → chunki **kodestan farqli** narsa: soliq mantiqi = qoidalar to'plami + hujjat formati; tarjima qilinadi, qayta yozilmaydi.
28. **Bozor o'sishi.** → **Topilma:** kichik biznes soni o'smoqda (1.20 → 1.24 mln 6 oyda); 2026 da SME'larga **140 trln so'm** kredit → yangi bizneslar ko'payadi → **baza o'sadi**.
29. **Raqamli savdo ulushi.** → **Topilma:** Jahon banki: SME savdosining **<30%** elektron. → **Qarar:** ya'ni qolgan 70% hujjatni **rasm/qog'oz**da oladi → **OCR modulining ahamiyati katta**.
30. **Bozor xulosasi.** → **Xulosa:** uch g'oya orasida **eng katta va eng "to'lanadigan"** bozor, eng past CAC, eng tez sotuv tsikli (kunlar, oylar emas).

## FAZA D (31–40). Global dalillar: AI-buxgalteriya ishlaydimi?

31. **Global yetakchi raqamlari.** → **Topilma:** Intuit QuickBooks **8.5 mln+ obunachi**, **7.5 mln** biznes AI funksiyalardan foydalanadi; AI Platformaga **$1 mlrd** investitsiya. → **Qaror:** ✅ model isbotlangan.
32. **Tejash qancha?** → **Topilma:** AI-buxgalteriya bilan kichik biznes **oyiga 10 soat** tejaydi, xarajat **40–50%** tushadi; bank rekonkiliatsiyasi **70% tezroq**; tranzaksiya tasnifi **85–95%** avtomatik. → **Qaror:** pitch'da "10 soat/oy" — eng tushunarli raqam.
33. **Adoption qanchalik tez?** → **Topilma:** AQSh kichik bizneslarining **45%** (2025) AI-buxgalteriya ishlatadi (2024 da 28%); Intuit 2026 hisoboti: AQSh SMB'larining **3/4**i muntazam AI ishlatadi (34 000 egasi so'rovda). → **Qaror:** O'zbekiston **2–3 yil orqada** → ya'ni **hozir kirish vaqti**.
34. **Buxgalterlar AI'ni qabul qildimi?** → **Topilma:** professional buxgalterlarning **82%** AI vositalarini ishlatadi; **72%** firma AI joriy etgan; haftasiga **4.6 soat** tejaydi. → **Qaror:** ✅ **buxgalter — dushman emas, kanal**.
35. **Xatarlar/cheklovlar.** → **Topilma:** 78% buxgalter **mijoz ma'lumoti maxfiyligi**ni asosiy xavf deb biladi; deyarli barcha AI yechimlar **inson tekshiruvini** talab qiladi. → **Qaror:** "human-in-the-loop" dizayn + mahalliy hosting = sotuv argumenti.
36. **Agentik AI bozori.** → **Topilma:** agentic AI **$9.14 mlrd (2026) → $139 mlrd (2034)**; Gartner: **40% korporativ ilovalar** 2026 oxirida agentlarga ega bo'ladi; **40%+ agentik loyihalar 2027 oxirigacha bekor qilinadi**. → **Qaror:** ⚠️ "agent" so'zini ehtiyotkor ishlatish; **aniq ROI metrikasi** bilan chiqish (bekor qilinadigan 40% ga kirmaslik).
37. **Nima uchun loyihalar bekor qilinadi?** → sabab: aniq ish oqimiga bog'lanmaganligi, o'lchanadigan natija yo'qligi. → **Qaror:** ✅ bizning ROI birinchi kundan o'lchanadi: **"nechta hujjat, nechta soat, nechta jarima oldini olindi"**.
38. **Narx trendi.** → **Topilma:** LLM API narxlari 2025→2026 da **~80% tushdi**; SLM-first arxitektura compute'ni **60–70%** tejaydi. → **Qaror:** ✅ **$0.01/hujjat** darajasidagi COGS real → narx strategiyasi erkin.
39. **Mahalliy analog bormi?** → **Topilma:** O'zbekistonda Didox, Faktura.uz, 1C asosidagi yechimlar **shakl/to'ldirish** uchun; **AI tushuntirish** qatlami yo'q. CoreAI kabi AI-infra startaplari $200k jalb qilgan (2026), lekin soliq vertikalida emas. → **Qaror:** ✅ **AI-maslahat qatlami bo'sh**.
40. **Faza D xulosasi.** → **Xulosa:** g'oya **global miqyosda isbotlangan**, mahalliy bo'shliq **aniq**, texnologik xarajat **bo'shatilgan**, talab **majburiy o'zgarish bilan** yaratilgan. → **Qaror:** ✅ **eng yuqori ehtimolli g'oya**.

## FAZA E (41–50). Raqobat va alternativa

41. **Bugun tadbirkor nima ishlatadi?** → (a) autsorsing buxgalter, (b) 1C/Excel, (c) Didox/Faktura.uz, (d) Telegram'dagi "buxgalter opa", (e) hech narsa. → **Qaror:** asosiy raqib — **(d) va (e)**, ya'ni odat va qo'rquv.
42. **Nima uchun Didox/Faktura.uz yetarli emas?** → ular **hujjat yaratadi**, **tushuntirmaydi**. Tadbirkor "nima uchun"ni so'raydi. → **Qaror:** pozitsiya: **"qatlam"** (layer) — ularning ustida ishlaymiz, ular bilan raqobat qilmaymiz.
43. **Nima uchun oddiy ChatGPT yetarli emas?** → (a) 2026 qoidalarini bilmaydi, (b) hujjatni o'qimaydi, (c) muddatlarni eslatmaydi, (d) javobgarlik yo'q, (e) o'zbekcha soliq atamalarini bilmaydi. → **Qaror:** ✅ shu 5 ta — pitch'dagi differensiatsiya jadvali.
44. **Raqobat 2×2.** → O'qlar: *Avtomatlashtirish* × *Tushuntirish/maslahat*. → Didox (yuqori, past), ChatGPT (past, o'rta), buxgalter (past, yuqori, qimmat), **biz (yuqori, yuqori, arzon)**.
45. **Katta o'yinchi kirib kelishi xavfi.** → Intuit/Xero O'zbekistonga kirmaydi (soliq tizimi mahalliy, bozor kichik). → **Qaror:** ✅ **himoya — mahalliy soliq mantiqi**, bu global o'yinchining retrofit qilmaydigan qismi.
46. **Buxgalteriya firmalari bizni raqib deb ko'radimi?** → Agar "buxgalterni almashtiramiz" desak — ha. → **Qaror:** ✅ pozitsiya: **"sizning har bir mijozga sarflagan vaqtingizni 50% qisqartiramiz"** → ular **ko'proq mijoz** oladi (Intuit ma'lumoti bilan tasdiqlangan).
47. **Banklar raqobatchimi?** → Banklar SMS-xabar yuboradi, lekin soliqni tushuntirmaydi. → **Qaror:** potensial **hamkor** (bank → mijoz kanali).
48. **Davlat raqobatchimi?** → **Topilma:** davlat **avtomatik deklaratsiya**ni o'zi tayyorlaydi (ZRU-1108) → ya'ni "deklaratsiya to'ldirish" **o'lib bormoqda**. → **Qaror:** 🔴 **bizning qiymat "to'ldirish" emas, "tushunish va optimallashtirish"**. Bu strategik tuzatish juda muhim — mahsulot shu nurda qurilishi kerak.
49. **Kim birinchi sotib oladi?** → ICP: Toshkent, **yangi ro'yxatdan o'tgan** YaTT/mikrofirma (0–18 oy), e-faktura chiqaradigan, savdo/xizmat sohasida. → **Qaror:** yangi biznes = yangi odat, qarshilik past.
50. **Faza E xulosasi.** → **Xulosa:** raqobat **zaif**, lekin **davlat avtomatlashtirishi** uzoq muddatda "deklaratsiya" qiymatini yeydi. → **Qaror:** pozitsiya = **qaror qabul qilish yordamchisi**, hisob-kitob emas.

## FAZA F (51–60). Texnologiya va arxitektura

51. **Demo uchun minimal texnologiya.** → `rasm/PDF → OCR (matn) → LLM extraction (JSON: sana, summa, QQS, kontragent, INN) → soliq qoidalari dvigateli → javob (Telegram)`.
52. **OCR qanday?** → O'zbek/lotin + kirill + raqamlar; EHF PDF'lari **matnli** (OCR shart emas) → **birinchi demo EHF PDF bilan** (aniq, barqaror). → **Qaror:** ✅ demo barqarorligi uchun PDF → matn yo'lini tanlash.
53. **Soliq qoidalari dvigateli (engine).** → JSON/YAML'da qoidalar: rejimlar, chegaralar (12 000 BRV = 4.94 → 5.28 mlrd), stavkalar (12/6/4/1%), muddatlar, imtiyozlar. → **Qaror:** ✅ **bu mahsulotning haqiqiy IP'si** — kod emas, **bilim bazasi**.
54. **Nima uchun bu IP?** → chunki har yil qoidalar o'zgaradi, raqobatchi kodni ko'chirsa ham **bilim bazasini** yangilab turolmaydi. → **Qaror:** versiyalash + "qoida o'zgargan sana" tarixi.
55. **"Rejim simulyatori" matematikasi.** → Input: aylanma, xarajatlar, kirim QQS ulushi, xaridorlar (QQS to'lovchimi?). → Output: 4 rejim bo'yicha **yillik soliq yuki** + risklar. → **Qaror:** ✅ **demoda ko'rsatiladigan eng ishonarli slayd** (real hisob-kitob).
56. **Ovozli kiritish.** → "Bugun 2 millionga tovar oldim" → LLM → tranzaksiya. → **Topilma:** o'zbek ASR endi yetuk (WER ~9.7% medium). → **Qaror:** 2-versiyada; demo'da 1 ta misol.
57. **Muddat eslatmalari.** → Soliq kalendari: QQS, aylanma, JShDS, statistika hisobotlari. → **Qaror:** ✅ eng arzon "retention" mexanizmi (har hafta foydali).
58. **Risk-skor izohi.** → Kirish: EHF ma'lumotlari; Chiqish: "ehtimoliy sabablar ro'yxati" (masalan: kontragent INN faol emas, narx bozor o'rtachasidan past, QQS zanjiri uzilgan) + **remediation** ("nima qilish kerak"). → **Qaror:** ⚠️ da'vo qilmaymiz: "ehtimoliy sabablar", "maslahat uchun buxgalterga".
59. **Arxitektura.** → Telegram Mini App (frontend) + FastAPI backend + Postgres + Redis + LLM (gpt/claude + lokal fallback) + mahalliy hosting. → **Qaror:** 36 soatda qurish mumkin bo'lgan minimal stack.
60. **Go/No-Go.** → ✅ **36 soatda to'liq ishlaydigan demo**: PDF → tahlil → rejim simulyatori → Telegram javob. Boshqa ikkala g'oyaga qaraganda **2× tez** va **100% barqaror**.

## FAZA G (61–70). Monetizatsiya va unit economics

61. **Narx pog'onalari.** → Free: 5 hujjat/oy; **Start: 99 000 so'm/oy** (100 hujjat, soliq kalendari); **Biznes: 199 000 so'm/oy** (cheksiz, simulyator, risk-izoh, buxgalter bilan ulanish). → **Qaror:** o'rtacha ARPU maqsad **130 000 so'm (~$11)**.
62. **B2B2C narx.** → Buxgalteriya firmasi: **$99/oy** (30 mijozgacha), keyin per-client. → **Qaror:** CAC ≈ 0 (firma o'z mijozlarini olib keladi).
63. **COGS.** → 1 hujjat: OCR+LLM ≈ **$0.005–0.01**; 100 hujjat/oy = $0.5–1 → ARPU $11 da **margin ~90%**. → **Qaror:** ✅ sof SaaS iqtisodi.
64. **CAC.** → Kanallar: Telegram soliq/o'zini band qilganlar guruhlari, buxgalter tavsiyasi, Instagram reels ("6% yoki 12%?"), bank hamkorligi. → **Gipoteza:** CAC **$5–12**; LTV (18 oy × $11 × 0.85) ≈ **$168** → **LTV/CAC 14–30×**. → **Qaror:** ✅ juda sog'lom (agar churn nazoratda bo'lsa).
65. **Churn.** → Sabab: biznes yopiladi; mavsumiylik; "buxgalter yana arzonroq". → **Qaror:** oylik churn maqsadi **<6%**; yillik to'lovga **20% chegirma** (cash-flow + retention).
66. **Payback.** → CAC $10 / ($11×0.9 margin) = **~1 oy**. → **Qaror:** ✅ **eng kuchli iqtisodiy argument** — bu VC'lar yaxshi ko'radigan raqam.
67. **Moliyaviy model (24 oy).** → 25 000 B2C ($11) = $275k/oy + 300 firma ($99) = $30k/oy → **$305k/oy ≈ $3.7 mln ARR**; jamoa 12 kishi ($25k/oy) + marketing ($40k/oy) → **breakeven ~9–12 oy**.
68. **Kapital.** → Seed **$300–500k** (IT Park Ventures $150k + angel + grantlar). → **Topilma:** IT Park Ventures o'rtacha **$150k**, idea $10k dan Series A $1 mln gacha. → **Qaror:** ✅ mos.
69. **Qo'shimcha daromad.** → (a) buxgalter marketplace komissiyasi 10–15%, (b) kredit-skoring uchun anonim agregat (banklar), (c) hujjat arxivi/premium, (d) soliq kurslari (o'quv mahsuloti). → **Qaror:** diqqatni yo'qotmaslik: 1-modda keyin.
70. **Faza G xulosasi.** → **Xulosa:** uch g'oya orasida **eng yaxshi unit economics** (payback 1 oy, margin 90%, CAC past).

## FAZA H (71–80). GTM: qanday qilib 1000 mijozga chiqish

71. **Birinchi 100 mijoz (30 kun).** → (a) 5 ta buxgalteriya firma (har biri 10–30 mijoz), (b) 3 ta Telegram guruh posti, (c) 20 ta jonli uchrashuv (startup markazlari, IT Park, "Tadbirkorlar maktabi"). → **Qaror:** 100 mijoz = 1 firma + 1 viral post bo'lishi mumkin.
72. **"Viral" mexanizm nima?** → **Bepul soliq kalkulyatori**: "6% yoki 12% — qaysi biri foydali?" — veb-sayt/bot, ulashish oson, natija shaxsiy. → **Qaror:** ✅ **eng arzon o'sish dvigateli**. Har tadbirkor bu savolni beradi.
73. **Kontent strategiyasi.** → Har hafta: 1 qoida o'zgarishi → 1 tushuntirish karuseli → 1 ta "haqiqiy misol". → **Qaror:** o'zbek tilida, soliq mavzusi qidiruvda juda faol.
74. **Hamkorlik.** → Banklar (mijozlariga bepul kalkulyator), buxgalteriya kurslari, IT Park, "Tadbirkorlikni qo'llab-quvvatlash" markazlari. → **Qaror:** bank kanali eng katta leverage.
75. **Sotuv suhbati (15 sekund).** → "Siz 6% QQS rejimiga o'tsangiz yiliga qancha tejaysiz, bilasizmi? 2 daqiqada hisoblab beraman." → **Qaror:** ✅ savol → hisob → ishonch.
76. **Nima sotmaymiz?** → "AI" so'zini birinchi jumlada ishlatmaymiz. Sotamiz: **pul, vaqt, xotirjamlik**.
77. **Onboarding.** → 3 qadam: Telegram → 2 savol (faoliyat turi, aylanma) → birinchi faktura yuklash. **90 sekund**. → **Qaror:** KPI "birinchi hujjat ≤ 3 daqiqa".
78. **Retention.** → Haftalik "soliq holati" xulosasi + muddat eslatmalari + "siz bu oy X so'm tejadingiz" hisoboti. → **Qaror:** foyda **ko'rinadigan** bo'lishi shart.
79. **Pitch'dagi tarqatish slaydi.** → "1 buxgalter = 30 mijoz; 300 buxgalter = 9 000 mijoz. Biz B2C'ga reklama sotmaymiz — biz **buxgalterlarga qurol** sotamiz."
80. **Faza H xulosasi.** → **Xulosa:** GTM **arzon va tez**, chunki mahsulot **majburiy og'riq**ni yechadi va **qidiruvda** topiladi.

## FAZA I (81–90). Risklar va mitigatsiya

81. **R1 — noto'g'ri soliq maslahati.** → Ta'sir: jarima, obro' yo'qotish. **Mitigatsiya:** "manba: Soliq kodeksi moddasi" har javobda; buxgalterga eskalatsiya; "maslahat emas, ma'lumot" shartnomasi; har bir javob versiyalangan.
82. **R2 — qoidalar o'zgarishi.** → **Topilma:** 2026 da 4 marta o'zgardi. **Mitigatsiya:** qoida bazasi **versiyalash** + "amal qilish sanasi" + avtomatik test to'plami.
83. **R3 — davlat avtomatlashtirishi.** → ZRU-1108 deklaratsiyani avtomatlashtiradi. **Mitigatsiya:** qiymatni **"tushunish/optimallashtirish/risk"**ga ko'chirish (48-bosqich).
84. **R4 — ma'lumot xavfsizligi.** → Mitigatsiya: mahalliy hosting, shifrlash, minimal saqlash, kirish jurnali, mustaqil audit.
85. **R5 — ishonchsizlik ("bot soliqni buzadi").** → Mitigatsiya: buxgalter **hamkor** pozitsiyasi, "AI taklif qiladi, inson tasdiqlaydi", ommaviy 3 ta keys.
86. **R6 — churn (biznes yopilishi).** → Mitigatsiya: segment fokus (yashovchan sohalar: savdo, xizmat, IT, ta'lim), yillik to'lov.
87. **R7 — katta o'yinchi (bank/telekom) kirishi.** → Mitigatsiya: buxgalterlar tarmog'i (o'tish narxi) + qoida bazasi chuqurligi.
88. **R8 — "yana bir Telegram bot" charchog'i.** → Mitigatsiya: **natija** ko'rsatish (tejangan pul), sifat (manba), brend (buxgalterlar bilan birga).
89. **Etika.** → Foydalanuvchi ma'lumotini banklarga/CRM'ga sotmaymiz; "soliqdan qochish" bo'yicha maslahat **berilmaydi** (faqat qonuniy optimallashtirish). → **Qaror:** yozma siyosat, ochiq e'lon.
90. **Faza I xulosasi.** → Risklar **boshqariladigan** va **moliyaviy emas, obro'-operatsion**. Bu — eng "past riskli" g'oya.

## FAZA J (91–100). Hackathon sintezi (TANLANGAN G'OYA)

91. **Demo 1 (30 sek):** Telegram'ga EHF PDF yuboriladi → "Bu faktura: 12 mln so'm, QQS 1.28 mln, kontragent INN faol, sizning rejimingizda QQS yuki +X so'm".
92. **Demo 2 (45 sek):** "6% yoki 12%?" simulyator: 3 parametr → 4 ta ustun → "sizga 6% foydali, yiliga 8.4 mln so'm tejaydi".
93. **Demo 3 (30 sek):** Risk-izoh: "Sizning 3 ta fakturada kontragent INN nofaol → ehtimoliy flag sababi; nima qilish kerak: ...".
94. **Demo 4 (20 sek):** Ovozli kiritish: "Bugun 2 millionga tovar oldim" → tranzaksiya + soliq oqibati.
95. **Metrika:** 1 faktura tahlili **<8 sekund**; 4 rejim simulyatsiyasi **<3 sekund**; xato foizi 20 ta test hujjatda.
96. **Arxitektura slaydi:** Telegram Mini App + qoidalar dvigateli + LLM + mahalliy hosting.
97. **Bozor slaydi:** 1 236 100 subyekt, 52.2% YaIM, 74% bandlik, 600 000+ ta'sirlangan.
98. **Why now slaydi:** ZRU-1108 + UP-153 + UP-100 + PP-247 — hammasi **2026**da.
99. **Hakam savoli:** "Davlat buni o'zi qilmaydimi?" → "Davlat **hisoblaydi**, biz **tushuntiramiz**. 1.2 mln odamga inspektor yetmaydi."
100. **Yakuniy baho: 92.8/100.** Kuchli: bozor, to'lov qobiliyati, demo, huquqiy tozalik, regulyativ tailwind, unit economics, eksport. Zaif: texnologik "wow" darajasi pastroq (bu hakamlar uchun minus bo'lishi mumkin) → **shu sababli demo'da vizual va jonli bo'lishi shart**.

---

# 6. UCH G'OYANI BAHOLASH: 12 MEZONLI MATRITSA

> Baholash **subyektiv emas**: har bir ball 1–5, vaznlar esa "hackathon mezoni (30% ishlaydi)" + "seed investor mezoni" aralashmasidan olingan.

| # | Mezon | Vazn | MEDSI | USTOZ | HISOB |
|---|-------|:---:|:---:|:---:|:---:|
| 1 | Muammoning o'tkirligi va majburiyligi | 10 | 5 | 5 | 5 |
| 2 | O'zbekistondagi bozor hajmi | 10 | 4 | 5 | 5 |
| 3 | To'lov qobiliyati / byudjetning mavjudligi | 12 | 4 | 3 | **5** |
| 4 | 36–48 soatda ishonchli demo | 12 | 3 | 4 | **5** |
| 5 | Ma'lumotga kirish (hozir, ruxsat bilan) | 10 | 2 | 3 | **4** |
| 6 | Raqobat bo'shlig'i (Toshkentda) | 8 | 4 | 2 | **4** |
| 7 | Regulyativ "tailwind" (2025–2026) | 10 | 5 | 4 | 5 |
| 8 | Skalalanuvchanlik va eksport | 8 | 3 | 4 | 4 |
| 9 | Unit economics (margin, payback, CAC) | 8 | 3 | 3 | **5** |
| 10 | Jamoaga moslik / bajarilish ehtimoli | 6 | 3 | 3 | 4 |
| 11 | Ijtimoiy ta'sir (nominatsiya/PR) | 4 | **5** | **5** | 4 |
| 12 | Huquqiy va klinik/akademik risk (yuqori ball = past risk) | 2 | 2 | 3 | **5** |
| | **VAZNLANGAN JAMI** | **100** | **73.2** | **74.0** | **92.8** |

### Natijaning o'qilishi
- **MEDSI 73.2** — hikoyasi eng kuchli, lekin **ma'lumot (2/5)** va **demo ishonchliligi (3/5)** uni cho'ktiradi. 4-mezon vazni 12 — ya'ni "ishlaydi" mezoni bu g'oyaga qarshi ishlaydi.
- **USTOZ 74.0** — bozori eng katta, lekin **raqobat 2/5** (bepul ChatGPT, EduBaza, Khan Academy) va **to'lov qobiliyati 3/5** (past ARPU + yuqori churn).
- **HISOB 92.8** — 12 mezondan 6 tasida maksimal ball; **hech bir mezonda 3 dan past emas**. Bu "yutadigan" profilning matematik ta'rifi.

## 6.1 "Kill criteria" — qachon fikrni o'zgartirish kerak

| G'oya | Raqobatdosh g'olib bo'lishi uchun zarur shart |
|---|---|
| MEDSI | Jamoada **vrach** bo'lsa + 1 klinika bilan **yozma pilot kelishuvi** bo'lsa (hackathon'gacha) |
| USTOZ | Jamoada **o'qituvchi/metodist** bo'lsa + 1 o'quv markazi piloti bo'lsa |
| HISOB | Jamoada **backend + LLM** tajribasi bo'lsa (pilot shart emas) |

> **Qoida:** agar jamoada shifokor bo'lsa va u klinikadan xat olib kela olsa — **MEDSI** jiddiy raqibga aylanadi (73 → ~85). Aks holda HISOB.

## 6.2 Yakuniy qaror va uning 3 sababi

### QAROR: **HISOB AI** — Tadbirkor treki

**1-sabab. Talab majburiy, taklif esa yo'q.**
2026-yil 1-yanvardan boshlab bir vaqtda: avtomatik deklaratsiya + o'zini band qilganlarga e-faktura (**ZRU-1108**), real-time AI QQS risk-skor (**UP-153**), 6% ixtiyoriy QQS va 12 000 BRV chegara (**UP-100**, 26.05.2026), 1% aylanma rejimi (**PP-247**). Bu — **600 000+ subyekt** uchun bir yilda to'rtta bir-biriga zid qaror. Bugun O'zbekistonda bu savollarga **o'zbek tilida, 24/7, arzon** javob beradigan vosita **yo'q**.

**2-sabab. Demo 100% barqaror, hakamlar buni ko'radi.**
Hackathon mezonlarining eng kattasi — "**ishlaydi**" (30%). HISOB'ning demo'si tashqi tizimga, internetga, tibbiy ma'lumotga yoki maktab infratuzilmasiga bog'liq emas: **PDF kirish → tahlil → javob**. Bir marta yozib qo'yilgan demo ham ishlaydi, jonli demo ham.

**3-sabab. Iqtisod 1-oyda qaytadi.**
CAC ~$10, ARPU ~$11, gross margin ~90% → **payback ~1 oy**. Boshqa ikkala g'oyada payback 4–12 oy. Bu farq investor suhbatida hal qiluvchi.

**Va yana bir narsa:** HISOB **ijtimoiy ta'sir** nominatsiyasiga ham tegadi — 10.5 mln kishi band bo'lgan sektorni **soyadan chiqarish**. Ya'ni bitta mahsulot bilan **asosiy sovrin + "eng dolzarb ijtimoiy loyiha"** ikkalasiga da'vo qilish mumkin (pitch'ning 9-slaydi shunga bag'ishlanadi).

---

# 7. "NIMA UCHUN" — 6 NUQTAI NAZAR

> Hakamlar, investorlar va mijozlar **bir xil faktlarni boshqacha** o'qiydi. Har biri uchun alohida javob tayyor.

## 7.1 Nima uchun HOZIR (Why now) — 5 ta mustaqil sabab bir vaqtda

| # | Sabab | Dalil | Qachon tugaydi |
|---|---|---|---|
| 1 | **Regulyativ zarba** | ZRU-1108 (25.12.2025), UP-153 (01.01.2026), UP-100 (26.05.2026), PP-247 (01.01.2026) | Deraza **6–12 oy**; keyin bozor o'rgangan bo'ladi |
| 2 | **Texnologiya arzonlashdi** | LLM API narxlari 2025→2026 da **−80%**; SLM-first compute'ni **−60–70%** | Doimiy, lekin **birinchi harakat ustunligi** 12 oy |
| 3 | **Tarqatish kanali tayyor** | Telegram **25 mln (85%)**; Click 12 mln+, Payme 8 mln+ | — (infratuzilma) |
| 4 | **Davlat pul va KPI qo'ydi** | UP-189: 2026 da **100 AI loyihasi**, $1 mlrd infra; PF-141: **250 AI rezident**, 200 tarmoq loyihasi; PQ-59: $2 mlrd venchur | **2026–2027** byudjet davri |
| 5 | **Global isbot paydo bo'ldi** | Intuit: 7.5 mln biznes AI-buxgalteriya ishlatadi; 45% AQSh SMB; oyiga 10 soat tejash | Isbot **kuchaymoqda** — kechikish qimmat |

> **Pitch jumlasi:** *"Bu g'oya 2 yil oldin o'lik edi — LLM qimmat, qoidalar eski, e-faktura hali majburiy emas edi. 2026-yil yanvardan uchala shart bir vaqtda bajarildi."*

## 7.2 Nima uchun O'ZBEKISTONDA (Why Uzbekistan) — 6 ta tuzilmaviy o'ziga xoslik

1. **Bozor "majburiy raqamli"**: e-faktura 2020 dan, e-retsept 2026, DMED 37 mln. Ya'ni **ma'lumot allaqachon raqamli** — AI uchun yoqilg'i bor.
2. **Bozor juda fragmentlangan**: 1.24 mln subyekt, 85% korxona kichik. Konsolidatsiya yo'q → **platforma imkoniyati**.
3. **Buxgalteriya xizmati qimmat va shaharda**: qishloqda tadbirkor **yolg'iz**. 1.24 mln ning yarmidan ko'pi Toshkentdan tashqarida.
4. **Til to'sig'i**: soliq tili rasmiy va murakkab; rus/ingliz xizmatlari yetarli emas. **O'zbek tilidagi AI** = bozor.
5. **Davlat "AI" ni KPI qilib qo'ydi**: PF-141 bo'yicha 200 ta tarmoq loyihasi, 250 rezident — ya'ni **bizning mahsulot davlat hisobotiga ham kiradi**.
6. **Eksportga chiqish oson**: bir xil muammo Qozog'iston, Ozarbayjon, Qirg'izistonda. Farq — **qoidalar fayli**, kod emas.

## 7.3 Nima uchun BIZ (Why us) — ikkala jamoa profili uchun

| Jamoa profili | Kuchli tomon | Nima qilish kerak |
|---|---|---|
| **Texnik jamoa** (2–4 dasturchi, ML bor) | 36 soatda demo. Bu eng katta raqobat ustunligi | **1 buxgalter** ni maslahatchi qilib olish (Telegram orqali, 2 soatga). Usiz qoidalar xato bo'ladi |
| **Aralash jamoa** (1 dev + 1 biznes) | Sotuv hikoyasi | Demo'ni **soddalashtirish**: 1 stsenariy, a'lo sifat |
| **Medik jamoa** | MEDSI'ga o'tish mantiqan to'g'ri (85+ ball) | Klinika pilot xati bilan |

> **Halol gap:** "Why us" hozircha **texnik tezlik + mahalliy kontekst**. Bu hackathon uchun yetarli. Investor uchun esa **"biz 2026-yilgi 4 ta soliq o'zgarishini kodga aylantirgan birinchi jamoa"** — bu aytiladigan va tekshiriladigan da'vo.

## 7.4 Nima uchun MIJOZ sotib oladi (Customer POV)

**Mijozning ichki monologi (buni pitch'da ovoz chiqarib aytish kerak):**
> *"Menga 6% yoki 12% — qaysi biri arzonligini kimdir aytishi kerak. Buxgalterga oyiga 1 million to'layman, u ham har safar aniq javob bermaydi. E-fakturam flag bo'ldi, sababini bilmayman. Jarima qo'rquvidan hujjatlarni kechiktiraman."*

**Qaror tenglamasi (mijoz ongida):**

| Savol | Javob |
|---|---|
| Muammo bormi? | Ha, har oy, pul va asab bilan |
| Muqobil bormi? | Buxgalter (qimmat), ChatGPT (ishonchsiz), do'st (xato) |
| Narx to'g'rimi? | 99 ming < 1 mln. **10× arzon** |
| Ishonch bormi? | Manba (Kodeks moddasi) + "buxgalter tasdiqlaydi" + mahalliy |
| Xavf bormi? | Past: u baribir qarorni o'zi qabul qiladi, AI faqat ko'rsatadi |
| Nima uchun bugun? | **Deklaratsiya muddati yaqin** |

## 7.5 Nima uchun BIZNES sifatida ishlaydi (Business POV)

| Ko'rsatkich | Qiymat | Izoh |
|---|---|---|
| TAM | ~$135 mln/yil | 900 000 subyekt × ~$12.5/oy |
| SAM | ~$52 mln/yil | 350 000 raqamli faol subyekt |
| SOM (24 oy) | **$3.7 mln ARR** | 25 000 B2C + 300 firma |
| ARPU | $11/oy (B2C), $99/oy (B2B2C) | |
| Gross margin | **~90%** | COGS $0.005–0.01/hujjat |
| CAC | $5–12 | Telegram + buxgalter tavsiyasi |
| Payback | **~1 oy** | |
| LTV/CAC | 14–30× | 18 oy umr, 6% churn |
| Breakeven | 9–12 oy | 12 kishi jamoa, $65k/oy xarajat |
| Seed ehtiyoji | **$300–500k** | IT Park Ventures $150k + angel |

**Daromad aralashmasi (24-oy):** 75% B2C obuna, 15% B2B2C, 10% xizmatlar/marketplace.

## 7.6 Nima uchun DAVLAT qo'llab-quvvatlaydi (Government POV)

| Davlat maqsadi (hujjat) | Bizning hissa |
|---|---|
| Soya iqtisodiyotini qisqartirish (UP-100 izohi: 600 000+ subyekt) | Har bir mijoz = rasmiylashtirilgan aylanma |
| Soliq bazasini kengaytirish | To'g'ri rejim tanlash → barqaror to'lov |
| PF-141: 200 tarmoq AI loyihasi, 250 AI rezident | Biz rezident + tarmoq loyihasi |
| UP-189: 2026 da 100 AI loyihasi | Biz loyihalardan biri |
| "5 Million AI Leaders" | O'quv moduli (soliq savodxonligi) — bepul |
| Soliq organlari yuki | Kamroq "nima uchun?" telefon qo'ng'irog'i |

> **Muhim nuance:** davlat **deklaratsiyani avtomatlashtirmoqda** (ZRU-1108). Ya'ni biz davlat bilan **raqobatlashmaymiz**, balki uning natijasini **tushunarli qilamiz**. Bu — pitch'dagi eng nozik va eng kuchli jumla.

## 7.7 Nima uchun INVESTOR qiziqadi (Investor POV)

- **Kategoriya:** vertical AI (Bessemer: vertical AI bozor kapitallashuvi legacy vertical SaaS'dan **≥10×** katta).
- **Timing:** O'zbekistonda AI rezidentligi + 0% soliq (IT Park) → **kapital samaradorligi** juda yuqori.
- **Metrika:** payback 1 oy, margin 90% — SaaS investor uchun "ideal egri".
- **Eksport hikoyasi:** "soliq qoidalari dvigateli" → 5 ta MDA davlati = **10× bozor**.
- **Chiqish yo'llari:** (a) strategik xaridor (bank, Didox/Faktura, 1C distribyutori), (b) mintaqaviy fintech, (c) M&A.
- **Nima uchun hozir:** PQ-59 bo'yicha 2030 gacha **$2 mlrd venchur** kerak, lekin taklif **$2 mlrd** allaqachon bor, talab esa **$20–30 mlrd** (Jahon banki) → **yaxshi aktivlar tanqis**. Ya'ni **yaxshi jamoa kapital topadi**.

## 7.8 Nima uchun RAQOBATCHI zaif (Competitor POV)

| Raqobatchi | Kuchli | Zaif (bizning hujum nuqtasi) |
|---|---|---|
| **Autsorsing buxgalter** | Ishonch, javobgarlik | Qimmat (5–10×), ish vaqti bilan, ko'p mijozda sifat tushadi |
| **ChatGPT/Gemini** | Bepul, aqlli | 2026 qoidalarini bilmaydi, hujjatni o'qimaydi, muddatni eslatmaydi, o'zbek soliq terminologiyasi zaif |
| **Didox / Faktura.uz** | Rasmiy integratsiya, obro' | Shakl to'ldirish, **tushuntirish yo'q**, AI qatlami yo'q |
| **1C** | To'liq buxgalteriya | Og'ir, qimmat, o'qitish kerak, kichik biznesga ortiqcha |
| **Bank ilovalari** | Tarqatish kuchi | Soliq maslahati yo'q, neytral emas |
| **Yangi AI startap** | Tez | Qoida bazasi va buxgalter tarmog'i yo'q (bizning moat) |

**Moat (himoya devori) uch qatlamda:**
1. **Bilim bazasi** — 2026 qoidalari, versiyalangan, manbali (nusxalash qiyin, yangilash qimmat).
2. **Buxgalterlar tarmog'i** — B2B2C kanal, o'zaro tavsiya (tarmoq effekti).
3. **Ma'lumot** — qaysi soha/segmentda qaysi rejim foydali (agregat, vaqt o'tishi bilan qimmatlashadi).

---

# 8. AMALIYOT: 72 SOATLIK PLAYBOOK (HISOB AI)

> **Muhim:** hozir 17-noyabr, ~08:00. Ro'yxatdan o'tish 10:00, trek tanlash 12:00. Ya'ni **qaror 4 soat ichida** qabul qilinishi kerak.

## 8.1 BLOK 0 — T−4 soat (08:00–12:00, bugun)

| Vaqt | Vazifa | Natija (deliverable) |
|---|---|---|
| 08:00–08:20 | Startklar holatini **aynan hozir** tekshir: Eventflow'da ticket "Pending" bo'lsa — tashkilotchiga qo'ng'iroq/Telegram (kommentlarda hamma shu muammoni yozgan) | Tasdiq skrinshoti yoki "borib ko'ramiz" qarori |
| 08:20–09:00 | **6 ta faktni yodlash:** 1 236 100 / 52.2% / 357 883 / ZRU-1108 / UP-100 6% / 99 ming so'm | Pitch'ning "raqamli umurtqasi" |
| 09:00–09:40 | **Buxgalter topish** (eng muhim vazifa): Telegram'dagi buxgalterlar guruhi, tanish, yoki Instagram'da "buxgalter Toshkent". 1 kishi, 30 daqiqa suhbat, **3 ta real faktura** olish | 3 PDF/rasm + 3 ta "eng ko'p beriladigan savol" |
| 09:40–10:00 | Demo **stsenariysi** yoziladi (8.4-bo'lim) | 1 bet |
| 10:00–12:00 | Ro'yxatdan o'tish + jamoa yig'ish. **Trek sifatida "Tadbirkor"** tanlanadi | Jamoa tarkibi qulflandi |

**Jamoa tarkibi (minimum 4 rol, bir kishi 2 rolni bajarishi mumkin):**

| Rol | Vazifa | Kim bo'lishi |
|---|---|---|
| **Builder** | Backend + LLM + Telegram bot | Eng kuchli dasturchi |
| **Data/Rules** | Qoidalar bazasi (stavkalar, chegaralar, muddatlar) + test hujjatlar | Diqqatli, hujjat bilan ishlay oladigan |
| **Design/Demo** | Mini App UI, demo video, slaydlar | Dizayner yoki frontend |
| **Pitch/Biznes** | Suhbat, pitch, hakamlar bilan aloqa | Eng yaxshi gapiradigan |

## 8.2 BLOK 1 — 1-kun, 12:00–22:00 (qurish)

| Vaqt | Builder | Rules | Design | Biznes |
|---|---|---|---|---|
| 12:00–13:00 | Repo, Telegram bot skeleti, LLM ulanish | 2026 soliq rejimlari jadvali (4 rejim × stavka × chegara) | Ekranlar eskizi (3 ekran) | 3 ta hujjat tayyorlash, 3 ta test savol |
| 13:00–14:00 | Tushlik | Tushlik | Tushlik | Tushlik |
| 14:00–17:00 | **PDF → matn → JSON** oqimi ishlaydi | Rejim simulyatori formulalari + test | Mini App 1-ekran | 10 ta mijoz bilan suhbat (telefon/Telegram) |
| 17:00–19:00 | JSON → soliq xulosasi (qoidalar dvigateli ulanishi) | 20 ta "nima bo'ladi agar" holat testi | 2-ekran (simulyator) | Pitch hikoyasi v1 |
| 19:00–22:00 | Ovozli kiritish (stretch) yoki barqarorlik | Xatolar tuzatish | Demo video yozish | Slayd 1–5 |

**1-kun oxirida bo'lishi shart:** bitta faktura → javob, terminalda bo'lsa ham. **Demo bor, slayd yo'q** — yaxshi. Aksincha bo'lsa — yomon.

## 8.3 BLOK 2 — 2-kun, 09:00–19:00 (sayqal + checkpoint)

| Vaqt | Vazifa |
|---|---|
| 09:00–10:00 | **Regressiya testi**: 10 ta hujjat, xatosiz o'tishi |
| 10:00–12:00 | Mentorlik sessiyasi → **aynan 3 ta savol** beriladi (8.6-bo'lim) |
| 12:00–14:00 | UI/UX sayqal, o'zbek tili matnlari, xato holatlari ("tushunmadim" javobi) |
| 14:00–15:00 | **Checkpoint 15:00 uchun tayyorgarlik**: 2 daqiqalik demo + 1 slayd |
| 15:00 | ⚠️ **CHECKPOINT** — bu yerda 20 finalist saralanadi. Demo ishlashi shart |
| 15:00–17:00 | Mentor fikridan keyin **tuzatish** (odatda: hikoya, narx, differensiatsiya) |
| 17:00–18:00 | Master-class (foydali bo'lsa) / davom etish |
| 18:00–19:00 | **Top-20 e'lon qilinadi** — ikkala holatga tayyor bo'lish |

**Agar Top-20 ga kirmasak (reja B):** 19:00–22:00 — 10 ta hakam/mentor bilan shaxsiy suhbat, kontakt yig'ish. Hackathon **aloqa yig'ish** maydoni; sovrin ikkinchi darajali.

## 8.4 BLOK 3 — 3-kun, 09:00–13:30 (pitch)

| Vaqt | Vazifa |
|---|---|
| 09:00–10:00 | Pitch **3 marta ovoz chiqarib** (vaqt bilan), demo 3 marta |
| 10:00 | Finalistlar pitch (odatda 3–5 daqiqa + savol) |
| 10:00–13:00 | Har bir raqib pitch'ini **tinglash** (hakamlar nima so'rayotganini bilib olish) |
| 13:30 | Natijalar |

## 8.5 Demo stsenariysi (aniq, 2 daqiqa 40 soniya)

1. **(0:00–0:15) Og'riq.** "Men 8 oydan beri YaTT'man. Har oy soliq. Buxgalterga 1 mln so'm to'layman. Va baribir qo'rqaman."
2. **(0:15–0:45) Harakat.** Telegram'ga **haqiqiy EHF PDF** yuboriladi. 6 sekundda javob: summa, QQS, kontragent holati, "bu sizning rejimingizda qanday oqibat beradi".
3. **(0:45–1:30) Qaror.** "Endi eng qimmat savol: **6% yoki 12%?**" → 3 parametr kiritiladi → 4 ustunli jadval → "**6% sizga yiliga 8.4 mln so'm tejaydi**". Hakamlar **o'z raqamlarini** kiritishi mumkin (jonli, lekin skript bilan).
4. **(1:30–2:05) Ishonch.** Risk-izoh: "Sizning 3 ta fakturangizda kontragent INN nofaol — ehtimoliy flag sababi. Nima qilish kerak: ...". Har bir javob ostida **"Manba: Soliq kodeksi, modda"**.
5. **(2:05–2:30) Miqyos.** "1 buxgalter = 30 mijoz. 300 buxgalter = 9 000 mijoz. Biz reklama sotmaymiz — **buxgalterlarga qurol sotamiz**."
6. **(2:30–2:40) Yakun.** "1.24 mln tadbirkor. 52% YaIM. Va ularning hech birida o'zbek tilida gapiradigan buxgalter yo'q."

**Demo fallback (majburiy):** 60 soniyalik **ekran yozuvi** (video) — internet uzilsa, loyiha yiqilsa qo'yiladi. Video **avvaldan** tayyorlanadi.

## 8.6 Mentorlarga beriladigan 3 savol (10:00, 2-kun)

1. "Hakamlar ro'yxatida kim bor va ular **nimanı** qadrlaydi: texnika, bozor yoki ijtimoiy ta'sir?"
2. "Bizning eng katta zaif tomonimiz deb nimani ko'rasiz — va 24 soatda nima tuzatish mumkin?"
3. "Demo'dan keyin **qaysi bitta raqam** sizni ishontirmadi?"

## 8.7 Slaydlar (10 ta, qat'iy tartib)

| # | Slayd | Kontent |
|---|---|---|
| 1 | Muqova | Nom + bir jumlada nima qiladi + jamoa |
| 2 | Muammo | 4 ta 2026 soliq o'zgarishi (sanalar bilan) + "1.24 mln tadbirkor tushunmaydi" |
| 3 | Mijoz | 1 personaj: "Dilshod, 29, Toshkent, 8 oylik YaTT, buxgalterga 1 mln to'laydi" |
| 4 | Yechim | 4 modul: **O'qiydi · Hisoblaydi · Tushuntiradi · Eslatadi** |
| 5 | Demo | 3 skrinshot + QR (jonli sinab ko'rish uchun) |
| 6 | Nima uchun biz / moat | Qoidalar bazasi + buxgalterlar tarmog'i + til |
| 7 | Bozor | TAM $135 mln / SAM $52 mln / SOM $3.7 mln ARR + 1 236 100 raqami |
| 8 | Biznes-model | 99/199 ming so'm + $99 B2B2C + payback 1 oy |
| 9 | Ijtimoiy ta'sir | Soya → rasmiy: 10.5 mln band, 52.2% YaIM; davlat KPI'lariga mos (PF-141) |
| 10 | So'rov | "Pilot uchun 10 ta buxgalteriya firma kerak" — **aniq so'rov**, umumiy "rahmat" emas |

## 8.8 Hakamlar savollari — 15 ta tayyor javob

1. **"Bu ChatGPT'dan nimasi bilan farq qiladi?"**
→ "ChatGPT 2026-yilgi 4 ta o'zgarishni bilmaydi, fakturangizni o'qimaydi, muddatni eslatmaydi va javob uchun javobgarlik olmaydi. Bizda **qoidalar bazasi + manba + muddat** bor." *(so'ng jonli: bir xil savolni ChatGPT'ga berib, noto'g'ri javobini ko'rsatish — kuchli harakat, lekin internetga bog'liq; video fallback)*
2. **"Davlat buni o'zi qilmaydimi?"**
→ "Davlat **hisoblaydi** (ZRU-1108 avtomatik deklaratsiya). Biz **tushuntiramiz** va optimallashtiramiz. 1.24 mln odamga inspektor yetmaydi."
3. **"Siz buxgalterlarni ishsiz qoldirasizmi?"**
→ "Yo'q. Intuit ma'lumoti: AI buxgalterning bir mijozga sarflagan vaqtini 50–60% qisqartiradi — u **2–3× ko'proq mijoz** oladi. Biz ularga qurol sotamiz."
4. **"Ma'lumotni qayerdan olasiz?"**
→ "Foydalanuvchi **o'z kabinetidan** yuklaydi. Biz hisobini saqlamaymiz, API'ga ruxsatsiz kirmaymiz. Bu huquqiy jihatdan eng toza yo'l."
5. **"Noto'g'ri maslahat bersangiz, jarima bo'lsa kim to'laydi?"**
→ "Biz **ma'lumot** beramiz, **qaror** emas. Har javobda manba, har amalda tasdiqlash. Shartnomada javobgarlik chegarasi. Va biz **buxgalterga eskalatsiya** qilamiz."
6. **"Nega siz? Jamoada buxgalter yo'q."**
→ "To'g'ri — shuning uchun 3 ta buxgalter bilan maslahatlashuv kelishuvimiz bor *(ko'rsatish)*. Bizning ustunligimiz — **kod va tezlik**, bilimni biz sotib olamiz."
7. **"Bozor kichik emasmi?"**
→ "O'zbekistonda $135 mln. Lekin mahsulot **qoidalar dvigateli** — Qozog'iston, Ozarbayjon, Qirg'iziston bir xil islohotdan o'tyapti. Kod emas, **qoidalar fayli** o'zgaradi."
8. **"Pul qachon qaytadi?"**
→ "CAC $10, ARPU $11, margin 90% → **1 oy**. Bu SaaS uchun eng yaxshi ko'rsatkich."
9. **"Nega hozir emas, 1 yildan keyin?"**
→ "Chunki deraza 6–12 oy: 2026-yilgi o'zgarishlar hali yangi, odat hali shakllanmagan. 2027 da bozor o'rganib qoladi."
10. **"Hackathon'dan keyin nima qilasiz?"**
→ "3 ta aniq qadam: 10 buxgalteriya firma pilot *(30 kun)*, 1 000 B2C foydalanuvchi *(60 kun)*, IT Park rezidentligi + grant arizasi *(90 kun)*."
11. **"Texnik jihatdan eng qiyin qismi nima?"**
→ "Qoidalar bazasini **to'g'ri va versiyalangan** saqlash. LLM oson — bilim qiyin. Shuning uchun IP shu yerda."
12. **"Nega oddiy skript/Excel emas?"**
→ "Skript fakturani **o'qimaydi** va savolga **o'zbek tilida javob bermaydi**. Bizning kirish nuqtasi — **rasm/PDF**, bu esa LLM talab qiladi."
13. **"Sizning yechimingiz xavfsizmi?"**
→ "Mahalliy hosting, shifrlash, minimal saqlash, audit-log, ma'lumotni uchinchi tomonga sotmaslik siyosati *(yozma)*."
14. **"Nima uchun aynan 'Tadbirkor' treki?"**
→ "Chunki mijoz — tadbirkor, va biz uning **vaqtini va pulini** qaytaramiz. Bu trekning eng to'g'ridan-to'g'ri talqini."
15. **"Eng katta xavf nima?"**
→ "Qoidalar o'zgarishi va davlat avtomatlashtirishi. Shuning uchun qiymatni 'hisoblash'dan **'tushunish va qaror'**ga ko'chirdik. Halol javob — hakamlar ishonchini oshiradi."

---

# 9. HACKATHONDAN KEYIN: 90 KUNLIK REJA

## 9.1 Bosqichlar

| Davr | Maqsad | Asosiy ishlar | Muvaffaqiyat mezoni |
|---|---|---|---|
| **1–14 kun** | Isbotlash | 10 buxgalter suhbati; 3 firma bilan pilot memorandum; qoidalar bazasi v1 (4 rejim); 20 test hujjat | 3 imzolangan pilot, 90% aniqlik |
| **15–30 kun** | Birinchi pul | 100 B2C foydalanuvchi; to'lov (Click/Payme); soliq kalkulyatori (bepul, viral); yuridik shartnomalar | **birinchi 5 mln so'm tushum** |
| **31–60 kun** | Takrorlash | 1 000 foydalanuvchi; 20 firma; retention tajribasi; qoida bazasi yangilanish jarayoni | D30 retention **>35%** |
| **61–90 kun** | Moliyalashish | IT Park rezidentligi; "Digital Startups" arizasi (PQ-59); IT Park Ventures; AI Award arizasi | **$150k+ grant/venchur** yoki aniq kelishuv |
| **4–6 oy** | Skalalash | 5 000 B2C + 100 firma; bank hamkorligi; Qozog'iston tadqiqoti | $60k/oy ARR |
| **7–12 oy** | Mintaqa | Qozog'iston/Ozarbayjon qoidalar fayli; seed round | **$300k+ ARR** |

## 9.2 90 kunlik byudjet (minimal)

| Modda | Summa (so'm) | Izoh |
|---|---|---|
| 2 dasturchi × 3 oy | 54 000 000 | $1 500/oy |
| 1 dizayner (yarim stavka) | 18 000 000 | |
| Buxgalter-maslahatchi | 6 000 000 | Eng muhim xarajat |
| LLM + hosting | 4 500 000 | |
| Yuridik + shartnomalar | 5 000 000 | |
| Marketing (kalkulyator, kontent) | 12 000 000 | |
| **JAMI** | **~99 500 000 (~$8 300)** | 3 oy |

> Bu **IT Park Ventures** ning eng kichik chekiga ($10k) ham sig'adigan bosqich. Ya'ni 1-o'rin yutmasa ham, **o'z kuchingiz bilan** boshlash mumkin.

## 9.3 KPI dashboard (har hafta)

| KPI | Maqsad (90 kun) |
|---|---|
| Ro'yxatdan o'tgan foydalanuvchi | 1 000 |
| Haftalik faol (WAU) | 400 |
| Birinchi hujjatni yuklaganlar | 60% |
| To'lovchi | 150 |
| B2B2C firma | 20 |
| Hujjat tahlili aniqligi | >92% |
| O'rtacha javob vaqti | <10 sek |
| D30 retention | >35% |
| NPS | >40 |
| Churn (oylik) | <7% |

## 9.4 Risk reyestri (ehtimol × ta'sir)

| Risk | Ehtimol | Ta'sir | Mitigatsiya | Egasi |
|---|---|---|---|---|
| Qoidalar o'zgarishi | Yuqori | O'rta | Versiyalangan baza + avtomatik test | Rules |
| Noto'g'ri maslahat shikoyati | O'rta | Yuqori | Manba, eskalatsiya, javobgarlik chegarasi, E&O sug'urta | CEO |
| Davlat avtomatlashtirishi | Yuqori | O'rta | Qiymatni "tushunish/risk"ga ko'chirish | CEO |
| Churn | O'rta | Yuqori | Muddat eslatma, haftalik hisobot, yillik to'lov | Growth |
| Katta o'yinchi (bank) | O'rta | O'rta | Buxgalter tarmog'i, tezlik | CEO |
| Ma'lumot sizib chiqishi | Past | Halokatli | Mahalliy hosting, shifrlash, audit | CTO |
| Jamoa tarqalishi | Yuqori | Yuqori | 3 oylik aniq maqsad + ulush kelishuvi | Founderlar |

---

# 10. AGAR JAMOA MEDIK BO'LSA: MEDSI'ga o'tish sharti

Agar 12:00 da jamoa tarkibida **shifokor** bo'lsa va u **1 klinikadan yozma qiziqish xati** olib kelsa — quyidagi o'zgarishlar bilan MEDSI'ga o'tish mantiqiy (ball 73.2 → ~85):

1. **Demo ambitsiyasi tushiriladi:** faqat **bitta qabul turi** (gipertoniya), 60 sekundlik audio, 20 ta sintetik dialog.
2. **Ma'lumot masalasi ochiq tan olinadi:** "bizda 40 soatlik real yozuv yo'q — birinchi 90 kun shunga ketadi".
3. **Pitch markazi:** "**hamma tashxis qo'ymoqchi, biz hujjatni yechamiz**" — bu differensiatsiya bugungi natijalarga qarab juda kuchli.
4. **Ijtimoiy ta'sir nominatsiyasi:** bu g'oyada eng kuchli (vrach vaqti → bemor bilan).
5. **Xavf:** demo internetga va LLM'ga bog'liq → **video fallback majburiy**.

**Va USTOZ AI'ga o'tish sharti:** jamoada **o'qituvchi/metodist** + **1 o'quv markazi** piloti. Aks holda — texnik demo chiroyli, lekin "yana bir AI tutor" taassurotidan chiqib ketish qiyin.

---

# 11. MANBALAR

**O'zbekiston qonunchiligi va davlat dasturlari**
1. PQ-358, 14.10.2024 — AI strategiyasi 2030 (gov.uz/digital; spot.uz; yuz.uz)
2. UP-189, 22.10.2025 — AI qo'shimcha choralar (uzdaily.uz; kun.uz; cis-legislation.com)
3. PF-141, 24.07.2026 — AI "Raqamli O'zbekiston 2030" ga (theleveragedyears.com tahlili)
4. PQ-59, 11.02.2026 — 5 000 startap / $2 mlrd venchur (piamg.uz; ixbt.uz)
5. PQ-357, 14.10.2024 — "Digital Startup", IT Park Ventures (it-park.uz)
6. ZRU-1108, 25.12.2025; UP-153; UP-100, 26.05.2026; PP-247, 12.08.2025 (vatupdate.com; regfollower.com; bizreg.uz; acsour.kz; zamon.uz)
7. PQ-415, 28.12.2023 — raqamli sog'liqni saqlash tizimi (akademik maqola)

**Sog'liqni saqlash**
8. National Health Compact — Uzbekistan (Jahon banki, 2025)
9. DMED / MED-ID / e-retsept — yuz.uz (13.11.2025), zamin.uz (12.12.2025)
10. Euronews (17.02.2026) — sog'liqni saqlash modernizatsiyasi, 9 000+ xususiy klinika
11. UzDaily (07.05.2025) — NCD $1 mlrd, 27 vrach/10k, 35% surunkali
12. Fergana.agency — vazirlar ishdan olinishi, 42 trln so'm xarajat
13. Statkom — farmatsevtika ishlab chiqarish 4.4 trln so'm (8 oy 2026)
14. Kun.uz (09.06.2025) — dori narxlari, 60% import
15. Medical Tourism Watch / Kun.uz (23.07.2026) — 86 199 (2025), 35 401 (1-yarim 2026)

**Ta'lim**
16. OECD PISA 2025 — Uzbekistan country note
17. OECD TALIS 2024 — Uzbekistan country note
18. Statkom — maktablar 11 118, o'quvchilar 6.87 mln, o'qituvchilar 577 700
19. NBER w35620 (08.2026) — Khanmigo 2 yillik RCT
20. Bastani et al., PNAS 2025; Harvard physics RCT; Tutor CoPilot RCT
21. TechBullion (14.09.2026) — O'zbekiston edtech 6 platforma

**Tadbirkorlik va moliya**
22. Statkom (26.01.2026; 01.07.2026) — kichik biznes 1 201.6k / 1 236.1k, YaIM 52.2%
23. UzDaily (04.11.2026) — SME rejasi 2026–2030, 50.5%, 140 trln so'm kredit
24. Jahon banki — SME elektron savdo <30%, kapital talabi $20–30 mlrd
25. Intuit QuickBooks 2026 AI Impact Report (34 000 egasi, 5.3 mln biznes)
26. Sage 2025, AICPA 2025, Karbon 2026 — AI-buxgalteriya statistikasi

**Global bozor/texnologiya**
27. Gartner (08.2025, 06.2025) — agentlar 40%, bekor qilinish 40%
28. Fortune Business Insights / Grand View — agentic AI $9.14 mlrd → $139 mlrd
29. Menlo Ventures 2025 — enterprise GenAI $37 mlrd; vertical AI $3.5 mlrd
30. NavAI Whisper (huggingface.co/navai-uz) — o'zbek ASR WER 9.73%
31. DataReportal "Digital 2026/2027: Uzbekistan"
32. 101digital.uz (2026) — Telegram 25 mln, Click 12 mln, Payme 8 mln

---

# 12. YAKUNIY XULOSA

**Uch g'oya, uch xil xavf:**

| | MEDSI | USTOZ | **HISOB** |
|---|---|---|---|
| Xavf turi | Klinik va huquqiy | Bozor va churn | **Operatsion** |
| Yutish ehtimoli (hackathon) | O'rta | O'rta | **Yuqori** |
| Omon qolish ehtimoli (12 oy) | Past-o'rta | Past | **Yuqori** |
| Hikoya kuchi | **Juda yuqori** | Yuqori | Yuqori |
| Demo barqarorligi | Past | O'rta | **Juda yuqori** |

**Bitta gapda:** *Sog'liqda qalbingiz bilan, ta'limda sabringiz bilan, tadbirkorlikda esa **hisob-kitobingiz** bilan yutasiz. Bugun hisob-kitob vaqti.*

**Bugungi birinchi 3 ta harakat:**
1. **09:00** — bitta buxgalter topib, 3 ta real faktura ol.
2. **10:00** — ro'yxatdan o't, **"Tadbirkor"** trekini tanla.
3. **12:00** — jamoa bilan **bitta** narsani qur: `PDF → javob`. Boshqa hech narsa.

> *Qolgan 297 bosqich — keyingi 90 kun ichida. Ular shu hujjatda, bosqichma-bosqich.*
