#!/usr/bin/env python3
"""MllyMed Backend Server — B2C va B2B Portallari uchun API serveri.

Ishga tushirish:
    python3 -m backend.server --port 8200
"""
from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Yo'llarni ulash
from . import config
from .api.router import ApiRouter
from .services import BridgeService

BRIDGE = BridgeService()
ROUTER = ApiRouter(BRIDGE)
ROLES = {"patient", "doctor", "pharmacist", "admin"}


def role_of(h: BaseHTTPRequestHandler) -> tuple[str, str]:
    role = (h.headers.get("X-Role") or "patient").strip().lower()
    if role not in ROLES:
        role = "patient"
    user = (h.headers.get("X-User") or "demo").strip()[:64]
    return role, user


class MllyMedHandler(BaseHTTPRequestHandler):
    server_version = "MllyMed/2.0"

    def log_message(self, *a):
        pass

    def _json(self, obj: dict | list, code: int = 200) -> None:
        body = json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")
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

    def do_GET(self) -> None:  # noqa: N802
        u = urlparse(self.path)
        q = parse_qs(u.query)
        role, _ = role_of(self)

        try:
            # 1. Frontend statik fayllarni uzatish
            if u.path in ("/", "/index.html"):
                return self._file(config.STATIC_DIR / "index.html")

            safe_rel = u.path.lstrip("/")
            target = (config.STATIC_DIR / safe_rel).resolve()
            if target.is_file() and str(target).startswith(str(config.STATIC_DIR.resolve())):
                return self._file(target)

            # 2. API so'rovlarni router orqali yo'naltirish
            res, code = ROUTER.route_get(u.path, q, role)
            return self._json(res, code)

        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_POST(self) -> None:  # noqa: N802
        u = urlparse(self.path)
        b = self._body()
        role, user = role_of(self)

        try:
            res, code = ROUTER.route_post(u.path, b, role, user)
            return self._json(res, code)
        except Exception as e:  # noqa: BLE001
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)


def run_server(port: int = 8200) -> None:
    server_addr = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_addr, MllyMedHandler)
    print(f"★ MllyMed Server ishga tushdi: http://127.0.0.1:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer to'xtatildi.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8200)
    args = parser.parse_args()
    run_server(args.port)
