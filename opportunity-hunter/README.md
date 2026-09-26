# Opportunity Hunter — Real Multi-Agent Research System (Saudi Arabia 🇸🇦)

A runnable multi-agent system that hunts **pains → evidence → business opportunities** for a solo technical founder
in Saudi Arabia, using global research to find adaptable models.

> **What "real multi-agent" means here:** every agent is a **separate OS process** — a headless Claude Code
> instance (`claude -p`) with its own system prompt, its own input, its own JSON schema, its own tool whitelist
> (only `WebSearch` + `WebFetch`, or no tools at all), its own turn limit and USD cap, and its own PID/session id.
> Agents share nothing except what the orchestrator explicitly passes to them. Independent agents run
> **concurrently** (thread pool of subprocesses). Every run is logged with PID, session id, timing, searches and cost.

## Architecture

```text
                          ┌──────────────────────────────┐
                          │ ORCHESTRATOR (hunter/)        │  Python control plane: stages, parallelism,
                          │ orchestrator.py + runner.py   │  budgets, retries, cache, dedup, gap routing
                          └──────────────┬───────────────┘
      ┌──────────────────────────────────┼─────────────────────────────────────┐
      ▼ 13 DISCOVERY AGENTS (parallel)   ▼                                     ▼
 problem · b2b · b2c · complaint · whatsapp/excel · jobs · foreign-model · competition-gap · integration-gap
 · ai-opportunity · market-change · future · individual
                                          │  raw signals (JSON schema: schemas/discovery.json)
                                          ▼
                      DEDUP: code (near-duplicate merge) + CONSOLIDATOR agent (semantic merge + ranking)
                                          │  top-N candidates (+ backlog)
                                          ▼
          VALIDATORS (parallel, batched): EVIDENCE · PAYMENT · COMPETITION · FEASIBILITY
                                          │
                                          ▼
                                    KILLER AGENT  ── NEEDS_MORE_EVIDENCE / payment gaps ──┐
                                          │                                              ▼
                                          │                         GAP DETECTOR → GAP_RESEARCHER (re-research)
                                          │                                              │
                                          ◄───────────── KILLER final round ◄────────────┘
                                          ▼
                              OPPORTUNITY SYNTHESIZER agent
                                          ▼
                  reports/final_report.md  +  database/opportunities.db  +  results/<run_id>/
```

## Project layout

| Path | Contents |
|---|---|
| `agents/<name>/agent.toml` + `prompt.md` | Discovery agents, consolidator, gap researcher, synthesizer (definition + limits + instructions) |
| `validators/<name>/` | Evidence, payment, competition, feasibility validators + Killer agent |
| `agents/orchestrator/README.md` | Why the orchestrator is code, and what it does |
| `prompts/base_rules.md` | Shared rules for every agent (evidence classes, ethics, no fabrication) |
| `schemas/*.json` | JSON Schemas every agent output must satisfy (enforced by `--json-schema` + `jsonschema` re-validation) |
| `hunter/runner.py` | Launches agent processes; retries, budget, cache, transcripts |
| `hunter/search_guard.py` | Claude Code hook: **hard** per-agent search/fetch caps + shared WebSearch cache |
| `hunter/orchestrator.py` | Pipeline stages |
| `hunter/dedup.py` | Deterministic dedup + fallback ranking |
| `hunter/report.py` | Final report renderer (incl. URL integrity check + execution log) |
| `hunter/selftest.py` | Offline (mock) and live self-tests |
| `config.toml` | Budgets, parallelism, retries, limits |
| `results/<run_id>/` | Every agent's JSON output, stage outputs, full agent transcripts (`transcripts/*.jsonl`) |
| `logs/<run_id>/run.log` | Human-readable timeline; `events.jsonl` structured events |
| `database/opportunities.db` | SQLite: runs, agent_runs, signals, candidates, validations, verdicts, research, sources |
| `research/` | Additional (gap) research outputs |
| `reports/final_report.md` | Final report |

## Running

Requirements: Python 3.11+, Claude Code CLI (`claude`) authenticated, `pip install -r requirements.txt`.

```bash
python -m hunter selftest          # offline orchestration test (mock backend, free)
python -m hunter selftest --live   # small real run (~$1–5): real agents, real searches, Killer must reject a bad idea
python -m hunter run               # full research run (all 13 discovery agents)
python -m hunter run --budget 30 --parallel 4 --agents problem_hunter,b2b_hunter --candidates 10
```

## Cost control (enforced in code)

| Control | Where |
|---|---|
| Max searches / fetches per agent (hard block) | `search_guard.py` hook, limits in each `agent.toml` |
| Max turns and max USD per agent process | `--max-turns`, `--max-budget-usd` |
| Max total run budget | `BudgetTracker` reserves each agent's cap before launch; refuses when exceeded |
| Max parallel agents | `max_parallel_agents` |
| Max retries (transient failures only) | `max_retries` |
| Search cache (shared across agents & runs) | identical queries served from `database/search_cache.db` |
| Agent result cache | identical agent calls reused from `agent_cache` table |
| Deduplication | `dedup.py` before the consolidator; consolidator merges semantically |

## Failure handling

- An agent that crashes, times out, or returns invalid JSON is retried (transient) or marked failed (permanent);
  the pipeline continues. The consolidator and synthesizer have deterministic fallbacks.
- A failed validator marks the candidate's dossier as incomplete; the gap detector routes it to re-research.
- All failures are listed in the report's **Research Limitations** section.

## Honesty guarantees

- Agents may only cite URLs they saw in their session; evidence is classified DIRECT / STRONG_INDIRECT / WEAK /
  HYPOTHESIS; missing evidence must be written as `NO RELIABLE EVIDENCE FOUND`.
- The report's URL integrity check lists any URL in the synthesis that no research agent collected in that run.
- Public information only. No CAPTCHA/login/paywall bypassing, no personal data, no contacting anyone.

## Known limitations

See section 9 of the final report. Main ones: the built-in WebSearch is not a Saudi-localized Google; social
platforms (X/TikTok/LinkedIn) are mostly login-gated; LLM judgements are not a substitute for customer interviews.

## Latest run (2026-09-26)

- Final report: [`reports/final_report.md`](reports/final_report.md) (pass 1 before gap research: `reports/final_report_pass1.md`)
- Run `full_20260926` (discovery → Killer round 1) + `full_20260926_pass2` (resumed: gap research → Killer final → synthesis)
  via `python -m hunter run --resume-from full_20260926 --run-id full_20260926_pass2`
- 41 real agent processes, 21 agent types, 0 failures · 401 web searches · 113 page fetches · $25.83 total
- 101 raw signals → 20 validated candidates (+37 backlog) → Killer: 3 survived, 17 rejected
- Self-tests: `logs/selftest_offline_*/selftest_result.txt` (15/15), `logs/selftest_live_*/selftest_result.txt` (11/11)
