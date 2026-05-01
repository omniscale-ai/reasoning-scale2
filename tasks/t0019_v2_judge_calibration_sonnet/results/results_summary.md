# Results Summary: v2 Judge Calibration with Sonnet

## Summary

Re-judged the same 55-row hierarchy pool from t0014 (12 v1-sonnet + 23 v2-haiku + 20 v2-sonnet)
under three judge configurations: the cached t0014 original-haiku verdicts as baseline, a
substantive critic prompt on `claude-sonnet-4-6`, and a model-rotated original-prompt judge on
`claude-sonnet-4-6`. The headline finding is that the +57 pp v2-vs-v1 schema-only gap from t0014
**partially survives** under sonnet judges: **+24.6 pp** under the substantive critic and **+37.3
pp** under the model-rotated judge, vs the **+58.0 pp** baseline. Neither pre-registered extreme
decision criterion (drops below +30 pp on both sonnet judges, or stays at or above +45 pp on both)
was simultaneously satisfied, so the answer is **Mixed / low confidence**.

## Methodology

* 110 fresh sonnet judge calls (55 substantive + 55 model-rotated) via the local `claude` CLI
  subprocess; the OAuth-issued ANTHROPIC_API_KEY in this environment lacks sonnet quota, so
  `intervention/critical_step_blocked.md` was filed and option 2 was authorised: raise the budget
  cap from $4.50 to $20.00 and switch transport from the Anthropic SDK to a `claude` CLI subprocess
  wrapper. The change is locked in `code/constants.py` (`BUDGET_CAP_USD = 20.00`,
  `JUDGE_TRANSPORT = "cli"` default) and documented in `intervention/critical_step_blocked.md`.
* All 110 calls returned valid JSON envelopes (0 parse failures, 0 call failures, 0 budget halts).
  Total spend was **$19.30** ($9.68 substantive, $9.63 model-rotated), comfortably within the raised
  $20 cap but ~4.3x the original $4.50 plan.
* Per-cell binary acceptance rates and Wilson 95% CIs, plus schema-only and model-only deltas under
  each judge, are emitted to `results/metrics.json` (explicit multi-variant format, registered
  metric only) and `data/computed_stats.json` (full audit).
* Cohen's kappa between the two sonnet judges overall: **0.626** (moderate agreement), with
  per-annotator kappas of 0.47 (v1-sonnet), 0.65 (v2-haiku), and 1.00 (v2-sonnet).

## Metrics

* **Schema-only delta (v2-haiku - v1-sonnet)** under each judge: **+58.0 pp** (baseline haiku),
  **+24.6 pp** (substantive sonnet), **+37.3 pp** (model-rotated sonnet).
* **Model-only delta (v2-sonnet - v2-haiku)** under each judge: **-1.3 pp** (baseline haiku), **+8.7
  pp** (substantive sonnet), **+4.3 pp** (model-rotated sonnet).
* **Per-cell accept rates**: v1-sonnet 33.3% / 66.7% / 58.3% (haiku / substantive / rotated);
  v2-haiku 91.3% / 91.3% / 95.7%; v2-sonnet 90.0% / 100.0% / 100.0%.
* **Average per-call sonnet cost**: **$0.176/call** (vs SDK + cache-hit projection of ~$0.024/call
  in `intervention/critical_step_blocked.md`); average sonnet latency **~14 s/call**.
* **Cohen's kappa overall** between substantive and model-rotated sonnet: **0.626**.
* **Total cost**: **$19.30** of a **$20.00** raised cap (vs original $4.50 plan ceiling).

## Verification

* `verify_task_file.py` — PASSED (logs in `logs/steps/015_reporting/`)
* `verify_logs.py` — PASSED
* `verify_task_results.py` — PASSED
* `verify_predictions_asset.py` — PASSED
* `verify_answer_asset.py` — PASSED
* `verify_task_metrics.py` — PASSED
* `verify_step_tracker.py` — PASSED
