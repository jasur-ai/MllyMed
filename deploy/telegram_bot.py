#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MllyMed Telegram bot — deploy ko'prigi (QO'SHIMCHA modul).

Bu fayl mahsulot kodiga TEGMAYDI va uni o'zgartirmaydi. U faqat Telegram
Bot API va MllyMed HTTP API o'rtasida ko'prik vazifasini bajaradi:

    foydalanuvchi → Telegram → shu bot → POST /api/b2c/chat → agent javobi

Ishga tushirish (uzoq so'rov / long polling — HTTPS va webhook shart emas):

    export TELEGRAM_BOT_TOKEN="<BotFather bergan token>"
    export MLLYMED_API="https://sizning-domeningiz.uz"   # yoki http://127.0.0.1:8200
    python3 deploy/telegram_bot.py

O'z-o'zini tekshirish (tarmoqsiz, faqat ichki mantiq):

    python3 deploy/telegram_bot.py --selftest

Muhim:
  • Token HECH QACHON kodga yozilmaydi — faqat muhit o'zgaruvchisi.
  • Bot hech qanday tibbiy qaror qabul qilmaydi; barcha javoblar MllyMed
    agentidan keladi (u xavfsizlik validatoridan o'tgan).
  • Har Telegram foydalanuvchisi alohida sid oladi: tg-<chat_id>.
  • "/yangi" — suhbatni tozalash (agent buni o'zi tushunadi).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
MLLYMED_API = os.environ.get("MLLYMED_API", "http://127.0.0.1:8200").rstrip("/")
TG_API = f"https://api.telegram.org/bot{TOKEN}"
TG_LIMIT = 4000  # Telegram xabarining 4096 belgidan kichik xavfsiz chegarasi

HELP_TEXT = (
    "🤖 MllyMed — Milliy dori vositalariga ishonch ekotizimi\n\n"
    "Dori nomini yozing: «paratsetamol», «nurofen 200»\n"
    "Shikoyatni yozing: «bosh og'riyapti», «tishim qattiq og'riyapti»\n\n"
    "Buyruqlar:\n"
    "/start — boshlash\n"
    "/help — yordam\n"
    "/yangi — suhbatni boshidan boshlash\n\n"
    "Men tashxis qo'ymayman va dori maslahati bermayman. "
    "Favqulodda holatda: 103."
)


# ── sof funksiyalar (tarmoqsiz test qilinadi) ───────────────────────────────

def map_command(text: str) -> tuple[str, str]:
    """Xabarni (kind, payload) ga ajratadi.

    kind: "help" | "chat"   — boshqa hamma narsa chat ga tushadi.
    """
    t = (text or "").strip()
    low = t.lower()
    if low in ("/start", "/help", "start", "help", "yordam"):
        return "help", ""
    if low == "/yangi":
        return "chat", "yangi"
    if low.startswith("/"):
        return "chat", t  # noma'lum buyruq — agentga uzatiladi, u o'zi hal qiladi
    return "chat", t


def sid_for(chat_id: int) -> str:
    return f"tg-{chat_id}"


def trim_reply(text: str) -> str:
    text = (text or "").strip() or "Javob bo'sh chiqdi. «/yangi» bosib qayta urinib ko'ring."
    return text if len(text) <= TG_LIMIT else text[: TG_LIMIT - 1] + "…"


# ── tarmoq qatlami ──────────────────────────────────────────────────────────

def _post_json(url: str, payload: dict, timeout: int) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def tg(method: str, **params) -> dict:
    return _post_json(f"{TG_API}/{method}", params, timeout=40)


def mllymed_chat(sid: str, text: str) -> dict:
    return _post_json(f"{MLLYMED_API}/api/b2c/chat",
                      {"sid": sid, "text": text}, timeout=30)


def handle_message(chat_id: int, text: str) -> str:
    kind, payload = map_command(text)
    if kind == "help":
        return HELP_TEXT
    try:
        data = mllymed_chat(sid_for(chat_id), payload)
    except urllib.error.URLError as exc:
        print(f"[xato] MllyMed API ga ulanib bo'lmadi: {exc.reason}", file=sys.stderr)
        return ("MllyMed xizmati hozircha javob bermayapti. "
                "Birozdan keyin urinib ko'ring. Favqulodda holatda: 103.")
    except Exception as exc:  # noqa: BLE001 — bot yiqilmasligi kerak
        print(f"[xato] chat: {type(exc).__name__}: {exc}", file=sys.stderr)
        return "Kutilmagan xato yuz berdi. «/yangi» bosib qayta boshlang."
    reply = trim_reply(str(data.get("reply") or ""))
    triage = data.get("triage") or {}
    if triage.get("urgency"):
        reply += f"\n\n⏱ Shoshilinchlik: {triage['urgency']}"
    return trim_reply(reply)


def poll_forever() -> int:
    if not TOKEN:
        print("XATO: TELEGRAM_BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan.", file=sys.stderr)
        return 2
    try:
        me = tg("getMe")
        print(f"Bot ishga tushdi: @{me.get('result', {}).get('username', '?')} "
              f"(MLLYMED_API={MLLYMED_API})")
    except Exception as exc:  # noqa: BLE001
        print(f"XATO: Telegram API ga ulanib bo'lmadi: {exc}", file=sys.stderr)
        return 2

    offset: int | None = None
    while True:
        try:
            upd = tg("getUpdates", timeout=30, offset=offset,
                     allowed_updates=["message"])
            for item in upd.get("result", []):
                offset = int(item["update_id"]) + 1
                msg = item.get("message") or {}
                chat_id = (msg.get("chat") or {}).get("id")
                text = msg.get("text")
                if not chat_id or not text:
                    continue
                reply = handle_message(int(chat_id), str(text))
                try:
                    tg("sendMessage", chat_id=chat_id, text=reply)
                except Exception as exc:  # noqa: BLE001
                    print(f"[xato] sendMessage: {exc}", file=sys.stderr)
        except KeyboardInterrupt:
            print("\nTo'xtatildi.")
            return 0
        except Exception as exc:  # noqa: BLE001 — tarmoq uzilishi: qayta urinamiz
            print(f"[ogohlantirish] getUpdates: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            time.sleep(3)


# ── o'z-o'zini tekshirish ───────────────────────────────────────────────────

def selftest() -> int:
    checks = [
        (map_command("/start") == ("help", ""), "/start → help"),
        (map_command("/help") == ("help", ""), "/help → help"),
        (map_command("yordam") == ("help", ""), "yordam → help"),
        (map_command("/yangi") == ("chat", "yangi"), "/yangi → reset"),
        (map_command("paratsetamol") == ("chat", "paratsetamol"), "dori → chat"),
        (map_command("ko'kragim og'riyapti") == ("chat", "ko'kragim og'riyapti"),
         "shikoyat → chat"),
        (sid_for(123) == "tg-123", "sid formati"),
        (trim_reply("") != "", "bo'sh javob himoyasi"),
        (len(trim_reply("x" * 10000)) <= TG_LIMIT, "uzun javob kesiladi"),
        ("103" in HELP_TEXT, "yordamda 103 bor"),
    ]
    failed = 0
    for ok, name in checks:
        print(("✅" if ok else "❌") + f" {name}")
        failed += 0 if ok else 1
    # Ixtiyoriy: lokal MllyMed API ishlayotgan bo'lsa — haqiqiy roundtrip
    try:
        data = mllymed_chat("tg-selftest", "yangi")
        print(f"✅ MllyMed API roundtrip ({MLLYMED_API}): reply={str(data.get('reply'))[:60]!r}")
    except Exception:
        print(f"ℹ️  MllyMed API ({MLLYMED_API}) hozir ishlamayapti — roundtrip o'tkazib yuborildi "
              "(bu o'z-o'zini tekshirishning xatosi emas)")
    print(f"\n{'HAMMASI O‘TDI' if failed == 0 else str(failed) + ' TA XATO'}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MllyMed Telegram bot ko'prigi")
    parser.add_argument("--selftest", action="store_true",
                        help="tarmoqsiz ichki tekshiruv")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    return poll_forever()


if __name__ == "__main__":
    sys.exit(main())
