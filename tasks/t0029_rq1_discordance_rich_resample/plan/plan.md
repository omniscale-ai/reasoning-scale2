---
spec_version: "2"
task_id: "t0029_rq1_discordance_rich_resample"
date_completed: "2026-05-03"
status: "complete"
---
# Plan — t0029 RQ1 Discordance-Rich Paired Resample

## Objective

Run a discordance-rich paired resample of arm A (Plan-and-Solve baseline) and arm B (scope-aware
ReAct) on claude-sonnet-4-6, accumulate enough discordant pairs to deliver a McNemar verdict on RQ1
("does scope-aware reasoning beat the scope-unaware baseline?"), and stop cleanly the moment
cumulative API spend reaches $35.00. Done = either (a) a full RQ1 verdict at >= 30 discordant pairs
with a McNemar exact-binomial p-value and 95% CI, or (b) a partial verdict with explicit power
caveat if the cap binds first; in both cases the predictions for both arms are saved as v2-compliant
assets so t0030 (RQ4 stratification) can run with zero new API spend.

## Task Requirement Checklist

The task text is `task_description.md`. The operative instructions, quoted verbatim:

> Resample paired A vs B to reach >=30 discordant pairs for an RQ1 McNemar verdict; hard $35 cap;
> partial verdict on cap.
> 
> ...
> 
> **Cap**: $35.00 USD. Track spend live in `results/costs.json` after each batch of API calls and in
> the harness. The budget verificator must show this task does not exceed $35 in
> `effective_budget_limit_usd`.
> 
> **Abort rule**: if the cap is hit (>= $35.00 cumulative) and the running discordant-pair count is
> < 30, halt all further API calls and proceed directly to the analysis step. Report a partial RQ1
> verdict ...
> 
> Goal: reach >= 30 discordant pairs between A and B.
> 
> Approach (pre-registered, in priority order):
> 1. Stratified resample from t0027's 130 paired instances: prioritise re-running on the 12
>    discordant pairs from t0027 plus instances flagged by t0027's recovery distribution as
>    "unknown" (B=29, C=33) where one arm's outcome is uncertain.
> 2. Expand within-subset coverage: draw additional paired instances from
>    `t0010_matched_mismatch_library` first from frontsci, then taubench, then SWE-bench Verified.
> 3. Concentrate on harder difficulty bands: t0027's per-subset table suggests A=0 outside
>    SWE-bench, so RQ1 discordance is entirely driven by B!=0 outcomes; sample with bias toward
>    instances where B is more likely to succeed and A more likely to fail.
> 
> ...
> 
> Deliverables:
> * `results/results_summary.md` and `results/results_detailed.md` with the McNemar verdict (full or
>   partial).
> * `results/metrics.json` with `mcnemar_b_count`, `mcnemar_c_count`, `mcnemar_p_value`,
>   `mcnemar_effect_size`, `mcnemar_ci_lower`, `mcnemar_ci_upper`, `discordant_pairs_total`,
>   `paired_n_total`, plus per-subset breakdowns.
> * `results/predictions/arm_a/` and `results/predictions/arm_b/` predictions assets covering all
>   paired instances actually run.
> * `results/suggestions.json` describing follow-up tasks ...
> * Per-subset stratification table (also reused by t0030).

Decomposed checklist:

* **REQ-1** — Run arm A (Plan-and-Solve baseline) on the chosen instance pool using
  `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/`
  with claude-sonnet-4-6. Evidence: predictions JSONL with one row per instance.
* **REQ-2** — Run arm B (scope-aware ReAct) on the same pool using the t0027 fault-tolerant
  scope-aware library (the runtime is in `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/`,
  reused via the `abc-rerun-a-reused` pointer) with the same model and decoding settings. Evidence:
  predictions JSONL with one row per instance.
* **REQ-3** — Reuse t0027's existing 130 paired predictions verbatim where both arms have a usable
  verdict; only re-run instances where t0027 has no usable result for that arm. Evidence: the merged
  predictions assets contain the full union with each row's `source` field set to either
  `t0027_reused` or `t0029_fresh`.
