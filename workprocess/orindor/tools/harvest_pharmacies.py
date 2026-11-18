#!/usr/bin/env python3
"""Mini apteka uchun ma'lumot yig'ish — KO'LAMGA MOS, kichik va tez.

QOIDA (foydalanuvchi talabi):
  · har kategoriyadan 3–4 ta mahsulot — ko'p bo'lsa og'ir bo'ladi;
  · tasodifiy emas: bir XPN (INN) ostida MAHALLIY va IMPORT juftligi bo'lgani
    birinchi olinadi — chunki O'RINDOR ning butun ishi shu juftlikda.

MANBALAR (ochiq, server-render; /api/ ikkalasida ham robots.txt da taqiqlangan):
  · apteka.uz      — kategoriya sahifalari: XPN, ishlab chiqaruvchi, sotuvchi,
                     «N ta dorixonada bor», narx
  · arzonapteka.uz — faqat bosh sahifa (20 mahsulot) + kategoriya daraxti

NATIJA: mini_apteka/data/catalog.json
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "mini_apteka", "data")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

MAX_PER_CAT = 4

# Ko'lam: e-retsept bo'yicha eng ko'p yoziladigan guruhlar
CATS = [
    ("antibiotiki",                                    "Antibiotiklar"),
    ("obezbolivayushchie",                             "Og'riq qoldiruvchi"),
    ("protivoallergicheskie",                          "Antiallergik"),
    ("preparaty-pri-prostudnykh-zabolevaniyakh-i-grippe", "Shamollash va gripp"),
    ("preparaty-ot-narusheniya-kislotnosti",           "Kislotalik (oshqozon)"),
    ("krov-i-krovoobrashchenie",                       "Qon aylanishi"),
    ("nervnaya-sistema",                               "Asab tizimi"),
    ("gormonalnye",                                    "Gormonal"),
    ("dykhatelnaya-sistema",                           "Nafas olish tizimi"),
    ("protivogribkovye",                               "Zamburug'ga qarshi"),
    ("pishchevaritelnyy-trakt-i-obmen-veshchestv",     "Hazm tizimi"),
    ("oftalmologicheskie-preparaty",                    "Ko'z vositalari"),
]

# Davlat nomlari — sayt kartada ko'rsatadi, shundan mahalliy/import aniqlanadi.
# "pharm" kabi umumiy so'zlar bilan taxmin qilish XATO natija bergan edi
# (Cosar Pharmaceutical, Novugen Pharma — import, lekin "pharm" bor).
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
}


def get(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "uz,ru;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def txt(h: str) -> str:
    h = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", "\x00", h)
    for a, b in (("&#39;", "'"), ("&quot;", '"'), ("&amp;", "&"),
                 ("&nbsp;", " "), ("&#x27;", "'"), ("&#x2F;", "/")):
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h)


def find_country(t: str) -> tuple[str | None, bool | None]:
    """Matndan ishlab chiqarilgan davlatni topish → (davlat, mahalliymi)."""
    low = t.lower()
    best = None
    for name, is_uz in COUNTRIES.items():
        i = low.find(name)
        if i >= 0 and (best is None or i < best[1]):
            best = (name, i, is_uz)
    if not best:
        return None, None
    return best[0].capitalize(), best[2]


def parse_cards(html: str, cat_label: str) -> list[dict]:
    """Karta tuzilmasi (apteka.uz, 2026-11):
         <a href="/uz/offer/SLUG"><img alt="NOM">  → mahsulot
         Vakil: <sotuvchi>   ·   Ishlab chiqaruvchi: <zavod>
         •N ta dorixonada bor  ·  <XPN>  ·  <narx> so'm dan
    """
    out = []
    for p in re.split(r'<div class="h-full relative" data-v-[a-z0-9]+>', html)[1:]:
        p = p[:7000]
        offer = re.search(r'href="(/uz/offer/[a-z0-9-]+)"', p)
        if not offer:
            continue
        alt = re.search(r'alt="([^"]{3,170})"', p)
        if not alt:
            continue
        inn = re.search(r'href="/uz/products/active-[a-z0-9-]+"[^>]*>([^<]{2,60})<', p)
        man = re.search(r"Ishlab chiqaruvchi</span>:\s*</div>\s*<div[^>]*>([^<]{2,90})<", p)
        seller = re.search(r"Vakil</span>:\s*</div>\s*<a[^>]*>([^<]{2,90})<", p)
        t = re.sub(r"\s+", " ", txt(p))
        price = re.search(r"([\d\s\u00a0]{3,14})\s*so'm dan", t)
        pharm = re.search(r"(\d+)\s*ta dorixonada bor", t)
        maker = re.sub(r"\s+", " ", man.group(1)).strip() if man else None
        country, local = find_country(t)
        out.append({
            "id": offer.group(1).rsplit("/", 1)[-1],
            "name": re.sub(r"\s+", " ", alt.group(1)).strip(),
            "inn": inn.group(1).strip() if inn else None,
            "manufacturer": maker,
            "country": country,
            "local": local,
            "seller": re.sub(r"\s+", " ", seller.group(1)).strip() if seller else None,
            "price_from_som": int(re.sub(r"\D", "", price.group(1))) if price else None,
            "pharmacies": int(pharm.group(1)) if pharm else None,
            "category": cat_label,
            "url": "https://apteka.uz" + offer.group(1),
            "source": "apteka.uz",
        })
    return out


def pick(cards: list[dict], n: int = MAX_PER_CAT) -> list[dict]:
    """Ko'lamga mos tanlov: juftlik hosil qiladigan XPN lar birinchi."""
    by_inn: dict[str, list[dict]] = {}
    for c in cards:
        key = (c["inn"] or "").lower()
        if key:
            by_inn.setdefault(key, []).append(c)

    def score(group: list[dict]) -> tuple:
        locs = {c["local"] for c in group}
        has_pair = (True in locs) and (False in locs)
        priced = sum(1 for c in group if c["price_from_som"])
        return (has_pair, priced, len(group))

    chosen: list[dict] = []
    used = set()
    # 1) mahalliy+import juftligi bor XPN lar
    for inn, group in sorted(by_inn.items(), key=lambda kv: score(kv[1]), reverse=True):
        if len(chosen) >= n:
            break
        if score(group)[0]:
            for c in group:
                if len(chosen) < n and c["id"] not in used:
                    chosen.append(c); used.add(c["id"])
    # 2) qolganini narxi borlardan to'ldirish
    if len(chosen) < n:
        for c in sorted(cards, key=lambda x: (x["price_from_som"] is None,
                                              -len(x["inn"] or ""))):
            if len(chosen) >= n:
                break
            if c["id"] not in used:
                chosen.append(c); used.add(c["id"])
    return chosen


