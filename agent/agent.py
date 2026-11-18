#!/usr/bin/env python3
"""O'RINDOR AGENT — dori ishonch kartasi + xavfsiz yo'naltirish (№17).

Ikki rejim, bitta agent:
  A. KARTA (yadro)   — dori nomi/XPN → davlat reyestri + referent narx +
                       INN guruhi + dalil holati. Har raqam manbasi bilan.
  B. TRIAJ (ikkinchi) — shikoyat → mutaxassis. Favqulodda qoidalar modeldan
                       oldin, majburiy skrining, xavfsiz default.

Uchta qat'iy chegara:
  1. TASHXIS YO'Q   — kasallik nomi aytilmaydi, da'vo qilinmaydi.
  2. DORI MASLAHATI YO'Q — triajda dori nomi/doza chiqmaydi. Kartada dori
     nomi — reyestr ma'lumoti, tavsiya emas.
  3. NAVBAT TASDIQLANMAYDI — faqat davlat havolasi; bron sahna ko'rsatilmaydi.

Ishga tushirish:
    python3 orindor/agent.py                 # jonli suhbat
    python3 orindor/agent.py --demo           # skriptlangan demo
    python3 orindor/agent.py --card paratsetamol
    python3 orindor/agent.py --ask "ko'kragim og'riyapti"
    python3 orindor/agent.py --stats
"""
from __future__ import annotations

import re
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import registry, render  # noqa: E402
from core.safety import (Level, check_emergency, read_answer,  # noqa: E402
                         screening_for, validate_card, validate_triage)
from core.session import Reminder, Session  # noqa: E402
from core.text import norm, tokens  # noqa: E402
from core.triage import (SPECIALISTS, Guess, Urgency, classify,  # noqa: E402
                         is_child_context, parse_age, age_from_bare, urgency)

HELP = """🤖 O'RINDOR agent — buyruqlar

  Dori tekshirish : «paratsetamol», «nurofen 200», «aspirin»
  Shikoyat        : «ko'kragim og'riyapti», «3 kundan beri boshim og'riyapti»
  Eslatma         : «eslatma ertaga 09:30»
  Boshqa          : eslatmalar · bordim · yangi · yordam

  Men tashxis qo'ymayman va dori tavsiya qilmayman. Kartadagi dori nomlari —
  davlat reyestridagi ma'lumot, tavsiya emas. Navbatni men tasdiqlamayman."""

CARD_WORDS = ("dori", "narx", "reyestr", "karta", "inn", "xpn", "sertifikat",
              "arzon", "qimmat", "original", "jenerik", "tabletka", "kapsula")


def _symptom_hit(text: str) -> bool:
    return bool(classify(text))


def detect_intent(text: str) -> str:
    """Xavfsizlik birinchi: shikoyat belgisi bo'lsa — triaj."""
    if _symptom_hit(text):
        return "triage"
    res = registry.resolve(text)
    if res["status"] in ("ok", "ambiguous"):
        return "card"
    if any(w in norm(text) for w in CARD_WORDS):
        return "card"
    # Bitta qisqa so'z ("florbaksinzz") — dori nomi bo'lishi ehtimoli yuqori.
    # Ilgari u triajga ketib, foydalanuvchiga aloqasiz tibbiy savol berardi.
    words = [w for w in norm(text).split() if w]
    if 1 <= len(words) <= 2 and all(len(w) >= 4 for w in words):
        return "card"
    return "triage"


def parse_reminder(text: str, subject: str = "eslatma") -> Reminder | None:
    low = text.lower()
    hm = re.search(r"\b(\d{1,2})[:.](\d{2})\b", low)
    if not hm:
        return None
    h, mi = int(hm.group(1)), int(hm.group(2))
    if not (0 <= h <= 23 and 0 <= mi <= 59):
        return None
    today = date.today()
    day = today
    if "ertaga" in low or "эртага" in low:
        day = today + timedelta(days=1)
    elif "indin" in low:
        day = today + timedelta(days=2)
    m = re.search(r"\b(\d{1,2})[./](\d{1,2})(?:[./](\d{2,4}))?", low)
    if m:
        dd, mm = int(m.group(1)), int(m.group(2))
        yy = int(m.group(3)) if m.group(3) else today.year
        if yy < 100:
            yy += 2000
        try:
            day = date(yy, mm, dd)
        except ValueError:
            return None
    when = datetime.combine(day, time(h, mi))
    return Reminder(subject=subject, when=when)


