"""ArzonApteka + apteka.uz — bitta dorixona katalogi ustidagi tekshiruv.

Bu modul **sotmaydi**: u narxni qonun (3735-son, F09) bo'yicha tekshiradi va
`mos / 80% dan qimmat / tekshirib bo'lmadi` deb hukm chiqaradi.

Halollik qoidalari (kodda):
  • ArzonApteka vitrinasida XPN yo'q → `has_inn=False`, almashtirishga
    qo'shilmaydi (README: 20 yozuv XPN siz);
  • `local` faqat ma'lum bo'lsa True/False, aks holda None — taxmin yo'q;
  • referent narx reyestri yopiq → 80% tekshiruvi chakana narx bo'yicha
    **proxy**, buni javobda ochiq yozamiz.
"""
from __future__ import annotations

import difflib
import json
import statistics
from functools import lru_cache

from . import paths

paths.ensure_core()

from core.text import norm as _core_norm  # noqa: E402
from core import registry  # noqa: E402

CATALOG = paths.DATA / "apteka_catalog.json"


def norm(s: str) -> str:
    return _core_norm(s or "")


@lru_cache(maxsize=1)
def _inn_index() -> tuple[str, ...]:
    """Reyestrdagi barcha XPN kalitlari — imlo farqini bog'lash uchun."""
    return tuple(sorted(registry._db()["inn"].keys()))       # noqa: SLF001


@lru_cache(maxsize=4096)
def canon_inn(inn: str) -> tuple[str, str, float]:
    """Katalogdagi XPN ni reyestr kalitiga bog'laydi.

    `parasetamol` → `paratsetamol` kabi imlo farqlari bor (manba saytlari
    o'zicha yozadi). Bog'lanish usuli va ishonchi qaytariladi — taxmin
    yashirilmaydi: `none` bo'lsa, XPN reyestrda topilmagan deb hisoblanadi.
    """
    k = norm(inn).strip()
    if not k:
        return "", "none", 0.0
    idx = _inn_index()
    if k in idx:
        return k, "exact", 1.0
    m = difflib.get_close_matches(k, idx, n=1, cutoff=0.90)
    if m:
        score = round(difflib.SequenceMatcher(None, k, m[0]).ratio(), 3)
        return m[0], "fuzzy", score
    # Tuz qo'shimchasi farqi: «bromgeksin gidroxloridi» ↔ «bromgeksin».
    # Faqat qisqa tomoni ≥8 belgi bo'lsa — tasodifiy moslikdan qochish uchun.
    if len(k) >= 8:
        cands = [x for x in idx
                 if (k in x or x in k) and min(len(k), len(x)) >= 8]
        if cands:
            best = max(cands, key=lambda x: difflib.SequenceMatcher(None, k, x).ratio())
            score = round(difflib.SequenceMatcher(None, k, best).ratio(), 3)
            if score >= 0.75:
                return best, "contains", score
    return k, "none", 0.0


@lru_cache(maxsize=1)
def catalog() -> dict:
    try:
        return json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"meta": {"counts": {}}, "products": []}


def products() -> list[dict]:
    return catalog().get("products", [])


def meta() -> dict:
    return catalog().get("meta", {})


def stats() -> dict:
    st = dict(meta().get("counts", {}))
    st["sellers"] = len({p["seller"] for p in products() if p.get("seller")})
    return st


@lru_cache(maxsize=1)
def linked() -> list[dict]:
    """Mahsulotlar + reyestrga bog'lanish (`canon_inn`, usul, ishonch)."""
    out = []
    for p in products():
        q = dict(p)
        if p.get("inn"):
            c, method, score = canon_inn(p["inn"])
            q.update(canon_inn=c, link_method=method, link_score=score)
        else:
            q.update(canon_inn=None, link_method="none", link_score=0.0)
        out.append(q)
    return out


