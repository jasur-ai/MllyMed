"""MllyMed B2C API — Bemorlar va Aholi uchun Xizmatlar."""
from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, unquote


def handle_b2c_get(bridge: Any, path: str, query: dict) -> tuple[dict | None, int]:
    """B2C GET so'rovlarini qayta ishlash."""
    # Katalog qidiruvi
    if path in ("/api/b2c/catalog", "/api/catalog"):
        q = (query.get("q") or [""])[0]
        page = int((query.get("page") or ["1"])[0] or 1)
        size = int((query.get("size") or ["20"])[0] or 20)
        local = (query.get("local") or [None])[0]
        category = (query.get("category") or [None])[0]
        return bridge.catalog(q=q, page=page, size=size, local=local, category=category), 200

    # Dori kartochkasi va 80% mahalliy analog tahlili
    if path in ("/api/b2c/card", "/api/card"):
        q = (query.get("q") or [""])[0]
        return bridge.card_lookup(q), 200

    # Arzon narxlar vitrinasi
    if path in ("/api/b2c/arzon", "/api/arzon"):
        limit = int((query.get("limit") or ["24"])[0] or 24)
        category = (query.get("category") or [None])[0]
        local = (query.get("local") or [None])[0]
        return bridge.arzon(limit=limit, category=category, local=local), 200

    # XPN umumiy ma'lumot
    if path.startswith("/api/b2c/inn/") or path.startswith("/api/inn/"):
        prefix = "/api/b2c/inn/" if path.startswith("/api/b2c/inn/") else "/api/inn/"
        inn = unquote(path.split(prefix, 1)[1])
        from built.src import apteka
        return apteka.summary(inn), 200

    # Bemor holati (navbatlar va retseptlar)
    if path in ("/api/b2c/state", "/api/state"):
        sid = (query.get("sid") or ["demo"])[0]
        return bridge.state(sid), 200

    # DMED bo'sh vaqtlar
    if path in ("/api/b2c/slots", "/api/dmed/slots"):
        doc_id = (query.get("doctor") or [""])[0]
        return {"slots": bridge.slots(doc_id)}, 200

    # DMED tavsiya
    if path in ("/api/b2c/doctors/suggest", "/api/dmed/doctors"):
        spec = (query.get("specialist") or ["terapevt"])[0]
        return bridge.suggest(spec), 200

    return None, 404


def handle_b2c_post(bridge: Any, path: str, body: dict) -> tuple[dict | None, int]:
    """B2C POST so'rovlarini qayta ishlash."""
    # MllyMed AI triaj va maslahat muloqoti
    if path in ("/api/b2c/chat", "/api/chat"):
        sid = body.get("sid") or "demo"
        text = (body.get("text") or "").strip()
        return bridge.chat(sid, text), 200

    # DMED navbat olish
    if path in ("/api/b2c/book", "/api/dmed/book"):
        res = bridge.book(
            patient=body.get("patient") or "demo",
            doctor_id=body.get("doctor_id") or "",
            slot=body.get("slot") or "",
            symptom=body.get("symptom") or ""
        )
        return res, 200

    return None, 404
