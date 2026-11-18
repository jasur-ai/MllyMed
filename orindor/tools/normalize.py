"""
O'RINDOR · nom normalizatsiyasi — MODEL qatlami (LLM emas)
======================================================
Muammo: bemor "paratsetamol" deydi, "парацетамол" deb yozadi, qadoqda
"Paracetamol", AQShda "acetaminophen", ba'zi hollarda xato yozadi.

Bu modul JONLI RxNorm va jonli openFDA ma'lumotidan foydalanadi (egiz/data/),
lekin eng muhimi — QAT'IY DARVOZA (gate).

NEGA DARVOZA SHART — real o'lchangan hodisa
-------------------------------------------
Kirillcha "парацетамол" ni to'g'ridan-to'g'ri RxNorm ga bersak, u
"incobotulinumtoxinA" (botulizm toksini) qaytaradi. Ya'ni oddiy nom
moslashtiruvchi bemorni BOSHQA doriga yuboradi. Bu — nazariy emas,
`ingest_real.py` da yozib olingan haqiqiy natija.

Uch qatlamli himoya:
  1. Skript aniqlash + transliteratsiya (kirill → lotin)
  2. Lug'at (uz / ru / JSST / AQSh nomlari)
  3. RxNorm + fuzzy, LEKIN natija RUXSAT ETILGAN INN ro'yxatida bo'lishi shart,
     aks holda "BILMAYMAN" — hech qanday taxmin qilinmaydi.

Ishga tushirish:  python3 egiz/normalize.py
"""

from __future__ import annotations

import difflib
import json
import os
import urllib.parse
import urllib.request
from dataclasses import dataclass

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "real_products.json")

# ------------------------------------------------------------
# 1. RUXSAT ETILGAN INN lar — agent FAQAT shular haqida gapiradi.
#    Ro'yxatdan tashqaridagi har qanday javob = abstention.
# ------------------------------------------------------------
ALLOWED_INNS = {
    "paracetamol": "N02BE01", "metformin": "A10BA02", "amoxicillin": "J01CA04",
    "ceftriaxone": "J01DD04", "ibuprofen": "M01AE01", "levothyroxine": "H03AA01",
    "warfarin": "B01AA03", "omeprazole": "A02BC01", "losartan": "C09CA01",
    "amlodipine": "C08CA01", "salbutamol": "R03AC02", "diclofenac": "M01AB05",
    "azithromycin": "J01FA10", "ciprofloxacin": "J01MA02", "insulin": "A10AB01",
    "metamizole": "N02BB02",
}

# ------------------------------------------------------------
# 2. LUG'AT — real nomlar, o'zbek/rus/AQSh variantlari
# ------------------------------------------------------------
ALIASES: dict[str, str] = {
    # o'zbekcha / lotin
    "paratsetamol": "paracetamol", "parasetamol": "paracetamol",
    "seftriakson": "ceftriaxone", "sefriakson": "ceftriaxone",
    "levotiroksin": "levothyroxine", "levotiroksin_natrium": "levothyroxine",
    "amoksitsillin": "amoxicillin", "amoksisillin": "amoxicillin",
    "azitromitsin": "azithromycin", "siprofloksatsin": "ciprofloxacin",
    "diklofenak": "diclofenac", "salbutamol": "salbutamol",
    "analgin": "metamizole", "metamizol": "metamizole",
    # rus / kirill (transliteratsiyadan keyin)
    "paratsetamol_r": "paracetamol", "metformin_r": "metformin",
    # AQSh nomlari (JSST nomidan farq qiladi) — real topilma
    "acetaminophen": "paracetamol", "albuterol": "salbutamol",
    "adrenaline": "insulin",
    # xato yozilishlar
    "paracitamol": "paracetamol", "paracetmol": "paracetamol",
    "metformine": "metformin", "ibuprofene": "ibuprofen",
}

CYR2LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh", "ъ": "",
    "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}

# kirill → INN to'g'ridan-to'g'ri (transliteratsiya xato qilsa ham ishonchli)
CYR_DIRECT = {
    "парацетамол": "paracetamol", "метформин": "metformin",
    "амоксициллин": "amoxicillin", "цефтриаксон": "ceftriaxone",
    "ибупрофен": "ibuprofen", "левотироксин": "levothyroxine",
    "варфарин": "warfarin", "омепразол": "omeprazole", "лозартан": "losartan",
    "амлодипин": "amlodipine", "сальбутамол": "salbutamol",
    "диклофенак": "diclofenac", "азитромицин": "azithromycin",
    "ципрофлоксацин": "ciprofloxacin", "инсулин": "insulin",
}


def is_cyrillic(s: str) -> bool:
    return any("а" <= ch <= "я" or ch == "ё" for ch in s.lower())


def translit(s: str) -> str:
    return "".join(CYR2LAT.get(ch, ch) for ch in s.lower())


def clean(s: str) -> str:
    return "".join(ch for ch in s.lower().strip() if ch.isalnum() or ch in " -'").strip()


