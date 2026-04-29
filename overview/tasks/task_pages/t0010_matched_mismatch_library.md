# ✅ Matched-mismatch library: condition C with deliberately wrong granularity tags

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0010_matched_mismatch_library` |
| **Status** | ✅ completed |
| **Started** | 2026-04-29T23:25:02Z |
| **Completed** | 2026-04-29T23:46:00Z |
| **Duration** | 20m |
| **Source suggestion** | `S-0007-01` |
| **Task types** | `write-library` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`granularity-conditioning`](../../by-category/granularity-conditioning.md), [`hierarchical-planning`](../../by-category/hierarchical-planning.md) |
| **Expected assets** | 1 library |
| **Step progress** | 9/15 |
| **Task folder** | [`t0010_matched_mismatch_library/`](../../../tasks/t0010_matched_mismatch_library/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0010_matched_mismatch_library/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0010_matched_mismatch_library/task_description.md)*

# Matched-Mismatch Library (Condition C)

## Motivation

The project's main hypothesis includes sub-hypothesis 2: scope-mismatched agents perform
strictly worse than both scope-aware (A) and scope-unaware (B) baselines. Without a C library,
research question 5 cannot be tested. This task implements C by wrapping the existing
libraries (`scope_aware_react_v1` from t0006 or `scope_unaware_planandsolve_v1` from t0007)
with a granularity-tag layer that emits **deliberately incorrect** tags at each step. The
library shares the canonical `TRAJECTORY_RECORD_FIELDS` schema from t0007 so a Phase 2 harness
can run all three conditions interchangeably. Implements suggestion S-0007-01.

## Scope

* Implement a library asset under `assets/library/matched_mismatch_v1/` exposing a
  `MatchedMismatchAgent` class that:
  * Accepts a problem statement, an annotation tree (the v2 hierarchy from t0009), a tool
    registry, a model-call callable, and a `mismatch_strategy: "random" | "adversarial"`.
  * Walks the v2 hierarchy in phase order (the harness's canonical walk), determines the
    correct granularity at each step from the annotation, and **assigns an incorrect tag**
    according to the strategy:
    * `random`: pick uniformly from `{global, subtask, atomic} \ correct_tag`.
    * `adversarial`: always pick the most distant tag (`atomic` when correct is `global`,
      `global` when correct is `atomic`, `atomic` when correct is `subtask`).
  * Delegates each step to either `scope_aware_react_v1` or `scope_unaware_planandsolve_v1`
    (configurable). The delegate handles the actual model call; the wrapper only controls the
    granularity tag.
  * Emits trajectory records in the canonical `TRAJECTORY_RECORD_FIELDS` schema, with the
    `granularity` field carrying the *wrong* tag (the actual correct tag is logged separately
    as `_correct_granularity` in an extras blob).
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0010_matched_mismatch_library/code/test_matched_mismatch.py` covering:
  random-strategy uniformity over `{global, subtask, atomic} \ correct_tag`,
  adversarial-strategy correctness, schema parity with t0007, end-to-end run with both
  delegate options.

Out of scope: the actual A/B/C experiment (handled by t0012), benchmark-specific tool
registries, remote execution.

## Approach

1. Read t0007's `scope_unaware_planandsolve_v1` library and t0006's `scope_aware_react_v1`
   library. Confirm the canonical trajectory schema is `TRAJECTORY_RECORD_FIELDS` from t0007.
2. Implement the library in `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`.
   Re-export the public API from `assets/library/matched_mismatch_v1/library/`.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests are deterministic (no live API calls). Use `ScriptedModel` from t0007 as the
   delegate's model.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/matched_mismatch_v1/` with `details.json`, `description.md`, `files/`.
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion to make the random-strategy mismatch ablation (uniform random vs.
  adversarial vs. matched) explicit in t0012.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  library assets. Reads `TRAJECTORY_RECORD_FIELDS` from t0007.

## Source Suggestion

S-0007-01 — "Implement matched-mismatch (C) library on top of scope_unaware_planandsolve_v1."

## Key Questions

1. What is the cleanest way to handle a granularity tag for steps that fall under
   `global_atomics` (cross-cutting atomics with no parent subtask)? Default: treat as `atomic`
   for the purposes of the mismatch strategy.
