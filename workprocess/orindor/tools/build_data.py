#!/usr/bin/env python3
"""Hamma yig'ilgan ma'lumotni bitta `data/` bo'limiga — ishlatsa bo'ladigan ko'rinishda.

Kirish:  orindor/data/uz_registry/*.jsonl   (xom yig'ish, JSONL)
         orindor/data/facts.json, arzon_sample.json
         mini_apteka/data/catalog.json
Chiqish: data/*.json (JSON massiv — ilovada to'g'ridan-to'g'ri o'qiladi)
         data/*.csv  (Excel/Sheets uchun)
         data/*.xlsx (rasmiy nusxa)
         data/index.json (manifest) + data/README.md (qo'llanma)

Ishga tushirish: python3 orindor/tools/build_data.py
"""
from __future__ import annotations

import csv
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "orindor", "data")
REG = os.path.join(SRC, "uz_registry")
OUT = os.path.join(ROOT, "data")
os.makedirs(OUT, exist_ok=True)

MANIFEST: list[dict] = []


def jsonl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def save(name: str, rows, *, note: str, source: str, keys: list[str] | None = None,
         csv_too: bool = True) -> None:
    """JSON massiv + (ixtiyoriy) CSV."""
    fp = os.path.join(OUT, name + ".json")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, separators=(",", ":"))
    entry = {
        "fayl": name + ".json",
        "yozuv": len(rows) if isinstance(rows, list) else 1,
        "kb": round(os.path.getsize(fp) / 1024, 1),
        "manba": source,
        "izoh": note,
    }
    if keys and csv_too and isinstance(rows, list) and rows:
        cp = os.path.join(OUT, name + ".csv")
        cols = keys or list(rows[0].keys())
        with open(cp, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow({k: (", ".join(v) if isinstance(v, list) else v)
                            for k, v in r.items() if k in cols})
        entry["csv"] = name + ".csv"
        entry["csv_kb"] = round(os.path.getsize(cp) / 1024, 1)
    MANIFEST.append(entry)
    print(f"  {entry['fayl']:<30} {entry['yozuv']:>7} yozuv  {entry['kb']:>8.0f} KB")


def main() -> None:
    print("=== data/ qurilmoqda ===")

    # 1) davlat reyestri
    drugs = jsonl(os.path.join(REG, "drugs.jsonl"))
    save("reyestr_dori", drugs,
         note="O'zbekiston davlat dori reyestri — to'liq",
         source="api.mpa.uz/drug-catalog-api/v2/drugs/portal/search",
         keys=["drugId", "shortName", "fullName", "mnn", "dosageForm", "strength",
               "country", "manufacturer", "registrationCode", "local", "atxCode",
               "icps", "tnved", "dispensingConditions", "prescriptionRequired"])

    # 2) referent narxlar
    ref = jsonl(os.path.join(REG, "referent.jsonl"))
    save("referent_narx", ref,
         note="3735-son bo'yicha referent (chegaraviy) narxlar",
         source="api.mpa.uz/drug-catalog-api/v1/referent-price/all",
         keys=["drugId", "trademark", "innName", "manufacturer", "registrationNumber",
               "price", "wholesalePrice", "retailPrice", "basePrice", "currency",
               "vatEnabled", "prescription", "uploadedAt"])

    # 3) tafsilot (chegara narx + tarkib)
    det = jsonl(os.path.join(REG, "details.jsonl"))
    save("tafsilot", det,
         note="dori tafsiloti: maxSalePrice = qonuniy chegara narx (asl valyutada), "
              "retailPrice = so'mdagi chakana, tarkib (substanceNames)",
         source="api.mpa.uz/drug-catalog-api/v2/drugs/{drugId}",
         keys=["id", "shortName", "fullName", "inn", "atcCode", "dosageForm", "strength",
               "country", "manufacturer", "registrationNumber", "local", "hasPrescription",
               "npp", "retailPrice", "wholeSalePrice", "maxSalePrice", "currency",
               "priceDate", "totalCountInPackage", "imgCount"])

    # 4) yordamchi jadvallar
    for src, name, note in [
        ("atc_groups.json", "atx_guruhlari", "ATX guruhlari va ulardagi dori soni"),
        ("dosage_forms.json", "dori_shakllari", "dori shakllari ro'yxati"),
        ("counts.json", "hisob", "umumiy hisob (dori + tibbiyot tashkiloti)"),
    ]:
        p = os.path.join(REG, src)
        if os.path.exists(p):
            obj = json.load(open(p, encoding="utf-8"))
            key = {"atx_guruhlari": "code", "dori_shakllari": None}.get(name)
            rows = obj if isinstance(obj, list) else obj.get("dosageForms", obj)
            save(name, rows, note=note,
                 source="api.mpa.uz/drug-catalog-api", keys=key or [])

    # 5) mini apteka katalogi (48 mahsulot)
    mp = os.path.join(ROOT, "mini_apteka", "data", "catalog.json")
    if os.path.exists(mp):
        cat = json.load(open(mp, encoding="utf-8"))
        save("mini_apteka_katalog", cat["products"],
             note="48 mahsulot: XPN, ishlab chiqaruvchi, davlat, narx, dorixonalar soni",
             source="apteka.uz (ochiq kategoriya sahifalari, 12 kategoriya × 4)",
             keys=["id", "name", "inn", "manufacturer", "country", "local", "seller",
                   "price_from_som", "pharmacies", "category", "url", "source"])

    # 6) ArzonApteka vitrinasi (20)
    ap = os.path.join(SRC, "arzon_sample.json")
    if os.path.exists(ap):
        doc = json.load(open(ap, encoding="utf-8"))
        save("arzon_vitrina", doc["products"],
             note="20 mahsulot ArzonApteka bosh sahifasidan (XPN ko'rsatilmaydi)",
             source="arzonapteka.uz/uz",
             keys=["name", "manufacturer", "price_from_som", "rx", "image_id"])

    # 7) huquqiy faktlar
    fp = os.path.join(SRC, "facts.json")
    if os.path.exists(fp):
        shutil.copy(fp, os.path.join(OUT, "faktlar.json"))
        n = len(json.load(open(fp, encoding="utf-8")).get("facts", []))
        MANIFEST.append({"fayl": "faktlar.json", "yozuv": n,
                         "kb": round(os.path.getsize(os.path.join(OUT, "faktlar.json")) / 1024, 1),
                         "manba": "lex.uz (17 hujjat)",
                         "izoh": "17 tekshirilgan fakt + 3735 narx modeli"})
        print(f"  faktlar.json                        {n:>7} fakt")

    # 8) rasmiy Excel nusxa
    xl = os.path.join(REG, "drugs_registry.xlsx")
    if os.path.exists(xl):
        shutil.copy(xl, os.path.join(OUT, "reyestr_dori.xlsx"))
        MANIFEST.append({"fayl": "reyestr_dori.xlsx", "yozuv": 40000,
                         "kb": round(os.path.getsize(xl) / 1024, 1),
                         "manba": "api.mpa.uz/v2/drugs/download-excel",
                         "izoh": "rasmiy Excel nusxa (11 ustun) — oflayn ishlash uchun"})
        print(f"  reyestr_dori.xlsx                  40000 qator  "
              f"{os.path.getsize(xl)/1048576:.1f} MB")

    # 9) manifest
    total = sum(m.get("kb", 0) for m in MANIFEST)
    man = {
        "loyiha": "O'RINDOR · №17",
        "yangilangan": "2026-11-18",
        "jami_mb": round(total / 1024, 1),
        "fayllar": MANIFEST,
        "manbalar": [
            "api.mpa.uz/drug-catalog-api (davlat reyestri, referent narx) — ochiq, kalitsiz",
            "apteka.uz (12 kategoriya) — ochiq sahifalar",
            "arzonapteka.uz (bosh sahifa, katalog daraxti) — ochiq sahifalar",
            "lex.uz (17 hujjat) — ochiq",
        ],
        "yopiq": [
            "GMP/GDP/GPP registrlari — E-IMZO talab qiladi (401)",
            "Asl Belgisi kod tekshiruvi — to'liq auth (401)",
            "GTIN / shtrix-kod — hech qayerda ochiq emas",
            "bioekvivalentlik hisobotlari — ochiq emas",
        ],
    }
    json.dump(man, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\njami: {man['jami_mb']} MB · {len(MANIFEST)} fayl → {OUT}")


if __name__ == "__main__":
    main()