def _level_urgency(level: Level) -> Urgency:
    return Urgency.NOW if level is Level.NOW else Urgency.TODAY


def _raise(u: Urgency, level: Urgency) -> Urgency:
    return level if level.rank < u.rank else u


class Agent:
    """Holatni saqlaydigan agent. Model chaqirilmaydi — qaror qoidalarda."""

    def __init__(self, online: bool = True):
        self.online = online

    # ── asosiy kirish
    def respond(self, s: Session, text: str) -> str:
        s.add("user", text)
        t = norm(text)

        if t in ("yordam", "help", "?", "buyruqlar"):
            return s.say(HELP)
        if t in ("yangi", "boshidan", "reset", "tozala"):
            s.reset()
            return s.say("Boshidan boshladik. Dori nomini yoki shikoyatni yozing.")
        if t in ("eslatmalar", "eslatmalarim", "eslatma"):
            return s.say(render.reminder_list(s))
        if t.startswith("eslat") or t.startswith("eslatma"):
            subj = s.guess.label if s.guess else (s.card or {}).get("name") or "eslatma"
            r = parse_reminder(text, subject=subj)
            if r:
                s.reminders.append(r)
                return s.say(
                    f"⏰ Eslatma saqlandi: {r.when.strftime('%d.%m.%Y %H:%M')} — "
                    f"{r.subject}.\n"
                    "   Bu push emas: ilova ochiq bo'lganda vaqti kelgan eslatma "
                    "ko'rsatiladi. «eslatmalar» bilan tekshirasiz.")
            return s.say("Vaqtni tushunmadim. Masalan: «eslatma ertaga 09:30» "
                         "yoki «eslatma 25.11 10:00».")
        if any(w in t for w in ("bordim", "keldim", "bo'ldim", "o'tdim")):
            for r in s.reminders:
                if r.sent_at is None:
                    r.sent_at = datetime.now()
            return s.say(
                "✅ Eslatmalar to'xtatildi.\n"
                "   Agar retsept yozilgan bo'lsa — dorini tekshirishim mumkin: "
                "nomini yozing. Narx va dalil holatini reyestr bo'yicha "
                "ko'rsataman, taxmin qilmayman.")

        # ── 1. Favqulodda: har qanday rejimda birinchi
        rf = check_emergency(text, s.age, s.pregnant)
        if rf:
            s.stage = "emergency"
            s.mode = "triage"
            return s.say(validate_triage(render.emergency_text(rf)))

        # ── 2. Skrining javobi
        if s.screening is not None and s.stage == "screening":
            scr = s.screening
            ans = read_answer(text)
            s.screening = None
            if ans == "no":
                return self._route(s, force=_level_urgency(scr.safe), screened=True)
            if ans == "yes":
                s.stage = "emergency"
                return s.say(validate_triage(self._escalation(scr.reason)))
            # noaniq javob — xavfsiz tomon
            s.stage = "emergency"
            return s.say(validate_triage(
                self._escalation(scr.reason + " (javob noaniq — xavfsiz default)")))

        # ── 3. Rejim tanlash
        if s.mode is None:
            s.mode = detect_intent(text)

        if s.mode == "card":
            return self._card_turn(s, text)
        return self._triage_turn(s, text)

    # ── karta rejimi
    def _card_turn(self, s: Session, text: str) -> str:
        t = norm(text)

        if s.stage == "choose" and re.fullmatch(r"\d{1,2}", t):
            i = int(t) - 1
            if 0 <= i < len(s.candidates):
                return self._show_card(s, s.candidates[i].id)
            return s.say("Bunday raqam yo'q. Ro'yxatdagi raqamni yozing.")

        if s.stage == "card" and s.card:
            if any(w in t for w in ("nega", "arzon", "farq", "sabab")):
                return s.say(validate_card(render.why_text(s.card)))
            if any(w in t for w in ("ishon", "dalil", "sertifikat", "haqiqiy",
                                    "bioekviv", "be ")):
                return s.say(validate_card(render.evidence_text(s.card)))
            if any(w in t for w in ("manba", "qayerdan", "havola", "link")):
                lines = ["📚 Manbalar:"]
                for label, url in registry.registry_sources(s.card["id"]):
                    lines.append(f"   · {label}: {url}")
                return s.say("\n".join(lines))
            if any(w in t for w in ("boshqa", "yana", "keyingi")):
                s.stage = "card"
                return s.say("Boshqa dorini yozing — nomi yoki XPN.")
            if any(w in t for w in ("hisobot", "xulosa", "qisqa")):
                return s.say(validate_card(render.card_text(s.card)))
            # dori qidiruvi emas, shikoyat bo'lsa — triajga o'tamiz
            if _symptom_hit(text) and not registry.resolve(text)["candidates"]:
                s.mode = "triage"
                s.stage = "idle"
                return self._triage_turn(s, text)

        res = registry.resolve(text)
        if res["status"] == "none":
            if _symptom_hit(text):
                s.mode = "triage"
                s.stage = "idle"
                return self._triage_turn(s, text)
            return s.say(
                f"🔎 «{text.strip()}» reyestrdan topilmadi.\n"
                "   Boshqacha yozib ko'ring: XPN (paratsetamol) yoki savdo nomi "
                "(nurofen).\n"
                "   Reyestr 46 079 yozuvdan iborat — imlo farqi bo'lishi mumkin.")
        if res["status"] == "ambiguous":
            s.candidates = res["candidates"]
            s.stage = "choose"
            return s.say(render.ambiguity_text(text, res["candidates"]))
        return self._show_card(s, res["drug"]["id"], alias=res.get("alias"))

    def _show_card(self, s: Session, drug_id: int, alias: str | None = None) -> str:
        c = registry.card(drug_id)
        if not c:
            return s.say("Karta yig'ilmadi — ma'lumot fayli topilmadi.")
        s.card = c
        s.mode = "card"
        s.stage = "card"
        head = f"🔎 «{alias}» → XPN bo'yicha topildi.\n\n" if alias else ""
        return s.say(validate_card(head + render.card_text(c)))

    # ── triaj rejimi
    def _triage_turn(self, s: Session, text: str) -> str:
        # Agar foydalanuvchi dori qidirayotgan bo'lsa (va favqulodda skriningda bo'lmasa)
        if s.stage != "screening":
            res = registry.resolve(text)
            if res["status"] in ("ok", "ambiguous") and not _symptom_hit(text):
                s.mode = "card"
                s.stage = "idle"
                return self._card_turn(s, text)

        s.symptoms.append(text)

        age = parse_age(text)
        if age is not None:
            s.age = age
        if is_child_context(text):
            s.child = True
        if s.age is None and s.asked_age:
            bare = age_from_bare(text)
            if bare is not None and 0 <= bare <= 120:
                s.age = bare
        if not s.pregnant and re.search(r"homilador|боременн|pregnan", norm(text)):
            s.pregnant = True

        # «bolam» — yosh taxmin qilinmaydi, so'raladi (critic.md)
        if s.child and s.age is None and not s.asked_age:
            s.asked_age = True
            s.stage = "age"
            return s.say("👶 Bolangiz necha yoshda? Yoshni yozing (masalan: «3 yosh»). "
                         "Bu mutaxassisni to'g'ri tanlash uchun kerak.")

        combined = " ".join(s.symptoms)
        scr = screening_for(combined, s.age, s.pregnant)
        if scr and scr.topic not in s.asked_topics:
            s.asked_topics.append(scr.topic)
            s.screening = scr
            s.stage = "screening"
            return s.say(render.screening_text(scr))

        guesses = classify(combined, s.age, s.sex)
        if not guesses:
            if len(s.symptoms) == 1:
                return s.say(
                    "Tushundim. Aniqroq yo'naltirish uchun 2 savol:\n"
                    "   1) Qayerda bezovta qiladi — bosh, qorin, ko'krak, bo'g'im, "
                    "teri?\n"
                    "   2) Qanchadan beri — kunlarmi yoki haftalabmi?\n"
                    "   (Yoshni ham yozsangiz aniqroq bo'ladi.)")
            return s.say(validate_triage(render.triage_text(
                None, Urgency.ROUTINE, None, s.age, fallback=True)))

        top = guesses[0]
        if top.score < 1.5:
            top = Guess("terapevt", top.score, top.hits)
            fallback = True
        else:
            fallback = False
        second = guesses[1] if len(guesses) > 1 else None
        u = urgency(combined, top if not fallback else None, s.age, s.child)
        s.guess, s.urgency = top, u
        s.stage = "routed"
        s.booking = {"specialty": top.specialist, "urgency": u.text,
                     "slot": None, "confirmed": False}
        body = render.triage_text(top, u, second, s.age, fallback=fallback)
        if u is not Urgency.NOW:
            body += "\n\n" + render.booking_text(top.specialist, u)
        return s.say(validate_triage(body))

    def _route(self, s: Session, force: Urgency | None = None,
               screened: bool = False) -> str:
        combined = " ".join(s.symptoms)
        guesses = classify(combined, s.age, s.sex)
        top = guesses[0] if guesses else Guess("terapevt", 0.0, [])
        fallback = not guesses or top.score < 1.5
        if fallback:
            top = Guess("terapevt", 0.0, [])
        second = guesses[1] if len(guesses) > 1 else None
        u = force or urgency(combined, top if not fallback else None, s.age, s.child)
        s.guess, s.urgency = top, u
        s.stage = "routed"
        s.booking = {"specialty": top.specialist, "urgency": u.text,
                     "slot": None, "confirmed": False}
        body = render.triage_text(top, u, second, s.age, screened=screened,
                                  fallback=fallback)
        if u is not Urgency.NOW:
            body += "\n\n" + render.booking_text(top.specialist, u)
        return s.say(validate_triage(body))

    def _escalation(self, reason: str) -> str:
        return (
            "⛔ SHOSHILINCH — 103\n"
            f"   Sabab: {reason}.\n"
            "   Hoziroq 103 ni chaqiring yoki eng yaqin tez yordam bo'limiga "
            "boring.\n"
            "   Men bu holatda navbatga yozmayman va dori aytmayman."
        )

    # ── oflayn
    def reconnect(self, s: Session) -> str:
        sent = s.outbox.flush(online=True)
        if not sent:
            return s.say("Kutayotgan yozuv yo'q.")
        return s.say(f"Aloqa qaytdi — {len(sent)} ta yozuv lokal outbox faylga "
                     f"eksport qilindi (tarmoqqa yuborilmadi, server yo'q).")


