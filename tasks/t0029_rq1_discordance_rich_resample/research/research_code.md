---
spec_version: "1"
task_id: "t0029_rq1_discordance_rich_resample"
research_stage: "code"
tasks_reviewed: 5
tasks_cited: 5
libraries_found: 4
libraries_relevant: 2
date_completed: "2026-05-03"
status: "complete"
---
# Research Code — t0029 RQ1 Discordance-Rich Resample

## Task Objective

Inventory the prior-task code that t0029 will reuse to run a paired arm-A vs arm-B resample under
the locked $35 cap, and identify any ambiguities before writing the plan and harness.

## Library Landscape

The relevant libraries from prior tasks are:

* `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/`
  — t0021 Plan-and-Solve v2 with verbalized `final_confidence`. This is the canonical scope- unaware
  Plan-and-Solve baseline used as the project's "control" arm.
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/plan_and_solve_v3/` — t0027's
  fault-tolerant fork of t0021. Adds bounded 3-attempt plan-parse recovery (clean -> reprompt ->
  JSON-fallback) so a malformed plan no longer aborts a run. Used as t0027 Variant B.
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/matched_mismatch_v2/` — t0027
  Variant C wrapper that delegates to plan_and_solve_v3 and applies adversarial granularity
  perturbation. Out of scope for t0029.
* `tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/` — description-only
  library (no Python source file in the asset). The runtime matched_mismatch_v1 code lives in
  `tasks/t0010_matched_mismatch_library/code/`.

The "scope-aware" arm in t0026/t0027 is `a-scope-aware`, implemented in
`tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/` and reused by reference in t0027 (the
`abc-rerun-a-reused` predictions asset is a pointer back to t0026 outputs). t0029 will keep that
pattern — reuse the t0027 reused-A asset rather than re-running the scope-aware agent.

## Key Findings

### Discordance is the binding constraint, not raw success rate

[t0027] reported A-vs-B discordant pairs of 6/130 (4.6% of paired instances), with the McNemar
exact-binomial p-value pinned at 1.0 because both arms succeeded on disjoint subsets of comparable
size. To reject the no-difference null at Bonferroni alpha=0.025 with reasonable power we need on
the order of 30 discordant pairs. Empirically that means roughly 650 paired instances if the 4.6%
discordance rate holds, well beyond t0029's $35 cap. The plan therefore pre-registers a *partial
verdict + power caveat* abort rule rather than a guarantee of statistical resolution.

### Parser hardening from t0027 carried through cleanly

[t0027] introduced `plan_and_solve_v3` with a bounded 3-attempt plan-parse recovery (clean →
reprompt → JSON-fallback). Across 130 instances the `raised_malformed_plan_error` field was 0 for
both Variant B and Variant C. This means t0029 can reuse `plan_and_solve_v3` verbatim and does not
need to budget remediation time for parser regressions, freeing the engineering time to focus on the
cap guardrail and discordance bookkeeping.

### t0026's three-variant pre-pass is the source of pairing — and it is expensive

[t0026] ran `a-scope-aware`, `b-plan-and-solve`, and `c-mismatched` on 147 instances; the paired
manifest of 130 instances is the intersection where all three judges produced non-null verdicts.
t0029 cannot cheaply expand the paired set by re-running t0026's three-variant pre-pass. Running A
and B directly on new instances and treating them as their own paired data is feasible: the
intersection rule degenerates to "A and B both produced a non-null verdict on the same instance,"
which is the only condition McNemar requires. This skips the expensive third variant entirely.

### Variant labeling is inverted between t0027 and the t0028 brainstorm

[t0027] inherits its labels from [t0026]: Variant A = scope-aware (treatment), Variant B =
plan-and-solve (control). The t0028 brainstorm session 8 description for t0029 calls "arm A" the
Plan-and-Solve baseline and "arm B" the scope-aware ReAct. The two namings reverse A and B. To
preserve the reused t0027 predictions assets without renaming files we adopt t0027's labeling
internally and relabel only in the final writeup. Implementers must check this convention before
reading any predictions JSONL.

### Cost per instance is dominated by the scope-aware pre-pass we are skipping

[t0027] total spend was $20.7631 across 130 paired instances × 2 variants (A reused free + B and C
fresh), so per-instance per-variant cost is ~$0.08. For t0029 the only paid work is the new B and
new A runs on expansion instances; reusing t0027's 130 paired predictions adds zero spend. At ~$0.16
per new paired instance, the $35 cap admits at most ~218 new paired instances, so the combined
sample ceiling is ~348 paired instances assuming no batch hits the cap mid-flight.

