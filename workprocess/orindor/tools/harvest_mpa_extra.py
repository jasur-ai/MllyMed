#!/usr/bin/env python3
"""Davlat reyestri API'sidan qo'shimcha parchalar — to'liq yig'ish.

TOPILGAN QO'SHIMCHA ENDPOINTLAR (avvalgi harvest_mpa.py dan keyin):
    · /v2/drugs/download-excel          → butun reyestr Excel (2.8 MB, 40 000 qator)
    · /v2/drugs/{drugId}                → tafsilot: maxSalePrice (dollar), retailPrice,
                                          priceDate, totalCountInPackage, npp, tarkib
                                          (substanceNames), 5 ta qadoq rasmi
    · /v1/atc-groups/all                → ATX guruhlari + dori soni
    · /v1/analysis/counts               → 46 079 dori · 400 tibbiyot tashkiloti
    · /v1/drugs/rec-drug-dosage-form    → dori shakllari ro'yxati

YOPIQ QOLGANLAR (tekshirildi, 401):
    · registry/gmp-registry, gdp, gpp, gcp, glp, gsp — auth kerak
    · instruction/detail                             — auth kerak
    · Asl Belgisi /api/cod/public/code               — to'liq auth (xtrace.aslbelgisi.uz)
    · GTIN / shtrix-kod — Excel da ham, qadoq rasmlarida ham yo'q

Ishga tushirish: python3 orindor/tools/harvest_mpa_extra.py
"""
from __future__ import annotations

import json
import os
import time
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "uz_registry")
BASE = "https://api.mpa.uz/drug-catalog-api"
UA = "ORINDOR data harvester (open portal API)"


def get(u: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def getj(u: str) -> dict | list:
    return json.loads(get(u).decode())


def main() -> None:
    os.makedirs(OUT, exist_ok=True)

    # 1) butun reyestr — Excel
    fp = os.path.join(OUT, "drugs_registry.xlsx")
    if not os.path.exists(fp) or os.path.getsize(fp) < 1_000_000:
        data = get(BASE + "/v2/drugs/download-excel")
        open(fp, "wb").write(data)
        print(f"1. Excel: {len(data)/1048576:.1f} MB → {os.path.basename(fp)}")

    # 2) ATX guruhlari
    atc = getj(BASE + "/v1/atc-groups/all")
    json.dump(atc, open(os.path.join(OUT, "atc_groups.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"2. ATX guruhlari: {len(atc)} ta (jami {sum(a.get('drugCount', 0) for a in atc)} dori)")

    # 3) umumiy hisob
    counts = getj(BASE + "/v1/analysis/counts")
    json.dump(counts, open(os.path.join(OUT, "counts.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"3. hisob: {counts}")

    # 4) dori shakllari
    forms = getj(BASE + "/v1/drugs/rec-drug-dosage-form")
    json.dump(forms, open(os.path.join(OUT, "dosage_forms.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"4. dori shakllari: {len(forms.get('dosageForms', []))} ta")

    # 5) tafsilotlar — referent narxi bor dorilar uchun (mini apteka XPN lari)
    ref = [json.loads(l) for l in
           open(os.path.join(OUT, "referent.jsonl"), encoding="utf-8")]
    ids, seen = [], set()
    for r in ref:
        i = r.get("drugId")
        if i and i not in seen:
            seen.add(i)
            ids.append(i)
    ids = ids[:1200]                      # birinchi 1200 — tafsilot namunasi
    det_fp = os.path.join(OUT, "details.jsonl")
    done = 0
    if os.path.exists(det_fp):
        done = sum(1 for _ in open(det_fp, encoding="utf-8"))
    print(f"5. tafsilot: {len(ids)} dori (bor: {done})")

    with open(det_fp, "a", encoding="utf-8") as f:
        for i in ids[done:]:
            try:
                d = getj(f"{BASE}/v2/drugs/{i}")
                r = d.get("result", d)
            except Exception:                                  # noqa: BLE001
                continue
            if not isinstance(r, dict) or "id" not in r:
                continue
            f.write(json.dumps({
                "id": r.get("id"),
                "shortName": r.get("shortName"),
                "fullName": r.get("fullName"),
                "inn": r.get("inn"),
                "atcCode": r.get("atcCode"),
                "dosageForm": r.get("dosageForm"),
                "strength": r.get("strength"),
                "country": r.get("country"),
                "manufacturer": r.get("manufacturer"),
                "registrationNumber": r.get("registrationNumber"),
                "local": r.get("local"),
                "hasPrescription": r.get("hasPrescription"),
                "npp": r.get("npp"),
                "retailPrice": r.get("retailPrice"),
                "wholeSalePrice": r.get("wholeSalePrice"),
                "maxSalePrice": r.get("maxSalePrice"),
                "currency": r.get("currency"),
                "priceDate": r.get("priceDate"),
                "totalCountInPackage": r.get("totalCountInPackage"),
                "substanceNames": r.get("substanceNames"),
                "imgCount": len(r.get("imgUrls") or []),
            }, ensure_ascii=False) + "\n")
            done += 1
            if done % 100 == 0:
                f.flush()
                print(f"   {done}/{len(ids)}")
            time.sleep(0.12)

    print(f"\n=== NATIJA ({OUT}) ===")
    for name in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, name)
        print(f"  {name:<24} {os.path.getsize(p)/1024:>9.0f} KB")


if __name__ == "__main__":
    main()
