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

Ishga tushirish:  python3 egiz/sources.py
"""

from __future__ import annotations

import json
import os
import time
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
    status: str = "?"        # OPEN / SHELL / CLOSED / BLOCKED / REQUEST
    evidence: str = ""
    next_step: str = ""


SOURCES: list[Source] = [
    # ---------------- T0 · rasmiy ----------------
    Source("T0", "O'zR dori vositalari davlat reyestri", "https://uzpharm-control.uz/registry/drugs",
           "Ro'yxatdan o'tgan dorilar, sertifikat raqami, ishlab chiqaruvchi",
           next_step="Sayt SPA. API nginx orqasida yopiq → yozma so'rov (Farmatsevtika agentligi)"),
    Source("T0", "Dori sertifikatlari reyestri", "https://uzpharm-control.uz/registry/drug-certificates",
           "Sertifikat raqami, amal qilish muddati — A2 dalil qatlamining asosi",
           next_step="Shu sahifa — №17 ning 'shaffof sertifikat' talabining manbasi"),
    Source("T0", "lex.uz — VMQ 738-son (24.11.2025)", "https://lex.uz/uz/docs/-7853907",
           "BE talabi, bioveyver, ICH 2029 — qoidalar matni",
           next_step="Ochiq. Matnni olib, band raqamlari bilan iqtibos qilish"),
    Source("T0", "ASL BELGISI / CRPT Turon", "https://aslbelgisi.uz",
           "GTIN, seriya, 44 belgili tekshiruv kodi — A1 haqiqiylik",
           next_step="API ochiq emas → operator bilan uchrashuv. MUHIM: A1 davlatniki, biz ustiga quramiz"),
    Source("T0", "O'zbekiston ochiq ma'lumotlar portali", "https://openinfo.uz",
           "Davlat datasetlari",
           next_step="Portal ochiq, lekin farmatsevtika dataseti topilmadi"),
    Source("T0", "Statistika qo'mitasi", "https://stat.uz", "Import/mahalliy ulush statistikasi",
           next_step="403 (bot bloki) — brauzer orqali yoki so'rov"),

    # ---------------- T1 · tijoriy / ochiq ----------------
    Source("T1", "apteka.uz", "https://apteka.uz",
           "Dorixona narxlari, savdo nomlari, ishlab chiqaruvchi — A3 narx qatlami",
           next_step="Sayt ochiq; ichki API /api/v1/search/drugs topildi, lekin baza host yopiq → hamkorlik so'rovi"),
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
            body = r.read(6000)
            code = r.getcode()
            ctype = r.headers.get("Content-Type", "")
            size = len(body)
        if "json" in ctype:
            s.status = "OPEN"
        elif size < 2500 and b"id=\"app\"" in body:
            s.status = "SHELL"          # SPA — API yopiq
        elif code == 200:
            s.status = "OPEN"
        else:
            s.status = "BLOCKED"
        s.evidence = f"HTTP {code} · {ctype.split(';')[0]} · {size}B"
    except Exception as e:
        s.status = "CLOSED"
        s.evidence = f"{type(e).__name__}"
    return s


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    print("O'RINDOR · manba holati (O'zbekiston birinchi)\n" + "═" * 78)
    for s in SOURCES:
        probe(s)
        mark = {"OPEN": "✅", "SHELL": "🟡", "CLOSED": "⛔", "BLOCKED": "⛔",
                "REQUEST": "📝", "?": "?"}[s.status]
        print(f"  {mark} [{s.tier}] {s.name:<38} {s.status:<8} {s.evidence}")
        time.sleep(0.2)

    print("\n" + "─" * 78)
    tiers = {}
    for s in SOURCES:
        tiers.setdefault(s.tier, []).append(s.status)
    for t in sorted(tiers):
        st = tiers[t]
        print(f"  {t}: {len(st)} manba · ochiq {st.count('OPEN')} · "
              f"yopiq {st.count('CLOSED') + st.count('BLOCKED')} · so'rov {st.count('REQUEST')}")

    fp = os.path.join(OUT, "source_status.json")
    with open(fp, "w") as f:
        json.dump({"built": TODAY, "sources": [asdict(s) for s in SOURCES]},
                  f, ensure_ascii=False, indent=1)
    print(f"\n→ {fp}")


if __name__ == "__main__":
    main()