def search(q: str, limit: int = 20) -> list[dict]:
    q = norm(q).strip()
    if not q:
        return []
    hits = [p for p in linked()
            if q in norm(p.get("name")) or q in norm(p.get("inn"))
            or q in norm(p.get("manufacturer"))]
    hits.sort(key=lambda p: (p.get("price_from_som") is None,
                             p.get("price_from_som") or 0))
    return hits[:limit]


def by_inn(inn: str) -> list[dict]:
    """XPN guruhi: avval mahalliy muqobillar, keyin import, ichida narx bo'yicha.

    Milliy ustuvorlik — **tartib**, da'vo emas: mahalliy mahsulot importdan
    arzon yoki sifatli deb aytilmaydi, faqat ro'yxat boshida turadi.
    """
    c, _, _ = canon_inn(inn)
    if not c:
        return []
    out = [p for p in linked()
           if p.get("has_inn") and p.get("canon_inn") == c]
    rank = {True: 0, None: 1, False: 2}
    out.sort(key=lambda p: (rank.get(p.get("local"), 1),
                            p.get("price_from_som") is None,
                            p.get("price_from_som") or 0))
    return out


def price_check(group: list[dict]) -> dict:
    """3735-son F09 ning PROXY tekshiruvi (referent narx yopiq)."""
    loc = [p for p in group if p.get("local") is True and p.get("price_from_som")]
    imp = [p for p in group if p.get("local") is False and p.get("price_from_som")]
    if not loc or not imp:
        return {"holat": "tekshirib bo'lmadi",
                "sabab": "bir XPN ostida mahalliy va import narxi yetarli emas"}
    lo = min(p["price_from_som"] for p in loc)
    hi = min(p["price_from_som"] for p in imp)
    chegara = round(hi * 0.80)
    return {
        "holat": "mos" if lo <= chegara else "80% dan qimmat",
        "mahalliy_eng_arzon": lo,
        "import_eng_arzon": hi,
        "chegara_80": chegara,
        "farq_foiz": round((1 - lo / hi) * 100, 1) if hi else None,
        "izoh": "chakana narx proxy sifatida — referent narx reyestri yopiq",
    }


def registry_view(inn: str) -> dict:
    """Reyestr tomoni: guruh bormi, narx qamrovi qanday.

    XPN imlosi katalogdan farq qilishi mumkin — `canon_inn` orqali
    bog'lanadi. Bog'lanmasa «topilmadi» (taxmin yo'q).
    """
    canon, method, score = canon_inn(inn)
    g = registry.group(canon) if canon else None
    if not g or not g.get("ids"):
        return {"holat": "topilmadi", "inn": inn,
                "link": {"method": method, "score": score}}
    c = registry.card(g["ids"][0])
    grp = c.get("group") or {}
    return {
        "holat": "bor",
        "inn": c.get("inn"),
        "canon_inn": canon,
        "name": c.get("name"),
        "reg": c.get("reg"),
        "group_n": grp.get("n"),
        "group_local": grp.get("local"),
        "group_import": grp.get("import"),
        "priced": grp.get("priced"),
        "price": c.get("price"),
        "link": {"method": method, "score": score},
    }


def summary(inn: str, limit: int = 6) -> dict:
    """Karta yonidagi takliflar: mahalliy birinchi, keyin import."""
    group = by_inn(inn)
    canon, method, score = canon_inn(inn)
    return {
        "inn": inn,
        "canon_inn": canon,
        "link": {"method": method, "score": score},
        "count": len(group),
        "offers": group[:limit],
        "check": price_check(group) if group else
                 {"holat": "tekshirib bo'lmadi", "sabab": "dorixona katalogida yo'q"},
        "registry": registry_view(inn),
        "note": ("Narx — «X so'mdan» (dorixona emas, eng past taklif). "
                 "80% tekshiruvi proxy, referent narx reyestri yopiq."),
    }


