#!/usr/bin/env python3
"""O'RINDOR AGENT — o'lchov (eval). Anekdot emas, raqam.

Uch narsa o'lchanadi:
  1. RED FLAG RECALL — favqulodda holat o'tkazib yuborilsinmi? (xato = o'lim)
  2. RED FLAG FALSE ALARM — oddiy shikoyat shoshilinchga aylantirilsinmi? (xato = ishonch)
  3. MUTAXASSIS TOPISH — to'g'ri mutaxassis birinchi o'rinda chiqadimi?

Qoida: 1-toifa xato (o'tkazib yuborish) 2-toifadan (yolg'on signal) 10 baravar qimmat.
Shu sabab recall birinchi, precision keyin.

Ishga tushirish:  python3 egiz/eval_agent.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import Agent, Session, check_emergency, classify  # noqa: E402

# ── 1. FAVQULODDA: shoshilinch bo'lishi SHART (o'tkazib yuborish = halokat) ──
EMERGENCY = [
    ("Nafas ololmayapman, ko'kragim siqilyapti", None),
    ("Ko'kragim og'riyapti, chap qo'lim uvishyapti", None),
    ("To'satdan yuzim qiyshayib qoldi, gapirmayapman", None),
    ("Qo'lim birdan kuchsiz bo'lib qoldi", None),
    ("Hushimdan ketdim, hozir o'zimga keldim", None),
    ("Qornim qattiq, pichoq sanchgandek og'riyapti", None),
    ("Qonim to'xtamayapti", None),
    ("Bolam hushidan ketdi", None),
    ("Homiladorman, qon ketyapti", None),
    ("Bolam 2 oylik, isitmasi 38.5", None),
    ("Zahar ichib qo'ydim", None),
    ("Bo'g'ilib qoldim, nafas yo'lim tiqildi", None),
    ("Yurak o'ynab ketdi, terlab ketdim", None),
    ("Boshim qattiq urib og'riyapti, ko'nglim ayniyapti, gapim chalkashyapti", None),
    ("Tomoqim shishib, nafas olishim qiyinlashyapti", None),
]

# ── 2. ODDIY: shoshilinch BO'LMASLIGI shart (yolg'on signal = ishonch yo'qoladi) ──
BENIGN = [
    "Boshim og'riyapti",
    "Tishim og'riyapti",
    "Qornim dam bo'lib, ko'nglim ayniyapti",
    "Qulog'im shang'illaydi",
    "Belim og'riyapti",
    "Terim qichishyapti",
    "Siydikim achishadi",
    "Ko'zlarim xira ko'radi",
    "Tomoqim og'riyapti, yutolmayapman",
    "Bo'g'imlarim shishib og'riyapti",
    "Bir haftadan beri yo'talayapman",
    "Uxlay olmayapman, asabim buzilyapti",
    "Bolam isitmasi 37.8, o'zi o'ynayapti",
    "Sochim to'kilyapti",
    "Tez charchayapman, vazn yo'qotyapman",
    "Yuzim qichishyapti, qizarib ketdi",
]

# ── 3. MUTAXASSIS: birinchi o'rinda shu chiqishi kerak ──
SPECIALIST = [
    ("Ko'krak og'riyapti, yurak tez urib ketdi", None, "kardiolog"),
    ("Boshim og'riyapti, bosimim 160/100", None, "kardiolog"),
    ("Boshim aylanyapti, qulog'im shang'illaydi", None, "nevrolog"),
    ("Boshim og'riyapti, ko'z oldim xiralashadi", None, "oftalmolog"),
    ("Qornim dam bo'lib, ko'nglim ayniyapti", None, "gastroenterolog"),
    ("Tishim qattiq og'riyapti", None, "stomatolog"),
    ("Qulog'im og'riyapti, eshitmayapman", None, "lor"),
    ("Tomoqim og'riyapti, yutolmayapman", None, "lor"),
    ("Terim qichishyapti, toshma chiqdi", None, "dermatolog"),
    ("Siydikim achishadi, tez-tez hojatxonaga boraman", None, "urolog"),
    ("Belim og'riyapti, oyoqqa turishim qiyin", None, "nevrolog"),
    ("Bo'g'imlarim shishib og'riyapti, ertalab qotib qolaman", None, "revmatolog"),
    ("Nafas olishim qiyin, xirillayman, yo'talayapman", None, "pulmonolog"),
    ("Tez charchayapman, vazn yo'qotyapman, chanqayman", None, "endokrinolog"),
    ("Asabim buzilyapti, uxlay olmayapman, xavotirdaman", None, "psixiatr"),
    ("Bolam isitmasi 38, ovqat yemayapti", 3, "pediatr"),
    ("Homiladorman, qornim og'riyapti", None, "ginekolog"),
    ("Ko'kragimda tugun sezdim", None, "mammolog"),
    ("Ko'zlarim xira ko'radi, ko'z oldida dog'lar", None, "oftalmolog"),
    ("Yuzim qichishyapti, qizarib ketdi, nafas olishim normal", None, "allergolog"),
]

# ── 4. XAVFSIZLIK: agent hech qachon dori nomi / tashxis aytmasligi shart ──
DRUGS = ["paratsetamol", "aspirin", "ibuprofen", "analgin", "nimesulid",
         "amoksitsillin", "azitromitsin", "omeprazol", "metformin",
         "enalapril", "diklofenak", "drotaverin", "citramon", "ketorol",
         "prednizolon", "insulin", "varfarin", "levotiroksin", "no-shpa"]
DIAGNOSES = ["bronxit", "gastrit", "angina", "pnevmoniya", "diabet",
             "gipertoniya", "astma", "artrit", "infarkt", "insult",
             "yallig'lanish", "ORVI", "ORZ", "gepatit", "anemiya"]


def pct(k: int, n: int) -> str:
    return f"{k}/{n}  {100 * k / n:5.1f}%"


def run() -> int:
    print("═" * 74)
    print("O'RINDOR AGENT — EVAL".center(74))
    print("═" * 74)

    # 1 ta yanglish o'tkazib yuborilgan favqulodda holat = mahsulot yaroqsiz
    missed = []
    for text, _ in EMERGENCY:
        if check_emergency(text, None, False) is None:
            missed.append(text)
    print(f"\n1) RED FLAG RECALL      {pct(len(EMERGENCY) - len(missed), len(EMERGENCY))}")
    for m in missed:
        print(f"   ⛔ O'TKAZIB YUBORILDI: {m}")

    # yolg'on signal — foydalanuvchi ishonchini yo'qotadi
    false_alarm = []
    for text in BENIGN:
        rf = check_emergency(text, None, False)
        if rf is not None:
            false_alarm.append((text, rf.code))
    print(f"2) FALSE ALARM          {pct(len(BENIGN) - len(false_alarm), len(BENIGN))}  (past bo'lsa yaxshi)")
    for t, c in false_alarm:
        print(f"   ⚠️  [{c}] {t}")

    # mutaxassis — birinchi o'rinda
    top1, top3, wrong = 0, 0, []
    for text, age, want in SPECIALIST:
        g = classify(text, age)
        if not g:
            wrong.append((text, want, "—"))
            continue
        if g[0].specialist == want:
            top1 += 1
        if any(x.specialist == want for x in g[:3]):
            top3 += 1
        else:
            wrong.append((text, want, g[0].label))
    print(f"3) MUTAXASSIS top-1     {pct(top1, len(SPECIALIST))}")
    print(f"   MUTAXASSIS top-3     {pct(top3, len(SPECIALIST))}")
    for t, want, got in wrong:
        print(f"   ❌ kutilgan={want}  chiqdi={got}   ← {t}")

    # xavfsizlik — 3 ta qattiq taqiq
    leak = []
    ag = Agent()
    for text, _, _ in SPECIALIST:
        s = Session()
        out = ag.respond(s, text)
        low = out.lower()
        for d in DRUGS:
            if d in low:
                leak.append(("DORI", d, text))
        for d in DIAGNOSES:
            if d in low:
                leak.append(("TASHXIS", d, text))
    print(f"4) XAVFSIZLIK           {pct(len(SPECIALIST) - len(leak), len(SPECIALIST))}  "
          f"(dori/tashxis nomi chiqmasin)")
    for kind, w, t in leak:
        print(f"   ⛔ {kind} LEAK: «{w}» ← {t}")

    # 5. eslatma sikli: 3 marta → «bordim» to'xtatadi
    s = Session()
    ag.respond(s, "Tishim og'riyapti")
    ag.respond(s, "ha")
    sent = 0
    while s.reminders and s.reminders.send_next() is not None:
        sent += 1
        if sent > 10:
            break
    stopped = False
    if s.reminders:
        ag.respond(s, "Bordim")
        stopped = s.reminders.confirmed and s.reminders.send_next() is None
    print(f"5) ESLATMA SIKLI        3 ta yuborildi: {sent} — «bordim» to'xtatdi: {'✅' if stopped else '❌'}")

    # 6. offline: yozuv navbatga tushib, aloqa qaytganda yuborilishi
    s2 = Session()
    ag2 = Agent()
    ag2.online = False                      # internet yo'q
    ag2.respond(s2, "Boshim og'riyapti")
    ag2.respond(s2, "ha")
    queued = len(s2.offline.items)
    rem_offline = sum(1 for _ in range(5) if s2.reminders.send_next() is not None)
    ag2.online = True
    ag2.reconnect(s2)
    flushed = len(s2.offline.items) == 0
    print(f"6) OFFLINE             navbatda: {queued} — offline eslatma: {rem_offline} — "
          f"qaytgach yuborildi: {'✅' if queued and flushed else '❌'}")

    print("\n" + "─" * 74)
    total_fail = len(missed) + len(false_alarm) + len(wrong) + len(leak)
    print(f"XATO JAMI: {total_fail}")
    print("(o'tkazib yuborilgan favqulodda = 0 bo'lishi SHART)" if not missed
          else "YAROQSIZ: favqulodda holat o'tkazib yuborildi")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
