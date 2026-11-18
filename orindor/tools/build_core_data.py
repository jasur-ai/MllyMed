#!/usr/bin/env python3
"""O'RINDOR — yadro ma'lumotini yig'ish.

Manba (xom, o'zgartirilmagan): `workprocess/data/`
    reyestr_dori.json   46 079 yozuv  — api.mpa.uz davlat reyestri
    referent_narx.json  12 612 yozuv  — 3735-son bo'yicha chegaraviy narxlar
    tafsilot.json          538 yozuv  — maxSalePrice + tarkib
    mini_apteka_katalog.json 48 yozuv  — apteka.uz narxlari (solishtirish)

Natija: `orindor/data/`
    drugs.json       siqilgan reyestr (massiv-yozuvlar, tez yuklanadi)
    inn.json         XPN guruhlari (mahalliy/import hisobi)
    refprice.json    referent narxlar
    detail.json      chegara narx + tarkib
    mini.json        dorixona katalogi
    stats.json       qamrov va sifat ko'rsatkichlari
    aliases.json     savdo nomi → XPN (qo'lda tekshirilgan)

Ishga tushirish:
    python3 orindor/tools/build_core_data.py
    python3 orindor/tools/build_core_data.py --src workprocess/data
"""
from __future__ import annotations

import argparse
import collections
import json
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = ROOT.parent / "workprocess" / "data"
OUT = ROOT / "data"

CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
    "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    "ў": "o", "қ": "q", "ғ": "g", "ҳ": "h",
}


def translit(s: str) -> str:
    return "".join(CYR.get(ch, ch) for ch in (s or "").lower())


def norm(s: str) -> str:
    t = unicodedata.normalize("NFKC", s or "").lower()
    t = translit(t)
    t = t.replace("ʻ", "'").replace("ʼ", "'").replace("‘", "'").replace("`", "'")
    t = t.replace("®", " ").replace("™", " ")
    t = "".join(ch if (ch.isalnum() or ch == "'") else " " for ch in t)
    return " ".join(t.split())


# Savdo nomi → XPN. Faqat bir ma'noli holatlar; har biri build paytida tekshiriladi.
ALIASES = {
    # xalqaro / lotin imlosi
    "paracetamol": "paratsetamol",
    "amoxicillin": "amoksitsillin",
    "azithromycin": "azitromitsin",
    "omeprazole": "omeprazol",
    "levothyroxine": "levotiroksin natriy",
    "levotiroksin": "levotiroksin natriy",
    "diclofenac": "diklofenak",
    "ceftriaxone": "tseftriakson",
    "prednisolone": "prednizolon",
    "dexamethasone": "deksametazon",
    "furosemide": "furosemid",
    "amlodipine": "amlodipin",
    "atorvastatin": "atorvastatin",
    "acetylsalicylic acid": "atsetilsalitsilovaya kislota",
    # savdo nomlari
    "aspirin": "atsetilsalitsilovaya kislota",
    "nurofen": "ibuprofen",
    "panadol": "paratsetamol",
    "efferalgan": "paratsetamol",
    "calpol": "paratsetamol",
    "voltaren": "diklofenak",
    "ketorol": "ketorolak",
    "ketorolac": "ketorolak",
    "noshpa": "drotaverin",
    "no shpa": "drotaverin",
    "suprastin": "xloropiramin",
    "chloropyramine": "xloropiramin",
    "mezim": "pankreatin",
    "smecta": "diosmektit",
    "analgin": "metamizol natriy",
    "metamizole": "metamizol natriy",
    "lasix": "furosemid",
    "asparkam": "kaliya va magniya asparaginat",
}