def arzon(limit: int = 24, category: str | None = None,
          local: str | None = None) -> dict:
    """«Arzon apteka» vitrinasi: har XPN uchun eng past taklif va tejamkorlik.

    Tejamkorlik guruhdagi **median chakana narxga** nisbatan hisoblanadi — bu
    «X so'mdan» takliflar orasidagi farq, dorixona kassasidagi kafolatlangan
    tejash emas. Vitrina (XPN siz 20 yozuv) alohida qaytariladi: ular
    almashtirishga kirmaydi, faqat narx ko'rsatkichi.
    """
    rows = [p for p in linked() if p.get("price_from_som")]
    groups: dict[str, list[dict]] = {}
    for p in rows:
        if p.get("has_inn") and p.get("canon_inn"):
            groups.setdefault(p["canon_inn"], []).append(p)

    deals = []
    for key, group in groups.items():
        if len(group) < 2:
            continue
        ordered = sorted(group, key=lambda p: p["price_from_som"])
        cheapest = ordered[0]
        med = statistics.median(p["price_from_som"] for p in ordered)
        if not med:
            continue
        deals.append({
            "inn_key": key,
            "inn": cheapest.get("inn"),
            "name": cheapest.get("name"),
            "category": cheapest.get("category"),
            "price_from_som": cheapest["price_from_som"],
            "median_som": round(med),
            "savings_pct": round((1 - cheapest["price_from_som"] / med) * 100),
            "offers": len(group),
            "local": cheapest.get("local"),
            "manufacturer": cheapest.get("manufacturer"),
            "seller": cheapest.get("seller"),
            "url": cheapest.get("url"),
        })

    if category:
        deals = [d for d in deals if d.get("category") == category]
    if local in ("local", "import"):
        want = local == "local"
        deals = [d for d in deals if d.get("local") is want]
    deals.sort(key=lambda d: (-d["savings_pct"], d["price_from_som"]))

    vitrina = sorted(
        [p for p in products()
         if p.get("source") == "arzonapteka.uz" and p.get("price_from_som")],
        key=lambda p: p["price_from_som"])

    all_priced = [p for group in groups.values() for p in group
                  if p.get("price_from_som")]
    return {
        "deals": deals[:limit],
        "total_deals": len(deals),
        "vitrina": [{"id": p.get("id"), "name": p.get("name"),
                     "price_from_som": p.get("price_from_som"),
                     "manufacturer": p.get("manufacturer"),
                     "seller": p.get("seller"), "rx": p.get("rx"),
                     "url": p.get("url"), "has_inn": False}
                    for p in vitrina],
        "stats": {
            "groups": len(deals),
            "offers": len(all_priced),
            "max_savings_pct": max((d["savings_pct"] for d in deals), default=0),
            "median_savings_pct": round(statistics.median(
                [d["savings_pct"] for d in deals]), 1) if deals else 0,
            "min_price_som": min((d["price_from_som"] for d in deals), default=None),
            "vitrina": len(vitrina),
        },
        "categories": sorted({d["category"] for d in linked()
                              if d.get("category")}),
        "note": ("Narx — dorixona taklifi «X so'mdan», kassa narxi emas. "
                 "Tejamkorlik guruh medianasiga nisbatan. 80% qoidasi proxy."),
    }


def coverage() -> dict:
    """Katalog qamrovi: nechta XPN reyestrga bog'landi, qaysi usul bilan."""
    rows = [p for p in linked() if p.get("has_inn")]
    keys = {p["canon_inn"] for p in rows if p.get("link_method") != "none"}
    return {
        "inn_total": len({p["inn_key"] for p in rows}),
        "inn_in_registry": len(keys),
        "link_exact": sum(1 for p in rows if p["link_method"] == "exact"),
        "link_fuzzy": sum(1 for p in rows if p["link_method"] == "fuzzy"),
        "link_none": sum(1 for p in rows if p["link_method"] == "none"),
        "product_total": len(products()),
    }
