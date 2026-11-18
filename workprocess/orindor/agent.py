"""
O'RINDOR · AGENT — suhbat orqali mutaxassisga yo'naltirish (№17 ekotizimi)
=====================================================================
VAZIFA (foydalanuvchi talab qilganidek, tor):
    Odam erkin, oddiy tilda gapiradi → agent kasallik TURINI aniqlaydi →
    QAYSI MUTAXASSISGA borishni aytadi → navbatga yozadi → eslatadi.

QAT'IY CHEGARA — uchta "YO'Q":
    1. TASHXIS YO'Q     — agent kasallik nomini aytmaydi ("sizda gastrit" ❌)
    2. DORI YO'Q        — dori nomi, doza, tavsiya chiqarilmaydi
    3. RETSEPT YO'Q     — retsept yozilmaydi, o'zgartirilmaydi

NEGA "AGENT", FAQAT "MODEL" EMAS:
    Model  — bitta qadam: matn → mutaxassis. Bu yerda L2 qatlami.
    Agent  — ko'p qadamli sikl: holat saqlaydi, qayta so'raydi, xavfni
             tekshiradi, navbatga yozadi, eslatma rejalashtiradi, oflayn
             ishlaydi va ulanish qaytganda sinxronlaydi.
    Ya'ni: model — agentning ICHIDAGI bitta asbob. Mahsulot — agent.

QATLAMLAR (pretsedent buzilmaydi):
    L0  FAVQULODDA  — qat'iy qoidalar, modeldan USTUN. Darhol 103.
    L1  YOSH/HOLAT  — homiladorlik, chaqaloq, surunkali holat → yo'naltirish
    L2  MUTAXASSIS  — ballash modeli (izohlanadigan)
    L3  TIL         — faqat matn shakllantirish (LLM o'rni shu yerda,
                      qaror chiqarmaydi)

Ishga tushirish:  python3 egiz/agent.py          (interaktiv demo)
                  python3 egiz/agent.py --demo    (avtomatik suhbat)
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from pathlib import Path

TODAY = date.today()


# ============================================================
# 0. LUG'AT — UZ (lotin/kirill) + RU
# ============================================================

CYR = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
       "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
       "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
       "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
       "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
       "ў": "o", "қ": "q", "ғ": "g", "ҳ": "h"}


VOWELS = set("aeiou")


# Ovoz jihatidan juft undoshlar — bitta sinfga keltiriladi.
# Sabab: o'zbekchada qo'shimcha oldidan undosh jarangsizlanadi/jaranglashadi:
#   ko'krak → ko'kragim (k→g),  quloq → qulog'im (q→g'),  tish → tishim
VOICE = {"k": "K", "g": "K", "q": "K", "p": "P", "b": "P", "t": "T", "d": "T",
         "s": "S", "z": "S", "f": "F", "v": "F", "x": "X", "h": "X",
         "j": "C", "c": "C"}


def skel(word: str) -> str:
    """Undosh skelet, ovoz sinflari bilan: 'ko'kragim'→'KKRM', 'ko'krak'→'KKRK'."""
    w = norm(word).replace("'", "")
    return "".join(VOICE.get(ch, ch.upper()) for ch in w if ch not in VOWELS)


def word_match(sig_word: str, text_skels: list[str]) -> bool:
    """Signal so'zi matndagi biror so'zga mos keladimi.

    Qoida: matndagi so'zning skeleti signal skeletidan boshlansa — mos.
    Prefiks yetarli, chunki qo'shimcha undosh QO'SHADI, mavjudini o'zgartirmaydi:
        ko'krak → ko'kragim : KKRK  → KKRKM   ✓ prefiks
        qorin   → qornim    : KRN   → KRNM    ✓ prefiks (unli tushgan)
        tish    → tishim    : TS    → TSM     ✓ prefiks
    Jarangsizlanish (k↔g↔q) VOICE jadvalida hal qilingan, shuning uchun
    oxirgi undoshni kesish SHART EMAS — kesish «bosim»→«bo'sh» kabi
    yolg'on mosliklarni keltirib chiqargan edi (o'lchandi).
    """
    sk = skel(sig_word)
    if len(sk) < 2:
        return False
    # ikki tomonlama prefiks: matn so'zi ham, signal so'zi ham qisqaroq bo'lishi mumkin
    #   og'ri → og'riyapti     (ts uzunroq)
    #   kuchsiz ↔ kuchsizlan   (signal uzunroq)
    return any(ts.startswith(sk) or (len(ts) >= 3 and sk.startswith(ts))
               for ts in text_skels)


def phrase_match(phrase: str, text: str) -> tuple[bool, bool]:
    """(aniq moslik, skelet mosligi)."""
    t = norm(text)
    parts = norm(phrase).split()
    if not parts:
        return False, False
    exact = norm(phrase) in t
    tskels = [skel(w) for w in t.split()]
    loose = all(word_match(p, tskels) for p in parts)
    return exact, loose


def norm(text: str) -> str:
    """Kirill/lotin, apostrof variantlari, ortiqcha bo'shliq — hammasi bir shaklga."""
    t = unicodedata.normalize("NFKC", text).lower()
    t = "".join(CYR.get(ch, ch) for ch in t)
    t = t.replace("ʻ", "'").replace("ʼ", "'").replace("‘", "'").replace("`", "'")
    t = re.sub(r"[^a-z0-9' ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ============================================================
# 1. L0 — FAVQULODDA BELGILAR (qat'iy, modeldan ustun)
# ============================================================

class Emergency(Enum):
    E1 = "SHOSHILINCH — 103 ni hoziroq chaqiring"


@dataclass
class RedFlag:
    code: str
    pattern: list[str]          # barchasi matnda bo'lishi shart (AND)
    any_of: list[str] = field(default_factory=list)   # yoki shu'lardan biri
    text: str = ""
    action: str = "103"


RED_FLAGS: list[RedFlag] = [
    RedFlag("CHEST", ["ko'krak"], ["nafas", "sovuq ter", "chap qo'l", "siqil", "siqilyap", "bosim", "yurak"],
            "Ko'krak og'rig'i + nafas olish/qo'l belgisi — shoshilinch tekshiruv kerak"),
    RedFlag("BREATH", ["nafas"], ["bo'g'il", "qisil", "siqil", "yetishmay", "qiynal",
                                  "olmayapman", "olmayman", "bo'g'ilib", "siqilyap"],
            "Nafas olish qiyinlashgan"),
    RedFlag("STROKE_FACE", ["yuz"], ["qiyshay", "shalpay", "uvish", "sezmay"],
            "Yuz qiyshayishi/sezmasligi — vaqt hal qiluvchi holat, hoziroq 103"),
    RedFlag("STROKE_ARM", ["qo'l"], ["kuchsiz", "shalpay", "ko'tarolmay", "kotarolmay", "uvishmay"],
            "Qo'l kuchsizligi — vaqt hal qiluvchi holat, hoziroq 103"),
    RedFlag("STROKE_SPEECH", ["gap"], ["chalkash", "olmay", "chiqmay", "tushunmay", "tutil"],
            "Gap buzilishi — vaqt hal qiluvchi holat, hoziroq 103"),
    RedFlag("UNCONSCIOUS", ["hush"], ["ketdi", "yo'qol", "yoqol", "befarq"],
            "Hushidan ketish"),
    RedFlag("BLEED", ["qon"], ["ko'p", "to'xtamay", "kuchli", "quyul"],
            "To'xtamaydigan qon ketish"),
    RedFlag("SUICIDE", ["o'zim"], ["o'ldir", "jonimga", "yashashni xohlamay", "o'lishni"],
            "O'z joniga qasd fikri — yolg'iz qolmang"),
    RedFlag("SUICIDE2", ["o'lish"], ["xohlay", "istay"], "O'lim haqidagi fikrlar"),
    RedFlag("POISON", ["zahar"], ["ichib", "ichdim", "yutib", "yutdim", "oldim"], "Zaharlanish"),
    RedFlag("OVERDOSE", ["doza"], ["oshdi", "ko'p ichdim", "oshib"], "Dori dozasi oshib ketdi"),
    RedFlag("PREGBLEED", ["homiladorman"], ["qon", "og'riq", "suv"], "Homiladorlikda qon ketish/og'riq"),
    RedFlag("BABYFEVER", ["chaqaloq", "bola"], ["isitma", "38", "39", "40"], "Kichik bolada yuqori isitma"),
    RedFlag("NECKSTIFF", ["bo'yin"], ["qot", "qattiq", "egilmay"], "Bo'yin qotishi + isitma"),
    RedFlag("YURAK", ["yurak", "o'yna"], ["terla", "nafas", "siqil", "hush", "ko'ngil", "uvish"],
            "Yurak urishi buzilishi + terlash/nafas — shoshilinch tekshiruv kerak"),
    RedFlag("ABDOMEN", ["qorin"], ["qattiq", "taqab", "chidab bo'lmay", "pichoq"],
            "Qattiq, chidab bo'lmaydigan qorin og'rig'i"),
]

EMERGENCY_TEXT = (
    "⛔ Bu holat shoshilinch yordam talab qiladi.\n"
    "   Hoziroq 103 ni chaqiring yoki eng yaqin tez yordam bo'limiga boring.\n"
    "   Men bu holatda navbatga yozmayman — bu xavfli.\n"
    "   {why}"
)


def _has(phrase: str, text: str) -> bool:
    """So'z matnda bormi — aniq yoki undosh skelet bo'yicha.

    Nega skelet: 'ko'kragim siqilyapti' da «ko'krak» so'zi YO'Q (qo'shimcha),
    lekin skeleti «kkrk» bor. Qat'iy qatlamda bu farq hal qiluvchi —
    o'lchovda aynan shu sabab favqulodda holat o'tkazib yuborilgan edi.
    """
    exact, loose = phrase_match(phrase, text)
    return exact or loose


def check_emergency(text: str, age: int | None, pregnant: bool) -> RedFlag | None:
    t = norm(text)
    if age is None:
        mo = re.search(r"\b(\d{1,2})\s*oylik\b", t)
        if mo:
            age = 0 if int(mo.group(1)) < 12 else 1
        elif re.search(r"\bchaqaloq\b", t):
            age = 0
    tskel = " " + " ".join(skel(w) for w in t.split()) + " "
    for rf in RED_FLAGS:
        if not all(_has(p, text) for p in rf.pattern):
            continue
        if rf.any_of and not any(_has(a, text) for a in rf.any_of):
            continue
        return rf
    # yoshga bog'liq qat'iy qoida: 1 yoshgacha isitma
    if age is not None and age < 1 and any(w in t for w in ("isitma", "harorat", "38", "39")):
        return RedFlag("INFANT_FEVER", [], [], "Bir yoshgacha bolada isitma")
    if pregnant and any(w in t for w in ("qon", "suv ketdi", "og'riq kuchli")):
        return RedFlag("PREG", [], [], "Homiladorlikda shoshilinch belgi")
    return None


# ============================================================
# 2. L2 — MUTAXASSIS MODELI (izohlanadigan ballash)
# ============================================================

SPECIALISTS = {
    "terapevt":            "Terapevt (oilaviy shifokor)",
    "kardiolog":           "Kardiolog",
    "nevrolog":            "Nevrolog",
    "gastroenterolog":     "Gastroenterolog",
    "pulmonolog":          "Pulmonolog",
    "endokrinolog":        "Endokrinolog",
    "urolog":              "Urolog",
    "ginekolog":           "Ginekolog",
    "travmatolog":         "Travmatolog-ortoped",
    "lor":                 "LOR (quloq-tomoq-burun)",
    "oftalmolog":          "Oftalmolog (ko'z)",
    "dermatolog":          "Dermatovenerolog",
    "stomatolog":          "Stomatolog",
    "onkolog":             "Onkolog",
    "psixiatr":            "Psixiatr / psixoterapevt",
    "ftiziatr":            "Ftiziatr (sil)",
    "infeksionist":        "Infeksionist",
    "allergolog":          "Allergolog-immunolog",
    "revmatolog":          "Revmatolog",
    "nefrolog":            "Nefrolog",
    "gematolog":           "Gematolog",
    "pediatr":             "Pediatr",
    "jarroh":              "Jarroh",
    "proktolog":           "Proktolog",
    "mammolog":            "Mammolog",
}

# signal → {mutaxassis: og'irlik}
SIGNALS: dict[str, dict[str, float]] = {
    # yurak
    "ko'krak og'ri": {"kardiolog": 3.0, "terapevt": 1.0},
    "yurak tez": {"kardiolog": 2.5, "endokrinolog": 1.0},
    "yurak urib": {"kardiolog": 2.5},
    "bosim yuqori": {"kardiolog": 2.5, "nefrolog": 1.0},
    "bosim past": {"kardiolog": 2.0, "terapevt": 1.0},
    "oyoq shish": {"kardiolog": 2.0, "nefrolog": 1.5},
    # nafas
    "yo'tal": {"pulmonolog": 2.0, "lor": 1.0, "terapevt": 1.0, "ftiziatr": 0.5},
    "nafas qis": {"pulmonolog": 2.5, "kardiolog": 1.0},
    "xirill": {"pulmonolog": 2.5},
    "yo'talda qon": {"ftiziatr": 3.0, "pulmonolog": 2.0, "onkolog": 1.5},
    "isitma": {"terapevt": 2.0, "infeksionist": 1.5, "pediatr": 1.0},
    # hazm
    "qorin og'ri": {"gastroenterolog": 2.5, "jarroh": 1.0, "ginekolog": 0.8},
    "qorin dam": {"gastroenterolog": 2.5},
    "jigar": {"gastroenterolog": 2.5, "infeksionist": 1.0},
    "ich ket": {"gastroenterolog": 2.0, "infeksionist": 1.5},
    "qabziyat": {"gastroenterolog": 2.0, "proktolog": 1.0},
    "qichish": {"proktolog": 2.0, "dermatolog": 1.0},
    "anal": {"proktolog": 2.5},
    # nevrolog
    "bosh og'ri": {"nevrolog": 2.0, "terapevt": 1.0, "lor": 0.5},
    "bosh aylan": {"nevrolog": 2.0, "lor": 1.5, "kardiolog": 0.8},
    "uvish": {"nevrolog": 2.5},
    "hush": {"nevrolog": 1.5},
    "uyqu": {"nevrolog": 1.5, "psixiatr": 1.5},
    "xotira": {"nevrolog": 2.0},
    # ruhiyat
    "xavotir": {"psixiatr": 2.5},
    "tushkun": {"psixiatr": 2.5},
    "asabiy": {"psixiatr": 2.0, "endokrinolog": 0.8},
    "stress": {"psixiatr": 2.0},
    "panik": {"psixiatr": 2.5},
    # endokrin
    "vazn": {"endokrinolog": 2.0, "gastroenterolog": 1.0},
    "chanq": {"endokrinolog": 2.5, "nefrolog": 1.0},
    "siyish ko'p": {"endokrinolog": 2.0, "urolog": 2.0},
    "qalqon": {"endokrinolog": 2.5},
    "soch to'kil": {"endokrinolog": 1.5, "dermatolog": 1.5},
    # buyrak/urolog
    "bel og'ri": {"nevrolog": 1.6, "travmatolog": 1.4, "nefrolog": 1.0, "urolog": 0.6},
    "siydik": {"urolog": 2.5, "nefrolog": 1.2},
    "bosim": {"kardiolog": 2.2, "terapevt": 1.0},
    "tugun": {"mammolog": 2.6, "onkolog": 1.4},
    "qizar": {"allergolog": 2.4, "dermatolog": 1.2},
    "toshma": {"dermatolog": 2.2, "allergolog": 1.0},
    "ko'ngil": {"gastroenterolog": 2.0},
    "hazm": {"gastroenterolog": 2.0},
    "asab": {"psixiatr": 2.0, "nevrolog": 1.2},
    "uyqu": {"psixiatr": 1.8, "nevrolog": 1.0},
    "achish": {"urolog": 1.5},
    "siyish og'ri": {"urolog": 2.5, "nefrolog": 1.0},
    "siyish tez": {"urolog": 2.0},
    "buyrak": {"nefrolog": 2.5, "urolog": 1.5},
    # ginekologiya
    "hayz": {"ginekolog": 2.5},
    "homilador": {"ginekolog": 2.5},
    "ayol": {"ginekolog": 1.0},
    "ko'krak bez": {"mammolog": 2.5, "ginekolog": 1.5},
    # teri
    "toshma": {"dermatolog": 2.5, "allergolog": 1.5},
    "teri qich": {"dermatolog": 2.5, "allergolog": 1.0},
    "dog'": {"dermatolog": 2.0, "onkolog": 0.5},
    "yara": {"dermatolog": 1.5, "jarroh": 1.0},
    # ko'z/quloq
    "ko'z": {"oftalmolog": 2.5},
    "ko'rish": {"oftalmolog": 2.5},
    "quloq": {"lor": 2.5},
    "tomoq": {"lor": 2.5, "terapevt": 0.8},
    "burun": {"lor": 2.5, "allergolog": 0.8},
    "hid": {"lor": 2.0},
    # tayanch
    "bo'g'im": {"revmatolog": 2.0, "travmatolog": 1.5},
    "tizza": {"travmatolog": 2.5, "revmatolog": 1.0},
    "suyak": {"travmatolog": 2.5},
    "jarohat": {"travmatolog": 2.5, "jarroh": 1.0},
    "yelka": {"travmatolog": 2.0, "nevrolog": 1.0},
    # qon
    "qon kam": {"gematolog": 2.5, "terapevt": 1.0},
    "tez charch": {"gematolog": 1.5, "terapevt": 1.5, "endokrinolog": 1.0},
    "limfa": {"gematolog": 2.0, "onkolog": 1.5},
    # boshqa
    "tish": {"stomatolog": 3.0},
    "og'iz yara": {"stomatolog": 2.0},
    "allergiya": {"allergolog": 2.5},
    "emlash": {"terapevt": 1.5, "pediatr": 1.5},
    "tekshiruv": {"terapevt": 2.0},
    "profilaktika": {"terapevt": 2.0},
}


@dataclass
class Guess:
    specialist: str
    score: float
    hits: list[str]

    @property
    def label(self) -> str:
        return SPECIALISTS[self.specialist]


def classify(text: str, age: int | None = None, sex: str | None = None) -> list[Guess]:
    """L2 model: matn → mutaxassis reytingi. Izohlanadigan: har ball qaysi so'zdan."""
    t = norm(text)
    tskel = " " + " ".join(skel(w) for w in t.split()) + " "
    scores: dict[str, float] = {}
    hits: dict[str, list[str]] = {}
    for phrase, targets in SIGNALS.items():
        p = norm(phrase)
        if not p:
            continue
        exact, skel_hit = phrase_match(phrase, text)
        if not (exact or skel_hit):
            continue
        mult = 1.0 if exact else 0.85        # skelet mosligi — bir oz ehtiyotkor
        for sp, w in targets.items():
            scores[sp] = scores.get(sp, 0.0) + w * mult
            hits.setdefault(sp, []).append(phrase)

    # yoshga bog'liq tuzatish
    if age is not None:
        if age < 15:
            if "pediatr" in scores:
                scores["pediatr"] *= 1.8
            if "terapevt" in scores:
                scores["terapevt"] *= 0.4   # kattalar shifokori emas
        if age < 15 and "terapevt" in scores:
            scores["terapevt"] *= 0.6
        if age >= 15 and "pediatr" in scores:
            scores["pediatr"] *= 0.3
    if sex == "erkak" and "ginekolog" in scores:
        del scores["ginekolog"]
        hits.pop("ginekolog", None)

    if not scores:
        return []
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    return [Guess(sp, round(sc, 2), hits.get(sp, [])) for sp, sc in ranked]


# ============================================================
# 3. AGENT HOLATI VA ASBOBLAR
# ============================================================

class Stage(Enum):
    GREET = "salomlashish"
    COLLECT = "ma'lumot yig'ish"
    SUGGEST = "mutaxassis tavsiyasi"
    BOOK = "navbatga yozish"
    REMIND = "eslatma"
    EMERGENCY = "shoshilinch"
    DONE = "yakun"


class Urgency(Enum):
    NOW = ("SHOSHILINCH", "bugun, iloji boricha tez", 0)
    SOON = ("1–3 kun", "3 kun ichida", 2)
    ROUTINE = ("1 hafta", "1 hafta ichida", 7)
    LATER = ("2–4 hafta", "2–4 hafta ichida", 21)

    @property
    def text(self) -> str:
        return self.value[0]

    @property
    def when(self) -> str:
        return self.value[1]

    @property
    def days(self) -> int:
        return self.value[2]


@dataclass
class Booking:
    specialty: str
    urgency: Urgency
    slot: datetime | None = None
    confirmed: bool = False


@dataclass
class Reminders:
    """3 marta tasdiqlanmaguncha eslatma. Motivatsion, qiziqarli matn."""
    booking: Booking
    sent: list[datetime] = field(default_factory=list)
    confirmed: bool = False
    max_n: int = 3

    TEMPLATES = [
        ("ertaga", "⏰ Ertaga soat {t} da {sp} qabuli. "
                   "Bitta savol: ertaga ertalab sizni nima to'xtatishi mumkin? "
                   "Javobini o'ylab qo'ying — va baribir boring. 🙂"),
        ("bugun", "📌 Bugun soat {t} da {sp}. Yo'lda 10 daqiqa erta chiqing — "
                  "navbat emas, xotirjamlik uchun."),
        ("oxirgi", "🔔 Oxirgi eslatma: bugun {t}, {sp}. "
                   "«Bordim» deb yozing — keyin sizni bezovta qilmayman. "
                   "Bormasangiz ham yozing, boshqa vaqtga qo'yamiz."),
    ]

    def schedule(self) -> list[str]:
        out = []
        sp = SPECIALISTS[self.booking.specialty]
        t = self.booking.slot.strftime("%H:%M") if self.booking.slot else "—"
        for i, (_, tpl) in enumerate(self.TEMPLATES[: self.max_n]):
            out.append(tpl.format(sp=sp, t=t))
        return out

    def send_next(self, now: datetime | None = None) -> str | None:
        if self.confirmed or len(self.sent) >= self.max_n:
            return None
        now = now or datetime.now()
        sp = SPECIALISTS[self.booking.specialty]
        t = self.booking.slot.strftime("%H:%M") if self.booking.slot else "—"
        tpl = self.TEMPLATES[len(self.sent)][1]
        self.sent.append(now)
        return tpl.format(sp=sp, t=t)

    def confirm(self) -> None:
        self.confirmed = True
        self.booking.confirmed = True


# oflayn navbat — internet yo'q bo'lsa saqlanadi
@dataclass
class OfflineQueue:
    items: list[dict] = field(default_factory=list)

    def add(self, action: str, payload: dict) -> None:
        self.items.append({"action": action, "payload": payload,
                           "created": datetime.now().isoformat()})

    def sync(self, online: bool) -> int:
        if not online:
            return 0
        n = len(self.items)
        self.items.clear()
        return n


# ============================================================
# 4. AGENT
# ============================================================

@dataclass
class Session:
    stage: Stage = Stage.GREET
    age: int | None = None
    sex: str | None = None
    pregnant: bool = False
    turns: list[dict] = field(default_factory=list)
    symptoms: list[str] = field(default_factory=list)
    guess: Guess | None = None
    urgency: Urgency = Urgency.ROUTINE
    booking: Booking | None = None
    reminders: Reminders | None = None
    offline: OfflineQueue = field(default_factory=OfflineQueue)
    red_flag: RedFlag | None = None
    asked_age: bool = False
    child: bool = False

    # --- yordamchi
    def add(self, role: str, text: str) -> None:
        self.turns.append({"role": role, "text": text, "at": datetime.now().isoformat()})

    def say(self, text: str) -> str:
        self.add("agent", text)
        return text


# Diqqat: "tashxis" so'zining O'ZI taqiqlanmagan — agent "tashxis qo'ymayman"
# deb aytishi kerak. Taqiq faqat DA'VO shakllari va DORI tavsiyasi uchun.
BANNED = re.compile(
    r"(sizda\s+\w+\s+(bor|kasalligi|yallig'lanish))|"
    r"\b(bronxit|gastrit|angina|diabet|gipertoniya|astma|artrit|infarkt|insult)\b|"
    r"\b(tabletka iching|kapsula iching|qabul qiling|doza oshiring|retsept yoz)\b|"
    r"\b\d+\s*mg\b", re.I)

# dorilar nomi — agent HECH QACHON aytmaydi
DRUGS = re.compile(
    r"\b(paracetamol|paratsetamol|ibuprofen|analgin|aspirin|amoksitsillin|"
    r"azitromitsin|metformin|levotiroksin|omeprazol|nurofen|panadol|"
    r"citramon|spazmalgon|suprastin|mezim|smecta|lineks)\b", re.I)


# ============================================================
# 3b. DALIL QATLAMI — «qayerdan bu raqam?»
# ============================================================
# Qoida: agent og'zidan chiqqan HAR BIR raqam yonida hujjat bo'lishi shart.
# Manba — egiz/data/facts.json (17 ta tekshirilgan fakt, lex.uz dan olingan).
FACTS_PATH = Path(__file__).resolve().parent / "data" / "facts.json"


def load_facts() -> dict:
    try:
        return json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def fact(fid: str) -> dict | None:
    for f in load_facts().get("facts", []):
        if f.get("id") == fid:
            return f
    return None


def why_number() -> str:
    """Retseptdan keyingi narx savoliga javob — har raqam hujjat bilan.

    Bu agentning triaj qismi emas: bu O'RINDOR ning ikkinchi yarmi (A2/A3).
    Triaj «kimga» deydi, bu qatlam «qancha va nega shuncha» deydi.
    """
    d = load_facts()
    pm = d.get("price_model", {})
    ex = pm.get("example", {})
    f09 = fact("F09") or {}
    f07 = fact("F07") or {}
    if not ex:
        return "Narx ma'lumoti yuklanmadi — qoida: raqamni hujjatsiz aytmayman."

    return (
        "Retsept chiqsa — narxni tekshirish mumkin:\n"
        f"  Original (import)      : {ex.get('import_yakuniy_narx_som'):,} so'm\n"
        f"  Mahalliy jenerik       : {ex.get('mahalliy_yakuniy_narx_som'):,} so'm "
        f"({ex.get('farq_foiz')}% arzon)\n"
        "\n"
        f"Nega shunday: {f09.get('claim', '')}.\n"
        f"  Hisob: {f07.get('claim', '')}\n"
        "\n"
        f"Manba: VM {f09.get('doc')}-son qarori, {f09.get('date')} — "
        f"{f09.get('url')}\n"
        "  (Bojxona to'lovi 0 deb olindi — eng qulay holat.)"
    )


def safety_check(text: str) -> str:
    """Chiqish matnini tekshiradi — tashxis yoki dori nomi o'tib ketmasin."""
    t = DRUGS.sub("[dori nomi olib tashlandi]", text)
    t = BANNED.sub("[tashxis olib tashlandi]", t)
    return t


class Agent:
    def __init__(self, online: bool = True):
        self.online = online

    # ---------- asosiy kirish ----------
    def respond(self, s: Session, user_text: str) -> str:
        s.add("user", user_text)

        # L0 — favqulodda: har qanday holatda birinchi tekshiriladi
        rf = check_emergency(user_text, s.age, s.pregnant)
        if rf:
            s.stage = Stage.EMERGENCY
            s.red_flag = rf
            return s.say(safety_check(EMERGENCY_TEXT.format(why="Sabab: " + rf.text)))

        # «2 oylik», «6 oylik» — yosh oylarda
        mo = re.search(r"\b(\d{1,2})\s*oylik\b", norm(user_text))
        if mo and s.age is None:
            s.age = 0 if int(mo.group(1)) < 12 else 1

        # bola haqida gap ketyaptimi — yosh so'ralmasa ham pediatrga og'amiz
        if not s.child and re.search(
                r"\b(bolam|bolasi|bolasi|o'g'lim|qizim|chaqaloq|farzand|bebek|go'dak)\b",
                norm(user_text)):
            s.child = True
            if s.age is None:
                s.age = 4          # "bola" — yosh taxmini emas, faqat pediatr og'irligi

        # homiladorlik — favqulodda tekshiruvdan keyin, lekin qat'iy belgi
        if not s.pregnant and re.search(r"homilador|боременн|pregnan", norm(user_text)):
            s.pregnant = True

        # yosh/parametr ajratish (bir marta)
        if s.age is None and not s.asked_age:
            m = re.search(r"\b(\d{1,3})\s*(yosh|yil|года|лет)?\b", norm(user_text))
            if m and 0 <= int(m.group(1)) <= 120 and m.group(2):
                s.age = int(m.group(1))

        # holat mashinasi
        if s.stage in (Stage.GREET, Stage.COLLECT):
            return self._collect(s, user_text)
        if s.stage == Stage.SUGGEST:
            return self._handle_suggest(s, user_text)
        if s.stage == Stage.BOOK:
            return self._handle_book(s, user_text)
        if s.stage == Stage.REMIND:
            return self._handle_remind(s, user_text)
        if s.stage == Stage.EMERGENCY:
            return s.say("Siz shoshilinch holatdasiz. Iltimos, 103 ni chaqiring. "
                         "Men bu holatda boshqa tavsiya bermayman.")
        return s.say("Suhbat yakunlandi. Yangi savol bo'lsa, qaytadan boshlaymiz.")

    # ---------- L2: ma'lumot yig'ish ----------
    def _collect(self, s: Session, text: str) -> str:
        s.symptoms.append(text)
        combined = " ".join(s.symptoms)
        guesses = classify(combined, s.age, s.sex)

        if not guesses:
            if len(s.symptoms) == 1:
                s.asked_age = True
                return s.say(
                    "Tushundim. Yana bir-ikki savol — shunda to'g'ri mutaxassisni "
                    "ayta olaman.\n"
                    "1) Qayerda bezovta qiladi — bosh, qorin, ko'krak, bo'g'im, teri?\n"
                    "2) Qanchadan beri — bir necha kunmi yoki haftalabmi?\n"
                    "3) Yoshingiz nechada?")
            s.stage = Stage.DONE
            return s.say(
                "Halol aytaman: bu ta'rifdan qaysi mutaxassis kerakligini aniq "
                "aytolmayman. Shuning uchun taxmin qilmayman.\n"
                "Eng to'g'ri qadam — **terapevt (oilaviy shifokor)**. U ko'rikdan "
                "keyin kerak bo'lsa tor mutaxassisga yo'naltiradi.\n"
                "Navbatga yozaymi?")

        s.guess = guesses[0]
        top, second = guesses[0], (guesses[1] if len(guesses) > 1 else None)

        # shoshilinchlik — belgilar asosida (tashxis emas)
        acute = any(w in norm(combined) for w in
                    ("birdan", "to'satdan", "kuchli", "bugun boshland", "kechadan"))
        s.urgency = Urgency.SOON if acute else Urgency.ROUTINE
        if s.guess.specialist in ("kardiolog", "nevrolog") and acute:
            s.urgency = Urgency.NOW

        # isitma darajasi — kattada 39+, bolada 38.5+ tezroq ko'riladi
        # raqamlar norm() dan o'tmaydi (u tinish belgilarini olib tashlaydi) —
        # shuning uchun "160/100" kabi qiymatlar XOM matnda qidiriladi
        raw = combined
        fever = re.search(r"\b(3[89](?:\.\d)?|4[0-2])\b", raw)
        if fever:
            v = float(fever.group(1))
            if v >= 39 or (s.child and v >= 38.5):
                s.urgency = Urgency.SOON if s.urgency is Urgency.ROUTINE else s.urgency

        # qon bosimi: 140/90 dan yuqori — bir hafta kutish noto'g'ri
        bp = re.search(r"\b(1[4-9]\d|2[0-4]\d)\s*[/\\]\s*(\d{2,3})\b", raw)
        if bp and s.urgency is Urgency.ROUTINE:
            s.urgency = Urgency.SOON

        # og'riq kuchi 8+ — kutish mumkin emas
        pain = re.search(r"\b(8|9|10)\s*(?:/|dan|ball)", raw)
        if pain and s.urgency is Urgency.ROUTINE:
            s.urgency = Urgency.SOON

        s.stage = Stage.SUGGEST
        lines = [
            f"Tushundim. Sizga **{top.label}** kerak ko'rinadi.",
            "",
            "Nega shunday dedim (tashxis emas, faqat yo'nalish):",
        ]
        for h in top.hits[:3]:
            lines.append(f"  · «{h}» — shu mutaxassis sohasi")
        if second and second.score >= top.score * 0.75:
            lines.append(f"  · agar bu qism yetakchi bo'lmasa — {second.label} ham variant")
        lines += [
            "",
            f"Qanchalik tez: **{s.urgency.text}** ({s.urgency.when})",
            "",
            "Eslatma: men tashxis qo'ymayman va dori aytmayman — buni faqat "
            "shifokor qiladi. Mening ishim — to'g'ri mutaxassisga olib borish.",
            "",
            "Navbatga yozaymi? (ha / yo'q)",
        ]
        return s.say(safety_check("\n".join(lines)))

    # ---------- tavsiyadan keyin ----------
    DURATION = re.compile(
        r"\b(\d+\s*(kun|hafta|oy|yil|soat|kunlik)|kechadan|bugun|birdan|"
        r"to'satdan|uzoq|yaqinda)\b")

    def _handle_suggest(self, s: Session, text: str) -> str:
        t = norm(text)
        if any(w in t for w in ("yo'q", "kerak emas", "o'zim", "shart emas")):
            s.stage = Stage.DONE
            return s.say("Mayli. Esda tuting: agar holat yomonlashsa — 103.\n"
                         "Yozib qo'ying: " + SPECIALISTS[s.guess.specialist])
        # faqat davomiylik javobi kelsa — bu rozilik emas, aniqlashtirish
        if self.DURATION.search(t) and not any(
                w in t for w in ("ha", "mayli", "yoz", "bo'ladi", "ok", "xo'p")):
            n = re.search(r"(\d+)\s*(kun|hafta|oy)", t)
            if n:
                v, unit = int(n.group(1)), n.group(2)
                if unit == "kun" and v >= 7:
                    s.urgency = Urgency.ROUTINE
                elif unit == "kun" and v <= 3:
                    s.urgency = Urgency.SOON
                elif unit == "hafta" and v >= 3:
                    s.urgency = Urgency.LATER
                elif unit == "oy" or (unit == "yil"):
                    s.urgency = Urgency.LATER
            # yosh endi ma'lum bo'lsa, mutaxassisni qayta baholaymiz
            if s.age is not None:
                again = classify(" ".join(s.symptoms), s.age, s.sex)
                if again and again[0].specialist != s.guess.specialist:
                    s.guess = again[0]
                    return s.say(f"Yoshni hisobga oldim — endi **{s.guess.label}** "
                                 f"to'g'riroq.\n"
                                 f"Navbatga yozaymi? (ha / yo'q)")
            return s.say(f"Tushundim, {text.strip()}. Shunga qarab: "
                         f"**{s.urgency.text}** ({s.urgency.when}).\n"
                         f"Navbatga yozaymi — {SPECIALISTS[s.guess.specialist]}? (ha / yo'q)")
        return self._book(s, s.guess.specialist, s.urgency)

    # ---------- navbat ----------
    def _book(self, s: Session, specialty: str, urgency: Urgency) -> str:
        slot = datetime.combine(TODAY + timedelta(days=urgency.days),
                               datetime.min.time()).replace(hour=9, minute=30)
        s.booking = Booking(specialty=specialty, urgency=urgency, slot=slot)
        s.reminders = Reminders(s.booking)
        s.stage = Stage.REMIND

        if not self.online:
            s.offline.add("booking", {"specialty": specialty,
                                      "slot": slot.isoformat()})
            return s.say(
                "Internet yo'q — so'rovni qurilmada saqladim. Ulanish qaytishi "
                "bilan avtomatik yuboriladi.\n"
                f"Reja: {SPECIALISTS[specialty]} · {slot.strftime('%d.%m, %H:%M')}")

        # davlat tizimiga havola (haqiqiy: my.gov.uz queue-doctor; DMED)
        return s.say(
            "Navbat tayyor:\n"
            f"  Mutaxassis : {SPECIALISTS[specialty]}\n"
            f"  Muddat     : {urgency.text} — {slot.strftime('%d.%m.%Y, %H:%M')}\n"
            f"  Tasdiqlash : https://my.gov.uz/oz/queue-doctor/\n"
            f"               (yoki DMED ilovasi — oilaviy shifokor qabuli)\n"
            "\n"
            "Havolani ochib tasdiqlaysiz. Men esa eslatib turaman — "
            "3 marta, to siz «bordim» demaguncha.\n"
            "\n"
            "«Bordim» deb yozganingizda to'xtayman.")

    def reconnect(self, s: Session) -> str:
        """Aloqa qaytdi — navbatdagi yozuvlarni yuboradi. Eslatmalar baribir ishlaydi."""
        n = s.offline.sync(online=True)
        if not n:
            return s.say("Aloqa bor. Kutayotgan yozuv yo'q.")
        return s.say(f"Aloqa qaytdi — {n} ta yozuv yuborildi. "
                     f"Eslatmalar rejasi o'zgarmadi.")

    def _handle_book(self, s: Session, text: str) -> str:
        return self._book(s, s.guess.specialist, s.urgency)

    # ---------- eslatmalar ----------
    def _handle_remind(self, s: Session, text: str) -> str:
        t = norm(text)
        if any(w in t for w in ("bordim", "bo'ldim", "keldim", "o'tdim", "ha bordim")):
            s.reminders.confirm()
            s.stage = Stage.DONE
            return s.say(
                "Zo'r. Eslatmalar to'xtatildi. 👍\n"
                "Shifokor nima dedi — qisqa yozib qo'ying, keyingi safar foydali "
                "bo'ladi.\n\n" + why_number() + "\n\nSog' bo'ling!")
        if any(w in t for w in ("bormadim", "bora olmadim", "kechiktir", "boshqa vaqt")):
            s.booking.slot = s.booking.slot + timedelta(days=7)
            s.reminders.sent.clear()
            return s.say(f"Mayli, boshqa vaqtga qo'ydim: "
                         f"{s.booking.slot.strftime('%d.%m, %H:%M')}. Qaytadan eslataman.")
        if any(w in t for w in ("eslat", "qachon", "qanday")):
            return s.say("Reja: " + SPECIALISTS[s.booking.specialty] + " · "
                         + s.booking.slot.strftime('%d.%m.%Y, %H:%M'))
        # boshqa gap — eslatma sifatida qabul qilamiz
        nxt = s.reminders.send_next()
        return s.say(nxt or "Eslatmalar tugadi. «Bordim» desangiz — yakunlayman.")


# ============================================================
# 5. DEMO
# ============================================================

DIALOGUES = [
    ("Ko'krak og'riyapti", ["2 kun", "28 yosh"]),
    ("Boshim og'riyapti va ko'z oldim xiralashadi", ["3 hafta", "35"]),
    ("Qornim dam bo'lib, ko'nglim ayniyapti", ["bir hafta", "40"]),
    ("Bolam 39 isitma bilan yotibdi", ["2 yosh"]),
    ("Yuzim qiyshayib qoldi, qo'lim kuchsiz", ["bugun"]),
    ("Tishim qattiq og'riyapti", ["kechadan"]),
    ("Nafas ololmayapman, ko'kragim siqilyapti", ["hozir"]),
    ("Boshim aylanyapti, qulog'im shang'illaydi", ["10 kun", "52"]),
    ("Uyqum buzilgan, xavotir bo'lyapti", ["2 oy", "30"]),
    ("xyz qwerty", ["assalomu alaykum"]),
]


def run_demo() -> None:
    print("╔" + "═" * 74 + "╗")
    print("║  O'RINDOR AGENT — suhbat → mutaxassis → navbat → eslatma" + " " * 19 + "║")
    print("╚" + "═" * 74 + "╝")
    ag = Agent(online=True)
    for opener, follow in DIALOGUES:
        print("\n" + "─" * 76)
        s = Session()
        print(f"👤 {opener}")
        print("🤖 " + ag.respond(s, opener).replace("\n", "\n   "))
        for f in follow:
            print(f"\n👤 {f}")
            print("🤖 " + ag.respond(s, f).replace("\n", "\n   "))
            if s.stage in (Stage.EMERGENCY, Stage.DONE):
                break
        if s.stage == Stage.REMIND:
            print("\n👤 Bordim")
            print("🤖 " + ag.respond(s, "Bordim"))


def run_interactive() -> None:
    print("O'RINDOR agent — chiqish uchun 'exit'\n")
    ag, s = Agent(online=True), Session()
    print("🤖 Salom! Nima bezovta qilyapti? Oddiy tilda yozing.\n")
    while True:
        try:
            print("👤 ", end="", flush=True)
            u = input().strip()
        except (EOFError, KeyboardInterrupt):
            break
        if u.lower() in ("exit", "quit", "chiqish"):
            break
        if not u:
            continue
        print("🤖 " + ag.respond(s, u).replace("\n", "\n   ") + "\n")


if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_interactive()
