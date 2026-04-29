# ⏹ Scope-unaware Plan-and-Solve library: condition B baseline

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0007_scope_unaware_planandsolve_library` |
| **Status** | ⏹ not_started |
| **Source suggestion** | `S-0002-06` |
| **Task types** | `write-library` |
| **Expected assets** | 1 library |
| **Task folder** | [`t0007_scope_unaware_planandsolve_library/`](../../../tasks/t0007_scope_unaware_planandsolve_library/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/task_description.md)*

# Scope-Unaware Plan-and-Solve Library (Condition B)

## Motivation

The literature survey in t0002 identified Plan-and-Solve (Wang2023) as the strongest published
prompt-only baseline that does not condition on explicit granularity tags. It is therefore the
canonical scope-unaware (B) baseline for the project's A-vs-B-vs-C comparison. This task
produces the matching library asset, sharing the trajectory-log schema with t0006 so a Phase 2
experiment can run both libraries against the same harness without bespoke glue. Implements
suggestion S-0002-06.

## Scope

* Implement a library asset under `assets/library/scope_unaware_planandsolve_v1/` exposing a
  `PlanAndSolveAgent` class that:
  * Accepts a problem statement, a tool registry, and a model-call callable.
  * Generates a free-form numbered plan, then executes each step sequentially through a
    Plan-and-Execute loop.
  * Emits trajectory records in the same schema as `scope_aware_react_v1` so both libraries
    are drop-in interchangeable. The `granularity` field in the schema is filled with the
    literal string `"unspecified"` to mark the B condition.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}`.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Adapt LangChain's `Plan-and-Execute` reference implementation rather than re-implementing
  from scratch. License is Apache 2.0; record attribution in `description.md`.
* Provide pytest coverage at
  `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` covering: plan
  parsing, sequential execution, trajectory schema parity with t0006, finish detection, and
  error recovery on malformed model output.

Out of scope: actual A-vs-B-vs-C experiment, benchmark-specific tool registries, remote
execution.

## Approach

1. Read t0002's Wang2023 paper summary and the LangChain Plan-and-Execute source to ground the
   prompt template and execution loop.
2. Implement the library in
   `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and re-export the
   public API from `assets/library/scope_unaware_planandsolve_v1/library/`.
3. Reuse the trajectory log schema defined in t0006 by reading t0006's library when it lands;
   if t0006 has not landed yet, define the schema here and document that t0006 must conform.
4. Write `details.json`, `description.md`, and `files/` for the asset.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_unaware_planandsolve_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for the matched mismatch (C) library.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. May reference t0006's library if it merges first; otherwise this task
  defines the trajectory schema and t0006 must conform.
* References Wang2023 paper asset (`10.48550_arXiv.2305.04091`) from t0002.

## Source Suggestion

S-0002-06 — "Implement Plan-and-Solve as the canonical scope-unaware (B) baseline."

## Key Questions

1. What plan format does Plan-and-Solve produce, and how should it be parsed
   deterministically?
2. How should the library mark the absence of a granularity tag in the trajectory record?
3. What is the minimal API surface that lets a Phase 2 harness swap between this and t0006's
   library by changing only one line?

</details>
