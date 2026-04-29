---
spec_version: "2"
task_id: "t0011_metric2_calibration_aggregator"
date_completed: "2026-04-29"
status: "complete"
---
# Plan: Metric 2 Calibration Aggregator (Xiong2024 Protocol)

## Objective

Implement a small, self-contained Python library that operationalizes the project's Metric 2
(`overconfident_error_rate`) using the Xiong2024 black-box calibration protocol — verbalized "low /
medium / high" confidence elicitation plus 3-sample self-consistency aggregation. "Done" means: a
registered `library` asset under `assets/library/metric2_calibration_aggregator_v1/` exists with
`details.json` and `description.md`; the Python module `code/calibration.py` implements the public
API surface listed in the task description; pytest covers the prompt template, label parser,
aggregator, threshold rule, and an end-to-end synthetic 10-record run; ruff, mypy, and
`verify_library_asset` all pass with zero errors.

## Task Requirement Checklist

```text
Task: Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency.

Short description: Write-library implementing the Xiong2024 verbalized-confidence + 3-sample
self-consistency aggregator that computes overconfident_error_rate.

Long description (excerpt):
* Implement a library asset under `assets/library/metric2_calibration_aggregator_v1/` exposing
  ConfidencePromptTemplate, ConfidenceJudge, compute_overconfident_error_rate(records),
  elicit_confidence(model_call, problem, action) -> (label, confidence), and CalibrationRecord
  (frozen dataclass).
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e.,
  must consume the canonical TRAJECTORY_RECORD_FIELDS schema as input.
* Provide pytest coverage at code/test_calibration.py covering: prompt template formatting,
  parsing of low/medium/high confidence labels, majority-vote aggregation across 3 samples
  (including ties), threshold-based overconfident detection, and end-to-end run on a synthetic
  10-record dataset.
* Out of scope: the actual experiment harness, live API calls, provider-specific calibration.
* Default HIGH_CONFIDENCE_THRESHOLD = 0.75 with verbalized labels mapped to
  {low: 0.25, medium: 0.5, high: 0.9}.
* Tests use ScriptedModel from t0007 to simulate model responses for the confidence prompt.
```

* **REQ-1**: Library asset folder `assets/library/metric2_calibration_aggregator_v1/` with
  `details.json` and `description.md` that pass `verify_library_asset`. Satisfied in Step 6.
* **REQ-2**: `code/calibration.py` defines `ConfidencePromptTemplate`, `ConfidenceJudge`,
  `compute_overconfident_error_rate`, `elicit_confidence`, and `CalibrationRecord` with the exact
  signatures from the task description. Satisfied in Steps 2-4.
* **REQ-3**: Library accepts records whose schema is the canonical `TRAJECTORY_RECORD_FIELDS` tuple
  from t0007 — at minimum the fields `granularity`, `action`, and `confidence` must round trip
  without modification. Satisfied in Step 3 by adapting trajectory records into `CalibrationRecord`
  via a documented `from_trajectory_record` helper.
* **REQ-4**: `code/test_calibration.py` covers prompt template formatting, parsing of low / medium /
  high (and malformed input), majority-vote aggregation including ties, threshold-based
  overconfident detection, and an end-to-end synthetic 10-record run. Satisfied in Step 5.
* **REQ-5**: Default `HIGH_CONFIDENCE_THRESHOLD = 0.75` and verbalized-label mapping
  `low → 0.25, medium → 0.5, high → 0.9` are exposed as module constants in `code/constants.py`.
  Satisfied in Step 1.
* **REQ-6**: Tests use a `ScriptedModel`-shaped fake (no live API calls). Satisfied in Step 5 via a
  local `ScriptedModel` dataclass mirroring t0007's interface.
* **REQ-7**: ruff, ruff format, and `mypy -p tasks.t0011_metric2_calibration_aggregator.code` all
  pass. Satisfied in Step 7.
* **REQ-8**: `pytest tasks/t0011_metric2_calibration_aggregator/code/` runs all tests and 0
  failures. Satisfied in Step 7.

## Approach

The library is a single-file module (`code/calibration.py`) plus `paths.py` and `constants.py`.
There are no external dependencies beyond the standard library. The design follows Xiong2024 §3.2
verbatim: the human-inspired prompt template asks for a `Confidence:` line with one of the three
verbalized labels and a one-sentence justification; the parser maps `low → 0.25`, `medium → 0.5`,
`high → 0.9`; the aggregator does majority vote on the predicted action across 3 samples and returns
the mean confidence within the majority cohort; on a 3-way tie it returns the highest-confidence
sample. The high-confidence threshold default is 0.75 because it sits strictly between the medium
and high anchor points and matches the Xiong2024 high-bucket boundary (research_papers.md,
"Operational Definition of Overconfident Error" finding).

