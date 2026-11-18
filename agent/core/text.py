"""Matn qatlami — o'zbek/rus/kirill normalizatsiyasi va qat'iy moslik.

Critic.md dagi asosiy topilma: eski `skel()` juda yumshoq edi — 2 harfli
skelet «qon» ni «kun» ga, «gap» ni «ko'p» ga moslashtirardi. Bu yerda:

  1. Kirill → lotin (o'zbek + rus harflari).
  2. Apostrof variantlari bir shaklga.
  3. Moslik uchun minimal uzunlik 4 va undosh-sinf prefiksi.
     «ko'krak»/«ko'kragim» → mos; «qon»/«kun» → mos EMAS.
  4. Inkor: «og'rimayapti», «... yo'q», «... emas» — signal hisoblanmaydi.
"""
from __future__ import annotations

import re
import unicodedata

CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
    "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    "ў": "o", "қ": "q", "ғ": "g", "ҳ": "h",
}

# Ovoz jihatidan juft undoshlar — qo'shimcha oldidan almashadi:
#   ko'krak → ko'kragim, quloq → qulog'im
VOICE = {"k": "K", "g": "K", "q": "K", "p": "P", "b": "P", "t": "T", "d": "T",
         "s": "S", "z": "S", "f": "F", "v": "F", "x": "X", "h": "X",
         "j": "C", "c": "C"}

NEG_TOKENS = {"yo'q", "emas", "yuq", "не", "нет"}
NEG_STEMS = ("mayapti", "mayapdi", "maydi", "mayapman", "mayman", "maymiz",
             "madim", "madi", "magan", "maganman", "mas", "maganman")
# 3 harfli o'zaklar uchun ruxsat etilgan qo'shimcha boshlanishlari.
# «qon»+«im» = qonim ✓, «qon»+«un» = qonun ✗ (qonun matni dori emas).
SUFFIX_START = (
    "im", "ing", "i", "lar", "lari", "dan", "da", "de", "ga", "ka", "qa",
    "ni", "ning", "li", "dim", "di", "gan", "gen", "ib", "ish", "si",
    "sini",    "yapti", "yapdi", "ayapti", "ayapdi", "yapman", "yapmiz", "yapsiz",
    "lari", "imiz", "laring",
)

MIN_STEM = 4          # 4 dan qisqa so'zlar faqat aniq moslik bilan
MAX_EDIT = 1          # uzun so'zlarda bitta imlo xatosi


def translit(s: str) -> str:
    return "".join(CYR.get(ch, ch) for ch in (s or "").lower())


def norm(s: str) -> str:
    """Bir xil shakl: kichik harf, lotin, oddiy apostrof, tinish belgisisiz."""
    t = unicodedata.normalize("NFKC", s or "").lower()
    t = translit(t)
    t = t.replace("ʻ", "'").replace("ʼ", "'").replace("‘", "'").replace("`", "'")
    t = t.replace("®", " ").replace("™", " ")
    t = "".join(ch if (ch.isalnum() or ch == "'") else " " for ch in t)
    return " ".join(t.split())


def tokens(s: str) -> list[str]:
    return norm(s).split()


def fuzzy_key(w: str) -> str:
    """Undosh sinflari, unlilar saqlanadi, apostrof olib tashlanadi."""
    w = w.replace("'", "")
    return "".join(VOICE.get(ch, ch.upper()) for ch in w)


def _cons(w: str) -> str:
    w = w.replace("'", "")
    return "".join(VOICE.get(ch, ch.upper()) for ch in w if ch not in "aeiou")


def _levenshtein(a: str, b: str, maxd: int = MAX_EDIT) -> int:
    if abs(len(a) - len(b)) > maxd:
        return maxd + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        if min(cur) > maxd:
            return maxd + 1
        prev = cur
    return prev[-1]


