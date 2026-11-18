"""MllyMed B2B API — Shifokor, Dorixona va Zavodlar uchun Xizmatlar."""
from __future__ import annotations

from typing import Any


def handle_b2b_get(bridge: Any, path: str, query: dict, role: str) -> tuple[dict | None, int]:
    """B2B GET so'rovlarini qayta ishlash."""
    # Shifokorlar ro'yxati
    if path in ("/api/b2b/doctors", "/api/doctors"):
        return bridge.doctors(), 200

    # Barcha qabullar
    if path in ("/api/b2b/appointments", "/api/appointments"):
        return {"items": bridge.all_appointments()}, 200

    # Bemor retseptlari
    if path in ("/api/b2b/prescriptions", "/api/prescriptions"):
        sid = (query.get("sid") or ["demo"])[0]
        return {"items": bridge.prescriptions(sid)}, 200

    # Dorixona uchun kutilayotgan retseptlar navbati
    if path in ("/api/b2b/prescriptions/queue", "/api/prescriptions/queue"):
        if role not in ("pharmacist", "admin"):
            return {"error": "Faqat farmatsevt yoki admin uchun ruxsat etilgan"}, 403
        return {"items": bridge.queue()}, 200

    # Zavod va Admin bozor tahlili
    if path in ("/api/b2b/analytics", "/api/analytics"):
        return bridge.analytics(), 200

    # Tizim audit jurnali
    if path in ("/api/b2b/audit", "/api/audit"):
        if role != "admin":
            return {"error": "Faqat admin uchun ruxsat etilgan"}, 403
        limit = int((query.get("limit") or ["50"])[0] or 50)
        return {"items": bridge.audit(limit=limit)}, 200

    return None, 404


def handle_b2b_post(bridge: Any, path: str, body: dict, role: str, user: str) -> tuple[dict | None, int]:
    """B2B POST so'rovlarini qayta ishlash."""
    # Shifokor: XPN bo'yicha retsept loyihasi
    if path in ("/api/b2b/prescriptions", "/api/prescriptions"):
        if role != "doctor":
            return {"error": "Faqat shifokor retsept yoza oladi"}, 403
        res = bridge.draft_prescription(
            doctor_id=user,
            patient=body.get("patient") or "demo",
            inn=body.get("inn") or "",
            days=int(body.get("days") or 7)
        )
        return res, 200

    # Shifokor: Retseptni raqamli imzolash
    if path in ("/api/b2b/prescriptions/sign", "/api/prescriptions/sign"):
        if role != "doctor":
            return {"error": "Faqat shifokor imzolay oladi"}, 403
        rx_id = body.get("id") or ""
        return bridge.sign_prescription(rx_id, user), 200

    # Dorixona: Dori tarqatish (dispense)
    if path in ("/api/b2b/prescriptions/dispense", "/api/prescriptions/dispense"):
        if role != "pharmacist":
            return {"error": "Faqat farmatsevt dori bera oladi"}, 403
        rx_id = body.get("id") or ""
        inn = body.get("inn") or None
        pharmacy_id = body.get("pharmacy_id") or "apteka_1"
        return bridge.dispense(rx_id, pharmacy_id=pharmacy_id, inn=inn, actor=user), 200

    return None, 404
