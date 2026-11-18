"""Matn shakllantirish — barcha chiqish shu yerdan o'tadi.

Bu qatlam ATAYLAB shablonli: har raqam ma'lumotdan, har da'vo fakt raqami
bilan. LLM keyin qo'shilsa ham, matn `safety.validate_*` dan o'tishi shart.
"""
from __future__ import annotations

from . import evidence, registry, sources
from .triage import Guess, SPECIALISTS, Urgency


def fmt(n) -> str:
    if n is None:
        return "—"
    if isinstance(n, float):
        s = f"{n:,.2f}".rstrip("0").rstrip(".")
        return s.replace(",", " ")
    return f"{n:,}".replace(",", " ")


def _local_tag(local: bool) -> str:
    return "MAHALLIY 🇺🇿" if local else "IMPORT 🌍"


def emergency_text(flag) -> str:
    level = "SHOSHILINCH — 103" if flag.level.value == "SHOSHILINCH" else "BUGUN"
    return (
        f"⛔ {level}\n"
        f"   Hoziroq 103 ni chaqiring yoki eng yaqin tez yordam bo'limiga boring.\n"
        f"   Sabab: {flag.why}.\n"
        "   Men bu holatda navbatga yozmayman va dori aytmayman — bu xavfli.\n"
        "   Keyingi qadam faqat bitta: tibbiy yordam."
    )


def screening_text(s) -> str:
    return (
        "❓ Aniqlashtirish kerak — bu xavfsizlik uchun majburiy savol:\n"
        f"   {s.question}\n"
        "   «ha» yoki «yo'q» deb yozing. Javob noaniq bo'lsa, xavfsiz tomonga "
        "o'taman."
    )


def ambiguity_text(query: str, cands) -> str:
    lines = [f"🔎 «{query}» bo'yicha {len(cands)} ta variant topildi. "
             "Qaysi birini tekshiramiz? (raqamini yozing)"]
    for i, c in enumerate(cands, 1):
        lines.append(f"   {i}. {c.line()}")
    lines.append("   Yoki aniqroq yozing: «paratsetamol 500».")
    return "\n".join(lines)


