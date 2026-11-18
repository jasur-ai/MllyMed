"""MllyMed Backend Konfiguratsiyasi va Yo'llar."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
BUILT_DIR = ROOT_DIR / "built"
DATA_DIR = ROOT_DIR / "data"
AGENT_DIR = ROOT_DIR / "agent"
CORE_DIR = ROOT_DIR / "orindor"

# Agar data/ papkasida fayllar bo'lmasa, built/data dan foydalanamiz
if not (DATA_DIR / "apteka_catalog.json").exists() and (BUILT_DIR / "data" / "apteka_catalog.json").exists():
    DATA_PATH = BUILT_DIR / "data"
else:
    DATA_PATH = DATA_DIR

STATIC_DIR = FRONTEND_DIR if FRONTEND_DIR.is_dir() else (BUILT_DIR / "src" / "web" / "static")

# Core agent import yo'lini ta'minlash
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
