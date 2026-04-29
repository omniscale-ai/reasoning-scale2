---
spec_version: "3"
task_id: "t0007_scope_unaware_planandsolve_library"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T19:50:53Z"
completed_at: "2026-04-29T20:00:00Z"
---
# Step 9: implementation

## Summary

Implemented the scope-unaware Plan-and-Solve library as `code/planandsolve.py`, wrote a 14-case
pytest suite in `code/test_planandsolve.py` (all passing), and authored the library asset metadata
(`assets/library/scope_unaware_planandsolve_v1/details.json` and `description.md`). All quality
gates pass: ruff with zero errors, mypy with zero errors, pytest 14/14, and
`meta.asset_types.library.verificator` passed with zero errors and zero warnings. The library
exports `TRAJECTORY_RECORD_FIELDS` so sister task t0006 can import-and- assert schema parity when
its branch reaches implementation.

## Actions Taken

1. Wrote `code/planandsolve.py` with the trajectory dataclass, `ScriptedModel`, plan parser,
   executor-output parser, and the `PlanAndSolveAgent` class.
2. Wrote `code/test_planandsolve.py` with 14 deterministic test cases covering the full plan
   `## Verification Criteria` matrix (REQ-3 through REQ-8).
3. Ran `uv run ruff check --fix` (auto-fixed 2; remaining 3 UP040 errors fixed manually by replacing
   `TypeAlias` with the `type` keyword).
4. Ran `uv run ruff format`, `uv run mypy -p tasks.t0007_scope_unaware_planandsolve_library.code`,
   and `uv run pytest tasks/t0007_scope_unaware_planandsolve_library/code/`. All pass.
5. Authored the library asset (`details.json` + `description.md`) per the v2 library asset
   specification, with the trajectory schema documented in a `## Trajectory Schema` block and the
   LangChain Apache-2.0 attribution in a `## License & Attribution` block.
6. Ran
   `uv run python -m meta.asset_types.library.verificator --task-id t0007_scope_unaware_planandsolve_library`
   — passed with zero errors and zero warnings.

## Outputs

* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py`
* `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py`
* `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/details.json`
* `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/description.md`
* `tasks/t0007_scope_unaware_planandsolve_library/logs/steps/009_implementation/step_log.md`

## Issues

The library asset specification's `entry_points[].kind` field only allows `"function"`, `"class"`,
or `"script"`, so the module-level constant `TRAJECTORY_RECORD_FIELDS` could not be listed in
`entry_points`; it is documented in the `## API Reference > Module-level constants` section of
`description.md` instead. No other issues encountered. All 9 REQ items in `plan/plan.md` are
satisfied — see the Requirement Completion Checklist below.

## Requirement Completion Checklist

* REQ-1 (library asset folder): **done** — `assets/library/scope_unaware_planandsolve_v1/` exists;
  verificator passes.
* REQ-2 (`PlanAndSolveAgent` class with deterministic-test mode): **done** — `PlanAndSolveAgent` and
  `ScriptedModel` implemented and tested.
* REQ-3 (numbered plan generation + sequential execution): **done** — `parse_plan` plus the `run()`
  loop; `test_sequential_execution` passes.
* REQ-4 (trajectory record schema parity): **done** — `TrajectoryRecord` dataclass plus
  `TRAJECTORY_RECORD_FIELDS` export; `test_trajectory_schema_parity` and
  `test_trajectory_record_fields_match_canonical_tuple` pass.
* REQ-5 (`granularity == "unspecified"` on every B record): **done** —
  `test_granularity_unspecified` passes.
* REQ-6 (deterministic-test mode): **done** — `ScriptedModel`; `test_scripted_model_round_trip`
  passes.
* REQ-7 (LangChain Apache-2.0 attribution): **done** — `## License & Attribution` block in
  `description.md`.
* REQ-8 (pytest coverage): **done** — 14 named test cases; all pass.
* REQ-9 (trajectory schema documented for t0006): **done** — `## Trajectory Schema` block in
  `description.md` with table, JSON example, and assertion snippet.
