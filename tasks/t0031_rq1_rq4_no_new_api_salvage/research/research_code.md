---
spec_version: "1"
task_id: "t0031_rq1_rq4_no_new_api_salvage"
research_stage: "code"
tasks_reviewed: 4
tasks_cited: 4
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-05-03"
status: "complete"
---
# Research Code — t0031_rq1_rq4_no_new_api_salvage

## Task Objective

Inventory the existing local outputs of `t0026_phase2_abc_runtime_n147_for_rq1_rq5` [t0026] and
`t0027_phase2_5_abc_rerun_with_fixed_b_and_c` [t0027] so that the four bounded no-new-API analyses
planned for this task (RQ4 stratification, RQ1 power/futility, infrastructure-vs-genuine-failure
audit, short report) can load **only** from already-on-disk artifacts and produce arm-labelling
consistent with the `t0028` reporting convention (arm A = Plan-and-Solve baseline, arm B =
scope-aware ReAct). t0029 [t0029] is `intervention_blocked`; this salvage task does not modify it.

## Library Landscape

No existing project library is reused for the four bounded analyses. The library aggregator returned
`plan_and_solve_v3` (registered by [t0027]) and `matched_mismatch_v2` (also registered by [t0027])
as the only libraries touching the A/B/C variants, but both are runtime libraries used to *produce*
predictions and trajectories. This task only *reads* the predictions JSONL files and hard-failure
aggregates already on disk, so neither library is imported. The four analysis scripts implemented in
`code/` are written from scratch with stdlib + pandas + scipy + matplotlib only.

## Key Findings

### Variant labelling reconciliation between t0027 and t0028 reporting

The t0027 internal labelling [t0027] is **opposite** to the t0031 / t0028 reporting labelling. The
t0027 plan fixes "RQ1: Does scope-aware ReAct (A) achieve a higher paired task-success rate than
scope-unaware Plan-and-Solve (B)" (`tasks/t0027_*/plan/plan.md` line 27), so internally
`variant_a = scope-aware ReAct`, `variant_b = plan_and_solve_v3`. The t0031 task description fixes
the reporting convention at `tasks/t0031_*/task_description.md` line 51: "arm A = Plan-and-Solve
baseline, arm B = scope-aware ReAct", with the explicit mapping at line 122: "Maps `variant_a` → arm
B (scope-aware ReAct) and `variant_b` → arm A (Plan-and-Solve baseline)". This single inversion must
be isolated in `code/load_paired_outputs.py`; downstream scripts must consume only the
post-inversion arm-labelled DataFrame.

### Paired-instance ground truth lives in three JSONL prediction assets

The 130 paired instances are persisted as JSONL prediction assets under
`tasks/t0027_*/assets/predictions/abc-rerun-{a-reused,b,c}/files/predictions_variant_{a,b,c}.jsonl`
[t0027]. Each row carries `instance_id`, `subset`, `variant`, `final_answer`, `final_confidence`,
`cost_usd`, `trajectory_path`, `judge_sonnet_success`, `judge_sonnet_rationale`. Variants B and C
additionally carry `plan_parser_recovery_path` taking values from
`clean | reprompt | json_fallback | all_failed | unknown`. The canonical instance filter is
`tasks/t0027_*/data/paired_manifest.json` (130 IDs: SWE-bench=20, FrontierScience=26, Tau-bench=84).
The `abc-rerun-a-reused` asset is a pointer to t0026's `variant_a` predictions [t0026].

### Hard-failure aggregates (audit input)

[t0026] `tasks/t0026_*/results/results_detailed.md` lines 65-96 record:

* A (scope-aware): 13 hard failures = 12 timeouts + 1 RuntimeError.
* B (plan_and_solve_v2 pre-fix): 40 = 22 timeouts + 2 RuntimeErrors + 16 MalformedPlanError.
* C (matched_mismatch_v1 pre-fix): 44 = 43 timeouts + 1 RuntimeError.

The 16 MalformedPlanError count in B is the parser-fragility signal that motivated [t0027]'s parser
rewrite (S-0026-01).

[t0027] `tasks/t0027_*/results/results_detailed.md` lines 162-173 record per-row parser recovery:

* B: 75 clean, 14 reprompt, 11 json_fallback, 1 all_failed, 29 unknown.
* C: 70 clean, 18 reprompt, 7 json_fallback, 2 all_failed, 33 unknown.
* MalformedPlanError raised: 0 for both B and C.

### t0029 power-analysis parameters [t0029]

`tasks/t0029_*/task_description.md` lines 45-56 fix the cap rule: hard cap **$35.00 USD**, abort if
cumulative cost ≥ $35 AND discordant pairs < 30. Discordance target ≥ 30 paired instances. Sampling
order: t0027 discordant pairs → unknown parser-recovery rows (B unknown = 29, C unknown = 33) →
subset expansion frontsci → taubench → SWE-bench. Per-pair cost rate ≈ $0.16/pair (so cap admits ≈
218 new paired instances).

## Reusable Code and Assets

The four analyses do **not** import from any prior task `code/` directory. All copy/import labels
are listed below for the four sources actually used.

