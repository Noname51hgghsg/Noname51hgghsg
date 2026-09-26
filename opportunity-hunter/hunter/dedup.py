"""Deterministic de-duplication and fallback ranking (no LLM)."""
from __future__ import annotations

import re

EVIDENCE_WEIGHT = {"DIRECT": 3, "STRONG_INDIRECT": 2, "WEAK": 1, "HYPOTHESIS": 0}
_STOP = set("the a an of for to in and or with on by is are be at from saudi arabia ksa riyadh في من على إلى الى عن مع و أو".split())


def tokens(text: str) -> set[str]:
    words = re.findall(r"[\w؀-ۿ]+", (text or "").lower())
    return {w for w in words if len(w) > 2 and w not in _STOP}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def evidence_score(signal: dict) -> float:
    ev = signal.get("evidence", [])
    score = sum(EVIDENCE_WEIGHT.get(e.get("evidence_type"), 0) for e in ev[:6])
    score += {"HIGH": 3, "MEDIUM": 1.5, "LOW": 0}.get(signal.get("confidence"), 0)
    if signal.get("existing_spend") and "NO RELIABLE" not in signal.get("existing_spend", "").upper():
        score += 2
    return score


def near_duplicate_merge(signals: list[dict], threshold: float = 0.72) -> tuple[list[dict], list[tuple[str, str]]]:
    """Merge near-identical signals (same problem + customer wording). Semantic merging is left to the
    CONSOLIDATOR agent; this pass only removes obvious duplicates to save tokens."""
    kept: list[dict] = []
    merged: list[tuple[str, str]] = []
    toks = []
    for s in signals:
        t = tokens(s.get("problem", "") + " " + s.get("customer", ""))
        dup_of = None
        for i, kt in enumerate(toks):
            if jaccard(t, kt) >= threshold:
                dup_of = i
                break
        if dup_of is None:
            s = dict(s)
            s["duplicate_ids"] = []
            kept.append(s)
            toks.append(t)
        else:
            base = kept[dup_of]
            base["duplicate_ids"].append(s["signal_id"])
            seen = {e.get("url") for e in base.get("evidence", [])}
            base["evidence"] = base.get("evidence", []) + [e for e in s.get("evidence", []) if e.get("url") not in seen]
            base.setdefault("also_found_by", []).append(s.get("agent"))
            merged.append((s["signal_id"], base["signal_id"]))
    return kept, merged


def fallback_candidates(signals: list[dict], limit: int) -> dict:
    """Used only if the CONSOLIDATOR agent fails: one candidate per signal, ranked by evidence score."""
    ranked = sorted(signals, key=evidence_score, reverse=True)
    cands = []
    for i, s in enumerate(ranked[:limit], 1):
        cands.append({
            "candidate_id": f"C{i:02d}", "title": s.get("problem", "")[:90], "problem": s.get("problem", ""),
            "customer": s.get("customer", ""), "segment": s.get("segment", "B2B"), "sector": s.get("sector", ""),
            "opportunity_type": s.get("opportunity_type", "NEW_OPPORTUNITY"), "time_horizon": s.get("time_horizon", "CURRENT_EVIDENCE"),
            "member_signal_ids": [s["signal_id"]] + s.get("duplicate_ids", []),
            "potential_solution": s.get("potential_solution", ""), "business_model": s.get("business_model", ""),
            "priority": max(1, min(10, round(evidence_score(s)))), "priority_rationale": "deterministic fallback: evidence score",
            "open_questions": s.get("unknowns", [])[:4]})
    backlog = [{"title": s.get("problem", "")[:90], "member_signal_ids": [s["signal_id"]],
                "reason_not_prioritized": "below candidate limit (fallback ranking)"} for s in ranked[limit:]]
    return {"candidates": cands, "backlog": backlog, "discarded": [],
            "merge_notes": "CONSOLIDATOR agent failed; deterministic fallback used (no semantic merging)."}