def card_text(c: dict) -> str:
    if not c:
        return "Karta topilmadi."
    L: list[str] = []
    name = c["name"] or c["full"][:60]
    L.append(f"💊 {name} — {c['strength'] or '—'}, {c['form_uz']}")
    L.append(f"   XPN (INN)        : {c['inn'] or '—'}")
    L.append(f"   Ishlab chiqaruvchi: {c['manufacturer'] or '—'} "
             f"({c['country'] or '—'}) — {_local_tag(c['local'])}")
    L.append(f"   Reyestr raqami   : {c['reg'] or '—'} · ATX {c['atc'] or '—'} · "
             f"{'Retsept bilan' if c['rx'] else 'Retseptsiz'}")
    L.append("   Holat            : ✅ davlat reyestrida ro'yxatga olingan")
    L.append("")

    # ── narx
    p, lim = c.get("price"), c.get("limit")
    grp = c.get("group") or {}
    L.append("💰 NARX — 3735-son bo'yicha CHEGARA narx (dorixona narxi emas)")
    if p:
        if p.get("retail"):
            L.append(f"   Referent chakana : {fmt(p['retail'])} so'm")
        if p.get("wholesale"):
            L.append(f"   Referent ulgurji : {fmt(p['wholesale'])} so'm")
        if p.get("base") and p.get("currency"):
            L.append(f"   Bazaviy narx     : {fmt(p['base'])} {p['currency']}")
        L.append(f"   Narx sanasi      : {p.get('date') or '—'}")
    else:
        L.append("   Referent narx    : MA'LUM EMAS — bu yozuv narx reyestrida yo'q")
        if grp.get("priced"):
            L.append(f"   Guruhda           : {grp['priced']} narxli yozuv bor "
                     "(boshqa doza/shakl — bevosita solishtirilmaydi)")
    if lim and lim.get("max") is not None:
        L.append(f"   Chegara narx     : {fmt(lim['max'])} {lim['currency']} "
                 f"({lim.get('date') or '—'})")
        if lim.get("retail"):
            L.append(f"   Shu yozuvdagi chakana: {fmt(lim['retail'])} so'm")
    L.append("   Manba: api.mpa.uz · lex.uz/uz/docs/-7952162")
    L.append("")

    # ── guruh
    g, same = c.get("group") or {}, c.get("same") or {}
    L.append(f"📊 GURUH — {c.get('inn_display') or c['inn']}: "
             f"{fmt(g.get('n', 0))} yozuv "
             f"({fmt(g.get('local', 0))} mahalliy · {fmt(g.get('import', 0))} import)")
    if same.get("n"):
        L.append(f"   Bir xil shakl/doza: {same['n']} yozuv · "
                 f"narxli: mahalliy {same.get('local', 0)}, "
                 f"import {same.get('import', 0)}")
    if same.get("local_min") and same.get("import_min"):
        L.append(f"   Eng past chegara narx (bir xil shakl/doza): mahalliy "
                 f"{fmt(same['local_min'])} so'm · import "
                 f"{fmt(same['import_min'])} so'm → {same.get('diff_pct')}% farq")
    elif g.get("local_min") and g.get("import_min"):
        L.append(f"   Eng past chegara narx (turli doza — solishtirish emas): "
                 f"mahalliy {fmt(g['local_min'])} · import "
                 f"{fmt(g['import_min'])} so'm")
    else:
        L.append("   Narxli taqqoslash: MA'LUM EMAS — guruhda narx yo'q")
    L.append("   ⚠️ Bu chegara narxlar; dorixonadagi haqiqiy narx farq emas.")
    L.append("")

    # ── dalil
    L.append("🧪 DALIL (A2) — bioekvivalentlik")
    L.append("   Hisobot            : MA'LUM EMAS — davlat dosyesi yopiq "
             "(ochiq manbada yo'q)")
    L.append("   2029-01-01 dan     : ICH talablariga muvofiq BE MAJBURIY — "
             "738-son, 24.11.2025")
    L.append("   80% qoidasi        : jenerik ≤ originalning 80% — 3735-son")
    L.append(f"   GMP sertifikati    : {sources.gmp_short()}")
    L.append("")

    # ── haqiqiylik
    L.append("🔐 HAQIQIYLIK (A1)")
    L.append("   ASL BELGISI        : 2027-07-01 dan dori vositalarida majburiy "
             "— 149-son")
    L.append("   Kod tekshiruvi     : HOZIR tekshirilmadi — Operator API yopiq")
    L.append("")

    L.append("📚 Manbalar:")
    for label, url in registry.registry_sources(c["id"]):
        L.append(f"   · {label}: {url}")
    L.append("")
    L.append("⚕️ Bu tibbiy maslahat emas va retsept emas. Qaror — shifokor yoki "
             "farmatsevt.")
    return "\n".join(L)


def why_text(c: dict) -> str:
    same, g = c.get("same") or {}, c.get("group") or {}
    L = ["❓ «Nega arzon?» — javob hujjat bilan, taxmin emas."]
    if same.get("diff_pct") is not None and same.get("local_min") and same.get("import_min"):
        L.append(f"   Bir xil shakl/doza: mahalliy {fmt(same['local_min'])} so'm · "
                 f"import {fmt(same['import_min'])} so'm → "
                 f"{same['diff_pct']}% farq")
    elif g.get("local_min") and g.get("import_min"):
        L.append(f"   Guruhdagi eng past: mahalliy {fmt(g['local_min'])} · "
                 f"import {fmt(g['import_min'])} so'm")
        L.append("   ⚠️ Bu TURLI DOZALARDAGI narxlar — bevosita solishtirish emas. "
                 "Bir xil shakl/doza bo'yicha ma'lumot yo'q.")
    else:
        L.append("   Bu dori bo'yicha narx solishtirish MA'LUM EMAS.")
        L.append(f"   {evidence.cite('F09')}")
        return "\n".join(L)

    L.append("")
    L.append("   Sabab 1 — 80% qoidasi (3735-son, F09):")
    L.append("     «Jenerik referent narxi originalning 80 foizidan qimmat "
             "bo'lishi mumkin emas.»")
    L.append("   Sabab 2 — mahalliy formula (F08): ChUN = (Rn + QQS) × UU — "
             "bojxona to'lovi yo'q.")
    ex = evidence.price_model().get("example", {})
    if ex:
        L.append("")
        L.append(f"   MISOL (hujjatdagi formula bilan, real dorixonadan emas): "
                 f"original {fmt(ex.get('original_referent_narx_som'))} so'm → "
                 f"import {fmt(ex.get('import_yakuniy_narx_som'))} · "
                 f"mahalliy {fmt(ex.get('mahalliy_yakuniy_narx_som'))} so'm "
                 f"({ex.get('farq_foiz')}% farq).")
    L.append(f"   Manba: {evidence.REF_URL}")
    L.append("   ⚠️ Chegara — ruxsat etilgan eng yuqori narx. Dorixonadagi "
             "haqiqiy narx alohida.")
    return "\n".join(L)