Compatibility with t0007's `TRAJECTORY_RECORD_FIELDS` is achieved by defining `CalibrationRecord` as
a frozen dataclass with three fields the aggregator needs (`predicted_label`,
`predicted_confidence`, `is_correct`) plus a constructor helper
`from_trajectory_record(record, is_correct)` that pulls `action` and `confidence` out of any mapping
using the canonical field names. This keeps the library independent of t0007's concrete
`TrajectoryRecord` class while honoring its schema.

**Alternative considered**: a fully open generic `Iterable[Mapping]` API where the aggregator
re-parses the trajectory records every call. Rejected because Xiong2024's metric is computed at the
per-problem (not per-step) level, so an explicit `CalibrationRecord` makes the granularity boundary
unambiguous and lets the type checker enforce the contract.

**Task type**: `write-library` (matches `task.json`). The write-library Planning Guidelines drove
the decision to (a) keep the public API minimal, (b) put all magic numbers in `constants.py`, (c)
write tests covering both happy paths and edge cases (3-way tie, malformed input, empty record
list).

## Cost Estimation

* OpenAI / Anthropic / vast.ai: $0 — no live API calls. Tests use a `ScriptedModel` fake.
* Compute: $0 — runs locally on the project's `uv` environment.
* Total: $0. Project budget unaffected.

## Step by Step

1. **Create `code/paths.py` and `code/constants.py`.** Define `TASK_ROOT`, `CODE_DIR`,
   `LIBRARY_ASSET_DIR` as `pathlib.Path` constants. In `constants.py` define
   `LIBRARY_ID = "metric2_calibration_aggregator_v1"`, the verbalized labels (`LABEL_LOW`,
   `LABEL_MEDIUM`, `LABEL_HIGH`), the numeric mapping `LABEL_TO_CONFIDENCE: dict[str, float]`,
   `HIGH_CONFIDENCE_THRESHOLD: float = 0.75`, `SELF_CONSISTENCY_SAMPLES: int = 3`, and the
   `TRAJECTORY_FIELD_*` constants matching t0007's `TRAJECTORY_RECORD_FIELDS`. Satisfies REQ-5.

2. **Implement `code/calibration.py` core dataclasses.** Define
   `CalibrationRecord(frozen=True, slots=True)` with fields
   `(problem_id: str, predicted_label: str, predicted_confidence: float, is_correct: bool)`. Define
   `ConfidenceSample(frozen=True, slots=True)` with
   `(predicted_label: str, verbalized_confidence: str, predicted_confidence: float, raw_response: str)`.
   Define `ConfidenceAggregate(frozen=True, slots=True)` with
   `(predicted_label: str, predicted_confidence: float, samples: tuple[ConfidenceSample, ...])`.
   Define `MalformedConfidenceError(ValueError)`. Satisfies REQ-2.

3. **Implement `ConfidencePromptTemplate` and `elicit_confidence`.** `ConfidencePromptTemplate` is a
   frozen dataclass with `template: str` and `format(problem, action) -> str` returning the literal
   Xiong2024 human-inspired prompt with `{problem}` and `{action}` substituted.
   `elicit_confidence(model_call, problem, action) -> tuple[str, float]` formats the prompt, calls
   `model_call`, parses the first matching `low|medium|high` token case-insensitively (preferring a
   `Confidence: <label>` line), and returns
   `(verbalized_label, LABEL_TO_CONFIDENCE[verbalized_label])`. Raise `MalformedConfidenceError` if
   no label is found. Satisfies REQ-2 and REQ-3.

4. **Implement `ConfidenceJudge` and `compute_overconfident_error_rate`.** `ConfidenceJudge` stores
   `prompt_template`, `samples` (default 3), and the `LABEL_TO_CONFIDENCE` mapping. Method
   `aggregate(samples: Sequence[ConfidenceSample]) -> ConfidenceAggregate` does majority vote on
   `predicted_label`; returns the mean confidence within the majority cohort. On a 3-way tie,
   returns the sample with the highest `predicted_confidence`. Method
   `judge(problem_id, problem, predicted_actions, gold_action) -> CalibrationRecord` calls
   `elicit_confidence` once per action (assumed already sampled), aggregates, and returns the
   `CalibrationRecord` with `is_correct = aggregate.predicted_label == gold_action`.
   `compute_overconfident_error_rate(records: Iterable[CalibrationRecord], threshold: float = HIGH_CONFIDENCE_THRESHOLD) -> float`
   returns the fraction with `not is_correct and predicted_confidence >= threshold`; returns `0.0`
   when the input iterable is empty. Satisfies REQ-2.

