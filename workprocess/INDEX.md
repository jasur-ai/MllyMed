# O'RINDOR — workspace xaritasi

**№17 · milliy dori vositalariga ishonch.** Nom: **O'RINDOR** (egizak emas).
Oxirgi yangilanish: 2026-11-18

---

## 1. Nima o'chirildi (va nega)

| O'chirildi | Sabab |
|---|---|
| `battle_card.html` | **HISOB AI** treki uchun yozilgan — bizning trek emas (sarlavhasidan tasdiqlandi) |
| `prototype/` (8 fayl, 150 KB) | Rad etilgan g'oyalar kodi + **`demo_data.json`** — siz "demo data hech qayerda bo'lmasin" degansiz |
| `.arena/`, `__pycache__/` | Texnik keraksiz |

**Hech narsa yo'qolmadi:** rad etilgan g'oyalar (Doribon, DoriYo'l, JUFT) **arxiv/** da qoldi — kerak bo'lsa qayta ochiladi, lekin asosiy ishga xalaqit bermaydi.

---

## 2. Papkalar

```
/
├── INDEX.md                      ← shu fayl (xarita)
│
├── data/                         ★★ MA'LUMOT BO'LIMI — ishlatsa bo'ladigan ko'rinishda
│   ├── README.md                 sxema, maydonlar, ishlatish misollari, nima yo'q
│   ├── index.json                manifest: har fayl → manba, yozuv soni, hajm
│   ├── reyestr_dori.json         46 079 dori (25 MB) ← asosiy
│   ├── reyestr_dori.xlsx         40 000 qator, rasmiy Excel
│   ├── referent_narx.json        12 612 chegaraviy narx (+ .csv)
│   ├── tafsilot.json             538 yozuv: maxSalePrice (chegara narx) + tarkib
│   ├── mini_apteka_katalog.json  48 mahsulot, 12 kategoriya
│   ├── arzon_vitrina.json        20 mahsulot
│   ├── atx_guruhlari.json · dori_shakllari.json · hisob.json
│   └── faktlar.json              17 huquqiy fakt + 3735 narx modeli
│
├── orindor/                      ★ MAHSULOT — hozir ishlaydigan narsa
│   ├── agent.py                  suhbat → mutaxassis → navbat → eslatma (872 satr)
│   ├── eval_agent.py             6 ta o'lchov, raqam beradi
│   ├── AGENT.md                  agent hujjati: nega LLM wrapper emas, 3 chegara
│   ├── DATA_INVENTAR.md          53 hujjat indeksi, 17 tekshirilgan fakt
│   ├── data/
│   │   ├── facts.json            ★ 17 fakt (iqtibos + hujjat + sana + URL)
│   │   ├── uz/                   17 ta lex.uz to'liq matni, 1.4 MB
│   │   ├── lex_index.json        53 hujjat indeksi
│   │   ├── arzon_sample.json     20 ArzonApteka mahsuloti (nom, ishlab chiqaruvchi, narx, Rx)
│   │   ├── real_products.json    300 openFDA yozuvi — faqat normalizatsiya testi
│   │   └── source_status.json    qaysi manba ochiq/yopiq
│   └── tools/                    ma'lumot yig'uvchi skriptlar
│                                 ├ harvest_mpa.py        ★ davlat reyestri + referent narx (60 so'rov)
│                                 ├ harvest_mpa_extra.py  ★ tafsilot, Excel, ATX, dori shakllari
│                                 ├ arzon.py              ArzonApteka vitrinasi (20)
│                                 ├ harvest_pharmacies.py mini apteka katalogi (48)
│                                 └ build_data.py         ★ data/ bo'limini quradi (json+csv+xlsx)
│
├── mini_apteka/                  ★ KO'RGAZMA — O'RINDOR dorixona oqimida
│   ├── server.py                 stdlib API, port 8100 (qidiruv · XPN · tekshiruv)
│   ├── index.html                bir sahifa: qidiruv → variantlar → O'RINDOR kartasi
│   ├── README.md                 nima real, nima yopiq, integratsiya shartnomasi
│   └── data/catalog.json         48 mahsulot · 25 XPN · 8 juftlik · 34 KB
│
├── tadqiqot/                     ★ DALIL — qarorlar shu yerga tayanadi
│   ├── data_mpa_reyestr.md       ★★ TOPILDI: davlat reyestri + referent narxlar API
│   ├── arzon_apteka_tekshiruv.md  ArzonApteka: nima ochiq, nima yopiq
│   ├── sogliq_treki_due_diligence.md   bozor, raqobat, 12 ta o'lik yo'l
│   ├── hackathon_razvedka_2026.md      trek, mezon, hakam tarkibi
│   ├── pdf_tahlil_yangi_pozitsiya.md   №17 ning rasmiy matni tahlili
│   ├── baholash_15_mezon.md            T1–T5 / B1–B5 / S1–S5 bo'yicha o'z-o'zini tekshirish
│   ├── AI_Hackathon_300_Bosqich_Masterplan.md   to'liq reja (112 KB)
│   ├── 300_bosqich_tracker.xlsx        bajarilgan ish hisobi
│   └── moliyaviy_model.xlsx            birlik iqtisodi
│
├── arxiv/                        rad etilgan / eski versiyalar (o'chirilmagan)
│   ├── doribon_brief.md · doribon_tahlil.md
│   ├── doriyol_masterplan.md · muammo_yechim_tahlili.md
│   ├── juft17_ishonch.md · juft_almashtirish.md
│   ├── juft_demo.html · qaysi_muammo.html
│   └── eski_web_juff/            JUFT veb-ilovasi (server.py + index.html)
│
└── manba/                        siz yuklagan xom fayllar
    ├── toshkent_dolzarb_muammolar (1).pdf   ← №17 manbasi
    ├── full.txt
    └── image-1.png
```

---

## 3. Hozir nima ishlaydi (tekshirilgan, bugun)

```bash
python3 orindor/agent.py --demo     # 10 ta suhbat, to'liq sikl
python3 orindor/agent.py            # jonli suhbat
python3 orindor/eval_agent.py       # o'lchov
```

```
1) RED FLAG RECALL   15/15  100%     ← o'tkazib yuborilgan favqulodda: 0
2) FALSE ALARM       16/16  100%
3) MUTAXASSIS top-1  19/20   95%     top-3 20/20 100%
4) XAVFSIZLIK        20/20  100%     ← dori/tashxis nomi chiqmadi
XATO JAMI: 0
```

---

## 4. Ochiq qaror (hali hal qilinmagan)

Tanqid review'ning xulosasi: **hammasini kesib, bitta mahsulot qoldirish**. Mening javobim:
review 70% haq, lekin uning yadro g'oyasi — "shifokor oldindan imzolagan almashtirish ro'yxati" —
**kerak emas**, chunki qonun buni allaqachon hal qilgan:

> «Retseptda ko'rsatilgan dori vositalari dorixonalar tomonidan ularning **xalqaro
> patentlanmagan nomiga asosan** beriladi.» — lex.uz/mact/-3032611

2025-12-10 dan e-retsept **INN asosida** yoziladi (Toshkent + 15 tuman; 2026 oxirigacha
butun mamlakat). Ya'ni almashtirish uchun yangi imzo kerak emas — **ko'rinish** kerak.

**Taklif qilingan kesim (hali tasdiqlanmagan):**
- kesiladi: 24 mutaxassis xaritasi, bron oqimi, 3 xatli eslatma sikli;
- qoladi: 40 satrlik red-flag qo'riqchisi (javobgarlik uchun) + INN-karta yadrosi
  (`hujjat topildi` / `shifokor ko'rdi` / `ma'lum emas`) + eval.

Bu ikki savolga javob kutilmoqda: **(1)** hakamlar "agent" mezonini rasmiy baholaydimi,
**(2)** kesim hozir qilinadimi.

---

## 5. Ma'lum bo'lgan bo'shliqlar (yashirmaymiz)

- **Bioekvivalentlik (BE) hisobotlari ochiq emas** — mahsulot bo'yicha bitta ham dalilim yo'q.
  Real ma'lumotda ko'p kartalar "ma'lum emas" chiqadi. Bu kamchilik emas, mahsulotning xususiyati.
- **Birorta shifokor tekshirmagan** — 15 red-flag qoidasi adabiyotga asoslangan, klinik ko'rikdan o'tmagan.
- **`my.gov.uz` da ochiq API yo'q** (404/403 tekshirildi) — navbat deep-link bilan.
- **Yuridik matn yo'q** — "tibbiy maslahat emas" ogohlantirishi va javobgarlik chegarasi yozilmagan.
