"""Davlat reyestri ustidagi qidiruv va «ishonch kartasi».

Ma'lumot: `data/` — 46 079 reyestr yozuvi, 2 941 XPN guruhi,
12 423 referent narx, 538 chegara narx (maxSalePrice).

Muhim halollik qoidalari:
  • narx — 3735-son bo'yicha CHEGARA narx, dorixonadagi real narx emas;
  • BE hisoboti ochiq emas → «ma'lum emas», taxmin qilinmaydi;
  • GTIN/QR kod ochiq API da yo'q → «tekshirilmadi»;
  • bir xil doza/shakl bo'lmasa, narxlar to'g'ridan-to'g'ri solishtirilmaydi.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from . import evidence, sources
from .text import norm, tokens

DATA = Path(__file__).resolve().parent.parent / "data"

FORM_UZ = {
    "таблетки": "tabletka", "таблетки шипучие": "tabletka (shishuvchan)",
    "капсулы": "kapsula", "раствор": "eritma", "спрей": "sprey",
    "суспензия": "suspenziya", "мазь": "malham", "крем": "krem",
    "капли": "tomchi", "порошок": "poroshok", "сироп": "sirop",
    "гель": "gel", "свечи": "shamcha", "эмульсия": "emulsiya",
    "концентрат": "konsentrat", "инъекции": "in'ektsiya", "драже": "draje",
    "гранулы": "granula", "лиофилизат": "liofilizat", "настойка": "damlama",
}


FORM_PREF = {"таблетки": 0, "капсулы": 1, "таблетки шипучие": 2,
             "драже": 3, "суспензия": 4, "сироп": 5, "капли": 6,
             "спрей": 7, "мазь": 8, "крем": 9, "гель": 10,
             "раствор": 12, "концентрат": 13, "инъекции": 14}


@dataclass(frozen=True)
class Candidate:
    id: int
    name: str
    inn: str
    local: bool
    form: str
    strength: str
    country: str
    score: int
    has_price: bool

    def line(self) -> str:
        mark = "mahalliy" if self.local else "import"
        price = " · narx bor" if self.has_price else ""
        return (f"{self.name} — {self.strength or '—'}, "
                f"{form_uz(self.form)} · {mark}{price}")


def form_uz(form: str) -> str:
    f = (form or "").strip().lower()
    return FORM_UZ.get(f, form or "shakl ko'rsatilmagan")


@lru_cache(maxsize=1)
def _db() -> dict:
    def read(name, default):
        try:
            return json.loads((DATA / name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default

    rows = read("drugs.json", [])
    by_id = {r[0]: r for r in rows}
    # Qidiruv uchun normalizatsiya bir marta (46 079 × 2 norm — sekin bo'lardi)
    nrows = [(r[0], norm(r[1]), norm(r[2]), r[4]) for r in rows]
    return {
        "rows": rows,
        "nrows": nrows,
        "by_id": by_id,
        "inn": read("inn.json", {}),
        "ref": read("refprice.json", {}),
        "det": read("detail.json", {}),
        "mini": read("mini.json", []),
        "aliases": read("aliases.json", {}),
        "stats": read("stats.json", {}),
    }


def stats() -> dict:
    return _db()["stats"]


def _row_dict(r: list) -> dict:
    return {
        "id": r[0], "name": r[1], "full": r[2], "inn": r[3], "inn_key": r[4],
        "form": r[5], "strength": r[6], "country": r[7], "manufacturer": r[8],
        "reg": r[9], "local": bool(r[10]), "atc": r[11], "rx": bool(r[12]),
    }


def _score(target: str, name: str, full: str, inn: str) -> int:
    if not target:
        return 0
    if name == target:
        return 100
    if inn == target:
        return 99
    if name.startswith(target) and len(target) >= 4:
        return 92
    if inn.startswith(target) and len(target) >= 4:
        return 90
    if target in name:
        return 82
    if target in inn:
        return 74
    if target in full:
        return 66
    qt = [t for t in tokens(target) if len(t) >= 3]
    if qt and all(t in name or t in inn or t in full for t in qt):
        return 58
    if len(target) >= 6:
        from .text import fuzzy_key
        fa, fb = fuzzy_key(target), fuzzy_key(name)
        if fa and fb.startswith(fa) and len(fa) >= 5:
            return 50
    return 0


def search(query: str, limit: int = 8) -> list[Candidate]:
    db = _db()
    q = norm(query)
    if not q:
        return []
    alias = db["aliases"].get(q)
    if alias:
        q = norm(alias)

    scored: list[tuple[int, list]] = []
    for did, nn, nf, inn in db["nrows"]:
        s = _score(q, nn, nf, inn)
        if s:
            scored.append((s, db["by_id"][did]))
    if not scored:
        return []
    # Eng ko'p ishlatiladigan shakl birinchi (tabletka > eritma), keyin narx.
    scored.sort(key=lambda x: (-x[0],
                               FORM_PREF.get((x[1][5] or "").strip().lower(), 11),
                               not (str(x[1][0]) in db["ref"]),
                               not x[1][10], x[1][1]))
    out, seen = [], set()
    for s, r in scored:
        key = (norm(r[1]), norm(r[6]))
        if key in seen:
            continue
        seen.add(key)
        out.append(Candidate(r[0], r[1], r[3], bool(r[10]), r[5], r[6],
                             r[7], s, str(r[0]) in db["ref"]))
        if len(out) >= limit:
            break
    return out


def resolve(query: str) -> dict:
    db = _db()
    q = norm(query)
    alias = db["aliases"].get(q)
    cands = search(query, limit=8)
    if not cands:
        return {"status": "none", "alias": alias, "candidates": []}
    if cands[0].score >= 92 or (alias and cands):
        return {"status": "ok", "alias": alias, "candidates": cands,
                "drug": _row_dict(db["by_id"][cands[0].id])}
    return {"status": "ambiguous", "alias": alias, "candidates": cands}


CURRENCY = {"узбекский сум": "so'm", "сум": "so'm", "so'm": "so'm",
            "доллар сша": "USD", "dollar": "USD", "доллар": "USD",
            "евро": "EUR", "evro": "EUR", "yevro": "EUR",
            "российский рубль": "RUB", "rubl": "RUB", "рубль": "RUB"}


def cur_name(c: str | None) -> str:
    return CURRENCY.get((c or "").strip().lower(), (c or "").strip())


def _price_line(drug_id: int) -> dict | None:
    db = _db()
    r = db["ref"].get(str(drug_id))
    if not r:
        return None
    return {"price": r[0], "wholesale": r[1], "retail": r[2], "base": r[3],
            "currency": cur_name(r[4]), "rx": r[5], "date": r[6],
            "trademark": r[7]}


def _limit_line(drug_id: int) -> dict | None:
    db = _db()
    d = db["det"].get(str(drug_id))
    if not d:
        return None
    return {"max": d[0], "currency": cur_name(d[1]), "retail": d[2],
            "wholesale": d[3], "date": d[4], "substances": d[5],
            "package": d[6], "imgs": d[7]}


def group(inn_key: str) -> dict | None:
    return _db()["inn"].get(inn_key)


def group_prices(inn_key: str) -> dict:
    """Guruh bo'yicha narx statistikasi (turli doza — faqat ma'lumot uchun)."""
    db = _db()
    g = db["inn"].get(inn_key)
    if not g:
        return {"n": 0, "local": 0, "import": 0, "priced": 0}
    local, imp = [], []
    for i in g["ids"]:
        r = db["ref"].get(str(i))
        if not r or not r[2]:
            continue
        row = db["by_id"].get(i)
        (local if (row and row[10]) else imp).append(float(r[2]))
    return {
        "n": g["n"], "local": g["local"], "import": g["import"],
        "priced": len(local) + len(imp),
        "local_min": min(local) if local else None,
        "import_min": min(imp) if imp else None,
    }


def same_form_prices(row: list) -> dict:
    """Bir xil shakl + doza ichida mahalliy/import narxlarini solishtirish.

    Faqat shu holatda farq foizini chiqarish halol: turli dozalarni
    solishtirish noto'g'ri bo'lardi.
    """
    db = _db()
    g = db["inn"].get(row[4])
    if not g:
        return {"n": 0}
    key = (norm(row[5]), norm(row[6]))
    local, imp, ids = [], [], []
    for i in g["ids"]:
        r2 = db["by_id"].get(i)
        if not r2 or (norm(r2[5]), norm(r2[6])) != key:
            continue
        ids.append(i)
        pr = db["ref"].get(str(i))
        if pr and pr[2]:
            (local if r2[10] else imp).append(float(pr[2]))
    diff = None
    if local and imp:
        lo, hi = min(local), min(imp)
        if hi > 0:
            diff = round(100 * (hi - lo) / hi, 1)
    return {"n": len(ids), "local": len(local), "import": len(imp),
            "local_min": min(local) if local else None,
            "import_min": min(imp) if imp else None, "diff_pct": diff}


def card(drug_id: int) -> dict:
    db = _db()
    r = db["by_id"].get(int(drug_id))
    if not r:
        return {}
    d = _row_dict(r)
    d["form_uz"] = form_uz(d["form"])
    d["price"] = _price_line(d["id"])
    d["limit"] = _limit_line(d["id"])
    d["group"] = group_prices(r[4])
    d["same"] = same_form_prices(r)
    d["inn_display"] = (db["inn"].get(r[4]) or {}).get("name", r[3])
    d["sources"] = registry_sources(d["id"])
    return d


def market_examples(inn_key: str, limit: int = 4) -> list[dict]:
    """Guruhdagi eng arzon mahalliy va import variantlari (dorixona narxi)."""
    db = _db()
    out = []
    for m in db["mini"]:
        if norm(m.get("inn") or "") == inn_key:
            out.append(m)
    out.sort(key=lambda m: (m.get("price") or 10 ** 9))
    return out[:limit]


def compare_pair(inn_key: str, local_min: float | None,
                 import_min: float | None, diff: float | None) -> dict:
    """Narx farqi uchun hujjatli izoh (3735-son F08/F09)."""
    pm = evidence.price_model()
    return {
        "local": local_min, "import": import_min, "diff_pct": diff,
        "rule_80": evidence.cite("F09", short=True),
        "formula_local": evidence.cite("F08", short=True),
        "formula_import": evidence.cite("F07", short=True),
        "example": pm.get("example", {}),
        "note": pm.get("note", ""),
    }


def registry_sources(drug_id: int) -> list[tuple[str, str]]:
    st = stats()
    return [
        ("Davlat dori reyestri", evidence.REGISTRY_HUMAN),
        ("Reyestr API", evidence.REGISTRY_URL + f" · drugId={drug_id}"),
        ("Referent narx (3735-son)", evidence.REF_URL),
        ("Bioekvivalentlik (738-son)", evidence.BE_URL),
        ("Markirovka (149-son)", evidence.MARK_URL),
        ("GMP reyestri (ochiq HTML)", sources.GMP_LOCAL),
        ("Ochiq ma'lumotlar (mpa.uz)", sources.OPEN_DATA),
    ]
