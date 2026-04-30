# Suggestions: `uncertainty-calibration`

7 suggestion(s) in category
[`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) **5 open** (3
medium, 2 low), **2 closed**.

[Back to all suggestions](../README.md)

---

## Medium Priority

<details>
<summary>🧪 <strong>Add an ablation: tree-schema-with-truncated-text to isolate the
truncation fix from the schema upgrade</strong> (S-0009-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0009_hierarchical_annotation_v2/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

v2 changed two things at once: schema (flat -> tree) and text completeness (truncated 1500
chars -> full). On FrontierScience-Olympiad and WorkArena++ the +67% and +100% deltas could be
entirely from the truncation fix (Xiong2024's prediction) or entirely from the schema upgrade.
Run a third condition: the v2 tree schema but truncate the problem to 1500 chars in both the
annotator and judge prompts. If accept rate drops materially below v2-full-text on
FrontierScience-Olympiad, truncation is the dominant cause; if it stays at v2-full-text
levels, the schema is the dominant cause. Cost ~$2 with haiku.

</details>

<details>
<summary>📚 <strong>Add Expected Calibration Error (ECE) computation alongside
overconfident_error_rate</strong> (S-0011-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

Extend the metric2_calibration_aggregator_v1 library (or add a sibling library) with Expected
Calibration Error (ECE) computation using the standard 10-bucket binning and produce
per-bucket calibration plots. Xiong2024 reports ECE as the primary headline metric; the
current library reports only the binary overconfident_error_rate. Adding ECE gives Phase 2 a
richer calibration signal and lets t0012's results display the bucket where overconfidence
concentrates rather than just a single number. Should be a small follow-up: bucket each
CalibrationRecord by predicted_confidence, compute |accuracy - mean_confidence| within each
bucket, weight by bucket size. Output should be both a scalar ECE value and a list of
(bucket_lower, bucket_upper, accuracy, mean_confidence, count) tuples for plotting.

</details>

<details>
<summary>🧪 <strong>Add provider-specific calibration prompt variants for
instruction-tuned vs reasoning models</strong> (S-0011-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

The current ConfidencePromptTemplate uses a single Xiong2024 human-inspired prompt.
Reasoning-focused models (e.g., o-series, Claude 4.5+ thinking models) often produce a
chain-of-thought before stating confidence, which the current parser handles but which
Xiong2024's own results show can hurt calibration in some configurations. Build a small
library of named prompt variants (instruction_tuned, reasoning_with_cot, reasoning_no_cot) and
benchmark them on a held-out 50-problem set during Phase 2. Goal: identify which variant
minimizes overconfident_error_rate per provider and ship that as the default mapping in
t0012's experiment harness. Out of scope for this task per task_description.md but identified
as the obvious next sweep.

</details>

## Low Priority

<details>
<summary>📊 <strong>Multi-judge disagreement study on hierarchical
annotation</strong> (S-0005-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Run the same 12-row spot-check with two judge models (claude-haiku-4-5 + claude-sonnet-4-6)
and compute pairwise verdict agreement plus a confusion matrix. The v1 single-judge accept
rate of 33% may be miscalibrated; multi-judge agreement gives a more reliable quality
estimate. Estimated cost: ~$0.30 per run.

</details>

<details>
<summary>📊 <strong>Sweep HIGH_CONFIDENCE_THRESHOLD to find the operating point that
maximizes signal in t0012</strong> (S-0011-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

The current default HIGH_CONFIDENCE_THRESHOLD = 0.75 sits between the verbalized medium (0.5)
and high (0.9) numeric anchor points and matches Xiong2024's high-bucket boundary. The
threshold is exposed as a module constant for sweeps. After t0012 runs, sweep the threshold
over {0.5, 0.6, 0.7, 0.75, 0.8, 0.9} and report overconfident_error_rate at each operating
point. The best threshold for the project's hierarchical agents may differ from Xiong2024's QA
setting because the project judges actions at trajectory steps, not final answers. Output: a
small chart and a recommended threshold for downstream tasks.

</details>

## Closed

<details>
<summary>✅ <s>Implement verbalized-confidence + 3-sample self-consistency aggregator
for Metric 2</s> — covered by <a
href="../../../tasks/t0011_metric2_calibration_aggregator/"><code>t0011_metric2_calibration_aggregator</code></a>
(S-0002-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Xiong2024 establishes that single-sample verbalized confidence is poorly calibrated and that
3-sample self-consistency aggregation reduces ECE by 2-8 points. The project should commit to
this protocol for Metric 2 (overconfident error rate). This task would specify the
human-inspired confidence prompt template (low/medium/high + brief justification), implement
the self-consistency aggregator, and validate calibration on a small held-out set before Phase
2 launches.

</details>

<details>
<summary>✅ <s>Re-run LLM-as-judge with full problem text (no truncation)</s> —
covered by <a
href="../../../tasks/t0009_hierarchical_annotation_v2/"><code>t0009_hierarchical_annotation_v2</code></a>
(S-0005-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

The v1 judge sees only the first 1500 chars of each problem. Three of four needs-revision
verdicts on FrontierScience-Olympiad rows complain about content not present in the truncated
excerpt. Re-run the audit using the full problem text (or a structured per-section summary)
and compare accept rates. Predict an absolute accept-rate increase of >=15 percentage points
on FrontierScience-Olympiad.

</details>
