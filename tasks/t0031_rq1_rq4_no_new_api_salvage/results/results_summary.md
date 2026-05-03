NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029

# RQ1/RQ4 No-New-API Preliminary Salvage

This task spends **$0.00** of new API budget. It runs four bounded analyses on the already-on-disk
outputs of `t0026_phase2_abc_runtime_n147_for_rq1_rq5` and
`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`. The labelled-arm convention follows `t0028`: arm A =
Plan-and-Solve baseline, arm B = scope-aware ReAct, arm C = matched-mismatch.

## Summary

Re-derived the t0027 paired discordance rate at **12/130 = 9.23%** (symmetric: 6 arm-A wins vs 6
arm-B wins, McNemar two-sided p = 1.0000). Stratified RQ4 shows discordance is concentrated in
opposite directions on SWE-bench (6/20 arm-B wins) and FrontierScience (5/26 arm-A wins). Under the
locked t0029 plan ($35 cap, ~$0.16/pair → ~218 admittable new pairs, ≈ 32 expected discordant at the
t0027 rate) RQ1 reaches **80% power only when the conditional B-wins rate p1 ≥ 0.75**. The
infrastructure-vs-genuine-failure audit confirms zero MalformedPlanError post-fix in t0027 but flags
22% (arm A) and 25% (arm C) of paired rows as parser-recovery `unknown` (cost-tracker boundary noise
that does not affect the discordance signal). This task does not replace t0029; it only narrows the
prior over likely outcomes.

## Metrics

* **Discordance rate (t0027 paired N=130)**: **12/130 = 0.0923** (re-derived from data, not
  hardcoded).
* **Discordance split**: arm-B wins **6**, arm-A wins **6**; McNemar exact-binomial two-sided p =
  **1.0000**.
* **SWE-bench arm-B pass rate**: **6/20 = 30.0%** (Wilson 95% CI [12.8%, 54.3%]); arm-A SWE-bench
  pass rate **0/20 = 0.0%**; SWE-bench McNemar p = **0.0312** (one-sided, 6 arm-B wins out of 6
  discordant).
* **FrontierScience arm-A pass rate**: **5/26 = 19.2%**; arm-B = **0/26 = 0.0%**; FrontSci McNemar p
  = **0.0625**.
* **Tau-bench**: 1 discordant pair out of 84; signal is dominated by both-fail (judge-success rate
  is **1.2%** for arm A and **0.0%** for arm B).
* **RQ1 cap arithmetic**: cap admits **218** new paired instances; total N at cap = **348**;
  expected discordant N = **32**.
* **RQ1 power at expected discordant N=32 (one-sided α=0.05)**: p1=0.55 → **0.082**, p1=0.60 →
  **0.205**, p1=0.65 → **0.405**, p1=0.70 → **0.644**, p1=0.75 → **0.846**, p1=0.80 → **0.959**.
* **Smallest discordant N for 80% power** per p1: 0.55 → >200, 0.60 → 158, 0.65 → 69, 0.70 → 37,
  0.75 → 23, 0.80 → 18.
* **Audit pre-fix (t0026, N=147)**: A hard-failures **13** (12 timeouts + 1 runtime), B
  hard-failures **40** (22 timeouts + 2 runtime + **16 MalformedPlanError**), C hard-failures **44**
  (43 timeouts + 1 runtime).
* **Audit post-fix (t0027, paired N=130)**: zero MalformedPlanError raised. Parser-recovery unknown
  bucket: arm A **29/130 (22.3%)**, arm C **33/130 (25.4%)**; flagged as cost-tracker-boundary
  infrastructure noise.
* **Total cost of this task**: **$0.00** (no API calls, no remote machines).

## Verification

* `verify_task_file.py` — PASSED (0 errors, 0 warnings)
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings) — both upstream tasks (`t0026`,
  `t0027`) are completed.
* `verify_logs.py` — PASSED for all step folders (0 errors).
* `verify_research_code.py` — PASSED (0 errors).
* `verify_plan.py` — PASSED with 1 expected orchestrator warning (PL-W009).
* `verify_task_results.py` — PASSED (0 errors).
* Re-derived discordance count (12) matches the value computed by `load_paired_outputs.py` from the
  loaded DataFrame; no hardcoded 4.6% or 9.2% figure was used.
* `results_summary.md` first line equals exactly
  `NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`.
* `results/images/` contains exactly three PNG charts: `rq4_stratification_heatmap.png`,
  `rq1_power_curve.png`, `log_audit_failure_breakdown.png`.
* `costs.json` reports `total_cost_usd: 0.00`; `remote_machines_used.json` is `[]`.

## Limitations

* The 130 paired instances are a fixed sample, not the discordance-rich resample that
  `t0029_rq1_discordance_rich_resample` is designed to draw. Replacement is not possible without new
  API spend.
* Per-cell N is small in some strata (SWE-bench N=20, FrontSci N=26); Wilson CIs are wide and
  several stratum-level McNemar tests rest on 5-6 discordant pairs.
* Power numbers depend on the assumed conditional B-wins rate p1, which is **not** yet observed at
  the cap; the existing 12-discordant sample is consistent with any p1 in roughly [0.25, 0.75].
* 29 arm-A and 33 arm-C rows had their parser-recovery label swallowed by a cost-tracker boundary in
  t0027. They still produced judged outcomes, so they are included in the discordance count, but the
  audit cannot certify them as clean parser runs.
* Arm B (scope-aware ReAct) rows from t0026 do not carry a `plan_parser_recovery_path` field at all;
  the audit relies on t0026's pre-fix hard-failure aggregates (12 timeouts + 1 runtime error) for
  arm B.
* This task does not replace `t0029`. `t0029` remains the canonical RQ1 verdict owner; resume from
  its locked plan once an Anthropic API key is available.
