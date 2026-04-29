# ✅ Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0011_metric2_calibration_aggregator` |
| **Status** | ✅ completed |
| **Started** | 2026-04-29T23:25:12Z |
| **Completed** | 2026-04-29T23:43:00Z |
| **Duration** | 17m |
| **Source suggestion** | `S-0002-02` |
| **Task types** | `write-library` |
| **Categories** | [`uncertainty-calibration`](../../by-category/uncertainty-calibration.md) |
| **Expected assets** | 1 library |
| **Step progress** | 9/15 |
| **Task folder** | [`t0011_metric2_calibration_aggregator/`](../../../tasks/t0011_metric2_calibration_aggregator/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0011_metric2_calibration_aggregator/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0011_metric2_calibration_aggregator/task_description.md)*

# Metric 2 Calibration Aggregator (Xiong2024 Protocol)

## Motivation

The project's Metric 2 (`overconfident_error_rate`) has no implementation: it is registered in
`meta/metrics/` but no code computes it. The literature survey (t0002) identified Xiong2024 as
the canonical calibration protocol — verbalized confidence elicitation (low / medium / high +
brief justification) plus 3-sample self-consistency aggregation. Without this library, the
Phase 2 smoke test (t0012) cannot report Metric 2 — only Metric 1 (success rate) and the
diagnostic Metric 3 (avg decisions per task). This task unblocks the headline experiment by
producing a library that any agent's trajectory records can be passed through to compute
`overconfident_error_rate`. Implements suggestion S-0002-02.

## Scope

* Implement a library asset under `assets/library/metric2_calibration_aggregator_v1/`
  exposing:
  * `class ConfidencePromptTemplate`: the human-inspired confidence-elicitation prompt (low /
    medium / high + one-sentence justification) per Xiong2024 §3.2.
  * `class ConfidenceJudge`: aggregator that takes 3 trajectory samples for the same problem
    and returns `(predicted_label, predicted_confidence, is_correct)`. Self-consistency is
    majority-vote on the predicted label; confidence is the mean across samples.
  * `function compute_overconfident_error_rate(records: Iterable[CalibrationRecord]) -> float`
    that returns the fraction of records where `is_correct == False` and `predicted_confidence
    > = HIGH_CONFIDENCE_THRESHOLD`. The threshold is a module constant (default 0.75).
  * `function elicit_confidence(model_call, problem, action) -> tuple[str, float]` that calls
    the model with the prompt template and parses the response.
  * `dataclass CalibrationRecord(frozen=True, slots=True)`: the canonical record shape that
    `compute_overconfident_error_rate` consumes.
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e.,
  must consume the canonical `TRAJECTORY_RECORD_FIELDS` schema as input.
* Provide pytest coverage at
  `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py` covering: prompt
  template formatting, parsing of low / medium / high confidence labels, majority-vote
  aggregation across 3 samples (including ties), threshold-based overconfident detection, and
  end-to-end run on a synthetic 10-record dataset.

Out of scope: the actual experiment harness (handled by t0012), live API calls (deterministic
tests only), provider-specific calibration variants.

## Approach

1. Read t0002's Xiong2024 paper summary
   (`tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md`)
   to ground the prompt template and threshold choice.
2. Implement in `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` with a
   `paths.py` and `constants.py` per the project Python style guide.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests use `ScriptedModel` from t0007 to simulate model responses for the confidence prompt.
5. Run `verify_library_asset`, ruff, mypy, and pytest.

## Expected Outputs

* `assets/library/metric2_calibration_aggregator_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` and tests.
* `results/results_summary.md` with API surface description, test summary, and the threshold
  default rationale.
* Follow-up suggestion for: provider-specific calibration variants, ECE (expected calibration
  error) computation in addition to overconfident-error-rate.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Xiong2024 paper asset (`10.48550_arXiv.2306.13063`) from t0002's library.
* Output format consumed by t0012's experiment harness.

## Source Suggestion

S-0002-02 — "Implement verbalized-confidence + 3-sample self-consistency aggregator for Metric
2."

## Key Questions

1. What is the right default `HIGH_CONFIDENCE_THRESHOLD`? Xiong2024 uses 0.75 with verbalized
   labels mapped to {low: 0.25, medium: 0.5, high: 0.9}; the default should match.
