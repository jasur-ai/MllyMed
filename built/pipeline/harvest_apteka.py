#!/usr/bin/env python3
"""apteka.uz — kengaytirilgan ochiq katalog yig'uvchi (katta mahsulot uchun).

Nega yangi skript: `workprocess` dagi mini yig'uvchi har kategoriyadan 4 ta
oladi (demo uchun). Katta mahsulotga 300+ mahsulot kerak.

Qoidalar (buzilmaydi):
  • faqat ochiq server-render sahifalar; `/api/` ga tegilinmaydi
    (robots.txt taqiqlaydi);
  • har yozuvda manba URL va yig'ilgan vaqt;
  • sahifalar tugaganda to'xtaydi, takror yozuvlar `id` bo'yicha olib
    tashlanadi;
  • hech narsa taxmin qilinmaydi: davlat topilmasa `local=null`.

Ishga tushirish (built/ ichidan):
    python3 pipeline/harvest_apteka.py --max-pages 6
Natija:
    built/data/raw_apteka.json
"""
from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BUILT = Path(__file__).resolve().parents[1]
OUT = BUILT / "data" / "raw_apteka.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CATS = [
    ("antibiotiki", "Antibiotiklar"),
    ("obezbolivayushchie", "Og'riq qoldiruvchi"),
    ("protivoallergicheskie", "Antiallergik"),
    ("preparaty-pri-prostudnykh-zabolevaniyakh-i-grippe", "Shamollash va gripp"),
    ("preparaty-ot-narusheniya-kislotnosti", "Kislotalik"),
    ("krov-i-krovoobrashchenie", "Qon aylanishi"),
    ("nervnaya-sistema", "Asab tizimi"),
    ("gormonalnye", "Gormonal"),
    ("dykhatelnaya-sistema", "Nafas olish"),
    ("protivogribkovye", "Zamburug'ga qarshi"),
    ("pishchevaritelnyy-trakt-i-obmen-veshchestv", "Hazm tizimi"),
    ("oftalmologicheskie-preparaty", "Ko'z vositalari"),
    ("serdechno-sosudistye-preparaty", "Yurak-qon tomir"),
    ("mochepolovaya-sistema", "Siydik-tanosil"),
    ("immunomodulyatory", "Immunitet"),
    ("vitaminy", "Vitaminlar"),
]

COUNTRIES = {
    "o'zbekiston": True, "узбекистан": True, "uzbekistan": True,
    "hindiston": False, "индия": False, "india": False,
    "rossiya": False, "россия": False, "russia": False,
    "ukraina": False, "германия": False, "germaniya": False, "germany": False,
    "turkiya": False, "турция": False, "xitoy": False, "китай": False,
    "belarus": False, "беларусь": False, "polsha": False, "польша": False,
    "vengriya": False, "венгрия": False, "sloveniya": False, "slovenia": False,
    "italiya": False, "италия": False, "fransiya": False, "франция": False,
    "aqsh": False, "сша": False, "koreya": False, "корея": False,
    "yaponiya": False, "япония": False, "shveytsariya": False,
    "iordaniya": False, "saudiya": False, "avstriya": False, "ispaniya": False,
    "chexiya": False, "ruminiya": False, "bolgariya": False, "latviya": False,
    "litva": False, "eston": False, "gretsiya": False, "kipr": False,
    "pokiston": False, "pakistan": False, "bangladesh": False,
    "vyetnam": False, "vetnam": False, "indoneziya": False,
}


def get(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Language": "uz,ru;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def txt(h: str) -> str:
    h = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>",
               " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", "\x00", h)
    for a, b in (("&#39;", "'"), ("&quot;", '"'), ("&amp;", "&"),
                 ("&nbsp;", " "), ("&#x27;", "'"), ("&#x2F;", "/")):
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h)


def find_country(t: str) -> tuple[str | None, bool | None]:
    low = t.lower()
    best = None
    for name, is_uz in COUNTRIES.items():
        i = low.find(name)
        if i >= 0 and (best is None or i < best[1]):
            best = (name, i, is_uz)
    if not best:
        return None, None
    return best[0].capitalize(), best[2]


