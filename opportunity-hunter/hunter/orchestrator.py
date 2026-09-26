"""ORCHESTRATOR — master control plane.

Pipeline:
  Discovery (parallel) → Deduplication (code + CONSOLIDATOR agent) → Evidence / Payment / Competition /
  Feasibility validation (parallel) → KILLER → Gap detection → GAP_RESEARCHER (additional research) →
  KILLER final round → OPPORTUNITY_SYNTHESIZER → final report.

Every agent is a separate `claude -p` process (see runner.py). This module only coordinates.
"""
from __future__ import annotations

import datetime as _dt
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import dedup, report
from .config import ROOT
from .db import Store
from .log import RunLogger
from .registry import AgentSpec, load_registry
from .runner import AgentResult, AgentRunner, ClaudeCLIBackend

DISCOVERY_ORDER = ["problem_hunter", "b2b_hunter", "b2c_hunter", "complaint_hunter", "whatsapp_excel_hunter",
                   "jobs_signal_hunter", "foreign_model_hunter", "competition_hunter", "gap_hunter",
                   "ai_opportunity_hunter", "market_change_hunter", "future_opportunity_hunter",
                   "individual_problem_hunter"]
VALIDATORS = ["evidence_validator", "payment_validator", "competition_validator", "feasibility_validator"]