# ── CLI ────────────────────────────────────────────────────────────────────

def _print_stats() -> None:
    st = registry.stats()
    print("📊 O'RINDOR — ma'lumot holati")
    print(f"   Reyestr yozuvi     : {st.get('drugs'):,}".replace(",", " "))
    print(f"   Mahalliy / import  : {st.get('local'):,} / {st.get('import'):,}"
          .replace(",", " "))
    print(f"   XPN guruhlari      : {st.get('inn_groups'):,}".replace(",", " "))
    print(f"   Referent narx      : {st.get('referent_prices'):,} "
          f"({st.get('price_coverage_pct')}% qamrov)".replace(",", " "))
    print(f"   Chegara narx       : {st.get('details')} yozuv")
    print(f"   Manba              : api.mpa.uz (ochiq) · lex.uz (17 hujjat)")
    from core import sources  # noqa: PLC0415
    print(f"   GMP reyestri       : {sources.status_of('https://uzpharm-gxp.uz')} "
          f"(uzpharm-gxp.uz/registry2, registry6)")


DIALOGUES = [
    ("Ko'kragim og'riyapti", ["yo'q", "eslatma ertaga 09:30"]),
    ("Qon qusdim", []),
    ("Yuzimning yarmi qimirlamayapti", []),
    ("Bolam tutqanoq tutdi", []),
    ("3 kundan beri boshim kuchli og'riyapti", ["yo'q"]),
    ("Ko'p kunlardan beri holsizman", []),
    ("Tishim qattiq og'riyapti", []),
    ("Tushkunman, hech narsa qiziqtirmaydi", []),
    ("Qornimning o'ng tomoni qattiq og'riyapti, qusdim, isitmam bor", []),
    ("Bolam 39 isitma bilan yotibdi", ["3 yosh", "yo'q"]),
]


