"""Xavfsizlik qatlami — favqulodda holatlar, skrining, chiqish validatori.

Critic.md P0:
  1. yumshoq skelet olib tashlandi (text.word_hit qat'iy);
  2. majburiy skrining savollari — marshrutlashdan OLDIN;
  3. xavfsiz default — yuqori xavfli so'z bor, xavf rad etilmagan bo'lsa
     «1 hafta» emas, «bugun»;
  4. yosh ajratishda «yil» endi yosh emas (triage.parse_age).

Qat'iy qoida: o'tkazib yuborilgan favqulodda holat — yolg'on signaldan
10 baravar qimmat. Shuning uchun shubha bo'lsa — yuqoriroq daraja.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from .text import any_hit, phrase_hit, tokens


class Level(Enum):
    NOW = "SHOSHILINCH"
    TODAY = "BUGUN"

    @property
    def text(self) -> str:
        return self.value


@dataclass(frozen=True)
class RedFlag:
    code: str
    level: Level
    all_of: tuple[str, ...]
    any_of: tuple[str, ...]
    why: str


# ── 1. FAVQULODDA QOIDALAR (modeldan ustun) ────────────────────────────────
# Har bir qoida: barcha `all_of` VA kamida bitta `any_of` topilishi shart.
FLAGS: tuple[RedFlag, ...] = (
    RedFlag("QON_QUS", Level.NOW, ("qon",), ("qus",),
            "Qon qusish — oshqozon-ichakdan qon ketishi belgisi"),
    RedFlag("RU_QON_QUS", Level.NOW, (),
            ("рвота с кровью", "кровь в рвоте", "кровавая рвота"),
            "Qon qusish (rus tilida) — oshqozon-ichakdan qon ketishi"),
    RedFlag("CHEST_ACS", Level.NOW, ("ko'krak",),
            ("chap qo'l", "nafas qisil", "sovuq terla", "tarqal", "siqil",
             "ezib", "bosim"),
            "Ko'krak og'rig'i yurak xuruji belgilari bilan"),
    RedFlag("NAFAS", Level.NOW, (), (
        "nafas ololmay", "nafas olmayapman", "nafas olmayapdi",
        "nafasim yetmay", "nafas yetmay", "nafas qisil", "nafas siqil",
        "bo'g'ilib", "bo'g'il", "nafas yo'lim tiqil", "xirillab nafas",
        "не могу дышать", "задыхаюсь", "тяжело дышать"),
            "Nafas olish yetishmovchiligi"),
    RedFlag("STROKE_FACE", Level.NOW, ("yuz",),
            ("qiyshay", "shalpay", "qimirlamay", "uvish", "sezmay", "tortil",
             "перекосило"),
            "Yuzning bir tomoni qiyshayishi — insult belgisi, vaqt hal qiluvchi"),
    RedFlag("STROKE_ARM", Level.NOW, ("qo'l",),
            ("kuchsiz", "shalpay", "ko'tarolmay", "kotarolmay", "qimirlamay",
             "uvish", "tortil", "og'irlash", "онемение", "слабость в руке"),
            "Qo'l kuchsizligi — insult belgisi, vaqt hal qiluvchi"),
    RedFlag("STROKE_SPEECH", Level.NOW, ("gap",),
            ("chiqmay", "chalkash", "tushunmay", "tutil", "aylanmay", "olmay",
             "не говорю", "речь нарушена"),
            "Gap buzilishi — insult belgisi, vaqt hal qiluvchi"),
    RedFlag("STROKE_TONGUE", Level.NOW, (),
            ("til aylanmay", "tilim aylanmay", "tili tutil",
             "язык заплетается"), "Til buzilishi — insult belgisi"),
    RedFlag("HUSH", Level.NOW, (), (
        "hushimdan ket", "hushidan ket", "esimni yo'qot", "hushim yo'q",
        "hushini yo'qot", "hushimni yo'qot", "hushim ket",
        "poteryal soznanie", "потерял сознание", "обморок"),
            "Hushidan ketish"),
    RedFlag("BLEED", Level.NOW, (), (
        "qon to'xtamay", "qon ketishi to'xtamay", "qonim to'xtamay",
        "qon ketyapti to'xtamay", "qon quyul", "ichimda qon",
        "кровотечение", "кровь не останавливается"),
            "To'xtamaydigan qon ketish"),
    RedFlag("SEIZURE", Level.NOW, (), (
        "tutqanoq", "talvasa", "qaltirab tush", "kramp",
        "sudorogi", "припадок", "судороги"),
            "Tutqanoq — darhol tekshiruv"),
    RedFlag("POISON", Level.NOW, (), (
        "zahar ich", "zahar yut", "zaharlan", "zahar oldim",
        "отравился", "отравилась"), "Zaharlanish"),
    RedFlag("OVERDOSE", Level.NOW, ("doza",), ("oshdi", "oshib", "ko'p ich"),
            "Dori dozasi oshib ketgan"),
    RedFlag("OVERDOSE_MANY", Level.NOW, (), (
        "tabletka ichib", "tabletka ko'p ich", "dori ko'p ich", "quti ich"),
        "Ko'p miqdorda dori ichilgan"),
    RedFlag("PREG_BLEED", Level.NOW, ("homilador",),
            ("qon ket", "qon ketyap", "qon ko'rdim", "suv ketdi", "suvim ketdi"),
            "Homiladorlikda qon ketish yoki suv ketishi"),
    RedFlag("SUICIDE", Level.NOW, (), (
        "o'ldirmoqchiman", "jonimga qasd", "yashashni xohlamay",
        "o'lishni xohlay", "o'zimni o'ldir",
        "не хочу жить", "покончить с собой"),
            "O'z joniga qasd fikri"),
    RedFlag("YURAK_FAST", Level.NOW, ("yurak", "terla"),
            ("o'ynab", "urib ketdi", "tez urib"), "Yurak urishi buzilishi + terlash"),
    RedFlag("MENINGIT", Level.NOW, ("bo'yin", "isitma"),
            ("qot", "qattiq", "egilmay"), "Bo'yin qotishi + isitma"),
    RedFlag("ABDOMEN_INFECT", Level.TODAY, ("qorin", "qus", "isitma"),
            ("qattiq", "o'ng tomon", "pichoq"),
            "Qattiq qorin og'rig'i + qusish/isitma — bugun jarroh ko'rishi kerak"),
    RedFlag("ABDOMEN_SEVERE", Level.TODAY, ("qorin",),
            ("qattiq", "pichoq", "chidab bo'lmay"),
            "Qattiq, chidab bo'lmaydigan qorin og'rig'i"),
    RedFlag("HEAD_SUDDEN", Level.TODAY, ("bosh",),
            ("birdan", "to'satdan", "eng kuchli", "chidab bo'lmay"),
            "To'satdan eng kuchli bosh og'rig'i — bugun tekshiruv"),
    RedFlag("VISION_SUDDEN", Level.TODAY, ("ko'z", "birdan"),
            ("ko'rmay", "xiralash", "yo'qol", "tuman"),
            "Ko'rishning birdan o'zgarishi — bugun tekshiruv"),
    RedFlag("NECK_STIFF", Level.TODAY, ("bo'yin",),
            ("qot", "qattiq", "egilmay"), "Bo'yin qotishi — bugun tekshiruv"),
)

FEVER = ("isitma", "harorat", "temperatura")


def _matches(flag: RedFlag, text: str, toks: list[str]) -> bool:
    for p in flag.all_of:
        if not phrase_hit(p, text, toks):
            return False
    if flag.any_of and not any_hit(flag.any_of, text, toks):
        return False
    return True


def parse_temperature(text: str) -> float | None:
    m = re.search(r"\b(3[5-9](?:[.,]\d)?|4[0-2](?:[.,]\d)?)\b", text)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def check_emergency(text: str, age: int | None = None,
                    pregnant: bool = False) -> RedFlag | None:
    """Matnda favqulodda belgi bormi. Birinchi mos qoida qaytadi."""
    toks = tokens(text)
    if not toks:
        return None

    if age is None:
        n = " ".join(toks)
        m = re.search(r"\b(\d{1,2})\s*oylik\b", n)
        if m:
            age = 0 if int(m.group(1)) < 12 else 1
        else:
            m = re.search(r"\b(\d{1,3})\s*yosh", n)
            if m:
                age = int(m.group(1))

    for flag in FLAGS:
        if _matches(flag, text, toks):
            return flag

    bp = re.search(r"\b(\d{3})\s*/\s*(\d{2,3})\b", text)
    if bp and (int(bp.group(1)) >= 180 or int(bp.group(2)) >= 110):
        return RedFlag("BP_CRISIS", Level.NOW, (), (),
                       "Qon bosimi 180/110 dan yuqori — gipertonik kriz")

    # yoshga bog'liq: 1 yoshgacha isitma ≥38 — shoshilinch
    if age is not None and age < 1:
        t = parse_temperature(text)
        if (t is not None and t >= 38) or any_hit(FEVER, text, toks):
            return RedFlag("INFANT_FEVER", Level.NOW, (), (),
                           "Bir yoshgacha bolada isitma")
    # homiladorlik + kuchli qorin og'rig'i
    if pregnant and phrase_hit("qorin og'ri", text, toks):
        return RedFlag("PREG_PAIN", Level.TODAY, (), (),
                       "Homiladorlikda qorin og'rig'i — bugun ko'rsating")
    return None


# ── 2. MAJBURIY SKRINING (marshrutlashdan oldin) ───────────────────────────

@dataclass(frozen=True)
class Screening:
    topic: str
    question: str
    escalation: Level          # javob yo'q / noaniq bo'lsa
    reason: str
    safe: Level = Level.TODAY  # «yo'q» javobidan keyingi xavfsiz default


CHEST_WORDS = ("ko'krak", "yurak sohasi")
SEVERE = ("kuchli", "qattiq", "juda", "chidab bo'lmay", "eng kuchli", "zo'r")


def screening_for(text: str, age: int | None = None,
                  pregnant: bool = False) -> Screening | None:
    """Yuqori xavfli mavzu bor, lekin favqulodda qoida ishlamadi → savol.

    Savol berilmasa yoki javob noaniq bo'lsa — `escalation` darajasi qo'llanadi.
    Bu «1 hafta» xatosini yopadi (critic.md: ko'krak og'rig'i → 1 hafta).
    """
    toks = tokens(text)

    if any_hit(CHEST_WORDS, text, toks):
        return Screening(
            "chest",
            "Ko'krak og'rig'i nafas qisilishi, sovuq terlash yoki chap qo'lga "
            "tarqalish bilan birgami? (ha / yo'q)",
            Level.NOW,
            "Ko'krak og'rig'i yurak xuruji belgisi bo'lishi mumkin",
            Level.TODAY)

    if any_hit(("nafas qisil", "nafas siqil", "nafas yetmay", "nafas ololmay",
                "xirill", "bo'g'il"), text, toks):
        return Screening(
            "breath",
            "Nafas qisilishi tinch holatda ham bormi — gapirganda ham "
            "nafas yetmayaptimi? (ha / yo'q)",
            Level.NOW, "Nafas olish qiyinlashuvi", Level.TODAY)

    if phrase_hit("qorin og'ri", text, toks) or any_hit(("qornim og'ri",), text, toks):
        return Screening(
            "abdomen",
            "Qorin og'rig'i qattiqmi, qusish yoki isitma bilan birgami? "
            "(ha / yo'q)",
            Level.TODAY, "Qattiq qorin og'rig'i jarrohlik holati bo'lishi mumkin",
            Level.TODAY)

    if phrase_hit("bosh og'ri", text, toks) and any_hit(SEVERE, text, toks):
        return Screening(
            "head",
            "Bosh og'rig'i bir necha soniyada eng kuchli bo'lib boshlanganmi, "
            "ko'ngil aynishi yoki qusish bilan birgami? (ha / yo'q)",
            Level.TODAY, "To'satdan kuchli bosh og'rig'i", Level.TODAY)

    if any_hit(("ko'rish xira", "ko'z oldi xira", "ko'z xira", "ko'rmay",
                "ko'rish pasay"), text, toks):
        return Screening(
            "vision",
            "Ko'rish birdan o'zgarganmi — bir necha daqiqa ichida "
            "yomonlashdimi? (ha / yo'q)",
            Level.TODAY, "Ko'rishning keskin o'zgarishi", Level.TODAY)

    if age is not None and age < 5 and any_hit(FEVER, text, toks):
        return Screening(
            "child_fever",
            "Bolada holsizlik, ovqat/ichimlikdan bosh tortish, tutqanoq yoki "
            "hushidan ketish bo'ldimi? (ha / yo'q)",
            Level.NOW, "Kichik bolada isitma — xavfni istisno qilish kerak",
            Level.TODAY)

    if pregnant and any_hit(("qorin og'ri", "qon ket", "suv ketdi"), text, toks):
        return Screening(
            "pregnancy",
            "Homiladorlikda qon ketish yoki suv ketishi bormi? (ha / yo'q)",
            Level.NOW, "Homiladorlikda shoshilinch belgi", Level.TODAY)
    return None


YES = ("ha", "bor", "bo'ldi", "bo'ldim", "shunday", "xu", "xop", "ok", "да", "есть")
NO = ("yo'q", "yuq", "emas", "bo'lmadi", "bo'lmagan", "yo'qdir", "нет",
      "yo'q deb", "hech narsa")


def read_answer(text: str) -> str:
    """Javob: yes / no / unclear. Noaniq javob xavfsiz tomonga ketadi."""
    t = " ".join(tokens(text))
    if not t:
        return "unclear"
    neg = any(t.startswith(n) or f" {n}" in f" {t}" for n in NO)
    pos = any(t == y or t.startswith(y + " ") or t.startswith(y + "?") or
              f" {y} " in f" {t} " or t.startswith(y) for y in YES)
    if pos and not neg:
        return "yes"
    if neg and not pos:
        return "no"
    return "unclear"


# ── 3. CHIQISH VALIDATORI (har javob shu yerdan o'tadi) ───────────────────

DX_WORDS = (
    "bronxit", "gastrit", "angina", "diabet", "gipertoniya", "astma", "artrit",
    "infarkt", "insult", "pnevmoniya", "yallig'lanish", "orvi", "orz",
    "gepatit", "anemiya", "appenditsit", "xoletsistit", "migren", "nevroz",
)
ADVICE = re.compile(
    r"\b(kuniga|har kuni|tunda)\b[^.\n]{0,30}\b(iching|qabul qiling|oling)\b|"
    r"\b(iching|qabul qiling|ichishni boshlang|davolang|davolanishni boshlang)\b|"
    r"\b(retsept yoz|dozani oshir|dori tavsiya)\b", re.I)
CLAIM = re.compile(
    r"sizda\s+[\w'-]+\s+(bor|kasalligi|yallig'lanishi)|"
    r"\b(tashxis|diagnoz)\s*[:—]", re.I)

TRIAGE_DRUGS = (
    "paratsetamol", "paracetamol", "ibuprofen", "aspirin", "analgin",
    "metamizol", "nurofen", "panadol", "ketorol", "diklofenak", "omeprazol",
    "metformin", "levotiroksin", "amoksitsillin", "azitromitsin", "varfarin",
    "insulin", "prednizolon", "enalapril", "amlodipin", "furosemid",
    "suprastin", "xloropiramin", "smecta", "mezim", "pankreatin",
)
_DOSE = re.compile(r"\b\d+(?:[.,]\d+)?\s*(mg|мг|ml|мл|mkg|мкг|tabletka|таб)\b", re.I)


def validate_triage(text: str) -> str:
    """Triaj javobi: dori nomi, doza, tashxis da'vosi, davolash maslahati yo'q."""
    t = text
    low = t.lower()
    for d in TRIAGE_DRUGS:
        t = re.sub(rf"\b{re.escape(d)}\w*\b", "[dori nomi olib tashlandi]", t,
                   flags=re.I)
        low = low.replace(d, "")
    t = ADVICE.sub("[davolash maslahati olib tashlandi]", t)
    t = CLAIM.sub("[tashxis da'vosi olib tashlandi]", t)
    for w in DX_WORDS:
        t = re.sub(rf"\b{re.escape(w)}\w*\b", "[tashxis nomi olib tashlandi]", t,
                   flags=re.I)
    t = _DOSE.sub("[doza olib tashlandi]", t)
    return t


def validate_card(text: str) -> str:
    """Karta javobi: dori nomlari — ma'lumot, ruxsat. Faqat maslahat taqiqlanadi."""
    t = ADVICE.sub("[davolash maslahati olib tashlandi]", text)
    t = CLAIM.sub("[tashxis da'vosi olib tashlandi]", t)
    return t


def violations(text: str, mode: str, allowed: set[str] | None = None) -> list[str]:
    """Test uchun: matnda taqiqlangan narsa qolganmi."""
    out: list[str] = []
    low = text.lower()
    for w in DX_WORDS:
        if re.search(rf"\b{re.escape(w)}\w*\b", low):
            out.append("dx:" + w)
    if ADVICE.search(text):
        out.append("advice")
    if CLAIM.search(text):
        out.append("claim")
    if mode == "triage":
        for d in TRIAGE_DRUGS:
            if re.search(rf"\b{re.escape(d)}\w*\b", low):
                out.append("drug:" + d)
        if _DOSE.search(text):
            out.append("dose")
    return out
