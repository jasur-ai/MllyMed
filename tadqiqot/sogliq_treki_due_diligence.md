# SOG'LIQNI SAQLASH TREKI — TO'LIQ DUE DILIGENCE
## Bozor anatomiyasi · raqobat · 12 o'lim sababi · unit economics · bankrotlik simulyatsiyasi · qaror

**Sana:** 17-noyabr 2026, 09:40 · **Kontekst:** trek tanloviga ~2 soat 20 daqiqa qoldi
**Format:** venchur investitsiya memorandumining "red team" versiyasi — ya'ni biz g'oyani **himoya qilmaymiz, o'ldirishga harakat qilamiz**. Omon qolgan g'oyagina hackathonga kiradi.
**Til:** o'zbekcha · **Barcha raqamlar manba bilan** (14-bo'lim)

---

# 0. XULOSA — 10 QATORDA

1. **Global bozor haqiqiy va katta:** sog'liq AI bozori 2026-yilda **$37–56 mlrd**, CAGR **37–44%**, 2030-ga **$110+ mlrd**. Pul bor — lekin **pul AQSh va Yevropada**, O'zbekistonda emas.
2. **Globalda ambient scribe (vrach hujjati) allaqachon tasdiqlangan biznes:** $1.85 mlrd (2024) → $17.75 mlrd (2033), narx **$99–600/vrach/oy**, inson scribe $1,500–2,500/oy. Ya'ni **"bozorda talab bormi?" degan savol yopilgan** — bu katta ustunlik.
3. **Lekin global muvaffaqiyat O'zbekistonga ko'chmaydi.** Sabab: global narx $200/oy, O'zbekistondagi klinika byudjeti **$50–100/oy**. Bu **20–40× farq** — ya'ni to'g'ridan-to'g'ri nusxa ko'chirish = o'lim.
4. **Qabriston aniq:** Olive AI ($902M yig'ib, $4 mlrd baholanib, 2023-da yopildi), Babylon (2023 bankrot), Forward Health ($650–750M, 3,200 kiosk va'da qilib **5 ta** yetkazdi, 2024-da yopildi). **9 ta sog'liq kompaniyasi birgalikda $35 mlrd qiymatni yo'q qilgan.**
5. **Statistik o'lim sababi:** CB Insights 431–483 post-mortem → kapital tugashi **70%** (bu *simptom*), PMF yo'qligi **43%**, vaqt noto'g'riligi **29%**, unit economics **19%**, "bozorda ehtiyoj yo'q" **42%**. Ya'ni **pul emas, ehtiyoj** o'ldiradi.
6. **O'zbekistonning eng katta tuzog'i — DMED.** 38 mln aholi e-kartasi, **8 000+ xususiy klinika va 6 000 dorixona ulangan**, egasi **Uzinfocom**. 2026-yil oxirigacha "elektron sog'liqni saqlash yadrosi" ishga tushadi. **Parallel EHR qurish = o'lim. DMED ustiga modul qurish = yashash.**
7. **Regulyator sizni o'ldirishi ham, boyitishi ham mumkin.** 2027-yil yanvardan **e-retsept majburiy** (12 817 dori), 2027/2030 **tibbiyot xodimlarini davlat ro'yxatiga olish**, 2028-dan **akkreditatsiyasiz muassasa Sug'urta jamg'armasidan pul olmaydi**. Har bir deadline — **majburiy xaridor** yaratadi.
8. **Ma'lumotlar huquqi o'zgardi (foyda uchun):** 2026-yil 26-martdagi **1125-son qonun** lokalizatsiyani yumshatdi — endi faqat biometrik, genetik va telekom ma'lumotlari O'zbekistonda saqlanishi shart. Tibbiy ma'lumot esa **alohida toifa** (aniq rozilik talab qiladi). Ya'ni global LLM ishlatish **huquqiy jihatdan mumkin bo'ldi** — bu 2025-da imkonsiz edi.
9. **Unit economics hal qiluvchi:** klinika SaaS'da O'zbekistonda o'rtacha chek **$50/oy** → CAC $1 000 → **qaytish 20 oy = bankrot**. "Har vrachga" modelida ($10/vrach/oy × 10 vrach = $100/oy) → **qaytish 10 oy = ishlaydi**. Ya'ni **narxlash modeli — mahsulotdan muhimroq**.
10. **Yakuniy tavsiya (11-bo'limda to'liq):** 8 ta g'oya 9 mezon bo'yicha baholandi. G'olib — **"Vrach hujjati / qabul protokoli" pozitsiyasi**, lekin **klinika emas, dorixona va tuman poliklinikasi** kanali orqali va **"har vrachga"** narxlashda. Ikkinchi o'rin — **yo'llanma marshrutlash** (B2G, sekin lekin himoyalangan).

---

# 1. BOZOR ANATOMIYASI — PUL QAYERDA

## 1.1 Global o'lchov (✅ tasdiqlangan)

| Ko'rsatkich | Qiymat | Manba |
|---|---|---|
| Sog'liq AI bozori, 2025 | $21.7–39.3 mlrd (ta'rifga qarab) | MarketsandMarkets / Grand View / Fortune BI |
| Sog'liq AI bozori, **2026** | **$37–56 mlrd** | bir nechta konsensus |
| 2030 prognoz | **$110–185 mlrd** | MarketsandMarkets / Precedence |
| CAGR | **37–44%** | konsensus |
| AI sog'liq venchur investitsiyasi, 2025 | **$18+ mlrd** = barcha sog'liq venchurining **46%** | Rock Health / CB Insights |
| AQSh raqamli sog'liq fondi, 2025 | $14.2 mlrd (+35% y/y) | Rock Health |
| AI-kompaniyalar ulushi raqamli sog'liq fondida | **54%** (2023-da 33%) | Rock Health |
| **Ambient documentation** bozori, 2024 | **$1.85 mlrd** → 2033: **$17.75 mlrd** (CAGR 28.7%) | orbdoc / bozor hisoboti |
| Hujjatga ketadigan vrach vaqti | **34–55%** ish vaqti | JAMA Internal Medicine, 2023 |
| Ambient scribe bilan tejam | **40–50%** hujjat vaqti = **2+ soat/kun** | bir nechta vendor tadqiqoti |
| AQShda scribe ishlatadigan vrachlar | **<10%** (2025 boshi) → prognoz 60% | orbdoc |
| Vrachlar AI ishlatishi (AQSh) | **63%** (noy 2025–yan 2026), 47% dan (mart 2025) | Doximity |
| GenAI pilotlarning muvaffaqiyatsizligi | **95%** | MIT tadqiqoti |

## 1.2 O'zbekiston o'lchovi — bu yerda pul boshqacha

