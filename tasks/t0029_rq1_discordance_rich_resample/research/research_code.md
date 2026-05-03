# Research Code — t0029 RQ1 Discordance-Rich Resample

## Objective

Inventory the prior-task code that t0029 will reuse to run a paired arm-A vs arm-B resample under
the locked $35 cap, and identify any ambiguities before writing the plan and harness.

## Background

t0029 is a power-driven follow-up to t0027 Phase 2.5. t0027 ran 130 paired instances with three
variants (A, B, C) and produced an underpowered McNemar verdict for RQ1 (6 vs 6 discordant, p=1.0).
t0029 must close the power gap by adding more discordant pairs under a hard cap, reusing t0027's
harness.

## Methodology Review

### t0027 harness (`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/`)

* `run_abc_rerun.py`: orchestrator with subcommands `--paired-manifest`, `--smoke <variant>`,
  `--full <variant>`. Concurrent execution via `ThreadPoolExecutor` (line 429), per-stream hard stop
  at `PER_STREAM_HARD_STOP_USD = $25` (line 106) checked at line 478, per-instance
  `_process_one_instance` at line 248. Cost recorded after every model call inside
  `_process_one_instance` via `local_tracker` (line 332).
* `planandsolve_v3.py`: fault-tolerant fork of t0021's plan-and-solve v2 with bounded 3-attempt
  plan-parse recovery. Entry point `PlanAndSolveAgentV3.run(problem)` at line 299.
* `matched_mismatch_v2.py`: wraps `PlanAndSolveAgentV3` and applies the adversarial granularity
  perturbation at lines 66-77. Entry point `MatchedMismatchV2Agent.run(problem, annotation)` at line
  188\.
* `instance_loader.py`: `load_instances()` at line 159 loads SWE-bench, taubench, and FrontSci
  problems with stratified difficulty.
* `anthropic_shim.py`: `CostTracker.record()` updates `cost_usd` after each API call;
  `make_model_call()` (line 229) wraps the Anthropic transport with retry logic.
* `judge.py`: Sonnet judge for evaluating final answers against gold.
* `paths.py`: defines `MODEL_UNDER_TEST = "claude-sonnet-4-6"`,
  `JUDGE_MODEL_PRIMARY = "claude-sonnet-4-6"`, plus prediction file paths.

### t0027 predictions assets

`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/`:

* `abc-rerun-a-reused/files/pointer.json` — pointer back to t0026's `a-scope-aware` predictions.
* `abc-rerun-b/files/predictions_variant_b.jsonl` — 130 rows with fields
  `instance_id, subset, variant, final_answer, final_confidence, cost_usd, trajectory_path, judge_sonnet_success, judge_sonnet_rationale, plan_parser_recovery_path, plan_parser_attempts, raised_malformed_plan_error`.
* `abc-rerun-c/files/predictions_variant_c.jsonl` — same schema.

### t0027 paired manifest

`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json` lists the 130 instance
ids with per-subset counts: SWE-bench 20, FrontSci 26, taubench 84. Computed as the intersection of
three t0026 predictions JSONL records where `judge_sonnet_success` is non-null.

### t0027 results highlights

* Variant A (reused from t0026 `a-scope-aware`): success rate **4.62%** (6/130).
* Variant B (`plan_and_solve_v3`): success rate **4.62%** (6/130), ECE 0.336.
* Variant C (`matched_mismatch_v2`): success rate **5.38%** (7/130), ECE 0.374.
* Paired McNemar A vs B: discordant 6 / 6, p = 1.0.
* Total task cost: $20.7631.
* Parser robustness: `raised_malformed_plan_error` = 0/130 for both B and C.

### Variant labeling ambiguity (KEY OPEN ITEM)

t0027 inherits its variant labels from t0026 where:

* **Variant A** = `a-scope-aware` (scope-conditioned plan-and-solve, "treatment" arm)
* **Variant B** = `b-plan-and-solve` then `plan_and_solve_v3` in t0027 (scope-unaware "control")
* **Variant C** = `c-mismatched` then `matched_mismatch_v2` (counter / adversarial)

t0029's task description (from t0028 brainstorm session 8) describes:

* **arm A** = "Plan-and-Solve baseline" (= t0027 Variant B by content)
* **arm B** = "scope-aware ReAct" (= t0027 Variant A by content, possibly different agent)

The two namings reverse A and B. To avoid invalidating reused t0027 predictions, t0029 will
internally adopt **t0027's variant naming** (A = scope-aware, B = scope-unaware) and clearly relabel
in the final results writeup so the reader understands which is the project's "treatment"
(scope-aware) and which is the "control" (Plan-and-Solve baseline).

## Key Findings

* The t0027 harness can be reused almost as-is. We only need a thin t0029 driver that:
  1. Picks a discordance-rich extension sample,
  2. Sets `PER_STREAM_HARD_STOP_USD = $35` (or wraps the cap differently),
  3. Runs only A and B (skip C),
  4. Reuses t0027 predictions for the 130 already-paired instances and only re-runs new instances
     that t0027 did not cover.
* `_compute_paired_manifest()` derives the paired set from t0026 predictions intersection. To expand
  beyond 130, we either need new t0026 predictions (extra cost) or a different paired source —
  t0010's library does NOT contain a separate paired list; it only describes the v1 matched-mismatch
  agent.
* **Important**: there is no separate file containing pre-paired instances beyond the 130 in t0027.
  Expanding the paired sample requires either re-running t0026's three-variant pre-pass on new
  instances OR running A and B directly on new instances and using both as their own paired data.
  The latter is feasible and cheaper because it skips the t0026 pre-pass.

## Recommended Approach

1. **Reuse the 130 paired instances** from t0027 verbatim — load A predictions from
   `abc-rerun-a-reused` (pointer to t0026 `a-scope-aware`) and B predictions from `abc-rerun-b`. No
   new API spend on these.
2. **Expand by running A and B directly** on additional instances drawn from
   `instance_loader.load_instances()` (the full benchmark population), prioritising FrontSci and
   taubench where t0027 showed B has a non-zero success rate (so A vs B discordance is more likely
   to be observed).
3. **Cap guardrail**: implement a `cumulative_cost_usd >= 35.00` check inside the harness. Check it
   after every batch (every N=8 instances) and exit cleanly if the cap is hit. Persist
   `results/costs.json` after each batch so a partial verdict is always derivable from disk.
4. **Stratification**: target adding ~100 frontsci + ~80 taubench + ~20 swebench new instances,
   knowing the cap may bind earlier. The McNemar denominator is the union of t0027's 130 + newly-run
   paired count.
5. **Judging**: reuse `judge.py` from t0027 — same model, same prompt, same gold-comparison rule.

## API key configuration

Anthropic auth is via the standard `ANTHROPIC_API_KEY` environment variable consumed by
`anthropic.Anthropic()` in `anthropic_shim.py:164`. The repo's `.envrc` sources the venv but does
not pin the key. The user must have `ANTHROPIC_API_KEY` set in their shell or `.env`. This will be
verified at the start of step 9 implementation; if absent, an `intervention/` file is written and
the task halts cleanly.

## References

* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/run_abc_rerun.py:100-200` (paired manifest
  computation and per-instance runner).
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/anthropic_shim.py:164,229-266` (auth and
  cost tracking).
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/paths.py:106`
  (`PER_STREAM_HARD_STOP_USD = 25.0`).
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json` (130 instance ids).
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_summary.md` (per-subset rates,
  McNemar verdict).
* `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/`
  (canonical arm-A scope-unaware library).
* `tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/` (description-only; no
  paired-instance file).
