"""Dalil qatlami — lex.uz faktlari va manba havolalari.

Qoida: agent og'zidan chiqqan har bir huquqiy da'vo yonida fakt raqami
(F01…) va URL bo'ladi. Faktlar `data/facts.json` dan o'qiladi; matn
o'zgartirilmaydi.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

REGISTRY_URL = "https://api.mpa.uz/drug-catalog-api/v2/drugs/portal/search"
REGISTRY_HUMAN = "https://uzpharm-control.uz/uz/registry/drugs"
REF_URL = "https://lex.uz/uz/docs/-7952162"
BE_URL = "https://lex.uz/uz/docs/-7853907"
MARK_URL = "https://lex.uz/uz/docs/-5936145"
PF_URL = "https://lex.uz/uz/docs/-8076453"
QUEUE_URL = "https://my.gov.uz/oz/queue-doctor/"


@lru_cache(maxsize=1)
def load() -> dict:
    try:
        return json.loads((DATA / "facts.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"facts": [], "price_model": {}}


def facts() -> list[dict]:
    return load().get("facts", [])


def fact(fid: str) -> dict | None:
    for f in facts():
        if f.get("id") == fid:
            return f
    return None


def cite(fid: str, short: bool = False) -> str:
    f = fact(fid)
    if not f:
        return ""
    if short:
        return f"{f['doc']}-son ({f['date']}) · {f['url']}"
    return f"«{f['claim']}» — {f['doc']}-son, {f['date']}, {f['url']}"


def price_model() -> dict:
    return load().get("price_model", {})


def facts_meta() -> dict:
    return load().get("meta", {})
