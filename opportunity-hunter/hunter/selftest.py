"""Self-tests.

offline (`python -m hunter selftest`): exercises the orchestration logic with a MockBackend (no API cost):
  failure isolation, retries, schema validation, parallelism, validator hand-off, killer rejection,
  gap-research loop, synthesis, report and logs.

live (`python -m hunter selftest --live`): a small REAL run — real `claude -p` agent processes with real web
search — including a deliberately bad injected opportunity (Killer must reject it) and a deliberately broken
agent (system must continue).
"""
from __future__ import annotations

import copy
import datetime as _dt
import json
import time
from pathlib import Path

from .config import ROOT, load_config
from .orchestrator import DISCOVERY_ORDER, Orchestrator
from .registry import load_registry
from .runner import MockBackend


# ----------------------------------------------------------------------------- mock handlers
def _signal(agent: str, i: int, problem: str) -> dict:
    return {"opportunity_id": f"{agent[:3].upper()}-{i:02d}", "problem": problem, "customer": "Saudi SMB owners",
            "segment": "B2B", "sector": "services", "market": "Saudi Arabia", "source": "mock",
            "evidence": [{"claim": problem, "url": f"https://example.org/{agent}/{i}", "source_title": "mock source",
                          "summary": "mock", "evidence_type": "DIRECT", "published": "2026"}],
            "existing_solution": [], "workaround": "Excel", "potential_solution": "SaaS", "business_model": "subscription",
            "opportunity_type": "NEW_OPPORTUNITY", "time_horizon": "CURRENT_EVIDENCE", "frequency": "HIGH",
            "severity": "MEDIUM", "existing_spend": "NO RELIABLE EVIDENCE FOUND", "confidence": "MEDIUM", "unknowns": []}


def _discovery(agent):
    def h(n, payload):
        if agent == "gap_hunter":
            raise RuntimeError("simulated permanent crash")          # → retried, then isolated
        if agent == "b2c_hunter" and n == 1:
            raise TimeoutError("simulated transient timeout")         # → retry succeeds
        if agent == "complaint_hunter" and n == 1:
            return {"agent": agent, "signals": "not-a-list"}         # → schema invalid → retry
        problems = {"problem_hunter": ["Clinics lose revenue to appointment no-shows", "KILLME paid prayer-times app"],
                    "b2b_hunter": ["Clinics lose revenue to appointment no-shows!", "Contractors track progress payments in Excel"]}
        ps = problems.get(agent, [f"{agent} pain about manual reporting"])
        return {"agent": agent, "signals": [_signal(agent, i, p) for i, p in enumerate(ps, 1)],
                "queries_used": ["mock query"], "limitations": []}
    return h


def _consolidator(n, payload):
    sigs = payload["signals"]
    return {"candidates": [{"candidate_id": f"C{i:02d}", "title": s["problem"][:60], "problem": s["problem"],
                            "customer": s["customer"], "segment": "B2B", "sector": "services",
                            "opportunity_type": "NEW_OPPORTUNITY", "time_horizon": "CURRENT_EVIDENCE",
                            "member_signal_ids": [s["id"]], "potential_solution": "SaaS", "business_model": "subscription",
                            "priority": 5, "priority_rationale": "mock", "open_questions": []}
                           for i, s in enumerate(sigs[:payload["candidate_limit"]], 1)],
            "backlog": [], "discarded": [], "merge_notes": "mock"}


RECEIVED: dict[str, list] = {}


