"""Bridge — O'RINDOR agenti + dorixona + mini DMED ni bitta javobga yig'adi.

Muhim chegara: bridge **qaror qabul qilmaydi**. U yadro agentining matnini
o'zgartirmaydi (u allaqachon `validate_*` dan o'tgan), faqat yoniga JSON
qo'shadi:
  • karta bo'lsa   → dorixonadagi takliflar + 80% proxy tekshiruvi;
  • triaj bo'lsa   → shifokorlar va bo'sh vaqtlar (navbat yaratilmaydi);
  • retsept oqimi  → faqat UI dagi "shifokor" tugmasi orqali (simulyatsiya).
"""
from __future__ import annotations

import threading

from . import analytics, apteka, dmed, paths

paths.ensure_core()

from agent import Agent  # noqa: E402
from core.session import Session  # noqa: E402
from core import registry, render  # noqa: E402


class Bridge:
    def __init__(self, dmed_state=None):
        self.agent = Agent()
        self.dmed = dmed.DMed(dmed_state)
        self.sessions: dict[str, Session] = {}
        self.lock = threading.Lock()

    def session(self, sid: str) -> Session:
        with self.lock:
            if sid not in self.sessions:
                self.sessions[sid] = Session()
            return self.sessions[sid]

    # ── suhbat
    def chat(self, sid: str, text: str) -> dict:
        s = self.session(sid)
        reply = self.agent.respond(s, text)

        out = {"sid": sid, "reply": reply, "stage": s.stage,
               "mode": s.mode, "synthetic": True}
        if s.card:
            out["card"] = s.card
            inn = s.card.get("inn_key") or s.card.get("inn") or ""
            out["apteka"] = apteka.summary(inn) if inn else None
        if s.stage == "routed" and s.guess:
            out["triage"] = {"specialist": s.guess.specialist,
                             "label": s.guess.label,
                             "urgency": s.urgency.text,
                             "when": s.urgency.when}
            out["dmed"] = self.dmed.suggest(s.guess.specialist)
        return out

    # ── DMED: foydalanuvchi harakati
    def slots(self, doctor_id: str) -> list[dict]:
        return self.dmed.free_slots(doctor_id)

    def suggest(self, specialist: str) -> dict:
        return self.dmed.suggest(specialist)

    def book_request(self, sid: str, doctor_id: str, slot: str) -> dict:
        """Foydalanuvchi vaqtni tanladi — hali TASDIQLANMAGAN so'rov."""
        return self.dmed.create_appointment(sid, doctor_id, slot)

    def book_confirm(self, sid: str, appt_id: str) -> dict:
        return self.dmed.confirm_appointment(sid, appt_id, actor="user")

    def book_cancel(self, sid: str, appt_id: str) -> dict:
        return self.dmed.cancel_appointment(sid, appt_id, actor="user")

    def state(self, sid: str) -> dict:
        return self.dmed.state_for(sid)

    def audit(self, limit: int = 50) -> list[dict]:
        return self.dmed.audit(limit)

    # ── retsept oqimi (simulyatsiyadagi shifokor paneli)
    def prescription_draft(self, sid: str, inn: str, doctor_id: str) -> dict:
        rx = self.dmed.create_prescription(sid, inn, doctor_id)
        return {"prescription": rx, "registry": apteka.registry_view(inn),
                "apteka": apteka.summary(inn)}

    def prescription_sign(self, rx_id: str) -> dict:
        """Ataylab alohida nom: faqat simulyatsiyadagi shifokor imzolaydi."""
        rx = self.dmed.sign_prescription(rx_id, actor="doctor_sim")
        return {"prescription": rx,
                "apteka": apteka.summary(rx["inn_key"])}

    def prescription_options(self, inn: str) -> dict:
        return {"registry": apteka.registry_view(inn),
                "apteka": apteka.summary(inn)}

    def dispense(self, rx_id: str, offer_id: str) -> dict:
        """Farmatsevt dorini beradi — taklif katalogdan, XPN mosligi tekshiriladi."""
        offer = next((p for p in apteka.linked() if p["id"] == offer_id), None)
        if not offer:
            raise ValueError("Taklif katalogda topilmadi")
        order = self.dmed.dispense(rx_id, offer, actor="pharmacist",
                                   role="pharmacist")
        return {"order": order, "prescription": self.dmed.prescriptions(order["patient"])}

    def prescriptions(self, sid: str) -> list[dict]:
        return self.dmed.prescriptions(sid)

    # ── ma'lumot
    def stats(self) -> dict:
        return {"registry": registry.stats(),
                "apteka": {**apteka.stats(), **apteka.coverage()},
                "dmed": self.dmed.stats()}

    def analytics(self) -> dict:
        a = analytics.overview()
        a["dmed"] = self.dmed.stats()
        a["checks"] = analytics.checks()
        return a

    def search(self, q: str, limit: int = 12) -> list[dict]:
        return apteka.search(q, limit)

    # ── katta mahsulot API si
    def card_lookup(self, q: str) -> dict:
        """Sessiyasiz karta: qidiruv natijasi + dorixona takliflari."""
        res = registry.resolve(q)
        out = {"query": q, "status": res["status"],
               "alias": res.get("alias"),
               "candidates": [{"id": c.id, "name": c.name, "line": c.line()}
                              for c in res["candidates"]]}
        if res["status"] == "ok":
            c = registry.card(res["drug"]["id"])
            out["card"] = c
            out["text"] = render.card_text(c)
            inn = c.get("inn_key") or c.get("inn") or ""
            out["apteka"] = apteka.summary(inn) if inn else None
        return out

    def catalog(self, q: str = "", page: int = 1, size: int = 20,
                local: str | None = None, category: str | None = None) -> dict:
        from core.text import norm as n
        rows = apteka.linked()
        # Milliy ustuvorlik: mahalliy takliflar ro'yxat boshida
        rows.sort(key=lambda p: (p.get("local") is not True,
                                 p.get("price_from_som") is None,
                                 p.get("price_from_som") or 0,
                                 n(p.get("name") or "")))
        qq = n(q).strip()
        if qq:
            rows = [p for p in rows
                    if qq in n(p.get("name")) or qq in n(p.get("inn"))
                    or qq in n(p.get("manufacturer"))]
        if local in ("local", "import", "unknown"):
            want = {"local": True, "import": False, "unknown": None}[local]
            rows = [p for p in rows if p.get("local") is want]
        if category:
            rows = [p for p in rows if p.get("category") == category]
        total = len(rows)
        size = max(1, min(size, 100))
        page = max(1, page)
        start = (page - 1) * size
        items = []
        for p in rows[start:start + size]:
            items.append({k: p.get(k) for k in
                          ("id", "name", "inn", "canon_inn", "manufacturer",
                           "country", "local", "price_from_som", "pharmacies",
                           "seller", "category", "source", "url", "rx")})
        cats: dict[str, int] = {}
        for p in apteka.linked():
            if p.get("category"):
                cats[p["category"]] = cats.get(p["category"], 0) + 1
        return {"total": total, "page": page, "size": size, "items": items,
                "facets": {"categories": cats}}

    def arzon(self, limit: int = 24, category: str | None = None,
              local: str | None = None) -> dict:
        """Arzon apteka vitrinasi — katalogdan hisoblangan, taxmin qo'shilmaydi."""
        return apteka.arzon(limit=limit, category=category, local=local)

    def doctors(self) -> dict:
        return {"doctors": dmed.DOCTORS, "clinics": dmed.CLINICS,
                "synthetic": True, "note": dmed.SYNTHETIC_NOTE}

    def all_appointments(self) -> list[dict]:
        return self.dmed.all_appointments()

    def queue(self) -> list[dict]:
        return self.dmed.prescription_queue()

    def all_prescriptions(self) -> list[dict]:
        return self.dmed.all_prescriptions()