* **Source**:
  `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-a-reused/files/predictions_variant_a.jsonl`
  * **What it does**: 130 paired-instance prediction rows for variant A (resolves to t0026's
    `variant_a`).
  * **Reuse method**: read from disk — no import.
  * **Adaptation needed**: rename `variant_a → arm_b` in load helper.
  * **Line count**: ≈ 130 rows JSONL.

* **Source**: `tasks/t0027_*/assets/predictions/abc-rerun-b/files/predictions_variant_b.jsonl`
  * **What it does**: 130 paired-instance prediction rows for variant B (Plan-and-Solve v3) with
    `plan_parser_recovery_path`.
  * **Reuse method**: read from disk.
  * **Adaptation needed**: rename `variant_b → arm_a`.
  * **Line count**: ≈ 130 rows JSONL.

* **Source**: `tasks/t0027_*/assets/predictions/abc-rerun-c/files/predictions_variant_c.jsonl`
  * **What it does**: 130 paired-instance prediction rows for variant C (matched-mismatch v2) with
    `plan_parser_recovery_path`.
  * **Reuse method**: read from disk.
  * **Adaptation needed**: rename `variant_c → arm_c`.
  * **Line count**: ≈ 130 rows JSONL.

* **Source**: `tasks/t0027_*/data/paired_manifest.json`
  * **What it does**: canonical 130-instance ID list with per-subset breakdown.
  * **Reuse method**: read from disk.
  * **Adaptation needed**: none.
  * **Line count**: ≈ 130 entries JSON.

## Lessons Learned

[t0026] established the parser fragility of the original Plan-and-Solve v2 (16 MalformedPlanError
rows out of 147 in B), which led to [t0027]'s `plan_and_solve_v3` rewrite with `_robust_parse_plan`
re-prompt + JSON tool-call fallback. After that fix [t0027] reported zero MalformedPlanError. This
means the t0026 hard-failure mix is no longer representative of fresh runs; the audit must attribute
the 16 t0026 parser-error rows to the *pre-fix* harness and treat [t0027] as the fixed baseline.

[t0027] also exposed an "unknown" parser-recovery bucket (29 rows in B, 33 in C) that does not
correspond to a plan-parse failure but to a harness/cost-tracker boundary that swallowed the
recovery path label. These rows still produced trajectories and judged outcomes, so the audit should
classify "unknown" as **infrastructure noise**, not as a model outcome failure.

The t0027 discordance figure must be re-derived from the paired DataFrame at load time. The t0031
task description warns explicitly: "must be re-derived from t0027 files; do NOT hardcode 4.6%". The
expected ballpark is ~12/130 ≈ 9.2% but the load helper computes it.

## Recommendations for This Task

1. **Single load helper, single inversion.** Implement `code/load_paired_outputs.py` that reads the
   three JSONL prediction files plus the paired manifest, filters to 130 rows, and applies the only
   `variant → arm` rename. Return a frozen `PairedFrame` dataclass with the wide DataFrame plus
   precomputed counts so downstream scripts cannot accidentally re-invert.
2. **No imports from t0026 / t0027 / t0028 `code/`.** The cross-task import rule forbids it; this
   task's analyses are short enough to write from scratch in pandas + scipy.
3. **Audit categorization.** Map (a) `unknown` parser path + harness timeouts + RuntimeErrors +
   cost-tracker errors → infrastructure failure; (b) judged-unsuccessful rows with parser path
   `clean | reprompt | json_fallback` → genuine model failure; (c) `all_failed` parser path →
   genuine plan-malformation failure (rare: 1 in B, 2 in C).
4. **Power grid.** Power-analysis script iterates conditional B-wins rates {0.55, 0.60, 0.65, 0.70,
   0.75, 0.80} with the t0027-derived discordance rate and the $35 cap (≈ 218 admittable new pairs
   at $0.16/pair).
5. **Re-derive discordance from data, not docs.** Compute discordant N from the post-inversion
   DataFrame; do not hardcode any figure.

## Task Index

### [t0026]

* Task ID: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`
* Name: Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5
* Status: completed
* Relevance: provides the `variant_a` predictions resolved by the t0027 pointer asset, plus the
  hard-failure aggregates (16 MalformedPlanError, 12 timeouts, etc.) that ground the audit's pre-fix
  view.

### [t0027]

* Task ID: `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
* Name: Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C
* Status: completed
* Relevance: produces the 130 paired-instance JSONL predictions, the parser recovery field
  (`plan_parser_recovery_path`), and the discordance ground truth used for both RQ4 and the power
  analysis.

### [t0028]

* Task ID: `t0028_brainstorm_results_8`
* Name: Brainstorm results 8
* Status: completed
* Relevance: fixes the reporting labelling convention (arm A = Plan-and-Solve baseline, arm B =
  scope-aware ReAct) that t0031 inherits and that drives the inversion in `load_paired_outputs.py`.

### [t0029]

* Task ID: `t0029_rq1_discordance_rich_resample`
* Name: RQ1 discordance-rich paired resample on the M-Sonnet/J-Sonnet axis
* Status: intervention_blocked
* Relevance: provides the locked plan parameters ($35 cap, $0.16/pair, 30-discordant target,
  sampling order) that drive the t0031 power/futility analysis.
