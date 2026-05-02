# Phase 2 A/B/C Runtime Smoke (N=30) for RQ1-RQ5

## Motivation

The t0025 synthesis answered RQ1-RQ5 using only external literature (the t0017 paper corpus). It
explicitly flagged that there is **zero project-internal runtime evidence** behind those answers.
The t0023 confirmatory ABC run (N>=157) was cancelled after t0019 surfaced a haiku-judge calibration
failure that would have invalidated outcomes.

This task closes that gap with a small, sharp, self-contained run that produces project-internal
evidence for **RQ1, RQ2, RQ3, RQ4** and direction-only signal for **RQ5** — within a ~$60 envelope.

## Research Questions Targeted

* **RQ1** — Does scope-aware ReAct (variant A) outperform a scope-unaware Plan-and-Solve baseline
  (variant B) on success rate?
* **RQ2** — Does mismatched-scope (variant C) underperform A on the same instances?
* **RQ3** — How well does a sonnet judge agree with programmatic ground truth on benchmark items
  that have one?
* **RQ4** — What is the calibration (ECE) of the verbalized `final_confidence` field emitted by the
  v2 Plan-and-Solve harness?
* **RQ5** — Does the strict double inequality `success(A) > success(B) > success(C)` hold in
  *direction* at N=30? Strict-inequality testing is explicitly out of scope at this N — this run
  reports direction and rough effect size only, with a power note.

## Scope and Configurations

Three variants, one model under test, one judge, one composite N=30 benchmark slice.

* **Variant A (scope-aware ReAct)** — uses the library produced by
  `t0006_scope_aware_react_library`. Each step receives the explicit scope description from the
  benchmark item.

* **Variant B (scope-unaware Plan-and-Solve v2)** — uses the library produced by
  `t0021_plan_and_solve_v2_with_final_confidence`. Plans the full solution, executes, emits
  `final_confidence` at the end of every action.

* **Variant C (mismatched-scope ReAct)** — uses the library produced by
  `t0010_matched_mismatch_library` to deliberately feed the wrong scope description. Same step
  structure as A.

* **Model under test (all variants)**: `claude-sonnet-4-6`. No haiku model under test in this run —
  cost is dominated by judge passes, not the agent.

* **Judge**: `claude-sonnet-4-6` rotated against `claude-opus-4-7` for a small (10-instance)
  inter-judge agreement check. Programmatic ground truth is used wherever the benchmark provides it
  (SWE-bench Verified Lite test execution, FrontierMath answer match). **No haiku judge** — this is
  the t0019 finding, encoded as a constraint on this task.

* **Confidence elicitation**: every action emits a numeric `final_confidence ∈ [0, 1]` via the v2
  harness. Variants A and C also emit a per-step confidence using the same field convention.

## Benchmark Slice (N=30)

Composite of N=30 instances drawn from already-downloaded subsets registered in
`t0003_download_benchmark_subsets`. Exact composition is decided in the planning step; the default
mix is:

* 10 from SWE-bench Verified Lite (programmatic judging via test execution)
* 10 from AgentBoard (programmatic subgoal-progress signal via t0022 harness)
* 10 from FrontierMath (programmatic exact-answer match)

Instance selection is reproducible — the planning step records the seed, the source manifest, and
the per-source instance IDs in `data/instance_manifest.json`. Each variant runs on the *same* 30
instances (paired design).

## Metrics (computed for every variant)

* `success_rate` — fraction passing the programmatic check (or judge for items without one)
* `progress_rate` — AgentBoard subgoal progress rate via t0022
* `eai_error_breakdown` — counts per Embodied Agent Interface error category via t0022
* `final_confidence_ece` — Expected Calibration Error of `final_confidence` against per-instance
  outcomes
* `judge_agreement_with_program` — agreement rate between sonnet judge and programmatic ground truth
  on items that have both
* `inter_judge_agreement` — sonnet vs opus on the 10-instance overlap slice
* Efficiency: `efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`

All metric keys must be registered in `meta/metrics/` before reporting; check with
`uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and add any missing
keys via `/add-metric` during planning.

## Data Handling

* Intermediate artifacts (per-instance traces, per-action JSON, raw judge prompts and responses)
  saved under `data/runs/{variant}/`.
* The fixed N=30 slice is saved as `data/instance_manifest.json` with explicit seed, source IDs, and
  source dataset hashes — required for reproducibility.
* Predictions assets (one per variant) created under `assets/predictions/{variant}/` containing the
  per-instance predictions, confidence values, success labels, and judge responses.

## Compute and Budget

Local-only — no remote machines. All runs hit the Anthropic API directly.

Per-variant cost estimate (sonnet 4.6 agent + sonnet 4.6 judge):

* Agent inference: ~10K input + 4K output tokens per instance × 30 instances ≈ $4-5 per variant
* Judge pass: ~6K input + 1K output tokens per instance × 30 ≈ $2-3 per variant
* Inter-judge slice (opus 4.7 on 10 items): ~$2

Total: about $18-24 (3 variants × $6-8) + $2 inter-judge + $5 buffer for retries and failures =
**about $25-31 estimated, $60 hard cap**.

## Key Questions and Falsifiability

1. Is `success(A) > success(B)` at N=30 (direction-only)? Falsifiable: if A ≤ B, RQ1's project
   answer flips from "supported" to "not supported by N=30 evidence."
2. Is `success(C) < success(A)` at N=30 (direction-only)? Falsifiable: if C ≥ A, RQ2's answer flips.
3. Does sonnet judge agree with programmatic ground truth at >=90%? Falsifiable: if agreement is
   under 80%, RQ3 reports "judge unreliable even at sonnet."
4. Is ECE on `final_confidence` under 0.15? Falsifiable: if ECE >= 0.20, RQ4 reports "verbalized
   confidence not calibrated at N=30 sample size."
5. Direction `success(A) > success(B) > success(C)`: falsifiable by any rank inversion. Statistical
   significance not claimed at N=30 — explicit power note in `results_detailed.md`.

## Outputs

* `assets/predictions/{a_scope_aware,b_plan_and_solve,c_mismatched}/` — three predictions assets
* `results/results_summary.md` — high-level findings against each RQ, with the direction-only RQ5
  caveat
* `results/results_detailed.md` — per-variant tables, per-benchmark breakdowns, reliability diagram,
  EAI error taxonomy table
* `results/metrics.json` — flat or multi-variant metric record covering every metric listed above
* `results/images/` — at minimum: success_rate_by_variant.png, ece_reliability_diagram.png,
  judge_agreement.png, eai_error_breakdown.png

## Cross-References

* **Source motivation**: t0024 brainstorm session 7 (rescope after t0019 calibration finding) and
  t0025 synthesis flagging zero internal evidence for RQ1-RQ5.
* **Replaces (smaller-N)**: t0023_phase2_abc_confirmatory_sonnet_swebench (cancelled).
* **Calibration baseline**: t0019_v2_judge_calibration_sonnet — informs the "no haiku judge"
  constraint on this run.
* **Harness reliability**: t0020_v2_truncation_vs_schema_ablation — informs the prompt-schema and
  truncation choices used by the harness.