2. Should the wrapper expose a way to override the mismatch policy per-step (e.g., to inject
   targeted mismatches in specific phases)? Default: no, keep the wrapper minimal.
3. How should the schema's `_correct_granularity` extras field be standardised so a downstream
   experiment can compute the mismatch contribution per step?

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Matched-Mismatch Agent (v1)](../../../tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/) | [`description.md`](../../../tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/description.md) |

## Suggestions Generated

<details>
<summary><strong>Add a uniform-random vs. adversarial vs. matched ablation to
t0012</strong> (S-0010-01)</summary>

**Kind**: experiment | **Priority**: high

When t0012 runs the A-vs-B-vs-C harness, include three C-condition variants in addition to A
and B: matched_mismatch_v1 with mismatch_strategy='random' and seed=0, matched_mismatch_v1
with mismatch_strategy='adversarial', and a phase-randomised C control (random walk over the
v2 hierarchy with the correct tag). The three-way ablation decomposes the C-condition gap into
'phase order matters', 'any wrong tag matters', and 'most-distant wrong tag matters',
preventing the granularity-mismatch effect from being conflated with a step-order-mismatch
effect (see research_papers.md, Wang2023 and Zhou2022).

</details>

<details>
<summary><strong>Per-step strategy override for matched_mismatch_v1</strong>
(S-0010-02)</summary>

**Kind**: library | **Priority**: medium

Extend matched_mismatch_v1 with a per-step strategy override so callers can inject targeted
mismatches in specific phases (e.g., wrong-tag only at the global level; correct everywhere
else). This decomposes the C-condition gap by phase kind and supports follow-up analysis on
which structural slots are most sensitive to tag mismatch. Should be additive: the existing
uniform-strategy API stays the default. Keep the trajectory schema unchanged; the override is
constructor-side only.

</details>

<details>
<summary><strong>Resolve the subtask-adversarial ambiguity with empirical
evidence</strong> (S-0010-03)</summary>

**Kind**: evaluation | **Priority**: low

ADVERSARIAL_MAP currently pins 'subtask -> atomic' because subtask is equidistant from global
and atomic. Run a small ablation in t0012 with both 'subtask -> atomic' and 'subtask ->
global' adversarial maps and report the per-step contribution. If the two choices differ
materially, document the chosen direction and the empirical justification in
matched_mismatch_v1's description.md. If they do not differ, lock the current choice and
remove the ambiguity note.

</details>

## Research

* [`research_papers.md`](../../../tasks/t0010_matched_mismatch_library/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0010_matched_mismatch_library/results/results_summary.md)*

# Results Summary: Matched-Mismatch Library (Condition C)

## Summary

Implemented the project's condition-C library `matched_mismatch_v1` — a wrapper that walks the
v2 hierarchy from t0009 in canonical phase order, substitutes a deliberately incorrect
granularity tag according to a `random` or `adversarial` strategy, and delegates the per-phase
model call to either the t0006 ReAct or t0007 Plan-and-Solve format. The library reuses
t0007's `TRAJECTORY_RECORD_FIELDS` schema unchanged and stores the correct tag in
`extras["_correct_granularity"]`. All 14 deterministic tests pass and every `REQ-*` checklist
item is satisfied.

## Metrics

* **Tests passed**: 14 of 14 (`uv run pytest tasks/t0010_matched_mismatch_library/code/ -v`).
* **Source lines (`matched_mismatch.py`)**: 463 lines including documentation and `__all__`
  export list.
* **Public API entry points**: 6 (`MatchedMismatchAgent`, `MatchedMismatchRecord`,
  `AgentRunResult`, `Phase`, `iter_phases`, `pick_mismatch_tag`).
* **Module-level constants exported**: 4 (`GRANULARITY_VALUES`, `ADVERSARIAL_MAP`,
  `CORRECT_GRANULARITY_EXTRAS_KEY`, re-exported `TRAJECTORY_RECORD_FIELDS`).
* **REQ checklist coverage**: 10 of 10 (REQ-1 through REQ-10) — see
  `results/results_detailed.md` § Task Requirement Coverage.
* **External cost**: $0 (deterministic local Python only; no API or remote compute).

## Verification

