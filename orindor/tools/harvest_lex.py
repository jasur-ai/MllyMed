"""
O'RINDOR · UZ QONUNCHILIGINI YIG'ISH (lex.uz) — T0 rasmiy manba
===========================================================
Nima qiladi: lex.uz ning to'liq matnli qidiruv API sidan foydalanib,
№17 uchun zarur bo'lgan barcha qonun hujjatlarini topadi, yuklaydi va
matnini toza holda saqlaydi. Har bir yozuvda: hujjat raqami, sana, havola.

Nega bu muhim: "738-son nima deydi?" degan savolga javob kod ichida
bo'lishi kerak, tarqoq eslatmada emas. A2 (ekvivalentlik) dalil qatlami
aynan shu hujjatlarga tayanadi.

API (topilgan, kalit so'ralmaydi):
    POST https://lex.uz/api/search/bybody
    {"text": "...", "lang": 4, "page_size": 20, "page_number": 1, "search_type": 1}
    → {"code":1,"data":{"totalRows":N,"items":[{lact_id,title,lact_number,...}]}}
    Hujjat: https://lex.uz/uz/docs/{lact_id}

Ishga tushirish:  python3 egiz/harvest_lex.py
"""

from __future__ import annotations

import html
import json
import os
import re
import time
import urllib.request
from datetime import date

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "uz")
TODAY = date.today().isoformat()
API = "https://lex.uz/api/search/bybody"

# №17 uchun kerakli mavzular — har biri alohida qidiriladi
TOPICS = [
    ("referent narx", "referens narx tizimi — A3 narx qatlami"),
    ("dori vositalarini markalash", "ASL BELGISI / serializatsiya — A1 haqiqiylik"),
    ("bioekvivalentlik", "BE tadqiqoti — A2 dalil qatlami"),
    ("hayotiy muhim dori vositalari", "majburiy ro'yxat — assortiment"),
    ("dori vositalari davlat ro'yxati", "reyestr — asosiy manba"),
    ("farmatsevtika mahsulotlari xavfsizligi", "nazorat organi"),
    ("dori vositalari narxini tartibga solish", "narx regulyatsiyasi"),
    ("dori vositalarini import qilish tartibi", "import — import/mahalliy nisbati"),
]


def post(url: str, payload: dict) -> dict | None:
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(), method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json",
                     "User-Agent": "Mozilla/5.0 (O'RINDOR research)"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"    ! search {type(e).__name__}: {e}")
        return None


def get_html(lact_id: int) -> str | None:
    url = f"https://lex.uz/uz/docs/{lact_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (O'RINDOR research)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"    ! doc {lact_id}: {type(e).__name__}")
        return None


NOISE = re.compile(
    r"(Hujjatga taklif yuborish|Audioni tinglash|Hujjat elementidan havola olish|"
    r"Oldingi tahrirga qarang|Keyingi tahrirga havola|Oldingi tahrirga havola|"
    r"QTUK boʻyicha indekslash|QMQ boʻyicha indekslash|ONLINE TRANSLATE)")


def clean_text(h: str) -> str:
    t = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<(br|/p|/div|/tr|/li|/h\d)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("\xa0", " ")
    lines = []
    for ln in t.split("\n"):
        ln = re.sub(r"[ \t]+", " ", ln).strip()
        if len(ln) < 3 or NOISE.search(ln):
            continue
        if ln.startswith("[ OKOZ:"):
            continue
        lines.append(ln)
    return "\n".join(lines)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    index: list[dict] = []
    seen: dict[int, dict] = {}

    print("O'RINDOR · lex.uz — UZ qonunchiligini yig'ish\n" + "═" * 76)
    for q, why in TOPICS:
        print(f"\n» {q}  ({why})")
        d = post(API, {"text": q, "lang": 4, "page_size": 20,
                       "page_number": 1, "search_type": 1})
        if not d or d.get("code") != 1:
            continue
        items = (d.get("data") or {}).get("items") or []
        total = (d.get("data") or {}).get("totalRows")
        print(f"  natija: {len(items)} / {total}")
        for it in items:
            lid = it.get("lact_id")
            if lid in seen:
                seen[lid]["topics"].append(q)
                continue
            rec = {"lact_id": lid, "title": it.get("title"),
                   "number": it.get("lact_number"), "form": it.get("display_name_form"),
                   "date": it.get("acceptance_date"), "status": it.get("status"),
                   "url": f"https://lex.uz/uz/docs/{lid}", "topics": [q],
                   "_provenance": {"source": "lex.uz", "query": q, "fetched": TODAY}}
            seen[lid] = rec
            index.append(rec)
            print(f"   · {rec['number'] or '—':<12} {rec['date'] or '':<11} "
                  f"{(rec['title'] or '')[:70]}")
        time.sleep(0.4)

    print(f"\n{'-' * 76}\nJami noyob hujjat: {len(index)}")

    # Muhim hujjatlar matnini yuklaymiz (barchasi emas — vaqt va hajm)
    MUST = []
    for r in index:
        blob = (r["title"] or "") + " " + (r["number"] or "")
        if re.search(r"738|markalash|referent|bioekvivalent|hayotiy muhim", blob, re.I):
            MUST.append(r)

    print(f"Matni yuklanadigan hujjat: {len(MUST)}")
    for r in MUST[:12]:
        h = get_html(r["lact_id"])
        if not h:
            continue
        txt = clean_text(h)
        fn = f"{abs(r['lact_id'])}_{re.sub(r'[^a-z0-9]+', '_', (r['number'] or 'doc').lower())[:24]}.txt"
        with open(os.path.join(OUT, fn), "w") as f:
            f.write(f"# {r['title']}\n# {r['number']} · {r['date']} · {r['url']}\n\n{txt}")
        r["text_file"] = fn
        r["chars"] = len(txt)
        print(f"   ✓ {r['number'] or r['lact_id']:<12} {len(txt):>7} belgi → {fn}")
        time.sleep(0.5)

    fp = os.path.join(OUT, "lex_index.json")
    with open(fp, "w") as f:
        json.dump({"built": TODAY, "source": API, "count": len(index),
                   "documents": index}, f, ensure_ascii=False, indent=1)
    print(f"\n→ {fp}")


if __name__ == "__main__":
    main()
