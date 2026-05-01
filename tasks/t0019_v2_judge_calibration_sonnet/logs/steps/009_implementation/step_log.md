---
spec_version: "3"
task_id: "t0019_v2_judge_calibration_sonnet"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-01T14:20:26Z"
completed_at: "2026-05-01T17:39:40Z"
---
# Step 9: implementation

## Summary

Implemented the v2 judge calibration sweep. Built the row pool (12 v1-sonnet from t0005, 23 v2-haiku
from t0009 with t0015 corrections, 20 v2-sonnet from t0014 = 55 rows), built the two judge prompt
templates (`substantive` critic that simulates atomic execution; `model-rotated` keeps t0014's
prompt verbatim and only swaps the judge model from claude-haiku-4-5 to claude-sonnet-4-6), wired
both to the `claude` CLI subprocess transport because the OAuth-issued API key in this environment
lacks sonnet quota (see `intervention/critical_step_blocked.md`), and executed 110 sonnet judge
calls under a $20.00 hard cap (raised from $4.50 per the intervention), spending $19.30. After the
two-call validation gate at `--limit 5` passed, the full sweep produced 110 fresh sonnet verdicts
covering all 55 rows × 2 judge configurations. Outputs were materialized into the predictions asset
(`assets/predictions/v2-judge-calibration/files/predictions.jsonl` plus `details.json`) and the
answer asset (`assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/`
plus `full_answer.md` and `details.json`).

## Actions Taken

1. Implemented `code/build_pool.py`, `code/judge_prompts.py`, `code/run_judges.py`,
   `code/build_outputs.py`, `code/constants.py`, `code/paths.py`.
2. Switched transport from Anthropic SDK to `claude` CLI subprocess after the SDK returned 401 on
   sonnet calls (recorded in `intervention/critical_step_blocked.md`); raised the hard cap from
   $4.50 to $20.00 per the intervention's option-2.
3. Re-ran validation at `--limit 5` for both judge configurations; both runs returned the expected
   accept/reject distributions.
4. Ran the full sweep: 55 rows × 2 sonnet configs = 110 calls. Total cost: $19.30. Wall time:
   approximately 26 minutes.
5. Built outputs: 9-cell metrics (3 annotators × 3 judge configs) with Wilson 95% CIs, schema-only
   deltas, model-only deltas, Cohen's kappa between judge configs, and two charts
   (`accept_rate_3x3.png` and `schema_only_delta_by_judge.png`).
6. Wrote the answer asset `full_answer.md` answering the question "Does v2 keep a 30+ pp delta under
   substantive and sonnet judges?" with confidence "low" because the result is mixed (substantive
   +24.6 pp, model-rotated +37.3 pp vs the t0014 baseline of +58.0 pp).

## Outputs

* `tasks/t0019_v2_judge_calibration_sonnet/code/` (Python implementation)
* `tasks/t0019_v2_judge_calibration_sonnet/assets/predictions/v2-judge-calibration/files/predictions.jsonl`
* `tasks/t0019_v2_judge_calibration_sonnet/assets/predictions/v2-judge-calibration/details.json`
* `tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/full_answer.md`
* `tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/details.json`
* `tasks/t0019_v2_judge_calibration_sonnet/results/metrics.json` (9 variants)
* `tasks/t0019_v2_judge_calibration_sonnet/results/images/accept_rate_3x3.png`
* `tasks/t0019_v2_judge_calibration_sonnet/results/images/schema_only_delta_by_judge.png`

## Issues

* SDK 401 on sonnet quota required switching to CLI subprocess and raising the budget cap. The
  intervention file documents this completely.
* Per-call cost rose from the planned ~$0.024 (SDK + cache hits) to ~$0.18 (CLI + cache-creation
  overhead); $19.30/$20.00 of the raised cap was consumed.
