"""Mini DMED — **simulyatsiya**, lekin qoidalari haqiqiy (SQLite, rollar, audit).

Nima simulyatsiya: klinikalar, shifokorlar, navbat vaqtlari — sintetik.
Haqiqiy DMED API'siga bog'lanmagan.

Nima qat'iy (kodda majburlangan):
  1. Navbatni **agent tasdiqlamaydi** — faqat `role="patient"` / `actor="user"`.
  2. Retsept **XPN bo'yicha**; XPN davlat reyestrida bo'lmasa — rad.
  3. Retseptni faqat **shifokor** imzolaydi.
  4. Dorini faqat **farmatsevt** beradi (`dispense`) va faqat imzolangan
     retsept bo'yicha, faqat o'sha XPN taklifi bilan.
  5. Har amal `audit` jadvaliga yoziladi (kim, qaysi rol, nima).
"""
from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path

from . import paths

paths.ensure_core()

from core import registry  # noqa: E402

STATE = paths.RUNTIME / "dmed.db"

SYNTHETIC_NOTE = (
    "SIMULYATSIYA: klinika, shifokor va navbat vaqtlari sintetik. "
    "Haqiqiy DMED API'siga bog'lanmagan, hech narsa bron qilinmaydi."
)

CLINICS = [
    {"id": "c1", "name": "1-son shahar poliklinikasi", "district": "Chilonzor"},
    {"id": "c2", "name": "Yunusobod tibbiyot markazi", "district": "Yunusobod"},
    {"id": "c3", "name": "Mirzo Ulug'bek klinikasi", "district": "Mirzo Ulug'bek"},
]

DOCTORS = [
    {"id": "d01", "name": "A. Karimova", "specialist": "terapevt", "clinic": "c1", "exp": 12},
    {"id": "d02", "name": "B. Toshpulatov", "specialist": "terapevt", "clinic": "c2", "exp": 7},
    {"id": "d03", "name": "D. Nazarova", "specialist": "kardiolog", "clinic": "c1", "exp": 15},
    {"id": "d04", "name": "E. Yusupov", "specialist": "kardiolog", "clinic": "c3", "exp": 9},
    {"id": "d05", "name": "F. Rahimova", "specialist": "nevrolog", "clinic": "c2", "exp": 11},
    {"id": "d06", "name": "G. Sobirov", "specialist": "gastroenterolog", "clinic": "c1", "exp": 10},
    {"id": "d07", "name": "H. Ismoilova", "specialist": "pulmonolog", "clinic": "c3", "exp": 8},
    {"id": "d08", "name": "J. Abdullayev", "specialist": "endokrinolog", "clinic": "c2", "exp": 13},
    {"id": "d09", "name": "K. Mirzayeva", "specialist": "urolog", "clinic": "c1", "exp": 6},
    {"id": "d10", "name": "L. Qodirova", "specialist": "ginekolog", "clinic": "c2", "exp": 14},
    {"id": "d11", "name": "M. Sattorov", "specialist": "travmatolog", "clinic": "c3", "exp": 9},
    {"id": "d12", "name": "N. Xolmatov", "specialist": "lor", "clinic": "c1", "exp": 12},
    {"id": "d13", "name": "O. Yo'ldosheva", "specialist": "oftalmolog", "clinic": "c2", "exp": 16},
    {"id": "d14", "name": "P. Ergashev", "specialist": "dermatolog", "clinic": "c3", "exp": 7},
    {"id": "d15", "name": "R. Umarova", "specialist": "stomatolog", "clinic": "c1", "exp": 10},
    {"id": "d16", "name": "S. Aliyev", "specialist": "onkolog", "clinic": "c3", "exp": 18},
    {"id": "d17", "name": "T. Bekmurodov", "specialist": "psixiatr", "clinic": "c2", "exp": 11},
    {"id": "d18", "name": "U. Sharipova", "specialist": "ftiziatr", "clinic": "c1", "exp": 13},
    {"id": "d19", "name": "V. Tursunov", "specialist": "infektsionist", "clinic": "c2", "exp": 9},
    {"id": "d20", "name": "X. Jo'rayeva", "specialist": "allergolog", "clinic": "c3", "exp": 8},
    {"id": "d21", "name": "Y. Xasanov", "specialist": "revmatolog", "clinic": "c1", "exp": 12},
    {"id": "d22", "name": "Z. Norboyeva", "specialist": "nefrolog", "clinic": "c2", "exp": 10},
    {"id": "d23", "name": "A. G'aniyev", "specialist": "gematolog", "clinic": "c3", "exp": 14},
    {"id": "d24", "name": "B. Sultonova", "specialist": "pediatr", "clinic": "c1", "exp": 11},
    {"id": "d25", "name": "D. Mahmudov", "specialist": "jarroh", "clinic": "c2", "exp": 17},
    {"id": "d26", "name": "E. Rustamova", "specialist": "proktolog", "clinic": "c3", "exp": 9},
    {"id": "d27", "name": "F. Xudoyberdiyeva", "specialist": "mammolog", "clinic": "c1", "exp": 10},
]

