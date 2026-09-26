"""Renders reports/final_report.md from the run's structured data."""
from __future__ import annotations

import datetime as _dt
import json
import re

URL_RE = re.compile(r"https?://[^\s\"'<>)\]]+")

SYSTEM_LIMITATIONS = [
    "WebSearch هو محرك البحث المدمج في Claude Code (فهرس مركزه الولايات المتحدة)؛ تغطية المحتوى العربي/السعودي المحلي أقل من Google في السعودية.",
    "منصات X و TikTok و LinkedIn و Instagram و Snapchat تتطلب تسجيل دخول غالبًا؛ استُخدم فقط ما يظهر في نتائج البحث العامة، ولم يتم تجاوز أي حماية.",
    "لا توجد مفاتيح APIs مدفوعة (SerpAPI / Google / X API)؛ جميع البيانات من صفحات عامة.",
    "تقييمات الوكلاء (تصنيف الأدلة، التعقيد، التكلفة) هي أحكام نموذج لغوي مبنية على المصادر المذكورة، وليست دراسات سوق ميدانية.",
    "لم يتم التواصل مع أي عميل أو شركة؛ لم تُختبر رغبة الدفع مباشرة — هذه أول خطوة يجب أن يقوم بها المؤسس.",
    "الروابط المذكورة شوهدت من قبل الوكلاء أثناء التشغيل، لكن صفحات الويب تتغير؛ تحقق من الأسعار قبل الاعتماد عليها.",
]


def _j(x) -> str:
    return json.dumps(x, ensure_ascii=False)


def _bullets(items, empty="—") -> str:
    items = [i for i in (items or []) if i]
    return "\n".join(f"  - {i}" for i in items) if items else f"  - {empty}"


def _links(urls) -> str:
    urls = [u for u in (urls or []) if u]
    return "\n".join(f"  - <{u}>" for u in urls) if urls else "  - NO RELIABLE EVIDENCE FOUND"


