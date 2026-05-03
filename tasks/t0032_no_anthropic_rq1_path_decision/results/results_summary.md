# RQ1 PATH DECISION — OPTION (A): EXISTING-RESULTS-ONLY VERDICT

## Summary

Locked in **option (a) — existing-results-only verdict** as the recommended RQ1 execution path under
the permanent no-Anthropic constraint. The t0031 re-derivation already yields the formal RQ1
conclusion at $0 with arm-labelling comparability against t0027 / t0028 trivially preserved: 12 /
130 discordant pairs, symmetric 6 / 6 split, two-sided exact-binomial McNemar p = **1.0000**, with a
real SWE-bench arm-B advantage and a marginal FrontierScience arm-A advantage that cancel in
aggregate. Options (b), (c), and (d) were each rejected on a documented comparability or foreclosure
basis; creative-thinking surfaced no non-obvious cost-saver that flips the recommendation.

## Metrics

* **Aggregate McNemar p (N=130, t0031)**: **1.0000** (12 discordant; 6 a_only; 6 b_only)
* **SWE-bench per-stratum cell**: b_only = **6**, a_only = **0** (n = 20; two-sided p = **0.0312**)
* **FrontierScience per-stratum cell**: a_only = **5**, b_only = **0** (n = 26; two-sided p =
  **0.0625**)
* **Tau-bench per-stratum cell**: 1 discordant of n = 84 (83 / 84 both-fail; two-sided p =
  **1.0000**)
* **Power at the t0029 cap**: crosses 0.80 only at p1 ≥ 0.75 (power = **0.846** at p1 = 0.75; below
  **0.10** at p1 = 0.55)
* **Per-paired-instance cost on Sonnet (t0026 + t0027)**: ≈ **$0.107** ($0.0344 arm A + $0.0727 arm
  B)
* **Option (c) USD point estimate**: $0.07 / pair × 218 = **$15.26** (band $15-$25)
* **This task's total cost**: **$0.00** (no paid API call, no remote compute)

## Verification

* `meta.asset_types.answer.verificator` (answer asset) — PASSED (0 errors, 0 warnings)
* `verify_plan` (plan/plan.md) — PASSED (0 errors, 0 warnings)
* `verify_task_dependencies` (t0027, t0031) — PASSED (0 errors, 0 warnings)
* `cross_check.py` (t0031 numbers re-derived in `code/decision_inputs.json`) — PASSED (verbatim
  match)
* `ruff check --fix . && ruff format .` and
  `mypy -p tasks.t0032_no_anthropic_rq1_path_decision.code` — clean