def arzon_home() -> tuple[list[dict], list[dict]]:
    # Vitrina allaqachon tools/arzon.py da yig'ilgan — qayta parse qilmaymiz
    pre = os.path.join(ROOT, "orindor", "data", "arzon_sample.json")
    if os.path.exists(pre):
        saved = json.load(open(pre, encoding="utf-8"))["products"]
        prods = [{"id": "arzon-" + re.sub(r"\W+", "-", p["name"].lower())[:40],
                  "name": p["name"], "inn": None,
                  "manufacturer": p.get("manufacturer"), "country": None,
                  "local": None, "seller": "ArzonApteka tarmog'i",
                  "price_from_som": p.get("price_from_som"), "pharmacies": None,
                  "category": "ArzonApteka vitrinasi",
                  "url": "https://arzonapteka.uz/uz", "source": "arzonapteka.uz",
                  "rx": p.get("rx")} for p in saved]
        cats_html = get("https://arzonapteka.uz/uz/catalog")
        cats, seen = [], set()
        for m in re.finditer(r'href="(/uz/catalog/[a-z0-9/-]+)"[^>]*>(.*?)</a>', cats_html, re.S):
            url, inner = m.group(1), txt(m.group(2))
            cnt = re.search(r"([\d\s]{1,9})\s*ta mahsulot", inner)
            nm = re.sub(r"[\d\s]+ta mahsulot", "", inner.replace("\x00", " ")).strip()
            if not nm or url in seen:
                continue
            seen.add(url)
            cats.append({"url": "https://arzonapteka.uz" + url, "name": nm,
                         "count": int(re.sub(r"\D", "", cnt.group(1))) if cnt else None})
        return prods, cats

    html = get("https://arzonapteka.uz/uz")
    prods = []
    h = re.sub(r"<svg\b.*?</svg>", "", html, flags=re.S)
    for a in re.split(r"<article\b", h)[1:]:
        a = re.sub(r'="[^"]{120,}"', '=""', a[:3000])
        nm = re.search(r">([^<>]{6,140})</p>", a)
        if not nm:
            continue
        man = re.search(r"text-muted-foreground[^>]*>([^<>]{2,80})</", a)
        pr = re.search(r">([\d\s\u00a0]{3,14})\s*so[\u02bb']mdan", a)
        name = re.sub(r"\s+", " ", nm.group(1)).strip()
        prods.append({
            "id": "arzon-" + re.sub(r"\W+", "-", name.lower())[:40],
            "name": name,
            "inn": None,
            "manufacturer": man.group(1).strip() if man else None,
            "country": None,
            "local": None,
            "seller": "ArzonApteka tarmog'i",
            "price_from_som": int(re.sub(r"\D", "", pr.group(1))) if pr else None,
            "pharmacies": None,
            "category": "ArzonApteka vitrinasi",
            "url": "https://arzonapteka.uz/uz",
            "source": "arzonapteka.uz",
        })
    cats_html = get("https://arzonapteka.uz/uz/catalog")
    cats, seen = [], set()
    for m in re.finditer(r'href="(/uz/catalog/[a-z0-9/-]+)"[^>]*>(.*?)</a>', cats_html, re.S):
        url, inner = m.group(1), txt(m.group(2))
        cnt = re.search(r"([\d\s]{1,9})\s*ta mahsulot", inner)
        name = re.sub(r"[\d\s]+ta mahsulot", "", inner.replace("\x00", " ")).strip()
        if not name or url in seen:
            continue
        seen.add(url)
        cats.append({"url": "https://arzonapteka.uz" + url, "name": name,
                     "count": int(re.sub(r"\D", "", cnt.group(1))) if cnt else None})
    return prods, cats


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    report = {
        "meta": {
            "olingan_vaqt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "manbalar": ["apteka.uz — 12 kategoriya (ochiq)",
                         "arzonapteka.uz — bosh sahifa + katalog daraxti (ochiq)"],
            "cheklov": "ikkala saytning /api/ yo'li robots.txt da taqiqlangan — tegmadik",
            "tanlov_qoidasi": "har kategoriyadan 3–4 ta; mahalliy+import juftligi "
                              "bo'lgan XPN lar birinchi",
        },
        "products": [], "categories": [], "arzon_showcase": [],
    }

    for slug, label in CATS:
        try:
            html = get(f"https://apteka.uz/uz/products/{slug}")
        except Exception as e:                                  # noqa: BLE001
            print(f"  ! {slug}: {e}")
            continue
        cards = parse_cards(html, label)
        chosen = pick(cards)
        report["products"].extend(chosen)
        report["categories"].append({
            "slug": slug, "name": label,
            "topildi": len(cards), "olindi": len(chosen),
            "juftlik": sum(1 for c in chosen
                           if c["inn"] and sum(1 for x in chosen
                                               if (x["inn"] or "").lower() == c["inn"].lower()) > 1),
        })
        print(f"  {label:<26} topildi {len(cards):>3} → olindi {len(chosen)}")
        time.sleep(0.6)

    try:
        showcase, arzon_cats = arzon_home()
        report["arzon_showcase"] = showcase
        report["arzon_katalog"] = arzon_cats
        print(f"  ArzonApteka vitrinasi      {len(showcase)} → {len(report['arzon_showcase'])}")
        print(f"  ArzonApteka kategoriya     {len(arzon_cats)}")
    except Exception as e:                                      # noqa: BLE001
        print("  arzonapteka xato:", e)

    prods = report["products"]
    report["meta"].update({
        "jami_mahsulot": len(prods),
        "xpni_bor": sum(1 for p in prods if p["inn"]),
        "narxi_bor": sum(1 for p in prods if p["price_from_som"]),
        "mahalliy": sum(1 for p in prods if p["local"]),
        "import": sum(1 for p in prods if p["local"] is False),
    })
    fp = os.path.join(OUT, "catalog.json")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    sz = os.path.getsize(fp) / 1024
    print(f"\nyozildi: {fp}  ({sz:.1f} KB)")
    print(f"  mahsulot {len(prods)} | XPN {report['meta']['xpni_bor']} | "
          f"narx {report['meta']['narxi_bor']} | mahalliy {report['meta']['mahalliy']}")


if __name__ == "__main__":
    main()
