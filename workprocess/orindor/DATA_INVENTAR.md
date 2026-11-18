# O'RINDOR · DATA INVENTARI
## O'zbekiston birinchi. Har bir fakt — manbasi bilan.

**Sana:** 17-noyabr 2026 · **Muammo:** №17 · **Qoida:** faqat real ma'lumot, demo data yo'q

---

# 0. BIR QARASHDA

| Ko'rsatkich | Qiymat |
|---|---|
| Indekslangan UZ qonun hujjati | **53** |
| Yuklangan to'liq matn | **17 hujjat** |
| Hajm | **1.4 MB** sof matn |
| Tasdiqlangan fakt (so'zma-so'z iqtibos bilan) | **17** |
| Manba | `lex.uz` — O'zR Adliya vazirligi rasmiy bazasi |
| Chet el ma'lumoti | 300 yozuv — **faqat nom normalizatsiyasi testida** |

**Bu turni eng muhim natijasi:** №17 uchun kerakli bo'lgan uchta huquqiy asos — **ekvivalentlik (A2), haqiqiylik (A1), narx (A3)** — uchtasi ham **UZ qonunidan so'zma-so'z** tasdiqlandi. Ilgari bular taxmin edi.

---

# 1. QANDAY YIG'ILDI

## 1.1 lex.uz qidiruv API'si (topildi)

lex.uz sayti JS bilan chiziladi, oddiy qidiruv ishlamaydi. API topildi va ochildi:

```
POST https://lex.uz/api/search/bybody
{"text": "<so'rov>", "lang": 4, "page_size": 20, "page_number": 1, "search_type": 1}
→ {"code":1,"data":{"totalRows":N,"items":[{lact_id,title,lact_number,acceptance_date}]}}
Hujjat: https://lex.uz/uz/docs/{lact_id}
```

Kalit so'ralmaydi, autentifikatsiya yo'q. Bu — **rasmiy davlat bazasi**, ya'ni T0 manbasi.

## 1.2 Nima qidirildi (8 mavzu)

| Mavzu | Topildi | Nega kerak |
|---|---|---|
| referent narx | 29 | A3 narx qatlami |
| farmatsevtika mahsulotlari xafšsizligi | 60 | nazorat organi |
| bioekvivalentlik | 7 | **A2 dalil qatlami** |
| dori vositalarini import qilish | 7 | import/mahalliy nisbati |
| dori vositalari narxini tartibga solish | 6 | narx regulyatsiyasi |
| dori vositalarini markalash | 2 | **A1 haqiqiylik** |
| hayotiy muhim dori vositalari | 1 | assortiment |
| dori vositalari davlat ro'yxati | 0 | *(qidiruv so'zi noto'g'ri — tuzatish kerak)* |

## 1.3 Yuklangan hujjatlar (17 ta)

| # | Hujjat | Sana | Nima | Belgi |
|---|---|---|---|---|
| 1 | **738** | 24.11.2025 | Dori vositalarini davlat ro'yxatidan o'tkazish | 171 902 |
| 2 | **3735** | 25.12.2025 | **Referent narx tizimi** | 28 687 |
| 3 | **3242-1** | 12.05.2025 | Referent narx — o'zgartirish | 17 278 |
| 4 | **3750** | 09.01.2026 | **Jenerik BE (farmakokinetik)** | 18 265 |
| 5 | **149** | 02.04.2022 | **Majburiy raqamli markirovka (ASL BELGISI)** | 81 913 |
| 6 | **322** | 20.05.2021 | Markirovkalanadigan mahsulotlar ro'yxati | 252 909 |
| 7 | **3386** | 12.09.2022 | **Sertifikatlashtirish qoidalari** | 82 667 |
| 8 | **3386-1** | 14.07.2025 | Sertifikat qoidalariga o'zgartirish | 34 356 |
| 9 | **3600** | 17.01.2025 | Klinik tadqiqotsiz ro'yxatdan o'tkazish | 12 354 |
| 10 | **PF-35** | 05.03.2026 | **Mahalliy ishlab chiqarishni rag'batlantirish** | 49 953 |
| 11 | **O'RQ-399** | 04.01.2016 | Dori vositalari to'g'risida QONUN | 66 013 |
| 12 | **415-I** | 25.04.1997 | Dori vositalari va farmatsevtika faoliyati | 23 605 |
| 13 | **3848** | 04.06.2026 | Ro'yxat hujjatlariga talablar | 20 650 |
| 14 | **3806** | 03.04.2026 | Ro'yxat jarayoni samaradorligi | 14 064 |
| 15 | **PQ-408** | 29.11.2024 | Tibbiyot muassasalarini ta'minlash | 29 329 |
| 16 | **662** | 21.10.2025 | O'zgartirishlar | 131 332 |
| 17 | **3735** indeks + 53 hujjat metama'lumoti | — | `lex_index.json` | 30 006 |

