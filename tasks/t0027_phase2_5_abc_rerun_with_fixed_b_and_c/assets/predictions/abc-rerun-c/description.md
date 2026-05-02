---
spec_version: "2"
predictions_id: "abc-rerun-c"
documented_by_task: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
date_documented: "2026-05-02"
---
# Variant C (re-run): matched_mismatch_v2 wrapping plan_and_solve_v3

## Metadata

* **Variant**: c
* **Model**: claude-sonnet-4-6 (Anthropic CLI transport, 10-turn cap, 4096 max output tokens)
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 130 (paired set; intersection of t0026 a/b/c completed runs)
* **Per-subset**: 20 swebench + 84 taubench + 26 frontsci
* **Created by**: t0027_phase2_5_abc_rerun_with_fixed_b_and_c

## Overview

This predictions asset is the t0027 re-run of variant C on the 130 paired instances inherited from
t0026, produced to address suggestion S-0026-02 (the wrong-delegate defect). In t0026, variant C
delegated to the t0010 `scope_aware_react` agent rather than to a plan-and-solve scaffold, which
made C structurally identical to variant A (scope-aware ReAct) plus mismatched-granularity noise.
Under that delegate, RQ5 ("does scaffold-granularity matter when the agent is plan-and-solve,
holding parser fixed?") was uninterpretable because variant B (plan-and-solve) and variant C (ReAct
+ noise) tested different scaffolds, not the same scaffold under matched/mismatched granularity.

The t0027 re-run uses a new `matched_mismatch_v2` library (`assets/library/matched_mismatch_v2/`)
that forks t0010's mismatch wrapper to delegate to `PlanAndSolveAgentV3` instead of
`scope_aware_react`. The wrapper continues to apply the adversarial granularity perturbation map
(`global -> atomic`, `subtask -> atomic`, `atomic -> global`) to a t0010-style synthetic v2
hierarchy before running the agent, producing the same shape of mismatched conditioning as t0010 but
now over the plan-and-solve scaffold. Concretely, every row in this asset reports
`delegate = "scope_unaware_planandsolve_v3"` — never `scope_aware_react`.

Because the underlying agent is plan_and_solve_v3, the bounded 3-attempt plan-parse recovery chain
(clean -> reprompt -> JSON-mode) and its per-instance diagnostics (`plan_parser_recovery_path`,
`plan_parser_attempts`, `raised_malformed_plan_error`) are inherited unchanged. This means the
C-vs-B McNemar comparison in `code/run_analysis.py` is now a clean "same agent, matched vs
mismatched granularity" contrast, with parser fragility neutralized in both arms.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The wrapper drives plan_and_solve_v3
once per instance with `max_turns=10` and `max_tokens=4096`. Tool registry is the canonical
`build_planandsolve_tool_registry` from t0012 (text-only generic tools). Synthetic v2 hierarchies
are constructed from each problem's `problem_text` using the same 4-phase construction as t0026's
runner.py (verbatim copy in `code/run_abc_rerun.py::_synthetic_annotation`): one global phase
followed by three atomic phases that label sub-portions of the problem text. The adversarial
perturbation map is applied unchanged from t0010.

Cost is tracked via the project CostTracker; per-instance cost is written to the JSONL `cost_usd`
field. Inter-judge agreement subset (30 instances on opus) is *not* re-collected in t0027 — only the
primary sonnet judge runs in this task.

## Data

The 130 paired instances are the intersection of all three t0026 variants' completed instances —
i.e., instances where every variant returned a non-null `judge_sonnet_success`. The exact instance
ids and per-subset breakdown live in `data/paired_manifest.json`. The full 147-instance manifest is
also persisted in `data/instance_manifest.json` for traceability with t0026 even though t0027 only
re-runs the 130-paired subset.

## Prediction Format

JSON Lines — one JSON object per line, identical schema to variant B in this task plus an explicit
`delegate` field. Each row carries:

* `instance_id` (str), `subset` (str ∈ {swebench, taubench, frontsci}), `variant` ("c")
* `final_answer` (str | null), `final_confidence` (float | null; 0..1 verbalised confidence)
* `cost_usd` (float), `trajectory_path` (str | null; per-instance trajectory in `data/runs/c/`)
* `judge_sonnet_success` (bool), `judge_sonnet_rationale` (str)
* `plan_parser_recovery_path` (str ∈ {clean, reprompt, json_mode, all_failed, unknown})
* `plan_parser_attempts` (int ∈ {1, 2, 3})
* `raised_malformed_plan_error` (bool; True iff all three plan-parse attempts failed)
* `delegate` (str = "scope_unaware_planandsolve_v3" on every row in this asset)

The opus inter-judge fields (`judge_opus_success`, `judge_opus_rationale`) are not produced in this
re-run; downstream consumers comparing to t0026 should treat them as absent.

## Metrics

The full set of headline metrics is computed by `code/run_analysis.py` and written to
`results/metrics.json`. The metrics relevant to register at the project level are:

* `success_rate_c_paired` — McNemar success rate for variant C on the 130-paired set
* `parser_failure_rate_c` — fraction of C runs with `raised_malformed_plan_error=True`
* `total_cost_usd_c` — wall-clock cost from CostTracker

Per-subset success-rate breakdowns and the recovery-path distribution table are persisted in
`data/mcnemar_results.json` and the calibration ECE in `data/calibration.json`.

## Main Ideas

* The matched_mismatch_v2 library fixes the structural defect that made t0026's variant C
  meaningless for RQ5: C now delegates to plan_and_solve_v3, so B and C share the same scaffold and
  parser, isolating the granularity-conditioning effect as the only systematic difference.
* The adversarial granularity perturbation policy is preserved verbatim from t0010
  (`global -> atomic`, `subtask -> atomic`, `atomic -> global`), so this task's C results compose
  cleanly with the t0010 matched-mismatch evaluation that established the wrapper's behaviour on a
  different model and scaffold combination.
* All three variants (A, B, C) use the same model — claude-sonnet-4-6. The original t0027 task
  description erroneously stated claude-opus-4-7 for B/C, but t0026 actually ran on Sonnet (verified
  via t0026's `paths.py:60` and trajectory error messages). t0027 was corrected to match. The B-vs-C
  McNemar therefore isolates the granularity-conditioning effect cleanly: same model, same scaffold,
  same parser, only the wrapper differs.

## Summary

This asset re-runs variant C on the 130 paired t0026 instances using the new matched_mismatch_v2
library, which retargets the t0010 mismatch wrapper at plan_and_solve_v3 instead of
`scope_aware_react`. This eliminates the wrong-delegate defect (S-0026-02) that made t0026's variant
C structurally identical to A and rendered RQ5 uninterpretable. Because B and C now share the same
scaffold and parser, the B-vs-C McNemar in `code/run_analysis.py` is a clean test of
granularity-conditioning under the plan-and-solve agent.

The headline finding for this asset will be the difference in success rate between variant B
(matched plan-and-solve) and variant C (mismatched plan-and-solve). If the gap is significant after
Bonferroni correction (α = 0.025), it confirms that scaffold-granularity affects plan-and-solve
performance even when the underlying scaffold and parser are held fixed; if the gap is not
significant, it suggests the granularity-conditioning effect observed in t0010 was scaffold- or
model-specific and does not generalize to plan-and-solve under claude-sonnet-4-6.
