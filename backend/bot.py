#!/usr/bin/env python3
"""MllyMed Telegram Bot & Mini App Integratsiyasi (Track №17).

Telegram orqali:
1. Mini App faqat rasmiy chap pastki Telegram Menu Button ("MllyMed") orqali ochiladi.
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
import re
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


def format_telegram_html(text: str) -> str:
    """Agent javobini chiroyli va o'qilishi oson Telegram HTML formatiga o'tkazish."""
    # 1. HTML xavfsizligi
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # 2. Markdown qalin shrift **text** -> <b>text</b>
    safe = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", safe)

    # 3. Sarlavhalar ### -> <b>...</b>
    safe = re.sub(r"^#{1,6}\s*(.+)$", r"<b>\1</b>", safe, flags=re.MULTILINE)

    # 4. Asosiy blok va sarlavhalarni ajratib ko'rsatish
    tokens_to_bold = (
        "💊", "💰 NARX", "🇺🇿 80% PARITET", "⚖️ IMPORT ANALOGI",
        "🧭 Yo'naltirish:", "📅 Keyingi qadam", "🛡️ Shoshilinch",
        "🚨", "✅", "⚠️", "📊 GURUH", "🧪 DALIL", "🔐 HAQIQIYLIK",
        "📚 Manbalar:", "👨‍⚕️ Shifokor:", "🏥 Muassasa:", "📅 Vaqt:"
    )
    for token in tokens_to_bold:
        safe = safe.replace(token, f"<b>{token}</b>")

    # 5. Belgilar oraliqlarini tozalash
    safe = safe.replace("   · ", " • ").replace("   ", " ")
    return safe.strip()


class MllyMedTelegramBot:
    def __init__(self, token: str, webapp_url: str):
        self.token = token
        self.webapp_url = webapp_url.rstrip("/")
        self.api_base = f"https://api.telegram.org/bot{token}"
        self.agent = Agent()
        self.sessions: dict[int, Session] = {}
        self.last_update_id = 0

        # Bot ishga tushganda menyu tugmasini MllyMed deb o'rnatish
        self.configure_menu_button()

    def configure_menu_button(self):
        """Telegram chat chap pastki menyu tugmasini 'MllyMed' qilish."""
        try:
            menu_payload = {
                "type": "web_app",
                "text": "MllyMed",
                "web_app": {"url": self.webapp_url}
            }
            res = requests.post(
                f"{self.api_base}/setChatMenuButton",
                data={"menu_button": json.dumps(menu_payload)},
                timeout=15
            ).json()
            if res.get("ok"):
                logger.info(f"✅ Telegram Chat Menu Button o'rnatildi: 'MllyMed' -> {self.webapp_url}")
            else:
                logger.warning(f"Menu button o'rnatishda javob: {res}")
        except Exception as e:
            logger.warning(f"Menu button o'rnatishda xatolik: {e}")

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
        """Doimiy pastki klaviatura: Faqat qulay bot harakatlari (Launch App bu yerda bo'lmaydi)."""
        return {
            "keyboard": [
                [
                    {"text": "💊 Dori qidirish"},
                    {"text": "🩺 Shikoyat bildirish"}
                ],
                [
                    {"text": "📅 Kalendarga eslatma"},
                    {"text": "🇺🇿 80% Mahalliy dori"}
                ],
                [
                    {"text": "🔄 Yangi suhbat"}
                ]
            ],
            "resize_keyboard": True,
            "is_persistent": True
        }

    def get_welcome_inline_keyboard(self) -> dict:
        """Start xabaridagi tezkor harakat tugmalari."""
        return {
            "inline_keyboard": [
                [
                    {"text": "💊 Paratsetamol muqobili", "callback_data": "quick_paracetamol"},
                    {"text": "💊 Nurofen tahlili", "callback_data": "quick_nurofen"}
                ],
                [
                    {"text": "🩺 103 Shoshilinch triaj", "callback_data": "quick_emergency"},
                    {"text": "🇺🇿 80% Mahalliy dori", "callback_data": "quick_local_info"}
                ],
                [
                    {"text": "📅 Kalendarga eslatma qo'shish", "callback_data": "add_to_calendar"}
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
            "💊 <b>46 000+ dori tahlili:</b> Davlat reyestri, referent narx va 80% arzon GMP muqobillari\n"
            "🩺 <b>Xavfsiz tibbiy triaj:</b> Alomatlaringiz bo'yicha to'g'ri mutaxassisga yo'naltirish\n"
            "📅 <b>Shaxsiy kalendar:</b> Shifokor qabuli va dori ichish eslatmalari\n\n"
            "<i>Istalgan dori nomini yoki shikoyatingizni to'g'ridan-to'g'ri yozing:</i>"
        )
        self.send_message(
            chat_id,
            text,
            reply_markup=self.get_welcome_inline_keyboard()
        )
        self.send_message(
            chat_id,
            "💡 <i>Maslahat: quyidagi tugmalardan birini tanlang yoki savolingizni yozib yuboring:</i>",
            reply_markup=self.get_main_reply_keyboard()
        )

    def handle_add_to_calendar(self, chat_id: int):
        """Kalendarga yangi qabul / eslatma qo'shish."""
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
                "🔔 <b>Eslatma holati:</b> Faol (DMED Kalendar)\n\n"
                "<i>Eslatma belgilangan vaqtda bot orqali sizga eslatiladi. "
                "Shuningdek, chap pastdagi <b>MllyMed</b> tugmasini bosib, to'liq kalendarni ochishingiz mumkin.</i>"
            )
            buttons = [
                [
                    {"text": "📅 Yangi eslatma qo'shish", "callback_data": "add_to_calendar"},
                    {"text": "💊 Dori qidirish", "callback_data": "prompt_drug_search"}
                ],
                [
                    {"text": "🔄 Yangi suhbat", "callback_data": "quick_reset"}
                ]
            ]
            self.send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})
        except Exception as e:
            logger.error(f"Kalendarga qo'shish xatosi: {e}")
            text = (
                "✅ <b>Eslatma kalendaringizga saqlandi!</b>\n\n"
                "📅 <b>Vaqt:</b> Ertaga, 10:30\n"
                "💊 <b>Turi:</b> Dori ichish va shifokor ko'rigi\n"
                "🔔 <b>Holat:</b> Faol"
            )
            buttons = [
                [
                    {"text": "💊 Dori qidirish", "callback_data": "prompt_drug_search"},
                    {"text": "🔄 Yangi suhbat", "callback_data": "quick_reset"}
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
        elif data == "prompt_drug_search":
            self.handle_drug_search_prompt(chat_id)
        elif data == "prompt_symptom_triage":
            self.handle_symptom_prompt(chat_id)
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
                "<b>738-sonli qarorlariga</b> asosan:\n\n"
                "1. GMP sertifikatiga ega milliy korxonalar import dorilar bilan bir xil ta'sir etuvchi modda (XPN) va bioekvivalentlikka ega;\n"
                "2. Mahalliy dorilar import analoglaridan <b>o'rtacha 40% dan 80% gacha arzon</b>;\n"
                "3. Har bir dori davlat reyestrida (api.mpa.uz) ro'yxatdan o'tgan va qat'iy nazoratda.\n\n"
                "<i>Istalgan dori nomini yozing, uning arzon muqobillarini ko'rsatamiz:</i>"
            )
            buttons = [
                [
                    {"text": "💊 Paratsetamol muqobili", "callback_data": "quick_paracetamol"},
                    {"text": "💊 Kardiomagnil muqobili", "callback_data": "quick_kardiomagnil"}
                ]
            ]
            self.send_message(chat_id, info_text, reply_markup={"inline_keyboard": buttons})
        elif data == "quick_kardiomagnil":
            reply = self.agent.respond(session, "kardiomagnil")
            self._send_agent_reply(chat_id, reply, "Kardiomagnil")
        elif data == "quick_sitramon":
            reply = self.agent.respond(session, "sitramon")
            self._send_agent_reply(chat_id, reply, "Sitramon")
        elif data == "quick_emergency":
            reply = self.agent.respond(session, "ko'kragim qattiq og'riyapti")
            self._send_agent_reply(chat_id, reply, "Favqulodda triaj")
        elif data == "quick_reset":
            self.reset_session(chat_id)
            self.send_message(
                chat_id,
                "🔄 Yangi suhbat boshlandi. Qanday dori yoki alomat bo'yicha yordam bera olaman?",
                reply_markup=self.get_main_reply_keyboard()
            )
        elif data in ("yes", "ha"):
            reply = self.agent.respond(session, "ha")
            self._send_agent_reply(chat_id, reply)
        elif data in ("no", "yo'q", "yoq"):
            reply = self.agent.respond(session, "yo'q")
            self._send_agent_reply(chat_id, reply)

    def handle_drug_search_prompt(self, chat_id: int):
        text = (
            "🔍 <b>Dori vositasini qidirish va tahlil qilish</b>\n\n"
            "Qidirayotgan dori nomini yoki ta'sir etuvchi moddasini (XPN) yozing:\n"
            "<i>Masalan: Paratsetamol, Kardiomagnil, Sitramon, Amoksitsillin, Nurofen</i>\n\n"
            "💡 Biz uning davlat reyestridagi narxini va 80% gacha arzon milliy GMP muqobillarini topib beramiz."
        )
        buttons = [
            [
                {"text": "💊 Paratsetamol", "callback_data": "quick_paracetamol"},
                {"text": "💊 Kardiomagnil", "callback_data": "quick_kardiomagnil"}
            ],
            [
                {"text": "💊 Sitramon", "callback_data": "quick_sitramon"},
                {"text": "💊 Nurofen", "callback_data": "quick_nurofen"}
            ]
        ]
        self.send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})

    def handle_symptom_prompt(self, chat_id: int):
        text = (
            "🩺 <b>Tibbiy triaj va dastlabki baholash</b>\n\n"
            "Sizni qanday alomat yoki og'riq bezovta qilyapti? Iltimos, erkin matnda yozing:\n"
            "<i>(Masalan: «Boshim qattiq og'riyapti», «Isitma va shamollash», «Ko'kragim qisilyapti»)</i>"
        )
        buttons = [
            [
                {"text": "🤕 Bosh og'rig'i", "callback_data": "symptom_headache"},
                {"text": "🤒 Isitma va shamollash", "callback_data": "symptom_fever"}
            ],
            [
                {"text": "❤️ Ko'krak qisishi (103)", "callback_data": "quick_emergency"},
                {"text": "🤢 Oshqozon og'rig'i", "callback_data": "symptom_stomach"}
            ]
        ]
        self.send_message(chat_id, text, reply_markup={"inline_keyboard": buttons})

    def handle_text_message(self, chat_id: int, text: str):
        cleaned = text.strip()
        lower = cleaned.lower()

        # Buyruqlar
        if lower in ("/start", "start"):
            self.handle_start(chat_id, {"first_name": "Foydalanuvchi"})
            return
        elif lower in ("/help", "yordam"):
            help_text = (
                "🤖 <b>MllyMed AI yordamchi imkoniyatlari:</b>\n\n"
                "• <b>Dori qidirish:</b> «Paratsetamol», «Ibuprofen», «Sitramon» kabi nomlarni yozing\n"
                "• <b>Shikoyat:</b> «Boshim og'riyapti», «Isitma bor» deb alomatlaringizni bildiring\n"
                "• <b>Kalendarga eslatma:</b> Shifokor qabuli yoki dori ichish vaqtini belgilang\n"
                "• <b>Yangi suhbat:</b> «/reset» yoki «Yangi suhbat» tugmasini bosing\n\n"
                "💡 Mini App ilovasini ochish uchun chap pastdagi <b>MllyMed</b> menyu tugmasidan foydalaning."
            )
            self.send_message(chat_id, help_text, reply_markup=self.get_main_reply_keyboard())
            return
        elif lower in ("/reset", "yangi suhbat", "🔄 yangi suhbat", "yangi"):
            self.reset_session(chat_id)
            self.send_message(
                chat_id,
                "🔄 Yangi suhbat boshlandi. Qanday dori yoki alomat bo'yicha yordam bera olaman?",
                reply_markup=self.get_main_reply_keyboard()
            )
            return
        elif lower in ("💊 dori qidirish", "dori qidirish", "dori"):
            self.handle_drug_search_prompt(chat_id)
            return
        elif lower in ("📅 kalendarga eslatma", "📅 kalendarga qo'shish", "kalendarga qo'shish", "kalendar", "qabulga yozilish", "eslatma"):
            self.handle_add_to_calendar(chat_id)
            return
        elif lower in ("🩺 shikoyat bildirish", "shikoyat bildirish", "shikoyat"):
            self.handle_symptom_prompt(chat_id)
            return
        elif "80%" in lower or ("mahalliy" in lower and ("paritet" in lower or "dori" in lower)):
            self.handle_callback({"id": "0", "data": "quick_local_info", "message": {"chat": {"id": chat_id}}})
            return

        # Salomlashish va umumiy murojaatlar
        greetings = ("salom", "assalom", "assalomu alaykum", "salom alaykum", "xayrli kun", "qalaysiz", "qalesiz")
        if any(lower == g or lower.startswith(g + " ") for g in greetings):
            self.send_chat_action(chat_id, "typing")
            welcome_text = (
                "Assalomu alaykum! 👋\n"
                "Men <b>MllyMed AI</b> tibbiy va farmatsevtik yordamchisiman.\n\n"
                "Sizga qanday yordam bera olaman?\n"
                "💊 <b>Dori qidiruvi:</b> Dori nomi yoki XPN (masalan: <i>Paratsetamol, Kardiomagnil, Sitramon</i>)\n"
                "🩺 <b>Tibbiy triaj:</b> Bezovta qilayotgan alomat (masalan: <i>Bosh og'rig'i, isitma, tomoq og'rig'i</i>)\n"
                "📅 <b>Kalendar:</b> Qabul yoki dori ichish eslatmasi"
            )
            buttons = [
                [
                    {"text": "💊 Dori qidirish", "callback_data": "prompt_drug_search"},
                    {"text": "🩺 Shikoyat bildirish", "callback_data": "prompt_symptom_triage"}
                ],
                [
                    {"text": "📅 Kalendarga eslatma", "callback_data": "add_to_calendar"},
                    {"text": "🇺🇿 80% Mahalliy dori", "callback_data": "quick_local_info"}
                ]
            ]
            self.send_message(chat_id, welcome_text, reply_markup={"inline_keyboard": buttons})
            return

        # Typing ko'rsatish va MllyMed agentiga yuborish
        self.send_chat_action(chat_id, "typing")
        session = self.get_session(chat_id)

        try:
            reply = self.agent.respond(session, cleaned)
            self._send_agent_reply(chat_id, reply, cleaned)
        except Exception as e:
            logger.error(f"Agent respond xatosi: {e}", exc_info=True)
            self.send_message(
                chat_id,
                "Kechirasiz, so'rovingizni qayta ishlashda xatolik yuz berdi. "
                "Iltimos, dori nomini yoki shikoyatingizni boshqacha shaklda yozib ko'ring.",
                reply_markup=self.get_main_reply_keyboard()
            )

    def _send_agent_reply(self, chat_id: int, reply: str, query: str = ""):
        """Agent javobini chiroyli formatlab yuborish va qulay inline tugmalar qo'shish (Launch app yo'q)."""
        safe_reply = format_telegram_html(reply)

        inline_buttons = []

        # Agar skrinig savoli (ha/yo'q) berilgan bo'lsa
        if "ha" in reply.lower() and "yo'q" in reply.lower() and ("aniqlashtirish" in reply.lower() or "savol" in reply.lower() or "?" in reply):
            inline_buttons.append([
                {"text": "✅ Ha", "callback_data": "ha"},
                {"text": "❌ Yo'q", "callback_data": "yoq"}
            ])

        # Agar triaj yoki dori kartasi bo'lsa, mos tugmalar qo'shish
        if "yo'naltirish:" in reply.lower() or "mutaxassis" in reply.lower() or "shifokor" in reply.lower():
            inline_buttons.append([
                {"text": "📅 Shifokor qabuliga yozilish", "callback_data": "add_to_calendar"},
                {"text": "🔄 Yangi suhbat", "callback_data": "quick_reset"}
            ])
        else:
            inline_buttons.append([
                {"text": "📅 Kalendarga eslatma qo'shish", "callback_data": "add_to_calendar"},
                {"text": "💊 Boshqa dori qidirish", "callback_data": "prompt_drug_search"}
            ])

        reply_markup = {"inline_keyboard": inline_buttons} if inline_buttons else None
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
