#!/usr/bin/env python3
"""`built/` ni yig'adi — tekshirilgan yadroni vendor qiladi, apteka katalogini quradi.

Nega vendor: `built/` o'z-o'ziga yetarli papka bo'lishi kerak (zip qilib
ko'rsatish mumkin), lekin yadro kodining ikkinchi nusxasi yozilmaydi.
Manba — `../orindor/`, `build.py` uni `vendor/orindor/` ga ko'chiradi.
Yadro o'zgarsa: `python3 built/build.py` (yoki `--check` bilan tekshirish).

Ishga tushirish:
    python3 built/build.py            # yig'ish
    python3 built/build.py --check    # manifest + import + sonlarni tekshirish
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BUILT = Path(__file__).resolve().parent
REPO = BUILT.parent
CORE_SRC = REPO / "orindor"
VENDOR = BUILT / "vendor" / "orindor"
DATA = BUILT / "data"
RAW = REPO / "workprocess" / "data"

CORE_FILES = ["agent.py"]
CORE_DATA = ["drugs.json", "inn.json", "refprice.json", "detail.json",
             "mini.json", "aliases.json", "stats.json", "facts.json",
             "source_status.json"]

HONESTY = {
    "apteka": ("48 mahsulot apteka.uz ochiq sahifalaridan, 20 mahsulot "
               "arzonapteka.uz vitrinasidan. Narx — «X so'mdan», aniq dorixona "
               "narxi emas."),
    "arzon_inn": ("ArzonApteka vitrinasida XPN (INN) maydoni yo'q — bu 20 "
                  "yozuv almashtirish uchun ISHLATILMAYDI, faqat narx "
                  "ko'rsatkichi sifatida qoladi."),
    "local": ("Mahalliy/import bayrog'i faqat apteka.uz yozuvlarida ma'lum "
              "(42/48); ArzonApteka yozuvlarida `local=null` — taxmin qilinmaydi."),
    "dmed": ("Mini DMED — SIMULYATSIYA. Shifokorlar, klinikalar, navbat "
             "vaqtlari sintetik; haqiqiy DMED API'siga bog'lanmagan."),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(s: str) -> str:
    return (s or "").lower().replace("ʻ", "'").replace("’", "'").replace("`", "'")


def vendor_core() -> None:
    if VENDOR.exists():
        shutil.rmtree(VENDOR)
    (VENDOR / "data").mkdir(parents=True)
    for f in CORE_FILES:
        shutil.copy2(CORE_SRC / f, VENDOR / f)
    shutil.copytree(CORE_SRC / "core", VENDOR / "core",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for f in CORE_DATA:
        src = CORE_SRC / "data" / f
        if src.exists():
            shutil.copy2(src, VENDOR / "data" / f)
        else:
            print(f"  ⚠️  yo'q: {src}")
    (VENDOR / "VENDORED.md").write_text(
        "# Vendor qilingan yadro\n\n"
        f"Manba: `{CORE_SRC}`\n\n"
        "Bu papka `built/build.py` tomonidan qayta yaratiladi — **qo'lda "
        "tahrirlanmaydi**. O'zgartirish kerak bo'lsa `orindor/` da qilinadi.\n",
        encoding="utf-8")


def build_apteka() -> dict:
    """Katalog: kengaytirilgan harvest bo'lsa o'sha, aks holda eski 48 ta."""
    arzon = json.loads((RAW / "arzon_vitrina.json").read_text(encoding="utf-8"))
    raw_path = DATA / "raw_apteka.json"
    harvest = None
    if raw_path.exists():
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        base = raw.get("products", [])
        harvest = raw.get("meta", {}).get("counts")
        base_source = "apteka.uz (kengaytirilgan harvest)"
    else:
        base = json.loads((RAW / "mini_apteka_katalog.json").read_text(encoding="utf-8"))
        base_source = "apteka.uz (mini katalog)"
    products: list[dict] = []

    for p in base:
        inn = p.get("inn")
        products.append({
            "id": p.get("id") or f"apteka-{len(products)}",
            "name": p.get("name"),
            "inn": inn,
            "inn_key": norm(inn) if inn else None,
            "has_inn": bool(inn),
            "manufacturer": p.get("manufacturer"),
            "country": p.get("country"),
            "local": p.get("local"),
            "seller": p.get("seller"),
            "price_from_som": p.get("price_from_som"),
            "pharmacies": p.get("pharmacies"),
            "category": p.get("category"),
            "rx": p.get("rx"),
            "url": p.get("url"),
            "source": "apteka.uz",
        })

    for i, p in enumerate(arzon):
        products.append({
            "id": f"arzon-{i:02d}",
            "name": p.get("name"),
            "inn": None,
            "inn_key": None,
            "has_inn": False,             # vitrinada XPN maydoni yo'q
            "manufacturer": p.get("manufacturer"),
            "country": None,
            "local": None,                # taxmin qilinmaydi
            "seller": "ArzonApteka",
            "price_from_som": p.get("price_from_som"),
            "pharmacies": None,
            "category": None,
            "rx": p.get("rx"),
            "url": p.get("source_url"),
            "source": "arzonapteka.uz",
        })

    with_inn = [p for p in products if p["has_inn"]]
    catalog = {
        "meta": {
            "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sources": [
                {"name": base_source, "count": len(base)},
                {"name": "arzonapteka.uz (vitrina, 20)", "count": len(arzon)},
            ],
            "harvest": harvest,
            "counts": {
                "products": len(products),
                "with_inn": len(with_inn),
                "without_inn": len(products) - len(with_inn),
                "inn_groups": len({p["inn_key"] for p in with_inn}),
                "local": sum(1 for p in with_inn if p["local"] is True),
                "import": sum(1 for p in with_inn if p["local"] is False),
            },
            "honesty": HONESTY,
        },
        "products": products,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "apteka_catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=1), encoding="utf-8")
    return catalog["meta"]


def build_manifest(meta: dict) -> None:
    stats = json.loads((VENDOR / "data" / "stats.json").read_text(encoding="utf-8"))
    files = {}
    for p in sorted(VENDOR.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            files[str(p.relative_to(BUILT)).replace("\\", "/")] = {
                "bytes": p.stat().st_size,
                "sha256": sha256(p),
            }
    manifest = {
        "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "core_source": str(CORE_SRC),
        "core_version": stats.get("schema"),
        "data": {k: stats.get(k) for k in
                 ("drugs", "local", "import", "inn_groups", "referent_prices",
                  "details", "price_coverage_pct")},
        "apteka": meta["counts"],
        "files": files,
    }
    (DATA / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")


def check() -> int:
    problems = []
    mpath = DATA / "build_manifest.json"
    if not mpath.exists():
        print("❌ manifest yo'q — avval `python3 built/build.py`")
        return 1
    m = json.loads(mpath.read_text(encoding="utf-8"))
    for rel, info in m["files"].items():
        p = BUILT / rel
        if not p.exists():
            problems.append(f"yo'q: {rel}")
        elif sha256(p) != info["sha256"]:
            problems.append(f"o'zgargan: {rel}")
    sys.path.insert(0, str(VENDOR))
    try:
        from core import registry  # noqa: PLC0415
        st = registry.stats()
        if st.get("drugs") != m["data"]["drugs"]:
            problems.append("reyestr soni manifest bilan mos emas")
        if not registry.search("paratsetamol"):
            problems.append("qidiruv ishlamayapti")
    except Exception as e:  # noqa: BLE001
        problems.append(f"core import: {type(e).__name__}: {e}")
    cat = json.loads((DATA / "apteka_catalog.json").read_text(encoding="utf-8"))
    if cat["meta"]["counts"] != m["apteka"]:
        problems.append("apteka katalogi manifest bilan mos emas")

    if problems:
        print("❌ CHECK FAIL")
        for p in problems:
            print("   -", p)
        return 1
    print("✅ CHECK OK")
    print(f"   core: {m['data']['drugs']} dori · {m['data']['inn_groups']} XPN · "
          f"narx qamrovi {m['data']['price_coverage_pct']}%")
    print(f"   apteka: {m['apteka']}")
    print(f"   fayllar: {len(m['files'])}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()

    print("═" * 74)
    print("BUILT · yig'ish".center(74))
    print("═" * 74)
    print("1/3 vendor core…")
    vendor_core()
    print(f"   → {VENDOR}")
    print("2/3 apteka katalogi…")
    meta = build_apteka()
    print(f"   → {DATA / 'apteka_catalog.json'} · {meta['counts']}")
    print("3/3 manifest…")
    build_manifest(meta)
    print(f"   → {DATA / 'build_manifest.json'}")
    return check()


if __name__ == "__main__":
    sys.exit(main())