def word_hit(sig: str, word: str) -> bool:
    """Signal so'zi matndagi so'zga mos keladimi.

    Talablar (ataylab qat'iy):
      • aynan teng → ha;
      • so'z signaldan boshlanadi va signal ≥4 harf → ha (qo'shimcha);
      • undosh-sinf prefiksi ≥4 harf → ha (k/g/q almashinuvi);
      • ≥6 harfli so'zlarda 1 imlo xatosi → ha.
    «qon»/«kun» (3 harf, prefiks yo'q) → yo'q. «gap»/«ko'p» → yo'q.
    """
    a, b = norm(sig), norm(word)
    if not a or not b:
        return False
    if a == b:
        return True
    if len(a) >= MIN_STEM and b.startswith(a):
        return True
    if len(a) == 3 and b.startswith(a) and b[3:].startswith(SUFFIX_START):
        return True
    fa, fb = fuzzy_key(a), fuzzy_key(b)
    # Ikki tomon ham ≥4 bo'lishi shart: «birdan» ↔ «bir» mos kelmasin.
    if len(fa) >= MIN_STEM and len(fb) >= MIN_STEM and \
            (fb.startswith(fa) or fa.startswith(fb)):
        return True
    # Unli tushishi: qorin → qornim, burun → burnim.
    # Xavfsizlik: dastlabki 3 belgi AYNAN teng bo'lishi shart — «qon»/«kun»
    # va «gap»/«ko'p» bu yerga tushmaydi (critic.md).
    if len(a) >= 4 and len(b) >= 4 and a[:3] == b[:3] and abs(len(a) - len(b)) <= 4:
        ca, cb = _cons(a), _cons(b)
        if len(ca) >= 3 and (cb.startswith(ca) or ca.startswith(cb)):
            return True
    if len(a) >= 6 and len(b) >= 6 and _levenshtein(a, b) <= MAX_EDIT:
        return True
    return False


def is_negated(toks: list[str], idx: int, sig: str = "") -> bool:
    """Shu so'z inkor qilinganmi: «og'rimayapti», «og'riq yo'q», «... emas».

    Muhim: inkor faqat signal O'ZAGIGA qo'shilganda hisoblanadi.
    «sezmayapti» — sezmay + apti, inkor emas (bu simptom).
    «og'rimayapti» — og'ri + mayapti, inkor (shikoyat yo'q).
    """
    if not (0 <= idx < len(toks)):
        return False
    w = toks[idx]
    a = norm(sig) if sig else ""
    if a and w.startswith(a):
        rest = w[len(a):]
        if rest and rest.startswith(NEG_STEMS):
            return True
    for nxt in toks[idx + 1: idx + 3]:
        if nxt in NEG_TOKENS:
            return True
    for prev in toks[max(0, idx - 2): idx]:
        if prev in NEG_TOKENS:
            return True
    return False


def phrase_hit(phrase: str, text: str, toks: list[str] | None = None) -> bool:
    """Barcha so'zlar topildi va (ko'p so'zli bo'lsa) 6 so'z oynasida."""
    toks = toks if toks is not None else tokens(text)
    parts = tokens(phrase)
    if not parts or not toks:
        return False
    if len(parts) == 1:
        return any(word_hit(parts[0], w) and not is_negated(toks, i, parts[0])
                   for i, w in enumerate(toks))

    hits = [[i for i, w in enumerate(toks)
             if word_hit(p, w) and not is_negated(toks, i, p)] for p in parts]
    if any(not h for h in hits):
        return False
    # tartib + yaqinlik
    for start in hits[0]:
        pos, ok = start, True
        for h in hits[1:]:
            nxt = [i for i in h if i > pos]
            if not nxt:
                ok = False
                break
            pos = nxt[0]
        if ok and pos - start <= 6:
            return True
    return False


def any_hit(phrases, text: str, toks: list[str] | None = None) -> str | None:
    toks = toks if toks is not None else tokens(text)
    for p in phrases:
        if phrase_hit(p, text, toks):
            return p
    return None


def split_lines(s: str) -> list[str]:
    return [x.strip() for x in re.split(r"[\n;]+", s or "") if x.strip()]
