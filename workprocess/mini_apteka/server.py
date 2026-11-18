#!/usr/bin/env python3
"""Mini apteka — stdlib server (fastapi/flask o'rnatilmagan, ataylab).

Vazifasi: O'RINDOR kartasi qanday ko'rinishini ko'rsatish uchun kichik,
tez, oflayn-ishlaydigan dorixona katalogi.

Ishga tushirish:  python3 mini_apteka/server.py        → http://0.0.0.0:8100
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "data", "catalog.json")
FACTS = os.path.join(os.path.dirname(HERE), "orindor", "data", "facts.json")
PORT = int(os.environ.get("PORT", "8100"))


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def norm(s: str) -> str:
    return (s or "").lower().replace("ʻ", "'").replace("’", "'").replace("`", "'")


def price_check(products: list[dict]) -> dict:
    """3735 (F09) qoidasining PROXY tekshiruvi.

    Qonun referent narx haqida: jenerik referent narxi originalning 80% idan
    oshmasligi kerak. Bizda referent narx YO'Q (reyestr yopiq), shuning uchun
    chakana narxni proxy sifatida olamiz va buni ochiq yozamiz.
    """
    loc = [p for p in products if p["local"] and p.get("price_from_som")]
    imp = [p for p in products if p["local"] is False and p.get("price_from_som")]
    if not loc or not imp:
        return {"holat": "tekshirib bo'lmadi",
                "sabab": "bir XPN ostida mahalliy va import narxi yetarli emas"}
    l, i = min(p["price_from_som"] for p in loc), min(p["price_from_som"] for p in imp)
    chegara = round(i * 0.80)
    return {
        "holat": "mos" if l <= chegara else "80% dan qimmat",
        "mahalliy_eng_arzon": l,
        "import_eng_arzon": i,
        "chegara_80": chegara,
        "farq_foiz": round((1 - l / i) * 100, 1),
        "izoh": "chakana narx proxy sifatida — referent narx reyestri yopiq",
    }


class H(BaseHTTPRequestHandler):
    server_version = "MiniApteka/1.0"

    def log_message(self, *a):        # konsol shovqinini kamaytirish
        pass

    def _json(self, obj, code: int = 200) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, path: str) -> None:
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:                                  # noqa: N802
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            return self._html(os.path.join(HERE, "index.html"))

        cat = load(CATALOG)
        prods = cat["products"] + cat.get("arzon_showcase", [])

        if u.path == "/api/catalog":
            return self._json(cat)

        if u.path == "/api/search":
            q = norm(parse_qs(u.query).get("q", [""])[0]).strip()
            if not q:
                return self._json({"q": q, "total": 0, "items": []})
            hits = [p for p in prods
                    if q in norm(p.get("name")) or q in norm(p.get("inn"))
                    or q in norm(p.get("manufacturer"))]
            # bir xil XPN dagi barcha variantlarni ham qo'shamiz (almashtirish)
            inss = {norm(p.get("inn")) for p in hits if p.get("inn")}
            if inss:
                extra = [p for p in prods
                         if norm(p.get("inn")) in inss and p not in hits]
                hits += extra
            return self._json({"q": q, "total": len(hits), "items": hits})

        if u.path.startswith("/api/inn/"):
            inn = norm(u.path.split("/api/inn/", 1)[1])
            group = [p for p in prods if norm(p.get("inn")) == inn]
            if not group:
                return self._json({"xato": "XPN topilmadi", "inn": inn}, 404)
            facts = load(FACTS)
            f09 = next((f for f in facts["facts"] if f["id"] == "F09"), None)
            f12 = next((f for f in facts["facts"] if f["id"] == "F12"), None)
            return self._json({
                "inn": group[0]["inn"],
                "products": group,
                "orindor": {
                    "narx_tekshiruv": price_check(group),
                    "reyestr": {"holat": "ma'lum emas",
                                "sabab": "davlat reyestri API'si ochiq emas"},
                    "asl_belgisi": {"holat": "ma'lum emas",
                                    "sabab": "GTIN/kod CRPT Turon orqali, ochiq emas"},
                    "dalil": [x for x in (f09, f12) if x],
                },
            })

        if u.path == "/api/stats":
            meta = cat["meta"]
            return self._json({
                "mahsulot": len(cat["products"]),
                "xpn": len({norm(p.get("inn")) for p in cat["products"] if p.get("inn")}),
                "mahalliy": sum(1 for p in cat["products"] if p["local"]),
                "import": sum(1 for p in cat["products"] if p["local"] is False),
                "kategoriya": len(cat["categories"]),
                "vitrina": len(cat.get("arzon_showcase", [])),
                "olingan_vaqt": meta.get("olingan_vaqt"),
                "olcham_kb": round(os.path.getsize(CATALOG) / 1024, 1),
            })

        return self._json({"xato": "yo'l topilmadi"}, 404)


if __name__ == "__main__":
    print(f"mini apteka → http://0.0.0.0:{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
