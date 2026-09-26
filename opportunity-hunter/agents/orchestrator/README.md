# ORCHESTRATOR (master agent / control plane)

The orchestrator is implemented as deterministic Python code in `hunter/orchestrator.py`, not as an LLM prompt.
This is deliberate:

- It must reliably enforce stage ordering, budgets, retries, parallelism and failure isolation — things code does
  better than a language model.
- Every judgement call (merging duplicates, validating claims, killing ideas, synthesising opportunities) is delegated
  to a real, separate LLM agent process (`claude -p`), whose output is schema-validated before the orchestrator uses it.

Responsibilities (all implemented):
1. Launch discovery agents in parallel (bounded by `max_parallel_agents`).
2. Collect, ID and store signals; exact/near-duplicate removal (`hunter/dedup.py`).
3. Semantic merging + ranking via the CONSOLIDATOR agent (with deterministic fallback if it fails).
4. Launch the 4 validators in parallel over candidate batches.
5. Send validated dossiers to the KILLER agent.
6. Gap detection: collect Killer `missing_info_requests` + orchestrator-detected gaps (e.g. payment UNCLEAR),
   dispatch the GAP_RESEARCHER, then re-run the Killer in `final_round` mode.
7. Send survivors + rejected + backlog to the OPPORTUNITY_SYNTHESIZER (deterministic fallback if it fails).
8. Render `reports/final_report.md`, write run statistics, and record research limitations.