def build(src: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)

    reg = json.loads((src / "reyestr_dori.json").read_text(encoding="utf-8"))
    ref = json.loads((src / "referent_narx.json").read_text(encoding="utf-8"))
    det = json.loads((src / "tafsilot.json").read_text(encoding="utf-8"))
    mini = json.loads((src / "mini_apteka_katalog.json").read_text(encoding="utf-8"))

    # ---------- reyestr ----------
    drugs = []
    groups: dict[str, dict] = {}
    for d in reg:
        inn_disp = (d.get("mnn") or "").strip()
        inn_key = norm(inn_disp)
        local = bool(d.get("local"))
        row = [
            d.get("drugId"),
            (d.get("shortName") or "").strip(),
            (d.get("fullName") or "").strip(),
            inn_disp,
            inn_key,
            (d.get("dosageForm") or "").strip(),
            (d.get("strength") or "").strip(),
            (d.get("country") or "").strip(),
            (d.get("manufacturer") or "").strip(),
            (d.get("registrationCode") or "").strip(),
            1 if local else 0,
            (d.get("atxCode") or "").strip(),
            1 if d.get("prescriptionRequired") else 0,
        ]
        drugs.append(row)
        g = groups.setdefault(inn_key, {"name": inn_disp, "n": 0, "local": 0,
                                        "import": 0, "atc": collections.Counter(),
                                        "ids": []})
        g["n"] += 1
        g["local" if local else "import"] += 1
        if d.get("atxCode"):
            g["atc"][d["atxCode"][:5]] += 1
        g["ids"].append(d["drugId"])

    # XPN ko'rinishi: eng ko'p uchraydigan yozilish
    display = collections.Counter(norm(d[3]) for d in drugs)

    inn_out = {}
    for key, g in groups.items():
        if not key:
            continue
        inn_out[key] = {
            "name": g["name"],
            "n": g["n"],
            "local": g["local"],
            "import": g["import"],
            "atc": (g["atc"].most_common(1)[0][0] if g["atc"] else ""),
            "ids": g["ids"],
        }

    # ---------- narx ----------
    refprice = {}
    for r in ref:
        if r.get("drugId") is None:
            continue
        refprice[str(r["drugId"])] = [
            r.get("price"), r.get("wholesalePrice"), r.get("retailPrice"),
            r.get("basePrice"), r.get("currency"), r.get("prescription"),
            r.get("uploadedAt"), (r.get("trademark") or "").strip(),
            norm(r.get("innName") or ""),
        ]

    detail = {}
    for t in det:
        detail[str(t["id"])] = [
            t.get("maxSalePrice"), t.get("currency"), t.get("retailPrice"),
            t.get("wholeSalePrice"), t.get("priceDate"),
            [s for s in (t.get("substanceNames") or []) if s],
            t.get("totalCountInPackage"), t.get("imgCount"),
            norm(t.get("inn") or ""), (t.get("atcCode") or "").strip(),
        ]

    mini_out = [{
        "name": m.get("name"), "inn": m.get("inn"), "local": m.get("local"),
        "manufacturer": m.get("manufacturer"), "country": m.get("country"),
        "price": m.get("price_from_som"), "pharmacies": m.get("pharmacies"),
        "category": m.get("category"), "url": m.get("url"),
    } for m in mini]

    # ---------- sifat ----------
    with_price_reg = sum(1 for d in drugs if str(d[0]) in refprice)
    with_detail = sum(1 for d in drugs if str(d[0]) in detail)
    by_inn = collections.Counter(d[4] for d in drugs if d[4])
    unresolved = [a for a, target in ALIASES.items() if norm(target) not in inn_out]

    stats = {
        "built": date.today().isoformat(),
        "drugs": len(drugs),
        "local": sum(1 for d in drugs if d[10] == 1),
        "import": sum(1 for d in drugs if d[10] == 0),
        "inn_groups": len(inn_out),
        "referent_prices": len(refprice),
        "details": len(detail),
        "drugs_with_referent_price": with_price_reg,
        "drugs_with_detail": with_detail,
        "price_coverage_pct": round(100 * with_price_reg / len(drugs), 1),
        "details_coverage_pct": round(100 * with_detail / len(drugs), 2),
        "top_inn": [{"inn": k, "n": v} for k, v in by_inn.most_common(10)],
        "aliases": len(ALIASES),
        "aliases_unresolved": unresolved,
        "schema": {
            "drug": ["drugId", "shortName", "fullName", "inn", "innKey",
                     "dosageForm", "strength", "country", "manufacturer",
                     "registrationCode", "local", "atcCode", "prescription"],
            "refprice": ["price", "wholesalePrice", "retailPrice", "basePrice",
                         "currency", "prescription", "uploadedAt", "trademark", "innKey"],
            "detail": ["maxSalePrice", "currency", "retailPrice", "wholeSalePrice",
                       "priceDate", "substances", "packageCount", "imgCount",
                       "innKey", "atcCode"],
        },
        "sources": [
            "api.mpa.uz/drug-catalog-api/v2/drugs/portal/search — davlat reyestri",
            "api.mpa.uz/drug-catalog-api/v1/referent-price/all — 3735-son narxlar",
            "api.mpa.uz/drug-catalog-api/v2/drugs/{id} — tafsilot, maxSalePrice",
            "apteka.uz — ochiq kategoriya sahifalari (solishtirish uchun)",
        ],
    }

    def dump(name: str, obj) -> None:
        (out / name).write_text(
            json.dumps(obj, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")

    dump("drugs.json", drugs)
    dump("inn.json", inn_out)
    dump("refprice.json", refprice)
    dump("detail.json", detail)
    dump("mini.json", mini_out)
    dump("stats.json", stats)
    dump("aliases.json", ALIASES)

    return stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(DEFAULT_SRC))
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    s = build(Path(a.src), Path(a.out))
    print(json.dumps({k: v for k, v in s.items() if k != "schema"},
                     ensure_ascii=False, indent=1))
    sizes = {p.name: round(p.stat().st_size / 1024, 1)
             for p in sorted(Path(a.out).glob("*.json"))}
    print("\nfayllar (KB):", json.dumps(sizes, ensure_ascii=False))


if __name__ == "__main__":
    main()
