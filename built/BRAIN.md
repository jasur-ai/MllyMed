# BRAIN v2 — keyingi AI uchun holat xaritasi

**Sana:** 2026-11-18 · **Papka:** `built/` · **Trek:** №17

Bu fayl — "miya": nima qurildi, nima **rad etildi**, nima **tasdiqlandi**,
qanday tekshiriladi, keyingi qadam nima. Kod o'zgarsa shu fayl yangilanadi.
Dalillar: `checkpoints/CP0…CP10`, mashina jurnali: `decisions.jsonl`.
Mahsulot talablari xaritasi: **7-bo'lim** (nima bor, nima yo'q, keyingi qadam).

---

## 1. Bir jumlada

`built/` — 46 079 dorili davlat reyestri, 308 mahsulotli real dorixona
katalogi (shu jumladan **Arzon apteka** bloki) va sintetik mini DMED ni bitta
rol-asosli veb-mahsulotga bog'laydigan tizim: bemor → agent → navbat →
shifokor → retsept → dorixona → berish. 17 test, 12 stsenariy va 5 veb-bo'lim
bilan tekshirilgan.

---

## 2. Qat'iy invariantlar — buzilsa mahsulot yaroqsiz

| # | Invariant | Qayerda majburlangan | Tekshiruv |
|---|---|---|---|
| I1 | Favqulodda qoida hamma narsadan oldin | `core/safety.py` | sim `rf-*`, eval suite 1 |
| I2 | Triajda tashxis/dori/doza yo'q | `validate_triage` | eval 7, sim har qadam |
| I3 | Navbatni agent tasdiqlamaydi | `dmed.confirm_appointment` | `test_agent_cannot_confirm` |
| I4 | Navbatni faqat bemor ochadi | `dmed.create_appointment(role)` | `test_only_patient_books` |
| I5 | Retsept faqat ro'yxatdagi XPN | `dmed.create_prescription` | `test_prescription_requires_registered_inn` |
| I6 | Retseptni faqat shifokor imzolaydi | `sign_prescription(role)` | `test_only_doctor_signs` |
| I7 | Dorini faqat farmatsevt beradi, imzolangan retsept bilan | `dispense(role, status)` | `test_dispense_requires_signed_and_role` |
| I8 | Berishda XPN mosligi shart | `dispense` `canon_inn` | `test_dispense_wrong_inn_rejected` |
| I9 | ArzonApteka vitrinasi XPN siz — almashtirishga kirmaydi | `build.py` `has_inn=false` | `test_arzon_entries...` |
| I10 | Noma'lum kelib chiqishi `null`, taxmin yo'q | `build.py` `local=None` | test + analitika |
| I11 | Har raqam manbali; yo'q bo'lsa «ma'lum emas» | `render.py`, `sources.py` | eval 8/10 |
| I12 | Vendor core qo'lda tahrirlanmaydi | `build.py` + SHA256 | `build.py --check` |

---

## 3. Xarita

| Fayl | Vazifa | Eslatma |
|---|---|---|
| `pipeline/harvest_apteka.py` | 16 kategoriya → `data/raw_apteka.json` | faqat ochiq sahifalar; `/api/` taqiqlangan |
| `build.py` | vendor core, katalog, manifest | yadro kodini bu yerda tahrirlamang |
| `src/apteka.py` | katalog, `canon_inn` (exact/fuzzy/contains), 80% proxy, `arzon()` | usul/ishonch javobda ko'rinadi |
| `src/analytics.py` | qamrov, paritet, ma'lumot sifati, `checks()` | barcha raqamlar hisoblangan |
| `src/dmed.py` | SQLite: navbat, retsept, berish, audit | rollar va statuslar kodda |
| `src/bridge.py` | agent + katalog + DMED + analitika | agent matni o'zgarmaydi |
| `src/web/server.py` | rol-asosli REST | `X-Role` / `X-User` |
| `src/web/static/index.html` | 5 bo'lim: Dorilar · Arzon apteka · Maslahat · Kabinet · Xodimlar | `SIMULYATSIYA` belgisi |
| `sim/` · `tests/` | 12 stsenariy · 17 invariant | o'chirish taqiqlanadi |

---

## 4. Tekshirilgan buyruqlar (2026-11-18)

```bash
cd orindor && PYTHONIOENCODING=utf-8 python eval_agent.py   # 10/10 · 0 xato · exit 0
cd built && python pipeline/harvest_apteka.py               # 288 mahsulot
cd built && python build.py                                  # CHECK OK · 308 mahsulot
cd built && python -m unittest discover -s tests             # 17/17 OK
cd built && python sim/run.py                                # 12/12 · exit 0
cd built && python -m src.web.server --port 8200             # 4 portal
```