def parse_cards(html: str, label: str) -> list[dict]:
    out = []
    chunks = re.split(r'<div class="h-full relative"', html)[1:]
    if not chunks:
        chunks = re.split(r'(?=href="/uz/offer/)', html)[1:]
    for p in chunks:
        p = p[:7000]
        offer = re.search(r'href="(/uz/offer/[a-z0-9-]+)"', p)
        alt = re.search(r'alt="([^"]{3,170})"', p)
        if not offer or not alt:
            continue
        inn = re.search(r'href="/uz/products/active-[a-z0-9-]+"[^>]*>([^<]{2,60})<', p)
        man = re.search(r"Ishlab chiqaruvchi</span>:\s*</div>\s*<div[^>]*>([^<]{2,90})<", p)
        seller = re.search(r"Vakil</span>:\s*</div>\s*<a[^>]*>([^<]{2,90})<", p)
        t = re.sub(r"\s+", " ", txt(p))
        price = re.search(r"([\d\s\u00a0]{3,14})\s*so'm dan", t)
        pharm = re.search(r"(\d+)\s*ta dorixonada bor", t)
        country, local = find_country(t)
        out.append({
            "id": offer.group(1).rsplit("/", 1)[-1],
            "name": re.sub(r"\s+", " ", alt.group(1)).strip(),
            "inn": inn.group(1).strip() if inn else None,
            "manufacturer": re.sub(r"\s+", " ", man.group(1)).strip() if man else None,
            "country": country,
            "local": local,
            "seller": re.sub(r"\s+", " ", seller.group(1)).strip() if seller else None,
            "price_from_som": int(re.sub(r"\D", "", price.group(1))) if price else None,
            "pharmacies": int(pharm.group(1)) if pharm else None,
            "category": label,
            "url": "https://apteka.uz" + offer.group(1),
            "source": "apteka.uz",
            "rx": "Retsept" in t,
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-pages", type=int, default=6)
    ap.add_argument("--sleep", type=float, default=0.5)
    args = ap.parse_args()

    seen: dict[str, dict] = {}
    stats = []
    for slug, label in CATS:
        got = 0
        for page in range(1, args.max_pages + 1):
            url = f"https://apteka.uz/uz/products/{slug}"
            if page > 1:
                url += f"?page={page}"
            try:
                html = get(url)
            except Exception as e:                        # noqa: BLE001
                print(f"  ! {slug} p{page}: {type(e).__name__}")
                break
            cards = parse_cards(html, label)
            new = [c for c in cards if c["id"] not in seen]
            for c in new:
                seen[c["id"]] = c
            got += len(new)
            if not cards or not new:
                break
            time.sleep(args.sleep)
        stats.append({"slug": slug, "name": label, "products": got})
        print(f"  {label:<22} {got:>3} yangi")

    products = list(seen.values())
    doc = {
        "meta": {
            "harvested": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": "apteka.uz — ochiq server-render sahifalar",
            "constraint": "/api/ robots.txt da taqiqlangan — ishlatilmadi",
            "categories": stats,
            "counts": {
                "products": len(products),
                "with_inn": sum(1 for p in products if p["inn"]),
                "priced": sum(1 for p in products if p["price_from_som"]),
                "local": sum(1 for p in products if p["local"] is True),
                "import": sum(1 for p in products if p["local"] is False),
                "unknown_origin": sum(1 for p in products if p["local"] is None),
                "sellers": len({p["seller"] for p in products if p["seller"]}),
                "inn_groups": len({(p["inn"] or "").lower() for p in products if p["inn"]}),
            },
        },
        "products": products,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    c = doc["meta"]["counts"]
    print(f"\n→ {OUT}")
    print(f"  mahsulot {c['products']} · XPN {c['with_inn']} · narx {c['priced']} · "
          f"mahalliy {c['local']} · import {c['import']} · noma'lum {c['unknown_origin']}")
    print(f"  sotuvchi {c['sellers']} · XPN guruh {c['inn_groups']}")
    return 0 if products else 1


if __name__ == "__main__":
    raise SystemExit(main())
