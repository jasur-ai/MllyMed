"""Yo'llar va yadroni ulash — bitta joyda.

`built/` ikki xil muhitda ishlaydi:
  • yig'ilgan (vendor/orindor bor) — ko'chirib ko'rsatish uchun;
  • ishlab chiqish (vendor yo'q) — `../orindor` dan to'g'ridan-to'g'ri.
"""
from __future__ import annotations

import sys
from pathlib import Path

BUILT = Path(__file__).resolve().parents[1]
REPO = BUILT.parent
VENDOR = BUILT / "vendor" / "orindor"
SOURCE_CORE = REPO / "orindor"
DATA = BUILT / "data"
RUNTIME = DATA / "runtime"
STATIC = BUILT / "src" / "web" / "static"


def core_dir() -> Path:
    return VENDOR if (VENDOR / "core").is_dir() else SOURCE_CORE


def ensure_core() -> Path:
    """Yadroni `sys.path` ga qo'shadi va papkasini qaytaradi."""
    d = core_dir()
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))
    return d


def core_data(name: str) -> Path:
    return core_dir() / "data" / name


def ensure_runtime() -> Path:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    return RUNTIME
