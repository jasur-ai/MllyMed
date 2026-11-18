#!/usr/bin/env python3
"""Virtual tajriba — stsenariylar bo'yicha agentni yurgizib, invariantlarni tekshiradi.

Bu "foydalanuvchi simulyatsiyasi": har stsenariy — persona + qadamlar.
Har qadamda:
  • javob yadro validatoridan o'tganmi (triajda taqiqlangan gaplar yo'qmi);
  • agent navbatni "tasdiqladi" deb yozmaganmi;
  • favqulodda holatda 103 chiqqanmi, navbat yaratilmaganmi;
  • karta bo'lsa reyestr raqami bormi, dorixona takliflari bog'langanmi.

Natija: `data/sim_report.json` + `sim/report.md` (qo'lda yozilmaydi).

Ishga tushirish (built/ ichidan):
    python3 sim/run.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILT = HERE.parent
sys.path.insert(0, str(BUILT))

from src import paths  # noqa: E402

paths.ensure_core()

from core.safety import violations  # noqa: E402
from src.bridge import Bridge  # noqa: E402

SCEN = HERE / "scenarios.json"
OUT_JSON = paths.DATA / "sim_report.json"
OUT_MD = HERE / "report.md"


def run_scenario(bridge: Bridge, scn: dict, state_path: Path) -> dict:
    sid = scn["id"]
    replies = []
    for text in scn["steps"]:
        r = bridge.chat(sid, text)
        replies.append(r)
        # invariant: triaj javobida taqiqlangan mazmun yo'q
        if (r.get("mode") == "triage"):
            for v in violations(r["reply"], "triage"):
                replies.append({"violation": v, "text": text})
    last = replies[-1]
    checks: list[tuple[str, bool, str]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))

    exp = scn.get("expect", {})
    if "stage" in exp:
        add(f"stage={exp['stage']}", last.get("stage") == exp["stage"],
            f"chiqdi: {last.get('stage')}")
    if "reply_has" in exp:
        for w in exp["reply_has"]:
            add(f"javobda «{w}»", w.lower() in last["reply"].lower())
    if "reply_not_has" in exp:
        for w in exp["reply_not_has"]:
            add(f"javobda «{w}» yo'q", w.lower() not in last["reply"].lower())
    if exp.get("has_card"):
        add("karta bor", bool(last.get("card")))
    if exp.get("card_reg"):
        add("reyestr raqami bor", bool((last.get("card") or {}).get("reg")))
    if "apteka_min" in exp:
        add(f"dorixona taklifi ≥{exp['apteka_min']}",
            (last.get("apteka") or {}).get("count", 0) >= exp["apteka_min"])
    if "dmed_doctors_min" in exp:
        add(f"DMED shifokor ≥{exp['dmed_doctors_min']}",
            len((last.get("dmed") or {}).get("doctors", [])) >= exp["dmed_doctors_min"])

    # global invariantlar
    appts = bridge.dmed.appointments(sid)
    if exp.get("no_appointments"):
        add("agent navbat yaratmadi", not appts, f"{len(appts)} ta")
    add("«tasdiqlandi» degan da'vo yo'q",
        "tasdiqlandi" not in last["reply"].lower())
    bad = [x for x in replies if "violation" in x]
    add("validator: taqiqlangan mazmun yo'q", not bad,
        "; ".join(x["violation"] for x in bad[:2]))

    return {"id": scn["id"], "persona": scn.get("persona", ""),
            "steps": scn["steps"], "ok": all(c[1] for c in checks),
            "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
            "final_stage": last.get("stage"),
            "final_reply": last["reply"][:400]}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                       # noqa: BLE001
        pass
    scenarios = json.loads(SCEN.read_text(encoding="utf-8"))
    results = []
    with tempfile.TemporaryDirectory() as td:
        for scn in scenarios:
            # har stsenariy — toza DMED holati (bir-biriga ta'sir qilmasin)
            state = Path(td) / f"{scn['id']}.json"
            bridge = Bridge(state)
            results.append(run_scenario(bridge, scn, state))

    passed = sum(1 for r in results if r["ok"])
    failed = [r for r in results if not r["ok"]]
    report = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "total": len(results), "passed": passed, "failed": len(failed),
        "scenarios": results,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=1),
                        encoding="utf-8")

    lines = ["# Virtual tajriba — natijalar", "",
             f"Yaratilgan: {report['generated']} · "
             f"**{passed}/{len(results)} stsenariy o'tdi**", "",
             "| # | Stsenariy | Persona | Natija | Bosqich |",
             "|---|---|---|---|---|"]
    for i, r in enumerate(results, 1):
        mark = "✅" if r["ok"] else "❌"
        lines.append(f"| {i} | `{r['id']}` | {r['persona']} | {mark} | "
                     f"{r['final_stage']} |")
    if failed:
        lines += ["", "## O'tmagan tekshiruvlar", ""]
        for r in failed:
            lines.append(f"### `{r['id']}`")
            for c in r["checks"]:
                if not c["ok"]:
                    lines.append(f"- ❌ {c['name']} {('— ' + c['detail']) if c['detail'] else ''}")
            lines.append(f"- javob: `{r['final_reply'][:200]}`")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("═" * 70)
    print("VIRTUAL TAJRIBA".center(70))
    print("═" * 70)
    for r in results:
        print(f"  {'✅' if r['ok'] else '❌'} {r['id']:<20} {r['final_stage']}")
        for c in r["checks"]:
            if not c["ok"]:
                print(f"       ⛔ {c['name']} {c['detail']}")
    print("─" * 70)
    print(f"NATIJA: {passed}/{len(results)} · xato: {len(failed)}")
    print(f"→ {OUT_JSON}\n→ {OUT_MD}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