5. **Write `code/test_calibration.py`.** Use pytest. Define a local
   `ScriptedModel(responses: list[str])` callable mirroring t0007's interface (raises IndexError on
   exhaustion). Cover: (a) prompt template formats `{problem}`/`{action}` correctly; (b) parser
   handles `low`, `medium`, `high`, mixed case, embedded labels, and `Confidence: high` prefix; (c)
   parser raises `MalformedConfidenceError` on unparseable response; (d) aggregator majority vote
   with clean 2-1 split (returns mean confidence within majority); (e) aggregator 3-way tie returns
   highest-confidence sample; (f) threshold-based overconfident detection at the boundary value 0.75
   (>= must qualify); (g) end-to-end run on a synthetic 10-record dataset producing the expected
   fraction. Satisfies REQ-4 and REQ-6.

6. **Create the library asset folder.** Write
   `assets/library/metric2_calibration_aggregator_v1/ details.json` per the library asset
   specification with `module_paths` listing `code/calibration.py`, `code/paths.py`,
   `code/constants.py`; `entry_points` listing `ConfidencePromptTemplate`, `ConfidenceJudge`,
   `compute_overconfident_error_rate`, `elicit_confidence`, `CalibrationRecord`; `test_paths`
   listing `code/test_calibration.py`; `categories: ["uncertainty-calibration"]`. Write
   `assets/library/metric2_calibration_aggregator_v1/description.md` with the seven mandatory
   sections (Metadata, Overview, API Reference, Usage Examples, Dependencies, Testing, Main Ideas,
   Summary). Satisfies REQ-1.

7. **Quality gate.** Run, in this order:
   `uv run ruff check --fix tasks/t0011_metric2_calibration_aggregator/code/`,
   `uv run ruff format tasks/t0011_metric2_calibration_aggregator/code/`,
   `uv run mypy -p tasks.t0011_metric2_calibration_aggregator.code`, and
   `uv run pytest tasks/t0011_metric2_calibration_aggregator/code/`. Fix any complaints. Run
   `uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0011_metric2_calibration_aggregator metric2_calibration_aggregator_v1`
   and confirm zero errors. Satisfies REQ-7 and REQ-8.

## Remote Machines

None required. All work runs locally with `uv`. No remote compute, no GPU.

## Assets Needed

* Xiong2024 paper summary at
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md`
  (already present in the project corpus). No other inputs required.

## Expected Assets

* One library asset: `assets/library/metric2_calibration_aggregator_v1/`. Library ID:
  `metric2_calibration_aggregator_v1`. Short description: "Verbalized-confidence + 3-sample
  self-consistency aggregator that computes overconfident_error_rate per the Xiong2024 protocol."
  Module paths: `code/calibration.py`, `code/paths.py`, `code/constants.py`. Categories:
  `uncertainty-calibration`.

## Time Estimation

* Implementation (Steps 1-4): ~30 min wall-clock.
* Tests (Step 5): ~15 min.
* Library asset metadata (Step 6): ~10 min.
* Quality gate and verificator (Step 7): ~10 min.
* Total: ~65 min for the implementation phase.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Parser too strict, fails on lowercase-only output | Medium | Medium | Case-insensitive regex; accept first matching label anywhere in response |
| `mypy -p` fails on package layout | Low | Medium | Use `tasks/$TASK_ID/__init__.py` and `code/__init__.py` already created in init-folders |
| Verificator `LA-W014` warns on missing test_paths | Low | Low | Test file is part of the asset; list it in `test_paths` |
| Threshold default disagrees with Xiong2024 PDF (not yet downloaded) | Low | Low | Threshold is exposed as a module constant — overrideable in one line |
| 3-way tie behavior mismatches a future caller's expectation | Medium | Low | Document the rule in the description's Main Ideas section and surface it in a test |
| Pre-commit hook trim-trailing-whitespace rewrites generated logs and aborts commit | Medium | Low | Re-add files and re-commit; this is normal |

## Verification Criteria

* `uv run pytest tasks/t0011_metric2_calibration_aggregator/code/` reports 0 failures and at least 8
  tests run, covering REQ-4 (prompt template, parser low/medium/high, malformed input, aggregator
  clean majority, aggregator 3-way tie, threshold boundary, end-to-end 10-record run).
* `uv run ruff check tasks/t0011_metric2_calibration_aggregator/code/` exits 0.
* `uv run mypy -p tasks.t0011_metric2_calibration_aggregator.code` exits 0.
* `uv run python -u -m arf.scripts.verificators.verify_library_asset --task-id t0011_metric2_calibration_aggregator metric2_calibration_aggregator_v1`
  reports zero errors.
* `assets/library/metric2_calibration_aggregator_v1/details.json` lists the five entry points named
  in REQ-2 with correct `kind` and `module` fields.
* `assets/library/metric2_calibration_aggregator_v1/description.md` contains all seven mandatory
  sections (Metadata, Overview, API Reference, Usage Examples, Dependencies, Testing, Main Ideas,
  Summary).
