# Results Summary — t0027 Phase 2.5 A/B/C re-run

## Summary

Forked t0021's plan-and-solve v2 into a fault-tolerant `plan_and_solve_v3` (bounded 3-attempt
plan-parse recovery) and t0010's mismatch wrapper into `matched_mismatch_v2` (now delegating to v3),
re-ran B and C on t0026's 130 paired instances under claude-sonnet-4-6, and recomputed paired
McNemar (Bonferroni α=0.025) for RQ1 (A vs B) and RQ5 (B vs C) plus 10-bin ECE calibration. Both
McNemar tests are **do_not_reject** under Bonferroni; parser-failure rate is **0.0** for both
variants (down from t0026's B=12%). Total task spend was **$20.7631** (cap $50).

## Metrics

* **Variant A (reused from t0026)** — task_success_rate = **0.0462** (6/130)
* **Variant B (plan_and_solve_v3)** — task_success_rate = **0.0462** (6/130),
  overconfident_error_rate = **0.0588**, ECE = **0.336**
* **Variant C (mismatch over v3)** — task_success_rate = **0.0538** (7/130),
  overconfident_error_rate = **0.143**, ECE = **0.374**
* **RQ1 paired McNemar (A vs B)** — discordant 6/6, p = **1.0**, do_not_reject (α=0.025)
* **RQ5 paired McNemar (B vs C)** — discordant 4/5, p = **1.0**, do_not_reject (α=0.025)
* **Parser robustness** — `raised_malformed_plan_error` = **0/130** for both B and C (acceptance
  gate REQ-6 met: target was < 3, actual is 0)
* **Cost** — agent + judge + smoke combined = **$20.7631** (B = $9.94, C = $10.76, A reused = $0)

## Verification

* `verify_task_metrics.py` — PASSED (0 errors)
* `verify_task_results.py` — PASSED (0 errors; warnings expected for spec_version="2"
  task-requirement-coverage labels)
* `verify_library_asset.py` (plan_and_solve_v3, matched_mismatch_v2) — PASSED (0 errors each)
* `verify_predictions_asset.py` (abc-rerun-a-reused, abc-rerun-b, abc-rerun-c) — PASSED (0 errors)
* `verify_logs.py` — PASSED (0 errors)
