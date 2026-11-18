"""Mutaxassis modeli — izohlanadigan ballash + yosh/qavat qoidalari.

Critic.md tuzatishlari:
  • «2 yil» endi yosh emas (davomiylik); yosh faqat «N yosh» dan olinadi;
  • «bolam» yoshni taxmin qilmaydi — so'raladi;
  • inkor («og'rimayapti», «og'riq yo'q») signal hisoblanmaydi (text.phrase_hit);
  • «kasalman» kabi umumiy so'zlar mutaxassis tanlamaydi.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from .text import phrase_hit, tokens


class Urgency(Enum):
    NOW = ("SHOSHILINCH", "hoziroq — 103", 0)
    TODAY = ("BUGUN", "bugun albatta ko'rsating", 0)
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

    @property
    def rank(self) -> int:
        return {"SHOSHILINCH": 0, "BUGUN": 1, "1–3 kun": 2,
                "1 hafta": 3, "2–4 hafta": 4}[self.value[0]]


SPECIALISTS = {
    "terapevt": "Terapevt (oilaviy shifokor)",
    "kardiolog": "Kardiolog",
    "nevrolog": "Nevrolog",
    "gastroenterolog": "Gastroenterolog",
    "pulmonolog": "Pulmonolog",
    "endokrinolog": "Endokrinolog",
    "urolog": "Urolog",
    "ginekolog": "Ginekolog",
    "travmatolog": "Travmatolog-ortoped",
    "lor": "LOR (quloq-tomoq-burun)",
    "oftalmolog": "Oftalmolog (ko'z)",
    "dermatolog": "Dermatovenerolog",
    "stomatolog": "Stomatolog",
    "onkolog": "Onkolog",
    "psixiatr": "Psixiatr / psixoterapevt",
    "ftiziatr": "Ftiziatr (sil)",
    "infeksionist": "Infeksionist",
    "allergolog": "Allergolog-immunolog",
    "revmatolog": "Revmatolog",
    "nefrolog": "Nefrolog",
    "gematolog": "Gematolog",
    "pediatr": "Pediatr",
    "jarroh": "Jarroh",
    "proktolog": "Proktolog",
    "mammolog": "Mammolog",
}

# signal → {mutaxassis: vazn}
SIGNALS: dict[str, dict[str, float]] = {
    # ── yurak / qon bosimi
    "ko'krak og'ri": {"kardiolog": 3.0, "terapevt": 1.0},
    "yurak og'ri": {"kardiolog": 3.0, "terapevt": 1.0},
    "yurak sanch": {"kardiolog": 3.0, "terapevt": 1.0},
    "yuragim": {"kardiolog": 2.8, "terapevt": 1.0},
    "yurak": {"kardiolog": 2.5, "terapevt": 1.0},
    "sanch": {"kardiolog": 2.0, "terapevt": 1.0},
    "yurak tez": {"kardiolog": 2.5},
    "yurak urib": {"kardiolog": 2.5},
    "yurak o'ynab": {"kardiolog": 2.5},
    "yurak sohasi": {"kardiolog": 2.0},
    "bosim yuqori": {"kardiolog": 2.4, "nefrolog": 1.0},
    "bosim past": {"kardiolog": 2.0, "terapevt": 1.0},
    "bosim": {"kardiolog": 2.2, "terapevt": 1.0},
    "oyoq shish": {"kardiolog": 2.0, "nefrolog": 1.5},
    # ── nafas
    "yo'tal": {"pulmonolog": 2.0, "lor": 1.0, "terapevt": 1.0, "ftiziatr": 0.5},
    "nafas qis": {"pulmonolog": 2.6, "kardiolog": 1.2},
    "xirill": {"pulmonolog": 2.5},
    "yo'talda qon": {"ftiziatr": 3.0, "pulmonolog": 2.0, "onkolog": 1.5},
    "balg'am": {"pulmonolog": 1.8, "terapevt": 0.8},
    "isitma": {"terapevt": 2.0, "infeksionist": 1.5, "pediatr": 1.2},
    "shamollash": {"terapevt": 2.2, "lor": 1.0},
    "shamolladim": {"terapevt": 2.2, "lor": 1.0},
    "gripp": {"terapevt": 2.2, "infeksionist": 1.0},
    "harorat": {"terapevt": 2.0, "infeksionist": 1.2},
    # ── hazm
    "qorin og'ri": {"gastroenterolog": 2.5, "jarroh": 1.2, "ginekolog": 0.8},
    "qornim": {"gastroenterolog": 2.5, "jarroh": 1.0},
    "oshqozon": {"gastroenterolog": 2.5, "terapevt": 1.0},
    "qorin dam": {"gastroenterolog": 2.5},
    "jigar": {"gastroenterolog": 2.5, "infeksionist": 1.0},
    "jigarim": {"gastroenterolog": 2.5, "infeksionist": 1.0},
    "ich ket": {"gastroenterolog": 2.0, "infeksionist": 1.5},
    "ichim og'ri": {"gastroenterolog": 2.5, "jarroh": 1.0},
    "qabziyat": {"gastroenterolog": 2.0, "proktolog": 1.0},
    "qichish": {"proktolog": 2.0, "dermatolog": 1.0},
    "anal": {"proktolog": 2.5},
    "ko'ngil ayni": {"gastroenterolog": 2.2},
    "hazm": {"gastroenterolog": 1.8},
    "achish": {"urolog": 1.5, "gastroenterolog": 1.0},
    # ── nevrolog
    "bosh og'ri": {"nevrolog": 2.0, "terapevt": 1.0, "lor": 0.5},
    "boshim": {"nevrolog": 2.0, "terapevt": 1.0},
    "bosh aylan": {"nevrolog": 2.0, "lor": 1.5, "kardiolog": 0.8},
    "uvish": {"nevrolog": 2.5},
    "hush": {"nevrolog": 1.5},
    "xotira": {"nevrolog": 2.0},
    "uyqu": {"nevrolog": 1.5, "psixiatr": 1.6},
    "qo'l kuchsiz": {"nevrolog": 2.6},
    "yuz qiyshay": {"nevrolog": 2.6},
    # ── ruhiyat
    "xavotir": {"psixiatr": 2.6},
    "tushkun": {"psixiatr": 3.0},
    "ruhiy tushkun": {"psixiatr": 3.0},
    "depress": {"psixiatr": 3.0},
    "asabiy": {"psixiatr": 2.0, "endokrinolog": 0.8},
    "asab": {"psixiatr": 1.8, "nevrolog": 1.2},
    "stress": {"psixiatr": 2.0},
    "panik": {"psixiatr": 2.5},
    "yig'loqi": {"psixiatr": 2.0},
    # ── endokrin
    "vazn yo'qot": {"endokrinolog": 2.4, "gastroenterolog": 0.8},
    "chanq": {"endokrinolog": 2.5, "nefrolog": 1.0},
    "siyish ko'p": {"endokrinolog": 2.0, "urolog": 2.0},
    "qalqon": {"endokrinolog": 2.5},
    "soch to'kil": {"endokrinolog": 1.5, "dermatolog": 1.5},
    "tez charch": {"gematolog": 1.5, "terapevt": 1.5, "endokrinolog": 1.2},
    "holsiz": {"terapevt": 2.0, "gematolog": 1.0},
    "holdan toy": {"terapevt": 1.8, "gematolog": 1.0},
    # ── buyrak / urolog
    "bel og'ri": {"nevrolog": 1.8, "travmatolog": 1.4, "nefrolog": 1.0, "urolog": 0.8},
    "belim": {"nevrolog": 1.8, "travmatolog": 1.4, "nefrolog": 1.0, "urolog": 0.8},
    "siydik": {"urolog": 2.5, "nefrolog": 1.2},
    "siyish achish": {"urolog": 2.8, "nefrolog": 1.0},
    "siyish tez": {"urolog": 2.2},
    "buyrak": {"nefrolog": 2.5, "urolog": 1.5},
    "buyragim": {"nefrolog": 2.5, "urolog": 1.5},
    # ── ginekologiya
    "hayz": {"ginekolog": 2.5},
    "homilador": {"ginekolog": 2.5},
    "ko'krak bez": {"mammolog": 2.5, "ginekolog": 1.5},
    "bachadon": {"ginekolog": 2.5},
    # ── teri
    "toshma": {"dermatolog": 2.5, "allergolog": 1.5},
    "teri qich": {"dermatolog": 2.5, "allergolog": 1.2},
    "terim qich": {"dermatolog": 2.5, "allergolog": 1.2},
    "dog'": {"dermatolog": 2.0, "onkolog": 0.5},
    "yara": {"dermatolog": 1.5, "jarroh": 1.0},
    "qizar": {"allergolog": 2.3, "dermatolog": 1.2},
    # ── ko'z / quloq / tomoq
    "ko'z": {"oftalmolog": 2.5},
    "ko'zim": {"oftalmolog": 2.5},
    "ko'rish": {"oftalmolog": 2.5},
    "ko'z oldi": {"oftalmolog": 2.4, "nevrolog": 1.0},
    "quloq": {"lor": 2.5},
    "qulog'im": {"lor": 2.5},
    "tomoq": {"lor": 2.5, "terapevt": 0.8},
    "tomog'im": {"lor": 2.5, "terapevt": 0.8},
    "burun": {"lor": 2.5, "allergolog": 0.8},
    "hid": {"lor": 2.0},
    "yutolmay": {"lor": 2.2},
    # ── tayanch-harakat
    "bo'g'im": {"revmatolog": 2.0, "travmatolog": 1.5},
    "tizza": {"travmatolog": 2.5, "revmatolog": 1.0},
    "suyak": {"travmatolog": 2.5},
    "jarohat": {"travmatolog": 2.5, "jarroh": 1.0},
    "yelka": {"travmatolog": 2.0, "nevrolog": 1.0},
    # ── qon
    "qon kam": {"gematolog": 2.5, "terapevt": 1.0},
    "limfa": {"gematolog": 2.0, "onkolog": 1.5},
    # ── boshqa
    "tish": {"stomatolog": 3.0},
    "tishim": {"stomatolog": 3.0},
    "og'iz yara": {"stomatolog": 2.0},
    "allergiya": {"allergolog": 2.5},
    "emlash": {"terapevt": 1.5, "pediatr": 1.5},
    "tekshiruv": {"terapevt": 2.0},
    "profilaktika": {"terapevt": 2.0},
    "tugun": {"mammolog": 2.6, "onkolog": 1.6},
}

ACUTE = ("birdan", "to'satdan", "kuchli", "bugun boshland", "kechadan",
         "hozir", "hozirda", "yangi")


@dataclass
class Guess:
    specialist: str
    score: float
    hits: list[str]

    @property
    def label(self) -> str:
        return SPECIALISTS[self.specialist]


def parse_age(text: str) -> int | None:
    """Faqat «N yosh» / «N yoshda» / «N oylik». «2 yil» — davomiylik, yosh emas."""
    t = " ".join(tokens(text))
    m = re.search(r"\b(\d{1,3})\s*(?:yosh(?:da|li|daman)?|ёш)\b", t)
    if m:
        v = int(m.group(1))
        return v if 0 <= v <= 120 else None
    m = re.search(r"\b(\d{1,2})\s*oylik\b", t)
    if m:
        return 0 if int(m.group(1)) < 12 else 1
    return None


CHILD_WORDS = ("bolam", "bolasi", "bolasini", "o'g'lim", "qizim", "chaqaloq",
               "farzand", "bebek", "go'dak", "bola", "bolamni")


def is_child_context(text: str) -> bool:
    return any(phrase_hit(w, text) for w in CHILD_WORDS)


def age_from_bare(text: str) -> int | None:
    t = " ".join(tokens(text))
    m = re.fullmatch(r"(\d{1,3})", t)
    return int(m.group(1)) if m else None


def classify(text: str, age: int | None = None,
             sex: str | None = None) -> list[Guess]:
    scores: dict[str, float] = {}
    hits: dict[str, list[str]] = {}
    toks = tokens(text)
    for phrase, targets in SIGNALS.items():
        if not phrase_hit(phrase, text, toks):
            continue
        for sp, w in targets.items():
            scores[sp] = scores.get(sp, 0.0) + w
            hits.setdefault(sp, []).append(phrase)

    if age is not None:
        if age < 15:
            if "pediatr" in scores:
                scores["pediatr"] *= 1.8
            if "terapevt" in scores:
                scores["terapevt"] *= 0.4
            if "ginekolog" in scores:
                scores.pop("ginekolog")
                hits.pop("ginekolog", None)
        elif "pediatr" in scores:
            scores["pediatr"] *= 0.3
    if sex == "erkak" and "ginekolog" in scores:
        scores.pop("ginekolog")
        hits.pop("ginekolog", None)

    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    return [Guess(sp, round(sc, 2), hits.get(sp, [])) for sp, sc in ranked]


def urgency(text: str, guess: Guess | None, age: int | None = None,
            child: bool = False, base: Urgency = Urgency.ROUTINE) -> Urgency:
    """Xavfsiz default: yuqori xavfli belgi bor bo'lsa «1 hafta» berilmaydi."""
    from .safety import parse_temperature

    t = " ".join(tokens(text))
    u = base

    def raise_to(level: Urgency) -> None:
        nonlocal u
        if level.rank < u.rank:
            u = level

    acute = any(w in t for w in ACUTE)
    if acute and guess and guess.specialist in (
            "kardiolog", "nevrolog", "pulmonolog", "jarroh"):
        raise_to(Urgency.TODAY)
    elif acute:
        raise_to(Urgency.SOON)

    fever = parse_temperature(text)
    if fever is not None and (fever >= 39 or (child and fever >= 38.5)):
        raise_to(Urgency.TODAY)
    if fever is not None and child and fever >= 38:
        raise_to(Urgency.TODAY)

    bp = re.search(r"\b(1[4-9]\d|2[0-4]\d)\s*[/\\]\s*\d{2,3}\b", text)
    if bp:
        raise_to(Urgency.TODAY)

    if re.search(r"\b(8|9|10)\s*(?:/|dan|ball)", text):
        raise_to(Urgency.TODAY)

    dur = re.search(r"\b(\d{1,2})\s*(kun|hafta|oy)\b", t)
    if dur and u is Urgency.ROUTINE:
        v, unit = int(dur.group(1)), dur.group(2)
        if unit == "kun" and v <= 3:
            u = Urgency.SOON
        elif unit == "hafta" and v >= 3:
            u = Urgency.LATER
        elif unit == "oy":
            u = Urgency.LATER
    return u
