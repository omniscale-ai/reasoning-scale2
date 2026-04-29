# Libraries: `uncertainty-calibration`

1 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>Metric 2 Calibration Aggregator</strong>
(<code>metric2_calibration_aggregator_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `metric2_calibration_aggregator_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0011_metric2_calibration_aggregator/code/calibration.py`, `tasks/t0011_metric2_calibration_aggregator/code/constants.py`, `tasks/t0011_metric2_calibration_aggregator/code/paths.py` |
| **Dependencies** | — |
| **Date created** | 2026-04-29 |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |
| **Created by** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Documentation** | [`description.md`](../../../tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/description.md) |

**Entry points:**

* `ConfidencePromptTemplate` (class) — Frozen dataclass wrapping the Xiong2024 §3.2
  human-inspired prompt with {problem} and {action} placeholders.
* `ConfidenceJudge` (class) — Self-consistency aggregator that majority-votes on predicted
  action labels and returns the mean confidence within the majority cohort, falling back to
  the highest-confidence sample on a 3-way tie.
* `compute_overconfident_error_rate` (function) — Returns the fraction of CalibrationRecord
  values that are incorrect with predicted_confidence >= HIGH_CONFIDENCE_THRESHOLD (default
  0.75); 0.0 for empty input.
* `elicit_confidence` (function) — Formats the confidence prompt, invokes a model_call, parses
  the verbalized label (low/medium/high), and returns (label, numeric_confidence).
* `CalibrationRecord` (class) — Frozen dataclass holding (problem_id, predicted_label,
  predicted_confidence, is_correct); the canonical input shape for
  compute_overconfident_error_rate.
* `calibration_record_from_trajectory` (function) — Adapter that converts a t0006/t0007/t0010
  trajectory record (canonical TRAJECTORY_RECORD_FIELDS schema) into a CalibrationRecord.

Verbalized-confidence + 3-sample self-consistency aggregator that computes
overconfident_error_rate per the Xiong2024 protocol.

</details>