def render(orch, candidates, validations, verdicts, research, backlog, discarded, signals, synthesis, summary) -> None:
    run_id = orch.run_id
    rows = orch.store.query("SELECT * FROM agent_runs WHERE run_id=? ORDER BY id", (run_id,))
    known_urls = set(URL_RE.findall(_j([signals, validations, verdicts, research, candidates])))
    cmap = {c["candidate_id"]: c for c in candidates}
    c = summary["counts"]
    out: list[str] = []
    w = out.append

    w(f"# تقرير صائد الفرص — Opportunity Hunter Final Report\n")
    w(f"- **Run ID:** `{run_id}` — **Mode:** `{orch.mode}` — **Generated:** {_dt.datetime.now():%Y-%m-%d %H:%M}")
    w(f"- **Market:** {orch.cfg['run']['market']} (global research used to find adaptable models)")
    w(f"- **Status:** {summary['status']} — **Elapsed:** {summary['elapsed_sec']}s — **Total agent cost:** ${c['total_cost_usd']}\n")

    w("## 0. ملخص التشغيل (Run Statistics)\n")
    w("| المؤشر | القيمة |\n|---|---|")
    for label, key in [("عمليات Agents التي أُطلقت فعليًا (processes incl. retries)", "agent_processes_launched"),
                       ("مهام Agents المنفّذة", "agent_tasks_executed"),
                       ("أنواع Agents المختلفة التي عملت", "distinct_agent_types_run"),
                       ("مهام ناجحة / فاشلة / متخطاة", None),
                       ("عمليات البحث (WebSearch)", "web_searches"),
                       ("جلب صفحات (WebFetch)", "web_fetches"),
                       ("إصابات Cache للبحث", "search_cache_hits"),
                       ("استدعاءات منعها حد الميزانية", "budget_blocked_tool_calls"),
                       ("الإشارات/الفرص الخام", "raw_signals"),
                       ("بعد إزالة التكرار الحرفي", "after_exact_dedup"),
                       ("مرشحون دخلوا التحقق (بعد التصفية)", "candidates_validated"),
                       ("طلبات بحث إضافي (Gap research)", "gap_research_requests"),
                       ("نجت من Killer Agent", "survived_killer"),
                       ("رفضها Killer Agent", "rejected_by_killer"),
                       ("غير محسومة", "undecided")]:
        val = f"{c['agent_tasks_succeeded']} / {c['agent_tasks_failed']} / {c['agent_tasks_skipped']}" if key is None else c[key]
        w(f"| {label} | {val} |")
    w("")

    if synthesis and synthesis.get("executive_summary"):
        w("### الخلاصة التنفيذية\n")
        w(synthesis["executive_summary"] + "\n")

    # ---------------------------------------------------------------- golden
    w("## 1. الفرص الذهبية (Golden Opportunities)\n")
    golden = (synthesis or {}).get("golden_opportunities") or []
    if synthesis is None:
        golden = _fallback_golden(candidates, validations, verdicts)
        w("> ⚠️ Synthesizer agent failed — this section was generated deterministically from validator outputs.\n")
    if not golden:
        w("**لم يتم العثور على فرصة تستحق التصنيف كفرصة ذهبية في هذا التشغيل.**\n")
        if synthesis and synthesis.get("no_opportunity_statement"):
            w(synthesis["no_opportunity_statement"] + "\n")
    for i, g in enumerate(golden, 1):
        v = verdicts.get(g.get("candidate_id"), {})
        w(f"### {i}. {g.get('name')}  \n`{g.get('candidate_id')}` · **{g.get('category')}** · Complexity: **{g.get('complexity')}** · "
          f"Evidence quality: **{g.get('evidence_quality')}** · Killer: **{v.get('verdict', 'n/a')}**\n")
        for label, key in [("المشكلة (Problem)", "problem"), ("العميل (Customer)", "customer"),
                           ("لماذا توجد المشكلة (Why it exists)", "why_it_exists"),
                           ("البدائل الحالية (Existing alternatives)", "existing_alternatives"),
                           ("الفرصة في السعودية (Saudi opportunity)", "saudi_opportunity"), ("الحل (Solution)", "solution"),
                           ("MVP", "mvp"), ("التقنية (Technology)", "technology"), ("التكلفة التقديرية (Estimated cost)", "estimated_cost"),
                           ("نموذج الإيرادات (Revenue model)", "revenue_model"),
                           ("استراتيجية أول عميل (First customer strategy)", "first_customer_strategy"),
                           ("التوسع (Expansion)", "expansion")]:
            w(f"- **{label}:** {g.get(key, '—')}")
        w("- **الأدلة (Evidence):**")
        for e in g.get("evidence", []):
            w(f"  - [{e.get('evidence_type')}] {e.get('claim')} — <{e.get('url')}>")
        w("- **المنافسون (Competitors):**")
        for comp in g.get("competitors", []):
            w(f"  - {comp.get('name')} — {comp.get('note', '')} <{comp.get('url', '')}>")
        w("- **المخاطر (Risks):**\n" + _bullets(g.get("risks")))
        w("- **المجهول (Unknowns):**\n" + _bullets(g.get("unknowns")))
        if v.get("remaining_uncertainties"):
            w("- **ما بقي غير مؤكد حسب Killer Agent:**\n" + _bullets(v.get("remaining_uncertainties")))
        w("- **المصادر (Sources):**\n" + _links(g.get("sources")))
        w("")

    # ---------------------------------------------------------------- other synthesis sections
    s = synthesis or {}
    w("## 2. جواهر مخفية (Hidden Gems)\n")
    gems = s.get("hidden_gems") or []
    if not gems:
        w("NO RELIABLE EVIDENCE FOUND / لا توجد عناصر.\n")
    for g in gems:
        w(f"- **{g.get('name')}** (`{g.get('candidate_id') or '-'}`, {g.get('validation_status')}, {g.get('complexity')}): "
          f"{g.get('one_liner')} — {g.get('why_interesting')} " + " ".join(f"<{u}>" for u in g.get("sources", [])[:3]))
    w("")
    w("## 3. نماذج عالمية قابلة للتكييف (Foreign Models)\n")
    for f in s.get("foreign_models") or []:
        w(f"- **{f.get('model_name')}** ({f.get('country')}) <{f.get('url')}> — {f.get('what_it_does')}  \n"
          f"  نموذج الإيراد: {f.get('revenue_model')} · الوضع في السعودية: {f.get('saudi_equivalent_status')}  \n"
          f"  التكييف: {f.get('adaptation_notes')} " + " ".join(f"<{u}>" for u in f.get("sources", [])[:3]))
    if not s.get("foreign_models"):
        w("لا توجد عناصر.")
    w("")
    w("## 4. أعمال مملة لكنها مربحة (Boring Businesses)\n")
    for b in s.get("boring_businesses") or []:
        w(f"- **{b.get('name')}** — {b.get('problem')}  \n  من يدفع: {b.get('who_pays')} · الدليل: {b.get('evidence')} "
          + " ".join(f"<{u}>" for u in b.get("sources", [])[:3]))
    if not s.get("boring_businesses"):
        w("لا توجد عناصر.")
    w("")
    w("## 5. فرص مستقبلية 1–3 سنوات (Future Opportunities)\n")
    w("> الأدلة الحالية (CURRENT EVIDENCE) منفصلة عن الفرضية (FUTURE HYPOTHESIS). لا شيء هنا حقيقة مؤكدة.\n")
    for f in s.get("future_opportunities") or []:
        w(f"- **{f.get('name')}** ({f.get('horizon')})  \n  **CURRENT EVIDENCE:** {f.get('current_evidence')}  \n"
          f"  **FUTURE HYPOTHESIS:** {f.get('hypothesis')}  \n  المحفّز: {f.get('trigger')} "
          + " ".join(f"<{u}>" for u in f.get("sources", [])[:3]))
    if not s.get("future_opportunities"):
        w("لا توجد عناصر.")
    w("")

    # ---------------------------------------------------------------- rejected
    w("## 6. الفرص المرفوضة (Rejected by Killer Agent)\n")
    w("> هذا القسم لتعرف ما الذي **لا يجب** أن تضيّع وقتك عليه.\n")
    rejected = [cid for cid, v in verdicts.items() if v.get("verdict") == "REJECTED"]
    if not rejected:
        w("لم يرفض Killer Agent أي فرصة.\n")
    for cid in rejected:
        v = verdicts[cid]
        cand = cmap.get(cid, {})
        w(f"### ❌ {cid} — {cand.get('title', '')}\n")
        w(f"- **المشكلة:** {cand.get('problem', '')}")
        for kr in v.get("kill_reasons", []):
            ev = " ".join(f"<{e.get('url')}>" for e in kr.get("evidence", []) if e.get("url"))
            w(f"- **[{kr.get('severity')}] {kr.get('category')}:** {kr.get('reason')} {ev}")
        if v.get("summary"):
            w(f"- **الخلاصة:** {v['summary']}")
        w("")

    # ---------------------------------------------------------------- buildability
    w("## 7. قابلية بناء MVP (Buildability of surviving opportunities)\n")
    w("| ID | الفرصة | Complexity | MVP cost (SAR) | Monthly (SAR) | Build (weeks) | Solo? | Someone pays now? | Market |")
    w("|---|---|---|---|---|---|---|---|---|")
    order = {"EASY": 0, "MODERATE": 1, "HARD": 2}
    surv = [cid for cid, v in verdicts.items() if v.get("verdict") == "SURVIVED"]
    surv.sort(key=lambda cid: order.get(validations.get(cid, {}).get("feasibility_validator", {}).get("complexity"), 3))
    for cid in surv:
        f = validations.get(cid, {}).get("feasibility_validator", {})
        p = validations.get(cid, {}).get("payment_validator", {})
        m = validations.get(cid, {}).get("competition_validator", {})
        w(f"| {cid} | {cmap.get(cid, {}).get('title', '')} | **{f.get('complexity', '?')}** | "
          f"{f.get('mvp_cost_sar_low', '?')}–{f.get('mvp_cost_sar_high', '?')} | {f.get('monthly_run_cost_sar', '?')} | "
          f"{f.get('build_time_weeks', '?')} | {f.get('solo_founder_feasible', '?')} | {p.get('someone_pays_now', '?')} | "
          f"{m.get('market_state', '?')} |")
    if not surv:
        w("| — | لا توجد فرص ناجية | | | | | | | |")
    w("\n> الأولوية لفرص **EASY** ثم **MODERATE**.\n")

    undecided = [cid for cid, v in verdicts.items() if v.get("verdict") == "UNDECIDED"]
    if undecided:
        w("### فرص غير محسومة (Undecided)\n")
        for cid in undecided:
            w(f"- `{cid}` {cmap.get(cid, {}).get('title', '')}: {verdicts[cid].get('summary', '')}")
        w("")

    w("## 8. قائمة الانتظار (Backlog — لم تدخل التحقق)\n")
    for b in backlog[:40]:
        w(f"- {b.get('title')} — _{b.get('reason_not_prioritized', '')}_ ({', '.join(b.get('member_signal_ids', []))})")
    if not backlog:
        w("لا توجد عناصر.")
    if discarded:
        w("\n**مستبعدة مبكرًا من Consolidator:**")
        for d in discarded[:30]:
            w(f"- {', '.join(d.get('signal_ids', []))}: {d.get('reason')}")
    w("")

    # ---------------------------------------------------------------- limitations
    w("## 9. قيود البحث (Research Limitations)\n")
    w("### قيود النظام\n" + "\n".join(f"- {x}" for x in SYSTEM_LIMITATIONS))
    if summary.get("failures"):
        w("\n### فشل الوكلاء (Agent failures — النظام استمر)\n")
        for f in summary["failures"]:
            w(f"- `{f['agent']}` [{f['label']}] {f['status']}: {str(f.get('error'))[:220]}")
    lims = list(dict.fromkeys(orch.state.get("limitations", [])))
    if lims:
        w("\n### قيود أبلغ عنها الوكلاء\n")
        for l in lims[:60]:
            w(f"- {l}")
    unverified = sorted({u.rstrip('.,') for u in URL_RE.findall(_j(synthesis or {}))} - {u.rstrip('.,') for u in known_urls})
    w("\n### فحص الروابط (URL integrity check)\n")
    if unverified:
        w("روابط ظهرت في التجميع النهائي ولم تُجمع من أي وكيل بحث في هذا التشغيل — **تعامل معها بحذر:**")
        for u in unverified:
            w(f"- <{u}>")
    else:
        w("✅ كل الروابط في الأقسام التجميعية مصدرها وكلاء البحث في هذا التشغيل (لم يُضف المُجمِّع روابط جديدة).")
    w("")

    # ---------------------------------------------------------------- execution proof
    w("## 10. سجل تنفيذ الوكلاء (Agent Execution Log — proof of real runs)\n")
    w("كل صف = مهمة Agent نُفّذت كعملية مستقلة `claude -p` (PID وsession مستقلان). السجل الكامل: "
      f"`logs/{run_id}/run.log` · النصوص الكاملة: `results/{run_id}/transcripts/`\n")
    w("| # | Agent | Task | Stage | Status | Attempts | PID | Session | Start | Dur (s) | Searches | Fetches | Cache hits | Cost $ |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        w(f"| {i} | {r['agent']} | {r['task_label']} | {r['stage']} | {r['status']}{' (cached)' if r['cache_hit'] else ''} | "
          f"{r['attempts']} | {r['pid'] or ''} | {(r['session_id'] or '')[:8]} | {(r['started_at'] or '')[11:19]} | "
          f"{r['duration_sec'] or 0} | {r['searches'] or 0} | {r['fetches'] or 0} | {r['search_cache_hits'] or 0} | "
          f"{(r['cost_usd'] or 0):.3f} |")
    w("\n### أزمنة المراحل\n")
    for k, v in summary.get("stage_times_sec", {}).items():
        w(f"- {k}: {v}s")
    w("\n## 11. المنهجية (Methodology)\n")
    w("Discovery (13 agents بالتوازي) → Deduplication (كود + Consolidator agent) → Evidence/Payment/Competition/Feasibility "
      "validators (بالتوازي على دفعات) → Killer Agent → Gap detection → Gap Researcher (بحث إضافي) → Killer final round → "
      "Opportunity Synthesizer → هذا التقرير. التفاصيل في `README.md`.")
    orch.report_path.parent.mkdir(parents=True, exist_ok=True)
    orch.report_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    orch.log.log("REPORT", f"written to {orch.report_path}")