* **REQ-4** — Implement a hard `cumulative_cost_usd >= 35.00` guardrail inside the harness; check it
  after every batch of N=8 instances and exit cleanly if true. Evidence: a unit-style log line
  `cap_hit_at_batch=k, cumulative_cost=$x.xx` and a non-zero exit when the cap binds.
* **REQ-5** — Persist `results/costs.json` after every batch so a partial verdict is always
  derivable from disk. Evidence: file mtime updates batch-by-batch and contents include
  `total_cost_usd`, `paired_n_completed`, `discordant_count_running`.
* **REQ-6** — Pre-register the sampling rule and the abort condition in this plan before any API
  call. Evidence: this Approach + Step by Step + Sampling Strategy sections.
* **REQ-7** — Stratify sampling by subset (frontsci > taubench > SWE-bench Verified) per the task
  text. Evidence: the harness selects new instances in that order until either the per-subset target
  is reached or the cap binds.
* **REQ-8** — Compute the McNemar paired exact-binomial test (b vs c on the 2x2 table) and emit
  `mcnemar_b_count`, `mcnemar_c_count`, `mcnemar_p_value`, `mcnemar_effect_size` (b/(b+c) and odds
  ratio), `mcnemar_ci_lower`, `mcnemar_ci_upper` (Wilson CI on b/(b+c)), `discordant_pairs_total`,
  `paired_n_total`. Evidence: `results/metrics.json` contains all eight fields plus per-subset
  variants.
* **REQ-9** — Produce the per-subset stratification table that t0030 will reuse, written to
  `results/results_detailed.md` and embedded as an `images/per_subset_stratification.png` chart.
  Evidence: file present and chart rendered.
* **REQ-10** — Save predictions assets at `assets/predictions/arm-a/` and
  `assets/predictions/arm-b/` (predictions spec v2; slug regex requires hyphens, not underscores).
  The `task_description.md` calls these directories `results/predictions/arm_a` and
  `results/predictions/arm_b` — those are deliverable references inside results, not the canonical
  asset path; the asset path is `assets/predictions/<slug>/files/predictions.jsonl` per the asset
  spec. Evidence: both folders exist with `details.json`, `description.md`, and a populated
  `files/predictions.jsonl`.
* **REQ-11** — Emit `results/suggestions.json` with follow-up tasks for RQ2 calibrator, RQ3
  instrumentation, RQ5 C-arm rebuild, and (conditional) a t0031 continuation if the cap bound before
  30 discordant pairs. No replacement task is launched in this wave. Evidence: file written and
  verificator passes.
* **REQ-12** — Verify before any paid call that `ANTHROPIC_API_KEY` is present in the environment;
  if absent, write `intervention/missing_api_key.md` and halt cleanly without spending. Evidence:
  the implementation step's preflight log entry shows the env-var check.

**Variant labeling note (binding for the implementation)**: t0027 inherits its variant labels from
t0026 with Variant A = scope-aware (treatment) and Variant B = Plan-and-Solve baseline (control).
The t0028 brainstorm description for t0029 inverts this: t0028 arm A = Plan-and-Solve baseline,
t0028 arm B = scope-aware ReAct. To preserve compatibility with reused predictions assets without
renaming files, the harness uses the **t0028 (task-description) naming** in all new outputs (asset
folders `arm-a` = baseline, `arm-b` = scope-aware) and applies the inverse mapping when reading
t0027's predictions: t0027 `abc-rerun-a-reused` -> arm B, t0027 `abc-rerun-b` -> arm A. Every code
path that reads or writes a "variant" field must call this mapping out in a comment.

## Approach

We **reuse rather than rebuild**. The t0027 harness
(`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/`) already has a working concurrent runner
(`run_abc_rerun.py`), a fault-tolerant Plan-and-Solve V3 agent (`planandsolve_v3.py`), a Sonnet
judge (`judge.py`), an instance loader (`instance_loader.py`), an Anthropic shim with a
`CostTracker` that records spend after every API call (`anthropic_shim.py`), and analysis utilities
(`mcnemar.py`, `calibration.py`, `make_result_charts.py`). The t0027 research code research at
`research/research_code.md` documents these surfaces with line numbers. t0029 copies the relevant
files into its own `code/` directory (cross-task imports are forbidden by project rule 9) and
adapts:

