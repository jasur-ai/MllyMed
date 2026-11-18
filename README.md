# MllyMed — Milliy dori vositalariga ishonch ekotizimi

**Track №17:** *Milliy dori vositalariga ishonch*  
**Mahsulot nomi:** **MllyMed**  
**Jonli demo (Production):** [https://mllymed.onrender.com/](https://mllymed.onrender.com/)  
**Mobil va Web versiya:** Moslashuvchan (Responsive Web App)

Loyihaning to'liq kod strukturasi professional darajada **Frontend**, **Backend**, **Agent** va **Data** qismlariga ajratildi. Har bir qatlamda **B2C (Bemorlar va aholi)** va **B2B (Biznes, Shifokor, Dorixona, Zavod)** yo'nalishlari aniq modullarga bo'lingan.

---

## 🏗️ Loyihaning Yangi Arxitekturasi

```
National_Hack/
│
├── frontend/                     # ★ FRONTEND ARXITEKTURASI
│   ├── index.html                # Asosiy portal (MagicHeal nav bar, B2C/B2B kommutator)
│   ├── b2c/                      # Bemorlar (B2C) moduli
│   │   ├── b2c.css               # B2C katalog, filtr va kartochkalar uslubi
│   │   ├── catalog.js            # Dori qidirish, filtrlar, SVG qadoqlar, 80% mahalliy paritet
│   │   └── patient.js            # Bemor shaxsiy kabineti (qabullar, retseptlar)
│   ├── b2b/                      # Biznes va Shifokorlar (B2B) moduli
│   │   ├── b2b.css               # B2B panellar, formalar va jadvallar
│   │   ├── doctor.js             # Shifokor e-retsept moduli (XPN tayinlash, raqamli imzo)
│   │   ├── pharmacist.js         # Dorixona dispense navbati va berish logikasi
│   │   └── factory.js            # Zavod & Regulyator (GMP, mahalliy bozor ulushi, audit)
│   ├── agent/                    # MllyMed AI Agent interfeysi
│   │   ├── agent_widget.css      # Floating FAB va popup chat uslublari
│   │   └── agent_widget.js       # AI triaj, qizil bayroqlar (103) va muloqot
│   └── shared/                   # Umumiy komponentlar va yordamchilar
│       ├── css/
│       │   ├── base.css          # Dizayn tokenlari, ranglar, nishonlar (badges)
│       │   ├── navbar.css        # MagicHeal uslubidagi suzuvchi nav bar
│       │   └── modal.css         # Umumiy dialog va modallar
│       ├── js/
│       │   ├── api.js            # API klient, xatoliklar va rol boshqaruvi (X-Role)
│       │   └── app.js            # Asosiy ilova bootstrap va rejimlar almashinuvi
│       └── assets/
│           └── logo.svg          # MllyMed rasmiy SVG logotipi
│
├── backend/                      # ★ BACKEND ARXITEKTURASI
│   ├── server.py                 # Asosiy HTTP server (B2C va B2B API + frontend statika)
│   ├── config.py                 # Konfiguratsiya va dinamik yo'llar
│   ├── api/                      # REST API marshrutlari
│   │   ├── router.py             # Yagona so'rovlar marshrutizatori
│   │   ├── b2c_routes.py         # B2C API (/api/b2c/catalog, /api/b2c/card, /api/b2c/chat, /api/b2c/state)
│   │   └── b2b_routes.py         # B2B API (/api/b2b/prescriptions, /api/b2b/dispense, /api/b2b/analytics)
│   └── services/                 # Domen servislari
│       ├── apteka_service.py     # Dorixona takliflari, 308 mahsulot, narxlar
│       ├── dmed_service.py       # Shifokorlar, qabullar va retseptlar
│       ├── analytics_service.py  # 80% mahalliy paritet, bozor qamrovi, audit
│       └── bridge_service.py     # Yagona integratsiya ko'prigi (Bridge)
│
├── agent/                        # ★ MLLYMED AI AGENTI
│   ├── agent.py                  # MllyMed AI triaj va klinik xavfsiz skrining
│   ├── eval.py                   # 10 ta mezon bo'yicha mustaqil evaluatsiya (Halol Eval)
│   └── core/                     # Xavfsizlik, dalillar va triaj qoidalari
│       ├── safety.py             # Qizil bayroqlar (Favqulodda 103)
│       ├── triage.py             # Simptomlar va mutaxassis tanlash
│       ├── evidence.py           # Lex.uz faktlari va reestr dalillari
│       └── text.py               # Fuzzy normalizatsiya va o'zbekcha leksika
│
├── data/                         # ★ MA'LUMOTLAR BAZASI
│   ├── reyestr_dori.json         # 46 079 ta dori vositasi
│   ├── referent_narx.json        # 12 612 ta chegaraviy narx
│   └── apteka_catalog.json       # 308 ta dorixona taklifi
│
├── run.py                        # Yagona boshqaruvchi (Web, CLI, Test, Check)
└── run.sh                        # Bash ishga tushiruvchi
```

---

## 🚀 Ishga Tushirish

### 1. Web ilovani ishga tushirish (Frontend + Backend)
```bash
./run.sh
# yoki
python3 run.py
```
Brauzerda ochiladi: **`http://127.0.0.1:8200`**

### 2. Tizim yaxlitligi va testlarni tekshirish
```bash
python3 run.py --test
```
* **17/17** Invariant domen testlari
* **12/12** Virtual tajriba stsenariylari
* **10/10** MllyMed AI Agent Halol Eval (100% muvaffaqiyatli)

### 3. Terminalda jonli MllyMed AI agenti bilan suhbat
```bash
python3 run.py --cli
```
 ### 4. Qo'llab quvvatlovchi yordamchi saytlar (asl saytlar bilan boglanish imkoniyati bolmaganligi sababli)

 https://orindor.pages.dev/dmed#
 https://orindor.pages.dev/#/asosiy