## Reusable Code and Assets

### Harness — `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/`

* `run_abc_rerun.py` — orchestrator. Subcommands `--paired-manifest`, `--smoke <variant>`,
  `--full <variant>`. Concurrent execution via `ThreadPoolExecutor` (line 429), per-stream hard stop
  at `PER_STREAM_HARD_STOP_USD = $25` (line 106) checked at line 478. Per-instance worker
  `_process_one_instance` at line 248 records cost via `local_tracker` after every model call (line
  332).
* `planandsolve_v3.py` — `PlanAndSolveAgentV3.run(problem)` at line 299; bounded 3-attempt
  plan-parse recovery.
* `matched_mismatch_v2.py` — `MatchedMismatchV2Agent.run(problem, annotation)` at line 188;
  adversarial granularity perturbation at lines 66-77. Out of scope for t0029.
* `instance_loader.py` — `load_instances()` at line 159 returns `list[Instance]` with
  `instance_id, subset, problem_text, gold` for SWE-bench, taubench, FrontSci.
* `anthropic_shim.py` — `make_model_call()` at line 229 with retry; `CostTracker.record()` updates
  `cost_usd` after every API call. Auth via `anthropic.Anthropic()` at line 164 which reads
  `ANTHROPIC_API_KEY` from env.
* `judge.py` — Sonnet judge for evaluating final answers against gold.
* `paths.py` — `MODEL_UNDER_TEST = "claude-sonnet-4-6"`,
  `JUDGE_MODEL_PRIMARY = "claude-sonnet-4-6"`, predictions paths.
* `mcnemar.py`, `calibration.py`, `make_result_charts.py` — analysis utilities reusable for step 12
  (results).

### Predictions assets to reuse

`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/`:

* `abc-rerun-a-reused/files/pointer.json` — pointer back to t0026's `a-scope-aware` predictions on
  130 paired instances.
* `abc-rerun-b/files/predictions_variant_b.jsonl` — 130 rows with fields
  `instance_id, subset, variant, final_answer, final_confidence, cost_usd, trajectory_path, judge_sonnet_success, judge_sonnet_rationale, plan_parser_recovery_path, plan_parser_attempts, raised_malformed_plan_error`.

### Paired manifest

`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json` lists the 130 instance
ids: SWE-bench 20, FrontSci 26, taubench 84. Computed as the intersection of t0026's three-variant
predictions where `judge_sonnet_success` is non-null.

### t0027 results headlines

* Variant A reused (= scope-aware): success rate **4.62%** (6/130).
* Variant B (`plan_and_solve_v3`, scope-unaware): success rate **4.62%** (6/130), ECE 0.336.
* Paired McNemar A vs B: discordant 6 / 6, p = 1.0 (do_not_reject under Bonferroni alpha=0.025).
* Total task cost: $20.7631.
* Parser robustness: `raised_malformed_plan_error` = 0/130 for both B and C.

### Variant labeling ambiguity (KEY OPEN ITEM)

t0027 inherits its variant labels from t0026 where:

* **Variant A** = `a-scope-aware` (scope-conditioned plan-and-solve, "treatment").
* **Variant B** = `b-plan-and-solve` then `plan_and_solve_v3` in t0027 (scope-unaware "control").
* **Variant C** = `c-mismatched` then `matched_mismatch_v2` (counter / adversarial).

t0029's task description (from t0028 brainstorm session 8) describes:

* **arm A** = "Plan-and-Solve baseline" (= t0027 Variant B by content).
* **arm B** = "scope-aware ReAct" (= t0027 Variant A by content).

The two namings reverse A and B. To avoid invalidating reused t0027 predictions, t0029 will
internally adopt **t0027's variant naming** (A = scope-aware, B = scope-unaware) and relabel only in
the final writeup so the reader understands which is the project's "treatment" (scope-aware) and
which is the "control" (Plan-and-Solve baseline).

## Lessons Learned

* `_compute_paired_manifest()` derives the paired set from t0026 predictions intersection. To expand
  beyond 130, we either need new t0026 predictions (extra cost) or a different paired source —
  t0010's library does NOT contain a separate paired list.
