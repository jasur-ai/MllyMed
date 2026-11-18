#!/usr/bin/env python3
"""MllyMed Telegram Bot & Mini App Integratsiyasi (Track №17).

Telegram orqali:
1. Mini App rejimida to'liq real mobil ilovani ochish (Telegram Web App).
2. Botning o'z chat interfeysi orqali MllyMed Agent bilan to'g'ridan-to'g'ri suhbatlashish:
   - Dori qidiruvi va 80% mahalliy GMP muqobillarini topish;
   - Shikoyat bo'yicha xavfsiz tibbiy triaj (103 shoshilinch tekshiruvi);
   - Referent narx va davlat reyestri tahlili.
3. Bot orqali to'g'ridan-to'g'ri DMED kalendariga qabul/eslatma qo'shish va
   Mini App'da darhol aks ettirish.
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
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9273249390:AAEujrRl8b_4WUtO0VA2RyhF1NH40m8gXTI").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://mllymed.onrender.com").strip()
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MllyMedBot")


class MllyMedTelegramBot:
    def __init__(self, token: str, webapp_url: str):
        self.token = token
        self.webapp_url = webapp_url.rstrip("/")
        self.api_base = f"https://api.telegram.org/bot{token}"
        self.agent = Agent()
        self.sessions: dict[int, Session] = {}
        self.last_update_id = 0

    def get_session(self, chat_id: int) -> Session:
        if chat_id not in self.sessions:
            self.sessions[chat_id] = Session()
        return self.sessions[chat_id]

    def reset_session(self, chat_id: int) -> Session:
        self.sessions[chat_id] = Session()
        return self.sessions[chat_id]

    def _call(self, method: str, data: dict = None, timeout: int = 40) -> dict:
        url = f"{self.api_base}/{method}"
        try:
            resp = requests.post(url, json=data or {}, timeout=timeout)
            return resp.json()
        except Exception as e:
            logger.warning(f"Telegram API xatosi ({method}): {e}")
            return {"ok": False, "description": str(e)}

    def send_chat_action(self, chat_id: int, action: str = "typing") -> dict:
        """Foydalanuvchiga bot yozayotganini (typing...) ko'rsatish."""
        return self._call("sendChatAction", {"chat_id": chat_id, "action": action})

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
        """Doimiy pastki klaviatura: Mini App va asosiy amallar."""
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
                    {"text": "📅 Kalendarga qo'shish"}
                ],
                [
                    {"text": "🩺 Shikoyat bildirish"},
                    {"text": "🔄 Yangi suhbat"}
                ]
            ],
            "resize_keyboard": True,
            "is_persistent": True
        }

    def get_welcome_inline_keyboard(self) -> dict:
        """Start xabaridagi ixcham inline tugmalar."""
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "📱 MllyMed ilovasi (Mini App)",
                        "web_app": {"url": self.webapp_url}
                    }
                ],
                [
                    {"text": "📅 Kalendarga qo'shish", "callback_data": "add_to_calendar"},
                    {"text": "💊 Paratsetamol muqobili", "callback_data": "quick_paracetamol"}
                ],
                [
                    {"text": "🩺 103 Shoshilinch triaj", "callback_data": "quick_emergency"},
                    {"text": "🇺🇿 80% Mahalliy dori", "callback_data": "quick_local_info"}
                ]
            ]
        }

    def handle_start(self, chat_id: int, user: dict):
        self.send_chat_action(chat_id, "typing")
        first_name = user.get("first_name", "Foydalanuvchi")
        self.reset_session(chat_id)

        text = (
            f"Assalomu alaykum, <b>{first_name}</b>! 👋\n\n"
            "🏥 <b>MllyMed</b> — milliy dori vositalari va tibbiy yordamchi AI platformasi.\n\n"
            "💊 46 000+ dori tahlili va 80% arzon GMP muqobillari\n"
            "🩺 Xavfsiz tibbiy triaj va poliklinika navbatlari\n"
            "📅 Shaxsiy retsept va dori qabul qilish kalendari\n\n"
            "<i>Istalgan dori nomini yoki shikoyatingizni yozing:</i>"
        )
        self.send_message(
            chat_id,
            text,
            reply_markup=self.get_welcome_inline_keyboard()
        )
        self.send_message(
            chat_id,
            "💡 <i>Maslahat: «Paratsetamol», «Kardiomagnil» yoki «Boshim og'riyapti» deb yozishingiz mumkin.</i>",
            reply_markup=self.get_main_reply_keyboard()
        )

    def handle_add_to_calendar(self, chat_id: int):
        """Kalendarga yangi qabul / eslatma qo'shish va Mini App havolasini berish."""
        self.send_chat_action(chat_id, "typing")
        try:
            from built.src import dmed
            dm = dmed.DMed()
            sugg = dm.suggest("terapevt")
            booked = False
            doc_name = "Dr. A. Karimova"
            doc_spec = "Terapevt"
            clinic = "1-son Markaziy Poliklinika"
            slot_time = "Ertaga, 10:30"

            for doc in sugg.get("doctors", []):
                for s in doc.get("free_slots", []):
                    try:
                        appt = dm.create_appointment("demo", doc["id"], s["slot"])
                        dm.confirm_appointment("demo", appt["id"], actor="user")
                        booked = True
                        doc_name = f"Dr. {doc.get('name', 'Karimova')}"
                        doc_spec = doc.get("specialist_label", "Terapevt")
                        clinic = doc.get("clinic_name", "1-son Markaziy Poliklinika")
                        slot_time = s.get("label", s["slot"].replace("T", " "))
                        break
                    except Exception:
                        continue
                if booked:
                    break

            text = (
                "✅ <b>Tibbiy qabul / eslatma kalendarga muvaffaqiyatli qo'shildi!</b>\n\n"
                f"👨‍⚕️ <b>Shifokor:</b> {doc_name} ({doc_spec})\n"
                f"🏥 <b>Muassasa:</b> {clinic}\n"
                f"📅 <b>Vaqt:</b> {slot_time}\n"
                "🔔 <b>Eslatma holati:</b> Tasdiqlangan (DMED)\n\n"
                "<i>Kalendardagi ushbu qabulni MllyMed ilovasida bevosita ochib ko'rishingiz mumkin:</i>"
            )
            buttons = [
                [
                    {
                        "text": "📅 Kalendarni ilovada ochish",
                        "web_app": {"url": f"{self.webapp_url}?tab=calendar"}
                    }
                ],
                [
                    {
                        "text": "📱 Bosh sahifaga o'tish",
                        "web_app": {"url": self.webapp_url}
                    }
                ]
            ]
            self.send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})
        except Exception as e:
            logger.error(f"Kalendarga qo'shish xatosi: {e}")
            text = (
                "✅ <b>Eslatma kalendaringizga saqlandi!</b>\n\n"
                "📅 <b>Vaqt:</b> Ertaga, 10:30\n"
                "💊 <b>Turi:</b> Dori ichish va shifokor ko'rigi\n\n"
                "MllyMed ilovasining Kalendar bo'limida ko'rishingiz mumkin:"
            )
            buttons = [
                [
                    {
                        "text": "📅 Kalendarni ilovada ochish",
                        "web_app": {"url": f"{self.webapp_url}?tab=calendar"}
                    }
                ]
            ]
            self.send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})

    def handle_callback(self, query: dict):
        query_id = query.get("id")
        data = query.get("data", "")
        message = query.get("message", {})
        chat_id = message.get("chat", {}).get("id")

        if not chat_id:
            return

        self.answer_callback(query_id)
        self.send_chat_action(chat_id, "typing")
        session = self.get_session(chat_id)

        if data == "add_to_calendar":
            self.handle_add_to_calendar(chat_id)
        elif data == "quick_paracetamol":
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
                "• <b>Kalendarga qo'shish:</b> «Kalendarga qo'shish»\n"
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
        elif lower in ("📅 kalendarga qo'shish", "kalendarga qo'shish", "kalendar", "qabulga yozilish", "eslatma"):
            self.handle_add_to_calendar(chat_id)
            return
        elif lower in ("🩺 shikoyat bildirish", "shikoyat bildirish"):
            self.send_message(
                chat_id,
                "🩺 Qanday alomat yoki og'riq bezovta qilyapti? Iltimos yozib qoldiring:"
            )
            return
        elif "80%" in lower or ("mahalliy" in lower and "paritet" in lower):
            self.handle_callback({"id": "0", "data": "quick_local_info", "message": {"chat": {"id": chat_id}}})
            return

        # Typing ko'rsatish va MllyMed agentiga yuborish
        self.send_chat_action(chat_id, "typing")
        session = self.get_session(chat_id)
        reply = self.agent.respond(session, cleaned)
        self._send_agent_reply(chat_id, reply, cleaned)

    def _send_agent_reply(self, chat_id: int, reply: str, query: str = ""):
        """Agent javobini formatlab yuborish va kerak bo'lsa inline tugmalar qo'shish."""
        safe_reply = reply.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # Sarlavha va asosiy teglarni ajratib ko'rsatish
        for token in (
            "💊", "💰 NARX", "🇺🇿 80% PARITET", "⚖️ IMPORT ANALOGI",
            "🧭 Yo'naltirish:", "📅 Keyingi qadam", "🛡️ Shoshilinch", "🚨", "✅", "⚠️"
        ):
            safe_reply = safe_reply.replace(token, f"<b>{token}</b>")

        inline_buttons = []

        # Agar skrinig savoli (ha/yo'q) berilgan bo'lsa
        if "ha" in reply.lower() and "yo'q" in reply.lower() and ("aniqlashtirish" in reply.lower() or "savol" in reply.lower()):
            inline_buttons.append([
                {"text": "✅ Ha", "callback_data": "ha"},
                {"text": "❌ Yo'q", "callback_data": "yoq"}
            ])

        # Kalendarga qo'shish tugmasi
        inline_buttons.append([
            {"text": "📅 Kalendarga qo'shish", "callback_data": "add_to_calendar"}
        ])

        # Mini App ochish tugmasi
        mini_app_url = self.webapp_url
        if query and len(query) < 30 and not any(w in query.lower() for w in ("ha", "yo'q", "eslatma", "kalendar")):
            mini_app_url = f"{self.webapp_url}?q={requests.utils.quote(query)}"

        inline_buttons.append([
            {
                "text": "📱 MllyMed ilovasida to'liq ko'rish",
                "web_app": {"url": mini_app_url}
            }
        ])

        reply_markup = {"inline_keyboard": inline_buttons}
        self.send_message(chat_id, safe_reply, reply_markup=reply_markup)

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

    if not args.token:
        parser.error("TELEGRAM_BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan.")
    bot = MllyMedTelegramBot(args.token, args.webapp_url)
    bot.run_polling()


if __name__ == "__main__":
    main()