2. How should the aggregator handle ties in the majority vote across 3 samples? Default:
   prefer the highest-confidence sample.
3. What is the expected output schema for compute_overconfident_error_rate so Phase 2 results
   can include it in `metrics.json` directly?

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Metric 2 Calibration Aggregator](../../../tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/) | [`description.md`](../../../tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/description.md) |

## Suggestions Generated

<details>
<summary><strong>Add Expected Calibration Error (ECE) computation alongside
overconfident_error_rate</strong> (S-0011-01)</summary>

**Kind**: library | **Priority**: medium

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
<summary><strong>Add provider-specific calibration prompt variants for
instruction-tuned vs reasoning models</strong> (S-0011-02)</summary>

**Kind**: experiment | **Priority**: medium

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

<details>
<summary><strong>Sweep HIGH_CONFIDENCE_THRESHOLD to find the operating point that
maximizes signal in t0012</strong> (S-0011-03)</summary>

**Kind**: evaluation | **Priority**: low

The current default HIGH_CONFIDENCE_THRESHOLD = 0.75 sits between the verbalized medium (0.5)
and high (0.9) numeric anchor points and matches Xiong2024's high-bucket boundary. The
threshold is exposed as a module constant for sweeps. After t0012 runs, sweep the threshold
over {0.5, 0.6, 0.7, 0.75, 0.8, 0.9} and report overconfident_error_rate at each operating
point. The best threshold for the project's hierarchical agents may differ from Xiong2024's QA
setting because the project judges actions at trajectory steps, not final answers. Output: a
small chart and a recommended threshold for downstream tasks.

</details>

## Research

* [`research_papers.md`](../../../tasks/t0011_metric2_calibration_aggregator/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0011_metric2_calibration_aggregator/results/results_summary.md)*

# Results Summary — Metric 2 Calibration Aggregator

## Summary

Implemented the metric2_calibration_aggregator_v1 library that operationalizes the project's
Metric 2 (`overconfident_error_rate`) using the Xiong2024 §3.2 black-box calibration protocol.
The library exposes `ConfidencePromptTemplate`, `ConfidenceJudge`, `elicit_confidence`,
`compute_overconfident_error_rate`, and `CalibrationRecord` plus a trajectory-record adapter,
with a single overridable threshold default (`HIGH_CONFIDENCE_THRESHOLD = 0.75`) and the
canonical low/medium/high → 0.25/0.5/0.9 numeric mapping.

## Metrics

* **Tests run**: 25 — all passed in 0.03 s (`uv run pytest
  tasks/t0011_metric2_calibration_aggregator/code/`).
* **Code lines written**: ~340 in `code/calibration.py`, ~125 in `code/constants.py`, ~40 in
  `code/paths.py`, ~370 in `code/test_calibration.py` (test count includes the `ScriptedModel`
  fake).
* **Public API surface**: 5 entry points required by the task description plus 1 helper
  (`calibration_record_from_trajectory`); 6 entry points listed in `details.json`.
* **External cost**: $0 — deterministic tests, no live API calls.
* **Type-checked source files**: 21 (mypy on the parent task package, zero errors).
* **Quality gates passed**: ruff check, ruff format, mypy, pytest, library asset verificator.

## Verification

* `uv run ruff check tasks/t0011_metric2_calibration_aggregator/code/` → All checks passed.
* `uv run ruff format tasks/t0011_metric2_calibration_aggregator/code/` → no changes.
* `uv run mypy -p tasks.t0011_metric2_calibration_aggregator` → Success: no issues found in 21
  source files.
* `uv run pytest tasks/t0011_metric2_calibration_aggregator/code/ -v` → 25 passed in 0.03s.
* `uv run python -m meta.asset_types.library.verificator --task-id
  t0011_metric2_calibration_aggregator metric2_calibration_aggregator_v1` → PASSED, no errors
  or warnings.
* `verify_research_papers`, `verify_plan` → both pass with zero errors and zero warnings.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0011_metric2_calibration_aggregator/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0011_metric2_calibration_aggregator" date_completed:
"2026-04-29" status: "complete" ---
# Results Detailed — Metric 2 Calibration Aggregator

