#!/usr/bin/env python3
"""O'RINDOR — brauzer demo (stdlib, 0 bog'liqlik).

    python3 orindor/web/server.py            # http://127.0.0.1:8000
    python3 orindor/web/server.py --port 8080

API:
    POST /api/chat      {"sid": "...", "text": "..."}
    GET  /api/card?q=paratsetamol
    GET  /api/stats
    GET  /api/reminders?sid=...
    GET  /api/health
"""
from __future__ import annotations

import json
import sys
import threading
import uuid
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from agent import Agent  # noqa: E402
from core import registry  # noqa: E402
from core.session import Session  # noqa: E402

AGENT = Agent()
SESSIONS: dict[str, Session] = {}
LOCK = threading.Lock()
INDEX = HERE / "index.html"


def _session(sid: str | None) -> tuple[str, Session]:
    with LOCK:
        if sid and sid in SESSIONS:
            return sid, SESSIONS[sid]
        new = sid or uuid.uuid4().hex[:12]
        SESSIONS[new] = Session()
        return new, SESSIONS[new]


class Handler(BaseHTTPRequestHandler):
    server_version = "OrindorDemo/1.0"

    def log_message(self, fmt, *args):  # jim
        pass

    def _send(self, code: int, payload, ctype="application/json; charset=utf-8"):
        if isinstance(payload, (dict, list)):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        elif isinstance(payload, str):
            body = payload.encode("utf-8")
        else:
            body = payload
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    # ── GET
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path in ("/", "/index.html"):
                return self._send(200, INDEX.read_bytes(), "text/html; charset=utf-8")
            if u.path == "/api/health":
                return self._send(200, {"ok": True, "product": "O'RINDOR",
                                        "problem": 17})
            if u.path == "/api/stats":
                st = registry.stats()
                return self._send(200, {k: v for k, v in st.items()
                                        if k != "schema"})
            if u.path == "/api/card":
                text = (q.get("q") or [""])[0]
                res = registry.resolve(text)
                out = {"status": res["status"], "alias": res.get("alias"),
                       "candidates": [asdict(c) for c in res["candidates"]]}
                if res["status"] == "ok":
                    c = registry.card(res["drug"]["id"])
                    out["card"] = c
                return self._send(200, out)
            if u.path == "/api/reminders":
                sid, s = _session((q.get("sid") or [None])[0])
                due = s.due_reminders()
                return self._send(200, {
                    "sid": sid,
                    "due": [r.to_dict() for r in due],
                    "all": [r.to_dict() for r in s.reminders],
                })
            return self._send(404, {"error": "not found"})
        except Exception as e:  # demo: xato yashirilmaydi, qaytariladi
            return self._send(500, {"error": f"{type(e).__name__}: {e}"})

    # ── POST
    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/api/chat":
            return self._send(404, {"error": "not found"})
        body = self._json_body()
        text = (body.get("text") or "").strip()
        if not text:
            return self._send(400, {"error": "text bo'sh"})
        try:
            sid, s = _session(body.get("sid"))
            with LOCK:
                reply = AGENT.respond(s, text)
                out = {
                    "sid": sid,
                    "reply": reply,
                    "stage": s.stage,
                    "mode": s.mode,
                    "card": s.card,
                    "candidates": [asdict(c) for c in s.candidates],
                    "urgency": s.urgency.text if s.guess else None,
                    "specialty": s.guess.label if s.guess else None,
                    "is_emergency": s.stage == "emergency",
                    "reminders": [r.to_dict() for r in s.reminders],
                }
            return self._send(200, out)
        except Exception as e:
            return self._send(500, {"error": f"{type(e).__name__}: {e}"})


def main() -> None:
    port = 8000
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    st = registry.stats()
    print("O'RINDOR demo → http://127.0.0.1:%d" % port)
    print(f"  {st.get('drugs')} dori · {st.get('inn_groups')} XPN · "
          f"{st.get('referent_prices')} narx · {st.get('details')} chegara narx")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