Fayllar: `egiz/data/uz/*.txt` — har birining boshida hujjat nomi, raqami, sanasi, havolasi.

---

# 2. TASDIQLANGAN FAKTLAR — 17 ta

Har biri `egiz/data/facts.json` da: fakt, **so'zma-so'z iqtibos**, hujjat raqami, sana, URL.

## 2.1 A2 — EKVIVALENTLIK (dalil qatlamining asosi)

> **F01.** "2029-yil 1-yanvardan boshlab jenerik dori vositalarning bioekvivalentligini xalqaro **ICH** talablariga muvofiq o'rganish **majburiy** hisoblanadi."
> — 738-son, 24.11.2025 · `lex.uz/docs/-7853907`
>
> ✅ **Bu bizning "2 yillik oyna" argumentimizning huquqiy tasdig'i.** Ilgari taxmin edi.

> **F02.** "I va III biofarmatsevtik klassifikatsiyalash tizimiga mansub dori moddasi saqlovchi dori vositalari uchun **bioveyver** usulida amalga oshirilgan bioekvivalentlikni tasdiqlovchi hisobotlar taqdim etilishi mumkin."
> — 738-son

> **F03.** "...referent preparatga nisbatan bioekvivalentligi **validatsiyalangan in vivo yoki in vitro** tadqiqot usullaridan foydalangan holda isbotlangan, natijalari **miqdoriy ko'rsatkichlar** shaklida taqdim etilgan peroral jenerik dori vositalari."
> — 738-son

> **F04.** "jenerik dori vositasi — original (patentlangan) dori vositasining faol moddasi bilan **sifat va miqdoriy jihatdan bir xil** tarkibga, dori shakliga ega bo'lgan..."
> — 738-son

**Xulosa:** E0–E3 dalil darajalari **o'ylab topilgan emas** — ular 738-soning talablaridan kelib chiqadi. E1 = bioveyver (F02), E2 = in vivo BE (F03), E3 = ICH-mos (F01).

## 2.2 A3 — NARX (eng katta topilma)

> **F05.** "referent narx shakllantirish tizimi — dori shakli, qadoqdagi soni, dozasi, konsentratsiyasi, hajmi va qadoqlanishini hisobga olgan holda **xuddi shunday faol moddaga ega** dori vositalarini ishlab chiqaru[vchilar]..."
> — 3735-son, 25.12.2025 · `lex.uz/docs/-7952162`

> **F06.** "referent mamlakatlar — **Jahon bankining** aholi jon boshiga nisbatan yalpi ichki mahsulotning hisoblangan daromadlar darajasidan yuqori, o'rtachadan yuqoriroq va o'rtachadan pastroq bo'lgan davlatlar guruhiga kiruvchi..."
> — 3735-son

> **F07 — IMPORT:** `ChUN = (Rn + B + Bx + QQS) × UU`
> Bx = referent narxning **2%**, QQS = **12%**, UU (ulgurji) = **15%**
>
> **F08 — MAHALLIY:** `ChUN = (Rn + QQS) × UU`
> **Bojxona to'lovi YO'Q.**
>
> **F09 — 80% QOIDASI:** "Jenerik dori vositalarining referent narxlari original dori vositalari referent narxlarining **80 foizidan qimmat bo'lishi mumkin emas**."
> — 3735-son

> **F10.** "Bir ishlab chiqaruvchi tomonidan turli savdo nomlari ostida tarkibi bir xil bo'lgan dori vositalarining barchasiga nisbatan **eng past** referent narx qo'llanadi."
>
> **F11.** Axborot tizimi hisoblangan qiymatlardan **eng kam qiymatni** oladi.