@dataclass
class NormResult:
    query: str
    inn: str | None
    confidence: float
    method: str                 # dictionary | cyrillic | rxnorm | fuzzy | abstain
    note: str
    candidates: list[str]

    @property
    def ok(self) -> bool:
        return self.inn is not None

    def show(self) -> str:
        if not self.ok:
            return f"«{self.query}» → BILMAYMAN ({self.method}): {self.note}"
        return (f"«{self.query}» → {self.inn} ({self.confidence:.2f}, {self.method})"
                + (f" · {self.note}" if self.note else ""))


# ------------------------------------------------------------
# 3. RxNorm (jonli, lekin darvoza bilan)
# ------------------------------------------------------------

_RXNORM_CACHE: dict[str, list[str]] = {}


def _rxcui_name(rxcui: str) -> str | None:
    url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/property.json?propName=RxNorm%20Name"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            d = json.loads(r.read())
        pc = ((d.get("propConceptGroup") or {}).get("propConcept") or [])
        return pc[0].get("propValue") if pc else None
    except Exception:
        return None


def rxnorm_lookup(name: str) -> list[str]:
    if name in _RXNORM_CACHE:
        return _RXNORM_CACHE[name]
    url = ("https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term="
           + urllib.parse.quote(name) + "&maxEntries=3")
    out: list[str] = []
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            d = json.loads(r.read())
        for c in (((d.get("approximateGroup") or {}).get("candidate") or [])[:2]):
            nm = c.get("name") or _rxcui_name(c.get("rxcui") or "")
            if nm:
                out.append(nm)
    except Exception:
        pass
    _RXNORM_CACHE[name] = out
    return out


def inn_from_rxname(rxname: str) -> str | None:
    """RxNorm nomi ichidan RUXSAT ETILGAN INN ni qidiradi.

    «acetaminophen 325 MG Oral Tablet» → paracetamol
    «incobotulinumtoxinA»              → None  ← darvoza shu yerda yopiladi
    """
    low = rxname.lower()
    for inn in ALLOWED_INNS:
        if inn in low:
            return inn
    for alias, inn in ALIASES.items():
        if alias.replace("_", " ") in low:
            return inn
    return None


# ------------------------------------------------------------
# 4. Asosiy funksiya
# ------------------------------------------------------------

def normalize(raw: str, use_network: bool = True) -> NormResult:
    q = clean(raw)
    if not q:
        return NormResult(raw, None, 0.0, "abstain", "bo'sh so'rov", [])

    # (1) kirill — to'g'ridan-to'g'ri lug'at, transliteratsiyadan oldin
    if is_cyrillic(raw):
        low = raw.lower().strip()
        if low in CYR_DIRECT:
            return NormResult(raw, CYR_DIRECT[low], 0.99, "cyrillic",
                              "kirill yozuvi lug'atdan aniqlandi", [])
        t = translit(low)
        if t in ALIASES:
            return NormResult(raw, ALIASES[t], 0.93, "cyrillic",
                              f"kirill → lotin ({t}) → lug'at", [t])
        if t in ALLOWED_INNS:
            return NormResult(raw, t, 0.95, "cyrillic", "kirill → lotin → INN", [t])
        q = clean(t)          # davom etamiz, lekin endi lotin

    # (2) lug'at
    if q in ALLOWED_INNS:
        return NormResult(raw, q, 1.0, "dictionary", "", [])
    if q in ALIASES:
        return NormResult(raw, ALIASES[q], 0.97, "dictionary",
                          f"alias: {q} → {ALIASES[q]}", [])

    # (3) fuzzy — faqat ruxsat etilgan ro'yxat ichida
    close = difflib.get_close_matches(q, list(ALLOWED_INNS) + list(ALIASES), n=2, cutoff=0.85)
    if close:
        best = close[0]
        inn = best if best in ALLOWED_INNS else ALIASES.get(best)
        if inn:
            return NormResult(raw, inn, 0.88, "fuzzy",
                              f"o'xshash: {q} ≈ {best}", close)

    # (4) RxNorm — LEKIN natija ruxsat etilgan INN bo'lishi shart
    if use_network:
        names = rxnorm_lookup(q)
        for nm in names:
            inn = inn_from_rxname(nm)
            if inn:
                return NormResult(raw, inn, 0.86, "rxnorm",
                                  f"RxNorm: «{nm}»", names)
        if names:
            return NormResult(raw, None, 0.0, "abstain",
                              f"RxNorm «{names[0]}» qaytardi, lekin bu ruxsat etilgan "
                              f"INN emas — taxmin qilmaymiz", names)

    return NormResult(raw, None, 0.0, "abstain",
                      "lug'at, fuzzy va RxNorm hech birini tasdiqlamadi", [])


def demo() -> None:
    print("O'RINDOR · nom normalizatsiyasi (model qatlami)\n" + "─" * 74)
    tests = ["парацетамол", "Парацетамол", "paratsetamol", "Paracetamol 500mg",
             "acetaminophen", "метформин", "seftriakson", "ceftriaxone",
             "levotiroksin", "азитромицин", "analgin", "asprin", "xyz123",
             "paracitamol", "ибупрофен"]
    for t in tests:
        print("  " + normalize(t).show())


if __name__ == "__main__":
    demo()
