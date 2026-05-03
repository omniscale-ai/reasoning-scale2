# Research Code — t0031_rq1_rq4_no_new_api_salvage

## Objective

Inventory the existing local outputs of `t0026_phase2_abc_runtime_n147_for_rq1_rq5` and
`t0027_phase2_5_abc_rerun_with_fixed_b_and_c` so that the four bounded no-new-API analyses planned
for `t0031` (RQ4 stratification, RQ1 power/futility, infrastructure-vs-genuine-failure audit, short
report) can load **only** from already-on-disk artifacts and produce arm-labelling consistent with
the `t0028` naming convention (arm A = Plan-and-Solve baseline, arm B = scope-aware ReAct).

## Background

`t0029` is `intervention_blocked` for missing `ANTHROPIC_API_KEY`; its locked plan (seed 20260503,
batch size 8, discordance target 30, sampling order frontsci → taubench → SWE-bench, $35 hard cap,
~$0.16/pair) is preserved unchanged. `t0031` is the bounded no-new-API salvage task that does
**not** modify `t0029` and does **not** launch `t0030`. All four analyses must read from local files
only.

The internal labelling convention in `t0027` is **opposite** to the reporting convention in `t0028`
/ `t0031`. The load helper must isolate the inversion in one place:

* t0027 internal: `variant_a` = scope-aware ReAct, `variant_b` = `plan_and_solve_v3`, `variant_c` =
  `matched_mismatch_v2`.
* t0031 reporting: arm A = Plan-and-Solve baseline, arm B = scope-aware ReAct.

## Methodology Review

The load helper uses the `t0027` paired predictions as the canonical ground truth for the 130 paired
instances. `variant_a` rows in `t0027` are pointer rows that resolve to `t0026`'s `variant_a`
predictions (no re-run). `variant_b` and `variant_c` rows in `t0027` are fresh re-runs with the
parser-fix and matched-mismatch redesign.

Per-instance failure classification for the audit comes from two layers:

1. **Hard-failure aggregates** in `tasks/t0026_*/results/results_detailed.md` and
   `tasks/t0027_*/results/results_detailed.md` (timeouts, RuntimeErrors, MalformedPlanError counts).
2. **Per-row fields** in the JSONL predictions: `plan_parser_recovery_path` (B and C only) with
   values `clean | reprompt | json_fallback | all_failed | unknown`, plus `judge_sonnet_success` for
   the model outcome.

The "unknown" parser bucket and `all_failed` bucket are the salvage signal for the infra-vs-genuine
audit: `unknown` typically reflects a harness/cost-tracker boundary that swallowed the recovery
path, not a model error; `all_failed` is the only parser-error category that should attribute to a
true plan-malformation outcome.

## Key Findings

### 1. 130-instance paired predictions (t0027)

Path roots:

* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-a-reused/files/predictions_variant_a.jsonl`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-b/files/predictions_variant_b.jsonl`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-c/files/predictions_variant_c.jsonl`

Each row carries: `instance_id`, `subset`, `variant`, `final_answer`, `final_confidence`,
`cost_usd`, `trajectory_path`, `judge_sonnet_success`, `judge_sonnet_rationale`. Variants B and C
additionally carry `plan_parser_recovery_path`.

### 2. Paired manifest

`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json` lists the 130 paired
instance IDs and the per-subset breakdown (SWE-bench=20, FrontierScience=26, Tau-bench=84). The
manifest is the canonical filter for the RQ4 stratification analysis.

### 3. Variant-labelling reconciliation

`tasks/t0027_*/plan/plan.md` line 27 fixes the t0027 internal mapping: "RQ1: Does scope-aware ReAct
(A) achieve a higher paired task-success rate than scope-unaware Plan-and-Solve (B)". So in t0027,
A=scope-aware, B=Plan-and-Solve.

`tasks/t0031_*/task_description.md` line 51 fixes the t0031 reporting mapping (matching t0028):
"Variant labelling: arm A = Plan-and-Solve baseline, arm B = scope-aware ReAct". And line 122
specifies the explicit inversion the load helper must perform: "Maps `variant_a` → arm B
(scope-aware ReAct) and `variant_b` → arm A (Plan-and-Solve baseline)".

This means the load helper is the **single** place in the task that touches the inversion. All
downstream code, tables, and charts must consume only the post-inversion arm-labelled DataFrame.

### 4. t0026 hard-failure aggregates (audit input)

`tasks/t0026_*/results/results_detailed.md` lines 65-96 record:

* A (scope-aware): 13 hard failures = 12 timeouts + 1 RuntimeError.
* B (plan_and_solve_v2 pre-fix): 40 = 22 timeouts + 2 RuntimeErrors + **16 MalformedPlanError**.
* C (matched_mismatch_v1 pre-fix): 44 = 43 timeouts + 1 RuntimeError.

The 16 MalformedPlanError count in B is the parser-fragility signal that motivated `t0027`'s parser
rewrite (S-0026-01).

### 5. t0027 parser recovery aggregates (audit input)

`tasks/t0027_*/results/results_detailed.md` lines 162-173 record:

* B parser recovery: 75 clean, 14 reprompt, 11 json_fallback, 1 all_failed, 29 unknown.
* C parser recovery: 70 clean, 18 reprompt, 7 json_fallback, 2 all_failed, 33 unknown.
* MalformedPlanError raised: **0** for both B and C — i.e., the parser fix prevented every
  hard-fail-on-parse instance that t0026 saw.

### 6. t0029 plan parameters (power-analysis driver)

`tasks/t0029_*/task_description.md` cap rule (~line 45-56): hard cap **$35.00 USD**, abort if
cumulative cost ≥ $35 AND discordant pairs < 30. Discordance target ≥ 30. Sampling order: stratified
from t0027's discordant pairs first, then "unknown" parser-recovery rows (B unknown = 29, C unknown
= 33), then subset expansion frontsci → taubench → SWE-bench. Per-pair cost rate: ~$0.16/pair (so
cap admits roughly 218 new paired instances).

### 7. t0027 discordance count (RQ4 stratification ground truth)

The README discordance figure should be re-derived from the t0027 paired predictions per the t0031
task description ("must be re-derived from t0027 files; do NOT hardcode 4.6%"). The expected
ballpark from t0027 documentation is ~12/130 ≈ 9.2% but the load helper computes it from the joined
DataFrame.

## Recommended Approach

### Load helper recipe (`code/load_paired_outputs.py`)

1. Read the 130-row paired manifest from `tasks/t0027_*/data/paired_manifest.json` and pin it as the
   canonical instance filter.
2. Read the three variant predictions JSONL files listed above. For variant A, resolve the pointer
   to t0026's `variant_a` predictions if the t0027 file is empty or a pure manifest; otherwise read
   directly.
3. Filter each variant DataFrame to the 130 paired `instance_id`s.
4. Apply the **single inversion**: rename `variant_a → arm_b`, `variant_b → arm_a`,
   `variant_c → arm_c`. Add an `arm` column (`arm_a`, `arm_b`, `arm_c`).
5. Pivot to wide format keyed on `instance_id`, `subset`, with columns `arm_a_judge_success`,
   `arm_b_judge_success`, `arm_a_recovery_path` (renamed from
   `variant_b.plan_parser_recovery_path`), etc. Concordance/discordance is
   `arm_a_judge_success != arm_b_judge_success`.
6. Return a frozen `PairedFrame` dataclass containing the wide DataFrame plus precomputed counts
   (per-subset N, discordant N) so downstream scripts cannot accidentally re-invert.

### Audit script (`code/analysis_log_audit.py`)

Combine t0026 aggregates (hard-failure breakdown) with t0027 parser recovery (per-row
`plan_parser_recovery_path`) into one infra-vs-genuine table:

* infra failure: timeouts, RuntimeErrors, parser `unknown`, parser `all_failed` (when not matched by
  a real model output), cost-tracker errors.
* genuine model failure: judged-unsuccessful rows with parser path `clean`, `reprompt`, or
  `json_fallback`.

### RQ4 stratification (`code/analysis_rq4_stratification.py`)

Group by `subset`, cross-tabulate `arm_a_judge_success` × `arm_b_judge_success`, attach Wilson 95%
CIs to each cell where N ≥ 5.

### RQ1 power/futility (`code/analysis_rq1_power.py`)

Use t0029's $35 cap (~218 admittable new pairs) over a conditional-B-wins grid {0.55, 0.60, 0.65,
0.70, 0.75, 0.80} and the discordance rate derived from the loaded t0027 table.

## References

* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/results_detailed.md`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/plan/plan.md`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_detailed.md`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-{a-reused,b,c}/files/predictions_variant_{a,b,c}.jsonl`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0029_rq1_discordance_rich_resample/task_description.md`
* `/Users/lysaniuk/Documents/reasoning-scale2/tasks/t0031_rq1_rq4_no_new_api_salvage/task_description.md`
