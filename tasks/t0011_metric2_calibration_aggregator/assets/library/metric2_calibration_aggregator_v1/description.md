---
spec_version: "2"
library_id: "metric2_calibration_aggregator_v1"
documented_by_task: "t0011_metric2_calibration_aggregator"
date_documented: "2026-04-29"
---
# Metric 2 Calibration Aggregator

## Metadata

* **Name**: Metric 2 Calibration Aggregator
* **Version**: 0.1.0
* **Task**: `t0011_metric2_calibration_aggregator`
* **Dependencies**: none (Python standard library only)
* **Modules**: `code/calibration.py`, `code/constants.py`, `code/paths.py`
* **Tests**: `code/test_calibration.py` (25 tests, all pass)
* **Categories**: `uncertainty-calibration`

## Overview

This library operationalizes the project's Metric 2 (`overconfident_error_rate`) using the Xiong2024
§3.2 black-box calibration protocol. It exposes a small, dependency-free Python module that any
agent's per-problem trajectory records can flow through to produce a single calibrated number: the
fraction of problems the agent answered incorrectly while claiming high stated confidence. The
library is the prerequisite for Phase 2 of the project — without it, the smoke experiment harness in
t0012 can report only Metric 1 (success rate) and the diagnostic Metric 3 (decisions per task), but
not the headline calibration signal.

The library has three responsibilities. First, it formats and parses the human-inspired
confidence-elicitation prompt that asks the model for a low / medium / high label plus a
one-sentence justification. Second, it aggregates 3 self-consistency samples per problem using
majority vote on the predicted action label and the mean confidence within the majority cohort, with
a deterministic tie-breaker for 3-way ties. Third, it computes the overconfident-error rate itself:
the fraction of records that are wrong with `predicted_confidence` at or above the high-confidence
threshold. All Xiong2024 protocol parameters (verbalized-to-numeric mapping, threshold, sample
count) live in `constants.py` so future tasks can sweep them without forking the library.

## API Reference

### `code/calibration.py`

#### `class CalibrationRecord`

```python
@dataclass(frozen=True, slots=True)
class CalibrationRecord:
    problem_id: str
    predicted_label: str
    predicted_confidence: float
    is_correct: bool
```

The canonical input shape for `compute_overconfident_error_rate`. `predicted_confidence` is the
aggregated numeric confidence from `ConfidenceJudge.judge` or any equivalent caller-supplied value.
`is_correct` is determined externally — this library never invents the correctness signal.

#### `class ConfidenceSample`

```python
@dataclass(frozen=True, slots=True)
class ConfidenceSample:
    predicted_label: str
    verbalized_confidence: str
    predicted_confidence: float
    raw_response: str
```

One parsed self-consistency sample. `verbalized_confidence` is the raw label produced by the model
(`low` / `medium` / `high`); `predicted_confidence` is the numeric mapping per
`LABEL_TO_CONFIDENCE`. `raw_response` is preserved for debugging and audit.

#### `class ConfidenceAggregate`

```python
@dataclass(frozen=True, slots=True)
class ConfidenceAggregate:
    predicted_label: str
    predicted_confidence: float
    samples: tuple[ConfidenceSample, ...]
```

Output of `ConfidenceJudge.aggregate`. The aggregated `predicted_label` is the majority vote winner;
on a 3-way tie it is the highest-confidence sample's label.

#### `class MalformedConfidenceError(ValueError)`

Raised by `_parse_confidence_label` when no `low|medium|high` token can be located in a model
response. Subclassing `ValueError` so callers can catch with either type.

#### `class ConfidencePromptTemplate`

```python
@dataclass(frozen=True, slots=True)
class ConfidencePromptTemplate:
    template: str = DEFAULT_PROMPT_TEMPLATE

    def format(self, *, problem: str, action: str) -> str: ...
```

Frozen dataclass holding the prompt template body. The default template is the Xiong2024 §3.2
human-inspired prompt with `{problem}` and `{action}` placeholders. `__post_init__` validates that
both placeholders are present.

#### `class ConfidenceJudge`

