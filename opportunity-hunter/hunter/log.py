"""Run logging: human-readable timeline + structured JSONL events."""
from __future__ import annotations

import datetime as _dt
import json
import threading
from pathlib import Path


class RunLogger:
    def __init__(self, log_dir: Path, echo: bool = True):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.text_path = self.log_dir / "run.log"
        self.events_path = self.log_dir / "events.jsonl"
        self.echo = echo
        self._lock = threading.Lock()

    def log(self, actor: str, message: str, level: str = "INFO", **data) -> None:
        now = _dt.datetime.now()
        prefix = "" if level == "INFO" else f"{level} "
        line = f"[{now:%H:%M:%S}] {prefix}{actor} {message}"
        event = {"ts": now.isoformat(timespec="seconds"), "level": level,
                 "actor": actor, "message": message, **data}
        with self._lock:
            with self.text_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
            with self.events_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
            if self.echo:
                print(line, flush=True)

    def events(self) -> list[dict]:
        if not self.events_path.exists():
            return []
        return [json.loads(l) for l in self.events_path.read_text(encoding="utf-8").splitlines() if l.strip()]
