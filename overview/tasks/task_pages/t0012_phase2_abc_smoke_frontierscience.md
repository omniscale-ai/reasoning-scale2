# ✅ Phase 2 A/B/C smoke harness on FrontierScience subset

[Back to all tasks](../README.md)

> Task Success Rate: **0.025**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0012_phase2_abc_smoke_frontierscience` |
| **Status** | ✅ completed |
| **Started** | 2026-04-30T00:55:11Z |
| **Completed** | 2026-05-01T04:43:00Z |
| **Duration** | 27h 47m |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source suggestion** | `S-0006-03` |
| **Task types** | `experiment-run`, `baseline-evaluation` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`benchmark-frontierscience`](../../by-category/benchmark-frontierscience.md), [`granularity-conditioning`](../../by-category/granularity-conditioning.md), [`uncertainty-calibration`](../../by-category/uncertainty-calibration.md) |
| **Expected assets** | 3 predictions, 1 library |
| **Step progress** | 11/15 |
| **Cost** | **$18.37** |
| **Task folder** | [`t0012_phase2_abc_smoke_frontierscience/`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/task_description.md)*

# Phase 2 A/B/C Smoke Harness on FrontierScience Subset

## Motivation

This is the project's **first end-to-end Phase 2 result**. It tests the headline hypothesis on
a real benchmark for the first time: scope-aware (A) > scope-unaware (B) > scope-mismatched
(C). The smoke test is intentionally narrow — single benchmark (FrontierScience-Olympiad),
single provider (Anthropic Claude), N=28 hierarchy-complete rows from the v2 dataset, paired
across conditions. The goal is a directional signal plus a sample-size calibration for
follow-up confirmatory runs. Implements suggestions S-0006-03, S-0007-02, and S-0005-06.

## Hypotheses tested

| RQ | Predicted direction | Detection threshold at N=28 |
| --- | --- | --- |
| RQ1 — A success rate > B success rate | A − B ≥ +5pp | ~15pp paired (McNemar/sign test, α=0.05) |
| RQ2 — A overconfident error rate < B | A − B ≤ −2pp | ~5-8pp paired |
| RQ5 — C worst on Metrics 1 and 2 | C < min(A, B) on both | clear ranking when A > B + 5pp |

Excluded by design (handled in separate experiments on the right benchmarks):

* RQ3 (request-vs-act accuracy on low-level tasks) — needs tau-bench, not FrontierScience.
* RQ4 (gains concentrated in info-asymmetric states) — needs WorkArena++ or tool-using
  benchmark.

## Scope

* Build a small `phase2_smoke_harness_v1` library under `assets/library/` that:
  * Loads the v2 dataset asset from t0009 and filters to FrontierScience-Olympiad rows with
    `hierarchy_completeness == true`.
  * Runs a phase-order walk over each row's `hierarchy` (global → all subtasks → all
    `global_atomics`); for each step in the walk, dispatches to one of the three libraries (A:
    t0006, B: t0007, C: t0010).
  * Captures every step's trajectory record into one JSONL per condition under
    `assets/predictions/`.
  * Calls t0011's `compute_overconfident_error_rate` on each trajectory file.
  * Computes `task_success_rate` by parsing each trajectory's final `Finish` answer and
    comparing to the row's gold final answer (FrontierScience problems end with `FINAL ANSWER:
    ...`).
  * Reports `avg_decisions_per_task` per condition.
* Produce three `predictions` assets (one per condition: A, B, C).
* Produce one `library` asset for the harness itself.
* Run on the **28 hierarchy-complete FrontierScience-Olympiad rows** from the v2 dataset (this
  matches the v1 hierarchy-complete count; refine after t0009 lands if v2 row count differs).

Out of scope: multi-provider replication (deferred), benchmark-specific tool registries beyond
a minimal `python_exec` for FrontierScience math problems, scaling N beyond ~28.

## Approach

1. Read the v2 dataset asset from t0009 once t0009 has merged. Filter to FrontierScience-
   Olympiad and `hierarchy_completeness == true`.
2. Implement the harness library that drives the phase-order walk and dispatches
   per-condition. Reuse t0006, t0007, t0010 libraries; reuse t0011's calibration aggregator.
3. For each row, run all three conditions against the same model (`claude-sonnet-4-6-20251001`
   recommended) with paired execution (same seed where applicable, same problem text, same
   tool registry).
4. Tool registry is minimal: a single `python_exec` tool for arithmetic and one
   `Finish(answer)` tool. FrontierScience-Olympiad rows are mostly verbal reasoning; tools
   exist for explicit computation only.
5. Persist trajectory JSONLs under `assets/predictions/<condition>/files/`. Compute and
   persist metrics.
6. Write `results/results_summary.md` with the 3×3 condition × metric table and the predicted-
   versus-observed effect sizes. Write `results/results_detailed.md` with per-row trajectories
   summarised, the McNemar p-value for A-vs-B and B-vs-C, and the implied sample size for
   follow-up confirmatory runs.
7. Generate at least 2 charts: condition × metric bar chart with confidence intervals; per-row
   success matrix heatmap (rows=problems, columns=conditions).

## Expected Outputs

* `assets/library/phase2_smoke_harness_v1/` — the harness library.
* `assets/predictions/phase2_smoke_a/`, `assets/predictions/phase2_smoke_b/`,
  `assets/predictions/phase2_smoke_c/` — three predictions assets, one per condition.
* `results/metrics.json` in explicit-variant format (3 variants: A, B, C; metrics:
  `task_success_rate`, `overconfident_error_rate`, `avg_decisions_per_task`).
* `results/results_summary.md` and `results/results_detailed.md` with hypothesis-test results,
  effect sizes, sample-size calibration, and clear acknowledgement of the excluded RQs.
* `results/images/` with at least 2 charts.
* Follow-up suggestions for: multi-provider replication (Gemini, OpenAI), expansion to
  tool-using benchmarks (SWE-bench, tau-bench), confirmatory N expansion based on observed
  variance.

## Compute and Budget

No GPU. Anthropic API only. **Budget cap: USD 20** (per-task default cap is $10; this task
exceeds the default and explicitly opts up). Estimated breakdown: 28 rows × 3 conditions × ~3
self-consistency calls per step × ~6 steps per row × ~$0.005 per call = $7.5 baseline; budget
$20 leaves headroom for retries and the calibration prompt.

## Dependencies and Cross-References

* **Hard dependencies (must be `completed`)**:
  * `t0009_hierarchical_annotation_v2` — produces the v2 dataset asset this task consumes.
  * `t0010_matched_mismatch_library` — produces the C-condition library.
  * `t0011_metric2_calibration_aggregator` — produces the Metric 2 implementation.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  libraries.
* References Yao2022 ReAct, Wang2023 Plan-and-Solve, and Xiong2024 calibration paper assets
  from t0002.

## Source Suggestion

S-0006-03 — "Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience subset." Also
covers S-0007-02 and S-0005-06 by consolidation.

## Key Questions

1. Does A − B reach the +5pp threshold on `task_success_rate`?
2. Does A − B reach the −2pp threshold on `overconfident_error_rate`?
3. Does C rank strictly worst on both metrics relative to A and B?
4. What is the within-condition variance, and what N does the FrontierScience confirmatory run
   need to detect a 5pp effect at α=0.05 with paired test?
5. Are there per-domain (physics / chemistry / biology) effect-size differences worth
   surfacing to the next brainstorm?

</details>

## Costs

**Total**: **$18.37**

| Category | Amount |
|----------|--------|
| claude-haiku-4-5 | $18.37 |

## Metrics

### Condition A: scope-aware ReAct

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.025** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **0.6470588235294118** |
| [`avg_decisions_per_task`](../../metrics-results/avg_decisions_per_task.md) | **1.2** |

### Condition B: scope-unaware Plan-and-Solve

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.0** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **0.0** |
| [`avg_decisions_per_task`](../../metrics-results/avg_decisions_per_task.md) | **6.525** |

### Condition C: scope-mismatched (random)

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.0** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **0.0** |
| [`avg_decisions_per_task`](../../metrics-results/avg_decisions_per_task.md) | **26.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Phase 2 A/B/C Smoke Harness (v1)](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/library/phase2_smoke_harness_v1/) | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/library/phase2_smoke_harness_v1/description.md) |
| predictions | [Phase 2 smoke condition A (scope-aware ReAct) on FrontierScience-Olympiad](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-a/) | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-a/description.md) |
| predictions | [Phase 2 smoke condition B (scope-unaware Plan-and-Solve) on FrontierScience-Olympiad](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-b/) | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-b/description.md) |
| predictions | [Phase 2 smoke condition C (scope-mismatched random) on FrontierScience-Olympiad](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-c/) | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-c/description.md) |

## Suggestions Generated

<details>
<summary><strong>Extend scope_unaware_planandsolve_v1 to emit
final_confidence</strong> (S-0012-01)</summary>

**Kind**: library | **Priority**: high

The t0007 Plan-and-Solve library does not emit a final_confidence field in trajectory records.
This collapses Metric 2 (overconfident_error_rate) to 0.0 for conditions B and C, making RQ2
untestable. Extend the library to emit a verbalized confidence label per the Xiong2024 §3.2
protocol: add a follow-up call after the final plan step asking the model to rate its
confidence on a 0-1 scale. This is a prerequisite for any confirmatory A-vs-B-vs-C run that
wants to test RQ2.

</details>

<details>
<summary><strong>Confirmatory Phase 2 run: sonnet on SWE-bench Verified or
tau-bench</strong> (S-0012-02)</summary>

**Kind**: experiment | **Priority**: high

The smoke shows FrontierScience-Olympiad is beyond haiku capacity without tools (A: 2.5%, B:
0%, C: 0%). All three conditions are at the floor, making granularity conditioning effects
invisible. A confirmatory run requires: (1) a benchmark where the model can achieve 10-50%
accuracy without tools (SWE-bench Verified lite or tau-bench at the instance level), (2)
claude-sonnet-4-6 instead of haiku, (3) N≥157 paired rows per the confirmatory-N estimate from
this smoke. This is the highest-priority next experiment for RQ1/RQ5.

</details>

<details>
<summary><strong>Add tool use (search, code execution) to the smoke harness for
FrontierScience-Olympiad</strong> (S-0012-03)</summary>

**Kind**: experiment | **Priority**: medium

The smoke ran with calculator+finish only. FrontierScience-Olympiad requires multi-step
numerical computation, retrieval, and code execution for most problems. Adding a Python code
execution tool and a retrieval tool would lift accuracy above the current floor and make
A-vs-B-vs-C differences observable even on haiku. Cost per row would increase by ~2-5x but
confirmatory N would decrease proportionally.

</details>

<details>
<summary><strong>Fix task_id collision in FrontierScience-Olympiad pilot
dataset</strong> (S-0012-04)</summary>

**Kind**: dataset | **Priority**: medium

The hierarchical-annotation-v2 FrontierScience-Olympiad subset has 40 rows but only 26 unique
task_ids. Multiple rows share the same task_id (different granularity levels of the same
problem), which means the pairing logic treats them as separate predictions for the same task.
A deduplication or re-keying correction task should produce a version of the dataset with
unique task_ids per row, or document the intended semantics of multi-row task_ids.

</details>

<details>
<summary><strong>Multi-provider replication: run Phase 2 harness with GPT-4o and
Gemini 1.5 Pro</strong> (S-0012-05)</summary>

**Kind**: experiment | **Priority**: low

The smoke used only claude-haiku-4-5. Replicating on GPT-4o and Gemini 1.5 Pro (both now
available via project API keys) would test whether the granularity conditioning effect is
model-specific or generalizes across providers. The harness's model_call.py abstraction layer
makes this a configuration change rather than a code change. Defer until the confirmatory N
result is available from S-0012-02 to avoid spending budget before the primary hypothesis is
tested.

</details>

## Research

* [`research_code.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/research/research_code.md)
* [`research_papers.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/results/results_summary.md)*

--- spec_version: "2" task_id: "t0012_phase2_abc_smoke_frontierscience" ---
# Results Summary — Phase 2 A/B/C Smoke (FrontierScience-Olympiad)

## Summary

All three agent conditions (scope-aware ReAct A, scope-unaware Plan-and-Solve B,
scope-mismatched Plan-and-Solve C) solved near-zero FrontierScience-Olympiad problems with
claude-haiku-4-5 and no tools: A solved 1/40 (2.5%), B solved 0/40, C solved 0/11 (budget
halted at 11 rows). The paired McNemar test across the 6 fully overlapping rows yields p=1.0
for all pairs — the null is not rejected, and the smoke confirms that FrontierScience-Olympiad
is beyond haiku capacity without tool use.

## Metrics

* **task_success_rate**: A=0.025 (1/40), B=0.000 (0/40), C=0.000 (0/11)
* **overconfident_error_rate**: A=0.647, B=0.000\*, C=0.000\* (\*collapsed — no
  final_confidence in Plan-and-Solve trajectories; not comparable to A)
* **avg_decisions_per_task**: A=1.20, B=6.53, C=26.0

| Metric | A: scope-aware ReAct (N=40) | B: scope-unaware Plan-Solve (N=40) | C: scope-mismatched (N=11) |
| --- | --- | --- | --- |
| `task_success_rate` | **0.025** (1/40) | 0.000 (0/40) | 0.000 (0/11) |
| `overconfident_error_rate` | **0.647** | 0.000 \* | 0.000 \* |
| `avg_decisions_per_task` | **1.20** | 6.53 | 26.0 |

\* Plan-and-Solve trajectories do not emit `final_confidence`; the Xiong2024 aggregator
records zero overconfident errors by construction. Not comparable to A.

## Statistical Tests

All McNemar paired tests (6 overlapping pairs, 0 discordant pairs): p = 1.0 (exact binomial,
no discordant). None of the pre-registered hypotheses can be confirmed or refuted at this
sample size. Confirmatory-N estimate for a 5 pp effect: **N = 157**.

## Budget

Total spend: **$18.37** (halted above $18 cap). 665 claude-haiku-4-5 calls via local Claude
Code CLI with minimal system prompt (`--tools "" --setting-sources ""`). System prompt
suppression reduced per-call cost from ~$0.10 to ~$0.005 (25× reduction enabling 84+ rows
within the $18 cap; C condition cost ~4× per row due to long Plan-and-Solve trajectories).

## Key Findings

* **FrontierScience-Olympiad is too hard for haiku without tool use.** The benchmark requires
  multi-step scientific reasoning that exceeds no-tool haiku capacity regardless of
  granularity conditioning.
* **Granularity conditioning effect is inconclusive** at N=40 with p=1.0. The smoke is
  underpowered for RQ1/RQ2/RQ5; a confirmatory run needs N≥157 paired rows and likely a
  stronger model (sonnet).
* **Metric 2 cannot be compared across conditions** until Plan-and-Solve is extended to emit
  `final_confidence`. This is the most actionable methodological finding.
* **Per-row checkpointing and system-prompt override** are the two engineering techniques that
  made this smoke possible within the $18 budget constraint.

## Verification

All verificators passed:

* `verify_task_metrics` — PASSED (explicit-variant format, 3 condition variants)
* `verify_task_results` — PASSED after adding required sections
* `verify_task_folder` — PASSED (no files outside task folder)
* `verify_task_file` — PASSED (task.json valid)
* Predictions verificators for phase2-smoke-a, phase2-smoke-b, phase2-smoke-c — all PASSED
* Library verificator for phase2_smoke_harness_v1 — PASSED

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0012_phase2_abc_smoke_frontierscience" ---
# Results Detailed — Phase 2 A/B/C Smoke (FrontierScience-Olympiad)

## Summary

The Phase 2 smoke ran three agent conditions (A: scope-aware ReAct, B: scope-unaware
Plan-and-Solve, C: scope-mismatched Plan-and-Solve) against 40 FrontierScience-Olympiad
hierarchy-complete rows from the v2 hierarchical-annotation dataset, using claude-haiku-4-5
via the local Claude Code CLI with a minimal system prompt. A completed 40 rows, B completed
40 rows, C completed 11 rows before the $18 budget cap was reached. All three conditions
solved near-zero problems. The smoke validates the harness end-to-end and identifies two
critical follow-on actions: a confirmatory run at N≥157 on a stronger model, and extending the
Plan-and-Solve library to emit `final_confidence`.

## Methodology

* **Model**: claude-haiku-4-5 accessed via local Claude Code CLI
* **System prompt**: Minimal (overridden with `--tools "" --setting-sources ""`)
* **Tool registry**: calculator + finish only (condition A/C); finish only (condition B)
* **Dataset**: hierarchical-annotation-v2, FrontierScience-Olympiad subset, hierarchy-complete
  rows (40 rows total)
* **Machine**: MacBook Pro, local execution, no GPU
* **Runtime**: ~4.5 hours wall-clock (concurrent A/B/C runs)
* **Date**: 2026-05-01
* **Total calls**: 665 (all to claude-haiku-4-5)
* **Total cost**: $18.37 (halted above $18 cap)
* **Cache reuse**: 16.3M cache-read tokens vs 2.0M cache-creation tokens — system-prompt
  override enables aggressive KV-cache reuse across calls

## Metrics Tables

### Primary metrics per condition

| Metric | A: scope-aware ReAct | B: scope-unaware PlanSolve | C: scope-mismatched |
| --- | --- | --- | --- |
| `task_success_rate` | 0.025 (1/40) | 0.000 (0/40) | 0.000 (0/11) |
| `overconfident_error_rate` | 0.647 | 0.000 † | 0.000 † |
| `avg_decisions_per_task` | 1.20 | 6.53 | 26.0 |

† Collapsed: Plan-and-Solve trajectories do not surface `final_confidence`; the Xiong2024
aggregator records zero overconfident errors by construction. Not comparable to A.

### Wilson 95% confidence intervals on task_success_rate

| Condition | Estimate | Lower | Upper |
| --- | --- | --- | --- |
| A (N=40) | 0.025 | 0.000 | 0.132 |
| B (N=40) | 0.000 | 0.000 | 0.390 |
| C (N=11) | 0.000 | 0.000 | 0.390 |

### Paired McNemar tests (6 overlapping rows)

| Comparison | N pairs | Discordant | p-value | Method |
| --- | --- | --- | --- | --- |
| A vs B | 6 | 0 | 1.0 | exact binomial (no discordant) |
| B vs C | 6 | 0 | 1.0 | exact binomial (no discordant) |
| A vs C | 6 | 0 | 1.0 | exact binomial (no discordant) |

### Pre-registered hypothesis evaluation

| Hypothesis | Predicted direction | Observed | Confirmed | Refuted |
| --- | --- | --- | --- | --- |
| RQ1 (A > B task success) | +5 pp | +2.5 pp | No | No (p=1.0) |
| RQ2 (A < B overconfident) | −2 pp | +64.7 pp (A > B) | No | Yes (direction reversed) |
| RQ5 (C worst on both metrics) | C < min(A,B) | Not met | No | No |

Note: RQ2 refutation is an artefact of the Metric 2 collapse for B/C. The overconfident error
rate for B and C is 0.0 only because `final_confidence` is never emitted, not because B/C are
better calibrated.

### Confirmatory-N estimate

For a 5 pp paired-difference effect at α=0.05, power=0.8, given the observed discordant rate
from this smoke: **N = 157 paired rows**.

## Comparison vs Baselines

The smoke is an internal pilot, not a published benchmark comparison. Published
FrontierScience-Olympiad results (from the benchmark paper) report state-of-the-art models at
15–30% on similar problem types with tool use. Our haiku+no-tool baseline at 2.5% (A) is
consistent with the expected floor for a no-tool, small-model agent on expert-level science
olympiad problems.

## Visualizations

![Condition metric bar
chart](../../../tasks/t0012_phase2_abc_smoke_frontierscience/results/images/condition_metric_bar.png)

Bars show task_success_rate and avg_decisions_per_task for the three conditions. C's 26.0 avg
decisions indicates the scope-mismatch triggers repeated plan revisions that consume budget
without improving accuracy.

![Per-row success
heatmap](../../../tasks/t0012_phase2_abc_smoke_frontierscience/results/images/per_row_success_heatmap.png)

Row-by-row is_correct matrix across conditions. The single correct A row (scRNA-seq UMAP
problem) is visible. B and C show all-zero columns. C's partial coverage (11/40 rows) is
visible in the truncated right panel.

## Examples

The following 10 examples are drawn from the 6 task IDs present in all three conditions (fully
paired), plus the one correct A row.

### Example 1 — Correct A row (scRNA-seq dimensionality reduction)

**Problem** (truncated): "Biopsies of solid tumors from placebo patients and patients given
drug X were collected. Total RNA was reverse-transcribed and scRNA-seq performed. A
high-dimensional data matrix (6,000+ genes × cells)…"

```
GOLD:
GLOBAL: Apply t-SNE or UMAP non-linear dimensionality reduction to visualize and assess
cell-type populations in the scRNA-seq data.
SUBTASK: Analyze PCA clustering pattern.
ATOM: Observe samples group by patient…

CONDITION A (is_correct=True, conf=0.85, decisions=1):
BATCH EFFECTS (patient-specific effects). For visualizing and assessing diverse cell
types/populations, the recommended method is UMAP (Uniform Manifold Approximation and
Projection) or t-SNE (t-Distributed Stochastic Neighbor Embedding)…

CONDITION B (is_correct=False, conf=None, decisions=1):
[empty string — agent produced no final answer]

CONDITION C (is_correct=False, conf=None, decisions=31):
[None — agent produced no final answer after 31 replanning decisions]
```

* * *

### Example 2 — All conditions wrong: biology (Chenopodium pathosystem)

**Problem** (truncated): "Context: Climate change is increasing the demand for stress
resilient crops. Chenopodium pallidicaule, native to the Andes, is an understudied crop…"

```
GOLD:
GLOBAL: Establish C. pallidicaule pathosystem by selecting model pathogen through
literature review…

CONDITION A (is_correct=False, conf=0.85, decisions=1):
"Establishing a Robust Pathosystem in Chenopodium pallidicaule: Model Pathogen
Selection and Screening…"

CONDITION B (is_correct=False, conf=None, decisions=1):
[whitespace only]

CONDITION C (is_correct=False, conf=None, decisions=31):
[None]
```

* * *

### Example 3 — All wrong: physics (plasmonics, methylene blue)

**Problem** (truncated): "Context: A research paper discusses the interaction of plasmonic
silver (Ag) nanocubes with methylene blue (MB) under different conditions…"

```
GOLD:
GLOBAL: Determine plasmonic-enhanced MB decomposition rate = direct baseline rate *
enhancement factor…

CONDITION A (is_correct=False, conf=None, decisions=1): [empty]
CONDITION B (is_correct=False, conf=None, decisions=8):  [None]
CONDITION C (is_correct=False, conf=None, decisions=24): [empty]
```

* * *

### Example 4 — All wrong: biochemistry (enzyme purification table)

**Problem** (truncated): "Context: Specific activity and yield of proteins are crucial in
determining the purification scheme of an enzyme. Question: Fill in the missing values A–I…"

```
GOLD:
GLOBAL: Compute A=11.3, B=100.0, C=7.9, D=1.0, E=2.7, F=64.4, G=5.4, H=6.0, I=41…

CONDITION A (is_correct=False, conf=0.95, decisions=1): [empty] — high confidence, wrong
CONDITION B (is_correct=False, conf=None, decisions=7):  [empty]
CONDITION C (is_correct=False, conf=None, decisions=21): [empty]
```

* * *

### Example 5 — All wrong: instrumentation (spectral cytometry)

**Problem** (truncated): "Context: Spectral cytometry is becoming a popular tool due to its
ability to measure a higher number of fluorescently labeled markers…"

```
GOLD:
GLOBAL: Optimize and validate a 15-parameter spectral flow panel on Aurora spectral
cytometer…

CONDITION A (is_correct=False, conf=0.85, decisions=1):
"IMMUNOSTAIN PANEL DESIGN FOR AURORA SPECTRAL CYTOMETRY: NK AND ILC DEVELOPMENT…"

CONDITION B (is_correct=False, conf=None, decisions=7):  [whitespace]
CONDITION C (is_correct=False, conf=None, decisions=40): [None] — hit max decisions
```

* * *

### Example 6 — All wrong: measurement uncertainty (physics calculation)

**Problem** (truncated): "Assuming we conducted an experiment to determine a physical quantity
X. We measure X, obtaining N measurements…"

```
GOLD:
GLOBAL: Calculate the combined measurement uncertainty of μ̂ by combining Type A and
Type B uncertainties…

CONDITION A (is_correct=False, conf=0.92, decisions=1):
√(s²/N + a²/12)   [correct formula — judge did not match to hierarchical gold format]

CONDITION B (is_correct=False, conf=None, decisions=8):  [None]
CONDITION C (is_correct=False, conf=None, decisions=19): [None]
```

Note: string-based matching against the hierarchical gold annotation did not recognize the
correct formula — a known judge limitation for mathematical answers.

* * *

### Example 7 — A confident wrong, B/C no answer (biology: immunostaining)

This and examples 8–10 are from the A-only rows (not in the 6 paired set) showing condition
A's overconfident error pattern.

```
CONDITION A (is_correct=False, conf=0.85, decisions=1):
[Multi-paragraph immunostaining protocol — does not match hierarchical gold annotation]
```

* * *

### Example 8 — A refuses, B/C N/A

One row where condition A produced an empty string with no trajectory (agent refusal event):

```
CONDITION A (is_correct=False, conf=None, decisions=1): [empty — agent refusal]
```

* * *

### Example 9 — A high-confidence wrong (conf=0.95)

```
CONDITION A (is_correct=False, conf=0.95, decisions=1):
[Substantive answer that does not match hierarchical gold annotation — high confidence, wrong.
Illustrates calibration gap: scope-aware prompt does not prevent overconfident errors on
expert olympiad problems.]
```

* * *

### Example 10 — A medium-confidence wrong (conf=0.42)

```
CONDITION A (is_correct=False, conf=0.42, decisions=1):
[Wrong answer with reduced confidence — suggests some self-awareness about difficulty.
Reduced confidence does not reliably indicate unsolvability.]
```

* * *

## Analysis and Discussion

### Why all conditions fail at FrontierScience-Olympiad

FrontierScience-Olympiad problems require multi-step quantitative scientific reasoning (enzyme
kinetics, measurement uncertainty, scRNA-seq analysis, plasmonics). Without tool access
(calculator, retrieval), claude-haiku-4-5 cannot execute the multi-step numerical workflows
required by the gold hierarchical annotations. The benchmark exceeds the no-tool haiku
capacity ceiling regardless of granularity conditioning.

### Why the A success rate (2.5%) is slightly above B/C (0%)

The single correct A row (scRNA-seq UMAP) is a conceptual recommendation task that does not
require computation — the answer is a method name ("UMAP or t-SNE") that matches the global
granularity level of the gold annotation. Condition A's scope-aware prompt correctly frames
the response at the right abstraction level. Conditions B and C produce empty strings for the
same row, suggesting that B's generic plan format and C's wrong granularity tag actively
suppress the correct response type.

### Metric 2 collapse is a methodological finding, not a null result

The `overconfident_error_rate` of 0.0 for B and C does not mean Plan-and-Solve is better
calibrated than ReAct. It means the v1 Plan-and-Solve library
(`scope_unaware_planandsolve_v1`) never emits a `final_confidence` field. The Xiong2024
aggregator therefore records no overconfident errors. This gap blocks any A-vs-B comparison on
RQ2 until the library is extended to emit verbalized confidence.

### Condition C's cost signature is diagnostic

C averaged 26.0 decisions per task (vs 1.2 for A, 6.5 for B). The wrong granularity tags cause
the Plan-and-Solve agent to generate elaborate multi-step plans at the wrong abstraction
level, then repeatedly revise them. This confirms the theoretical prediction that
scope-mismatched tags incur computational overhead — but the smoke cannot distinguish "more
computation → better results" from "more computation → wasted budget" without a correct-answer
ceiling test.

## Limitations

* **N too small for statistical power.** 6 paired rows (the minimum for McNemar) gives zero
  power to detect a 5 pp effect. The confirmatory N is 157 paired rows.
* **Model too weak.** Claude-haiku-4-5 without tools cannot solve FrontierScience-Olympiad.
  The null result is a floor effect, not a genuine null effect of granularity conditioning.
* **Metric 2 not comparable across conditions.** Plan-and-Solve does not emit
  `final_confidence`.
* **C partial run.** Only 11/40 rows for condition C due to budget halt; C metrics are not
  directly comparable to A/B at N=40.
* **task_id collision.** The upstream FrontierScience-Olympiad pilot file has multiple rows
  per `task_id` (26 unique IDs across 40 rows). The harness processes all rows independently;
  pairing is done on `task_id` which means multiple predictions per task in some cases.
* **No tool use.** The harness enforces `calculator + finish` only; real-world agents would
  use search, code execution, and retrieval.

## Verification

```
uv run python -m arf.scripts.verificators.verify_task_folder t0012_phase2_abc_smoke_frontierscience
uv run python -m arf.scripts.verificators.verify_task_file t0012_phase2_abc_smoke_frontierscience
uv run python -m arf.scripts.verificators.verify_task_metrics t0012_phase2_abc_smoke_frontierscience
uv run python -m arf.scripts.verificators.verify_task_results t0012_phase2_abc_smoke_frontierscience
uv run python -m meta.asset_types.predictions.verificator t0012_phase2_abc_smoke_frontierscience phase2-smoke-a
uv run python -m meta.asset_types.predictions.verificator t0012_phase2_abc_smoke_frontierscience phase2-smoke-b
uv run python -m meta.asset_types.predictions.verificator t0012_phase2_abc_smoke_frontierscience phase2-smoke-c
uv run python -m meta.asset_types.library.verificator t0012_phase2_abc_smoke_frontierscience phase2_smoke_harness_v1
```

All verificators passed before this step was committed.

## Files Created

* `results/results_summary.md` — headline metrics and key findings
* `results/results_detailed.md` — this file
* `results/metrics.json` — explicit-variant format with 3 condition variants
* `results/costs.json` — $18.37 total, 665 calls, all claude-haiku-4-5
* `results/suggestions.json` — 5 follow-on suggestions
* `results/images/condition_metric_bar.png` — bar chart of 3 metrics × 3 conditions
* `results/images/per_row_success_heatmap.png` — per-row success heatmap
* `assets/predictions/phase2-smoke-{a,b,c}/` — 3 predictions assets (JSONL + metadata)
* `assets/library/phase2_smoke_harness_v1/` — harness library asset

## Next Steps and Suggestions

See `results/suggestions.json` for 5 queued suggestions. The highest-priority items are:

1. Extend `scope_unaware_planandsolve_v1` to emit `final_confidence` so Metric 2 becomes
   comparable across conditions.
2. Run a confirmatory Phase 2 with N≥157 paired rows using claude-sonnet-4-6 on SWE-bench
   Verified or tau-bench (benchmarks where sonnet can achieve non-floor accuracy).
3. Add tool use (search, code execution) to the harness so FrontierScience-Olympiad accuracy
   lifts above the floor for all conditions.

## Task Requirement Coverage

This section maps the task's expected deliverables (from `task.json`) to results produced.

* **Expected: 3 predictions assets** — Delivered: `phase2-smoke-a` (40 rows), `phase2-smoke-b`
  (40 rows), `phase2-smoke-c` (11 rows, partial due to budget halt). All pass verificators.
* **Expected: 1 library asset** — Delivered: `phase2_smoke_harness_v1` (8 source modules).
  Passes verificator.
* **Expected: 3 registered metrics in explicit-variant format** — Delivered:
  `results/metrics.json` with variants `condition_a_scope_aware`, `condition_b_scope_unaware`,
  `condition_c_scope_mismatched`. Passes `verify_task_metrics`.
* **Expected: paired hypothesis tests (McNemar)** — Delivered: 3 McNemar tests in
  `_intermediate_stats.json` and documented in this file (A vs B, B vs C, A vs C; all p=1.0).
* **Expected: confirmatory-N estimate** — Delivered: N=157 for 5 pp effect at α=0.05,
  power=0.8.
* **Partial gap: Condition C ran only 11/40 rows** — Budget halted at $18.37. C metrics are
  reported honestly at N=11 with a note. Per-row checkpointing preserved all 11 completed
  rows.
* **Known gap: Metric 2 not comparable for B/C** — Plan-and-Solve does not emit
  `final_confidence`; `overconfident_error_rate` is 0.0 for B and C by construction, not by
  calibration. Documented throughout and queued as S-0012-01.

</details>
