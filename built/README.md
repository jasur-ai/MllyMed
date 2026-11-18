# built/ — O'RINDOR v2: agent + dorixona + mini DMED + analitika

**№17 · mahalliy dori vositalariga ishonch.** Katta mahsulot: bitta API va
to'rt portal — bemor, shifokor, dorixona, admin.

```
bemor savoli
   │
   ├── favqulodda ──────────────────────► 103 (navbat yo'q)
   ├── dori nomi/XPN ──► ishonch kartasi ──► 308 dorixona taklifi (80% proxy)
   └── shikoyat ──► skrining ──► mutaxassis ──► navbat (faqat bemor tasdiqlaydi)
                                                   │
                              shifokor XPN bo'yicha retsept yozadi
                                                   │
                              dorixona: imzolangan retsept → dori beriladi
```

## Tez start (built/ ichidan)

```bash
python3 pipeline/harvest_apteka.py        # 288 real mahsulot (ixtiyoriy, yangilash)
python3 build.py                          # vendor core + katalog + manifest
python3 -m unittest discover -s tests -v  # 17 invariant test
python3 sim/run.py                        # 12 stsenariy → data/sim_report.json
python3 -m src.web.server --port 8200     # 4 portalli demo
```

`build.py --check` — SHA256 manifest, yadro importi, sonlar.

## Nima real, nima sintetik

| Qism | Holat | Manba |
|---|---|---|
| 46 079 dori · 2 941 XPN · 12 422 referent narx | ✅ real | `api.mpa.uz` |
| **308 dorixona mahsuloti · 158 XPN · 70 sotuvchi** | ✅ real | apteka.uz (16 kategoriya) |
| 20 ArzonApteka vitrinasi (XPN siz) | ✅ real | arzonapteka.uz |
| Analitika (paritet, qamrov, sifat) | ✅ hisoblangan | katalog + reyestr |
| Klinikalar, shifokorlar, navbat vaqtlari | ⚠️ **sintetik** | `src/dmed.py` |
| Navbat/retsept/berish yozuvlari | ⚠️ lokal SQLite | `data/runtime/dmed.db` |

**Mini DMED — haqiqiy DMED emas.** Tashqi tizimga so'rov yo'q, bron yo'q.
UI'da `DMED: SIMULYATSIYA` belgisi turadi.

## Rollar va qoidalar (kodda)

| Rol | Nima qila oladi | Chegara |
|---|---|---|
| `patient` | navbat so'rovi, tasdiqlash, bekor qilish | agent tasdiqlamaydi |
| `doctor` | XPN bo'yicha retsept qoralamasi, imzo | faqat ro'yxatdagi XPN |
| `pharmacist` | imzolangan retseptni berish | faqat mos XPN taklifi |
| `admin` | analitika, audit | — |

Boshqa rol → `403`. Har amal `audit` jadvaliga yoziladi.

## API (asosiy)

```
GET  /api/health · /api/stats · /api/analytics
GET  /api/card?q=… · /api/catalog?q=&page=&size=&local=&category=
GET  /api/arzon?limit=&category=&local=   # Arzon apteka: eng past taklif + vitrina
GET  /api/inn/<inn> · /api/doctors · /api/appointments
GET  /api/prescriptions?sid= · /api/prescriptions/queue · /api/audit
POST /api/chat
POST /api/appointments · /confirm · /cancel
POST /api/prescriptions · /sign · /dispense
```

Sarlavhalar: `X-Role`, `X-User` (demo autentifikatsiyasi).

## Tuzilma

```
built/
├── build.py                 vendor core + katalog + manifest
├── pipeline/harvest_apteka.py  16 kategoriya → 288 mahsulot
├── src/
│   ├── apteka.py            katalog, XPN bog'lash, 80% proxy, `arzon()`
│   ├── analytics.py         paritet, qamrov, ma'lumot sifati
│   ├── dmed.py              SQLite: navbat, retsept, berish, audit
│   ├── bridge.py            agent + katalog + DMED + analitika
│   └── web/                 API + 4 portalli UI
├── sim/ · tests/            virtual tajriba · invariantlar
├── data/                    katalog, manifest, sim, runtime SQLite
├── vendor/orindor/          build.py yaratadi
├── BRAIN.md · CHECKPOINTS.md · checkpoints/ · decisions.jsonl
└── datas/                   eski tadqiqot fayllari
```

## Natijalar (2026-11-18, shu papkada o'lchangan)

```
yadro eval (orindor)      10/10 suite · JAMI XATO: 0
invariant testlar          17/17 OK
virtual tajriba            12/12 stsenariy
katalog                    308 mahsulot · 285 XPN · 158 guruh · 70 sotuvchi
reyestr bog'lanishi        95/156 XPN (60.1%) · exact 132 · fuzzy 55
narx pariteti              14 juftlik · 10 tasi 80% dan qimmat
ma'lumot sifati            narx yo'q 0.4% · XPN yo'q 7.5% · kelib chiqishi noma'lum 8.4%
arzon apteka               54 guruh · 284 narxli taklif · median farq −24.5% · vitrina 19
e2e oqim                   qoralama → imzo → berish · rol 403 bilan himoyalangan
```

## Veb-bo'limlar

| Bo'lim | Nima |
|---|---|
| Dorilar | Karta qidiruvi, dorixona takliflari, 80% proxy, katalog |
| Arzon apteka | Har XPN uchun eng past taklif, tejamkorlik, vitrina jadvali |
| Maslahat | Agent: karta yoki triaj; mutaxassis va bo'sh vaqtlar |
| Kabinet | Navbatlar, retseptlar, berilgan dorilar |
| Xodimlar | Shifokor / dorixona / admin panellari, rol 403 |

Batafsil: `BRAIN.md`, `CHECKPOINTS.md`, `sim/report.md`.
