#!/usr/bin/env python3
"""Claude Code hook: hard per-agent search/fetch budget + shared WebSearch cache.

Registered for PreToolUse and PostToolUse on WebSearch|WebFetch via `--settings`.
Each agent process gets its own state file through environment variables:

  HUNTER_GUARD_STATE   path to this agent run's JSON counter file
  HUNTER_MAX_SEARCHES  max WebSearch calls for this agent run
  HUNTER_MAX_FETCHES   max WebFetch calls for this agent run
  HUNTER_CACHE_DB      shared SQLite search cache (all agents, all runs)
  HUNTER_CACHE_TTL_H   cache TTL in hours

Exit code 2 blocks the tool call; stderr is shown to the agent.
"""
from __future__ import annotations

import fcntl
import json
import os
import re
import sqlite3
import sys
import time


def _norm(q: str) -> str:
    return re.sub(r"\s+", " ", (q or "").strip().lower())


def _cache_conn():
    path = os.environ.get("HUNTER_CACHE_DB")
    if not path:
        return None
    conn = sqlite3.connect(path, timeout=30)
    conn.execute("CREATE TABLE IF NOT EXISTS search_cache (query TEXT PRIMARY KEY, created_at REAL, response TEXT)")
    return conn


def _update_state(fn):
    path = os.environ.get("HUNTER_GUARD_STATE")
    if not path:
        return fn({})
    with open(path, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        raw = f.read()
        state = json.loads(raw) if raw.strip() else {}
        result = fn(state)
        f.seek(0)
        f.truncate()
        f.write(json.dumps(state))
        fcntl.flock(f, fcntl.LOCK_UN)
    return result


def pre(event: dict) -> int:
    tool = event.get("tool_name")
    tin = event.get("tool_input") or {}
    max_s = int(os.environ.get("HUNTER_MAX_SEARCHES", "10"))
    max_f = int(os.environ.get("HUNTER_MAX_FETCHES", "6"))
    ttl = float(os.environ.get("HUNTER_CACHE_TTL_H", "72")) * 3600

    if tool == "WebSearch":
        q = _norm(tin.get("query", ""))
        conn = _cache_conn()
        if conn:
            row = conn.execute("SELECT created_at, response FROM search_cache WHERE query = ?", (q,)).fetchone()
            conn.close()
            if row and time.time() - row[0] < ttl:
                _update_state(lambda s: s.__setitem__("cache_hits", s.get("cache_hits", 0) + 1))
                sys.stderr.write(
                    "CACHE_HIT (not an error, no budget used): this exact query was already searched earlier "
                    "in this research system. Cached real results follow:\n" + row[1][:12000])
                return 2

        def take(s):
            if s.get("searches", 0) >= max_s:
                s["blocked"] = s.get("blocked", 0) + 1
                return False
            s["searches"] = s.get("searches", 0) + 1
            s.setdefault("queries", []).append(tin.get("query", ""))
            return True
        if not _update_state(take):
            sys.stderr.write(f"SEARCH BUDGET EXHAUSTED ({max_s}/{max_s} searches used). Do not search again. "
                             "Finish now and return your structured output with the evidence you already have.")
            return 2
        return 0

    if tool == "WebFetch":
        def take(s):
            if s.get("fetches", 0) >= max_f:
                s["blocked"] = s.get("blocked", 0) + 1
                return False
            s["fetches"] = s.get("fetches", 0) + 1
            s.setdefault("urls", []).append(tin.get("url", ""))
            return True
        if not _update_state(take):
            sys.stderr.write(f"FETCH BUDGET EXHAUSTED ({max_f}/{max_f} fetches used). Do not fetch again. "
                             "Finish with the evidence you already have.")
            return 2
    return 0


def post(event: dict) -> int:
    if event.get("tool_name") != "WebSearch":
        return 0
    q = _norm((event.get("tool_input") or {}).get("query", ""))
    resp = event.get("tool_response")
    if not q or not resp:
        return 0
    text = resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False)
    if len(text) < 50:
        return 0
    conn = _cache_conn()
    if conn:
        conn.execute("INSERT OR REPLACE INTO search_cache VALUES (?,?,?)", (q, time.time(), text[:20000]))
        conn.commit()
        conn.close()
    return 0


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0  # never break the agent because of a malformed hook payload
    try:
        if event.get("hook_event_name") == "PostToolUse":
            return post(event)
        return pre(event)
    except Exception as e:  # guard failures must not kill the agent
        sys.stderr.write(f"search_guard internal error: {e}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
