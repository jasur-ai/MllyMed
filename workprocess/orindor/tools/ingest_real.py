"""
O'RINDOR · real ma'lumot yig'ish (demo ma'lumot EMAS)
================================================
Talab: "demo data ishlatmaymiz, faqat real ma'lumotlarni yig'amiz".

Manbalar (ikkisi ham jonli, kalitsiz, ochiq):
  1. openFDA drug/label  — haqiqiy ro'yxatdan o'tgan mahsulotlar: brend, INN,
                           ishlab chiqaruvchi, doza, shakl, yo'l.
  2. RxNorm (NLM)        — INN ↔ savdo nomi normalizatsiyasi (haqiqiy AI qatlami).

Har bir yozuv yonida PROVENANCE saqlanadi: manba URL, olingan sana, maydon.
Bu muhim: "bu raqam qayerdan?" degan savolga javob faylning o'zida turadi.

Nima ULAB BO'LMAYDI (halol chegara):
  - O'zbekiston reyestri, sertifikat raqamlari, BE dosyelari, narxlar —
    bular openFDA da YO'Q. Ular uchun `uz_registry` sxemasi tayyor, lekin
    to'ldirilmagan. Kod ularni "PENDING" deb belgilaydi, o'ylab topmaydi.

Ishga tushirish:  python3 egiz/ingest_real.py
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from datetime import date

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TODAY = date.today().isoformat()

# O'zbekiston dorixonalarida eng ko'p uchraydigan INN lar.
# MUHIM REAL TOPILMA: bir xil modda turli mamlakatda turli nomda.
#   paracetamol (UZ/JSST) = acetaminophen (AQSh)
#   salbutamol  (UZ/JSST) = albuterol     (AQSh)
# Shuning uchun har INN uchun alias ro'yxati — bu agent ning nom
# normalizatsiyasi qatlami aynan shu muammoni yechadi.
TARGET_INNS = [
    ("paracetamol", ["acetaminophen"]), ("metformin", []), ("amoxicillin", []),
    ("ceftriaxone", []), ("ibuprofen", []), ("levothyroxine", []),
    ("warfarin", []), ("omeprazole", []), ("losartan", []), ("amlodipine", []),
    ("salbutamol", ["albuterol"]), ("diclofenac", []), ("azithromycin", []),
    ("ciprofloxacin", []), ("insulin", []),
]


def _get(url: str, tries: int = 3) -> dict | None:
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "O'RINDOR/1.0 (research)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except Exception as e:
            if i == tries - 1:
                print(f"    ! {type(e).__name__}: {e}")
                return None
            time.sleep(1.2 * (i + 1))
    return None


def fetch_openfda(inn: str, limit: int = 20) -> list[dict]:
    q = urllib.parse.quote(f'openfda.generic_name:"{inn}"')
    url = f"https://api.fda.gov/drug/label.json?search={q}&limit={limit}"
    d = _get(url)
    if not d:
        return []
    out = []
    for r in d.get("results", []):
        of = r.get("openfda", {})
        out.append({
            "id": r.get("id") or r.get("set_id"),
            "brand": (of.get("brand_name") or [None])[0],
            "inn": (of.get("generic_name") or [None])[0],
            "substance": (of.get("substance_name") or [None])[0],
            "manufacturer": (of.get("manufacturer_name") or [None])[0],
            "dosage_form": (of.get("dosage_form") or [None])[0],
            "route": (of.get("route") or [None])[0],
            "product_type": (of.get("product_type") or [None])[0],
            "spl_strength": (r.get("dosage_and_administration") or [None])[0],
            "_provenance": {"source": "openFDA drug/label", "url": url,
                            "fetched": TODAY, "field_origin": "openfda block"},
        })
    return out


def _rxcui_name(rxcui: str) -> str | None:
    """rxcui → o'qiladigan nom. approximateTerm faqat ID beradi."""
    url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/property.json?propName=RxNorm%20Name"
    d = _get(url)
    pc = (((d or {}).get("propConceptGroup") or {}).get("propConcept") or [])
    return pc[0].get("propValue") if pc else None


def rxnorm_normalize(name: str) -> dict:
    """Haqiqiy normalizatsiya — jonli RxNorm. INN ga eng yaqin tushunchani qaytaradi."""
    url = ("https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term="
           + urllib.parse.quote(name) + "&maxEntries=3")
    d = _get(url)
    cands = (((d or {}).get("approximateGroup") or {}).get("candidate") or [])
    matched = []
    for c in cands[:2]:
        nm = c.get("name") or _rxcui_name(c.get("rxcui") or "")
        matched.append({"rxcui": c.get("rxcui"), "name": nm,
                        "score": c.get("score"), "rank": c.get("rank")})
    return {
        "query": name,
        "matched": matched,
        "_provenance": {"source": "RxNorm approximateTerm + rxcui/property",
                        "url": url, "fetched": TODAY},
    }


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    products, norm = [], []

    print("1) openFDA — haqiqiy mahsulotlar")
    for inn, aliases in TARGET_INNS:
        real = []
        for q in [inn] + aliases:
            real.extend(r for r in fetch_openfda(q) if r["inn"] and r["brand"])
            time.sleep(0.25)
        for r in real:
            r["inn_who"] = inn          # JSST nomi — birlashtiruvchi kalit
        products.extend(real)
        tag = f" (+{', '.join(aliases)})" if aliases else ""
        print(f"   {inn:<14}{tag:<16} {len(real):>3} yozuv")

    print("\n2) RxNorm — nom normalizatsiyasi (o'zbekcha yozilish variantlari bilan)")
    variants = ["paracetamol", "парацетамол", "paratsetamol", "analgin",
                "metformin", "метформин", "levothyroxine", "levotiroksin",
                "amoxicillin", "амоксициллин", "ceftriaxone", "seftriakson"]
    for v in variants:
        norm.append(rxnorm_normalize(v))
        m = norm[-1]["matched"]
        top = (m[0].get("name") or "—") if m else "—"
        print(f"   {v:<14} → {top[:56]}")
        time.sleep(0.3)

    ds = {
        "meta": {
            "built": TODAY,
            "sources": ["openFDA drug/label (api.fda.gov)", "RxNorm (rxnav.nlm.nih.gov)"],
            "products": len(products),
            "note": ("Bu HAQIQIY ochiq ma'lumot. Lekin AQSh bozori — O'zbekiston "
                     "reyestri emas. UZ maydonlari (sertifikat, BE, narx) PENDING."),
        },
        "products": products,
        "rxnorm": norm,
        "uz_registry": {
            "status": "PENDING",
            "why": "uzpharm-control.uz dan import qilinishi kerak",
            "fields_needed": ["sertifikat raqami", "BE tadqiqoti", "referent mahsulot",
                              "referens narx", "partiya ro'yxati", "GTIN (ASL BELGISI)"],
        },
    }
    fp = os.path.join(OUT, "real_products.json")
    with open(fp, "w") as f:
        json.dump(ds, f, ensure_ascii=False, indent=1)
    print(f"\n→ {fp}  ({len(products)} real yozuv, {len(norm)} normalizatsiya)")


if __name__ == "__main__":
    main()
