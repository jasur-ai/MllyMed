#!/usr/bin/env python3
"""MllyMed Telegram Bot & Mini App Integratsiyasi (Track №17).

Telegram orqali:
1. Mini App rejimida to'liq real mobil ilovani ochish (Telegram Web App).
2. Botning o'z chat interfeysi orqali MllyMed Agent bilan to'g'ridan-to'g'ri suhbatlashish:
   - Dori qidiruvi va 80% mahalliy GMP muqobillarini topish;
   - Shikoyat bo'yicha xavfsiz tibbiy triaj (103 shoshilinch tekshiruvi);
   - Referent narx va davlat reyestri tahlili.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time
from pathlib import Path

# Loyiha ildizini Python path-ga qo'shish
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    import requests
except ImportError:
    print("Xatolik: 'requests' kutubxonasi o'rnatilmagan. Iltimos: pip install requests")
    sys.exit(1)

from agent.agent import Agent, Session

# Konfiguratsiya
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9273249390:AAEujrRl8b_4WUtO0VA2RyhF1NH40m8gXTI")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://jasur-ai.github.io/MllyMed/")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MllyMedBot")


class MllyMedTelegramBot:
    def __init__(self, token: str, webapp_url: str):
        self.token = token
        self.webapp_url = webapp_url
        self.api_base = f"https://api.telegram.org/bot{token}"
        self.agent = Agent()
        self.sessions: dict[int, Session] = {}
        self.last_update_id = 0

    def get_session(self, chat_id: int) -> Session:
        if chat_id not in self.sessions:
            self.sessions[chat_id] = Session(f"tg_{chat_id}")
        return self.sessions[chat_id]

    def reset_session(self, chat_id: int) -> Session:
        self.sessions[chat_id] = Session(f"tg_{chat_id}")
        return self.sessions[chat_id]

    def _call(self, method: str, data: dict = None, timeout: int = 40) -> dict:
        url = f"{self.api_base}/{method}"
        try:
            resp = requests.post(url, json=data or {}, timeout=timeout)
            return resp.json()
        except Exception as e:
            logger.warning(f"Telegram API xatosi ({method}): {e}")
            return {"ok": False, "description": str(e)}

    def send_message(self, chat_id: int, text: str, reply_markup: dict = None) -> dict:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._call("sendMessage", payload)

    def answer_callback(self, callback_id: str, text: str = None) -> dict:
        payload = {"callback_query_id": callback_id}
        if text:
            payload["text"] = text
        return self._call("answerCallbackQuery", payload)

    def get_main_reply_keyboard(self) -> dict:
        """Doimiy pastki klaviatura: Mini App va tezkor tugmalar."""
        return {
            "keyboard": [
                [
                    {
                        "text": "📱 MllyMed ilovasini ochish",
                        "web_app": {"url": self.webapp_url}
                    }
                ],
                [
                    {"text": "💊 Dori qidirish"},
                    {"text": "🩺 Shikoyat bildirish"}
                ],
                [
                    {"text": "🇺🇿 80% Mahalliy dori pariteti"},
                    {"text": "🔄 Yangi suhbat"}
                ]
            ],
            "resize_keyboard": True,
            "is_persistent": True
        }

    def get_welcome_inline_keyboard(self) -> dict:
        """Start xabaridagi inline tugmalar."""
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "📱 MllyMed Mini App (To'liq ilova)",
                        "web_app": {"url": self.webapp_url}
                    }
                ],
                [
                    {"text": "💊 Paratsetamol muqobili", "callback_data": "quick_paracetamol"},
                    {"text": "💊 Nurofen tahlili", "callback_data": "quick_nurofen"}
                ],
                [
                    {"text": "🇺🇿 Mahalliy dori kafolati", "callback_data": "quick_local_info"},
                    {"text": "🛡️ 103 Shoshilinch triaj", "callback_data": "quick_emergency"}
                ]
            ]
        }

    def handle_start(self, chat_id: int, user: dict):
        first_name = user.get("first_name", "Foydalanuvchi")
        self.reset_session(chat_id)

        text = (
            f"Assalomu alaykum, <b>{first_name}</b>!\n\n"
            "🏥 <b>MllyMed (O'RINDOR) — Milliy dori vositalariga ishonch ekotizimi</b>\n"
            "<i>Milliy AI Hackathon · 17-trek (Sog'liqni saqlash)</i>\n\n"
            "Men sizga dori vositalarining haqiqiyligi, referent narxi va sifatli "
            "<b>mahalliy GMP muqobillarini</b> topishda yordam beraman.\n\n"
            "✨ <b>Nimalar qila olaman?</b>\n"
            "• 💊 <b>Dori tekshiruvi:</b> 46 079 ta davlat ro'yxatidagi dori, XPN (INN) va referent narxlar;\n"
            "• 🇺🇿 <b>80% Mahalliy paritet:</b> Qimmat import o'rniga O'zbekistonning 45-80% arzon dori analoglari;\n"
            "• 🩺 <b>Tibbiy triaj:</b> Shikoyatingiz bo'yicha birlamchi xavfsiz yo'naltirish;\n"
            "• 📱 <b>Telegram Mini App:</b> To'liq mobil ilova interfeysi.\n\n"
            "👇 <b>Quyidagi tugma orqali ilovani oching yoki dori nomini / shikoyatingizni to'g'ridan-to'g'ri yozing:</b>"
        )
        self.send_message(
            chat_id,
            text,
            reply_markup=self.get_welcome_inline_keyboard()
        )
        # Shuningdek doimiy reply keyboardni ham yoqamiz
        self.send_message(
            chat_id,
            "💡 <i>Maslahat: Istalgan vaqtda dori nomini yozsangiz (masalan: «Paratsetamol» yoki «Kardiomagnil»), tahlil qilib beraman.</i>",
            reply_markup=self.get_main_reply_keyboard()
        )

    def handle_callback(self, query: dict):
        query_id = query.get("id")
        data = query.get("data", "")
        message = query.get("message", {})
        chat_id = message.get("chat", {}).get("id")

        if not chat_id:
            return

        self.answer_callback(query_id)
        session = self.get_session(chat_id)

        if data == "quick_paracetamol":
            reply = self.agent.respond(session, "paratsetamol")
            self._send_agent_reply(chat_id, reply, "Paratsetamol")
        elif data == "quick_nurofen":
            reply = self.agent.respond(session, "nurofen")
            self._send_agent_reply(chat_id, reply, "Nurofen")
        elif data == "quick_local_info":
            info_text = (
                "🇺🇿 <b>Mahalliy dori vositalarining 80% paritet kafolati</b>\n\n"
                "O'zbekiston Respublikasi Prezidentining <b>PF-35</b> va Vazirlar Mahkamasining "
                "<b>738-sonli qarorlariga</b> asosan:\n"
                "1. GMP sertifikatiga ega milliy korxonalar import dorilar bilan bir xil ta'sir etuvchi modda (XPN) va bioekvivalentlikka ega;\n"
                "2. Mahalliy dorilar import analoglaridan <b>o'rtacha 40% dan 80% gacha arzon</b>;\n"
                "3. Har bir dori davlat reyestrida (api.mpa.uz) ro'yxatdan o'tgan va qat'iy nazoratda."
            )
            self.send_message(chat_id, info_text)
        elif data == "quick_emergency":
            reply = self.agent.respond(session, "ko'kragim qattiq og'riyapti")
            self._send_agent_reply(chat_id, reply, "Favqulodda triaj")
        elif data in ("yes", "ha"):
            reply = self.agent.respond(session, "ha")
            self._send_agent_reply(chat_id, reply)
        elif data in ("no", "yo'q", "yoq"):
            reply = self.agent.respond(session, "yo'q")
            self._send_agent_reply(chat_id, reply)

    def handle_text_message(self, chat_id: int, text: str):
        cleaned = text.strip()
        lower = cleaned.lower()

        # Buyruqlar
        if lower in ("/start", "start"):
            self.handle_start(chat_id, {"first_name": "Foydalanuvchi"})
            return
        elif lower in ("/help", "yordam"):
            help_text = (
                "🤖 <b>MllyMed AI yordamchi buyruqlari:</b>\n\n"
                "• <b>Dori qidirish:</b> «Paratsetamol», «Ibuprofen», «Sitramon»\n"
                "• <b>Shikoyat:</b> «Boshim og'riyapti», «Ko'nglim ayniyapti»\n"
                "• <b>Yangi suhbat:</b> «/reset» yoki «Yangi suhbat»\n\n"
                "📱 To'liq interfeys uchun <b>«📱 MllyMed ilovasini ochish»</b> tugmasidan foydalaning."
            )
            self.send_message(chat_id, help_text, reply_markup=self.get_main_reply_keyboard())
            return
        elif lower in ("/reset", "yangi suhbat", "🔄 yangi suhbat", "yangi"):
            self.reset_session(chat_id)
            self.send_message(
                chat_id,
                "🔄 Yangi suhbat boshlandi. Qanday dori yoki shikoyat bo'yicha yordam bera olaman?",
                reply_markup=self.get_main_reply_keyboard()
            )
            return
        elif lower in ("💊 dori qidirish", "dori qidirish"):
            self.send_message(
                chat_id,
                "🔍 Qidirayotgan dori nomini yozing (masalan: <i>Amoksitsillin, Kardiomagnil, Sitramon</i>):"
            )
            return
        elif lower in ("🩺 shikoyat bildirish", "shikoyat bildirish"):
            self.send_message(
                chat_id,
                "🩺 Qanday alomat yoki og'riq bezovta qilyapti? Iltimos yozib qoldiring:"
            )
            return
        elif "80%" in lower or "mahalliy" in lower and "paritet" in lower:
            self.handle_callback({"id": "0", "data": "quick_local_info", "message": {"chat": {"id": chat_id}}})
            return

        # MllyMed agentiga yuborish
        session = self.get_session(chat_id)
        reply = self.agent.respond(session, cleaned)
        self._send_agent_reply(chat_id, reply, cleaned)

    def _send_agent_reply(self, chat_id: int, reply: str, query: str = ""):
        """Agent javobini formatlab yuborish va kerak bo'lsa inline tugmalar qo'shish."""
        safe_reply = reply.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # Javob turiga qarab inline tugmalar tayyorlash
        inline_buttons = []

        # Agar skrinig savoli (ha/yo'q) berilgan bo'lsa
        if "ha" in reply.lower() and "yo'q" in reply.lower() and ("aniqlashtirish" in reply.lower() or "savol" in reply.lower()):
            inline_buttons.append([
                {"text": "✅ Ha", "callback_data": "ha"},
                {"text": "❌ Yo'q", "callback_data": "yoq"}
            ])

        # Mini App ochish tugmasi
        mini_app_url = self.webapp_url
        if query and len(query) < 30 and not any(w in query.lower() for w in ("ha", "yo'q", "eslatma")):
            # Qidiruv so'rovi bilan ochish
            mini_app_url = f"{self.webapp_url}?q={requests.utils.quote(query)}"

        inline_buttons.append([
            {
                "text": "📱 MllyMed ilovasida to'liq ko'rish",
                "web_app": {"url": mini_app_url}
            }
        ])

        reply_markup = {"inline_keyboard": inline_buttons}
        self.send_message(chat_id, f"<pre>{safe_reply}</pre>", reply_markup=reply_markup)

    def run_polling(self):
        """Telegram Long Polling sikli."""
        logger.info(f"MllyMed Telegram Bot ishga tushdi! (WebApp: {self.webapp_url})")
        print(f"\n✅ MllyMed Telegram Bot faol! (@MllyMed_bot)")
        print(f"🔗 Mini App URL: {self.webapp_url}")
        print("Bot xabarlarni kutmoqda...\n")

        while True:
            try:
                updates = self._call("getUpdates", {
                    "offset": self.last_update_id + 1,
                    "timeout": 25
                })

                if not updates.get("ok"):
                    time.sleep(2)
                    continue

                for update in updates.get("result", []):
                    self.last_update_id = update["update_id"]

                    if "callback_query" in update:
                        self.handle_callback(update["callback_query"])
                    elif "message" in update:
                        msg = update["message"]
                        chat_id = msg.get("chat", {}).get("id")
                        text = msg.get("text")
                        user = msg.get("from", {})

                        if not chat_id:
                            continue

                        if text:
                            if text.startswith("/start"):
                                self.handle_start(chat_id, user)
                            else:
                                self.handle_text_message(chat_id, text)

            except KeyboardInterrupt:
                logger.info("Bot foydalanuvchi tomonidan to'xtatildi.")
                break
            except Exception as e:
                logger.error(f"Polling xatosi: {e}")
                time.sleep(3)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="MllyMed Telegram Bot Runner")
    parser.add_argument("--token", default=BOT_TOKEN, help="Telegram Bot Token")
    parser.add_argument("--webapp-url", default=WEBAPP_URL, help="Telegram Mini App URL (HTTPS)")
    args = parser.parse_args()

    bot = MllyMedTelegramBot(args.token, args.webapp_url)
    bot.run_polling()


if __name__ == "__main__":
    main()
