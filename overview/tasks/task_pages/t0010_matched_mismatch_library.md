# ⏹ Matched-mismatch library: condition C with deliberately wrong granularity tags

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0010_matched_mismatch_library` |
| **Status** | ⏹ not_started |
| **Source suggestion** | `S-0007-01` |
| **Task types** | `write-library` |
| **Expected assets** | 1 library |
| **Task folder** | [`t0010_matched_mismatch_library/`](../../../tasks/t0010_matched_mismatch_library/) |

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
