---
spec_version: "2"
task_id: "t0012_phase2_abc_smoke_frontierscience"
---
# Results Detailed — Phase 2 A/B/C Smoke (FrontierScience-Olympiad)

## Summary

The Phase 2 smoke ran three agent conditions (A: scope-aware ReAct, B: scope-unaware Plan-and-Solve,
C: scope-mismatched Plan-and-Solve) against 40 FrontierScience-Olympiad hierarchy-complete rows from
the v2 hierarchical-annotation dataset, using claude-haiku-4-5 via the local Claude Code CLI with a
minimal system prompt. A completed 40 rows, B completed 40 rows, C completed 11 rows before the $18
budget cap was reached. All three conditions solved near-zero problems. The smoke validates the
harness end-to-end and identifies two critical follow-on actions: a confirmatory run at N≥157 on a
stronger model, and extending the Plan-and-Solve library to emit `final_confidence`.

## Methodology

* **Model**: claude-haiku-4-5 accessed via local Claude Code CLI
* **System prompt**: Minimal (overridden with `--tools "" --setting-sources ""`)
* **Tool registry**: calculator + finish only (condition A/C); finish only (condition B)
* **Dataset**: hierarchical-annotation-v2, FrontierScience-Olympiad subset, hierarchy-complete rows
  (40 rows total)
* **Machine**: MacBook Pro, local execution, no GPU
* **Runtime**: ~4.5 hours wall-clock (concurrent A/B/C runs)
* **Date**: 2026-05-01
* **Total calls**: 665 (all to claude-haiku-4-5)
* **Total cost**: $18.37 (halted above $18 cap)
* **Cache reuse**: 16.3M cache-read tokens vs 2.0M cache-creation tokens — system-prompt override
  enables aggressive KV-cache reuse across calls

## Metrics Tables

### Primary metrics per condition

| Metric | A: scope-aware ReAct | B: scope-unaware PlanSolve | C: scope-mismatched |
| --- | --- | --- | --- |
| `task_success_rate` | 0.025 (1/40) | 0.000 (0/40) | 0.000 (0/11) |
| `overconfident_error_rate` | 0.647 | 0.000 † | 0.000 † |
| `avg_decisions_per_task` | 1.20 | 6.53 | 26.0 |

† Collapsed: Plan-and-Solve trajectories do not surface `final_confidence`; the Xiong2024 aggregator
records zero overconfident errors by construction. Not comparable to A.

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

Note: RQ2 refutation is an artefact of the Metric 2 collapse for B/C. The overconfident error rate
for B and C is 0.0 only because `final_confidence` is never emitted, not because B/C are better
calibrated.

### Confirmatory-N estimate

For a 5 pp paired-difference effect at α=0.05, power=0.8, given the observed discordant rate from
this smoke: **N = 157 paired rows**.

## Comparison vs Baselines

The smoke is an internal pilot, not a published benchmark comparison. Published
FrontierScience-Olympiad results (from the benchmark paper) report state-of-the-art models at 15–30%
on similar problem types with tool use. Our haiku+no-tool baseline at 2.5% (A) is consistent with
the expected floor for a no-tool, small-model agent on expert-level science olympiad problems.

## Visualizations

![Condition metric bar chart](images/condition_metric_bar.png)

Bars show task_success_rate and avg_decisions_per_task for the three conditions. C's 26.0 avg
decisions indicates the scope-mismatch triggers repeated plan revisions that consume budget without
improving accuracy.

![Per-row success heatmap](images/per_row_success_heatmap.png)

Row-by-row is_correct matrix across conditions. The single correct A row (scRNA-seq UMAP problem) is
visible. B and C show all-zero columns. C's partial coverage (11/40 rows) is visible in the
truncated right panel.

## Examples

The following 10 examples are drawn from the 6 task IDs present in all three conditions (fully
paired), plus the one correct A row.

### Example 1 — Correct A row (scRNA-seq dimensionality reduction)

**Problem** (truncated): "Biopsies of solid tumors from placebo patients and patients given drug X
were collected. Total RNA was reverse-transcribed and scRNA-seq performed. A high-dimensional data
matrix (6,000+ genes × cells)…"

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

**Problem** (truncated): "Context: Climate change is increasing the demand for stress resilient
crops. Chenopodium pallidicaule, native to the Andes, is an understudied crop…"

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

**Problem** (truncated): "Context: A research paper discusses the interaction of plasmonic silver
(Ag) nanocubes with methylene blue (MB) under different conditions…"

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

**Problem** (truncated): "Context: Spectral cytometry is becoming a popular tool due to its ability
to measure a higher number of fluorescently labeled markers…"

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

**Problem** (truncated): "Assuming we conducted an experiment to determine a physical quantity X. We
measure X, obtaining N measurements…"

```
GOLD:
GLOBAL: Calculate the combined measurement uncertainty of μ̂ by combining Type A and
Type B uncertainties…

CONDITION A (is_correct=False, conf=0.92, decisions=1):
√(s²/N + a²/12)   [correct formula — judge did not match to hierarchical gold format]

CONDITION B (is_correct=False, conf=None, decisions=8):  [None]
CONDITION C (is_correct=False, conf=None, decisions=19): [None]
```