def evidence_text(c: dict) -> str:
    L = ["🧪 «Ishonsa bo'ladimi?» — dalil holati (yashirmasdan):"]
    L.append("   ✅ Ro'yxatdan o'tgan: ha — davlat reyestrida, raqami "
             f"{c['reg'] or '—'}")
    L.append("   ✅ Markirovka tartibi: ASL BELGISI 2027-07-01 dan majburiy "
             "(149-son)")
    L.append("   ❓ Bioekvivalentlik hisoboti: MA'LUM EMAS — davlat dosyesi yopiq.")
    L.append("   ❓ " + sources.gmp_text())
    L.append("")
    L.append("   Nima uchun BE muhim: 2029-01-01 dan jeneriklar uchun ICH "
             "talablariga muvofiq BE majburiy (738-son, F01).")
    L.append("   Ya'ni «ishonch» hozir ikki qismdan: hujjat (bor) + ko'rinish "
             "(yo'q). Biz ikkinchisini ko'rsatamiz, birinchisini taxmin "
             "qilmaymiz.")
    return "\n".join(L)


def triage_text(guess: Guess | None, urgency: Urgency, second: Guess | None,
                age: int | None = None, screened: bool = False,
                fallback: bool = False) -> str:
    if guess is None:
        return (
            "🧭 Aniq mutaxassisni ayta olmayman — taxmin qilmayman.\n"
            "   Eng to'g'ri qadam: TERAPEVT (oilaviy shifokor). U ko'rikdan "
            "keyin kerak bo'lsa tor mutaxassisga yo'naltiradi."
        )
    L = [f"🧭 Yo'naltirish: {guess.label}"]
    if guess.hits:
        L.append("   Sabab: " + ", ".join(f"«{h}»" for h in guess.hits[:4]))
    L.append(f"   Muddat: {urgency.text} — {urgency.when}")
    if second and second.score >= guess.score * 0.75:
        L.append(f"   Ikkinchi variant: {second.label}")
    if age is not None:
        L.append(f"   Yosh hisobga olindi: {age}")
    if screened:
        L.append("   Skrining: savolga javob asosida (xavfsiz default qo'llandi)")
    if fallback:
        L.append("   Diqqat: aniq belgi topilmadi — bu taxmin emas, umumiy yo'l.")
    L.append("")
    L.append("   Men tashxis qo'ymayman va dori aytmayman — buni faqat shifokor "
             "qiladi. Mening ishim: to'g'ri mutaxassisga olib borish.")
    return "\n".join(L)


def booking_text(specialty: str, urgency: Urgency) -> str:
    return (
        "📅 Keyingi qadam — navbatni MEN TASDIQLAMAYMAN\n"
        f"   Mutaxassis: {SPECIALISTS[specialty]} · {urgency.text} "
        f"({urgency.when})\n"
        f"   1) {evidence.QUEUE_URL} — vaqtni o'zingiz tanlaysiz\n"
        "   2) DMED ilovasi — oilaviy shifokor qabuli\n"
        "   3) Eslatma kerak bo'lsa: «eslatma ertaga 09:30» deb yozing\n"
        "   Men havolani ochmayman va hech narsani bron qilmayman — buni "
        "faqat siz tasdiqlaysiz."
    )


def reminder_list(s) -> str:
    if not s.reminders:
        return "📭 Rejalashtirilgan eslatma yo'q. «eslatma ertaga 09:30» deb yozing."
    L = ["⏰ Eslatmalar (vaqt bo'yicha, qurilmada saqlanadi):"]
    for r in s.reminders:
        mark = "✅" if r.sent_at else "•"
        L.append(f"   {mark} {r.when.strftime('%d.%m.%Y %H:%M')} — {r.subject}")
    L.append("   Bu push-bildirishnoma emas: ilova ochiq bo'lganda vaqti kelgan "
             "eslatmalar ko'rsatiladi.")
    return "\n".join(L)
