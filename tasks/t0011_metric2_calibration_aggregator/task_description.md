# Metric 2 Calibration Aggregator (Xiong2024 Protocol)

## Motivation

The project's Metric 2 (`overconfident_error_rate`) has no implementation: it is registered in
`meta/metrics/` but no code computes it. The literature survey (t0002) identified Xiong2024 as the
canonical calibration protocol — verbalized confidence elicitation (low / medium / high + brief
justification) plus 3-sample self-consistency aggregation. Without this library, the Phase 2 smoke
test (t0012) cannot report Metric 2 — only Metric 1 (success rate) and the diagnostic Metric 3 (avg
decisions per task). This task unblocks the headline experiment by producing a library that any
agent's trajectory records can be passed through to compute `overconfident_error_rate`. Implements
suggestion S-0002-02.

## Scope

* Implement a library asset under `assets/library/metric2_calibration_aggregator_v1/` exposing:
  * `class ConfidencePromptTemplate`: the human-inspired confidence-elicitation prompt (low / medium
    / high + one-sentence justification) per Xiong2024 §3.2.
  * `class ConfidenceJudge`: aggregator that takes 3 trajectory samples for the same problem and
    returns `(predicted_label, predicted_confidence, is_correct)`. Self-consistency is majority-vote
    on the predicted label; confidence is the mean across samples.
  * `function compute_overconfident_error_rate(records: Iterable[CalibrationRecord]) -> float` that
    returns the fraction of records where `is_correct == False` and `predicted_confidence
    > = HIGH_CONFIDENCE_THRESHOLD`. The threshold is a module constant (default 0.75).
  * `function elicit_confidence(model_call, problem, action) -> tuple[str, float]` that calls the
    model with the prompt template and parses the response.
  * `dataclass CalibrationRecord(frozen=True, slots=True)`: the canonical record shape that
    `compute_overconfident_error_rate` consumes.
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e., must
  consume the canonical `TRAJECTORY_RECORD_FIELDS` schema as input.
* Provide pytest coverage at `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py`
  covering: prompt template formatting, parsing of low / medium / high confidence labels,
  majority-vote aggregation across 3 samples (including ties), threshold-based overconfident
  detection, and end-to-end run on a synthetic 10-record dataset.

Out of scope: the actual experiment harness (handled by t0012), live API calls (deterministic tests
only), provider-specific calibration variants.

## Approach

1. Read t0002's Xiong2024 paper summary
   (`tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md`)
   to ground the prompt template and threshold choice.
2. Implement in `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` with a `paths.py`
   and `constants.py` per the project Python style guide.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests use `ScriptedModel` from t0007 to simulate model responses for the confidence prompt.
5. Run `verify_library_asset`, ruff, mypy, and pytest.

## Expected Outputs

* `assets/library/metric2_calibration_aggregator_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` and tests.
* `results/results_summary.md` with API surface description, test summary, and the threshold default
  rationale.
* Follow-up suggestion for: provider-specific calibration variants, ECE (expected calibration error)
  computation in addition to overconfident-error-rate.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Xiong2024 paper asset (`10.48550_arXiv.2306.13063`) from t0002's library.
* Output format consumed by t0012's experiment harness.

## Source Suggestion

S-0002-02 — "Implement verbalized-confidence + 3-sample self-consistency aggregator for Metric 2."

## Key Questions

1. What is the right default `HIGH_CONFIDENCE_THRESHOLD`? Xiong2024 uses 0.75 with verbalized labels
   mapped to {low: 0.25, medium: 0.5, high: 0.9}; the default should match.
2. How should the aggregator handle ties in the majority vote across 3 samples? Default: prefer the
   highest-confidence sample.
3. What is the expected output schema for compute_overconfident_error_rate so Phase 2 results can
   include it in `metrics.json` directly?