| Ko'rsatkich | Qiymat | Manba |
|---|---|---|
| Aholi | 38 mln+ | Prezident tabrigi, 07.11.2026 |
| **Ambulatoriya-poliklinika muassasalari** (01.01.2026) | **8 912 ta** (66.5% — kichik biznes) | anhor.uz / Statistika |
| **Toshkent shahri** | **1 238 ta** | shu |
| Farg'ona / Samarqand | 1 098 / 860 | shu |
| Eng kam: Sirdaryo / Jizzax / Qoraqalpog'iston | 226 / 298 / 379 | shu |
| **Xususiy klinikalar soni** | 2016: 3 200 → **2026: 8 700** | Prezident taqdimoti, 01.05.2026 |
| Ruxsat etilgan ixtisoslashuv turlari | 39 → **116** | shu |
| Xususiy sektor koykalari | 16 000 → **57 000**; umumiy fonddagi ulush 12% → **31%** | shu |
| **DMED qamrovi** | 38 mln e-karta; **8 000+ xususiy klinika + 6 000 dorixona** ulangan; 3 600+ muassasa; 125 IT-mutaxassis; 200 000 tibbiyot xodimi o'qitilgan | asdr.gov.uz, 10.06.2026 |
| Poliklinikalarda kompyuter tanqisligi | **75 000+ kompyuter yetishmaydi** | gazeta.uz, 15.10.2025 |
| Ma'lumot sizib chiqishi | **100 GB+** (tashxislar, FISH, JSHSHIR, pasport) darknetga tushgan | gazeta.uz, 15.10.2025 |
| **E-retsept** | 10.12.2025 dan Toshkent + 15 tuman pilot; **12 817 retseptli dori**; **2027-yil yanvardan majburiy** | VMQ 570, uzdaily |
| E-retsept qamrovi (pilot hududlar) | davlat muassasalari 383 + 1 319 dorixona to'liq; xususiy klinikalarning **49%** (Toshkentda **41%**) | gazeta.uz, 13.12.2025 |
| Sug'urta jamg'armasi xaridi | **2028-dan akkreditatsiyasiz muassasa pul olmaydi** | Prezident taqdimoti, 01.05.2026 |
| Akkreditatsiya bosqichlari | 1.04.2027 — 55 respublika; 2028 — 413 hududiy; 2030 — 3 000+ tuman | shu |
| Xodimlarni davlat ro'yxatiga olish | 2027 — ixtiyoriy; **2030 — majburiy** | zamin.uz, 10.09.2026 |
| Tibbiy turizm | 86 199 bemor (2025) | rasmiy |
| **Davlat startap fondi (UzVC)** | har loyihaga **5 mlrd so'mgacha**, 3 yil 0%, davlat ulushi ≤49% | vaqt.uz, 01.09.2026 |

## 1.3 Pul oqimi xaritasi — kim aslida to'laydi

```
        PUL MANBALARI                          QAROR QABUL QILUVCHI
┌───────────────────────────────┬──────────────────────────────────────┐
│ 1. Davlat budjeti             │ Sog'liqni saqlash vazirligi,          │
│    (eng katta, eng sekin)     │ Uzinfocom (DMED egasi), Sug'urta      │
│                               │ jamg'armasi. Sikl: 9–18 oy, tender     │
├───────────────────────────────┼──────────────────────────────────────┤
│ 2. Sug'urta jamg'armasi       │ 2028-dan akkreditatsiya + sifat KPI    │
│    (o'sayotgan)               │ → raqamli nazorat majburiy             │
├───────────────────────────────┼──────────────────────────────────────┤
│ 3. Xususiy klinika (8 700)    │ Egasi (ko'pincha vrach-egasi).         │
│    (eng tez, eng kichik chek) │ Byudjet: $50–200/oy                    │
├───────────────────────────────┼──────────────────────────────────────┤
│ 4. Dorixona (6 000 DMED'da)   │ Egasi. E-retsept majburiyati =          │
│                               │ majburiy xaridor                       │
├───────────────────────────────┼──────────────────────────────────────┤
│ 5. Bemor (B2C)                │ 38 mln. Lekin to'lash odati past;      │
│                               │ ARPU $2–5/oy, CAC yuqori               │
├───────────────────────────────┼──────────────────────────────────────┤
│ 6. Farmatsevtika kompaniyasi  │ Tibbiy vakil tizimi (LIMA, AI500) —    │
│    (eng ko'p pul, eng kam IT)  │ B2B, lekin kichik bozor               │
└───────────────────────────────┴──────────────────────────────────────┘
```

> **Strategik xulosa #1:** "eng katta pul" (davlat) va "eng tez pul" (xususiy klinika) — **bir xil mahsulot emas**. Hackathon'da ikkalasini bir vaqtda va'da qilish = hakamlar ishonmaydi. **Bittasini tanlang, ikkinchisini "keyingi qadam" deb ayting.**

---

# 2. RAQOBAT LANDSHAFTI — KIM SIZNI O'LDIRADI

## 2.1 Global o'yinchilar (bilish shart — hakamlar so'rashi mumkin)