## Summary

This task produced one library asset (`metric2_calibration_aggregator_v1`) implementing the
Xiong2024 §3.2 black-box calibration protocol — verbalized "low / medium / high" confidence
elicitation, 3-sample self-consistency aggregation, and the binary overconfident-error metric.
All 25 deterministic tests pass; ruff check, ruff format, and mypy on the parent task package
report zero issues; the library asset verificator passes with zero errors and zero warnings.
No external API calls were made; the project budget is unaffected.

## Methodology

* **Machine**: macOS Darwin 25.3.0 (the orchestrator's local workstation).
* **Python**: 3.13.11 via `uv` from the project's `.venv`.
* **Runtime**: 0.03 s wall-clock for the full pytest run; the implementation step took ~25
  minutes including code, tests, asset metadata, and quality gates.
* **Timestamps**: prestep `2026-04-29T23:34:13Z`, poststep `2026-04-29T23:39:48Z`.
* **Workers**: single-process (no multiprocessing required).
* **Determinism**: every test uses a `ScriptedModel` fake with pre-recorded responses; there
  is no randomness in any code path under test.

## Metrics

This task does not measure any of the three project-registered metrics (`task_success_rate`,
`overconfident_error_rate`, `avg_decisions_per_task`) because it is a write-library task whose
deliverable is the library that *computes* `overconfident_error_rate`, not a measurement of
it. `metrics.json` is therefore `{}` per the `task_results_specification.md` rule. Operational
signals (test count, lines of code) live in this file and in `results_summary.md`.

* Test cases: 25 (all pass)
* Public API entry points: 6 (5 required by the task + 1 trajectory adapter helper)
* External dependencies: 0 (Python standard library only)

## Verification

* `verify_research_papers t0011_metric2_calibration_aggregator` → PASSED, 0 errors, 0
  warnings.
* `verify_plan t0011_metric2_calibration_aggregator` → PASSED, 0 errors, 0 warnings.
* `meta.asset_types.library.verificator --task-id t0011_metric2_calibration_aggregator
  metric2_calibration_aggregator_v1` → PASSED, 0 errors, 0 warnings.
* `uv run ruff check tasks/t0011_metric2_calibration_aggregator/code/` → exit 0.
* `uv run ruff format tasks/t0011_metric2_calibration_aggregator/code/` → no changes.
* `uv run mypy -p tasks.t0011_metric2_calibration_aggregator` → 21 files, 0 errors.
* `uv run pytest tasks/t0011_metric2_calibration_aggregator/code/ -v` → 25 passed in 0.03s.

## Limitations

* The library implements only the binary overconfident-error rate. It does not compute
  Expected Calibration Error (ECE) or produce bucketed-confidence plots; those are out of
  scope for this task and will be picked up by a follow-up suggestion (S-0011-NEW-ECE).
* The verbalized-to-numeric mapping (low → 0.25, medium → 0.5, high → 0.9) and the threshold
  default (0.75) are reconstructed from the Xiong2024 abstract and the bucketed-ECE convention
  because the full Xiong2024 PDF was not downloaded for t0002 (download deferred). If a future
  task downloads the PDF and the published mapping disagrees, the four module constants in
  `code/constants.py` are the only edits needed; no test rewrite is required.
* The library does not validate that the model actually produced its three samples
  independently — it consumes whatever `sampled_actions` the caller provides. Any
  caller-introduced bias (e.g., always passing the same action three times) will pass through
  unchecked. This is intentional: validation of upstream sampling discipline belongs to the
  experiment harness in t0012.
* The 3-way tie tiebreak (highest-confidence sample wins, first wins on equal max) is a
  conservative choice not prescribed by Xiong2024. Documented in the description's Main Ideas
  section and asserted by tests so callers can rely on it.
* Tests do not cover an asynchronous `model_call` shape; the `ModelCall` Protocol is
  synchronous. Adding async support is a small follow-up if any future caller needs it.

## Files Created

* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` — main library module
* `tasks/t0011_metric2_calibration_aggregator/code/constants.py` — Xiong2024 protocol
  parameters
* `tasks/t0011_metric2_calibration_aggregator/code/paths.py` — filesystem path constants
* `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py` — 25-test pytest suite
* `tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/details.json`
* `tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/description.md`
* `tasks/t0011_metric2_calibration_aggregator/research/research_papers.md`
* `tasks/t0011_metric2_calibration_aggregator/plan/plan.md`
* `tasks/t0011_metric2_calibration_aggregator/results/results_summary.md`
* `tasks/t0011_metric2_calibration_aggregator/results/results_detailed.md` (this file)
* `tasks/t0011_metric2_calibration_aggregator/results/metrics.json` — `{}` (no
  project-registered metrics measured)
* `tasks/t0011_metric2_calibration_aggregator/results/costs.json`
* `tasks/t0011_metric2_calibration_aggregator/results/remote_machines_used.json`

## Task Requirement Coverage

The operative task text from `task.json` and `task_description.md`:

```text
Task name: Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency
Short description: Write-library implementing the Xiong2024 verbalized-confidence + 3-sample
self-consistency aggregator that computes overconfident_error_rate.

Long description (excerpt from task_description.md):
* Implement a library asset under assets/library/metric2_calibration_aggregator_v1/ exposing
  ConfidencePromptTemplate, ConfidenceJudge, compute_overconfident_error_rate(records),
  elicit_confidence(model_call, problem, action) -> tuple[str, float], and CalibrationRecord
  (frozen dataclass).
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e.,
  must consume the canonical TRAJECTORY_RECORD_FIELDS schema as input.
* Provide pytest coverage at code/test_calibration.py covering: prompt template formatting,
  parsing of low/medium/high confidence labels, majority-vote aggregation across 3 samples
  (including ties), threshold-based overconfident detection, and end-to-end run on a synthetic
  10-record dataset.
* Out of scope: experiment harness, live API calls, provider-specific calibration variants.
* Default HIGH_CONFIDENCE_THRESHOLD = 0.75 with verbalized labels mapped to
  {low: 0.25, medium: 0.5, high: 0.9}.
* Tests use ScriptedModel from t0007 to simulate model responses.
```

| ID | Requirement | Result | Status | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | Library asset folder with details.json + description.md passing verificator | Asset created and verifies clean | Done | `assets/library/metric2_calibration_aggregator_v1/{details.json,description.md}`; verificator output captured in `logs/commands/013_*.stdout.txt`. |
| REQ-2 | code/calibration.py defines the 5 named symbols | All 5 plus `ConfidenceSample`, `ConfidenceAggregate`, `MalformedConfidenceError`, `calibration_record_from_trajectory` | Done | `code/calibration.py` lines 56-369; `details.json` `entry_points`. |
| REQ-3 | Library accepts the canonical TRAJECTORY_RECORD_FIELDS schema | `calibration_record_from_trajectory` accepts mapping records and parses `action` and `confidence`; covered by 3 tests | Done | `code/calibration.py` `calibration_record_from_trajectory`; tests `test_calibration_record_from_trajectory_*`. |
| REQ-4 | Pytest covers prompt template, label parsing (low/medium/high), majority-vote (incl. ties), threshold, end-to-end 10-record run | 25 tests covering every listed concern | Done | `code/test_calibration.py`; pytest log `logs/commands/011_*.stdout.txt`. |
| REQ-5 | HIGH_CONFIDENCE_THRESHOLD = 0.75 and label mapping low→0.25/medium→0.5/high→0.9 as module constants | All four values present in `constants.py`; sanity test asserts them | Done | `code/constants.py`; `test_constants_match_xiong2024_protocol`. |
| REQ-6 | Tests use ScriptedModel-shaped fake (no live API) | Local `ScriptedModel` dataclass mirrors t0007's interface | Done | `code/test_calibration.py` lines 35-52. |
| REQ-7 | ruff check, ruff format, mypy all pass | All three pass; mypy 21 files clean | Done | `logs/commands/006_*` (ruff), `010_*` (mypy). |
| REQ-8 | Pytest reports 0 failures | 25 passed in 0.03s | Done | `logs/commands/011_*.stdout.txt`. |

Out-of-scope items from the task description (experiment harness, live API calls,
provider-specific calibration variants) were intentionally not produced. Provider-specific
calibration is captured as a follow-up suggestion in `results/suggestions.json`.

</details>
