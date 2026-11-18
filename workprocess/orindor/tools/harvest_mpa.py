#!/usr/bin/env python3
"""Davlat dori reyestri + referent narxlar — OCHIQ API dan yig'ish.

TOPILGAN MANBA (bu asosiy yutuq):
    https://api.mpa.uz/drug-catalog-api/
    · /v2/drugs/portal/search?search=&page=&size=   → davlat reyestri (46 079 dori)
    · /v1/referent-price/all?page=&size=            → referent narxlar (12 612 yozuv)

Nega bu muhim: shu paytgacha "yopiq" deb hisoblangan uchta maydon aslida OCHIQ:
    · reyestr raqami        → registrationCode
    · XPN (INN)             → mnn / innName
    · mahalliy/import       → local (rasmiy bayroq, taxmin emas)
    · referent narx         → price / wholesalePrice / retailPrice

Xulq: 1000 tadan so'raladi (47 + 13 so'rov), har so'rov orasida 0.5 s kutish.
Yozuv davom etadigan (resume): har sahifa JSONL ga qo'shiladi, meta.json da holat.

Ishga tushirish:  python3 orindor/tools/harvest_mpa.py
Natija:           orindor/data/uz_registry/{drugs.jsonl, referent.jsonl, meta.json}
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "uz_registry")
BASE = "https://api.mpa.uz/drug-catalog-api"
UA = "ORINDOR data harvester (open portal API; contact: workspace)"
PAGE = 1000
DELAY = 0.5

DRUG_KEYS = ["drugId", "shortName", "fullName", "mnn", "dosageForm", "strength",
             "country", "manufacturer", "registrationCode", "local", "atxCode",
             "icps", "tnved", "dispensingConditions", "prescriptionRequired"]
REF_KEYS = ["drugId", "trademark", "innName", "manufacturer", "registrationNumber",
            "price", "wholesalePrice", "retailPrice", "basePrice", "currency",
            "vatEnabled", "prescription", "uploadedAt"]


def get(url: str, tries: int = 3) -> dict:
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if i == tries - 1:
                raise
            print(f"    qayta urinish ({e})")
            time.sleep(2 + i * 3)
    return {}


def body(d: dict) -> dict:
    """Ba'zi endpointlar {"result": {...}} ichida, ba'zilari to'g'ridan-to'g'ri."""
    return d.get("result", d)


def harvest(name: str, url_tpl: str, keys: list[str]) -> dict:
    os.makedirs(OUT, exist_ok=True)
    fp = os.path.join(OUT, f"{name}.jsonl")
    meta_fp = os.path.join(OUT, "meta.json")
    meta = {}
    if os.path.exists(meta_fp):
        meta = json.load(open(meta_fp, encoding="utf-8"))
    m = meta.setdefault(name, {})
    start = m.get("pages_done", 0)

    # birinchi so'rov — jami hajmni bilish uchun
    first = body(get(url_tpl.format(page=0, size=1)))
    total = first.get("totalElements", 0)
    pages = (total + PAGE - 1) // PAGE
    print(f"{name}: jami {total} yozuv → {pages} sahifa (boshlanish: {start})")

    done = start
    for page in range(start, pages):
        d = body(get(url_tpl.format(page=page, size=PAGE)))
        rows = d.get("content", [])
        if not rows:
            break
        with open(fp, "a", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps({k: row.get(k) for k in keys},
                                   ensure_ascii=False) + "\n")
        done = page + 1
        m.update({"pages_done": done, "total": total, "pages": pages,
                  "updated": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        meta[name] = m
        json.dump(meta, open(meta_fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"  sahifa {done}/{pages} — {len(rows)} yozuv")
        time.sleep(DELAY)

    m["ok"] = True
    meta[name] = m
    json.dump(meta, open(meta_fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return m


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    print("=== 1. davlat reyestri ===")
    harvest("drugs",
            BASE + "/v2/drugs/portal/search?search=&page={page}&size={size}",
            DRUG_KEYS)

    print("\n=== 2. referent narxlar ===")
    harvest("referent",
            BASE + "/v1/referent-price/all?page={page}&size={size}",
            REF_KEYS)

    # qisqa hisobot
    print("\n=== NATIJA ===")
    for name in ("drugs", "referent"):
        fp = os.path.join(OUT, f"{name}.jsonl")
        if not os.path.exists(fp):
            continue
        n = sum(1 for _ in open(fp, encoding="utf-8"))
        kb = os.path.getsize(fp) / 1024
        print(f"  {name}: {n} yozuv, {kb:.0f} KB")

    dfp = os.path.join(OUT, "drugs.jsonl")
    if os.path.exists(dfp):
        rows = [json.loads(l) for l in open(dfp, encoding="utf-8")]
        loc = sum(1 for r in rows if r.get("local") is True)
        inn = len({(r.get("mnn") or "").lower() for r in rows if r.get("mnn")})
        reg = sum(1 for r in rows if r.get("registrationCode"))
        print(f"  mahalliy: {loc} | import: {len(rows) - loc} | XPN turi: {inn} | "
              f"reyestr kodi bor: {reg}")


if __name__ == "__main__":
    main()
