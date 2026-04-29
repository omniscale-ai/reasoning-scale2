---
spec_version: "3"
task_id: "t0011_metric2_calibration_aggregator"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T23:34:13Z"
completed_at: "2026-04-29T23:55:00Z"
---
# Step 9: implementation

## Summary

Implemented the metric2_calibration_aggregator_v1 library: `code/calibration.py` (the library
itself, ~340 lines), `code/constants.py` (Xiong2024 protocol parameters), `code/paths.py`
(filesystem constants), and `code/test_calibration.py` (25 deterministic tests, all pass). The
library asset folder `assets/library/metric2_calibration_aggregator_v1/` contains `details.json` and
`description.md` and passes the library verificator with zero errors and zero warnings. ruff check
and ruff format both pass; mypy on the full task package reports zero issues across 21 source files;
pytest reports 25 passed in 0.03s.

## Requirement Completion Checklist

* **REQ-1**: done — `assets/library/metric2_calibration_aggregator_v1/details.json` and
  `description.md` exist and pass the verificator.
* **REQ-2**: done — `code/calibration.py` defines `CalibrationRecord`, `ConfidencePromptTemplate`,
  `ConfidenceJudge`, `compute_overconfident_error_rate`, and `elicit_confidence` plus the supporting
  `ConfidenceSample`, `ConfidenceAggregate`, and `MalformedConfidenceError`.
* **REQ-3**: done — `calibration_record_from_trajectory` adapts t0006/t0007/t0010 trajectory records
  (canonical `TRAJECTORY_RECORD_FIELDS` schema) into `CalibrationRecord` values; tests cover both
  verbalized and numeric confidence inputs.
* **REQ-4**: done — `code/test_calibration.py` covers prompt template formatting and validation,
  label parsing for low / medium / high (including freeform-text fallback and the malformed-input
  error path), aggregator clean majorities, unanimous votes, 3-way ties (with deterministic
  tiebreak), threshold boundary at 0.75, end-to-end synthetic 10-record run, and custom thresholds.
* **REQ-5**: done — `HIGH_CONFIDENCE_THRESHOLD = 0.75` and the verbalized-label mapping (low → 0.25,
  medium → 0.5, high → 0.9) are exposed as module constants in `code/constants.py`. A test asserts
  these values explicitly.
* **REQ-6**: done — tests use a local `ScriptedModel` dataclass mirroring t0007's interface (no live
  API calls, no cross-task imports).
* **REQ-7**: done — `uv run ruff check tasks/t0011_metric2_calibration_aggregator/code/`,
  `uv run ruff format`, and `uv run mypy -p tasks.t0011_metric2_calibration_aggregator` all pass.
* **REQ-8**: done — `uv run pytest tasks/t0011_metric2_calibration_aggregator/code/` reports
  `25 passed in 0.03s`.

## Actions Taken

1. Wrote `code/paths.py` with `pathlib.Path` constants for the task root, code directory, and
   library asset paths.
2. Wrote `code/constants.py` with all Xiong2024 protocol parameters as module-level `Final[...]`
   constants (verbalized labels, numeric mapping, threshold default of 0.75, sample count of 3,
   prompt template body, trajectory field names).
3. Wrote `code/calibration.py` implementing `CalibrationRecord`, `ConfidenceSample`,
   `ConfidenceAggregate`, `MalformedConfidenceError`, `ConfidencePromptTemplate`, `ConfidenceJudge`
   (with `aggregate` and `judge` methods), `elicit_confidence`, `compute_overconfident_error_rate`,
   and `calibration_record_from_trajectory`.
4. Wrote `code/test_calibration.py` with 25 deterministic pytest cases covering every public API
   surface and edge case.
5. Ran `ruff check --fix` (3 errors found, 2 auto-fixed, 1 line-length error in `constants.py` fixed
   by hand by rephrasing the docstring); re-ran `ruff check` and `ruff format` — clean.
6. Ran `mypy -p tasks.t0011_metric2_calibration_aggregator` — clean across 21 source files.
7. Ran `pytest tasks/t0011_metric2_calibration_aggregator/code/ -v` — 25 passed in 0.03 s.
8. Wrote `assets/library/metric2_calibration_aggregator_v1/details.json` per the v2 library asset
   spec, listing all six entry points, the three module paths, the test path, and the
   `uncertainty-calibration` category.
9. Wrote `assets/library/metric2_calibration_aggregator_v1/description.md` with all seven mandatory
   sections (Metadata, Overview, API Reference, Usage Examples, Dependencies, Testing, Main Ideas,
   Summary) plus the v2 frontmatter.
10. Ran the library asset verificator
    (`python -m meta.asset_types.library.verificator --task-id t0011_metric2_calibration_aggregator metric2_calibration_aggregator_v1`)
    — passed with zero errors and zero warnings.

## Outputs

* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py`
* `tasks/t0011_metric2_calibration_aggregator/code/constants.py`
* `tasks/t0011_metric2_calibration_aggregator/code/paths.py`
* `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py`
* `tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/details.json`
* `tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/description.md`

## Issues

`uv run mypy -p tasks.t0011_metric2_calibration_aggregator.code` initially reported only one source
file because the `code` package alone has no `__init__.py`-level imports tying the four files
together. Resolved by running `mypy -p tasks.t0011_metric2_calibration_aggregator` (the parent
package) to type-check all 21 source files reachable from the task root. Both invocations report
zero errors.
