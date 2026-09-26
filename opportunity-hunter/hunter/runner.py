"""Agent execution layer.

Every agent run is a *separate OS process*: `claude -p` (Claude Code headless mode)
with its own system prompt, input, JSON schema, tool whitelist and hard limits.
The runner adds: budget accounting, retries, result caching, JSON validation,
per-run transcripts and observability.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import jsonschema

from .config import ROOT
from .db import Store
from .log import RunLogger
from .registry import AgentSpec

TRANSIENT_SUBTYPES = {"error_during_execution", "timeout", "crash", "no_output", "invalid_output"}


@dataclass
class AgentResult:
    agent: str
    task_label: str
    status: str                      # ok | failed | skipped
    output: dict | None = None
    cost_usd: float = 0.0
    searches: int = 0
    fetches: int = 0
    search_cache_hits: int = 0
    blocked_calls: int = 0
    turns: int = 0
    attempts: int = 0
    duration_sec: float = 0.0
    cache_hit: bool = False
    error: str | None = None
    pid: int | None = None
    session_id: str | None = None
    started_at: str = ""
    finished_at: str = ""
    queries: list[str] = field(default_factory=list)


@dataclass
class RawInvocation:
    ok: bool
    subtype: str
    structured_output: dict | None = None
    cost_usd: float = 0.0
    turns: int = 0
    tool_counts: dict = field(default_factory=dict)
    guard_state: dict = field(default_factory=dict)
    pid: int | None = None
    session_id: str | None = None
    error: str | None = None


class ClaudeCLIBackend:
    """Runs an agent as an independent `claude -p` subprocess."""

    def __init__(self, cfg: dict, work_dir: Path, cache_db: Path):
        self.cfg = cfg
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.cache_db = cache_db
        self.settings_path = self.work_dir / "guard_settings.json"
        guard = f"{sys.executable} {ROOT / 'hunter' / 'search_guard.py'}"
        hook = [{"matcher": "WebSearch|WebFetch", "hooks": [{"type": "command", "command": guard, "timeout": 30}]}]
        self.settings_path.write_text(json.dumps({"hooks": {"PreToolUse": hook, "PostToolUse": hook}}, indent=2))

    def invoke(self, spec: AgentSpec, system_prompt: str, user_prompt: str, schema: dict,
               transcript: Path, timeout: int) -> RawInvocation:
        state_file = transcript.with_suffix(".guard.json")
        state_file.write_text("{}")
        model = spec.model or self.cfg["run"].get("model")
        cmd = ["claude", "-p", "--output-format", "stream-json", "--verbose",
               "--system-prompt", system_prompt,
               "--tools", ",".join(spec.tools) if spec.tools else "",
               "--max-turns", str(spec.max_turns),
               "--max-budget-usd", str(spec.max_budget_usd),
               "--json-schema", json.dumps(schema),
               "--settings", str(self.settings_path),
               "--no-session-persistence"]
        if spec.tools:
            cmd += ["--allowedTools", ",".join(spec.tools)]
        if model:
            cmd += ["--model", model]
        env = dict(os.environ)
        env.update({"HUNTER_GUARD_STATE": str(state_file),
                    "HUNTER_MAX_SEARCHES": str(spec.max_searches),
                    "HUNTER_MAX_FETCHES": str(spec.max_fetches),
                    "HUNTER_CACHE_DB": str(self.cache_db),
                    "HUNTER_CACHE_TTL_H": str(self.cfg["run"].get("search_cache_ttl_hours", 72))})
        with transcript.open("w", encoding="utf-8") as out, open(transcript.with_suffix(".stderr.txt"), "w") as err:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=out, stderr=err, text=True,
                                    cwd=str(self.work_dir), env=env)
            try:
                proc.communicate(input=user_prompt, timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                return RawInvocation(ok=False, subtype="timeout", pid=proc.pid,
                                     guard_state=_read_json(state_file),
                                     error=f"agent exceeded timeout of {timeout}s")
        return self._parse(transcript, proc.pid, proc.returncode, _read_json(state_file))

    @staticmethod
    def _parse(transcript: Path, pid: int, returncode: int, guard: dict) -> RawInvocation:
        tool_counts: dict[str, int] = {}
        result, session_id = None, None
        for line in transcript.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "system" and ev.get("subtype") == "init":
                session_id = ev.get("session_id")
            elif ev.get("type") == "assistant":
                for c in ev.get("message", {}).get("content", []):
                    if c.get("type") == "tool_use":
                        tool_counts[c["name"]] = tool_counts.get(c["name"], 0) + 1
            elif ev.get("type") == "result":
                result = ev
        if result is None:
            stderr = transcript.with_suffix(".stderr.txt").read_text(errors="replace")[-1500:]
            return RawInvocation(ok=False, subtype="crash" if returncode else "no_output", pid=pid,
                                 tool_counts=tool_counts, guard_state=guard, session_id=session_id,
                                 error=f"no result event (exit={returncode}) {stderr}".strip())
        so = result.get("structured_output")
        if so is None and not result.get("is_error"):
            so = _extract_json(result.get("result") or "")
        ok = (not result.get("is_error")) and isinstance(so, dict)
        subtype = result.get("subtype", "unknown") if not result.get("is_error") else result.get("subtype", "error")
        if not ok and subtype == "success":
            subtype = "invalid_output"
        text = str(result.get("result") or "")
        if not ok and ("issue with the selected model" in text or "Invalid API key" in text or "not logged in" in text.lower()):
            subtype = "config_error"  # permanent: do not retry
        return RawInvocation(ok=ok, subtype=subtype, structured_output=so if isinstance(so, dict) else None,
                             cost_usd=float(result.get("total_cost_usd") or 0), turns=int(result.get("num_turns") or 0),
                             tool_counts=tool_counts, guard_state=guard, pid=pid, session_id=session_id,
                             error=None if ok else f"{subtype}: {str(result.get('result') or result.get('errors') or '')[:500]}")


class MockBackend:
    """In-process fake backend used only by the offline self-test to exercise
    orchestration logic (failures, retries, parallelism) without spending money.
    It is never used for real research and is labelled as mock in all logs."""

    def __init__(self, handlers: dict[str, Callable[[str, dict], dict]], delay: float = 0.5):
        self.handlers = handlers
        self.delay = delay
        self.calls: dict[str, int] = {}
        self._lock = threading.Lock()

    def invoke(self, spec, system_prompt, user_prompt, schema, transcript, timeout) -> RawInvocation:
        with self._lock:
            self.calls[spec.name] = self.calls.get(spec.name, 0) + 1
            n = self.calls[spec.name]
        time.sleep(self.delay)
        payload = json.loads(user_prompt.split("INPUT_JSON:\n", 1)[1]) if "INPUT_JSON:\n" in user_prompt else {}
        handler = self.handlers.get(spec.name)
        if handler is None:
            return RawInvocation(ok=False, subtype="crash", error=f"mock: no handler for {spec.name}")
        try:
            out = handler(n, payload)
        except TimeoutError as e:
            return RawInvocation(ok=False, subtype="timeout", error=str(e))
        except Exception as e:  # simulated hard failure
            return RawInvocation(ok=False, subtype="crash", error=f"mock failure: {e}")
        transcript.write_text(json.dumps({"mock": True, "output": out}, ensure_ascii=False))
        return RawInvocation(ok=True, subtype="success", structured_output=out, cost_usd=0.0, turns=1,
                             tool_counts={"WebSearch": 1}, guard_state={"searches": 1}, pid=os.getpid(),
                             session_id=f"mock-{spec.name}-{n}")


class BudgetTracker:
    def __init__(self, limit_usd: float):
        self.limit = limit_usd
        self.spent = 0.0
        self.reserved = 0.0
        self._lock = threading.Lock()

    def reserve(self, amount: float) -> bool:
        with self._lock:
            if self.spent + self.reserved + amount > self.limit:
                return False
            self.reserved += amount
            return True

    def settle(self, reserved: float, actual: float) -> None:
        with self._lock:
            self.reserved -= reserved
            self.spent += actual


class AgentRunner:
    def __init__(self, cfg: dict, store: Store, logger: RunLogger, run_id: str, run_dir: Path, backend):
        self.cfg = cfg
        self.store = store
        self.log = logger
        self.run_id = run_id
        self.run_dir = Path(run_dir)
        self.backend = backend
        self.budget = BudgetTracker(float(cfg["run"]["max_total_budget_usd"]))
        self.transcripts = self.run_dir / "transcripts"
        self.outputs = self.run_dir / "agent_outputs"
        self.transcripts.mkdir(parents=True, exist_ok=True)
        self.outputs.mkdir(parents=True, exist_ok=True)
        self._seq = 0
        self._seq_lock = threading.Lock()

    def _next(self) -> int:
        with self._seq_lock:
            self._seq += 1
            return self._seq

    def run(self, spec: AgentSpec, task: str, payload: dict, task_label: str = "") -> AgentResult:
        label = task_label or spec.name
        actor = spec.display + (f"[{task_label}]" if task_label else "")
        system_prompt = spec.system_prompt(self.cfg)
        schema = spec.schema
        today = _dt.date.today().isoformat()
        payload = {"run_id": self.run_id, "today": today, "market": self.cfg["run"]["market"],
                   "search_budget": {"max_web_searches": spec.max_searches, "max_web_fetches": spec.max_fetches},
                   **payload}
        user_prompt = f"TASK:\n{task}\n\nINPUT_JSON:\n{json.dumps(payload, ensure_ascii=False, indent=1)}"
        key_src = json.dumps([spec.name, system_prompt, schema, task, {k: v for k, v in payload.items() if k not in ("run_id", "today")},
                              spec.max_searches, spec.model or self.cfg["run"].get("model")], ensure_ascii=False, sort_keys=True)
        cache_key = hashlib.sha256(key_src.encode()).hexdigest()
        res = AgentResult(agent=spec.name, task_label=label, status="failed",
                          started_at=_dt.datetime.now().isoformat(timespec="seconds"))

        if self.cfg["run"].get("agent_cache_enabled", True):
            cached = self.store.cache_get(cache_key)
            if cached is not None:
                res.status, res.output, res.cache_hit = "ok", cached, True
                res.finished_at = res.started_at
                self.log.log(actor, "cache hit — reused previous identical agent result (no cost)", agent=spec.name)
                return self._finish(res, spec)

        reserve = spec.max_budget_usd
        if not self.budget.reserve(reserve):
            res.status, res.error = "skipped", "BUDGET_EXHAUSTED: run budget would be exceeded"
            self.log.log(actor, f"skipped — {res.error} (spent ${self.budget.spent:.2f})", level="WARN", agent=spec.name)
            return self._finish(res, spec)

        max_retries = int(self.cfg["run"].get("max_retries", 2))
        backoff = float(self.cfg["run"].get("retry_backoff_sec", 5))
        timeout = int(self.cfg["run"].get("agent_timeout_sec", 1500))
        t0 = time.time()
        self.log.log(actor, "started", agent=spec.name, stage=spec.stage)
        try:
            for attempt in range(1, max_retries + 2):
                res.attempts = attempt
                seq = self._next()
                transcript = self.transcripts / f"{seq:03d}_{spec.name}_{_safe(label)}_a{attempt}.jsonl"
                raw = self.backend.invoke(spec, system_prompt, user_prompt, schema, transcript, timeout)
                g = raw.guard_state or {}
                res.cost_usd += raw.cost_usd
                res.turns += raw.turns
                res.searches += int(g.get("searches", raw.tool_counts.get("WebSearch", 0)))
                res.fetches += int(g.get("fetches", raw.tool_counts.get("WebFetch", 0)))
                res.search_cache_hits += int(g.get("cache_hits", 0))
                res.blocked_calls += int(g.get("blocked", 0))
                res.queries += g.get("queries", [])
                res.pid, res.session_id = raw.pid, raw.session_id
                if raw.ok:
                    try:
                        jsonschema.validate(raw.structured_output, schema)
                    except jsonschema.ValidationError as e:
                        raw.ok, raw.subtype, raw.error = False, "invalid_output", f"schema validation failed: {e.message[:300]}"
                if raw.ok:
                    res.status, res.output, res.error = "ok", raw.structured_output, None
                    break
                res.error = raw.error
                transient = raw.subtype in TRANSIENT_SUBTYPES or raw.subtype.startswith("error_max_turns")
                if attempt <= max_retries and transient:
                    self.log.log(actor, f"attempt {attempt} failed ({raw.subtype}) — retrying: {str(raw.error)[:200]}",
                                 level="WARN", agent=spec.name, retry=True)
                    time.sleep(backoff * attempt)
                    continue
                self.log.log(actor, f"failed ({raw.subtype}) — not retrying: {str(raw.error)[:300]}", level="ERROR",
                             agent=spec.name)
                break
        finally:
            self.budget.settle(reserve, res.cost_usd)
        res.duration_sec = round(time.time() - t0, 1)
        res.finished_at = _dt.datetime.now().isoformat(timespec="seconds")
        if res.status == "ok":
            if self.cfg["run"].get("agent_cache_enabled", True):
                self.store.cache_put(cache_key, spec.name, res.output)
        return self._finish(res, spec)

    def _finish(self, res: AgentResult, spec: AgentSpec) -> AgentResult:
        actor = spec.display + (f"[{res.task_label}]" if res.task_label != spec.name else "")
        out_path = ""
        if res.output is not None:
            p = self.outputs / f"{spec.name}_{_safe(res.task_label)}.json"
            p.write_text(json.dumps(res.output, ensure_ascii=False, indent=2), encoding="utf-8")
            out_path = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
        if res.status == "ok" and not res.cache_hit:
            self.log.log(actor, f"completed in {res.duration_sec}s — searches={res.searches} fetches={res.fetches} "
                                f"cache_hits={res.search_cache_hits} blocked={res.blocked_calls} turns={res.turns} "
                                f"cost=${res.cost_usd:.3f} pid={res.pid}",
                         agent=spec.name, searches=res.searches, cost=res.cost_usd)
        self.store.execute(
            "INSERT INTO agent_runs (run_id, agent, stage, task_label, status, attempts, started_at, finished_at, duration_sec,"
            " cost_usd, searches, fetches, search_cache_hits, blocked_calls, turns, pid, session_id, cache_hit, error, output_path)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (self.run_id, spec.name, spec.stage, res.task_label, res.status, res.attempts, res.started_at, res.finished_at,
             res.duration_sec, res.cost_usd, res.searches, res.fetches, res.search_cache_hits, res.blocked_calls, res.turns,
             res.pid, res.session_id, int(res.cache_hit), res.error, out_path))
        return res


def _safe(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in s)[:60]


def _read_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text() or "{}")
    except Exception:
        return {}


def _extract_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None