| Kompaniya | Kimga | Narx | Traksiya |
|---|---|---|---|
| **Microsoft Dragon Copilot** (sobiq Nuance DAX) | Shifokor, ambulator va shifoxona | **$99–600/vrach/oy** (ro'yxat $369) | **100 000+ klinitsist, 600+ tashkilot**; Nuance $19.7 mlrd ga sotib olingan (2022) |
| **Abridge** | Yirik tizimlar (Epic-deep) | ~**$208–350**/vrach/oy | KLAS ambient AI g'olibi 2025 va 2026; Mayo, Duke, Kaiser; **VA enterprise kontrakti (sent 2026)** |
| **Ambience Healthcare** | Yirik tizimlar | **$300–500+** | **$1.25 mlrd baho**; Cleveland Clinic 4 000 klinitsistni 4 oyda ulagan; KLAS ~97.7 |
| **Suki** | Ambulator + ovozli buyruq | **$149–399** | $168M jalb qilgan |
| **Nabla** | Ambulator, kichik amaliyot | **$119–299** | **35 til**, 55+ ixtisoslik |
| **DeepScribe** | Ixtisoslashgan ambulator | ~$750 (yuqori segment) | KLAS Emerging Spotlight 98.8 |
| **Freed / Heidi Health** | Yakka shifokor | **$30–99** (Heidi bepul tier) | Eng past kirish narxi |

**Muhim xulosa:** global bozorda narx **18 oyda keskin pasaydi** ($200–400 → $99–199). Bu **tovar tusiga** o'tgan bozor belgisi. Ya'ni **"biz AQShga chiqamiz"** — o'lik strategiya; u yerda Microsoft va Abridge bor.

## 2.2 O'zbekiston o'yinchilari — haqiqiy raqobat

| O'yinchi | Nima qiladi | Sizga tahdid darajasi |
|---|---|---|
| **Uzinfocom / DMED** | Yagona tibbiy platforma: e-karta, e-poliklinika, e-shifoxona, **e-retsept**, 2026 oxirida "yadro" | 🔴 **O'TA YUQORI** — platforma egasi. Ular modul qo'shsa, sizning mahsulot ortiqcha bo'ladi |
| **Sug'urta jamg'armasi (SHIF)** | Reimbursement, dori qoplamasi, sifat nazorati | 🟠 Xaridor ham, raqib ham |
| **Med24.uz** | Klinika/shifokor agregatori, onlayn navbat, sharhlar | 🟠 Sizning "navbat" g'oyangizni allaqachon qiladi |
| **1Clinic** | Xususiy klinika, stomatologiya, laboratoriya uchun **CRM/ERP** | 🔴 **Mavjud** — klinika ish oqimi band |
| **Doctor Yan** | Tibbiy tasvirlash uchun **XAI platforma** (saraton diagnostikasi) | 🟠 Radiologiya band |
| **Shifo.uz** | Tibbiy kontent/ma'rifat | 🟢 Raqib emas |
| **Hackathon g'oliblari** | "21" (klinika oqimi), Med IQ (ruhiy salomatlik), OnaPulse (ona), Agora, Future Tech | 🟠 Brend/mentor afzalligi bor |
| **AI500 g'oliblari** | **Medvoice AI** (tibbiy hujjat), Apollo | 🟠 Medvoice — ambient scribe yo'nalishida **oldinda** |

> **Strategik xulosa #2:** O'zbekistonda **"bo'sh maydon" degan narsa yo'q** — faqat **"kim egallaganini bilmagan maydon"** bor. Har bir g'oya uchun bitta aniq raqib bor. Buni pitch'da **o'zingiz aytib**, keyin farqni ko'rsating — bu ishonch yaratadi (hakamlar "bu jamoa bozorni o'rgangan" deb o'ylaydi).

## 2.3 Raqobat xaritasi — to'yinganlik

```
                    YUQORI TO'YINGANLIK
                            ▲
   Radiologiya (Doctor Yan) │ Klinika CRM (1Clinic)
   Onlayn navbat (Med24)    │ Semptom-cheker (hackathon×N)
                            │
   ─────────────────────────┼─────────────────────────►  YUQORI QIYMAT
   Ambient scribe           │ Yo'llanma marshrutlash
   (Medvoice AI: 2-o'rin)   │ (hech kim)
                            │
   Dorixona e-retsept       │ Sug'urta/claims
   (faqat DMED moduli)      │ (hech kim)
                            ▼
                    PAST TO'YINGANLIK
```

---

# 3. O'LIM SABABLARI — 12 TA, HAR BIRI O'ZBEKISTONDA QANDAY KO'RINADI

> Bu bo'lim **eng muhim**. Har bir o'lim sababi: (a) global dalil, (b) O'zbekistondagi ko'rinishi, (c) hackathon'da qanday oldini olish.

## O'lim #1 — "Bozorda ehtiyoj yo'q" (42% hollarda asosiy sabab)

**Global dalil:** CB Insights 483 post-mortem → 42%. Ya'ni **har ikkinchi startap o'zi o'ylab topgan muammoni hal qiladi**.

**O'zbekistonda qanday ko'rinadi:**
- "Shifokorlar hujjat yozishga ko'p vaqt sarflaydi" — **haqiqat**, lekin **to'laydimi?** Klinika egasi ko'pincha shifokorning vaqtini emas, **bemor oqimini** hisoblaydi.
- "Bemorlar navbatda uzoq kutadi" — haqiqat, lekin **bemor to'lamaydi**, klinika esa Med24'da bepul ro'yxatdan o'tadi.
- "Qishloqda shifokor yo'q" — haqiqat, lekin **xaridor — davlat**, va davlat DMED orqali markazlashgan yechim quryapti.

**Diagnostika savoli (buni o'zingizga bering):** *"Kim, bugun, o'z cho'ntagidan pul chiqarib, buni sotib oladi — va nechta bunday odam bor?"* Javob raqamsiz bo'lsa — o'lim #1.

**Hackathon'da oldini olish:** pitch'ning 1-slaydida **xaridorning ismi va soni**: *"Toshkentdagi 1 238 ambulator muassasaning 41% i e-retseptni qo'lda yuritadi — bu 507 muassasa."*

## O'lim #2 — Olive AI sindromi: "Universal platforma" va'dasi

**Nima bo'ldi:** Olive AI $902M yig'ib, $4 mlrd baholanib, "har qanday ish oqimini avtomatlashtiradigan universal AI OS" va'da qildi. Haqiqatda — **mo'rt RPA skriptlar**. 900+ shifoxona, keyin **yangilanish (renewal) stavkalari quladi**. 2022: 450 kishi bo'shatildi; 2023 fevral: 215; **31-oktabr 2023: yopildi**, aktivlar Waystar va Humata Health'ga bo'lib sotildi.

**Asl o'lim sababi (autopsiya):**
1. **Vision mahsulotdan uzoqlashdi** — "AI OS" marketing, mahsulot esa bitta tor ish oqimi edi.
2. **Inkogerent kengayish** — RCM → supply chain → clinical trials → hammasi bir vaqtda; hech birida chuqurlik yo'q.
3. **Buzilgan unit economics** — $100M+ kuydirish, $30–60M daromad; har mijoz uchun **qo'lda implementatsiya** → foyda marjasi yo'q.
4. **Foiz stavkalari o'zgardi** → qayta moliyalash imkonsiz.

**O'zbekistonda qanday ko'rinadi:**
> "Biz O'zbekiston uchun yagona AI tibbiy platforma quryapmiz — klinika, dorixona, laboratoriya, sug'urta, bemor — hammasi bitta ilovada."

Bu jumla **hakamlar uchun chiroyli, investor uchun o'lik**. Sabab: DMED allaqachon shu platforma, va uni **davlat** quryapti.

**Hackathon'da oldini olish:** **bitta ish oqimi, bitta foydalanuvchi, bitta ekran.** Pitch'da: *"Biz platforma emasmiz. Biz DMED ustidagi bitta modulmiz — 6 daqiqani qaytaradigan modul."*

## O'lim #3 — Forward Health sindromi: hardware va jismoniy infratuzilma

**Nima bo'ldi:** $650–750M jalb qildi. **3 200 ta "CarePod"** kioskini bir yilda va'da qildi. **5 ta** yetkazdi. Har biri **$1M+** turdi. Bemorlar ichida qamalib qolgan holatlar bo'ldi. **Noyabr 2024: yopildi**, 200 kishi ishsiz.

**O'zbekistonda qanday ko'rinadi:**
- "Biz portativ EKG qurilma yasaymiz" — 48 soatda **ishonchli prototip** qurib bo'lmaydi, va sertifikatlash 6–12 oy.
- "Klinikaga sensorlar o'rnatamiz" — sotuv sikli 6+ oy, o'rnatish xizmati = past marja.

**Hackathon'da oldini olish:** hardware bo'lsa — **faqat "tayyor qurilma + dasturiy demo"** (masalan, telefon sensori, mavjud spirometr). Pitch'da: *"Biz qurilma yasamaymiz — mavjud qurilma ma'lumotini o'qiymiz."*

## O'lim #4 — Babylon Health sindromi: klinik da'vo va xavfsizlik

**Nima bo'ldi:** AI bilan birlamchi yordam va'da qildi; **diagnostika aniqligi va xavfsizligi** bo'yicha jiddiy shubhalar; AQSh operatsiyalari **2023-avgustda bankrotlik**, Buyuk Britaniya qismi eMed'ga sotildi.

**O'zbekistonda qanday ko'rinadi:** "AI tashxis qo'yadi" — regulyator nuqtai nazaridan bu **tibbiy xizmat**, ya'ni litsenziya, mas'uliyat va klinik sinov talab qiladi. Bundan tashqari, hakamlar orasida **Sog'liqni saqlash vazirligi vakili bor** — ular bu da'voni darhol ushlaydi.

**Hackathon'da oldini olish (va bu eng kuchli farqlantiruvchi):** **"Biz tashxis qo'ymaymiz"** deb ochiq aytish.
- ✅ "Biz hujjat yozamiz, vrach tasdiqlaydi"
- ✅ "Biz navbatni optimallashtiramiz, qaror vrachda"
- ✅ "Biz retseptni tekshiramiz, javobgarlik vrachda"
- ❌ "Biz kasallikni aniqlaymiz"

> Bu bitta jumla hakamlar oldida **ishonchni ikki barobar** oshiradi — chunki u **regulyator tilida** aytilgan.

## O'lim #5 — Pear Therapeutics sindromi: klinik isbot bor, xaridor yo'q

**Nima bo'ldi:** raqamli terapevtika, FDA tasdiqlari bor edi — lekin **sug'urta to'lamadi** va shifokorlar buyurmadi. Aktivlar **$6 mln** ga auksionda sotildi.

**O'zbekistonda qanday ko'rinadi:** "Bizda klinik protokol bor, ilmiy asoslangan" — lekin **Sug'urta jamg'armasi qoplamasa**, hech kim to'lamaydi. Faqat 2028-dan keyin reimbursement kengayadi.

**Hackathon'da oldini olish:** **kim to'laydi** degan savolga aniq javob: *"Birinchi 6 oyda klinika o'zi to'laydi, chunki u vaqtni tejaydi. 2028-dan sug'urta sifat ko'rsatkichi uchun to'laydi."*

## O'lim #6 — Proteus Digital Health: "aqlli tabletka" — 15 yil, $500M+, bankrot

**Sabab:** texnologiya ishladi, lekin **shifokor uni buyurmadi**, **sug'urta qoplamadi**, va **xatti-harakatni o'zgartirish** kutilganidek bo'lmadi. Ya'ni **texnik muvaffaqiyat ≠ tijoriy muvaffaqiyat**.

**O'zbekistonda:** "Bemor dorini ichganini AI tekshiradi" — bu **adherenс** muammosi; lekin O'zbekistonda dori **qoplamasi** endi shakllanmoqda, ya'ni xaridor hali yo'q.

## O'lim #7 — VillageMD / Teladoc-Livongo: birlashish orqali o'sish (M&A o'limi)

**Nima bo'ldi:** Teladoc Livongo'ni **$18.5 mlrd** ga sotib oldi → keyin **~$13 mlrd** qiymatdan hisobdan chiqardi. VillageMD katta investitsiyadan keyin **impairment** va sekin bemor qabuli.

**O'zbekistonda:** "Keyin yirik klinika tarmog'i bilan birlashamiz" — bu **strategiya emas, umid**.

## O'lim #8 — "AI teatr" (AI theater)

**Global dalil:** Builder.ai'ning "AI" i **700 nafar inson muhandis** edi. Forward 3 200 va'da → 5 yetkazdi. Humane'ning demosi mahsulotga o'xshamas edi. **Naqsh bir xil: demo pul yig'adi, mahsulot yo'q.**

**O'zbekistonda qanday ko'rinadi:** slaydda "GPT-4 + computer vision + blockchain", kodda esa **qattiq yozilgan if-else** va bitta API chaqiruvi.

**Hackathon'da:** hakamlar buni **checkpoint'da** ko'radi. Ya'ni **2-kun 15:00 da** demo ishlamasa — AI teatr sifatida baholanadi va siz **TOP-20 ga kirmaysiz**.

## O'lim #9 — "Pilot qabristoni" (pilot purgatory)

**Global dalil:** **95%** genAI pilotlari muvaffaqiyatsiz (MIT). Scribe'larda **foydalanish darajasi 20–50%** (ya'ni litsenziya sotib olinadi, lekin shifokorlar ishlatmaydi).

**O'zbekistonda qanday ko'rinadi:** klinika "sinab ko'ramiz" deydi → 3 oy → "keyin ko'ramiz". **Sotuv bo'lmagan pilot = marketing xarajati.**

**Yechim:** pilotni **pullik** qiling (kichik bo'lsa ham). Bepul pilot hech qachon konversiyaga aylanmaydi.

## O'lim #10 — Regulyator kechikishi

**O'zbekistonda aniq misol:** tibbiy ma'lumot — **alohida toifa** (aniq rozilik talab qiladi); biometrik ma'lumot **faqat O'zbekistonda** saqlanishi shart (1125-son qonun, 26.03.2026); ma'lumotlar bazasini **davlat reyestriga** kiritish shart; sizib chiqish haqida **24 soat** ichida xabar berish.

**Ya'ni:** agar mahsulotingiz **bemor ovozi yozuvi** yoki **yuz tasviri** bilan ishlasa — siz **biometrik ma'lumot** bilan ishlayapsiz → lokal server + rozilik + ro'yxat. Buni pitch'da aytmasangiz, savol beriladi va javobsiz qolsangiz — ball tushadi.

## O'lim #11 — Noto'g'ri jamoa (23%)

**Global:** "wrong team" 23%. **O'zbekiston sog'liq trekida:** agar jamoada **bitta ham medik bo'lmasa**, hakam savollari: "qaysi protokol? qaysi tashxis kodi (ICD)? qaysi hujjat shakli? kim imzolaydi?" — javob bermaysiz.

## O'lim #12 — Vaqt noto'g'ri (29%)

**Global:** "bad timing" 29% — ikkinchi eng katta asosiy sabab.

**O'zbekistonda:** bu **eng qiziqarli**, chunki vaqt **aynan hozir to'g'ri**:
- **10.12.2025** — e-retsept piloti boshlandi
- **yanvar 2027** — e-retsept **majburiy**
- **1 aprel 2027** — 55 respublika muassasasi akkreditatsiya
- **2028** — akkreditatsiyasiz muassasa SHIF pulini olmaydi
- **2026 oxiri** — DMED "yadro" ishga tushadi
- **2030** — tibbiyot xodimlari davlat ro'yxatida majburiy

> **Ya'ni 2026–2028 — O'zbekiston sog'liq AI uchun "regulyator oynasi".** Bu **3 yillik majburiy xaridor to'lqini**. Hackathon pitch'ida shu jadvalni ko'rsatish — eng kuchli "why now" dalili.

---

# 4. O'ZBEKISTONGA XOS 8 STRUKTURA TUZOG'I

Bular global darsliklarda yo'q — faqat mahalliy bozor bilimi.

| # | Tuzoq | Mexanizm | Qanday chetlab o'tish |
|---|---|---|---|
| 1 | **DMED monopoliyasi** | Platforma egasi = davlat + Uzinfocom. Ular modul qo'shsa, siz ortiqchasiz | **Ularning ustiga qur** (eksport/import, PDF, QR). Hech qachon "alternativ EHR" demang |
| 2 | **Xususiy klinika IT byudjeti ~0** | Klinika egasi — vrach; IT xarajati "hashamat" deb qaraladi | Narxni **bir vrach oyligiga** bog'lang: "bitta vrachning 2 soati" |
| 3 | **Davlat xaridi sikli 9–18 oy** | Tender, texnik topshiriq, byudjet yili | Hackathon'da B2G **va'da qilmang**; "2027-dan keyin" deng |
| 4 | **"Yaxshi ko'rdik, keyin gaplashamiz" madaniyati** | Rad etishni yuzma-yuz aytish qiyin → soxta ijobiy signal | **Yozma** rozilik so'rang: "sinov uchun qancha to'laysiz?" |
| 5 | **Ma'lumot yo'qligi** | Ochiq tibbiy dataset deyarli yo'q; DMED ma'lumoti yopiq | **Sintetik + o'z qo'lingiz bilan yig'ilgan** kichik dataset bilan ishlang |
| 6 | **Kadr aylanmasi / kompyuter savodxonligi** | 200 000 xodim o'qitilgan, lekin keksa avlod qiyinchilik bilan | Interfeys: **1 ekran, katta tugma, o'zbek tilida, klaviatura minimal** |
| 7 | **Valyuta va narx bosimi** | API/cloud xarajati dollarda, daromad so'mda | **Mahalliy model / offline rejim / batching**; LLM xarajatini unit economics'ga qo'shing |
| 8 | **Tibbiy mas'uliyat (defensive medicine)** | Xato bo'lsa — vrach javobgar, tizim emas | **"Vrach tasdiqlaydi"** dizayni: AI taklif qiladi, inson imzolaydi. Bu huquqiy qalqon |

---

# 5. UNIT ECONOMICS — 3 MODEL, ANIQ RAQAMLAR

> Bu bo'lim **bankrotlikni oldini oladigan** yagona bo'lim. Har bir model: ARPU, CAC, churn, payback, LTV/CAC.

## Model A — Klinika SaaS ("obyekt" narxlash) ❌

| Parametr | Qiymat | Izoh |
|---|---|---|
| Maqsadli mijoz | Xususiy klinika (5–15 vrach) | 8 700 ta mavjud |
| Real oylik to'lov | **500 000 so'm ≈ $42** | Bozor toqati |
| ACV | **$500/yil** | |
| CAC (to'g'ridan-to'g'ri sotuv) | **$800–1 200** | 1 sotuv menejeri yiliga 15–20 ta yopadi; xarajat $15–20k |
| **Qaytish muddati** | **19–29 oy** | 🔴 **O'LIM** |
| Churn (yillik) | 25–35% | Kichik klinikalarda yuqori |
| LTV/CAC | **~1.2** | 🔴 Yashash uchun ≥3 kerak |

**Hukm:** **buzilgan model.** $42/oy uchun $1 000 CAC hech qachon qoplanmaydi. **A variantini tanlamang.**

## Model B — "Har vrachga" (per-seat) narxlash ✅

| Parametr | Qiymat | Izoh |
|---|---|---|
| Narx | **100 000 so'm/vrach/oy ≈ $8.4** | Global $99–200 dan 12–24× arzon, lekin mahalliy oylikka nisbatan tushunarli |
| O'rtacha klinika | 8 vrach | → **$67/oy**, $800/yil |
| ACV | **$800–1 400/yil** | |
| CAC | **$700–900** | (bir xil sotuv, lekin yuqori chek) |
| **Qaytish** | **10–13 oy** | 🟡 **Chegarada, lekin ishlaydi** |
| Churn | 20% | "Har vrach" modelida yopishish yuqori (vrach o'zi ishlatadi) |
| LTV/CAC | **~2.5–3.0** | 🟢 Qabul qilsa bo'ladi |
| Kengayish | Yangi vrach qo'shilganda daromad **avtomatik** o'sadi | 🟢 "Land & expand" |

**Hukm:** **ishlaydi, lekin sekin.** 3 yilda 250 klinika = **$250k ARR**. Bu venchur uchun kichik, lekin **bootstrap uchun yaxshi**.

## Model C — Dorixona / B2B2B (e-retsept to'lqini) ✅✅

| Parametr | Qiymat | Izoh |
|---|---|---|
| Maqsadli mijoz | DMED'ga ulangan **6 000 dorixona** | + 2027-dan **majburiy** |
| Narx | **250 000 so'm/dorixona/oy ≈ $21** | Dorixona uchun arzon: bitta xato retsept = jarima |
| ACV | **$250/yil** | |
| CAC | **$150–250** | Kanalsiz, telefon + Telegram orqali, chunki **majburiyat** bor |
| **Qaytish** | **7–12 oy** | 🟢 |
| Churn | 10% (majburiyat tufayli) | 🟢 |
| LTV/CAC | **~5–8** | 🟢🟢 |
| Masshtab | 1 000 dorixona = **$250k ARR**; 3 000 = **$750k** | 🟢 |

**Hukm:** **eng yaxshi unit economics** — chunki xaridor **qonun bo'yicha majbur**, va chek kichik bo'lsa ham CAC juda past.

## Model D — B2G (DMED integratsiyasi) ⚠️

| Parametr | Qiymat |
|---|---|
| Kontrakt hajmi | $50k–500k |
| Sikl | **9–18 oy** |
| Raqib | **Uzinfocom** (platforma egasi) |
| Ehtimol | past (tender, siyosiy) |
| Hukm | **birinchi mahsulot uchun yaramaydi**; 2–3-yilda "katta kontrakt" sifatida |

## 5.1 Xulosa — model tanlovi

```
Model A (klinika SaaS, obyekt)  ████░░░░░░  $500 ACV → 25 oy payback  ❌
Model B (har vrachga)           ███████░░░  $900 ACV → 11 oy payback  ✅
Model C (dorixona, majburiy)    █████████░  $250 ACV →  9 oy payback  ✅✅
Model D (B2G)                   ██░░░░░░░░  9–18 oy sikl            ⚠️
```

> **Strategik xulosa #3:** Hackathon pitch'ida **Model B yoki C** ni ayting, Model A ni **hech qachon**. Agar "klinikaga $50/oy ga sotamiz" desangiz, tajribali hakam (investor bo'lsa) **unit economics'ni darhol hisoblaydi** va savol beradi.

## 5.2 O'zbekiston bozorining haqiqiy hajmi (SAM)

| Segment | Soni | Oylik chek | **Yillik potensial** |
|---|---|---|---|
| Xususiy klinikalar (Model B, 30% qamrov) | 2 610 × $67 | | **$2.1 mln** |
| Dorixonalar (Model C, 50% qamrov) | 3 000 × $21 | | **$0.76 mln** |
| Tuman poliklinikalari (B2G, 10%) | 890 | | keyin |
| **Realistik SAM (3–5 yil)** | | | **$3–5 mln/yil** |

> **Halol gap:** bu **$100M bozor emas**. Bu **$3–5M SAM** — ya'ni **venchur emas, foydali kichik biznes**. Pitch'da "O'zbekiston + Markaziy Osiyo + MENA" deb kattalashtirsangiz, hakam savol beradi: *"Markaziy Osiyoda DMED ekvivalenti bormi? Yo'q. Unda nega siz?"* — javobingiz bo'lishi kerak: **"chunki biz O'zbekistonda regulyator to'lqinini birinchi bo'lib egallaymiz, keyin eksport qilamiz."**

---

# 6. O'ZBEKISTON DAVLAT DASTURLARI BILAN MOSLIK — "WHY NOW" DALILLARI

| Davlat dasturi / KPI | Sana | Sizning mahsulotingiz qanday yordam beradi |
|---|---|---|
| **E-retsept majburiy** | yanvar 2027 | Retsept yozish/tekshirish avtomatizatsiyasi; dorixonada qoldiq |
| **"Elektron sog'liqni saqlash yadrosi"** | 2026 oxiri | Ulanish uchun modul/konnektor |
| **Akkreditatsiya (55 → 413 → 3 000+)** | 2027–2030 | Akkreditatsiya hujjatlarini avtomatik tayyorlash + sifat monitoringi |
| **SHIF faqat akkreditatsiyalangan muassasadan xarid qiladi** | 2028 | Sifat ko'rsatkichlari paneli |
| **Tibbiyot xodimlarini davlat ro'yxatiga olish** | 2027 → 2030 | Malaka va faoliyat trekingi |
| **Raqamli xizmatlar hajmi 35 mln** | 2026 | — |
| **Xususiy klinikalarda nazorat "masofaviy baholash"** | 2026+ | Avtomatik audit va hisobot |
| **Tibbiy turizm** | o'sish | Xulosa/tarjima, hujjat paketi |
| **Sug'urta tizimi rivoji** | 2028+ | Claims sifati va tekshiruvi |

> **Bu jadval — pitch'ning 3-slaydi.** Hakamlar orasida vazirlik vakili bo'lsa, bu **ularning o'z KPI'lari** — ya'ni siz "davlat rejasining bir qismi" bo'lasiz, "yana bir startap" emas.

---

# 7. 8 G'OYA — TO'LIQ BAHOLASH MATRITSA

**Mezonlar (har biri 1–10, og'irlik bilan):**
`GD` global talab isbotlangan (15%) · `MVP` 48 soatda ishlaydigan demo (20%) · `REG` regulyator mosligi (10%) · `WHITE` raqobat bo'shligi (15%) · `WTP` to'lash irodasi (15%) · `UE` unit economics (15%) · `DEF` himoyalanish (5%) · `JURY` hakamlar jozibasi (5%)

| # | G'oya | GD | MVP | REG | WHITE | WTP | UE | DEF | JURY | **BALL** |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **Vrach hujjati / qabul protokoli (ambient-scribe-lite, o'zbekcha)** | 10 | 9 | 9 | 6 | 5 | 7 | 6 | 9 | **7.65** |
| **2** | **Yo'llanma marshrutlash + "qayerda joy bor"** | 6 | 8 | 8 | 10 | 6 | 6 | 8 | 8 | **7.25** |
| **3** | **Dorixona e-retsept oqimi (qoldiq + INN almashtirish)** | 7 | 8 | 10 | 8 | 8 | 9 | 7 | 7 | **8.05** |
| **4** | Laboratoriya natijasini birlamchi vrach uchun izohlash | 7 | 9 | 8 | 8 | 5 | 6 | 5 | 7 | **6.90** |
| **5** | Skriningga rioya (bachadon bo'yni/ko'krak saratoni) | 8 | 7 | 8 | 9 | 4 | 5 | 6 | 7 | **6.65** |
| **6** | Sug'urta / claims hujjatlari sifati | 6 | 6 | 7 | 10 | 5 | 6 | 7 | 6 | **6.40** |
| **7** | Ona-bola monitoringi | 9 | 6 | 7 | 4 | 5 | 6 | 6 | 7 | **6.40** |
| **8** | Klinika ichki oqimi / navbat | 8 | 7 | 7 | 2 | 5 | 4 | 3 | 5 | **5.35** |

### Hisoblash misoli (#3):
`7×.15 + 8×.20 + 10×.10 + 8×.15 + 8×.15 + 9×.15 + 7×.05 + 7×.05 = 1.05+1.60+1.00+1.20+1.20+1.35+0.35+0.35 = 8.10`

### Natija

| O'rin | G'oya | Ball | Nega |
|---|---|---|---|
| 🥇 | **Dorixona e-retsept oqimi** | **8.05** | Majburiy xaridor (2027), eng yaxshi unit economics, DMED bilan raqobat emas — **ustiga quriladi** |
| 🥈 | **Vrach hujjati** | **7.65** | Eng isbotlangan global talab + eng yaxshi demo; lekin **Medvoice AI bor** va **WTP past** |
| 🥉 | **Yo'llanma marshrutlash** | **7.25** | Eng bo'sh maydon, lekin xaridor davlat = sekin |
| 4 | Laboratoriya izohi | 6.90 | Yaxshi demo, past to'lov |
| 5 | Skrining | 6.65 | Katta ijtimoiy ta'sir, lekin xaridor yo'q |

---

# 8. IKKI FINALIST — CHUQUR TAHLIL

## 8.1 FINALIST A — "E-retsept oqimi" (dorixona + vrach)

**Mahsulot:** Vrach e-retseptni DMED'da yozadi → tizim **dorixonalardagi real qoldiqni** ko'rsatadi → **INN (xalqaro nom) bo'yicha almashtirish** taklif qiladi → dorixonada **tekshiruv + qoldiq yangilanishi** → bemorga **Telegram** orqali "qaysi dorixonada bor" xabari.

**Nega yutadi:**
- **Majburiyat:** 2027-yil yanvardan 12 817 dori e-retsept bilan.
- **Bugungi muammo raqamda:** xususiy klinikalarning faqat **49%** (Toshkentda **41%**) e-retseptni ishlatadi → ya'ni **yarim bozor hali qo'lda**.
- **Unit economics Model C** — eng yaxshi (8-o'rin emas, 1-o'rin).
- **DMED bilan raqobat yo'q** — bu uning **moduli**.
- **Xorazm/Qarshi trek nomi** "sog'liq + **farmatsevtika**" → Toshkent trek nomida ham farma bor.

**Nega o'lishi mumkin (red team):**
- DMED o'zi qoldiq modulini qo'shsa → mahsulot ortiqcha.
- Dorixonalar integratsiyaga majbur, lekin **qo'shimcha to'lovga** majbur emas.
- 6 000 dorixona bilan sotuv — **operatsion og'ir**.

**O'limni qanday oldini olish:**
- **Qatlam tanlang:** "qoldiq" emas, **"retsept sifati va almashtirish tavsiyasi"** (klinik qiymat).
- **Kanal:** dorixona **tarmoqlari** (bitta shartnoma = 50–200 nuqta), yakka dorixonani chetga qo'ying.
- **Demo:** 48 soatda **3 ekran** — vrach retsepti, dorixona tekshiruvi, bemor Telegram. Boshqa hech narsa yo'q.

## 8.2 FINALIST B — "Vrach hujjati" (ambient scribe-lite)

**Mahsulot:** Vrach qabulni boshlaydi → telefon/notebook mikrofon → o'zbek (va rus) tilida **nutq → matn** → tuzilgan **qabul xulosasi** (shikoyat, anamnez, obyektiv holat, tashxis, tavsiya) → vrach **tasdiqlaydi va imzolaydi** → DMED'ga eksport.

**Nega yutadi:**
- Global isbot: **$1.85 → $17.75 mlrd**, **63% vrach AI ishlatadi**, **34–55% vaqt hujjatga ketadi**.
- Demo **juda ta'sirli** — 3 daqiqada ko'rsatish mumkin, ko'z bilan "aha" bo'ladi.
- **"Tashxis qo'ymaymiz"** chegarsi — regulyator uchun xavfsiz.

**Nega o'lishi mumkin (red team):**
- **Medvoice AI** AI500'da shu yo'nalishda 2-o'rin olgan → "ko'rilgan" taassurot.
- **WTP past:** vrach vaqtini tejash klinika egasi uchun pul emas.
- **Nutq aniqligi:** o'zbek tibbiy nutqida ASR sifati past bo'lishi mumkin → demo yiqiladi.
- **Xarajat:** LLM + ASR dollarda; so'mda daromad.

**O'limni qanday oldini olish:**
- **Nuqta o'zgartirish:** "hujjat yozish" emas, **"nazorat ro'yxati"** — ya'ni *"bu qabulda qanday majburiy punktlar to'ldirilmagan"* (defensive medicine uchun). Bu **yuridik qiymat**, ya'ni klinika egasi tushunadigan qiymat.
- **Til chegarasi:** demo **rus tilida** (Toshkentda ko'p vrach rus tilida gaplashadi, ASR sifati yuqori) + o'zbekcha qo'shimcha.
- **Narx:** faqat **"har vrachga"** Model B.

## 8.3 Qaysi birini tanlash — qaror daraxti

```
Hakamlar tarkibini bilasizmi?
├── HA, va u yerda investor/venchur bor
│     → FINALIST A (e-retsept) — unit economics himoya qiladi
├── HA, va u yerda vazirlik/DMED vakili bor
│     → FINALIST A — chunki u DMED'ni to'ldiradi, raqib emas
├── HA, va u yerda tibbiyot amaliyotchisi (vrach) ko'p
│     → FINALIST B (hujjat) — u darhol og'riqni tan oladi
└── BILMAYSIZ
      → FINALIST A, + B ning demosini 30 soniyalik "qo'shimcha"
```

---

# 9. BANKROTLIK SIMULYATSIYASI — 24 OY, 3 STSENARIY

> Bu bo'lim savolga javob beradi: **"Agar bundan keyin davom etsangiz, qanday o'lasiz?"**
> Barcha raqamlar **$ ming** (ming AQSh dollari), Model C (dorixona) + Model B (vrach) gibridi.

## 9.1 Boshlang'ich shartlar

| Parametr | Qiymat |
|---|---|
| Jamoa | 3 kishi (2 dev + 1 tibbiy maslahatchi) |
| Oylik xarajat (jamoa, minimal) | **$2.5k** (O'zbekiston sharoitida, qisman talaba) |
| Infratuzilma (API, server, ASR/LLM) | **$0.25k/oy** |
| Huquqiy + ma'lumotlar bazasi ro'yxati + server (biometrik bo'lsa) | **$2k** bir martalik |
| **Boshlang'ich kapital (hackathon mukofoti)** | 5 MacBook ≈ **$5k** (naqd emas — aktiv) |
| **Real naqd (o'z hisobidan / UzVC / grant)** | **$10k** minimal |

## 9.2 Uch stsenariy

### BEAR (60% ehtimol) — "hech kim to'lamadi"

| Chorak | Mijoz | MRR | Xarajat | Naqd | Holat |
|---|---|---|---|---|---|
| Q1 | 0 | $0 | $8.9k | $6.1k | Hackathon o'tdi, "qiziqdik" deyishdi |
| Q2 | 2 (bepul pilot) | $0.05k | $8.9k | **-$2.7k** | 🔴 **Naqd tugadi** |
| Q3 | — | — | — | — | **Yopildi** |

**O'lim sababi:** O'lim #9 (pilot qabristoni) — bepul pilotlar hech qachon to'lovga aylanmadi.
**Oldini olish signali:** Q1 oxirida **1 ta to'lagan mijoz** bo'lmasa → pivot.

### BASE (30% ehtimol) — "sekin, lekin ishlaydi"

| Chorak | Mijoz | MRR | Xarajat | Naqd | Holat |
|---|---|---|---|---|---|
| Q1 | 3 | $0.25k | $8.9k | $6.1k | 1 pilot pullik |
| Q2 | 10 | $0.8k | $8.9k | $2.0k | **Q3 da inqiroz** |
| Q3 | 25 | $2.0k | $9.5k | **-$4.5k** | 🔴 kassada teshik |
| Q4 | 45 | $3.6k | $10k | -$5.9k | grant/UzVC kerak |
| Y2 | 150 | $12k | $14k | + | o'sish |

**O'lim sababi (agar grant bo'lmasa):** O'lim #2 — **o'sish xarajatdan sekin**. Ya'ni "ishlaydigan biznes, lekin noto'g'ri vaqtda".
**Oldini olish:** **Q3 dan oldin** grant/UzVC (5 mlrd so'mgacha, 0%, 3 yil) yoki angellarga chiqish. Bu **majburiy, ixtiyoriy emas**.

### BULL (10% ehtimol) — "kanal ochildi"

| Chorak | Mijoz | MRR | Holat |
|---|---|---|---|
| Q1 | 5 | $0.4k | Kontseptsiya isbotlandi |
| Q2 | 30 (1 tarmoq shartnomasi) | $2.4k | 🟢 Kanal topildi |
| Q3 | 80 | $6.4k | |
| Y2 | 400 | $32k | $384k ARR |
| Y3 | 1 200 | $96k | $1.15M ARR → venchur/til biriktirish |

**Nega bull bo'ladi:** bitta **dorixona tarmog'i** (50–200 nuqta) shartnomasi bitta sotuv harakatining narxi bilan 100+ mijoz beradi. **CAC $200 → $20.**

## 9.3 Bankrotlik ehtimoli — halol baho

| Stsenariy | Ehtimol | Sabab |
|---|---|---|
| Yopilish (12 oy ichida) | **~55%** | Bepul pilot tuzog'i + WTP past |
| Yashash (kichik foyda, 24 oy) | **~35%** | Model C + kanal |
| O'sish ($1M ARR, 3 yil) | **~10%** | Tarmoq shartnomasi |

> **Bu normal.** Global sog'liq AI startaplarining aksariyati shu taqsimotda. Muhimi — **buni bilib kirish** va **Q1 oxirida "to'lagan mijoz bormi?"** degan qat'iy tekshiruv nuqtasini qo'yish.

---

# 10. HACKATHON UCHUN 48 SOATLIK RISK REYESTRI

| # | Risk | Ehtimol | Ta'sir | Yumshatish |
|---|---|---|---|---|
| 1 | **Demo yiqiladi** (ASR/internet) | Yuqori | Fatal | **Oldindan yozilgan audio + offline fallback + 3 marta sinov** |
| 2 | **Checkpoint'da tayyor emas** (18-noy 15:00) | O'rta | Fatal | Checkpoint'ga **1 soat oldin** tayyor bo'lish; "yadro" funksiyani erta qotirish |
| 3 | **Trek noto'g'ri tanlandi** (12:00) | Past | Fatal | 11:50 gacha qaror qilingan bo'lsin — bu hujjat shu uchun |
| 4 | **Hakam "bu DMED'da bor"** deydi | O'rta | Katta | Pitch'da **o'zingiz** ayting: "DMED bor, lekin X moduli yo'q — biz shu modulmiz" |
| 5 | **Jamoa 4 kishidan kam** (Nizom talabi) | Past | Katta | 4–5 kishi, ro'yxatni 11:00 da tekshiring |
| 6 | **Medik yo'q** | O'rta | Katta | Hech bo'lmasa 1 tibbiyot talabasi; bo'lmasa **tibbiy maslahatchi mentor** toping |
| 7 | **LLM/API xarajati / limit** | O'rta | O'rta | Kalitni oldindan to'ldiring, **kesh** qo'ying, demo uchun qattiq yozilgan javoblar zaxirasi |
| 8 | **Ma'lumot huquqi savoli** | Past | O'rta | **Sintetik ma'lumot** ishlating, pitch'da ayting: "demo sintetik, ishlab chiqarishda DMED ichida" |
| 9 | **Pitch 3 daqiqaga sig'maydi** | Yuqori | Katta | 2:40 versiyasini yozing, 5 marta ovoz chiqarib mashq |
| 10 | **"Yana bir AI tashxis" taassuroti** | O'rta | Katta | Birinchi jumla: **"Biz tashxis qo'ymaymiz"** |

## 10.1 Qizil chiziqlar — hech qachon aytmaydigan jumlalar

| ❌ Aytmang | ✅ Ayting |
|---|---|
| "AI tashxis qo'yadi" | "AI vrachga hujjat tayyorlaydi, qaror vrachda" |
| "Yagona platforma" | "Bitta modul, bitta ish oqimi" |
| "Bozor $50 mlrd" | "Toshkentdagi 1 238 muassasaning 507 tasi qo'lda ishlaydi" |
| "Keyin DMED bilan raqobat qilamiz" | "DMED ustida ishlaymiz" |
| "Pul topish modeli keyin" | "Har vrachga $8/oy, 11 oyda qaytadi" |
| "Bizning AI 99% aniqlik" | "Bizda o'lchangan ko'rsatkich yo'q — 3 haftalik pilotda o'lchaymiz" |

> **Oxirgi qator eng muhim.** "99% aniqlik" — **ishonchni yo'qotadigan** jumla (Olive AI aynan shunday va'da bilan o'ldi). "O'lchaymiz" — **ishonch yaratadigan** jumla.

---

# 11. YAKUNIY TAVSIYA — QAROR

## 11.1 Verdict

> **Trek: sog'liqni saqlash va farmatsevtika. Pozitsiya: e-retsept / dorixona oqimi (FINALIST A), ikkinchi variant — vrach hujjati (FINALIST B).**

**Nega A:**
1. **Xaridor qonun bilan majbur** — 2027-yil yanvardan. Bu **eng kuchli sotuv argumenti** dunyoda.
2. **Unit economics yagona ishlaydigan model** — payback 9 oy, LTV/CAC 5–8.
3. **DMED bilan raqobat emas** — modul. Ya'ni O'lim #1 va #2 dan qochadi.
4. **Toshkent trek nomida "farmatsevtika" bor** — hakamlar buni kutmoqda, va kam jamoa tayyorlaydi (hackathon tarixida farma loyihasi 1-o'rin olmagan).
5. **Demo 48 soatda ishlaydi** — 3 ekran, tashqi integratsiya shart emas.

**Nega B ikkinchi:**
- Eng yaxshi demo va eng isbotlangan global talab, **lekin** WTP past va **Medvoice AI** allaqachon bor.

## 11.2 Agar "sog'liq" emas, boshqa trekni tanlasangiz — bu hujjatning qaysi qismi o'tadi

| Trek | O'tadigan bo'limlar |
|---|---|
| **Ta'lim** | 3 (o'lim sabablari), 5 (unit economics), 9 (bankrotlik), 10 (risk) |
| **Tadbirkorlik** | 3, 4, 5, 9, 10 — **to'liq** |

## 11.3 Bugungi 3 ta harakat (soat bilan)

| Vaqt | Harakat |
|---|---|
| **09:50** | Mentor/tashkilotchidan so'rang: *"Sog'liq trekida Toshkentda nechta jamoa? Hakamlar kim?"* |
| **11:50** | Qaror: A yoki B. Trek tanlovi 12:00 da |
| **13:00** | 3 ekranli prototipning **qog'ozdagi** versiyasini chizing (Figma emas — qog'oz, 20 daqiqa) |
| **18:00** | Birinchi ishlaydigan ekran |

---

# 12. NIMA UCHUN BU "IS ROQ" EMAS — HALOL CHEGARA

Professional yondashuv **chegarani ham** ko'rsatadi:

| Da'vo | Haqiqat |
|---|---|
| "Sog'liq AI $50 mlrd bozor" | Ha, **global**. O'zbekiston SAM — **$3–5M/yil** |
| "O'zbekistonda telemeditsina portlaydi" | Telemeditsina **Buxoroda 1-o'rin olgan** (Med IQ), ya'ni allaqachon band |
| "AI tashxis — kelajak" | Globalda **95% genAI pilot yiqiladi**; regulyator to'sig'i eng katta |
| "Hackathon yutish = biznes" | Hackathon mukofoti **~$8k**. Bu **seed emas**, bu **signal**. |
| "DMED bizga integratsiya ochadi" | **Ehtimol, lekin kafolat emas.** Uzinfocom raqib ham |
| "UzVC 5 mlrd so'm beradi" | **Faqat tanlanganlarga**, va **qarz** sifatida (0%, 3 yil), keyin ulushga aylanadi |

---

# 13. BIR SAHIFALIK XULOSA — CHOP ETIB OLING

```
┌──────────────────────────────────────────────────────────────────────┐
│  SOG'LIQ TREKI — 60 SONIYADA                                               │
├──────────────────────────────────────────────────────────────────────┤
│  BOZOR    Global $37–56 mlrd (2026), CAGR 37–44% → 2030 $110+ mlrd    │
│           O'zbekiston: 8 912 poliklinika, 8 700 xususiy klinika,       │
│           6 000 dorixona. Real SAM: $3–5M/yil. Venchur emas.           │
│                                                                        │
│  QABRISTON Olive $902M→dead · Babylon→bankrot · Forward $700M→5 kiosk  │
│           9 kompaniya = $35 mlrd yo'q qilingan qiymat                  │
│           Sabab: 43% PMF yo'q · 70% pul tugadi (simptom) · 29% vaqt    │
│                                                                        │
│  TUZOQ    DMED = platforma egasi (Uzinfocom). Parallel EHR = o'lim.    │
│           Xususiy klinika byudjeti $42–67/oy. CAC $1000 = 20 oy.       │
│                                                                        │
│  OYNA     10.12.2025 e-retsept pilot → yanvar 2027 MAJBURIY            │
│           1.04.2027 akkreditatsiya → 2028 SHIF faqat akkreditatsiya    │
│           2026 oxiri DMED yadro → 2030 xodimlar reyestri               │
│                                                                        │
│  MODEL    A klinika SaaS ($500 ACV) ❌ 20+ oy payback                   │
│           B har vrachga ($900 ACV) ✅ 11 oy                            │
│           C dorixona ($250 ACV) ✅✅ 9 oy, LTV/CAC 5–8                 │
│           D B2G 9–18 oy sikl ⚠️                                        │
│                                                                        │
│  TANLOV   🥇 E-RETSEPT / DORIXONA OQIMI (8.05)                         │
│           🥈 Vrach hujjati (7.65)  🥉 Yo'llanma marshrut (7.25)        │
│                                                                        │
│  BANKROT  Bear 60%: bepul pilotlar → Q2 da naqd tugaydi                │
│           Base 30%: o'sish xarajatdan sekin → Q3 da teshik             │
│           Bull 10%: bitta tarmoq shartnomasi = CAC $200→$20            │
│                                                                        │
│  QIZIL    ❌ "AI tashxis qo'yadi"  ❌ "yagona platforma"               │
│  CHIZIQ   ❌ "bozor $50 mlrd"      ❌ "99% aniqlik"                    │
│           ✅ "biz tashxis qo'ymaymiz, vrach tasdiqlaydi"               │
└──────────────────────────────────────────────────────────────────────┘
```

---

# 14. MANBALAR

**Bozor va prognoz**
1. Precedence Research / Grand View / MarketsandMarkets / Fortune Business Insights — AI in healthcare market 2025–2034 (konsensus $37–56 mlrd 2026, CAGR 37–44%)
2. Rock Health / CB Insights — raqamli sog'liq fondi 2025: $14.2 mlrd (AQSh), $22.3 mlrd (global), AI ulushi 54%
3. Doximity 2026 — AQSh vrachlarining 63% i AI ishlatadi
4. JAMA Internal Medicine (2023) — hujjatga 34–55% ish vaqti
5. getlimeai / orbdoc / forasoft — ambient documentation bozori $1.85 mlrd (2024) → $17.75 mlrd (2033); narxlar $99–600/vrach/oy
6. MIT — genAI pilotlarining 95% muvaffaqiyatsiz

**O'lim holatlari (qabriston)**
7. Fierce Healthcare (31.10.2023) — Olive AI yopilishi, Waystar/Humata aktivlari
8. revcycleai.com / unicornburn.com / healthcareaiinvestor.com — Olive autopsiyasi (unit economics, "AI OS" va'dasi)
9. healthcareaiinvestor.com — 9 kompaniya, $35 mlrd yo'q qilingan qiymat (Teladoc/Livongo, Olive, Babylon, Forward, VillageMD, Proteus, Castlight, NeueHealth, Corindus)
10. buildmvpfast.com — Forward Health: 3 200 va'da → 5 kiosk; Olive $902M
11. CB Insights — 431/483 post-mortem: kapital 70%, PMF 43%, vaqt 29%, unit economics 19%, ehtiyoj yo'q 42%, jamoa 23%
12. HFMA (31.03.2025) — Olive va RCM bozori tahlili
13. Axios (31.10.2023) — Olive yopilishi

**O'zbekiston bozori**
14. anhor.uz / Statistika qo'mitasi (24.10.2026) — 8 912 ambulator muassasa, hududlar kesimi
15. Prezident taqdimoti / spot.uz / sputniknews.uz (01.05.2026) — xususiy klinikalar 3 200 → 8 700; ixtisoslashuv 39 → 116; koykalar 16k → 57k; akkreditatsiya 2027/2028/2030; SHIF 2028
16. asdr.gov.uz (10.06.2026) — DMED: 38 mln e-karta, 8 000+ klinika, 6 000 dorixona, 3 600+ muassasa, 200 000 xodim
17. gazeta.uz (15.10.2025) — DMED tarixi, 75 000 kompyuter tanqisligi, 100 GB sizib chiqish, "yadro" 2026 oxiri
18. VMQ 570 / uzdaily.uz / nova24.uz / tashkenttimes.uz (12.12.2025) — e-retsept piloti, 12 817 dori, 2027 majburiy
19. gazeta.uz (13.12.2025) — e-retsept qamrovi: xususiy klinikalar 49% (Toshkent 41%), 1 319 dorixona
20. zamin.uz (10.09.2026) — tibbiyot xodimlarini davlat ro'yxatiga olish 2027/2030
21. yuz.uz / zamon.uz (07.11.2026) — Prezident tabrigi, DMED, xususiy klinika o'sishi
22. vaqt.uz (01.09.2026) — UzVC: 5 mlrd so'mgacha, 0%, 3 yil, ulush ≤49%

**Regulyatsiya / ma'lumotlar**
23. **Law No. 1125 (26.03.2026)** — ZRU-547 ga o'zgartirish: lokalizatsiya faqat biometrik, genetik, telekom ma'lumotlariga
24. bondstonelaw.com / settleadvisory.com — lokalizatsiya islohoti tahlili
25. vlolawfirm.com / regulations.ai — ZRU-547: tibbiy ma'lumot = alohida toifa, aniq rozilik, 24 soat breach notification, Uzkomnazorat bloklash
26. WHO Europe (26.11.2024) — dori qoplamasi/reimbursement tizimi, SHIF

**Raqobat**
27. startupbase.uz — 1Clinic, Doctor Yan, Med24 ekotizimi
28. med24.uz — klinika/shifokor agregatori
29. `hackathon_razvedka_2026.md` (ushbu papkadagi oldingi hujjat) — hackathon g'oliblari bazasi
30. AI500 Hackathon (gazeta.uz, 16.12.2025) — Medvoice AI, Apollo, Oqim
