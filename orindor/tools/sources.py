"""
O'RINDOR · MANBA REJASI — O'ZBEKISTON BIRINCHI, CHET EL FAQAT BO'SHLIQ UCHUN
=======================================================================
Qoida (buzilmaydi):
    T0  O'zbekiston rasmiy manbasi
    T1  O'zbekiston tijoriy/ochiq manbasi
    T2  Xalqaro standart (JSST INN, ATC, GS1) — nomlash uchun
    T3  Chet el ma'lumoti — FAQAT T2/T3 maydonlari uchun, va HECH QACHON
        O'zbekiston kartasida "UZ reyestri" deb ko'rsatilmaydi.

Bu fayl har bir manbani JONLI tekshiradi va holatini yozib qo'yadi.
Natija — "ma'lumot olish rejasi": nima ochiq, nima so'rov talab qiladi.

Muhim farq (2026-11-18 dan):
    CLOSED     — manba umuman yopiq (401/403/404, API yo'q).
    UNRESOLVED — manba OCHIQ, lekin domen bu muhitda DNS'da topilmaydi.
                 Bu "yopiq" degani EMAS: brauzerdan ochiladi, kod yozish
                 uchun tarmoq/DNS kerak. Kartada ham shu so'z bilan
                 ko'rsatiladi, aks holda foydalanuvchini chalg'itamiz.

Ishga tushirish:  python3 orindor/tools/sources.py
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from datetime import date

TODAY = date.today().isoformat()
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


@dataclass
class Source:
    tier: str
    name: str
    url: str
    what: str                # nima olinadi
    status: str = "?"        # OPEN / SHELL / CLOSED / BLOCKED / UNRESOLVED / REQUEST
    evidence: str = ""
    next_step: str = ""


SOURCES: list[Source] = [
    # ---------------- T0 · rasmiy ----------------
    Source("T0", "O'zR dori vositalari davlat reyestri",
           "https://uzpharm-control.uz/registry/drugs",
           "Ro'yxatdan o'tgan dorilar, sertifikat raqami, ishlab chiqaruvchi",
           next_step="Sayt SPA. API nginx orqasida yopiq → yozma so'rov "
                     "(Farmatsevtika agentligi). Lekin api.mpa.uz ochiq."),
    Source("T0", "Dori sertifikatlari reyestri",
           "https://uzpharm-control.uz/registry/drug-certificates",
           "Sertifikat raqami, amal qilish muddati — A2 dalil qatlamining asosi",
           next_step="Shu sahifa — №17 ning 'shaffof sertifikat' talabining manbasi"),
    Source("T0", "GMP sertifikatlari reyestri — mahalliy ishlab chiqaruvchilar",
           "https://uzpharm-gxp.uz/registry2",
           "GMP sertifikati: egasi, obyekt, soha, raqam, berilgan/amal muddati, "
           "holat (Active/Inactive), oxirgi inspeksiya",
           next_step="OCHIQ HTML JADVAL (sahifalash ?page=N). Bu muhitda domen "
                     "DNS'da yo'q → UNRESOLVED. Yig'ish skripti tayyor bo'lishi "
                     "kerak: HTML jadval → data/gmp.json."),
    Source("T0", "GMP sertifikatlari reyestri — xorijiy ishlab chiqaruvchilar",
           "https://uzpharm-gxp.uz/registry6",
           "Xorijiy zavodlar uchun GMP_UZ sertifikatlari (raqam, muddat, soha)",
           next_step="OCHIQ HTML JADVAL. UNRESOLVED (DNS). Import dori "
                     "ishlab chiqaruvchisini shu reyestr bilan bog'lash mumkin."),
    Source("T0", "GMP API (api.mpa.uz)",
           "https://api.mpa.uz/drug-catalog-api/v1/gmp-registry",
           "GMP ma'lumotini JSON ko'rinishida berishi mumkin edi",
           next_step="401 — E-IMZO talab qiladi. HTML reyestr (registry2/6) "
                     "bunga muqobil, lekin DNS muammosi bor."),
    Source("T0", "Yo'riqnoma (instruction) API",
           "https://api.mpa.uz/drug-catalog-api/v1/instruction/detail",
           "Dori yo'riqnomasi: ko'rsatmalar, qo'llash usuli",
           next_step="certificateNumber parametri talab qiladi; haqiqiy "
                     "reyestr raqami bilan ham 404. Ochiq emas — yozma so'rov."),
    Source("T0", "Ishlab chiqaruvchilar ro'yxati (STIR bilan)",
           "https://pharmagency.uz/en/service/manufacturers",
           "59 farmatsevtika ishlab chiqaruvchisi, STIR — kompaniya nomini "
           "normallashtirish uchun",
           next_step="Bu muhitda UNRESOLVED (DNS). Kerak bo'lsa qo'lda Excel."),
    Source("T0", "mpa.uz ochiq ma'lumotlar bo'limi",
           "https://mpa.uz/uz/open-data",
           "Ochiq datasetlar: katalog, sertifikatlarni tekshirish, tibbiy "
           "buyumlar, moliyaviy hisobot",
           next_step="SPA (JS). Marshrutlar JS bundle'da topildi: "
                     "open-data/catalog, open-data/certificates-verification, "
                     "open-data/medical-items. API yo'llarini aniqlash kerak."),
    Source("T0", "lex.uz — VMQ 738-son (24.11.2025)",
           "https://lex.uz/uz/docs/-7853907",
           "BE talabi, bioveyver, ICH 2029 — qoidalar matni",
           next_step="Ochiq. Matn olib, band raqamlari bilan iqtibos qilingan"),
    Source("T0", "ASL BELGISI / CRPT Turon",
           "https://aslbelgisi.uz",
           "GTIN, seriya, 44 belgili tekshiruv kodi — A1 haqiqiylik",
           next_step="API ochiq emas (xtrace 401) → operator bilan uchrashuv. "
                     "MUHIM: A1 davlatniki, biz ustiga quramiz"),
    Source("T0", "O'zbekiston ochiq ma'lumotlar portali (yangi)",
           "https://data.egov.uz/datasets",
           "Davlat datasetlari; «Tarkibi bir xil, nomi turlicha» so'rovi "
           "363 ovoz bilan birinchi o'rinda",
           next_step="Portal ochiq (Nuxt SSR), lekin bu dataset hali SO'ROV — "
                     "e'lon qilinmagan. Farmatsevtika dataseti topilmadi."),
    Source("T0", "Ochiq ma'lumotlar portali (eski)",
           "https://olddata.gov.uz/uz",
           "«Tarkibi bir xil ammo turli nomlanishga ega dori vositalari» "
           "so'rovi — rasmiy ekvivalentlik ro'yxati bo'lardi",
           next_step="REQUEST: 363 ovoz yig'ilgan, hali dataset emas. "
                     "Bizning INN guruhi vaqtincha shu bo'shliqni yopadi."),
    Source("T0", "Statistika qo'mitasi", "https://stat.uz",
           "Import/mahalliy ulush statistikasi",
           next_step="403 (bot bloki) — brauzer orqali yoki so'rov"),

    # ---------------- T1 · tijoriy / ochiq ----------------
    Source("T1", "apteka.uz", "https://apteka.uz",
           "Dorixona narxlari, savdo nomlari, ishlab chiqaruvchi — A3 narx qatlami",
           next_step="Sayt ochiq; 48 mahsulot yig'ilgan (mini.json). To'liq "
                     "katalog uchun hamkorlik so'rovi."),
    Source("T1", "Dorixona tarmoqlari (POS)", "—",
           "Real narx va qoldiq",
           next_step="W0 pilot: 1 tarmoq bilan to'g'ridan-to'g'ri shartnoma"),

    # ---------------- T2 · xalqaro standart ----------------
    Source("T2", "JSST INN / ATC", "https://atcddd.fhi.no",
           "Xalqaro nom va ATC kodi — birlashtiruvchi kalit",
           next_step="Ochiq jadval, bir marta yuklanadi"),
    Source("T2", "GS1", "https://www.gs1.org/standards",
           "GTIN tuzilishi, tekshiruv raqami",
           next_step="Ochiq spetsifikatsiya"),

    # ---------------- T3 · chet el (FAQAT bo'shliq uchun) ----------------
    Source("T3", "openFDA", "https://api.fda.gov/drug/label.json",
           "AQSh ro'yxati: brend, INN, ishlab chiqaruvchi",
           next_step="Ochiq API. LEKIN bu AQSh bozori — UZ kartasida ISHLATILMAYDI"),
    Source("T3", "RxNorm", "https://rxnav.nlm.nih.gov/REST",
           "Nom normalizatsiyasi",
           next_step="Ochiq. Faqat nomlash uchun; qaytgan natija darvozadan o'tishi shart"),
]


def probe(s: Source, timeout: int = 12) -> Source:
    if s.url.startswith("—"):
        s.status, s.evidence = "REQUEST", "hamkorlik so'rovi kerak"
        return s
    try:
        req = urllib.request.Request(s.url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; O'RINDOR/1.0)",
            "Accept": "text/html,application/json,*/*"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(20000)
            code = r.getcode()
            ctype = r.headers.get("Content-Type", "")
            size = len(body)
        if "json" in ctype:
            s.status = "OPEN"
        elif b"<table" in body.lower():
            s.status = "OPEN"           # ochiq HTML jadval (GMP reyestri)
        elif size < 2500 and b'id="app"' in body:
            s.status = "SHELL"          # SPA — API yopiq
        elif size < 3000 and b"__NUXT__" in body:
            s.status = "SHELL"
        elif code == 200:
            s.status = "OPEN"
        else:
            s.status = "BLOCKED"
        s.evidence = f"HTTP {code} · {ctype.split(';')[0]} · {size}B"
    except urllib.error.HTTPError as e:
        s.status = "BLOCKED" if e.code in (401, 403) else "CLOSED"
        s.evidence = f"HTTP {e.code}"
    except Exception as e:
        reason = str(getattr(e, "reason", e))
        if "getaddrinfo" in reason or "Name or service" in reason:
            s.status = "UNRESOLVED"     # manba ochiq, DNS yo'q — "yopiq" EMAS
            s.evidence = "DNS: domen topilmadi (bu muhitda)"
        elif "timed out" in reason.lower():
            s.status = "BLOCKED"
            s.evidence = "timeout"
        else:
            s.status = "CLOSED"
            s.evidence = f"{type(e).__name__}: {reason}"[:80]
    return s


MARK = {"OPEN": "✅", "SHELL": "🟡", "CLOSED": "⛔", "BLOCKED": "⛔",
        "UNRESOLVED": "🌐", "REQUEST": "📝", "?": "?"}


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    print("O'RINDOR · manba holati (O'zbekiston birinchi)\n" + "═" * 78)
    for s in SOURCES:
        probe(s)
        print(f"  {MARK[s.status]} [{s.tier}] {s.name:<52} "
              f"{s.status:<11} {s.evidence}")
        time.sleep(0.1)

    print("\n" + "─" * 78)
    tiers = {}
    for s in SOURCES:
        tiers.setdefault(s.tier, []).append(s.status)
    for t in sorted(tiers):
        st = tiers[t]
        print(f"  {t}: {len(st)} manba · ochiq {st.count('OPEN')} · "
              f"yopiq {st.count('CLOSED') + st.count('BLOCKED')} · "
              f"DNS yo'q {st.count('UNRESOLVED')} · so'rov {st.count('REQUEST')}")

    gmp = [s for s in SOURCES if s.url.startswith("https://uzpharm-gxp.uz")]
    print(f"\n  GMP: {len(gmp)} ochiq HTML reyestr topildi, holati — "
          f"{', '.join(sorted({s.status for s in gmp})) or '—'}")

    fp = os.path.join(OUT, "source_status.json")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump({"built": TODAY, "sources": [asdict(s) for s in SOURCES]},
                  f, ensure_ascii=False, indent=1)
    print(f"\n→ {fp}")


if __name__ == "__main__":
    main()