```python
@dataclass(slots=True)
class ConfidenceJudge:
    samples: int = SELF_CONSISTENCY_SAMPLES  # 3
    prompt_template: ConfidencePromptTemplate = ...

    def aggregate(
        self, confidence_samples: Sequence[ConfidenceSample]
    ) -> ConfidenceAggregate: ...

    def judge(
        self, *,
        problem_id: str,
        problem: str,
        sampled_actions: Sequence[str],
        gold_action: str,
        model_call: ModelCall,
    ) -> CalibrationRecord: ...
```

`aggregate` does the math: majority vote on `predicted_label`, mean confidence within the majority
cohort. On a 3-way tie (every sample distinct), returns the sample with the highest
`predicted_confidence` (first wins on equal max). `judge` is the end-to-end driver: for each sampled
action it calls `model_call`, parses the response into a `ConfidenceSample`, and aggregates.

#### `def elicit_confidence`

```python
def elicit_confidence(
    *,
    model_call: ModelCall,
    problem: str,
    action: str,
    prompt_template: ConfidencePromptTemplate | None = None,
) -> tuple[str, float]:
    ...
```

Single-call helper. Renders the prompt, invokes `model_call`, parses the response, and returns
`(verbalized_label, numeric_confidence)`. Raises `MalformedConfidenceError` if no label can be
found.

#### `def compute_overconfident_error_rate`

```python
def compute_overconfident_error_rate(
    *,
    records: Iterable[CalibrationRecord],
    threshold: float = HIGH_CONFIDENCE_THRESHOLD,
) -> float:
    ...
```

Returns the fraction of records with `not is_correct and predicted_confidence >= threshold`. Returns
`0.0` for empty input. The default `HIGH_CONFIDENCE_THRESHOLD` is `0.75` (the Xiong2024 high-bucket
boundary, sitting strictly between `medium` (0.5) and `high` (0.9)).

#### `def calibration_record_from_trajectory`

```python
def calibration_record_from_trajectory(
    *,
    problem_id: str,
    record: Mapping[str, object],
    is_correct: bool,
) -> CalibrationRecord:
    ...
```

Adapter that converts a trajectory record produced by t0006/t0007/t0010 (canonical
`TRAJECTORY_RECORD_FIELDS` schema) into a `CalibrationRecord`. Accepts both verbalized (`"high"`)
and numeric (`0.42`) values for the `confidence` field. Raises if `confidence` is `None` because the
metric is undefined without a confidence value.

### `code/constants.py`

Exposes `LIBRARY_NAME`, `LIBRARY_VERSION`, the verbalized labels (`LABEL_LOW`, `LABEL_MEDIUM`,
`LABEL_HIGH`), the numeric mapping `LABEL_TO_CONFIDENCE`, `SELF_CONSISTENCY_SAMPLES = 3`,
`HIGH_CONFIDENCE_THRESHOLD = 0.75`, the trajectory field names, and the `DEFAULT_PROMPT_TEMPLATE`
body.

## Usage Examples

End-to-end with a deterministic fake model:

```python
from dataclasses import dataclass, field

from tasks.t0011_metric2_calibration_aggregator.code.calibration import (
    CalibrationRecord,
    ConfidenceJudge,
    compute_overconfident_error_rate,
)


@dataclass(slots=True)
class ScriptedModel:
    responses: list[str]
    cursor: int = field(default=0)

    def __call__(self, *, prompt: str) -> str:
        out = self.responses[self.cursor]
        self.cursor += 1
        return out


model = ScriptedModel(
    responses=[
        "Confidence: high\nClear arithmetic.",
        "Confidence: high\nSecond opinion agrees.",
        "Confidence: medium\nSlight doubt.",
    ],
)

judge = ConfidenceJudge()
record = judge.judge(
    problem_id="p1",
    problem="What is 2+2?",
    sampled_actions=["Add 2 and 2", "Add 2 and 2", "Multiply 2 by 2"],
    gold_action="Add 2 and 2",
    model_call=model,
)

records: list[CalibrationRecord] = [record]
metric_value = compute_overconfident_error_rate(records=records)
```

Adapting an existing trajectory record:

```python
from tasks.t0011_metric2_calibration_aggregator.code.calibration import (
    calibration_record_from_trajectory,
)

trajectory_record = {
    "turn_index": 0,
    "granularity": "unspecified",
    "thought": "Reasoning ...",
    "action": "do_x",
    "observation": "ok",
    "confidence": "high",
}

record = calibration_record_from_trajectory(
    problem_id="p42",
    record=trajectory_record,
    is_correct=False,
)
```