def _validator(kind):
    def h(n, payload):
        RECEIVED.setdefault(kind, []).extend(c["candidate_id"] for c in payload["candidates"])
        res = []
        for c in payload["candidates"]:
            base = {"candidate_id": c["candidate_id"], "summary": "mock"}
            if kind == "evidence_validator":
                base.update(claims=[], problem_evidence_level="DIRECT", market_model_evidence_level="WEAK",
                            demand_signals=[], new_sources=[])
            elif kind == "payment_validator":
                base.update(someone_pays_now="UNCLEAR" if "Contractors" in c["title"] else "YES",
                            payment_evidence=[], labor_cost_signals=[], willingness_to_pay_assessment="mock")
            elif kind == "competition_validator":
                base.update(competitors=[], market_state="WEAK_MARKET", gap_description="mock", differentiation_angle="mock")
            else:
                base.update(stack={k: "x" for k in ["frontend", "backend", "database", "authentication", "ai", "apis",
                                                    "hosting", "payments", "integrations"]},
                            mvp_scope=["x"], mvp_cost_sar_low=300, mvp_cost_sar_high=900, monthly_run_cost_sar="100",
                            build_time_weeks="3", complexity="EASY", solo_founder_feasible=True, regulatory=[],
                            data_dependencies=[], blockers=[])
            res.append(base)
        return {"results": res, "queries_used": [], "limitations": []}
    return h


def _killer(n, payload):
    RECEIVED.setdefault("killer_agent", []).append({"final": payload["final_round"],
                                                    "ids": [c["candidate_id"] for c in payload["candidates"]],
                                                    "has_validation": all("validation" in c for c in payload["candidates"])})
    res = []
    for c in payload["candidates"]:
        if "KILLME" in c["title"]:
            v = "REJECTED"
        elif "no-shows" in c["title"] and not payload["final_round"]:
            v = "NEEDS_MORE_EVIDENCE"
        else:
            v = "SURVIVED"
        res.append({"candidate_id": c["candidate_id"], "verdict": v,
                    "kill_reasons": [{"category": "STRONG_COMPETITOR", "reason": "free incumbents dominate", "severity": "FATAL",
                                      "evidence": [{"url": "https://example.org/free", "summary": "free app"}]}] if v == "REJECTED" else [],
                    "attacks_attempted": ["competition"], "remaining_uncertainties": [],
                    "missing_info_requests": [{"question": "Do clinics pay for reminder tools?", "route_to": "payment"}]
                    if v == "NEEDS_MORE_EVIDENCE" else [], "survival_notes": "", "summary": "mock"})
    return {"results": res, "queries_used": [], "limitations": []}


def _gap_researcher(n, payload):
    RECEIVED.setdefault("gap_researcher", []).extend(r["candidate_id"] for r in payload["requests"])
    return {"results": [{"candidate_id": r["candidate_id"], "answers": [
        {"question": q["question"], "finding": "FOUND", "answer": "mock", "sources": [{"url": "https://example.org/p", "title": "p"}]}
        for q in r["questions"]]} for r in payload["requests"]], "queries_used": [], "limitations": []}


def _synth(n, payload):
    RECEIVED["synth_survivors"] = [s["candidate_id"] for s in payload["survivors"]]
    return {"executive_summary": "mock", "golden_opportunities": [
        {"candidate_id": s["candidate_id"], "name": s["title"], "category": "NEW_OPPORTUNITY", "problem": s["problem"],
         "customer": "x", "evidence": [], "why_it_exists": "x", "existing_alternatives": "x", "competitors": [],
         "saudi_opportunity": "x", "solution": "x", "mvp": "x", "technology": "x", "estimated_cost": "x",
         "complexity": "EASY", "revenue_model": "x", "first_customer_strategy": "x", "expansion": "x", "risks": [],
         "unknowns": [], "evidence_quality": "MEDIUM", "sources": ["https://invented.example.com/not-collected"]}
        for s in payload["survivors"]],
        "hidden_gems": [], "foreign_models": [], "boring_businesses": [], "future_opportunities": [],
        "no_opportunity_statement": ""}