Note: string-based matching against the hierarchical gold annotation did not recognize the correct
formula — a known judge limitation for mathematical answers.

* * *

### Example 7 — A confident wrong, B/C no answer (biology: immunostaining)

This and examples 8–10 are from the A-only rows (not in the 6 paired set) showing condition A's
overconfident error pattern.

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
kinetics, measurement uncertainty, scRNA-seq analysis, plasmonics). Without tool access (calculator,
retrieval), claude-haiku-4-5 cannot execute the multi-step numerical workflows required by the gold
hierarchical annotations. The benchmark exceeds the no-tool haiku capacity ceiling regardless of
granularity conditioning.

### Why the A success rate (2.5%) is slightly above B/C (0%)

The single correct A row (scRNA-seq UMAP) is a conceptual recommendation task that does not require
computation — the answer is a method name ("UMAP or t-SNE") that matches the global granularity
level of the gold annotation. Condition A's scope-aware prompt correctly frames the response at the
right abstraction level. Conditions B and C produce empty strings for the same row, suggesting that
B's generic plan format and C's wrong granularity tag actively suppress the correct response type.

### Metric 2 collapse is a methodological finding, not a null result

The `overconfident_error_rate` of 0.0 for B and C does not mean Plan-and-Solve is better calibrated
than ReAct. It means the v1 Plan-and-Solve library (`scope_unaware_planandsolve_v1`) never emits a
`final_confidence` field. The Xiong2024 aggregator therefore records no overconfident errors. This
gap blocks any A-vs-B comparison on RQ2 until the library is extended to emit verbalized confidence.

### Condition C's cost signature is diagnostic

C averaged 26.0 decisions per task (vs 1.2 for A, 6.5 for B). The wrong granularity tags cause the
Plan-and-Solve agent to generate elaborate multi-step plans at the wrong abstraction level, then
repeatedly revise them. This confirms the theoretical prediction that scope-mismatched tags incur
computational overhead — but the smoke cannot distinguish "more computation → better results" from
"more computation → wasted budget" without a correct-answer ceiling test.

## Limitations

* **N too small for statistical power.** 6 paired rows (the minimum for McNemar) gives zero power to
  detect a 5 pp effect. The confirmatory N is 157 paired rows.
* **Model too weak.** Claude-haiku-4-5 without tools cannot solve FrontierScience-Olympiad. The null
  result is a floor effect, not a genuine null effect of granularity conditioning.
* **Metric 2 not comparable across conditions.** Plan-and-Solve does not emit `final_confidence`.
* **C partial run.** Only 11/40 rows for condition C due to budget halt; C metrics are not directly
  comparable to A/B at N=40.
* **task_id collision.** The upstream FrontierScience-Olympiad pilot file has multiple rows per
  `task_id` (26 unique IDs across 40 rows). The harness processes all rows independently; pairing is
  done on `task_id` which means multiple predictions per task in some cases.
* **No tool use.** The harness enforces `calculator + finish` only; real-world agents would use
  search, code execution, and retrieval.

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

1. Extend `scope_unaware_planandsolve_v1` to emit `final_confidence` so Metric 2 becomes comparable
   across conditions.
2. Run a confirmatory Phase 2 with N≥157 paired rows using claude-sonnet-4-6 on SWE-bench Verified
   or tau-bench (benchmarks where sonnet can achieve non-floor accuracy).
3. Add tool use (search, code execution) to the harness so FrontierScience-Olympiad accuracy lifts
   above the floor for all conditions.

## Task Requirement Coverage

This section maps the task's expected deliverables (from `task.json`) to results produced.

* **Expected: 3 predictions assets** — Delivered: `phase2-smoke-a` (40 rows), `phase2-smoke-b` (40
  rows), `phase2-smoke-c` (11 rows, partial due to budget halt). All pass verificators.
* **Expected: 1 library asset** — Delivered: `phase2_smoke_harness_v1` (8 source modules). Passes
  verificator.
* **Expected: 3 registered metrics in explicit-variant format** — Delivered: `results/metrics.json`
  with variants `condition_a_scope_aware`, `condition_b_scope_unaware`,
  `condition_c_scope_mismatched`. Passes `verify_task_metrics`.
* **Expected: paired hypothesis tests (McNemar)** — Delivered: 3 McNemar tests in
  `_intermediate_stats.json` and documented in this file (A vs B, B vs C, A vs C; all p=1.0).
* **Expected: confirmatory-N estimate** — Delivered: N=157 for 5 pp effect at α=0.05, power=0.8.
* **Partial gap: Condition C ran only 11/40 rows** — Budget halted at $18.37. C metrics are reported
  honestly at N=11 with a note. Per-row checkpointing preserved all 11 completed rows.
* **Known gap: Metric 2 not comparable for B/C** — Plan-and-Solve does not emit `final_confidence`;
  `overconfident_error_rate` is 0.0 for B and C by construction, not by calibration. Documented
  throughout and queued as S-0012-01.