def _fallback_golden(candidates, validations, verdicts) -> list[dict]:
    order = {"EASY": 0, "MODERATE": 1, "HARD": 2}
    pay_rank = {"YES": 0, "PARTIAL": 1, "UNCLEAR": 2, "NO": 3}
    surv = [c for c in candidates if verdicts.get(c["candidate_id"], {}).get("verdict") == "SURVIVED"]
    surv.sort(key=lambda c: (pay_rank.get(validations.get(c["candidate_id"], {}).get("payment_validator", {}).get("someone_pays_now"), 4),
                             order.get(validations.get(c["candidate_id"], {}).get("feasibility_validator", {}).get("complexity"), 3)))
    out = []
    for c in surv[:10]:
        v = validations.get(c["candidate_id"], {})
        f, p, m = v.get("feasibility_validator", {}), v.get("payment_validator", {}), v.get("competition_validator", {})
        out.append({"candidate_id": c["candidate_id"], "name": c.get("title"), "category": c.get("opportunity_type"),
                    "problem": c.get("problem"), "customer": c.get("customer"),
                    "evidence": [{"claim": e.get("claim"), "url": e.get("url"), "evidence_type": e.get("evidence_type")} for e in c.get("evidence", [])[:6]],
                    "why_it_exists": "—", "existing_alternatives": m.get("summary", "—"),
                    "competitors": [{"name": x.get("name"), "url": x.get("url"), "note": x.get("weaknesses", "")} for x in m.get("competitors", [])[:5]],
                    "saudi_opportunity": m.get("gap_description", "—"), "solution": c.get("potential_solution"),
                    "mvp": "; ".join(f.get("mvp_scope", [])), "technology": _j(f.get("stack", {})),
                    "estimated_cost": f"{f.get('mvp_cost_sar_low')}–{f.get('mvp_cost_sar_high')} SAR + {f.get('monthly_run_cost_sar')}/month",
                    "complexity": f.get("complexity", "MODERATE"), "revenue_model": c.get("business_model"),
                    "first_customer_strategy": "—", "expansion": "—", "risks": f.get("blockers", []),
                    "unknowns": c.get("unknowns", []), "evidence_quality": "MEDIUM" if p.get("someone_pays_now") == "YES" else "LOW",
                    "sources": [e.get("url") for e in c.get("evidence", [])[:6]]})
    return out
