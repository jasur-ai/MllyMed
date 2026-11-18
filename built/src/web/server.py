#!/usr/bin/env python3
"""Katta mahsulot API si — bemor, shifokor, farmatsevt, admin.

Ishga tushirish (built/ ichidan):
    python3 -m src.web.server --port 8200

Rollar `X-Role` sarlavhasi bilan: patient | doctor | pharmacist | admin.
Bu demo: autentifikatsiya yo'q, rol faqat UI portalini ajratadi — lekin
domen qoidalari (kim tasdiqlaydi, kim imzolaydi, kim beradi) kodda.
"""
from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src import apteka, paths  # noqa: E402
from src.bridge import Bridge  # noqa: E402

BRIDGE = Bridge()
ROLES = {"patient", "doctor", "pharmacist", "admin"}


def role_of(h) -> tuple[str, str]:
    role = (h.headers.get("X-Role") or "patient").strip().lower()
    if role not in ROLES:
        role = "patient"
    user = (h.headers.get("X-User") or "demo").strip()[:64]
    return role, user


class H(BaseHTTPRequestHandler):
    server_version = "Built/2.0"

    def log_message(self, *a):
        pass

    def _json(self, obj, code: int = 200) -> None:
        body = json.dumps(obj, ensure_ascii=False, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,X-Role,X-User")
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            return self._json({"error": "topilmadi"}, 404)
        body = path.read_bytes()
        mimes = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".svg": "image/svg+xml",
            ".png": "image/png",
            ".ico": "image/x-icon",
            ".woff2": "font/woff2",
        }
        ctype = mimes.get(path.suffix, "text/plain; charset=utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def _need(self, role: str) -> None:
        if role_of(self)[0] != role:
            raise PermissionError(f"Bu amal uchun rol: {role}")

    # ── GET
    def do_GET(self) -> None:                       # noqa: N802
        u = urlparse(self.path)
        q = parse_qs(u.query)
        role, _ = role_of(self)
        try:
            if u.path in ("/", "/index.html"):
                return self._file(paths.STATIC / "index.html")
            safe_rel = u.path.lstrip("/")
            candidate = (paths.STATIC / safe_rel).resolve()
            if candidate.is_file() and str(candidate).startswith(str(paths.STATIC.resolve())):
                return self._file(candidate)
            if u.path == "/api/health":
                return self._json({"ok": True, "product": "O'RINDOR built",
                                   "version": 2, "role": role})
            if u.path == "/api/stats":
                return self._json(BRIDGE.stats())
            if u.path == "/api/analytics":
                return self._json(BRIDGE.analytics())
            if u.path == "/api/card":
                return self._json(BRIDGE.card_lookup((q.get("q") or [""])[0]))
            if u.path == "/api/arzon":
                return self._json(BRIDGE.arzon(
                    limit=int((q.get("limit") or ["24"])[0] or 24),
                    category=(q.get("category") or [None])[0],
                    local=(q.get("local") or [None])[0]))
            if u.path == "/api/catalog":
                return self._json(BRIDGE.catalog(
                    q=(q.get("q") or [""])[0],
                    page=int((q.get("page") or ["1"])[0] or 1),
                    size=int((q.get("size") or ["20"])[0] or 20),
                    local=(q.get("local") or [None])[0],
                    category=(q.get("category") or [None])[0]))
            if u.path.startswith("/api/inn/"):
                inn = unquote(u.path.split("/api/inn/", 1)[1])
                return self._json(apteka.summary(inn))
            if u.path == "/api/dmed/doctors":
                return self._json(BRIDGE.suggest((q.get("specialist") or ["terapevt"])[0]))
            if u.path == "/api/dmed/slots":
                return self._json({"slots": BRIDGE.slots((q.get("doctor") or [""])[0])})
            if u.path == "/api/doctors":
                return self._json(BRIDGE.doctors())
            if u.path == "/api/state":
                return self._json(BRIDGE.state((q.get("sid") or ["demo"])[0]))
            if u.path == "/api/appointments":
                return self._json({"items": BRIDGE.all_appointments()})
            if u.path == "/api/prescriptions":
                return self._json({"items": BRIDGE.prescriptions(
                    (q.get("sid") or ["demo"])[0])})
            if u.path == "/api/prescriptions/queue":
                if role not in ("pharmacist", "admin"):
                    return self._json({"error": "faqat farmatsevt"}, 403)
                return self._json({"items": BRIDGE.queue()})
            if u.path == "/api/audit":
                if role != "admin":
                    return self._json({"error": "faqat admin"}, 403)
                return self._json({"items": BRIDGE.audit(
                    int((q.get("limit") or ["50"])[0] or 50))})
            return self._json({"error": "yo'l topilmadi"}, 404)
        except Exception as e:                        # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    # ── POST
    def do_POST(self) -> None:                      # noqa: N802
        u = urlparse(self.path)
        b = self._body()
        sid = b.get("sid") or "demo"
        role, user = role_of(self)
        try:
            if u.path == "/api/chat":
                return self._json(BRIDGE.chat(sid, (b.get("text") or "").strip()))
            if u.path == "/api/appointments":
                appt = BRIDGE.book_request(sid, b.get("doctor_id"), b.get("slot"))
                return self._json({"appointment": appt,
                                   "note": "So'rov yaratildi — hali TASDIQLANMAGAN"})
            if u.path == "/api/appointments/confirm":
                return self._json({"appointment": BRIDGE.book_confirm(sid, b.get("id"))})
            if u.path == "/api/appointments/cancel":
                return self._json({"appointment": BRIDGE.book_cancel(sid, b.get("id"))})
            if u.path == "/api/prescriptions":
                self._need("doctor")
                return self._json(BRIDGE.prescription_draft(
                    b.get("patient") or sid, b.get("inn") or "",
                    b.get("doctor_id") or user))
            if u.path == "/api/prescriptions/sign":
                self._need("doctor")
                return self._json(BRIDGE.prescription_sign(b.get("id")))
            if u.path == "/api/prescriptions/dispense":
                self._need("pharmacist")
                return self._json(BRIDGE.dispense(b.get("id"), b.get("offer_id")))
            return self._json({"error": "yo'l topilmadi"}, 404)
        except PermissionError as e:
            return self._json({"error": str(e)}, 403)
        except ValueError as e:
            return self._json({"error": str(e)}, 400)
        except Exception as e:                        # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8200)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), H)
    print(f"built demo v2 → http://{args.host}:{args.port}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