1. The cap constant goes from `PER_STREAM_HARD_STOP_USD = $25` to a single
   `CUMULATIVE_TASK_CAP_USD = $35.00` checked across both arms together (not per-stream).
2. The orchestrator (`run_resample.py`) keeps the t0027 batch-runner skeleton but adds a pre-pass
   that constructs the paired instance pool from (a) t0027's 130 paired instances reused verbatim
   and (b) new instances drawn by stratified expansion.
3. The McNemar/CI computation is extended to emit the metric fields enumerated in REQ-8.

**Why rebuild not extend in place**: per project rule 9 ("tasks must not import from other tasks'
`code/` directories"), we cannot import t0027 code at runtime; we copy it. Copying makes the cap
constant and sampling logic local to t0029, which is also the right unit for the budget-verificator
check.

**Alternatives considered**:

* *Option A: re-run t0026's three-variant pre-pass on a larger N to derive a fresh paired manifest.*
  Rejected — t0026's three-variant pre-pass costs ~$0.24/instance/three-variants, which would burn
  the entire $35 cap on ~145 new pre-pass instances and leave nothing for the paired A vs B run that
  actually answers RQ1.
* *Option B: skip the t0027 reused pool and run A and B on a fresh 200-instance pool.* Rejected —
  the t0027 pool is free (predictions exist, cost = $0), and discarding it shrinks the combined
  sample by 130 paired instances for no benefit.
* *Option C: run only on frontsci where t0027 showed B has a non-zero success rate, ignoring
  taubench and SWE-bench.* Rejected — REQ-9 requires a per-subset stratification table that t0030
  reuses; restricting to one subset breaks that downstream contract. We bias *order* of expansion by
  subset (frontsci first, then taubench, then SWE-bench) but do not exclude subsets entirely.

**Task types**: `task.json` lists `experiment-run` and `comparative-analysis`. Both apply: the task
runs paid LLM experiments and reports a comparative McNemar verdict. The `experiment-run` Planning
Guidelines drive the cap-and-abort design and the per-batch cost checkpointing; the
`comparative-analysis` Planning Guidelines drive the per-subset breakdown and the McNemar test
choice.

## Cost Estimation

Hard cap: **$35.00**. Per-instance per-variant cost from t0027 was approximately **$0.08** (130
paired instances x 2 paid variants for $20.7631 over the full task). Reusing t0027's 130 paired
instances costs **$0.00**. New paired instances cost **~$0.16/pair** (one A + one B call plus judge
invocation amortized).

Spending plan, in priority order:

| Bucket | Instances | Variant calls | Est. cost | Notes |
| --- | --- | --- | --- | --- |
| Reuse t0027 paired pool | 130 | 0 | $0.00 | predictions already exist on disk |
| New frontsci pairs | up to 60 | 120 | $9.60 | priority subset (largest t0027 B>0 gap) |
| New taubench pairs | up to 80 | 160 | $12.80 | second priority |
| New SWE-bench pairs | up to 60 | 120 | $9.60 | third priority |
| Judge re-invocations on new pairs | 200 | 200 | $1.60 | $0.008/judge call |
| Buffer for retries / partial batches | — | — | $1.40 | 4% safety margin |
| **Total upper bound** | **330 paired** | **600** | **~$35.00** | cap binds at this point |

The expected discordance rate of 4-9% (t0027 priors) implies a total of 330 paired instances (130
reused + 200 new = 330) yields between **13 and 30 discordant pairs**, with the 30-pair ceiling
reached only if expansion biases successfully amplify discordance. The plan therefore explicitly
anticipates a partial verdict.

## Step by Step

Milestone 1: harness setup (no API spend).

1. **[CRITICAL] Copy t0027 harness files into `code/`.** Copy
   `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/{run_abc_rerun.py,planandsolve_v3.py,instance_loader.py,anthropic_shim.py,judge.py,paths.py,mcnemar.py,calibration.py,make_result_charts.py}`
   into `tasks/t0029_rq1_discordance_rich_resample/code/`. Do **not** copy `matched_mismatch_v2.py`
   (out of scope per task description). Rename the orchestrator to `run_resample.py`. Update every
   import path in the copied files to use the `tasks.t0029_rq1_discordance_rich_resample.code.*`
   package root. Run `uv run mypy -p tasks.t0029_rq1_discordance_rich_resample.code` and confirm 0
   errors. Satisfies REQ-1, REQ-2 (sets up the runtime).

2. **Set the cap constant in `paths.py`.** Replace `PER_STREAM_HARD_STOP_USD = 25.00` with
   `CUMULATIVE_TASK_CAP_USD: float = 35.00`. Remove the per-stream cap entirely — the new design
   tracks one shared `cumulative_cost_usd` across both arms. Add `BATCH_SIZE: int = 8` and
   `DISCORDANCE_TARGET: int = 30`. Satisfies REQ-4.

3. **Write `code/load_t0027_paired.py`.** A small loader that reads
   `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-a-reused/files/pointer.json`
   and `.../abc-rerun-b/files/predictions_variant_b.jsonl`, returns `list[ReusedPair]` dataclasses
   with
   `(instance_id, subset, arm_a_success, arm_b_success, arm_a_final_confidence, arm_b_final_confidence, arm_a_judge_rationale, arm_b_judge_rationale)`.
   Apply the variant-label inversion in this loader: the t0027 `abc-rerun-a-reused` rows populate
   `arm_b_*` fields (scope-aware), and the t0027 `abc-rerun-b` rows populate `arm_a_*` fields
   (Plan-and-Solve). The loader emits a single warning per call summarizing the inversion. Inputs:
   t0027 predictions assets. Outputs: `list[ReusedPair]` of length 130. Satisfies REQ-3.

4. **Write `code/sampling.py`.** A pre-registered sampling module that:
   * reads `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json` (130 ids)
     and `instance_loader.load_instances()` for the full instance population,
   * computes the candidate set = full population - t0027's 130 paired ids,
   * orders candidates by subset (frontsci first, then taubench, then SWE-bench), within each subset
     random with a fixed seed `T0029_SEED = 20260503`,
   * exposes `next_batch(n: int) -> list[Instance]` that pops the next `n` candidates from the
     stratified queue. Inputs: t0027 paired manifest, instance loader. Outputs: a generator that
     yields stratified batches. Satisfies REQ-7, REQ-6.

5. **[CRITICAL] Write `code/run_resample.py`.** The orchestrator. Pseudocode:
   * `assert_env_var_present("ANTHROPIC_API_KEY")` — if absent, write
     `intervention/missing_api_key.md` and `sys.exit(0)` (clean exit, no spend). Satisfies REQ-12.
   * Load reused pairs via `load_t0027_paired.py`. Compute initial discordant_count from the reused
     pairs (t0027 had 6 A-wins + 6 B-wins = 12 discordant, after the variant-label inversion the
     counts are unchanged because the inversion is symmetric). Satisfies REQ-3.
   * Initialize `cumulative_cost_usd = 0.0`, `pairs_completed = 130`, `arm_a_rows`, `arm_b_rows`
     from reused pool.
   * Loop: while `cumulative_cost_usd < CUMULATIVE_TASK_CAP_USD` and
     `discordant_count_running < DISCORDANCE_TARGET` and stratified queue is non-empty:
     * Pull a batch of `BATCH_SIZE = 8` new instances from `sampling.next_batch(8)`.
     * For each instance in the batch, in parallel via `ThreadPoolExecutor(max_workers=4)`:
       * Run arm A (PlanAndSolveAgentV3) -> record predictions row with `variant="arm_a"`.
       * Run arm B (scope-aware ReAct via the copy of t0026's runtime) -> record predictions row
         with `variant="arm_b"`.
       * Run Sonnet judge on each arm's `final_answer` against gold; populate `judge_sonnet_success`
         and `judge_sonnet_rationale`.
       * Update `cumulative_cost_usd += local_tracker.cost_usd_for_instance`.
     * After the batch:
       * If both arms produced a valid (non-null) judge verdict: append rows to `arm_a_rows` and
         `arm_b_rows`; update the running 2x2 contingency table; increment paired count.
       * Else: log the failure mode and skip this instance (do not consume against discordance
         target).
       * Persist `results/costs.json` with
         `{total_cost_usd, paired_n_completed, discordant_count_running, batches_completed, last_batch_at_iso}`.
         Satisfies REQ-5.
       * If `cumulative_cost_usd >= CUMULATIVE_TASK_CAP_USD`: log
         `cap_hit_at_batch=k cumulative_cost=$x.xx`, break out of the loop. Satisfies REQ-4.
   * After the loop: write final predictions assets `assets/predictions/arm-a/` and
     `assets/predictions/arm-b/` per the predictions asset specification (`details.json`,
     `description.md`, `files/predictions.jsonl`). Satisfies REQ-10.
   * Write a final `results/costs.json` and a `results/run_log.md` summarizing the loop's control
     state. Inputs: env var `ANTHROPIC_API_KEY`, t0027 reused pairs, instance population. Outputs:
     `assets/predictions/arm-a/`, `assets/predictions/arm-b/`, `results/costs.json`,
     `results/run_log.md`. Satisfies REQ-1, REQ-2, REQ-3, REQ-4, REQ-5, REQ-7, REQ-10, REQ-12.

   **Validation gate (preflight smoke test)**: before kicking off the full loop, run the
   orchestrator with `--limit 4` (one batch of 4 instances, ~ $0.32). If both arms produce non-null
   judge verdicts on at least 2 of 4 and the cap+costs file logic exercises correctly, proceed. If
   both arms produce 0 valid verdicts or the cap check does not log, halt and inspect individual
   outputs in `logs/sessions/`. **Trivial baseline to compare**: t0027's per-arm success rate of
   4.62%. If preflight shows 0 successes across both arms, that is below the 4.62% baseline and
   warrants debugging before the full run.

6. **Compute the McNemar verdict.** Write `code/run_analysis.py` that loads the merged predictions,
   builds the 2x2 contingency table, computes `b` and `c` (discordant counts in each direction), the
   exact-binomial p-value via `scipy.stats.binomtest(k=b, n=b+c, p=0.5, alternative='two-sided')`,
   the effect size `b/(b+c)` with a Wilson 95% CI, and the per-subset breakdown (frontsci, taubench,
   SWE-bench). Persist all eight metric fields plus per-subset variants to `results/metrics.json`.
   Inputs: merged predictions. Outputs: `results/metrics.json`. Satisfies REQ-8, REQ-9 (data layer).

7. **Render the per-subset stratification chart.** Extend `make_result_charts.py` (already copied in
   step 1) with a `plot_per_subset_stratification()` function and call it from `run_analysis.py`.
   The chart is a grouped bar plot: x = subset, y = discordance rate, two bars per subset = arm A
   wins (b/n) and arm B wins (c/n). Save to `results/images/per_subset_stratification.png`. Inputs:
   `results/metrics.json`. Outputs: `results/images/per_subset_stratification.png`. Satisfies REQ-9
   (chart layer).

Milestone 2: paid execution.

8. **[CRITICAL] Run preflight smoke test.** From the worktree, in a screen/tmux session:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0029_rq1_discordance_rich_resample -- uv run python -u -m tasks.t0029_rq1_discordance_rich_resample.code.run_resample --limit 4`.
   Expected: 4 paired instances completed in ~5 minutes, both arms produce non-null judge verdicts
   on at least 2 of 4, `results/costs.json` shows cumulative_cost_usd in range [$0.20, $0.40], no
   malformed-plan errors. If any check fails, halt and debug — do not proceed to step 9.

9. **[CRITICAL] Run full resample.** Execute
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0029_rq1_discordance_rich_resample -- uv run python -u -m tasks.t0029_rq1_discordance_rich_resample.code.run_resample`.
   The orchestrator manages its own batch loop and exits cleanly when either the discordance target
   or the cap binds. Expected wall-clock: 4-8 hours. Expected end state: `results/costs.json` shows
   `total_cost_usd <= 35.00` and a non-zero `paired_n_completed` >= 130 (the reused floor).

10. **Run the analysis.** Execute
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0029_rq1_discordance_rich_resample -- uv run python -u -m tasks.t0029_rq1_discordance_rich_resample.code.run_analysis`.
    Outputs: `results/metrics.json`, `results/images/per_subset_stratification.png`.

## Remote Machines

None required. All compute is local CPU + Anthropic API. claude-sonnet-4-6 is invoked through the
official Anthropic Python SDK; no GPU, no third-party hosting. Reason: the task is a
deterministic-prompt LLM benchmark with judge re-invocations, all of which fit within the Anthropic
API's serverless model.

## Assets Needed

* **Library**:
  `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/`
  — sourced from t0021. Used as the canonical Plan-and-Solve baseline for arm A. Imported via copy
  (cross-task code import forbidden).
* **Library**: `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/plan_and_solve_v3/`
  — t0027's fault-tolerant fork. Used internally by arm A inside the resample harness. Imported via
  copy.
* **Predictions asset**:
  `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-a-reused/files/pointer.json`
  — pointer back to t0026 a-scope-aware predictions, becomes our reused arm B rows.
* **Predictions asset**:
  `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-b/files/predictions_variant_b.jsonl`
  — becomes our reused arm A rows.
* **Manifest**: `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json` — 130
  paired ids.
* **External resource**: claude-sonnet-4-6 via Anthropic API (`ANTHROPIC_API_KEY` in env).

## Expected Assets

Two predictions assets matching `task.json` `expected_assets: {"predictions": 2}`:

* `assets/predictions/arm-a/` — Plan-and-Solve baseline predictions on the union of t0027 reused
  pairs and t0029 fresh pairs. `details.json` declares `slug: "arm-a"`,
  `model: "claude-sonnet-4-6"`, `task_id: "t0029_rq1_discordance_rich_resample"`.
  `files/predictions.jsonl` contains one row per instance with fields
  `instance_id, subset, variant, final_answer, final_confidence, cost_usd, trajectory_path, judge_sonnet_success, judge_sonnet_rationale, source ("t0027_reused" or "t0029_fresh"), plan_parser_recovery_path, plan_parser_attempts, raised_malformed_plan_error`.
* `assets/predictions/arm-b/` — Scope-aware ReAct predictions, same schema, same union.
  `details.json` declares `slug: "arm-b"`.

## Time Estimation

* Research: completed in step 6 (~10 minutes).
* Planning: this step, ~30 minutes.
* Implementation (steps 1-7): 2-3 hours of code work.
* Preflight smoke test (step 8): ~10 minutes wall clock.
* Full resample (step 9): 4-8 hours wall clock, depending on Anthropic API throughput and how early
  the cap or discordance target binds.
* Analysis (step 10): ~5 minutes.
* Results / suggestions / reporting steps (12, 14, 15): ~1 hour.

Total wall clock: roughly **8-12 hours** end to end.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `ANTHROPIC_API_KEY` is missing or invalid | Low | Blocking, no spend | Step 5 preflight checks env var; on miss, write `intervention/missing_api_key.md` and exit 0 |
| Cumulative spend overshoots $35 because the cap is checked between batches | Medium | Up to ~$1.50 overshoot on a worst-case batch | BATCH_SIZE=8 caps the worst-case overshoot at 8 instances x 2 variants x ~$0.08 = ~$1.28; document the overshoot bound in `results/run_log.md` |
| t0027's reused predictions schema drifts from t0029's expected schema | Low | Loader breaks on read | `load_t0027_paired.py` validates each row against an explicit dataclass; on schema mismatch, log the failing row and abort before any new spend |
| Anthropic API rate limit / 429 storms during the full run | Medium | Long stalls, possible run abort | The t0027 `anthropic_shim.make_model_call()` already has exponential-backoff retry; the harness logs every retry to `logs/commands/` |
| Discordance rate is lower than t0027 priors (4-9%); cap binds with N_discordant < 30 | High | Partial verdict only | Pre-registered in this plan: emit a partial verdict with explicit power caveat; do not silently extend or relaunch |
| Variant-label inversion bug: code reads t0027 reused arm A as arm A instead of arm B | Medium | McNemar verdict pointed in the wrong direction | `load_t0027_paired.py` has the inversion in one place; integration test in step 1 verifies that `count(arm_a_success=True) == 6` from the reused pool (= t0027 Variant B's success count) |
| Judge disagreement on edge cases inflates discordance artificially | Low | Inflated discordant count | Reuse the t0027 Sonnet judge prompt verbatim, no changes; document this in `results/results_detailed.md` |
| `instance_loader.load_instances()` returns instances missing from t0027's pool but with malformed `gold` fields | Low | Skipped batches, lower N | Skip the row, log to `logs/commands/`, do not count against discordance target |

## Verification Criteria

Pre-execution gate (must hold before step 8 paid run):

* `uv run python -u -m arf.scripts.verificators.verify_plan t0029_rq1_discordance_rich_resample`
  prints `PASSED — no errors`.
* `uv run mypy -p tasks.t0029_rq1_discordance_rich_resample.code` exits 0.
* `uv run ruff check tasks/t0029_rq1_discordance_rich_resample/code/` exits 0.
* `tasks/t0029_rq1_discordance_rich_resample/code/load_t0027_paired.py` self-test confirms
  `len(reused_pairs) == 130` and the reused-pool 2x2 contingency matches t0027's reported 6/6
  discordance.

Post-execution gate (must hold before step 12 results step):

* `tasks/t0029_rq1_discordance_rich_resample/results/costs.json` exists with
  `total_cost_usd <= 35.00`.
* `tasks/t0029_rq1_discordance_rich_resample/results/metrics.json` exists and contains all eight
  required McNemar fields plus per-subset variants. Confirms REQ-8 and REQ-9.
* `tasks/t0029_rq1_discordance_rich_resample/assets/predictions/arm-a/files/predictions.jsonl` and
  `.../arm-b/files/predictions.jsonl` both exist with row count >= 130. Confirms REQ-10.
* `uv run python -u -m arf.scripts.verificators.verify_predictions_asset arm-a --task-id t0029_rq1_discordance_rich_resample`
  and the same for `arm-b` both print `PASSED`.
* `tasks/t0029_rq1_discordance_rich_resample/results/images/per_subset_stratification.png` exists
  and is >= 10 KB (plausibly rendered, not empty).
* `cat results/costs.json | jq '.discordant_count_running'` returns either >= 30 (full verdict) or <
  30 with `cap_hit_at_batch` set in `results/run_log.md` (partial verdict). The results writeup must
  reflect whichever case applies.

## Implementation Note on the Variant-Label Inversion (Pinned)

This is the single highest-risk source of silent error in the task. To make the inversion auditable,
every file that reads or writes a "variant" string must include this comment block verbatim near the
import section:

```python
# Variant labeling convention for t0029 (pinned by plan/plan.md):
#   t0028 task description: arm_a = Plan-and-Solve baseline, arm_b = scope-aware ReAct.
#   t0027 predictions assets: variant_a = scope-aware, variant_b = Plan-and-Solve baseline.
# When reading t0027 predictions: t0027 variant_a -> our arm_b; t0027 variant_b -> our arm_a.
# When writing t0029 outputs: arm_a = baseline, arm_b = scope-aware. No further inversion.
```

The integration test in step 1 enforces the count check
(`count(arm_a_success=True) == 6 and count(arm_b_success=True) == 6` on the t0027 reused pool); a
divergence from those counts is a labeling bug.
