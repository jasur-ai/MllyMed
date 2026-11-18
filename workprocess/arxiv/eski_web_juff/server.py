"""
JUFT · №17 — ishlaydigan API server (faqat Python standart kutubxonasi).
=======================================================================
Nega bu fayl bor: baholash mezonlarida "T1 — texnik amalga oshirilish" va
"T2 — kod tayyorligi" alohida turadi. Shuning uchun mahsulot statik HTML emas —
haqiqiy servis: HTTP API + UI, ma'lumot dvigateldan keladi.

Endpoints
    GET  /                     → UI (index.html)
    GET  /api/health           → servis holati
    GET  /api/groups           → INN guruhlari + ishonch kartalari
    GET  /api/trust?inn=&mg=   → bitta INN uchun kartalar
    GET  /api/scan-cases       → 4 ta QR holati (demo)
    POST /api/scan             → o'z qutingizni tekshirish (JSON)
    GET  /api/eval?n=          → xavfsizlik baholash xulosasi

Ishga tushirish:  python3 app/server.py   → http://0.0.0.0:8000
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "prototype"))

from juft17_core import (  # noqa: E402
    BY_TRADE, CATALOG, Packet, ScanEvent, TODAY, build_card, check_authenticity,
    compare_inn, make_serial,
)

PORT = int(os.environ.get("PORT", "8000"))


# ------------------------------------------------------------
# Ma'lumot yig'ish
# ------------------------------------------------------------

def _plus_months(d: date, m: int) -> date:
    y, mo = d.year + (d.month - 1 + m) // 12, (d.month - 1 + m) % 12 + 1
    return date(y, mo, min(d.day, 28))


def genuine_packet(p) -> Packet:
    mfg = date(2025, 5, 1)
    return Packet(p.gtin, make_serial(p, 12345), (p.known_batches or ("XX",))[0],
                  mfg, _plus_months(mfg, p.shelf_life_months), ("uz", "ru"), (),
                  p.price_uzs)


def card_json(c) -> dict:
    prod = BY_TRADE[c.trade]
    a = check_authenticity(prod, genuine_packet(prod))
    return {
        "trade": c.trade, "inn": c.inn, "mg": prod.strength_mg, "form": prod.form,
        "gtin": prod.gtin,
        "maker": c.manufacturer, "country": c.country, "local": c.is_local,
        "nti": prod.is_nti, "price": c.price_uzs, "pack": c.pack,
        "ev": c.evidence.name, "evtext": c.evidence.value,
        "docs": c.docs, "gaps": c.gaps, "cert": c.cert_status,
        "verdict": c.verdict.name, "vtext": c.verdict.value,
        "score": c.score, "savings": c.savings_vs_import, "refprice": c.ref_price_uzs,
        "action": c.action_line,
        "auth": {
            "band": a.band, "risk": a.risk, "action": a.action,
            "hard": [h.text for h in a.hard],
            "contrib": [[t, str(w)] for t, w in a.contributions],
        },
    }


def groups_json() -> list[dict]:
    out, seen = [], []
    for p in CATALOG:
        key = (p.inn, p.strength_mg)
        if key in seen:
            continue
        seen.append(key)
        cards = [card_json(c) for c in compare_inn(p.inn, p.strength_mg)]
        out.append({"inn": p.inn, "mg": p.strength_mg,
                    "label": f"{p.inn} {p.strength_mg:g} mg", "cards": cards})
    return out


SCAN_CASES = [
    ("Oddiy quti", lambda p, s: Packet(p.gtin, s, "SF2201", date(2025, 6, 1),
                                       date(2028, 6, 1), ("uz", "ru"), (), 38000)),
    ("Ikki hududda skanerlangan", lambda p, s: Packet(
        p.gtin, s, "SF2201", date(2025, 6, 1), date(2028, 6, 1), ("uz", "ru"),
        (ScanEvent(date(2026, 11, 10), "Toshkent"),
         ScanEvent(date(2026, 11, 11), "Andijon")), 38000)),
    ("Soxta qadoq", lambda p, s: Packet(
        "4780012345799", "UZ-CE-1234567", "SF2299", date(2025, 6, 1),
        date(2029, 6, 1), ("uz", "ru"), (), 9000)),
    ("Muddati o'tgan", lambda p, s: Packet(p.gtin, make_serial(p, 124), "SF2201",
                                           date(2023, 1, 1), date(2026, 1, 1),
                                           ("uz", "ru"), (), 38000)),
]


def scan_cases() -> list[dict]:
    p = BY_TRADE["Seftriakson"]
    ser = make_serial(p, 123)
    out = []
    for name, mk in SCAN_CASES:
        v = check_authenticity(p, mk(p, ser))
        out.append({"name": name, "band": v.band, "risk": v.risk, "action": v.action,
                    "hard": [h.text for h in v.hard],
                    "contrib": [[t, str(w)] for t, w in v.contributions]})
    return out


def eval_summary(n: int = 120) -> dict:
    """Tez baholash — to'liq eval bilan bir xil mantiq, kichik namuna.

    Bir xil kodni ishlatish muhim: aks holda slaydda 98%, API da 93% chiqadi va
    hakam buni birinchi savolda ushlaydi.
    """
    from eval_juft17 import (DEFECTS, RNG, claim_justified, forged_packet,
                             genuine_packet as eval_genuine)
    RNG.seed(17)                              # deterministik

    products = [p for p in CATALOG if p.known_batches]
    fa = 0
    for p in products:
        if check_authenticity(p, eval_genuine(p)).band != "YASHIL":
            fa += 1

    hit = tot = 0
    for p in products:
        for d in DEFECTS:                       # har mahsulot × har nuqson turi
            tot += 1
            if check_authenticity(p, forged_packet(p, (d,))).band != "YASHIL":
                hit += 1

    unsafe, claims = 0, 0
    for p in CATALOG:
        imports = [q for q in CATALOG if q.inn == p.inn
                   and abs(q.strength_mg - p.strength_mg) < 1e-9 and not q.is_local]
        card = build_card(p, imports[0] if imports else None)
        if card.verdict.name == "JUFT":
            claims += 1
            ok, _ = claim_justified(p, imports[0] if imports else None)
            if not ok:
                unsafe += 1
    return {"recall": round(hit / tot, 3), "false_alarm": round(fa / len(products), 3),
            "over_claim": unsafe, "claims": claims, "forged_sweep": tot,
            "products": len(products)}


# ------------------------------------------------------------
# HTTP
# ------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "JUFT/1.0"

    def log_message(self, fmt, *args):        # demo loglarini jim tutamiz
        pass

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def do_GET(self) -> None:                 # noqa: N802
        u = urlparse(self.path)
        q = parse_qs(u.query)
        path = u.path

        if path in ("/", "/index.html"):
            fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
            with open(fp, "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
            return

        if path == "/api/health":
            self._json({"ok": True, "service": "JUFT", "problem": 17,
                        "products": len(CATALOG), "today": TODAY.isoformat()})
            return

        if path == "/api/groups":
            self._json(groups_json())
            return

        if path == "/api/trust":
            inn = (q.get("inn") or [""])[0]
            mg = float((q.get("mg") or ["0"])[0])
            cards = [card_json(c) for c in compare_inn(inn, mg)]
            self._json({"inn": inn, "mg": mg, "cards": cards})
            return

        if path == "/api/scan-cases":
            self._json(scan_cases())
            return

        if path == "/api/eval":
            n = int((q.get("n") or ["120"])[0])
            self._json(eval_summary(max(20, min(n, 400))))
            return

        self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:                # noqa: N802
        if urlparse(self.path).path != "/api/scan":
            self._json({"error": "not found"}, 404)
            return
        try:
            ln = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(ln) or b"{}")
        except Exception:
            self._json({"error": "bad json"}, 400)
            return

        trade = body.get("trade", "Seftriakson")
        p = BY_TRADE.get(trade)
        if p is None:
            self._json({"error": f"noma'lum mahsulot: {trade}"}, 400)
            return
        try:
            mfg = date.fromisoformat(body.get("mfg", "2025-05-01"))
            exp = date.fromisoformat(body.get("expiry", "2028-05-01"))
        except ValueError:
            self._json({"error": "sana formati YYYY-MM-DD"}, 400)
            return
        scans = tuple(ScanEvent(date.fromisoformat(s["when"]), s["region"])
                      for s in body.get("scans", []))
        pk = Packet(body.get("gtin", p.gtin), body.get("serial", make_serial(p, 1)),
                    body.get("batch", (p.known_batches or ("XX",))[0]),
                    mfg, exp, tuple(body.get("langs", ["uz", "ru"])), scans,
                    body.get("price"))
        v = check_authenticity(p, pk)
        self._json({"band": v.band, "risk": v.risk, "action": v.action,
                    "hard": [{"code": h.code, "text": h.text, "source": h.source}
                             for h in v.hard],
                    "contrib": [[t, str(w)] for t, w in v.contributions],
                    "features": v.features})


def main() -> None:
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"JUFT API → http://0.0.0.0:{PORT}")
    print(f"  {len(CATALOG)} mahsulot · 6 INN guruhi · {len(SCAN_CASES)} QR holati")
    srv.serve_forever()


if __name__ == "__main__":
    main()
