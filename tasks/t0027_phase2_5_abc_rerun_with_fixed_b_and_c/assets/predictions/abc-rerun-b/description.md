---
spec_version: "2"
predictions_id: "abc-rerun-b"
documented_by_task: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
date_documented: "2026-05-02"
---
# Variant B (re-run): plan_and_solve_v3 with bounded plan-recovery chain

## Metadata

* **Variant**: b
* **Model**: claude-sonnet-4-6 (Anthropic CLI transport, 10-turn cap, 4096 max output tokens)
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 130 (paired set; intersection of t0026 a/b/c completed runs)
* **Per-subset**: 20 swebench + 84 taubench + 26 frontsci
* **Created by**: t0027_phase2_5_abc_rerun_with_fixed_b_and_c

## Overview

This predictions asset is the t0027 re-run of variant B on the 130 paired instances inherited from
t0026, produced to address suggestion S-0026-01 (B's parser fragility under the v2 plan parser). In
t0026, 16 of 130 paired runs of variant B (12.3%) collapsed to MalformedPlanError because the
single-shot plan parser could not recover from common model formatting drift (numbered lists with
non-canonical separators, prose preambles, bracketed step labels). Those failures contaminated the
A-vs-B paired McNemar comparison since they appeared as agent-level failures rather than capability
ceilings.

The t0027 re-run replaces the v2 agent with a new plan_and_solve_v3 library
(`assets/library/plan_and_solve_v3/`) that wraps the same v2 plan/solve loop with a bounded
3-attempt plan-parse recovery chain:

1. **Clean** — the standard PS+ template; if `parse_plan` succeeds, return immediately.
2. **Reprompt** — on first parse failure, re-issue the planner call with a short corrective preamble
   asking the model to format the plan as a clean numbered list.
3. **JSON-mode** — on second parse failure, issue a third call that forces JSON-mode output and
   parses the steps from a structured payload.
4. **all_failed** — if all three attempts fail, the agent re-raises MalformedPlanError exactly as v2
   did, so the failure is still observable but is now bounded by the chain rather than by a single
   fragile pass.

Each per-instance prediction records which path was taken (`plan_parser_recovery_path` ∈ {clean,
reprompt, json_mode, all_failed, unknown}) and the number of attempts used (`plan_parser_attempts` ∈
{1, 2, 3}). The `raised_malformed_plan_error` boolean is True iff all three attempts failed.

The asset shares the schema and judge wiring with t0026's `b-plan-and-solve` so paired McNemar
analyses (A vs B in this task; B-old vs B-new across t0026 and t0027 by joining on instance_id) can
re-use the same instance manifest and the same primary sonnet judge.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The agent runs the plan_and_solve_v3
scaffold with `max_turns=10` and `max_tokens=4096` per call. Tool registry is the canonical
`build_planandsolve_tool_registry` from t0012 (text-only generic tools — no scope-aware tools, no
filesystem, no shell). Cost is tracked in-memory via the project CostTracker; per-instance cost is
written to the JSONL `cost_usd` field. Inter-judge agreement subset (30 instances on opus) is *not*
re-collected in t0027 — only the primary sonnet judge runs in this task.

## Data

The 130 paired instances are the intersection of all three t0026 variants' completed instances —
i.e., instances where every variant returned a non-null judge_sonnet_success. The exact instance ids
and subset breakdown live in `data/paired_manifest.json`. The full 147-instance manifest is also
persisted in `data/instance_manifest.json` for traceability with t0026 even though t0027 only
re-runs the 130-paired subset.

## Prediction Format

JSON Lines — one JSON object per line, identical schema to t0026's `b-plan-and-solve` plus three new
diagnostic fields. Each row carries:

* `instance_id` (str), `subset` (str ∈ {swebench, taubench, frontsci}), `variant` ("b")
* `final_answer` (str | null), `final_confidence` (float | null; 0..1 verbalised confidence)
* `cost_usd` (float; per-instance cost from CostTracker)
* `trajectory_path` (str | null; absolute path to the per-instance trajectory JSON in
  `data/runs/b/`)
* `judge_sonnet_success` (bool), `judge_sonnet_rationale` (str)
* `plan_parser_recovery_path` (str ∈ {clean, reprompt, json_mode, all_failed, unknown})
* `plan_parser_attempts` (int ∈ {1, 2, 3})
* `raised_malformed_plan_error` (bool; True iff all three plan-parse attempts failed)

The opus inter-judge fields (`judge_opus_success`, `judge_opus_rationale`) are not produced in this
re-run; downstream consumers comparing to t0026 should treat them as absent.

## Metrics

The full set of headline metrics is computed by `code/run_analysis.py` and written to
`results/metrics.json`. The most relevant ones to register at the project level are:

* `success_rate_b_paired` — McNemar success rate for variant B on the 130-paired set
* `parser_failure_rate_b` — fraction of B runs with `raised_malformed_plan_error=True` (target:
  significantly below the 12.3% observed in t0026)
* `total_cost_usd_b` — wall-clock cost from CostTracker

Per-subset success-rate breakdowns and the recovery-path distribution table are persisted in
`data/mcnemar_results.json` and the calibration ECE in `data/calibration.json`.

## Main Ideas

* The v3 fallback chain restores B as a viable agent under model formatting drift. The recovery path
  distribution itself is a useful diagnostic: instances landing on `reprompt` or `json_mode`
  identify families of problems where the model's natural plan format diverges from PS+ template
  expectations.
* All three variants (A, B, C) use the same model — claude-sonnet-4-6. The original t0027 task
  description erroneously stated claude-opus-4-7, but t0026 actually ran on Sonnet (verified via
  t0026's `paths.py:60` and trajectory error messages). t0027 was corrected to match. The A-vs-B
  McNemar is therefore a clean comparison: same model, different scaffold (scope-aware ReAct vs
  plan-and-solve with v3 fault-tolerant parser).
* The 130-paired filter ensures the McNemar test in `data/mcnemar_results.json` is a true
  paired-difference test on the same instances across variants, with Bonferroni-corrected α = 0.025.

## Summary

This asset re-runs variant B on the 130 paired t0026 instances using the new plan_and_solve_v3
library that we developed in this task to fix the MalformedPlanError defect that contaminated 12.3%
of t0026's variant-B runs. The new agent retains the v2 plan/solve loop but adds a bounded
three-attempt plan-parse recovery chain (clean -> re-prompt -> JSON-mode), records the recovery path
taken on each instance, and only re-raises MalformedPlanError when all three attempts fail.

The headline finding for this asset will be the new variant-B parser-failure rate (target:
substantially below 12.3%) and the recovery-path distribution that diagnoses *which* recovery
strategy was needed for each instance. The McNemar A-vs-B analysis in `code/run_analysis.py`
re-evaluates RQ1 ("does the scope-aware ReAct scaffold beat plan-and-solve under a fair parser?")
under the fixed parser. Since A and B share claude-sonnet-4-6, the McNemar isolates the
scaffold/parser difference. The B-vs-C McNemar addresses RQ5 ("does scaffold-granularity matter when
the agent is plan-and-solve, holding parser fixed?") and is now meaningful for the first time
because t0027's variant C delegates to plan_and_solve_v3 as well, eliminating the C-vs-A
delegate-conflation defect (S-0026-02) that made t0026's RQ5 uninterpretable.
