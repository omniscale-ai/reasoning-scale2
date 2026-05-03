---
spec_version: "3"
task_id: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-02T17:26:53Z"
completed_at: "2026-05-03T00:30:00Z"
---
## Summary

Built `plan_and_solve_v3` (bounded 3-attempt plan-parse recovery: clean → reprompt → JSON-mode) and
`matched_mismatch_v2` (mismatch wrapper retargeted at v3) libraries, ran smoke gates (5 FrontSci
each) on B and C, then ran full B and C variants on the 130 paired instances using claude-sonnet-4-6
(corrected from the original opus-4-7 spec to match t0026's variant A and stay under the $50 cap).
Judged predictions with the primary sonnet judge and computed paired McNemar tests for RQ1 (A vs B)
and RQ5 (B vs C) with Bonferroni α=0.025, plus Xiong2024 10-bin ECE calibration for B and C. All
four artefacts (`mcnemar_results.json`, `calibration.json`, `metrics.json`,
`parser_failure_count.json`) were written and verified non-empty.

## Actions Taken

1. Authored libraries `plan_and_solve_v3` and `matched_mismatch_v2` under `assets/library/`, plus
   per-task copies in `code/` for execution; corrected the predictions-asset descriptions to state
   claude-sonnet-4-6 as the model under test for B and C.
2. Ran B and C smoke gates (5 FrontSci each) and verified projected full-run cost stayed under cap:
   B projected $13.47, C projected $20.49, both with 0 parser failures. SMOKE GATE PASS for both.
3. Ran full B variant (130 paired instances) end-to-end: agent cost $9.4534, judge cost $0.1534,
   total $9.6068, 0 parser failures, success rate 6/130 = 0.0462. Wrote
   `assets/predictions/abc-rerun-b/files/predictions_variant_b.jsonl`.
4. Ran full C variant (130 paired instances) end-to-end: agent cost $9.3392, judge cost $0.1300,
   total $9.4692, 0 parser failures, success rate 7/130 = 0.0538. Wrote
   `assets/predictions/abc-rerun-c/files/predictions_variant_c.jsonl`.
5. Ran `run_analysis.py` to produce `data/mcnemar_results.json` (RQ1 A-vs-B p=1.0 do_not_reject; RQ5
   B-vs-C p=1.0 do_not_reject after Bonferroni), `data/calibration.json` (B ECE=0.336, C ECE=0.374;
   A excluded — variant A does not elicit verbalised confidence), and `results/metrics.json`
   (per-variant task_success_rate and overconfident_error_rate).

## Outputs

* `code/plan_and_solve_v3.py` — bounded 3-attempt plan-parse recovery agent
* `code/matched_mismatch_v2.py` — adversarial mismatch wrapper retargeted at v3
* `code/run_abc_rerun.py` — smoke and full-run harness with per-stream cost gate
* `code/run_analysis.py` — paired McNemar (Bonferroni α=0.025) + 10-bin ECE
* `assets/library/plan_and_solve_v3/` — library asset (full description + files)
* `assets/library/matched_mismatch_v2/` — library asset (full description + files)
* `assets/predictions/abc-rerun-a-reused/files/pointer.json` — pointer to t0026 variant-A JSONL
* `assets/predictions/abc-rerun-b/files/predictions_variant_b.jsonl` — 130 lines, sonnet-judge
* `assets/predictions/abc-rerun-c/files/predictions_variant_c.jsonl` — 130 lines, sonnet-judge
* `data/runs/b/` — 130 per-instance trajectory JSONs for variant B
* `data/runs/c/` — 130 per-instance trajectory JSONs for variant C
* `data/mcnemar_results.json` — paired McNemar tables (overall + per-subset) for RQ1 and RQ5
* `data/calibration.json` — 10-bin ECE for B and C, with note explaining A's exclusion
* `data/parser_failure_count.json` — per-variant parser failure counters and recovery-path mix
* `data/paired_manifest.json` — the 130 paired instance ids and per-subset breakdown
* `results/metrics.json` — per-variant task_success_rate and overconfident_error_rate

## Issues

The original task description specified claude-opus-4-7 for B and C, but t0026's variant A was
produced on claude-sonnet-4-6. Continuing with opus-4-7 would have introduced a cross-model confound
and projected cost above the $50 cap (≈$61). The decision was to switch B and C to claude-sonnet-4-6
to make A-vs-B and B-vs-C clean same-model contrasts and stay within budget. This decision is
recorded explicitly in every predictions-asset description and in `mcnemar_results.json`
`model_confound_note`.
