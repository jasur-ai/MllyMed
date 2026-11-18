"""Sessiya holati, eslatmalar, offline navbat.

Critic.md P2 (demo halolligi):
  • navbat «tasdiqlandi» deb yozilmaydi — faqat davlat havolasi;
  • eslatma vaqti foydalanuvchi bergan vaqt; taymer/kalit soxta emas;
  • offline navbat HAQIQATAN diskka yoziladi (xotirada emas).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .safety import Screening
from .triage import Guess, Urgency

RUNTIME = Path(__file__).resolve().parent.parent / "data" / "runtime"


@dataclass
class Reminder:
    subject: str
    when: datetime
    sent_at: datetime | None = None
    simulated: bool = False

    def to_dict(self) -> dict:
        return {"subject": self.subject, "when": self.when.isoformat(),
                "sent_at": self.sent_at.isoformat() if self.sent_at else None,
                "simulated": self.simulated}


class Outbox:
    """Offline yozuvlar — haqiqiy fayl. `flush` ularni `outbox_sent.json` ga
    ko'chiradi va qaytaradi. Tarmoqqa yuborilmaydi (server yo'q)."""

    def __init__(self, path: Path | None = None):
        self.path = path or (RUNTIME / "outbox_pending.json")
        self.sent_path = self.path.with_name("outbox_sent.json")
        self.items: list[dict] = []
        self._load()

    def _load(self) -> None:
        try:
            self.items = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.items = []

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.items, ensure_ascii=False, indent=1),
                             encoding="utf-8")

    def add(self, action: str, payload: dict) -> None:
        self.items.append({"action": action, "payload": payload,
                           "created": datetime.now().isoformat()})
        self._save()

    def pending(self) -> int:
        return len(self.items)

    def flush(self, online: bool = True) -> list[dict]:
        if not online or not self.items:
            return []
        sent = list(self.items)
        try:
            old = json.loads(self.sent_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            old = []
        old.extend(sent)
        self.sent_path.parent.mkdir(parents=True, exist_ok=True)
        self.sent_path.write_text(json.dumps(old, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
        self.items = []
        self._save()
        return sent


@dataclass
class Session:
    mode: str | None = None            # "card" | "triage" | None
    stage: str = "idle"
    age: int | None = None
    sex: str | None = None
    pregnant: bool = False
    child: bool = False
    asked_age: bool = False
    symptoms: list[str] = field(default_factory=list)
    guess: Guess | None = None
    urgency: Urgency = Urgency.ROUTINE
    screening: Screening | None = None
    asked_topics: list[str] = field(default_factory=list)
    card: dict | None = None
    candidates: list = field(default_factory=list)
    turns: list[dict] = field(default_factory=list)
    reminders: list[Reminder] = field(default_factory=list)
    booking: dict | None = None
    outbox: Outbox = field(default_factory=Outbox)

    def add(self, role: str, text: str) -> None:
        self.turns.append({"role": role, "text": text,
                           "at": datetime.now().isoformat()})

    def say(self, text: str) -> str:
        self.add("agent", text)
        return text

    def reset(self) -> None:
        self.mode = None
        self.stage = "idle"
        self.symptoms = []
        self.guess = None
        self.screening = None
        self.asked_topics = []
        self.card = None
        self.candidates = []
        self.asked_age = False
        self.urgency = Urgency.ROUTINE

    def due_reminders(self, now: datetime | None = None) -> list[Reminder]:
        now = now or datetime.now()
        out = []
        for r in self.reminders:
            if r.sent_at is None and r.when <= now:
                r.sent_at = now
                out.append(r)
        return out
