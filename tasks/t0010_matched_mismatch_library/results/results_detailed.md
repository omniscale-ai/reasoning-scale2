---
spec_version: "2"
task_id: "t0010_matched_mismatch_library"
---
# Results Detailed: Matched-Mismatch Library (Condition C)

## Summary

Delivered the project's condition-C library, `matched_mismatch_v1`, as a write-library task with
zero external cost. The library exposes a `MatchedMismatchAgent` class that walks a v2 hierarchy
from t0009 in canonical phase order, substitutes a deliberately incorrect granularity tag at each
step, and delegates per-phase model calls to either the t0006 ReAct or t0007 Plan-and-Solve prompt
format. The trajectory record schema (`TRAJECTORY_RECORD_FIELDS`) from t0007 is reused unchanged;
the correct tag is recorded under `extras["_correct_granularity"]`. All 14 deterministic tests pass
and the library asset verificator reports zero errors and zero warnings.

## Methodology

* **Machine specs**: local development (Apple Darwin 25.3.0, Python 3.13.11). No remote compute.
* **Runtime**: implementation + tests + asset writing wall-clock < 10 minutes; pytest suite runs in
  0.04s.
* **Timestamps**: implementation step started 2026-04-29T23:34:58Z; results step started
  2026-04-29T23:41:44Z.
* **Approach**: per-phase model call with delegate-specific prompt format and output parser. The
  wrapper drives the v2-walk loop itself rather than calling each delegate's outer `run()`, because
  each delegate's `run()` runs its own multi-turn loop that would conflict with the per-phase walk.
  The wrapper reuses each delegate's *parsing* logic (`_parse_model_output` from t0006,
  `_parse_executor_output` from t0007) so the prompt-format and output-parser axis is delegated
  correctly.
* **Test design**: deterministic via `ScriptedModel` from t0006 and t0007. Random-strategy
  uniformity is verified across N=300 trials per correct tag with a 100/300 lower-bound acceptance
  band (well within the fair-coin 3-sigma envelope).

## Verification

* `verify_research_papers.py` — PASSED (0 errors, 0 warnings).
* `verify_plan.py` — PASSED (0 errors, 0 warnings).
* `meta/asset_types/library/verificator.py` — PASSED (0 errors, 0 warnings).
* `ruff check` — 0 issues.
* `ruff format` — clean.
* `mypy -p tasks.t0010_matched_mismatch_library.code` — 0 issues.
* `pytest tasks/t0010_matched_mismatch_library/code/` — 14 of 14 PASSED.

## Limitations

* The wrapper does not propagate any post-`run()` book-keeping the delegates do (e.g., t0006's
  `TrajectoryWriter` writing a JSONL file). Consumers that need that side effect must invoke the
  delegates directly or open an issue against this library.
* The mismatch strategy is a single literal applied uniformly across all phases; per-step strategy
  overrides are not currently supported.
* `subtask` is equidistant from `global` and `atomic` in the adversarial map; the choice
  `subtask → atomic` is documented and pinned by tests but represents one of two reasonable
  interpretations of "most distant tag" for `subtask`.
* Phase-order vs. mismatched-tag confound (per the research synthesis) is not addressed by this
  library — t0012 must include a phase-randomised control to isolate the two effects.

## Files Created

* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` (463 lines).
* `tasks/t0010_matched_mismatch_library/code/test_matched_mismatch.py` (310 lines).
* `tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/details.json`.
* `tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/description.md`.
* `tasks/t0010_matched_mismatch_library/research/research_papers.md`.
* `tasks/t0010_matched_mismatch_library/plan/plan.md`.
* `tasks/t0010_matched_mismatch_library/results/results_summary.md`.
* `tasks/t0010_matched_mismatch_library/results/results_detailed.md` (this file).
* `tasks/t0010_matched_mismatch_library/results/metrics.json`.
* `tasks/t0010_matched_mismatch_library/results/costs.json`.
* `tasks/t0010_matched_mismatch_library/results/remote_machines_used.json`.
* `tasks/t0010_matched_mismatch_library/results/suggestions.json` (produced by the suggestions
  step).
* All step logs under `tasks/t0010_matched_mismatch_library/logs/steps/NNN_*/step_log.md`.

## Task Requirement Coverage

The operative task request from `tasks/t0010_matched_mismatch_library/task.json`:

> **Name**: Matched-mismatch library: condition C with deliberately wrong granularity tags
>
> **Short description**: Write-library implementing condition C: wrap scope_unaware_planandsolve_v1
> with a tag-classifier that assigns deliberately incorrect granularity tags.

The resolved long description (from `task_description.md`) requires: a `MatchedMismatchAgent` that
accepts a problem statement, an annotation tree (the v2 hierarchy from t0009), a tool registry, a
model-call callable, and a `mismatch_strategy: "random" | "adversarial"`; walks the v2 hierarchy in
phase order; assigns an incorrect tag according to the strategy; delegates each step to either
`scope_aware_react_v1` (t0006) or `scope_unaware_planandsolve_v1` (t0007); emits trajectory records
carrying the wrong `granularity` tag with the correct tag logged separately as
`_correct_granularity` in extras; supports a deterministic-test mode; and provides pytest coverage
of random-strategy uniformity, adversarial-strategy correctness, schema parity with t0007, and
end-to-end runs with both delegate options. Expected outputs:
`assets/library/matched_mismatch_v1/{details.json, description.md, files/}` (note: the v2 library
asset spec drops `files/` — code lives in `code/`),
`tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` and tests, and
`results/results_summary.md` with API surface description and test summary.

| ID | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | `MatchedMismatchAgent` class accepts `problem`, `annotation`, `tool_registry`, `model_call`, `mismatch_strategy`, and a delegate selector | Done | `code/matched_mismatch.py` (`@dataclass(slots=True) class MatchedMismatchAgent` with keyword-only `run`); `test_records_carry_wrong_tag_with_correct_tag_in_extras` and end-to-end tests construct and call the class. |
| REQ-2 | Phase-ordered walk over v2 hierarchy (`global → for each subtask: (subtask, atomics) → global_atomics`) | Done | `iter_phases` in `code/matched_mismatch.py`; pinned by `test_phase_order` against an 8-phase fixture. |
| REQ-3 | `random` strategy picks uniformly from `{global, subtask, atomic} \ correct_tag` | Done | `pick_mismatch_tag(...strategy="random"...)` in `code/matched_mismatch.py`; `test_random_strategy_uniformity` runs 300 trials per correct tag and asserts ≥ 100 of each wrong tag and zero of the correct tag. |
| REQ-4 | `adversarial` strategy picks the most distant tag (`global → atomic`, `atomic → global`, `subtask → atomic`) | Done | `ADVERSARIAL_MAP` in `code/matched_mismatch.py`; `test_adversarial_strategy_correctness` checks all three correct-tag cases and `test_granularity_values_and_adversarial_map` pins the literal map. |
| REQ-5 | Schema parity with t0007's `TRAJECTORY_RECORD_FIELDS` | Done | Module-level `assert TRAJECTORY_RECORD_FIELDS == _TRAJECTORY_FIELDS_EXPECTED` in `code/matched_mismatch.py`; `test_trajectory_schema_parity_with_t0007` asserts the canonical six-tuple matches and that `MatchedMismatchRecord`'s first six dataclass fields match in order. |
| REQ-6 | Trajectory records carry the *wrong* tag in `granularity` and the correct tag in `extras["_correct_granularity"]` | Done | `MatchedMismatchRecord` dataclass and the `extras` payload assembled in `MatchedMismatchAgent.run`; `test_records_carry_wrong_tag_with_correct_tag_in_extras` and the two end-to-end tests verify per-record. |
| REQ-7 | Wrapper delegates to either `scope_aware_react_v1` (t0006) or `scope_unaware_planandsolve_v1` (t0007); the wrapper only controls the granularity tag | Done | `_run_react_phase` / `_run_planandsolve_phase` dispatch via the chosen delegate's parser and prompt template; `test_end_to_end_with_react_delegate` and `test_end_to_end_with_planandsolve_delegate` run a full v2-fixture trajectory through each. |
| REQ-8 | Deterministic-test mode using t0007's `ScriptedModel` | Done | All 14 tests construct either `ReactScriptedModel` (t0006) or `PlanAndSolveScriptedModel` (t0007). The pytest suite runs in 0.04s with no API keys and no network. |
| REQ-9 | Library asset `assets/library/matched_mismatch_v1/{details.json, description.md}` per the v2 library spec | Done | `assets/library/matched_mismatch_v1/details.json` and `description.md` exist; the library asset verificator (`meta/asset_types/library/verificator.py`) reports `PASSED — no errors or warnings`. |
| REQ-10 | `global_atomics` handling — treat as `atomic` for the mismatch policy | Done | `iter_phases` yields `correct_tag="atomic"` for items from the `global_atomics` list; `test_global_atomics_treated_as_atomic` asserts this on a two-item global-atomic fixture. |

All ten REQ items are marked `Done`. No `Partial` or `Not done` items remain.
