# Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5

## Motivation

The t0025 synthesis answered RQ1-RQ5 using only external literature (the t0017 paper corpus). It
explicitly flagged that there is **zero project-internal runtime evidence** behind those answers.
The t0023 confirmatory ABC run (N>=157) was cancelled after t0019 surfaced a haiku-judge calibration
failure that would have invalidated outcomes.

This task closes that gap with a properly powered, paired A/B/C run on N=147 instances spanning all
three runnable benchmark subsets (SWE-bench Verified, Tau-bench, FrontierScience). The design
produces project-internal evidence for **RQ1, RQ2, RQ3, RQ4** and a properly powered McNemar paired
test for **RQ5**. Total budget envelope: ~$125, hard cap $135.

## Research Questions Targeted

* **RQ1** — Does scope-aware ReAct (variant A) outperform a scope-unaware Plan-and-Solve baseline
  (variant B) on success rate? Tested by paired McNemar across the full N=147.
* **RQ2** — Does mismatched-scope (variant C) underperform A on the same instances? Tested by paired
  McNemar across N=147.
* **RQ3** — How well does a sonnet judge agree with programmatic ground truth on benchmark items
  that have one (SWE-bench tests, FrontierScience exact-match)?
* **RQ4** — What is the calibration (ECE) of the verbalized `final_confidence` field emitted by the
  v2 Plan-and-Solve harness?
* **RQ5** — Does the strict double inequality `success(A) > success(B) > success(C)` hold? At N=147
  with paired binary outcomes, McNemar can detect ~10 percentage-point pairwise gaps with
  alpha=0.025 each (Bonferroni-corrected for the two pairwise tests). Both `success(A) > success(B)`
  and `success(B) > success(C)` must reach significance for RQ5 to be affirmed.

## Scope and Configurations

Three variants, one model under test, one judge per pass with an inter-judge slice.

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
  RQ4 calibration must be cleanly attributable to verbalized confidence, not to a model-skill
  confound.

* **Judge**: `claude-sonnet-4-6` for the primary pass on every instance. `claude-opus-4-7` runs the
  same pass on a 30-instance overlap slice (10 from each benchmark) for inter-judge agreement.
  Programmatic ground truth is used wherever the benchmark provides it (SWE-bench tests,
  FrontierScience exact-answer match). Tau-bench has weaker programmatic ground truth and relies on
  judge plus tool-trace heuristics. **No haiku judge** — this is the t0019 finding, encoded as a
  constraint on this task.

* **Confidence elicitation**: every action emits a numeric `final_confidence in [0, 1]` via the v2
  harness. Variants A and C also emit a per-step confidence using the same field convention.

## Benchmark Slice (N=147)

Composite of N=147 instances drawn from already-downloaded subsets registered in
`t0003_download_benchmark_subsets`. WorkArena++ is excluded (no enumerable instances; requires gated
ServiceNow + HuggingFace access).

* 20 from SWE-bench Verified subset (out of 60 available; programmatic judging via test execution)
* 87 from Tau-bench subset (full subset; tool-trace plus judge)
* 40 from FrontierScience olympiad subset (full subset; programmatic exact-answer match)

Instance selection is reproducible — the planning step records the seed, the source manifest, and
the per-source instance IDs in `data/instance_manifest.json`. The 20 SWE-bench instances are sampled
with stratification across the difficulty buckets in the upstream subset. Each variant runs on the
*same* 147 instances (paired design).

## Metrics (computed for every variant)

* `success_rate` — fraction passing the programmatic check (or judge for items without one)
* `progress_rate` — AgentBoard subgoal progress rate via t0022 (where applicable; tau-bench and
  FrontierScience are single-step so this metric is reported only on SWE-bench)
* `eai_error_breakdown` — counts per Embodied Agent Interface error category via t0022
* `final_confidence_ece` — Expected Calibration Error of `final_confidence` against per-instance
  outcomes
* `judge_agreement_with_program` — agreement rate between sonnet judge and programmatic ground truth
  on items that have both (SWE-bench, FrontierScience)