def run_offline() -> bool:
    RECEIVED.clear()
    cfg = load_config(overrides={"run": {"max_parallel_agents": 6, "retry_backoff_sec": 0.2, "agent_cache_enabled": False,
                                         "candidate_limit": 10, "validation_batch_size": 3}})
    handlers = {a: _discovery(a) for a in DISCOVERY_ORDER}
    handlers.update({"consolidator": _consolidator, "killer_agent": _killer, "gap_researcher": _gap_researcher,
                     "synthesizer": _synth})
    handlers.update({v: _validator(v) for v in ["evidence_validator", "payment_validator", "competition_validator",
                                                "feasibility_validator"]})
    backend = MockBackend(handlers, delay=1.0)
    run_id = f"selftest_offline_{_dt.datetime.now():%Y%m%d_%H%M%S}"
    db = ROOT / "results" / run_id / "selftest.db"
    orch = Orchestrator(cfg, run_id=run_id, mode="selftest_offline", backend=backend, db_path=db,
                        report_path=ROOT / "reports" / "selftest_offline_report.md")
    t0 = time.time()
    summary = orch.run()
    elapsed = time.time() - t0
    events = orch.log.events()
    rows = orch.store.query("SELECT * FROM agent_runs WHERE run_id=?", (run_id,))
    disc = [r for r in rows if r["stage"] == "discovery"]

    def overlap(rs):
        iv = [(r["started_at"], r["finished_at"]) for r in rs]
        return any(a[0] < b[1] and b[0] < a[1] for i, a in enumerate(iv) for b in iv[i + 1:])

    report = orch.report_path.read_text(encoding="utf-8")
    checks = {
        "1_orchestrator_runs_end_to_end": summary["status"] == "completed",
        "2_agent_can_be_run": any(r["status"] == "ok" for r in rows),
        "3_agent_returns_valid_json(schema-invalid output rejected then retried)":
            any(r["agent"] == "complaint_hunter" and r["status"] == "ok" and r["attempts"] == 2 for r in rows),
        "4_results_reach_orchestrator": summary["counts"]["raw_signals"] > 0,
        "5_parallel_execution": overlap(disc) and elapsed < 13 * 1.0 * 0.8 + 30,
        "6_validators_receive_results": all(len(RECEIVED.get(v, [])) == summary["counts"]["candidates_validated"]
                                            for v in ["evidence_validator", "payment_validator", "competition_validator", "feasibility_validator"]),
        "7a_killer_receives_validation": all(k["has_validation"] for k in RECEIVED.get("killer_agent", [])),
        "7b_killer_can_reject": summary["counts"]["rejected_by_killer"] >= 1,
        "7c_gap_research_loop(NEEDS_MORE_EVIDENCE→research→final killer)":
            bool(RECEIVED.get("gap_researcher")) and any(k["final"] for k in RECEIVED.get("killer_agent", [])),
        "8_synthesizer_builds_report": "الفرص الذهبية" in report and "Rejected by Killer" in report,
        "8b_url_integrity_check_flags_invented_urls": "invented.example.com" in report,
        "9_logs_work": any("started" in e["message"] for e in events) and any("completed" in e["message"] for e in events),
        "10a_failure_isolated(gap_hunter crashed, run continued)":
            any(r["agent"] == "gap_hunter" and r["status"] == "failed" for r in rows) and summary["status"] == "completed",
        "10b_transient_failure_retried(b2c_hunter)": any(r["agent"] == "b2c_hunter" and r["status"] == "ok" and r["attempts"] == 2 for r in rows),
        "10c_rejected_not_sent_to_synthesizer": all("KILLME" not in orch.store.query(
            "SELECT title FROM candidates WHERE run_id=? AND candidate_id=?", (run_id, c))[0]["title"]
            for c in RECEIVED.get("synth_survivors", [])),
    }
    return _print_checks("OFFLINE SELF-TEST (mock backend, no API cost)", checks, orch, elapsed)


