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
├── INDEX.md                      ← shu fayl
│
├── orindor/                      ★ MAHSULOT — hozir ishlaydigan narsa
│   ├── agent.py                  suhbat → mutaxassis → navbat → eslatma (872 satr)
│   ├── eval_agent.py             10 ta o'lchov, raqam beradi
│   ├── AGENT.md                  agent hujjati: nega LLM wrapper emas, 3 chegara
│   ├── DATA_INVENTAR.md          53 hujjat indeksi, 17 tekshirilgan fakt
│   ├── data/
│   │   ├── facts.json            ★ 17 fakt (iqtibos + hujjat + sana + URL)
│   │   ├── uz/                   17 ta lex.uz to'liq matni, 1.4 MB
│   │   ├── lex_index.json        53 hujjat indeksi
│   │   ├── real_products.json    300 openFDA yozuvi — faqat normalizatsiya testi
│   │   └── source_status.json    qaysi manba ochiq/yopiq
│   └── tools/                    ma'lumot yig'uvchi skriptlar (normalize, harvest_lex…)
│
├── tadqiqot/                     ★ DALIL — qarorlar shu yerga tayanadi
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
python3 orindor/agent.py --demo        # karta + triaj + offline demo
python3 orindor/agent.py               # jonli suhbat
python3 orindor/agent.py --card nurofen
python3 orindor/eval_agent.py          # 10 ta o'lchov
python3 orindor/tools/sources.py       # 19 manbani jonli tekshirish
python3 orindor/web/server.py          # brauzer demo :8000
```

```
1) RED FLAG RECALL   32/32  100%     ← yangi iboralar, UZ/RU/kirill
2) FALSE ALARM      100/100 100%     ← 100 oddiy gap
3) MUTAXASSIS top-1  26/26  100%     top-3 26/26
4) XAVFSIZ DEFAULT    4/4   100%     ← javobsiz «1 hafta» chiqmaydi
5) YOSH AJRATISH      4/4   100%     ← «2 yil» yosh emas
6) KARTA (xom manba) 30/30  100%     ← haqiqiy reyestr bilan solishtirildi
7) XAVFSIZLIK        30/30  100%
9) DATA INTEGRITY      ✅
10) MANBA HALOLLIGI    1/1   100%     ← GMP holati fayldan, da'vo qo'lda emas
XATO JAMI: 0
```

Ma'lumot: **46 079 dori · 2 941 XPN · 12 423 referent narx · 538 chegara narx**
(`api.mpa.uz`, ochiq). Batafsil: `orindor/AGENT.md`.

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
- **GMP reyestri ochiq, lekin bu hostda DNS yo'q** — `uzpharm-gxp.uz/registry2`
  va `registry6` HTML jadvallari, E-IMZO talab qilmaydi. Karta shuning uchun
  «TEKSHIRILMADI» deydi («sertifikat yo'q» emas). Batafsil: `orindor/AGENT.md` 9-bo'lim.
- **`my.gov.uz` da ochiq API yo'q** (404/403 tekshirildi) — navbat deep-link bilan.
- **Yuridik matn yo'q** — "tibbiy maslahat emas" ogohlantirishi va javobgarlik chegarasi yozilmagan.

---

## 6. `built/` — yig'ilgan mahsulot (2026-11-18)

`built/` — agent + dorixona + mini DMED ni bitta oqimga bog'laydigan,
12 invariant test va 12 stsenariyli virtual tajriba bilan tekshirilgan demo.

```bash
cd built
python3 build.py                          # vendor core + katalog + manifest
python3 -m unittest discover -s tests     # 12/12
python3 sim/run.py                        # 12/12
python3 -m src.web.server --port 8200     # brauzer demo
```

| Hujjat | Nima uchun |
|---|---|
| `built/BRAIN.md` | keyingi AI uchun holat, invariantlar, qarorlar, talablar xaritasi, keyingi qadam |
| `built/CHECKPOINTS.md` | CP0–CP9 indeksi |
| `built/checkpoints/` | har checkpoint: maqsad, tasdiq/rad, dalil |
| `built/decisions.jsonl` | mashina o'qiydigan qarorlar jurnali |
| `built/sim/report.md` | virtual tajriba hisoboti (kod yaratadi) |

Natijalar (v2 + CP10): yadro eval **10/10 suite · 0 xato**; testlar **17/17**;
virtual tajriba **12/12**; katalog **308 mahsulot · 158 XPN guruhi · 70 sotuvchi**
(95 XPN reyestrga bog'langan, 60.1%); analitika 6/6 izchillik testi.
**Arzon apteka**: 54 narx guruhi · 284 taklif · vitrina 19 yozuv · median farq
−24.5% (`/api/arzon`). Veb — 5 bo'lim: Dorilar · Arzon apteka · Maslahat ·
Kabinet · Xodimlar. Mini DMED — **sintetik**, UI'da `SIMULYATSIYA`/`DEMO`
belgisi; dorini berish faqat farmatsevt rolida. Talablar xaritasi:
`built/BRAIN.md` 7-bo'lim.