### Nega bu hal qiluvchi

**Ilgari:** biz "import 21 000, mahalliy 6 500, 69% arzon" deb **taxminiy demo raqam** yozgandik.

**Endi:** narx farqi — **qonun bilan hisoblanadi**. Va asosiy sabab bojxona emas:

```
Misol: original referent narx = 126 000 so'm (10 USD × 12 600)

Import  : (126 000 + 0 + 2 520) × 1.12 × 1.15 × 1.20 = 198 640 so'm
Mahalliy: jenerik ≤ 80% → 100 800 so'm
          (100 800 + 0) × 1.12 × 1.15 × 1.20        = 155 796 so'm
                                                    ─────────────
Farq: 21.6%  ·  sabab: F09 (80% qoidasi) + bojxona
```

**Ya'ni №17 ning "tanlashga rag'batlantirish" talabi — davlat tomonidan allaqachon narx mexanizmi bilan qo'yilgan.** Faqat buni **ko'rsatadigan** narsa yo'q. Bu — mahsulotning butun mantiqiy asosi, endi hujjat bilan.

## 2.3 A1 — HAQQIYLIK

> **F12.** "«Asl belgisi» mahsulotlarni markirovkalash va kuzatib borish milliy axborot tizimi" — VM **737-son (20.11.2020)**; dori vositalarida majburiy raqamli markirovka — **149-son (02.04.2022)**
>
> **F13.** "**Operator** tomonidan ... markirovka kodlari [beriladi]" — ya'ni kodni ishlab chiqaruvchi o'zi yarata olmaydi
>
> **F14.** "to'rtinchi guruh — ... dori vositalari — **2027-yil 1-iyuldan** boshlab [majburiy]"

**Bu tahlil tanqidini tasdiqlaydi:** A1 davlat tizimida **qisman hal qilingan**. Biz "aniqlaymiz" emas, **"davlat natijasini A2/A3 bilan bir kartada birlashtiramiz"** deyishimiz kerak. Bu — kuchliroq pozitsiya, chunki regulyator hikoyasi "ustiga quriladi" bo'lib qoladi.

## 2.4 SOHANI TUSHUNISH

> **F15.** "original dori vositalarining patent muddati tugagandan so'ng **1 yil ichida** ... ishlab chiqarishni yo'lga qo'ygan ishlab chiqaruvchilarga texnologiyalar transferi xarajatlarining **50 foizi, biroq 50 ming AQSH dollaridan** [oshmagan miqdorda]..."
> — PF-35, 05.03.2026

> **F16.** "mahsulot va xizmatlar eksportini **300 million AQSH dollariga** yetkazish" — davlat maqsadi
> — PF-35

> **F17.** Farmatsevtika mahsulotlarini **sertifikatlash qoidalari** — 3386-son (12.09.2022), 2025-da o'zgartirilgan (3386-1, 14.07.2025)

**Nega muhim:** PF-35 — 2026-yil mart. Ya'ni davlat **hozir** mahalliy ishlab chiqarishni pul bilan rag'batlantiryapti. Bu "why now" argumentini taxmin bo'lmagan holga keltiradi.

---

# 3. NIMA YO'Q — VA UNI QANDAY OLISH KERAK

| # | Kerak | Kimda bor | Holat | Yo'l |
|---|---|---|---|---|
| 1 | **Dori ro'yxati** (savdo nomi, INN, doza) | `uzpharm-control.uz/registry/drugs` | 🟡 SPA, API nginx orqasida yopiq | Yozma so'rov → Farmatsevtika agentligi |
| 2 | **Sertifikat raqamlari** | `uzpharm-control.uz/registry/drug-certificates` | 🟡 SPA | Xuddi shu so'rov |
| 3 | **Referent va cheklangan narxlar reyestri** | Farmatsevtika agentligi axborot tizimi (F05–F11) | ⛔ tizim yopiq | So'rov — **eng qimmatli ma'lumot** |
| 4 | **GTIN / seriya / 44 belgili kod** | CRPT Turon (Operator) | ⛔ sayt ulanmadi | Operator bilan uchrashuv |
| 5 | **Dorixona real narxlari** | `apteka.uz` | 🟡 API yo'llari topildi, baza host yopiq | Hamkorlik so'rovi |
| 6 | **BE tadqiqot hisobotlari** | Ro'yxatdan o'tkazish dosyesi | ⛔ maxfiy | Faqat "bor/yo'q" faktini bilish yetarli |
| 7 | **Bojxona stavkalari** (dori uchun) | Bojxona qo'mitasi | ❔ tekshirilmagan | `customs.uz` / lex.uz tarif |

