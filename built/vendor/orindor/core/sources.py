"""Manba holati qatlami — `data/source_status.json` (jonli probe natijasi).

Nega kerak: karta «ma'lum emas» deyotganda foydalanuvchi *nima uchun*
ma'lum emasligini bilishi shart. Ikki holat butunlay boshqa:

  CLOSED / BLOCKED — manba yopiq (API 401, sahifa yo'q) → so'rov kerak;
  UNRESOLVED       — manba OCHIQ, lekin bu qurilmadan yetib bo'lmadi
                     (DNS/tarmoq) → brauzerda ochiladi, kodga tarmoq kerak.

Ilgari kartada «GMP: ochiq reyestr E-IMZO talab qiladi» deb yozilgan edi.
Bu **noto'g'ri** edi: `uzpharm-gxp.uz/registry2` va `/registry6` — ochiq HTML
jadvallar, E-IMZO yo'q. 401 faqat `api.mpa.uz/.../gmp-registry` da.
Shuning uchun matn endi `source_status.json` dan olinadi, qo'lda yozilmaydi.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

GMP_LOCAL = "https://uzpharm-gxp.uz/registry2"
GMP_FOREIGN = "https://uzpharm-gxp.uz/registry6"
OPEN_DATA = "https://mpa.uz/uz/open-data"
DATA_PORTAL = "https://data.egov.uz/datasets"

STATUSES = ("OPEN", "SHELL", "CLOSED", "BLOCKED", "UNRESOLVED", "REQUEST")


@lru_cache(maxsize=1)
def load() -> dict:
    try:
        return json.loads((DATA / "source_status.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"built": None, "sources": []}


def items() -> list[dict]:
    return load().get("sources", [])


def built() -> str | None:
    return load().get("built")


def find(prefix: str) -> dict | None:
    for s in items():
        if (s.get("url") or "").startswith(prefix):
            return s
    return None


def status_of(prefix: str) -> str:
    s = find(prefix)
    return (s or {}).get("status") or "?"


def counts() -> dict:
    out: dict[str, int] = {}
    for s in items():
        st = s.get("status") or "?"
        out[st] = out.get(st, 0) + 1
    return out


def gmp_short() -> str:
    """Karta uchun bir qatorli, halol GMP holati."""
    st = status_of("https://uzpharm-gxp.uz")
    if st == "OPEN":
        return f"reyestr ochiq — tekshirish mumkin ({GMP_LOCAL})"
    if st == "UNRESOLVED":
        return ("TEKSHIRILMADI — reyestr OCHIQ (uzpharm-gxp.uz/registry2, "
                "registry6), lekin bu qurilmada domen ochilmadi (DNS). "
                "«Sertifikat yo'q» degani EMAS.")
    if st in ("CLOSED", "BLOCKED"):
        return f"TEKSHIRILMADI — reyestr bu so'rovda ochilmadi ({st})"
    return "TEKSHIRILMADI — manba holati noma'lum"


def gmp_text() -> str:
    """«Ishonsa bo'ladimi?» javobidagi to'liq GMP bandi."""
    st = status_of("https://uzpharm-gxp.uz")
    if st == "UNRESOLVED":
        return ("GMP sertifikati: TEKSHIRILMADI — OCHIQ reyestr bor "
                f"({GMP_LOCAL} mahalliy, {GMP_FOREIGN} xorijiy), ammo bu "
                "muhitda domen DNS'da topilmadi.\n"
                "     Ya'ni «sertifikat yo'q» emas: hujjat bor, biz hozir "
                "ko'ra olmadik. Taxmin qilmaymiz.")
    return f"GMP sertifikati: {gmp_short()}"


def open_data_note() -> str:
    """Ochiq ma'lumotlar bo'yicha bir qator — nima topildi, nima yo'q."""
    egov = status_of(DATA_PORTAL)
    return (f"Ochiq ma'lumotlar portali ({DATA_PORTAL}): {egov}. "
            "«Tarkibi bir xil, nomi turlicha» ro'yxati hali SO'ROV (363 ovoz), "
            "dataset emas — shu bo'shliqni INN guruhi yopadi.")


def card_sources() -> list[tuple[str, str]]:
    """Karta oxiridagi manba havolalari (faqat mavjudlari)."""
    out = []
    g = find("https://uzpharm-gxp.uz")
    if g:
        out.append(("GMP reyestri (ochiq HTML)", GMP_LOCAL))
        out.append(("GMP reyestri — xorijiy", GMP_FOREIGN))
    out.append(("Ochiq ma'lumotlar (mpa.uz)", OPEN_DATA))
    return out
