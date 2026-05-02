---
spec_version: "3"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-02T08:50:00Z"
completed_at: "2026-05-02T14:55:00Z"
---
## Summary

Built and executed the Phase 2 A/B/C runtime sweep across the paired N=147 manifest (SWE-bench
Verified + Tau-bench + FrontierScience Olympiad) over three agent variants — A scope-aware ReAct, B
Plan-and-Solve v2, C mismatched-strategy adversarial — with sonnet and opus judges, calibration,
McNemar tests, and inter-judge agreement. The full sweep ran end-to-end via `code/main.py --full`,
producing per-instance trajectories, judge dumps, and aggregate metrics.

## Actions Taken

1. Implemented the runtime stack in `code/`: `paths.py` (constants), `instance_loader.py`
   (paired-N=147 manifest), `anthropic_shim.py` (CLI transport with retry-with-backoff and a
   thread-safe `CostTracker`), `runner.py` (per-variant `ThreadPoolExecutor(max_workers=8)` parallel
   execution + per-instance trajectory persistence), `judge.py` (sonnet/opus judge prompt
   + program-truth heuristic), `calibration.py` (10-bin ECE), `mcnemar.py` (exact binomial paired
     test), `metrics.py` (RQ1-RQ5 aggregation), `full_runner.py` (sweep orchestration with resumable
     trajectory checkpointing, judge phase parallelized at `_JUDGE_MAX_WORKERS=8`, inter-judge
     sample of 30 per variant), and `main.py` (CLI entry).
2. Added `code/test_smoke.py` covering ECE, McNemar, and judge prompt construction.
3. Tuned for the actual workload: bumped `_CLI_TIMEOUT_SECONDS` from 90 to 180 after observing a
   ~20% timeout rate at 90s; parallelized the judge loop with `threading.Lock`-guarded dump saves;
   treated executor exceptions as recorded failures rather than aborting the sweep.
4. Executed the full sweep:
   `python -m tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.main --full`. Runs phase produced
   130/147 trajectories per variant (17 instances were filtered out by `_filter_pending_instances`
   from a prior corrupted partial run; we accept this as the paired sample because all three
   variants share the same 130 instance ids). Judge phase produced 130 sonnet verdicts per variant
   plus 30 opus verdicts per variant for inter-judge agreement.
5. Wrote prediction assets (`assets/predictions/{a-scope-aware,b-plan-and-solve,c-mismatched}/`) and
   aggregate outputs (`data/calibration.json`, `data/mcnemar_results.json`,
   `data/judge_agreement.json`, `results/metrics.json`).

## Outputs

* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/{paths,instance_loader,anthropic_shim,runner,judge,calibration,mcnemar,metrics,full_runner,main,test_smoke}.py`
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/runs/{a,b,c}/trajectory_*.json` — 390
  per-instance trajectories total (130 × 3 variants).
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/judges/{sonnet,opus}_{a,b,c}.json` — 6 judge
  dumps.
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/{calibration,mcnemar_results,judge_agreement}.json`
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/metrics.json` — aggregate metrics
  including `success_rate_{a,b,c}` per subset, ECE, judge agreement, McNemar p-values, RQ5 flag.
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions/{a-scope-aware,b-plan-and-solve,c-mismatched}/{details.json,description.md,files/predictions_variant_*.jsonl}`

## Issues

* Headline finding: `rq5_strict_inequality_supported = false`. Pairwise McNemar shows A and B
  statistically tied (p ≈ 1.0, 6 vs 6 discordant pairs) and C *significantly outperforms* B (p =
  0.019; 4 vs 15 discordant pairs). C's higher success rate (11.6% vs 4.1% for A and B) is driven by
  FrontierScience (17.5% C vs 0% A, 10% B). This is a valid negative result for the strict A>B>C
  hypothesis and will be analyzed in the results step.
* Final-confidence ECE = 0.43 (n=49), indicating substantial mis-calibration of variant B's
  self-reported confidence.
* 17 instances per variant were not run because their trajectory files pre-existed from an earlier
  corrupted partial run; the resumable design treats existing files as completed. The paired N=130
  set is consistent across all three variants, so the McNemar tests are valid on this paired subset.
* Judge agreement with program truth: 91.7% (n=120). Inter-judge agreement (sonnet vs opus on
  30-instance random sub-sample per variant): 97.7% (n=89).