_SPECIALIST_LABEL = {
    "terapevt": "Terapevt", "kardiolog": "Kardiolog", "nevrolog": "Nevrolog",
    "gastroenterolog": "Gastroenterolog", "pulmonolog": "Pulmonolog",
    "endokrinolog": "Endokrinolog", "urolog": "Urolog", "ginekolog": "Ginekolog",
    "travmatolog": "Travmatolog", "lor": "LOR", "oftalmolog": "Oftalmolog",
    "dermatolog": "Dermatolog", "stomatolog": "Stomatolog", "onkolog": "Onkolog",
    "psixiatr": "Psixiatr", "ftiziatr": "Ftiziatr", "infektsionist": "Infeksionist",
    "allergolog": "Allergolog", "revmatolog": "Revmatolog", "nefrolog": "Nefrolog",
    "gematolog": "Gematolog", "pediatr": "Pediatr", "jarroh": "Jarroh",
    "proktolog": "Proktolog", "mammolog": "Mammolog",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS appointments(
  id TEXT PRIMARY KEY, patient TEXT NOT NULL, doctor_id TEXT NOT NULL,
  specialist TEXT, slot TEXT NOT NULL, status TEXT NOT NULL,
  created_at TEXT, confirmed_at TEXT, confirmed_by TEXT);
CREATE UNIQUE INDEX IF NOT EXISTS ux_appt_slot
  ON appointments(doctor_id, slot)
  WHERE status IN ('requested','confirmed');
CREATE TABLE IF NOT EXISTS prescriptions(
  id TEXT PRIMARY KEY, patient TEXT NOT NULL, doctor_id TEXT NOT NULL,
  doctor TEXT, inn TEXT NOT NULL, inn_key TEXT NOT NULL, status TEXT NOT NULL,
  created_at TEXT, signed_at TEXT, signed_by TEXT);
CREATE TABLE IF NOT EXISTS orders(
  id TEXT PRIMARY KEY, rx_id TEXT NOT NULL, patient TEXT NOT NULL,
  pharmacy TEXT, offer_id TEXT, name TEXT, price INTEGER,
  status TEXT NOT NULL, created_at TEXT, dispensed_at TEXT);
CREATE TABLE IF NOT EXISTS audit(
  id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL,
  actor TEXT, role TEXT, action TEXT NOT NULL,
  entity TEXT, entity_id TEXT, payload TEXT);
"""


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _nid(prefix: str) -> str:
    return f"{prefix}-{secrets.token_hex(4)}"


def _h(*parts: str) -> int:
    return int(hashlib.sha256("|".join(parts).encode()).hexdigest()[:8], 16)


class DMed:
    def __init__(self, state_path: Path | None = None):
        self.path = Path(state_path or STATE)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self):
        c = sqlite3.connect(self.path, timeout=10)
        c.row_factory = sqlite3.Row
        try:
            yield c
            c.commit()
        finally:
            c.close()

    def _audit(self, c, actor: str, role: str, action: str,
               entity: str, entity_id: str, payload: dict) -> None:
        c.execute("INSERT INTO audit(at,actor,role,action,entity,entity_id,payload) "
                  "VALUES(?,?,?,?,?,?,?)",
                  (_now(), actor, role, action, entity, entity_id,
                   json.dumps(payload, ensure_ascii=False)))

    # ── shifokorlar / navbat
    def doctor(self, doctor_id: str) -> dict | None:
        return next((d for d in DOCTORS if d["id"] == doctor_id), None)

    def free_slots(self, doctor_id: str, days: int = 7) -> list[dict]:
        if not self.doctor(doctor_id):
            return []
        with self._conn() as c:
            taken = {r["slot"] for r in c.execute(
                "SELECT slot FROM appointments WHERE doctor_id=? "
                "AND status IN ('requested','confirmed')", (doctor_id,))}
        out: list[dict] = []
        today = date.today()
        for day in range(days):
            cur = today + timedelta(days=day)
            for hour in range(9, 17):
                if hour == 13:
                    continue
                for minute in (0, 30):
                    slot = f"{cur.isoformat()}T{hour:02d}:{minute:02d}"
                    if slot in taken or _h(doctor_id, slot) % 7 == 0:
                        continue
                    out.append({"slot": slot,
                                "label": cur.strftime("%d.%m") + f" {hour:02d}:{minute:02d}",
                                "day": cur.isoformat()})
                    if len(out) >= 24:
                        return out
        return out

    def suggest(self, specialist: str, limit: int = 3) -> dict:
        docs = [d for d in DOCTORS if d["specialist"] == specialist][:limit]
        out = []
        for d in docs:
            clinic = next((c for c in CLINICS if c["id"] == d["clinic"]), {})
            out.append({**d,
                        "specialist_label": _SPECIALIST_LABEL.get(specialist, specialist),
                        "clinic_name": clinic.get("name", "—"),
                        "district": clinic.get("district", "—"),
                        "free_slots": self.free_slots(d["id"])[:4]})
        return {"specialist": specialist,
                "specialist_label": _SPECIALIST_LABEL.get(specialist, specialist),
                "doctors": out, "synthetic": True, "note": SYNTHETIC_NOTE}

    def create_appointment(self, patient: str, doctor_id: str, slot: str,
                           actor: str = "patient",
                           role: str = "patient") -> dict:
        if role != "patient":
            raise PermissionError("Navbatni faqat bemor ochadi")
        d = self.doctor(doctor_id)
        if not d:
            raise ValueError("Shifokor topilmadi")
        if slot not in {s["slot"] for s in self.free_slots(doctor_id)}:
            raise ValueError("Bu vaqt bo'sh emas yoki o'tib ketgan")
        appt = {"id": _nid("appt"), "patient": patient, "doctor_id": doctor_id,
                "specialist": d["specialist"], "slot": slot,
                "status": "requested", "created_at": _now(),
                "confirmed_at": None, "confirmed_by": None}
        try:
            with self._conn() as c:
                c.execute("INSERT INTO appointments VALUES(?,?,?,?,?,?,?,?,?)",
                          (appt["id"], patient, doctor_id, d["specialist"], slot,
                           "requested", appt["created_at"], None, None))
                self._audit(c, actor, role, "appointment.requested",
                            "appointment", appt["id"], appt)
        except sqlite3.IntegrityError:
            raise ValueError("Bu vaqt allaqachon band") from None
        return appt

    def _appt(self, patient: str, appt_id: str) -> dict:
        with self._conn() as c:
            r = c.execute("SELECT * FROM appointments WHERE id=? AND patient=?",
                          (appt_id, patient)).fetchone()
        if not r:
            raise ValueError("Navbat topilmadi")
        return dict(r)

    def confirm_appointment(self, patient: str, appt_id: str,
                            actor: str = "user", role: str = "patient") -> dict:
        """Tasdiqlash faqat bemor tomonidan — agent/qoida emas."""
        if actor != "user" and role != "patient":
            raise PermissionError("Navbatni faqat foydalanuvchi tasdiqlaydi")
        if actor != "user" and actor != patient:
            raise PermissionError("Navbatni faqat foydalanuvchi tasdiqlaydi")
        appt = self._appt(patient, appt_id)
        if appt["status"] == "confirmed":
            return appt
        if appt["status"] != "requested":
            raise ValueError("Bu navbatni tasdiqlab bo'lmaydi")
        at = _now()
        with self._conn() as c:
            c.execute("UPDATE appointments SET status='confirmed', confirmed_at=?, "
                      "confirmed_by=? WHERE id=?", (at, "user", appt_id))
            self._audit(c, actor, role, "appointment.confirmed",
                        "appointment", appt_id, {"slot": appt["slot"]})
        return self._appt(patient, appt_id)

    def cancel_appointment(self, patient: str, appt_id: str,
                           actor: str = "user", role: str = "patient") -> dict:
        if role != "patient":
            raise PermissionError("Bekor qilishni faqat bemor qiladi")
        self._appt(patient, appt_id)
        with self._conn() as c:
            c.execute("UPDATE appointments SET status='cancelled' WHERE id=?",
                      (appt_id,))
            self._audit(c, actor, role, "appointment.cancelled",
                        "appointment", appt_id, {})
        return self._appt(patient, appt_id)

    # ── retsept (XPN bo'yicha)
    def create_prescription(self, patient: str, inn: str, doctor_id: str,
                            actor: str = "doctor_sim",
                            role: str = "doctor") -> dict:
        if role != "doctor":
            raise PermissionError("Retseptni faqat shifokor yozadi")
        d = self.doctor(doctor_id)
        if not d:
            raise ValueError("Shifokor topilmadi")
        res = registry.resolve(inn)
        if res["status"] != "ok":
            raise ValueError("XPN davlat reyestrida topilmadi — retsept yozilmaydi")
        drug = res["drug"]
        rx = {"id": _nid("rx"), "patient": patient, "doctor_id": doctor_id,
              "doctor": d["name"], "inn": drug["inn"],
              "inn_key": drug["inn_key"], "status": "draft",
              "created_at": _now(), "signed_at": None}
        with self._conn() as c:
            c.execute("INSERT INTO prescriptions VALUES(?,?,?,?,?,?,?,?,?,?)",
                      (rx["id"], patient, doctor_id, d["name"], drug["inn"],
                       drug["inn_key"], "draft", rx["created_at"], None, None))
            self._audit(c, actor, role, "prescription.draft", "prescription",
                        rx["id"], rx)
        return rx

    def sign_prescription(self, rx_id: str, actor: str = "doctor_sim",
                          role: str = "doctor") -> dict:
        """Imzo — faqat shifokor. Agent imzolamaydi."""
        if role != "doctor" or actor != "doctor_sim":
            raise PermissionError("Retseptni faqat shifokor imzolaydi")
        with self._conn() as c:
            r = c.execute("SELECT * FROM prescriptions WHERE id=?", (rx_id,)).fetchone()
            if not r:
                raise ValueError("Retsept topilmadi")
            if r["status"] != "draft":
                raise ValueError("Faqat qoralamani imzolash mumkin")
            at = _now()
            c.execute("UPDATE prescriptions SET status='signed', signed_at=?, "
                      "signed_by=? WHERE id=?", (at, actor, rx_id))
            self._audit(c, actor, role, "prescription.signed",
                        "prescription", rx_id, {"inn": r["inn"]})
            r = c.execute("SELECT * FROM prescriptions WHERE id=?", (rx_id,)).fetchone()
        return dict(r)

    def dispense(self, rx_id: str, offer: dict, actor: str = "pharmacist",
                 role: str = "pharmacist") -> dict:
        """Dorini berish — faqat farmatsevt, faqat imzolangan retsept bilan."""
        if role != "pharmacist":
            raise PermissionError("Dorini faqat farmatsevt beradi")
        with self._conn() as c:
            r = c.execute("SELECT * FROM prescriptions WHERE id=?", (rx_id,)).fetchone()
            if not r:
                raise ValueError("Retsept topilmadi")
            if r["status"] != "signed":
                raise ValueError("Retsept imzolanmagan — dori berilmaydi")
            off_inn = offer.get("canon_inn") or offer.get("inn_key")
            if off_inn != r["inn_key"]:
                raise ValueError("Taklif XPN bo'yicha mos emas")
            order = {"id": _nid("ord"), "rx_id": rx_id, "patient": r["patient"],
                     "pharmacy": offer.get("pharmacy") or offer.get("seller"),
                     "offer_id": offer.get("id"), "name": offer.get("name"),
                     "price": offer.get("price_from_som"), "status": "dispensed",
                     "created_at": _now(), "dispensed_at": _now()}
            c.execute("INSERT INTO orders VALUES(?,?,?,?,?,?,?,?,?,?)",
                      (order["id"], rx_id, r["patient"], order["pharmacy"],
                       order["offer_id"], order["name"], order["price"],
                       "dispensed", order["created_at"], order["dispensed_at"]))
            c.execute("UPDATE prescriptions SET status='dispensed' WHERE id=?", (rx_id,))
            self._audit(c, actor, role, "prescription.dispensed", "prescription",
                        rx_id, order)
        return order

    # ── o'qish
    def prescriptions(self, patient: str) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM prescriptions WHERE patient=? ORDER BY created_at DESC",
                (patient,))]

    def appointments(self, patient: str) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM appointments WHERE patient=? ORDER BY slot",
                (patient,))]

    def orders(self, patient: str) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM orders WHERE patient=? ORDER BY created_at DESC",
                (patient,))]

    def all_appointments(self, limit: int = 100) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM appointments ORDER BY slot LIMIT ?", (limit,))]

    def prescription_queue(self, limit: int = 100) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM prescriptions WHERE status='signed' "
                "ORDER BY signed_at LIMIT ?", (limit,))]

    def all_prescriptions(self, limit: int = 100) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM prescriptions ORDER BY created_at DESC LIMIT ?",
                (limit,))]

    def state_for(self, patient: str) -> dict:
        return {"appointments": self.appointments(patient),
                "prescriptions": self.prescriptions(patient),
                "orders": self.orders(patient),
                "synthetic": True, "note": SYNTHETIC_NOTE}

    def audit(self, limit: int = 50) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM audit ORDER BY id DESC LIMIT ?", (limit,))]

    def stats(self) -> dict:
        with self._conn() as c:
            q = lambda sql: c.execute(sql).fetchone()[0]      # noqa: E731
            return {"synthetic": True,
                    "clinics": len(CLINICS), "doctors": len(DOCTORS),
                    "specialists": len({d["specialist"] for d in DOCTORS}),
                    "appointments": q("SELECT COUNT(*) FROM appointments"),
                    "confirmed": q("SELECT COUNT(*) FROM appointments WHERE status='confirmed'"),
                    "prescriptions": q("SELECT COUNT(*) FROM prescriptions"),
                    "signed": q("SELECT COUNT(*) FROM prescriptions WHERE status='signed'"),
                    "dispensed": q("SELECT COUNT(*) FROM prescriptions WHERE status='dispensed'"),
                    "audit_rows": q("SELECT COUNT(*) FROM audit")}
