#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O'RINDOR — Milliy dori vositalariga ishonch ekotizimi.

Bitta buyruq bilan ishga tushirish skripti:
    python3 run.py              # Web serverni ishga tushiradi va brauzerni ochadi
    python3 run.py --cli        # Terminalda agent bilan jonli suhbat
    python3 run.py --test       # Barcha testlar va simulyatsiyalarni tekshirish
    python3 run.py --check      # Yadro va ma'lumotlar bazasi yaxlitligini tekshirish
    python3 run.py --port 8200  # Muayyan portda ishga tushirish
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BUILT_DIR = ROOT_DIR / "built"
ORINDOR_DIR = ROOT_DIR / "orindor"

# UTF-8 kodlashni ta'minlash
os.environ["PYTHONIOENCODING"] = "utf-8"

BANNER = r"""
  ___  ____  ___ _   _ ____   ___  ____  
 / _ \|  _ \|_ _| \ | |  _ \ / _ \|  _ \ 
| | | | |_) || ||  \| | | | | | | | |_) |
| |_| |  _ < | || |\  | |_| | |_| |  _ < 
 \___/|_| \_\___|_| \_|____/ \___/|_| \_\
                                         
   ★ №17 · Milliy dori vositalariga ishonch ekotizimi ★
"""


def print_banner() -> None:
    print("\033[1;36m" + BANNER + "\033[0m")
    print("\033[1;32m● Loyiha holati: To'liq tayyor va sinovdan o'tgan\033[0m")
    print("● Ma'lumotlar: 46 079 dori · 2 941 XPN · 308 dorixona taklifi")
    print("● Portallar: Bemor · Shifokor · Dorixona · Admin / Analitika\n")


def run_checks() -> bool:
    print("\033[1;33m[1/3] Baza va ma'lumotlar yaxlitligi tekshirilmoqda...\033[0m")
    cmd = [sys.executable, str(BUILT_DIR / "build.py"), "--check"]
    res = subprocess.run(cmd, cwd=str(BUILT_DIR))
    return res.returncode == 0


def run_tests() -> bool:
    print("\n\033[1;33m[2/3] Invariant testlar (17 ta qoida) tekshirilmoqda...\033[0m")
    cmd_tests = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    res_tests = subprocess.run(cmd_tests, cwd=str(BUILT_DIR))

    print("\n\033[1;33m[3/3] Virtual tajriba va stsenariylar (12 ta holat)...\033[0m")
    cmd_sim = [sys.executable, str(BUILT_DIR / "sim" / "run.py")]
    res_sim = subprocess.run(cmd_sim, cwd=str(BUILT_DIR))

    print("\n\033[1;33m[Qo'shimcha] Agent Halol Eval (10 ta o'lchov)...\033[0m")
    cmd_eval = [sys.executable, str(ORINDOR_DIR / "eval_agent.py")]
    res_eval = subprocess.run(cmd_eval, cwd=str(ORINDOR_DIR))

    success = (res_tests.returncode == 0 and res_sim.returncode == 0 and res_eval.returncode == 0)
    if success:
        print("\n\033[1;32m✅ BARCHA TESTLAR VA EVAL MUVAFFAQIYATLI O'TDI (0 ta xato)!\033[0m\n")
    else:
        print("\n\033[1;31m❌ Ayrim testlarda xatolik aniqlandi!\033[0m\n")
    return success


def run_cli_agent() -> None:
    print("\033[1;32mTerminalda O'RINDOR agenti ishga tushmoqda...\033[0m")
    print("Chiqish uchun 'chiqish' yoki 'exit' deb yozing.\n")
    cmd = [sys.executable, str(ORINDOR_DIR / "agent.py")]
    subprocess.run(cmd, cwd=str(ORINDOR_DIR))


def run_web_server(host: str = "127.0.0.1", port: int = 8200, open_browser: bool = True) -> None:
    # Serverni ishga tushirishdan oldin yo'llar va kataloglarni tayyorlash
    sys.path.insert(0, str(ROOT_DIR))
    sys.path.insert(0, str(BUILT_DIR))
    from src import paths
    paths.ensure_runtime()

    url = f"http://{host}:{port}"
    print(f"\033[1;32m🚀 Server ishga tushmoqda: \033[4;34m{url}\033[0m\033[0m")
    print("\033[1;37mMavjud modulli arxitektura va portallar:\033[0m")
    print("  1. 💊 \033[1mB2C Portali\033[0m — Dori vositalari katalogi, 80% mahalliy paritet, narxlar")
    print("  2. 🤖 \033[1mMllyMed AI\033[0m  — Klinik triaj, xavfsiz simptom skrining va yo'naltirish")
    print("  3. 📋 \033[1mBemor Kabineti\033[0m — Qabullar (DMED) va elektron retseptlar")
    print("  4. 🩺 \033[1mB2B Shifokor\033[0m — XPN bo'yicha e-retsept rasmiylashtirish va imzolash")
    print("  5. 💊 \033[1mB2B Dorixona\033[0m — Retseptlar navbati va dori berish (dispense)")
    print("  6. 🏭 \033[1mB2B Zavod/Admin\033[0m — Bozor qamrovi, GMP auditi va paritet ko'rsatkichlari")
    print("\n\033[90mServerni to'xtatish uchun: Ctrl+C bosing\033[0m\n")

    if open_browser:
        def _open():
            time.sleep(1.0)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        import threading
        threading.Thread(target=_open, daemon=True).start()

    try:
        from backend.server import MllyMedHandler, ThreadingHTTPServer
        handler_cls = MllyMedHandler
    except Exception:
        from src.web.server import H, ThreadingHTTPServer
        handler_cls = H

    try:
        srv = ThreadingHTTPServer((host, port), handler_cls)
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[1;33mServer to'xtatildi. Salomat bo'ling!\033[0m")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n\033[1;31mXato: Port {port} band! Boshqa port bilan urinib ko'ring:\033[0m")
            print(f"    python3 run.py --port {port + 1}\n")
        else:
            raise


def main() -> None:
    parser = argparse.ArgumentParser(description="O'RINDOR tizimini yagona buyruq bilan boshqarish")
    parser.add_argument("--cli", action="store_true", help="Terminalda agent bilan suhbatlashish")
    parser.add_argument("--test", action="store_true", help="Barcha testlar va evalni ishga tushirish")
    parser.add_argument("--check", action="store_true", help="Faqat ma'lumotlar bazasi va yadro yaxlitligini tekshirish")
    parser.add_argument("--port", type=int, default=8200, help="Web server porti (standart: 8200)")
    parser.add_argument("--host", default="127.0.0.1", help="Web server hosti (standart: 127.0.0.1)")
    parser.add_argument("--no-browser", action="store_true", help="Brauzerni avtomatik ochmaslik")

    args = parser.parse_args()
    print_banner()

    if args.check:
        run_checks()
        return

    if args.test:
        run_checks()
        run_tests()
        return

    if args.cli:
        run_cli_agent()
        return

    # Standart rejim: Web serverni ishga tushirish
    run_web_server(host=args.host, port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