E2E (rol sarlavhalari bilan): `analytics 200`, `card 200`, `draft 200` →
`sign 200` → `dispense` bemor roli bilan **403**, farmatsevtdan **200
dispensed 56000**, `audit 3`, `queue` bemor roli bilan **403**.

Windows: `pkill` yo'q → `netstat -ano | grep :PORT` + `taskkill //F //PID`.
Har Python buyrug'ida `PYTHONIOENCODING=utf-8`.

---

## 5. Qarorlar (to'liq: `decisions.jsonl`)

### Tasdiqlangan
- **A1.** Yadro `build.py` bilan vendor (bitta manba, drift yo'q).
- **A2.** Bridge agent matnini o'zgartirmaydi — faqat JSON qo'shadi.
- **A3.** Katalog 288 ta real mahsulotga kengaytirildi (mini 48 emas).
- **A4.** Domen SQLite'ga o'tdi: rollar, statuslar, audit jadvali.
- **A5.** Dorini berish (`dispense`) — alohida qadam, farmatsevt roli.
- **A6.** XPN bog'lash exact → fuzzy(0.90) → contains(0.75), usul ko'rinadi.
- **A7.** ArzonApteka 20 yozuvi `has_inn=false`, `local=null`.
- **A8.** Analitika ham mahsulot qismi: paritet, qamrov, sifat.

### Rad etilgan
- **R1.** Yadro kodini qayta yozish · **R2.** haqiqiy DMED API ·
  **R3.** agent navbatni tasdiqlashi · **R4.** ArzonApteka `/api/` skrapingi ·
  **R5.** ArzonApteka yozuvlariga XPN taxmini · **R6.** erkin matnli retsept ·
  **R7.** "klinik validatsiya" deb atash.
- **R8.** Dorini "avtomatik berish" — retsept imzosisiz berish rad etildi.
- **R9.** `dispense` ni bemor rolida ochish — 403 bilan yopildi.
- **R10.** Narxni "dorixona narxi" deb ko'rsatish — bu «X so'mdan».
- **R11.** Paket/doza bo'yicha normallashtirishni hozir qilish — katalogda
  doza alohida maydon emas; keyingi qadam.

### Tasdiqlangan (CP10)
- **A9.** Arzon apteka tejamkorligi **guruh medianasiga** nisbatan; «kafolatlangan
  tejash» yoki «kassa narxi» deb nomlanmaydi.
- **A10.** Vitrina yozuvlari alohida jadvalda, XPN siz `badge` bilan — I9 UI da
  ko'rinadigan bo'ldi.
- **A11.** Milliy ustuvorlik — **tartib**, sifat da'vosi emas: `by_inn()` va
  `catalog()` mahalliy takliflarni boshiga qo'yadi; eng past narx alohida
  `badge` bilan belgilanadi (`local` ma'lumoti yo'q bo'lsa taxmin qilinmaydi).

### Ochiq
- **O1.** GMP reyestri (`uzpharm-gxp.uz`) DNS'da yo'q — yig'ilmagan.
- **O2.** Katalog 308 — hali ham to'liq bozor emas.
- **O3.** Klinik ko'rik yo'q.
- **O4.** Demo autentifikatsiyasi yo'q (`X-Role` faqat UI uchun).
- **O5.** 92 XPN bog'lanmadi — imlo/ekstrakt farqlari.
- **O6.** Haqiqiy qoldiq (stock) yo'q — taklif bor, soni yo'q.
- **O7.** Arzon apteka foizlari paket/doza bo'yicha normallashtirilmagan —
  ba'zi farqlar juda katta (−89%) chiqadi, izoh UI da bor.
- **O8.** Vitrina 20 yozuvdan 19 tasida narx bor (bittasi narxsiz).
- **O9.** «Milliy ustuvorlik» reytingi yo'q — `local` bayrog'i bor, tartib yo'q.
- **O10.** Shifokor tasdiqlagan muqobillar ro'yxati yo'q — uni to'qib bo'lmaydi.

---

## 6. Ma'lum cheklovlar

- DMED **sintetik**; "6 000 dorixona" kabi daqiqalar da'vo qilinmaydi.
- Narx — «X so'mdan»; 80% tekshiruvi **proxy** (referent narx reyestri yopiq).
- 95/156 XPN reyestrga bog'landi (60.1%); qolgani ochiq «topilmadi».
- Qoldiq soni yo'q — `pharmacies` faqat nechta dorixonada borligi.
- UI demo: autentifikatsiya, shifrlash, rate-limit yo'q.
- Arzon apteka foizlari turli paket/dozalarni bir guruhga qo'shadi — bu
  «tejash kafolati» emas, ko'rsatkich.

---

## 7. Mahsulot talablari xaritasi (2026-11-18 note)

Bu — foydalanuvchi bergan asosiy funksiyalar ro'yxati va kodning **hozirgi**
holati. «Bor» faqat kod bilan tekshirilgan bo'lsa yoziladi; reklama emas.

| # | Talab | Holat | Dalil / yetishmayotgani |
|---|---|---|---|
| 1 | **Milliy ustuvorlik** — qidiruvda avval mahalliy muqobillar | ✅ bor | `by_inn()` va `catalog()` mahalliyni boshiga qo'yadi (A11); kartada «milliy ustuvorlik» izohi; eng past narx alohida badge. Arzon ro'yxati esa narx bo'yicha qoladi |
| 2 | **Doktor turkumi** — har dori uchun shifokor tasdiqlagan o'rinbosarlar | ❌ yo'q | XPN guruhi bo'yicha muqobillar hisoblanadi, lekin «shifokor tasdiqladi» degan ma'lumot manbasi yo'q. Uni to'qish **taqiqlanadi** (I11). Kerak: shifokor ko'rigi jarayoni va imzoli ro'yxat |
| 3 | **Sifat isboti** — arzonlik sifatsizlik emas, MNN bir xilligi | ⚠️ qisman | Kartada XPN va guruh hajmi ko'rinadi; bioekvivalentlik (BE) hisoboti ochiq emas (O3) |
| 4 | **Ishonch belgisi** — davlat reyestri, GMP, shifokor tasdig'i | ⚠️ qisman | Reyestr ✅; GMP yig'ilmagan (O1, DNS yo'q); shifokor tasdig'i ❌ |
| 5 | **E-retsept o'rinbosari** — shifokor oldindan muqobilni tasdiqlasin | ❌ yo'q | Retsept bitta XPN; `dispense` faqat shu XPN ni qabul qiladi (I8). Maydon va imzo oqimi kerak |
| 6 | **ArzonApteka bloki** — alohida blok, kichik real ma'lumot | ✅ bor | CP10: `/api/arzon`, 54 guruh, 19 vitrina yozuvi, alohida bo'lim |
| 7 | **Tashxissiz AI agent** — faqat qaysi shifokorga borishni aytadi | ✅ bor | `core/triage.py` + `validate_triage`; eval 10/10, sim 12/12 |
| 8 | **Bron va kalendar** | ⚠️ qisman | Slot tanlash, bemor tasdiqlashi, SQLite — **sintetik**; real DMED va `.ics` eksport yo'q |
| 9 | **3 marta eslatma** («Mutolaa» uslubi) | ❌ yo'q | `built/` da eslatma sikli yo'q; eski agentda g'oya bor, taymer yo'q |
| 10 | **Offline-first + Firebase** | ❌ yo'q | API serverga tayanadi; service worker/sync yo'q; Firebase hali tanlanmagan |
| 11 | **100% real data** | ⚠️ qisman | Reyestr va dorixona katalogi real; DMED **sintetik** va shunday belgilangan; Reddit manbasi yo'q |

**Muhim ziddiyat:** 11-band («100% real») hozirgi sintetik DMED bilan birga
bo'lmaydi. Yoki DMED real manbaga almashtiriladi, yoki UI da sintetik belgisi
qoladi. Buni yashirish — I11 ni buzadi.

---

## 8. Keyingi qadamlar (tartib bilan)

1. **Arzon ro'yxatida ham milliy filtr:** hozir arzon ro'yxati tejamkorlik
   bo'yicha; «avval mahalliy» ko'rinishi uchun alohida tab kerak.
2. **GMP qatlami:** `registry2/6` HTML → `data/gmp.json`; kartada
   `GMP: Active / muddat` yoki «bog'lanmadi».
3. **Muqobil dorilar:** XPN guruhi asosida «muqobil» bloki, lekin faqat
   shifokor tasdiqlagan ro'yxat bilan; tasdiq bo'lmasa «tasdiqlanmagan» yoziladi.
4. **Bron + eslatma:** `.ics` eksport, 3 bosqichli eslatma (simulyatsiya
   belgisi bilan), keyin real DMED integratsiyasi.
5. **Offline-first:** PWA service worker + navbat/retsept draftlarini lokal
   saqlash; sinxronlash uchun Firebase yoki alternativani **tanlash kerak**.
6. **Qoldiq va auth:** POS `offer.stock`, JWT/session, rate-limit.
7. **Katalog:** 308 → 1 000+; har yangilashda `pipeline` + `build.py`.

---

## 9. Qanday davom ettirish

```bash
cd built
python build.py --check && python -m unittest discover -s tests
python sim/run.py
# o'zgartirish: src/ yoki orindor/ da
python build.py && python sim/run.py
# hujjat: checkpoints/CP10_*.md + decisions.jsonl qatori
```

Yangi stsenariy: `sim/scenarios.json` (`stage`, `reply_has`, `reply_not_has`,
`has_card`, `card_reg`, `apteka_min`, `dmed_doctors_min`, `no_appointments`).
Yangi endpoint: `src/web/server.py` + `src/bridge.py`; rol tekshiruvi serverda.
