"""CLI:
  python -m hunter selftest            offline orchestration test (mock backend, free)
  python -m hunter selftest --live     small real run with real agents
  python -m hunter run                 full research run (all agents)
  python -m hunter run --budget 30 --parallel 4 --agents problem_hunter,b2b_hunter
"""
from __future__ import annotations

import argparse
import shutil
import sys

from .config import load_config


def main() -> int:
    ap = argparse.ArgumentParser(prog="hunter")
    sub = ap.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("selftest")
    st.add_argument("--live", action="store_true")
    rn = sub.add_parser("run")
    rn.add_argument("--budget", type=float, help="max total USD for this run")
    rn.add_argument("--parallel", type=int, help="max parallel agent processes")
    rn.add_argument("--agents", help="comma-separated discovery agents (default: all)")
    rn.add_argument("--candidates", type=int, help="candidate limit for validation funnel")
    rn.add_argument("--run-id")
    args = ap.parse_args()

    if shutil.which("claude") is None and (args.cmd == "run" or getattr(args, "live", False)):
        print("ERROR: `claude` CLI not found on PATH. Install Claude Code and authenticate first.", file=sys.stderr)
        return 2

    if args.cmd == "selftest":
        from . import selftest
        return 0 if (selftest.run_live() if args.live else selftest.run_offline()) else 1

    overrides: dict = {"run": {}}
    if args.budget:
        overrides["run"]["max_total_budget_usd"] = args.budget
    if args.parallel:
        overrides["run"]["max_parallel_agents"] = args.parallel
    if args.candidates:
        overrides["run"]["candidate_limit"] = args.candidates
    cfg = load_config(overrides=overrides)
    from .orchestrator import Orchestrator
    orch = Orchestrator(cfg, run_id=args.run_id, mode="full",
                        discovery_agents=args.agents.split(",") if args.agents else None)
    summary = orch.run()
    print(f"\nFinal report: {orch.report_path}")
    print(summary["counts"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