def _priced_queries(n: int = 2) -> list[str]:
    """Narxi bor XPN larni topadi — demoda narx blokini ko'rsatish uchun."""
    out = []
    for g in registry.stats().get("top_inn", []):
        c = registry.search(g["inn"], 1)
        if c and c[0].has_price:
            out.append(g["inn"])
        if len(out) >= n:
            break
    return out


def run_demo() -> None:
    _print_stats()
    ag = Agent()

    print("\n" + "═" * 78)
    print("A) KARTA REJIMI — dori ishonch kartasi (real reyestr)")
    print("═" * 78)
    queries = ["paratsetamol", "nurofen"] + _priced_queries(1)
    for q in queries:
        s = Session()
        print(f"\n👤 {q}")
        out = ag.respond(s, q)
        print("🤖 " + out.replace("\n", "\n   "))
        if s.stage == "card":
            print("\n👤 nega arzon?")
            print("🤖 " + ag.respond(s, "nega arzon?").replace("\n", "\n   "))

    print("\n" + "═" * 78)
    print("B) TRIAJ REJIMI — favqulodda, skrining, xavfsiz default")
    print("═" * 78)
    for opener, follow in DIALOGUES:
        s = Session()
        print(f"\n👤 {opener}")
        print("🤖 " + ag.respond(s, opener).replace("\n", "\n   "))
        for f in follow:
            print(f"\n👤 {f}")
            print("🤖 " + ag.respond(s, f).replace("\n", "\n   "))
            if s.stage == "emergency":
                break
        if s.stage == "routed":
            print("\n👤 eslatmalar")
            print("🤖 " + ag.respond(s, "eslatmalar").replace("\n", "\n   "))

    print("\n" + "═" * 78)
    print("C) OFFLINE — haqiqiy disk yozuvi")
    print("═" * 78)
    s = Session()
    ag2 = Agent(online=False)
    print("👤 Boshim og'riyapti")
    print("🤖 " + ag2.respond(s, "Boshim og'riyapti").split("\n")[0])
    s.outbox.add("triage", {"specialty": s.guess.specialist if s.guess else "—"})
    print(f"   navbatda: {s.outbox.pending()} yozuv → {s.outbox.path}")
    print("🤖 " + ag2.reconnect(s))


def run_interactive() -> None:
    ag, s = Agent(), Session()
    print("O'RINDOR agent · chiqish: 'exit' · yordam: 'yordam'\n")
    print("🤖 Dori nomini yoki shikoyatni yozing. Tashxis qo'ymayman.\n")
    while True:
        try:
            u = input("👤 ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if u.lower() in ("exit", "quit", "chiqish"):
            break
        if not u:
            continue
        print("🤖 " + ag.respond(s, u).replace("\n", "\n   ") + "\n")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = sys.argv[1:]
    if "--demo" in args:
        run_demo()
    elif "--stats" in args:
        _print_stats()
    elif "--card" in args:
        q = " ".join(args[args.index("--card") + 1:]) or "paratsetamol"
        s = Session()
        print(Agent().respond(s, q))
    elif "--ask" in args:
        q = " ".join(args[args.index("--ask") + 1:])
        s = Session()
        print(Agent().respond(s, q))
    else:
        run_interactive()


if __name__ == "__main__":
    main()