class Orchestrator:
    def __init__(self, cfg: dict, *, run_id: str | None = None, mode: str = "full", backend=None,
                 discovery_agents: list[str] | None = None, inject_candidates: list[dict] | None = None,
                 extra_specs: dict[str, AgentSpec] | None = None, db_path: Path | None = None,
                 report_path: Path | None = None, echo: bool = True, resume_from: str | None = None):
        self.cfg = cfg
        self.mode = mode
        self.run_id = run_id or f"{mode}_{_dt.datetime.now():%Y%m%d_%H%M%S}"
        self.run_dir = ROOT / "results" / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.log = RunLogger(ROOT / "logs" / self.run_id, echo=echo)
        self.store = Store(db_path or ROOT / "database" / "opportunities.db")
        self.specs = load_registry(cfg)
        if extra_specs:
            self.specs.update(extra_specs)
        self.backend = backend or ClaudeCLIBackend(cfg, self.run_dir / "_work", ROOT / "database" / "search_cache.db")
        self.runner = AgentRunner(cfg, self.store, self.log, self.run_id, self.run_dir, self.backend)
        self.discovery_agents = discovery_agents or DISCOVERY_ORDER
        self.inject_candidates = inject_candidates or []
        self.report_path = report_path or ROOT / "reports" / "final_report.md"
        self.max_parallel = int(cfg["run"]["max_parallel_agents"])
        self.resume_from = resume_from
        self.run_ids = [self.run_id] + ([resume_from] if resume_from else [])
        self.state: dict = {"stage_times": {}, "failures": [], "limitations": [], "retries": 0}

    # ------------------------------------------------------------------ utils
    def _parallel(self, jobs: list[tuple[str, str, dict, str]]) -> list[AgentResult]:
        """jobs: (agent_name, task, payload, label). Runs up to max_parallel agent processes at once."""
        def one(job):
            name, task, payload, label = job
            spec = self.specs.get(name)
            if spec is None:
                self.log.log("ORCHESTRATOR", f"agent '{name}' not registered — skipped", level="ERROR")
                return AgentResult(agent=name, task_label=label, status="skipped", error="not registered")
            try:
                return self.runner.run(spec, task, payload, label)
            except Exception as e:  # isolate any unexpected crash inside a worker
                self.log.log(spec.display, f"crashed unexpectedly: {e!r}", level="ERROR")
                return AgentResult(agent=name, task_label=label, status="failed", error=repr(e))
        with ThreadPoolExecutor(max_workers=self.max_parallel) as pool:
            results = list(pool.map(one, jobs))
        for r in results:
            if r.status != "ok":
                self.state["failures"].append({"agent": r.agent, "label": r.task_label, "status": r.status, "error": r.error})
        return results

    def _save(self, name: str, data) -> None:
        (self.run_dir / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _stage(self, name: str):
        orch = self

        class _S:
            def __enter__(self):
                self.t = time.time()
                orch.log.log("ORCHESTRATOR", f"=== STAGE {name} started ===", stage=name)

            def __exit__(self, *exc):
                dt = round(time.time() - self.t, 1)
                orch.state["stage_times"][name] = dt
                orch.log.log("ORCHESTRATOR", f"=== STAGE {name} finished in {dt}s ===", stage=name)
        return _S()

    @staticmethod
    def _batches(items: list, size: int) -> list[list]:
        return [items[i:i + size] for i in range(0, len(items), size)]

    # --------------------------------------------------------------- pipeline
    def run(self) -> dict:
        t0 = time.time()
        self.store.execute("INSERT OR REPLACE INTO runs (run_id, started_at, mode, status, config_json) VALUES (?,?,?,?,?)",
                           (self.run_id, _dt.datetime.now().isoformat(timespec="seconds"), self.mode, "running",
                            json.dumps(self.cfg, ensure_ascii=False)))
        self.log.log("ORCHESTRATOR", f"run {self.run_id} started (mode={self.mode}, max_parallel={self.max_parallel}, "
                                     f"budget=${self.cfg['run']['max_total_budget_usd']})")
        status = "completed"
        try:
            if self.resume_from:
                signals, candidates, backlog, discarded, validations, verdicts = self.load_previous(self.resume_from)
            else:
                with self._stage("1_DISCOVERY"):
                    signals = self.discovery()
                with self._stage("2_DEDUPLICATION"):
                    candidates, backlog, discarded = self.deduplicate(signals)
                with self._stage("3_VALIDATION"):
                    validations = self.validate(candidates)
                with self._stage("4_KILLER_ROUND_1"):
                    verdicts = self.kill(candidates, validations, research={}, round_no=1, final=False)
            research: dict = {}
            for rnd in range(1, int(self.cfg["run"].get("max_gap_research_rounds", 1)) + 1):
                with self._stage(f"5_GAP_DETECTION_R{rnd}"):
                    requests = self.detect_gaps(candidates, validations, verdicts)
                if not requests:
                    self.log.log("ORCHESTRATOR", "no evidence gaps detected — skipping additional research")
                    break
                with self._stage(f"6_ADDITIONAL_RESEARCH_R{rnd}"):
                    research = self.gap_research(requests, rnd, research)
                with self._stage(f"7_KILLER_FINAL_R{rnd}"):
                    recheck = [c for c in candidates if c["candidate_id"] in requests]
                    verdicts.update(self.kill(recheck, validations, research, round_no=rnd + 1, final=True))
            # anything still NEEDS_MORE_EVIDENCE after the loop is undecided
            for cid, v in verdicts.items():
                if v.get("verdict") == "NEEDS_MORE_EVIDENCE":
                    v["verdict"] = "UNDECIDED"
            with self._stage("8_SYNTHESIS"):
                synthesis = self.synthesize(candidates, validations, verdicts, research, backlog, signals)
        except Exception as e:
            status = "failed"
            self.log.log("ORCHESTRATOR", f"pipeline aborted: {e!r}", level="ERROR")
            raise
        finally:
            summary = self.summary(time.time() - t0, status)
            self.store.execute("UPDATE runs SET finished_at=?, status=?, summary_json=? WHERE run_id=?",
                               (_dt.datetime.now().isoformat(timespec="seconds"), status,
                                json.dumps(summary, ensure_ascii=False), self.run_id))
        with self._stage("9_REPORT"):
            report.render(self, candidates, validations, verdicts, research, backlog, discarded, signals, synthesis, summary)
        self._save("run_summary", summary)
        self.log.log("ORCHESTRATOR", f"run finished: {json.dumps(summary['counts'], ensure_ascii=False)}")
        return summary

    # -- resume
    def load_previous(self, src: str):
        """Continue from a finished run's saved stage outputs (discovery → killer round 1), so later stages can
        be re-run without paying for earlier agents again. The source run's agent executions are included in
        this run's statistics and execution log."""
        d = ROOT / "results" / src
        load = lambda n: json.loads((d / f"{n}.json").read_text(encoding="utf-8"))
        signals = load("01_raw_signals")
        cons = load("02_candidates")
        validations = load("03_validations")
        verdicts = load("04_verdicts_round1")
        candidates = cons["candidates"]
        for c in candidates:
            self.store.put_json("candidates", {"run_id": self.run_id, "candidate_id": c["candidate_id"]}, c,
                                {"title": c.get("title", ""), "status": verdicts.get(c["candidate_id"], {}).get("verdict", "CANDIDATE")})
        prev = self.store.query("SELECT summary_json FROM runs WHERE run_id=?", (src,))
        pc = json.loads(prev[0]["summary_json"])["counts"] if prev and prev[0]["summary_json"] else {}
        self.state.update(raw_signals=len(signals), after_exact_dedup=pc.get("after_exact_dedup", len(signals)),
                          candidates=len(candidates), backlog=len(cons.get("backlog", [])), discarded=len(cons.get("discarded", [])))
        self.log.log("ORCHESTRATOR", f"resumed from {src}: {len(signals)} signals, {len(candidates)} candidates, "
                                     f"{sum(1 for v in verdicts.values() if v.get('verdict') == 'SURVIVED')} survivors of Killer round 1")
        for n in ("01_raw_signals", "02_candidates", "03_validations", "04_verdicts_round1"):
            self._save(n, load(n))
        return signals, candidates, cons.get("backlog", []), cons.get("discarded", []), validations, verdicts

    # -- stage 1
    def discovery(self) -> list[dict]:
        task = ("Run your discovery mission now for the market in INPUT_JSON. Use your search budget wisely, "
                "then return your signals through the structured output.")
        jobs = [(a, task, {"agent_name": a}, a) for a in self.discovery_agents]
        results = self._parallel(jobs)
        signals: list[dict] = []
        n = 0
        for r in results:
            if r.status != "ok":
                continue
            found = r.output.get("signals", [])
            self.log.log(self.specs[r.agent].display, f"returned {len(found)} signals "
                         f"({len(r.output.get('queries_used', []))} queries reported)", agent=r.agent, signals=len(found))
            for s in found:
                n += 1
                s = dict(s)
                s["signal_id"] = f"S{n:03d}"
                s["agent"] = r.agent
                signals.append(s)
                self.store.put_json("signals", {"run_id": self.run_id, "signal_id": s["signal_id"], "agent": r.agent}, s)
                for e in s.get("evidence", []):
                    self.store.add_source(e.get("url", ""), e.get("source_title", ""), self.run_id, r.agent)
            for lim in r.output.get("limitations", []):
                self.state["limitations"].append(f"{r.agent}: {lim}")
        self._save("01_raw_signals", signals)
        ok = sum(1 for r in results if r.status == "ok")
        self.log.log("ORCHESTRATOR", f"discovery complete: {ok}/{len(results)} agents succeeded, {len(signals)} raw signals")
        self.state["raw_signals"] = len(signals)
        return signals

    # -- stage 2
    def deduplicate(self, signals: list[dict]):
        unique, merged = dedup.near_duplicate_merge(signals)
        self.log.log("DEDUP", f"deterministic pass: {len(signals)} → {len(unique)} signals ({len(merged)} near-duplicates merged)")
        self.state["after_exact_dedup"] = len(unique)
        limit = int(self.cfg["run"]["candidate_limit"])
        compact = [{"id": s["signal_id"], "agent": s["agent"], "also_found_by": s.get("also_found_by", []),
                    "problem": s.get("problem"), "customer": s.get("customer"), "segment": s.get("segment"),
                    "sector": s.get("sector"), "type": s.get("opportunity_type"), "horizon": s.get("time_horizon"),
                    "solution": s.get("potential_solution"), "business_model": s.get("business_model"),
                    "existing_spend": s.get("existing_spend"), "confidence": s.get("confidence"),
                    "frequency": s.get("frequency"), "severity": s.get("severity"),
                    "evidence_types": [e.get("evidence_type") for e in s.get("evidence", [])],
                    "existing_solutions": [x.get("name") for x in s.get("existing_solution", [])],
                    "unknowns": s.get("unknowns", [])[:3]} for s in unique]
        cons = None
        if unique:
            r = self._parallel([("consolidator", "Merge duplicate pains and rank candidates as instructed.",
                                 {"candidate_limit": limit, "signals": compact}, "consolidator")])[0]
            cons = r.output if r.status == "ok" else None
        if cons is None:
            self.log.log("ORCHESTRATOR", "CONSOLIDATOR unavailable — using deterministic fallback ranking", level="WARN")
            self.state["limitations"].append("Consolidator agent failed; candidates were ranked deterministically without semantic merging.")
            cons = dedup.fallback_candidates(unique, limit)
        by_id = {s["signal_id"]: s for s in signals}
        candidates = []
        for c in cons["candidates"][:limit]:
            members = [by_id[i] for i in c.get("member_signal_ids", []) if i in by_id]
            for m in list(members):
                members += [by_id[d] for d in m.get("duplicate_ids", []) if d in by_id]
            c = dict(c)
            c["source_agents"] = sorted({m["agent"] for m in members})
            ev, seen = [], set()
            for m in members:
                for e in m.get("evidence", []):
                    if e.get("url") not in seen:
                        seen.add(e.get("url"))
                        ev.append(e)
            c["evidence"] = ev[:14]
            c["existing_solutions"] = [x for m in members for x in m.get("existing_solution", [])][:10]
            c["foreign_models"] = [m["foreign_model"] for m in members if m.get("foreign_model", {}).get("name")]
            c["workarounds"] = list(dict.fromkeys(m.get("workaround", "") for m in members if m.get("workaround")))[:4]
            c["existing_spend"] = list(dict.fromkeys(m.get("existing_spend", "") for m in members if m.get("existing_spend")))[:4]
            c["unknowns"] = list(dict.fromkeys(u for m in members for u in m.get("unknowns", [])))[:8]
            candidates.append(c)
        for inj in self.inject_candidates:
            candidates.append(dict(inj))
            self.log.log("ORCHESTRATOR", f"injected test candidate {inj['candidate_id']}: {inj['title']}")
        for c in candidates:
            self.store.put_json("candidates", {"run_id": self.run_id, "candidate_id": c["candidate_id"]}, c,
                                {"title": c.get("title", ""), "status": "CANDIDATE"})
        self._save("02_candidates", {"candidates": candidates, "backlog": cons.get("backlog", []),
                                     "discarded": cons.get("discarded", []), "merge_notes": cons.get("merge_notes", "")})
        self.state["candidates"] = len(candidates)
        self.state["backlog"] = len(cons.get("backlog", []))
        self.state["discarded"] = len(cons.get("discarded", []))
        self.log.log("ORCHESTRATOR", f"deduplication complete: {len(candidates)} candidates, "
                     f"{len(cons.get('backlog', []))} backlog, {len(cons.get('discarded', []))} discarded groups")
        return candidates, cons.get("backlog", []), cons.get("discarded", [])

    @staticmethod
    def _dossier(c: dict) -> dict:
        keys = ["candidate_id", "title", "problem", "customer", "segment", "sector", "opportunity_type", "time_horizon",
                "potential_solution", "business_model", "evidence", "existing_solutions", "foreign_models",
                "workarounds", "existing_spend", "unknowns", "open_questions", "source_agents"]
        return {k: c.get(k) for k in keys if c.get(k) not in (None, [], "")}

    # -- stage 3
    def validate(self, candidates: list[dict]) -> dict:
        size = int(self.cfg["run"]["validation_batch_size"])
        batches = self._batches([self._dossier(c) for c in candidates], size)
        jobs = []
        for v in VALIDATORS:
            for i, b in enumerate(batches, 1):
                jobs.append((v, f"Validate every candidate in INPUT_JSON.candidates as the {v.upper()}. "
                                "Return exactly one result per candidate_id, using the same ids.",
                             {"candidates": b}, f"batch{i}"))
        self.log.log("ORCHESTRATOR", f"dispatching {len(jobs)} validator jobs ({len(VALIDATORS)} validators × {len(batches)} batches)")
        results = self._parallel(jobs)
        validations: dict = {c["candidate_id"]: {} for c in candidates}
        for (v, _, payload, _), r in zip(jobs, results):
            ids = [c["candidate_id"] for c in payload["candidates"]]
            if r.status != "ok":
                for cid in ids:
                    validations[cid][v] = {"_missing": True, "error": r.error}
                continue
            got = {x.get("candidate_id"): x for x in r.output.get("results", [])}
            for cid in ids:
                if cid in got:
                    validations[cid][v] = got[cid]
                    self.store.put_json("validations", {"run_id": self.run_id, "candidate_id": cid, "validator": v}, got[cid])
                    for key in ("new_sources", "payment_evidence", "competitors"):
                        for s in got[cid].get(key, []):
                            self.store.add_source(s.get("url", ""), s.get("title", s.get("name", "")), self.run_id, v)
                    for cl in got[cid].get("claims", []):
                        for s in cl.get("sources", []):
                            self.store.add_source(s.get("url", ""), s.get("title", ""), self.run_id, v)
                else:
                    validations[cid][v] = {"_missing": True, "error": "validator omitted this candidate"}
            for lim in r.output.get("limitations", []):
                self.state["limitations"].append(f"{v}: {lim}")
        for cid, vals in validations.items():
            p = vals.get("payment_validator", {}).get("someone_pays_now", "n/a")
            m = vals.get("competition_validator", {}).get("market_state", "n/a")
            f = vals.get("feasibility_validator", {}).get("complexity", "n/a")
            e = vals.get("evidence_validator", {}).get("problem_evidence_level", "n/a")
            self.log.log("VALIDATION", f"{cid}: problem_evidence={e} pays_now={p} market={m} complexity={f}", candidate=cid)
        self._save("03_validations", validations)
        return validations

    # -- stage 4 / 7
    def kill(self, candidates: list[dict], validations: dict, research: dict, round_no: int, final: bool) -> dict:
        size = int(self.cfg["run"]["validation_batch_size"])
        dossiers = []
        for c in candidates:
            d = self._dossier(c)
            d["validation"] = {k: v for k, v in validations.get(c["candidate_id"], {}).items()}
            if c["candidate_id"] in research:
                d["additional_research"] = research[c["candidate_id"]]
            dossiers.append(d)
        jobs = [("killer_agent", "Try to kill every candidate in INPUT_JSON.candidates. One result per candidate_id.",
                 {"candidates": b, "final_round": final, "round": round_no}, f"r{round_no}_batch{i}")
                for i, b in enumerate(self._batches(dossiers, size), 1)]
        results = self._parallel(jobs)
        verdicts: dict = {}
        for (_, _, payload, _), r in zip(jobs, results):
            got = {x.get("candidate_id"): x for x in (r.output or {}).get("results", [])} if r.status == "ok" else {}
            for d in payload["candidates"]:
                cid = d["candidate_id"]
                v = got.get(cid) or {"candidate_id": cid, "verdict": "UNDECIDED", "kill_reasons": [],
                                     "summary": f"Killer agent unavailable: {r.error}", "remaining_uncertainties": [],
                                     "missing_info_requests": [], "attacks_attempted": [], "survival_notes": ""}
                if final and v.get("verdict") == "NEEDS_MORE_EVIDENCE":
                    v["verdict"] = "UNDECIDED"
                verdicts[cid] = v
                self.store.put_json("verdicts", {"run_id": self.run_id, "candidate_id": cid, "round": round_no}, v,
                                    {"verdict": v["verdict"]})
                self.store.execute("UPDATE candidates SET status=? WHERE run_id=? AND candidate_id=?",
                                   (v["verdict"], self.run_id, cid))
                for kr in v.get("kill_reasons", []):
                    for s in kr.get("evidence", []):
                        self.store.add_source(s.get("url", ""), s.get("summary", "")[:80], self.run_id, "killer_agent")
                reason = "; ".join(k["reason"][:90] for k in v.get("kill_reasons", []) if k.get("severity") == "FATAL")[:200]
                self.log.log("KILLER_AGENT", f"{cid} → {v['verdict']}" + (f" ({reason})" if reason and v['verdict'] == 'REJECTED' else ""),
                             candidate=cid, verdict=v["verdict"], round=round_no)
        self._save(f"04_verdicts_round{round_no}", verdicts)
        return verdicts

    # -- stage 5
    def detect_gaps(self, candidates, validations, verdicts) -> dict:
        """Returns {candidate_id: [questions]} — Killer requests + orchestrator-detected gaps."""
        requests: dict[str, list[dict]] = {}
        for c in candidates:
            cid = c["candidate_id"]
            v = verdicts.get(cid, {})
            if v.get("verdict") == "NEEDS_MORE_EVIDENCE":
                qs = v.get("missing_info_requests") or [{"question": "What evidence would decide this candidate?", "route_to": "evidence"}]
                requests[cid] = list(qs)
            elif v.get("verdict") == "SURVIVED":
                qs = []
                pay = validations.get(cid, {}).get("payment_validator", {})
                if pay.get("_missing") or pay.get("someone_pays_now") in ("UNCLEAR", "NO"):
                    qs.append({"question": f"Is anyone in Saudi Arabia/GCC currently paying for a solution to: "
                                           f"{c.get('problem', '')[:200]}? Find prices, paid tools, service fees or salaries.",
                               "route_to": "payment"})
                    self.log.log("GAP_DETECTOR", f"{cid}: survived but payment evidence is "
                                                 f"{pay.get('someone_pays_now', 'missing')} → re-research", candidate=cid)
                # Survivors go to synthesis only after the Killer's open uncertainties were researched.
                qs += [{"question": u, "route_to": "market"} for u in v.get("remaining_uncertainties", [])[:3]]
                if qs:
                    requests[cid] = qs
                    self.log.log("GAP_DETECTOR", f"{cid}: survived with {len(qs)} unresolved uncertainty(ies) "
                                                 "→ additional research + final Killer round", candidate=cid)
            for vname, val in validations.get(cid, {}).items():
                if val.get("_missing") and cid in requests:
                    requests[cid].append({"question": f"(validator {vname} failed) fill in the missing {vname.split('_')[0]} information",
                                          "route_to": vname.split("_")[0]})
        for cid, qs in requests.items():
            self.log.log("GAP_DETECTOR", f"{cid}: {len(qs)} open question(s) → GAP_RESEARCHER", candidate=cid,
                         questions=[q["question"] for q in qs])
        self.state["gap_requests"] = self.state.get("gap_requests", 0) + len(requests)
        return requests

    # -- stage 6
    def gap_research(self, requests: dict, rnd: int, research: dict) -> dict:
        items = [{"candidate_id": cid, "questions": qs} for cid, qs in requests.items()]
        jobs = [("gap_researcher", "Answer every open question for every candidate in INPUT_JSON.requests.",
                 {"requests": b}, f"r{rnd}_{b[0]['candidate_id']}") for i, b in enumerate(self._batches(items, 1), 1)]
        self.log.log("ORCHESTRATOR", f"re-dispatching research: {len(items)} candidates in {len(jobs)} GAP_RESEARCHER job(s)")
        self.state["retries"] += len(jobs)
        for r in self._parallel(jobs):
            if r.status != "ok":
                continue
            for x in r.output.get("results", []):
                cid = x.get("candidate_id")
                research.setdefault(cid, []).extend(x.get("answers", []))
                self.store.put_json("research", {"run_id": self.run_id, "candidate_id": cid, "round": rnd}, x)
                for a in x.get("answers", []):
                    for s in a.get("sources", []):
                        self.store.add_source(s.get("url", ""), s.get("title", ""), self.run_id, "gap_researcher")
                found = sum(1 for a in x.get("answers", []) if a.get("finding") == "FOUND")
                self.log.log("GAP_RESEARCHER", f"{cid}: {found}/{len(x.get('answers', []))} questions answered with evidence",
                             candidate=cid)
        (ROOT / "research").mkdir(exist_ok=True)
        (ROOT / "research" / f"{self.run_id}_gap_research.json").write_text(
            json.dumps(research, ensure_ascii=False, indent=2), encoding="utf-8")
        self._save(f"05_gap_research_r{rnd}", research)
        return research

    # -- stage 8
    def synthesize(self, candidates, validations, verdicts, research, backlog, signals) -> dict | None:
        surv = [c for c in candidates if verdicts.get(c["candidate_id"], {}).get("verdict") == "SURVIVED"]
        rej = [c for c in candidates if verdicts.get(c["candidate_id"], {}).get("verdict") == "REJECTED"]
        self.state["survived"] = len(surv)
        self.state["rejected"] = len(rej)
        self.state["undecided"] = sum(1 for c in candidates if verdicts.get(c["candidate_id"], {}).get("verdict") == "UNDECIDED")
        dossier = {
            "survivors": [{**self._dossier(c), "validation": validations.get(c["candidate_id"], {}),
                           "killer": verdicts.get(c["candidate_id"]), "additional_research": research.get(c["candidate_id"], [])}
                          for c in surv],
            "rejected": [{"candidate_id": c["candidate_id"], "title": c.get("title"),
                          "kill_reasons": verdicts[c["candidate_id"]].get("kill_reasons", [])} for c in rej],
            "backlog_leads": [{**b, "signals": [{"problem": s.get("problem"), "customer": s.get("customer"),
                                                 "evidence": s.get("evidence", [])[:3]}
                                                for s in signals if s["signal_id"] in b.get("member_signal_ids", [])][:2]}
                              for b in backlog[:30]],
            "foreign_model_signals": [{"id": s["signal_id"], "problem": s.get("problem"), "foreign_model": s.get("foreign_model"),
                                       "evidence": s.get("evidence", [])[:3], "existing_solution": s.get("existing_solution", [])[:3]}
                                      for s in signals if s.get("foreign_model", {}).get("name")],
            "future_signals": [{"id": s["signal_id"], "problem": s.get("problem"), "evidence": s.get("evidence", [])[:4],
                                "unknowns": s.get("unknowns", [])} for s in signals if s.get("time_horizon") == "FUTURE_HYPOTHESIS"],
        }
        self._save("06_synthesis_input", dossier)
        r = self._parallel([("synthesizer", "Build the final opportunity set from the dossier in INPUT_JSON as instructed.",
                             dossier, "synthesizer")])[0]
        if r.status != "ok":
            self.log.log("ORCHESTRATOR", "SYNTHESIZER failed — report will use deterministic fallback", level="WARN")
            self.state["limitations"].append("Synthesizer agent failed; the report sections were generated deterministically.")
            return None
        self._save("07_synthesis", r.output)
        self.log.log("OPPORTUNITY_SYNTHESIZER", f"{len(r.output.get('golden_opportunities', []))} golden, "
                     f"{len(r.output.get('hidden_gems', []))} hidden gems, {len(r.output.get('foreign_models', []))} foreign models")
        return r.output

    # ----------------------------------------------------------------- stats
    def summary(self, elapsed: float, status: str) -> dict:
        marks = ",".join("?" for _ in self.run_ids)
        rows = self.store.query(f"SELECT * FROM agent_runs WHERE run_id IN ({marks})", tuple(self.run_ids))
        executed = [r for r in rows if not r["cache_hit"] and r["status"] != "skipped"]
        return {
            "run_id": self.run_id, "resumed_from": self.resume_from, "mode": self.mode, "status": status, "elapsed_sec": round(elapsed, 1),
            "counts": {
                "agent_processes_launched": sum(r["attempts"] or 0 for r in executed),
                "agent_tasks_executed": len(executed),
                "distinct_agent_types_run": len({r["agent"] for r in executed}),
                "agent_tasks_succeeded": sum(1 for r in executed if r["status"] == "ok"),
                "agent_tasks_failed": sum(1 for r in executed if r["status"] == "failed"),
                "agent_tasks_skipped": sum(1 for r in rows if r["status"] == "skipped"),
                "agent_cache_hits": sum(1 for r in rows if r["cache_hit"]),
                "web_searches": sum(r["searches"] or 0 for r in rows),
                "web_fetches": sum(r["fetches"] or 0 for r in rows),
                "search_cache_hits": sum(r["search_cache_hits"] or 0 for r in rows),
                "budget_blocked_tool_calls": sum(r["blocked_calls"] or 0 for r in rows),
                "raw_signals": self.state.get("raw_signals", 0),
                "after_exact_dedup": self.state.get("after_exact_dedup", 0),
                "candidates_validated": self.state.get("candidates", 0),
                "backlog": self.state.get("backlog", 0),
                "gap_research_requests": self.state.get("gap_requests", 0),
                "survived_killer": self.state.get("survived", 0),
                "rejected_by_killer": self.state.get("rejected", 0),
                "undecided": self.state.get("undecided", 0),
                "total_cost_usd": round(sum(r["cost_usd"] or 0 for r in rows), 3),
            },
            "stage_times_sec": self.state["stage_times"],
            "failures": self.state["failures"],
        }