* There is no separate file containing pre-paired instances beyond the 130 in t0027. Expanding the
  paired sample requires either re-running t0026's three-variant pre-pass on new instances OR
  running A and B directly on new instances and using both as their own paired data. The latter is
  feasible and cheaper because it skips the t0026 pre-pass.
* t0027's per-stream cap ($25) was checked at line 478 of `run_abc_rerun.py` between batches. We can
  copy that pattern but tighten the cap to $35 cumulative across BOTH variants (cumulative_cost_usd
  > = 35.00 -> exit cleanly).
* t0027's parser hardening worked: `raised_malformed_plan_error` = 0 across 130 instances. Reusing
  `plan_and_solve_v3` is safe with no further fault-tolerance work required.
* The Anthropic auth is implicit via `anthropic.Anthropic()` reading `ANTHROPIC_API_KEY` from the
  environment. Step 9 will verify the env var is set before issuing any API call; if missing, write
  an intervention file and halt cleanly without spending.

## Recommendations for This Task

1. **Reuse the 130 paired instances** from t0027 verbatim — load A predictions from
   `abc-rerun-a-reused` (pointer to t0026 `a-scope-aware`) and B predictions from `abc-rerun-b`. No
   new API spend on these.
2. **Expand by running A and B directly** on additional instances drawn from
   `instance_loader.load_instances()`, prioritising FrontSci and taubench where t0027 showed B has a
   non-zero success rate (so A vs B discordance is more likely to be observed).
3. **Cap guardrail**: implement a `cumulative_cost_usd >= 35.00` check inside the harness. Check it
   after every batch (N=8 instances) and exit cleanly if the cap is hit. Persist
   `results/costs.json` after each batch so a partial verdict is always derivable from disk.
4. **Stratification**: target adding up to ~100 frontsci + ~80 taubench + ~20 swebench new
   instances, knowing the cap may bind earlier. The McNemar denominator is the union of t0027's 130
   \+ newly-run paired count.
5. **Judging**: reuse `judge.py` from t0027 — same model, same prompt, same gold-comparison rule.

## Task Index

The full task list is enumerated via
`uv run python -u -m arf.scripts.aggregators.aggregate_tasks --format markdown --detail short`. The
five tasks cited in the body of this document are listed below.

### [t0010]

* **Task ID**: `t0010_matched_mismatch_library`
* **Name**: Matched-mismatch library v1
* **Status**: completed
* **Relevance**: registered the description-only `matched_mismatch_v1` library; confirms that no
  separate paired-instance file exists outside t0026/t0027, so t0029 must derive expansion pairs by
  running A and B directly on new instances rather than re-using a t0010 manifest.

### [t0021]

* **Task ID**: `t0021_plan_and_solve_v2_with_final_confidence`
* **Name**: Plan-and-Solve v2 with verbalized final confidence
* **Status**: completed
* **Relevance**: source of the canonical scope-unaware Plan-and-Solve baseline that t0027's
  `plan_and_solve_v3` forks; defines the `final_confidence` field that t0029 will preserve in its
  predictions schema for downstream calibration analysis.

### [t0026]

* **Task ID**: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`
* **Name**: Phase 2 ABC runtime on N=147 for RQ1/RQ5
* **Status**: completed
* **Relevance**: produced the original `a-scope-aware`, `b-plan-and-solve`, and `c-mismatched`
  predictions on 147 instances; t0029 reuses its `a-scope-aware` predictions verbatim through the
  t0027 `abc-rerun-a-reused` pointer.

### [t0027]

* **Task ID**: `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
* **Name**: Phase 2.5 ABC rerun with fixed B and C
* **Status**: completed
* **Relevance**: provides the harness, judge, paired manifest of 130 instances, and
  `plan_and_solve_v3` library that t0029 reuses end-to-end; its results define both the priors for
  expected discordance and the variant-labeling convention that t0029 inherits.

### [t0028]

* **Task ID**: `t0028_brainstorm_results_8`
* **Name**: Brainstorm session 8 (RQ1 follow-up planning)
* **Status**: completed
* **Relevance**: locked the t0029 task spec including the $35 cap, the discordance-rich resample
  framing, and the partial-verdict abort rule; this document's variant-labeling resolution exists to
  reconcile the t0028 description with t0027's predictions assets.

## References

* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/run_abc_rerun.py` lines 100-200, 248, 332,
  478\.
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/anthropic_shim.py` lines 164, 229-266.
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/paths.py` line 106.
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json`.
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_summary.md`.
* `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/`.
* `tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/`.
