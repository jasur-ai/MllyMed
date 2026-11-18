#!/usr/bin/env python3
"""ArzonApteka ochiq sahifalaridan real ma'lumot yig'ish.

CHEKLOVLAR (aniqlangan, taxmin emas):
  · robots.txt:  "Allow: /"  ·  "Disallow: /api/"  → /api/ ga TEGILMAYDI.
  · api.arzonapteka.uz → 401 "X-Session-Id header is required" (auth kerak).
    Demak dori qidiruvi, dorixona narxlari va katalog — hammasi yopiq.
  · Server tomonda render bo'ladigan yagona sahifa — bosh sahifa (20 unikal mahsulot).
  · /uz/search, /uz/catalog, /uz/pharmacies, /uz/org/* → brauzerda chiziladi (HTML bo'sh).

Shuning uchun bu skript FAQAT ochiq sahifani o'qiydi va ochiq aytadi:
bu to'liq katalog EMAS, bu vitrina namunasi.

Ishga tushirish:  python3 orindor/tools/arzon.py
Natija:           orindor/data/arzon_sample.json
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data")
PAGES = [
    ("uz", "https://arzonapteka.uz/uz"),
    ("ru", "https://arzonapteka.uz/ru"),
    ("en", "https://arzonapteka.uz/en"),
]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                              "Accept-Language": "uz,ru,en"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")


def parse_cards(html: str) -> list[dict]:
    """Kartani ajratish.

    Muammo: har bir tugma/svg ichida 600+ belgili class ro'yxati bor, shuning
    uchun kartaning "foydali" qismi 2500 belgidan keyin boshlanadi.
    Yechim: avval svg va uzun atribut qiymatlarini olib tashlaymiz.
    """
    h = re.sub(r"<svg\b.*?</svg>", "", html, flags=re.S)
    h = re.sub(r'="[^"]{120,}"', '=""', h)          # uzun class/srcSet qiymatlari
    out = []
    for a in re.split(r"<article\b", h)[1:]:
        a = a[:3000]
        name = re.search(r">([^<>]{6,140})</p>", a)
        if not name:
            continue
        man = re.search(r'text-muted-foreground[^>]*>([^<>]{2,80})</', a)
        price = re.search(r">([\d\s\u00a0]{3,14})\s*so[\u02bb\u2018\u2019']mdan", a)
        img = re.search(r"media\.arzonapteka\.uz/arzonapteka/([a-f0-9]{16,})\.png", a)
        out.append({
            "name": re.sub(r"\s+", " ", name.group(1)).strip(),
            "manufacturer": re.sub(r"\s+", " ", man.group(1)).strip() if man else None,
            "price_from_som": int(re.sub(r"\D", "", price.group(1))) if price else None,
            "rx": "Retseptli" in a,
            "image_id": img.group(1) if img else None,
        })
    return out


def main() -> None:
    got: dict[str, dict] = {}
    meta = []
    for lang, url in PAGES:
        try:
            html = get(url)
        except Exception as e:                     # noqa: BLE001
            meta.append({"lang": lang, "url": url, "ok": False, "error": str(e)})
            continue
        cards = parse_cards(html)
        meta.append({"lang": lang, "url": url, "ok": True,
                     "bytes": len(html), "cards": len(cards)})
        for c in cards:
            key = c["name"]
            # nom tilda farq qiladi (Парацетамол / Paracetamol) — narx bo'yicha birlashtiramiz
            if key not in got:
                c["seen_langs"] = [lang]
                c["source_url"] = url
                got[key] = c
            else:
                got[key]["seen_langs"].append(lang)
                if c["price_from_som"]:
                    prev = got[key]["price_from_som"]
                    got[key]["price_from_som"] = min(
                        prev, c["price_from_som"]) if prev else c["price_from_som"]
        time.sleep(1.2)

    records = list(got.values())
    doc = {
        "meta": {
            "manba": "arzonapteka.uz — ochiq (server-render) sahifalar",
            "olingan_vaqt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "cheklov": "robots.txt /api/ ni taqiqlaydi; api.arzonapteka.uz 401 "
                       "(X-Session-Id) — katalog va dorixona narxlari YOPIQ",
            "qamrov": "vitrina namunasi, to'liq katalog EMAS",
            "sahifalar": meta,
        },
        "products": records,
    }
    os.makedirs(OUT, exist_ok=True)
    fp = os.path.join(OUT, "arzon_sample.json")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)

    with_price = [r for r in records if r["price_from_som"]]
    print(f"yozildi: {fp}")
    print(f"  unikal mahsulot : {len(records)}")
    print(f"  narxi bor       : {len(with_price)}")
    print(f"  retseptli       : {sum(1 for r in records if r['rx'])}")
    if with_price:
        ps = sorted(r["price_from_som"] for r in with_price)
        print(f"  narx oralig'i   : {ps[0]:,} – {ps[-1]:,} so'm".replace(",", " "))


if __name__ == "__main__":
    main()