**Muhim:** 1–4 bo'lmasa, mahsulotning A1 va A3 qatlamlari **to'liq ishlamaydi**. Demak W0 ning birinchi ishi — texnika emas, **4 ta rasmiy so'rov**. Bu halol va aytish oson.

---

# 4. NIMA ISHLATILMAYDI

| Ma'lumot | Hajm | Qaror |
|---|---|---|
| openFDA (AQSh) — 300 yozuv | 1 file | ❌ **UZ kartasida ishlatilmaydi.** Faqat nom normalizatsiyasi testida |
| Sintetik demo mahsulotlar (12 ta) | `juft17_core.py` | ❌ olib tashlanadi — real reyestr sxemasi bilan almashtiriladi |

**Sabab:** O'zbekiston dorixonasida "acetaminophen" yo'q — "paratsetamol" bor. AQSh ma'lumoti mahsulotga **hech qanday qiymat qo'shmaydi**, lekin hakam oldida "bu qayerdan?" degan savolni tug'diradi.

---

# 5. KEYINGI QADAM

| # | Ish | Vaqt | Natija |
|---|---|---|---|
| 1 | **4 ta so'rov xati** (Agentlik, CRPT Turon, apteka.uz, Bojxona) | 45 daq | Rasmiy javob olish yo'li |
| 2 | Qolgan 36 hujjatni indekslash (hozir 17/53) | 30 daq | To'liq qonunchilik bazasi |
| 3 | `hayotiy muhim dori vositalari` qidiruvini tuzatish | 10 daq | Majburiy assortiment ro'yxati |
| 4 | Faktlarni mashina o'qiydigan qoidalarга aylantirish | 60 daq | A2/A3 dvigateli real qonunga tayanadi |
| 5 | Har kartada manba yorlig'i: `738-§`, `3735-§` | 30 daq | "Bu raqam qayerdan?" — javob kartaning o'zida |

---

# 6. BIR SAHIFA

```
┌────────────────────────────────────────────────────────────────────────┐
│  DATA — HOLAT                            O'RINDOR · №17                    │
├────────────────────────────────────────────────────────────────────────┤
│  OLINDI                                                                 │
│    lex.uz API ochildi (rasmiy, kalitsiz)                                │
│    53 hujjat indekslandi · 17 tasi to'liq matn · 1.4 MB                 │
│    17 fakt so'zma-so'z iqtibos bilan                                    │
│                                                                         │
│  TASDIQLANDI (ilgari taxmin edi)                                        │
│    ICH 2029 majburiy          → 738-§ (F01)                             │
│    Bioveyver BCS I/III        → 738-§ (F02)                             │
│    Import narx formulasi      → 3735 (F07)                              │
│    Mahalliy narx formulasi    → 3735 (F08)  ← bojxona yo'q              │
│    Jenerik ≤ 80% original     → 3735 (F09)  ← ENG MUHIM FAKT            │
│    ASL BELGISI operator beradi→ 149 (F13)                              │
│    Mahalliy ishlab chiqarishga 50% kompensatsiya → PF-35 (F15)          │
│                                                                         │
│  HALOL CHEGARA                                                          │
│    Reyestr · sertifikat · referent narx reyestri · QR kodlar → YOPIQ    │
│    → 4 ta rasmiy so'rov kerak. Texnika emas, ALOQA.                     │
│                                                                         │
│  ISHLATILMAYDI                                                          │
│    AQSh (openFDA) 300 yozuv → faqat nom testi                           │
│    Sintetik demo 12 mahsulot → olib tashlanadi                          │
└────────────────────────────────────────────────────────────────────────┘
```

---

*Har bir iqtibos `egiz/data/uz/` dagi to'liq matndan olingan. Tekshirish: `egiz/data/facts.json` → `file` maydoni → o'sha fayl → qidiruv.*