* `uv run ruff check tasks/t0010_matched_mismatch_library/code/` — PASSED (0 issues).
* `uv run ruff format tasks/t0010_matched_mismatch_library/code/` — PASSED (no changes
  required).
* `uv run mypy -p tasks.t0010_matched_mismatch_library.code` — PASSED (0 issues).
* `uv run pytest tasks/t0010_matched_mismatch_library/code/ -v` — 14 PASSED.
* `meta.asset_types.library.verificator --task-id t0010_matched_mismatch_library
  matched_mismatch_v1` — PASSED (0 errors, 0 warnings).
* `verify_research_papers t0010_matched_mismatch_library` — PASSED (0 errors, 0 warnings).
* `verify_plan t0010_matched_mismatch_library` — PASSED (0 errors, 0 warnings).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0010_matched_mismatch_library/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0010_matched_mismatch_library" ---
# Results Detailed: Matched-Mismatch Library (Condition C)

## Summary

Delivered the project's condition-C library, `matched_mismatch_v1`, as a write-library task
with zero external cost. The library exposes a `MatchedMismatchAgent` class that walks a v2
hierarchy from t0009 in canonical phase order, substitutes a deliberately incorrect
granularity tag at each step, and delegates per-phase model calls to either the t0006 ReAct or
t0007 Plan-and-Solve prompt format. The trajectory record schema (`TRAJECTORY_RECORD_FIELDS`)
from t0007 is reused unchanged; the correct tag is recorded under
`extras["_correct_granularity"]`. All 14 deterministic tests pass and the library asset
verificator reports zero errors and zero warnings.

## Methodology

* **Machine specs**: local development (Apple Darwin 25.3.0, Python 3.13.11). No remote
  compute.
* **Runtime**: implementation + tests + asset writing wall-clock < 10 minutes; pytest suite
  runs in 0.04s.
* **Timestamps**: implementation step started 2026-04-29T23:34:58Z; results step started
  2026-04-29T23:41:44Z.
* **Approach**: per-phase model call with delegate-specific prompt format and output parser.
  The wrapper drives the v2-walk loop itself rather than calling each delegate's outer
  `run()`, because each delegate's `run()` runs its own multi-turn loop that would conflict
  with the per-phase walk. The wrapper reuses each delegate's *parsing* logic
  (`_parse_model_output` from t0006, `_parse_executor_output` from t0007) so the prompt-format
  and output-parser axis is delegated correctly.
* **Test design**: deterministic via `ScriptedModel` from t0006 and t0007. Random-strategy
  uniformity is verified across N=300 trials per correct tag with a 100/300 lower-bound
  acceptance band (well within the fair-coin 3-sigma envelope).

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
  `TrajectoryWriter` writing a JSONL file). Consumers that need that side effect must invoke
  the delegates directly or open an issue against this library.
* The mismatch strategy is a single literal applied uniformly across all phases; per-step
  strategy overrides are not currently supported.
* `subtask` is equidistant from `global` and `atomic` in the adversarial map; the choice
  `subtask → atomic` is documented and pinned by tests but represents one of two reasonable
  interpretations of "most distant tag" for `subtask`.
* Phase-order vs. mismatched-tag confound (per the research synthesis) is not addressed by
  this library — t0012 must include a phase-randomised control to isolate the two effects.

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

The resolved long description (from `task_description.md`) requires: a `MatchedMismatchAgent`
that accepts a problem statement, an annotation tree (the v2 hierarchy from t0009), a tool
registry, a model-call callable, and a `mismatch_strategy: "random" | "adversarial"`; walks
the v2 hierarchy in phase order; assigns an incorrect tag according to the strategy; delegates
each step to either `scope_aware_react_v1` (t0006) or `scope_unaware_planandsolve_v1` (t0007);
emits trajectory records carrying the wrong `granularity` tag with the correct tag logged
separately as `_correct_granularity` in extras; supports a deterministic-test mode; and
provides pytest coverage of random-strategy uniformity, adversarial-strategy correctness,
schema parity with t0007, and end-to-end runs with both delegate options. Expected outputs:
`assets/library/matched_mismatch_v1/{details.json, description.md, files/}` (note: the v2
library asset spec drops `files/` — code lives in `code/`),
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

</details>
