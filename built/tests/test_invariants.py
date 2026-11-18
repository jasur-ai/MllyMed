"""Invariant testlar — kod bilan majburlangan qoidalar buzilmasin.

Ishga tushirish (built/ ichidan):
    python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

BUILT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUILT))

from src import apteka  # noqa: E402
from src.bridge import Bridge  # noqa: E402
from src.dmed import DMed  # noqa: E402


class TestApteka(unittest.TestCase):
    def test_catalog_counts(self):
        st = apteka.stats()
        self.assertGreaterEqual(st["products"], 288)
        self.assertGreaterEqual(st["with_inn"], 280)
        self.assertGreaterEqual(st["without_inn"], 20)
        self.assertGreaterEqual(st["inn_groups"], 150)

    def test_arzon_entries_have_no_inn_and_unknown_local(self):
        arzon = [p for p in apteka.linked() if p["source"] == "arzonapteka.uz"]
        self.assertEqual(len(arzon), 20)
        for p in arzon:
            self.assertFalse(p["has_inn"])
            self.assertIsNone(p["local"])

    def test_spelling_link(self):
        canon, method, score = apteka.canon_inn("parasetamol")
        self.assertEqual(canon, "paratsetamol")
        self.assertIn(method, ("fuzzy", "contains"))
        self.assertGreaterEqual(score, 0.9)

    def test_by_inn_returns_only_inn_products(self):
        group = apteka.by_inn("paratsetamol")
        self.assertGreaterEqual(len(group), 1)
        self.assertTrue(all(p["has_inn"] for p in group))

    def test_price_check_states(self):
        ok = apteka.price_check([
            {"local": True, "price_from_som": 100},
            {"local": False, "price_from_som": 200},
        ])
        self.assertEqual(ok["holat"], "mos")
        self.assertEqual(ok["chegara_80"], 160)

        bad = apteka.price_check([
            {"local": True, "price_from_som": 170},
            {"local": False, "price_from_som": 200},
        ])
        self.assertEqual(bad["holat"], "80% dan qimmat")

        missing = apteka.price_check([
            {"local": True, "price_from_som": 100},
            {"local": False, "price_from_som": None},
        ])
        self.assertEqual(missing["holat"], "tekshirib bo'lmadi")


class TestAnalytics(unittest.TestCase):
    def test_checks_all_pass(self):
        from src import analytics
        bad = [c for c in analytics.checks() if not c["ok"]]
        self.assertEqual(bad, [])

    def test_catalog_sums(self):
        from src import analytics
        a = analytics.overview()
        c = a["catalog"]
        self.assertEqual(c["products"], c["with_inn"] + c["without_inn"])
        self.assertEqual(c["local"] + c["import"] + c["unknown_origin"], c["with_inn"])
        self.assertGreater(c["inn_groups"], 100)


class TestDMed(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.dm = DMed(Path(self.td.name) / "state.json")

    def tearDown(self):
        self.td.cleanup()

    def test_unknown_doctor(self):
        with self.assertRaises(ValueError):
            self.dm.create_appointment("p1", "d-xxx", "2026-01-01T09:00")

    def test_only_patient_books(self):
        slots = self.dm.free_slots("d01")
        with self.assertRaises(PermissionError):
            self.dm.create_appointment("p1", "d01", slots[0]["slot"], role="doctor")

    def test_agent_cannot_confirm(self):
        slots = self.dm.free_slots("d01")
        appt = self.dm.create_appointment("p1", "d01", slots[0]["slot"])
        with self.assertRaises(PermissionError):
            self.dm.confirm_appointment("p1", appt["id"], actor="agent")
        done = self.dm.confirm_appointment("p1", appt["id"], actor="user")
        self.assertEqual(done["status"], "confirmed")
        self.assertEqual(done["confirmed_by"], "user")

    def test_prescription_requires_registered_inn(self):
        with self.assertRaises(ValueError):
            self.dm.create_prescription("p1", "florbaksinzz", "d01")

    def test_only_doctor_signs(self):
        rx = self.dm.create_prescription("p1", "paratsetamol", "d01")
        self.assertEqual(rx["status"], "draft")
        with self.assertRaises(PermissionError):
            self.dm.sign_prescription(rx["id"], actor="agent")
        signed = self.dm.sign_prescription(rx["id"], actor="doctor_sim")
        self.assertEqual(signed["status"], "signed")

    def _linked_offer(self):
        for p in apteka.linked():
            if (p.get("has_inn") and p.get("price_from_som")
                    and p.get("canon_inn")):
                return p
        self.skipTest("bog'langan taklif yo'q")

    def test_dispense_requires_signed_and_role(self):
        offer = self._linked_offer()
        rx = self.dm.create_prescription("p1", offer["canon_inn"], "d01")
        with self.assertRaises(ValueError):
            self.dm.dispense(rx["id"], offer)
        self.dm.sign_prescription(rx["id"])
        with self.assertRaises(PermissionError):
            self.dm.dispense(rx["id"], offer, role="patient")
        order = self.dm.dispense(rx["id"], offer)
        self.assertEqual(order["status"], "dispensed")
        self.assertEqual(self.dm.prescriptions("p1")[0]["status"], "dispensed")

    def test_dispense_wrong_inn_rejected(self):
        offer = self._linked_offer()
        other = next(p for p in apteka.linked()
                     if p.get("has_inn") and p.get("canon_inn")
                     and p["canon_inn"] != offer["canon_inn"])
        rx = self.dm.create_prescription("p1", offer["canon_inn"], "d01")
        self.dm.sign_prescription(rx["id"])
        with self.assertRaises(ValueError):
            self.dm.dispense(rx["id"], other)


class TestBridge(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.b = Bridge(Path(self.td.name) / "state.json")

    def tearDown(self):
        self.td.cleanup()

    def test_emergency_does_not_create_appointment(self):
        r = self.b.chat("x", "Qon qusdim")
        self.assertEqual(r["stage"], "emergency")
        self.assertIn("103", r["reply"])
        self.assertEqual(self.b.state("x")["appointments"], [])

    def test_card_links_pharmacy(self):
        r = self.b.chat("y", "ezomeprazol")
        self.assertEqual(r["stage"], "card")
        self.assertGreaterEqual((r.get("apteka") or {}).get("count", 0), 1)

    def test_triage_offers_doctors_not_booking(self):
        self.b.chat("z", "Ko'kragim og'riyapti")
        r = self.b.chat("z", "yo'q")
        self.assertEqual(r["stage"], "routed")
        self.assertGreaterEqual(len((r.get("dmed") or {}).get("doctors", [])), 1)
        self.assertEqual(self.b.state("z")["appointments"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
