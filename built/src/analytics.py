"""Analitika — mahsulot paneli uchun haqiqiy raqamlar.

Hech narsa taxmin qilinmaydi: har ko'rsatkich katalog va reyestrdan
hisoblanadi. `data_quality` — ma'lumotning **yo'qligi** ham ko'rsatkich.
"""
from __future__ import annotations

import statistics

from . import apteka, paths

paths.ensure_core()

from core import registry  # noqa: E402


def _median(xs: list[float]) -> float | None:
    return round(statistics.median(xs), 1) if xs else None


def overview() -> dict:
    rows = apteka.linked()
    with_inn = [p for p in rows if p.get("has_inn")]
    priced = [p for p in with_inn if p.get("price_from_som")]

    # XPN bo'yicha guruhlar
    groups: dict[str, list[dict]] = {}
    for p in with_inn:
        groups.setdefault(p["canon_inn"] or p["inn_key"], []).append(p)
    top = sorted(groups.items(), key=lambda kv: len(kv[1]), reverse=True)[:10]

    # Mahalliy/import narx pariteti (faqat juftlik bor XPN lar)
    parity, expensive = [], 0
    for key, group in groups.items():
        loc = [p["price_from_som"] for p in group if p.get("local") is True
               and p.get("price_from_som")]
        imp = [p["price_from_som"] for p in group if p.get("local") is False
               and p.get("price_from_som")]
        if not loc or not imp:
            continue
        lo, hi = min(loc), min(imp)
        chk = apteka.price_check(group)
        if chk.get("holat") == "80% dan qimmat":
            expensive += 1
        parity.append({"inn": key, "local_min": lo, "import_min": hi,
                       "diff_pct": round((hi - lo) / hi * 100, 1),
                       "check": chk.get("holat")})

    cov = apteka.coverage()
    st = registry.stats()
    cat = apteka.stats()
    local_n = sum(1 for p in with_inn if p.get("local") is True)
    import_n = sum(1 for p in with_inn if p.get("local") is False)
    unknown_n = sum(1 for p in with_inn if p.get("local") is None)

    return {
        "catalog": {
            "products": len(rows),
            "with_inn": len(with_inn),
            "without_inn": len(rows) - len(with_inn),
            "inn_groups": cat["inn_groups"],
            "sellers": cat["sellers"],
            "categories": len({p["category"] for p in rows if p.get("category")}),
            "priced": len(priced),
            "local": local_n,
            "import": import_n,
            "unknown_origin": unknown_n,
        },
        "registry": {
            "drugs": st.get("drugs"),
            "inn_groups": st.get("inn_groups"),
            "referent_prices": st.get("referent_prices"),
            "price_coverage_pct": st.get("price_coverage_pct"),
            "linked_inn": cov["inn_in_registry"],
            "link_exact": cov["link_exact"],
            "link_fuzzy": cov["link_fuzzy"],
            "link_none": cov["link_none"],
            "link_pct": round(100 * cov["inn_in_registry"] / cov["inn_total"], 1)
            if cov["inn_total"] else 0.0,
        },
        "parity": {
            "groups_with_both": len(parity),
            "above_80": expensive,
            "median_diff_pct": _median([p["diff_pct"] for p in parity]),
            "examples": sorted(parity, key=lambda p: p["diff_pct"], reverse=True)[:5],
        },
        "top_inn": [
            {"inn": k, "products": len(v),
             "local": sum(1 for p in v if p.get("local") is True),
             "import": sum(1 for p in v if p.get("local") is False),
             "min_price": min((p["price_from_som"] for p in v
                               if p.get("price_from_som")), default=None)}
            for k, v in top
        ],
        "data_quality": {
            "missing_price_pct": round(100 * (len(with_inn) - len(priced))
                                       / len(with_inn), 1) if with_inn else 0.0,
            "missing_inn_pct": round(100 * (len(rows) - len(with_inn))
                                     / len(rows), 1) if rows else 0.0,
            "unknown_origin_pct": round(100 * unknown_n / len(with_inn), 1)
            if with_inn else 0.0,
            "arzon_without_inn": sum(1 for p in rows
                                     if p["source"] == "arzonapteka.uz"),
        },
    }


def checks() -> list[dict]:
    """Analitika ichki izchilligi — UI va testlar uchun."""
    a = overview()
    c, r = a["catalog"], a["registry"]
    out = [
        {"name": "mahsulot = XPN bilan + XPN siz",
         "ok": c["products"] == c["with_inn"] + c["without_inn"]},
        {"name": "mahsulot ≥ 288 (kengaytirilgan katalog)",
         "ok": c["products"] >= 288},
        {"name": "narxli ≤ XPN bilan",
         "ok": c["priced"] <= c["with_inn"]},
        {"name": "mahalliy + import + noma'lum = XPN bilan",
         "ok": c["local"] + c["import"] + c["unknown_origin"] == c["with_inn"]},
        {"name": "reyestr 46 079 dori",
         "ok": r["drugs"] == 46079},
        {"name": "link_pct 0–100",
         "ok": 0 <= r["link_pct"] <= 100},
    ]
    return out