def run_live() -> bool:
    cfg = load_config(overrides={"run": {"max_parallel_agents": 4, "max_total_budget_usd": 8.0, "candidate_limit": 2,
                                         "validation_batch_size": 3, "max_retries": 1, "agent_cache_enabled": False,
                                         "agent_timeout_sec": 900}})
    specs = load_registry(cfg)
    for s in specs.values():            # small budgets for the live test
        if s.max_searches:
            s.max_searches, s.max_fetches = 3, 1
        s.max_budget_usd = min(s.max_budget_usd, 1.5)
    broken = copy.deepcopy(specs["problem_hunter"])
    broken.name, broken.display, broken.model = "broken_test_agent", "BROKEN_TEST_AGENT", "nonexistent-model-xyz"
    extra = dict(specs)
    extra["broken_test_agent"] = broken
    bad = {"candidate_id": "TEST_BAD", "title": "Paid subscription app showing prayer times in Saudi Arabia (20 SAR/month)",
           "problem": "People in Saudi Arabia need to know prayer times.", "customer": "Muslim individuals in Saudi Arabia",
           "segment": "B2C", "sector": "religious apps", "opportunity_type": "NEW_OPPORTUNITY", "time_horizon": "CURRENT_EVIDENCE",
           "potential_solution": "A mobile app that shows prayer times, 20 SAR/month subscription",
           "business_model": "consumer subscription 20 SAR/month", "evidence": [], "open_questions": [],
           "unknowns": ["Would anyone pay when free apps exist?"], "source_agents": ["selftest_injection"]}
    run_id = f"selftest_live_{_dt.datetime.now():%Y%m%d_%H%M%S}"
    orch = Orchestrator(cfg, run_id=run_id, mode="selftest_live", discovery_agents=["problem_hunter", "b2b_hunter", "broken_test_agent"],
                        inject_candidates=[bad], extra_specs=extra, report_path=ROOT / "reports" / "selftest_live_report.md")
    t0 = time.time()
    summary = orch.run()
    elapsed = time.time() - t0
    rows = orch.store.query("SELECT * FROM agent_runs WHERE run_id=?", (run_id,))
    disc = [r for r in rows if r["stage"] == "discovery" and r["status"] == "ok"]
    iv = [(r["started_at"], r["finished_at"]) for r in disc]
    overlap = any(a[0] < b[1] and b[0] < a[1] for i, a in enumerate(iv) for b in iv[i + 1:])
    verdict_bad = orch.store.query("SELECT verdict FROM verdicts WHERE run_id=? AND candidate_id='TEST_BAD' ORDER BY round DESC", (run_id,))
    report = orch.report_path.read_text(encoding="utf-8")
    events = orch.log.events()
    checks = {
        "1_orchestrator_runs_end_to_end": summary["status"] == "completed",
        "2_real_agent_processes_ran(distinct PIDs)": len({r["pid"] for r in rows if r["pid"]}) >= 5,
        "3_agents_return_schema_valid_json": all(r["status"] == "ok" for r in rows if r["agent"] != "broken_test_agent"),
        "4_results_reach_orchestrator": summary["counts"]["raw_signals"] > 0,
        "5_parallel_execution(overlapping discovery agents)": overlap,
        "5b_real_web_searches_performed": summary["counts"]["web_searches"] > 0,
        "6_validators_ran": sum(1 for r in rows if r["stage"] == "validation" and r["status"] == "ok") >= 4,
        "7_killer_rejects_bad_opportunity(TEST_BAD)": bool(verdict_bad) and verdict_bad[0]["verdict"] == "REJECTED",
        "8_synthesizer_report_built": orch.report_path.exists() and "Rejected by Killer" in report,
        "9_logs_work": any("completed" in e["message"] for e in events),
        "10_broken_agent_failed_without_stopping_system":
            any(r["agent"] == "broken_test_agent" and r["status"] == "failed" for r in rows) and summary["status"] == "completed",
    }
    return _print_checks("LIVE SELF-TEST (real claude -p agents + real web search)", checks, orch, elapsed)


def _print_checks(title: str, checks: dict, orch, elapsed: float) -> bool:
    ok = all(checks.values())
    lines = [f"\n{'=' * 70}", title, f"run_id={orch.run_id}  elapsed={elapsed:.1f}s", "=" * 70]
    lines += [f"  [{'PASS' if v else 'FAIL'}] {k}" for k, v in checks.items()]
    lines.append(f"RESULT: {'ALL PASSED' if ok else 'FAILURES PRESENT'}")
    text = "\n".join(lines)
    print(text)
    (ROOT / "logs" / orch.run_id / "selftest_result.txt").write_text(text + "\n", encoding="utf-8")
    (ROOT / "logs" / orch.run_id / "selftest_result.json").write_text(json.dumps(checks, indent=1, ensure_ascii=False))
    return ok