* `inter_judge_agreement` — sonnet vs opus on the 30-instance overlap slice
* `mcnemar_p_a_vs_b` — paired McNemar p-value for `success(A) > success(B)`
* `mcnemar_p_b_vs_c` — paired McNemar p-value for `success(B) > success(C)`
* Efficiency: `efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`

All metric keys must be registered in `meta/metrics/` before reporting; check with
`uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and add any missing
keys via `/add-metric` during planning.

## Data Handling

* Intermediate artifacts (per-instance traces, per-action JSON, raw judge prompts and responses)
  saved under `data/runs/{variant}/`.
* The fixed N=147 slice is saved as `data/instance_manifest.json` with explicit seed, source IDs,
  and source dataset hashes — required for reproducibility.
* Predictions assets (one per variant) created under `assets/predictions/{variant}/` containing the
  per-instance predictions, confidence values, success labels, and judge responses.

## Compute and Budget

Local-only — no remote machines. All runs hit the Anthropic API directly.

Per-variant cost estimate (sonnet 4.6 agent + sonnet 4.6 judge):

* SWE-bench (20 instances × ~$0.85/instance) ≈ $17 per variant
* Tau-bench (87 instances × ~$0.20/instance) ≈ $17.40 per variant
* FrontierScience (40 instances × ~$0.18/instance) ≈ $7.20 per variant
* Per-variant subtotal: ~$41.60
* Three variants subtotal: ~$125
* Inter-judge slice (opus 4.7 on 30 items): ~$5
* Buffer for retries: ~$5

Total: **about $135 estimated, $145 hard cap**. Current project budget is $200 with $74.08 already
spent, leaving $125.92 — the hard cap fits with $0-20 of slack. The planning step must re-estimate
on real prompt-token measurements before launching the full run; if measurements indicate the cap
will be breached, the SWE-bench slice is the first thing to shrink.

## Key Questions and Falsifiability

1. Is `success(A) > success(B)` significantly at alpha=0.025 (Bonferroni)? Falsifiable: if the
   McNemar test fails to reject, RQ1's project answer becomes "not supported by N=147 evidence."
2. Is `success(B) > success(C)` significantly at alpha=0.025? Falsifiable: if the test fails to
   reject, RQ2 (and RQ5) flip.
3. Does sonnet judge agree with programmatic ground truth at >=90%? Falsifiable: if agreement is
   under 80%, RQ3 reports "judge unreliable even at sonnet."
4. Is ECE on `final_confidence` under 0.15? Falsifiable: if ECE >= 0.20, RQ4 reports "verbalized
   confidence not calibrated at this scale."
5. Strict double inequality `success(A) > success(B) > success(C)`: affirmed only if both pairwise
   tests in (1) and (2) are significant; otherwise reported as direction-only or refuted.

## Outputs

* `assets/predictions/{a_scope_aware,b_plan_and_solve,c_mismatched}/` — three predictions assets
* `results/results_summary.md` — high-level findings against each RQ, with explicit pass/fail per
  falsifiability question
* `results/results_detailed.md` — per-variant tables, per-benchmark breakdowns, reliability diagram,
  EAI error taxonomy table, McNemar contingency tables
* `results/metrics.json` — flat or multi-variant metric record covering every metric listed above
* `results/images/` — at minimum: success_rate_by_variant.png, success_rate_by_benchmark.png,
  ece_reliability_diagram.png, judge_agreement.png, eai_error_breakdown.png

## Cross-References

* **Source motivation**: t0024 brainstorm session 7 (rescope after t0019 calibration finding) and
  t0025 synthesis flagging zero internal evidence for RQ1-RQ5.
* **Replaces (smaller-N)**: t0023_phase2_abc_confirmatory_sonnet_swebench (cancelled).
* **Calibration baseline**: t0019_v2_judge_calibration_sonnet — informs the "no haiku judge"
  constraint on this run.
* **Harness reliability**: t0020_v2_truncation_vs_schema_ablation — informs the prompt-schema and
  truncation choices used by the harness.
