# Suggestions: `uncertainty-calibration`

3 suggestion(s) in category
[`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) **3 open** (2
high, 1 low).

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>📚 <strong>Implement verbalized-confidence + 3-sample self-consistency
aggregator for Metric 2</strong> (S-0002-02)</summary>

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
<summary>📊 <strong>Re-run LLM-as-judge with full problem text (no
truncation)</strong> (S-0005-02)</summary>

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