## Dependencies

No external dependencies. The library uses only the Python standard library (`dataclasses`, `re`,
`collections`, `collections.abc`, `typing`, `pathlib`). Tests use `pytest`, which is already a
project-level dependency.

## Testing

Run the test suite with:

```bash
uv run pytest tasks/t0011_metric2_calibration_aggregator/code/ -v
```

The suite contains 25 tests covering: prompt template construction and validation, case-insensitive
label parsing for low / medium / high (including freeform-text fallback and the malformed-input
error path), aggregation under clean 2-1 majorities (cohort-mean verification), unanimous votes,
3-way ties (highest-confidence tiebreak with deterministic first-wins behavior on equal max), the
threshold boundary at 0.75 (`>=` qualifies), correct predictions never counting as overconfident
errors, the empty-input contract, a synthetic 10-record end-to-end run, custom-threshold behavior,
the trajectory-record adapter for both verbalized and numeric confidence values, the adapter's
None-confidence error path, and a sanity check that the Xiong2024 protocol constants have the
expected values.

All 25 tests pass on the project's `uv` environment in well under one second; there are no live API
calls.

## Main Ideas

* **Xiong2024 protocol verbatim**: the prompt template, the `low → 0.25`, `medium → 0.5`,
  `high → 0.9` mapping, the 3-sample self-consistency aggregation, and the high-confidence threshold
  of 0.75 all come directly from the canonical paper. Future tasks that disagree with any of these
  values can override them in one place (`constants.py`) without forking the library or rewriting
  any test.
* **Cohort mean, not global mean**: the aggregated confidence is the mean within the majority
  cohort, not the global mean across all samples. This matches Xiong2024's self-consistency rule and
  is the most commonly missed implementation detail. The test suite asserts this explicitly.
* **Deterministic tie-breaker**: 3-way ties (every sample distinct) fall back to the
  highest-confidence sample with first-wins on equal max. This is conservative — it surfaces the
  model's most-confident wrong answer when the model itself cannot agree — and it makes every
  aggregation reproducible.
* **No live API calls in tests**: the test suite uses a `ScriptedModel`-shaped fake mirroring
  t0007's interface. The library never imports from t0007 directly (per the project's cross-task
  import rule); any caller that wants to use t0007's `ScriptedModel` simply passes it as the
  `model_call` argument.
* **Trajectory-record compatibility**: the `calibration_record_from_trajectory` adapter consumes
  records emitted by t0006/t0007/t0010 (the canonical `TRAJECTORY_RECORD_FIELDS` schema) and
  produces `CalibrationRecord` values directly, so the experiment harness in t0012 can plug this
  library in without any glue code.
* **None-confidence rejection**: a trajectory record with `confidence=None` is a hard error, not a
  silent skip. The metric is undefined without a confidence value, and silently imputing a default
  would corrupt the numerator.

## Summary

This library implements the project's Metric 2 (`overconfident_error_rate`) as a tightly scoped,
dependency-free Python module. It provides the Xiong2024 §3.2 human-inspired confidence-elicitation
prompt, a 3-sample self-consistency aggregator, and the binary overconfident-error metric itself.
All protocol parameters — the verbalized-to-numeric mapping, the high-confidence threshold, the
sample count — live in `constants.py` as overridable module-level values, so future tasks can run
sweeps without forking any code.

The library fits the project as the missing piece between the trajectory libraries
(t0006/t0007/t0010, which produce `TRAJECTORY_RECORD_FIELDS` records) and the Phase 2 smoke
experiment harness (t0012, which needs a single number to put in `metrics.json`). The
`calibration_record_from_trajectory` adapter accepts trajectory records directly; the
`compute_overconfident_error_rate` function returns a `float` ready to write into the
`overconfident_error_rate` field of `metrics.json`. There is no other glue code needed.

Limitations and future work: the current implementation reports only the binary overconfident-error
rate. A future task should add Expected Calibration Error (ECE) computation with bucketed plots, per
the Xiong2024 reporting convention, and a provider-specific calibration variant that adjusts the
prompt template for models that respond differently to the human-inspired prompt (e.g.,
reasoning-focused vs. instruction-tuned models). The threshold default and the verbalized-to-numeric
mapping are both exposed as overridable constants, so a downstream task can sweep them end-to-end
without modifying this library.
