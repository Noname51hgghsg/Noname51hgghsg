"""SQLite storage for runs, agent executions, signals, candidates, validations, verdicts."""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY, started_at TEXT, finished_at TEXT, mode TEXT,
  status TEXT, config_json TEXT, summary_json TEXT);
CREATE TABLE IF NOT EXISTS agent_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, agent TEXT, stage TEXT, task_label TEXT,
  status TEXT, attempts INTEGER, started_at TEXT, finished_at TEXT, duration_sec REAL,
  cost_usd REAL, searches INTEGER, fetches INTEGER, search_cache_hits INTEGER, blocked_calls INTEGER,
  turns INTEGER, pid INTEGER, session_id TEXT, cache_hit INTEGER, error TEXT, output_path TEXT);
CREATE TABLE IF NOT EXISTS signals (
  run_id TEXT, signal_id TEXT, agent TEXT, json TEXT, PRIMARY KEY (run_id, signal_id));
CREATE TABLE IF NOT EXISTS candidates (
  run_id TEXT, candidate_id TEXT, title TEXT, status TEXT, json TEXT, PRIMARY KEY (run_id, candidate_id));
CREATE TABLE IF NOT EXISTS validations (
  run_id TEXT, candidate_id TEXT, validator TEXT, json TEXT,
  PRIMARY KEY (run_id, candidate_id, validator));
CREATE TABLE IF NOT EXISTS verdicts (
  run_id TEXT, candidate_id TEXT, round INTEGER, verdict TEXT, json TEXT,
  PRIMARY KEY (run_id, candidate_id, round));
CREATE TABLE IF NOT EXISTS research (
  run_id TEXT, candidate_id TEXT, round INTEGER, json TEXT,
  PRIMARY KEY (run_id, candidate_id, round));
CREATE TABLE IF NOT EXISTS sources (
  url TEXT PRIMARY KEY, title TEXT, first_run TEXT, first_agent TEXT, seen_count INTEGER);
CREATE TABLE IF NOT EXISTS agent_cache (
  cache_key TEXT PRIMARY KEY, agent TEXT, created_at REAL, json TEXT);
"""


class Store:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self.conn = sqlite3.connect(str(self.path), check_same_thread=False, timeout=30)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def execute(self, sql: str, params: tuple = ()) -> None:
        with self._lock:
            self.conn.execute(sql, params)
            self.conn.commit()

    def query(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._lock:
            cur = self.conn.execute(sql, params)
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    # --- helpers -----------------------------------------------------------
    def put_json(self, table: str, keys: dict, payload, extra: dict | None = None) -> None:
        cols = dict(keys)
        cols.update(extra or {})
        cols["json"] = json.dumps(payload, ensure_ascii=False)
        names = ",".join(cols)
        marks = ",".join("?" for _ in cols)
        self.execute(f"INSERT OR REPLACE INTO {table} ({names}) VALUES ({marks})", tuple(cols.values()))

    def add_source(self, url: str, title: str, run_id: str, agent: str) -> None:
        if not url or not url.startswith("http"):
            return
        with self._lock:
            cur = self.conn.execute("UPDATE sources SET seen_count = seen_count + 1 WHERE url = ?", (url,))
            if cur.rowcount == 0:
                self.conn.execute("INSERT INTO sources VALUES (?,?,?,?,1)", (url, title or "", run_id, agent))
            self.conn.commit()

    def cache_get(self, key: str, ttl_sec: float | None = None):
        rows = self.query("SELECT json, created_at FROM agent_cache WHERE cache_key = ?", (key,))
        if not rows:
            return None
        if ttl_sec and time.time() - rows[0]["created_at"] > ttl_sec:
            return None
        return json.loads(rows[0]["json"])

    def cache_put(self, key: str, agent: str, payload) -> None:
        self.execute("INSERT OR REPLACE INTO agent_cache VALUES (?,?,?,?)",
                     (key, agent, time.time(), json.dumps(payload, ensure_ascii=False)))
