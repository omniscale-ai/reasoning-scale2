# ⏹ Scope-aware ReAct library: condition A with explicit granularity tags

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0006_scope_aware_react_library` |
| **Status** | ⏹ not_started |
| **Source suggestion** | `S-0002-07` |
| **Task types** | `write-library` |
| **Expected assets** | 1 library |
| **Task folder** | [`t0006_scope_aware_react_library/`](../../../tasks/t0006_scope_aware_react_library/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0006_scope_aware_react_library/task_description.md)*

# Scope-Aware ReAct Library (Condition A)

## Motivation

The project's main hypothesis is that explicit granularity conditioning improves agent
performance. The literature survey in t0002 identified ReAct (Yao2022) as the canonical
foundation for the scope-aware (A) condition. This task produces a self-contained library that
extends ReAct with a `{global, subtask, atomic}` granularity tag emitted at every Thought /
Action turn, plus a logging hook that records the active tag alongside the model's confidence.
The library is the substrate every Phase 2 A-condition experiment will import. Implements
suggestion S-0002-07.

## Scope

* Implement a library asset under `assets/library/scope_aware_react_v1/` exposing a
  `ScopeAwareReactAgent` class that:
  * Accepts a problem statement, a fixed `granularity` argument (`"global" | "subtask" |
    "atomic"`), a tool registry, and a model-call callable.
  * Loops Thought / Action / Observation steps, prepending the active granularity tag to every
    Thought emission, and parses Action JSON until the agent emits a `Finish` action.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}` to
    a JSONL trajectory file the experiment harness can replay.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0006_scope_aware_react_library/code/test_scope_aware_react.py` covering: tag
  injection, action parsing, finish detection, error recovery on malformed JSON, and
  trajectory logging integrity.

Out of scope: the actual A-vs-B-vs-C experiment (a separate experiment-run task), benchmark-
specific tool registries (also a separate task), and any remote-execution wiring.

## Approach

1. Read t0002's `research/research_papers.md` and the Yao2022 paper summary to ground the
   prompt format. Reuse LangChain's ReAct prompt where appropriate; the project licence is
   Apache 2.0.
2. Implement the library in `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`
   and re-export the public API from a `library/__init__.py` shim under `assets/library/
   scope_aware_react_v1/`.
3. Write the asset's `details.json`, `description.md`, and `files/` directory with the
   runnable source.
4. Write tests as deterministic unit tests; no live API calls.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_aware_react_v1/` with `details.json`, `description.md`, and `files/`.
* `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` and matching test file.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for benchmark-specific tool registries.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Yao2022 paper asset (`10.48550_arXiv.2210.03629`) from t0002.
* Sister task `t0007_scope_unaware_planandsolve_library` produces the matched B baseline; both
  must follow the same trajectory-logging schema so a Phase 2 experiment can consume both.

## Source Suggestion

S-0002-07 — "Implement scope-aware (A) as ReAct extended with explicit granularity tags."

## Key Questions

1. What is the minimal extension to ReAct's prompt template that reliably elicits a
   granularity tag on every Thought emission?
2. How should the library handle a model that refuses to emit a tag (back off, abort, or
   default to `atomic`)?
3. What schema for the trajectory log lets t0007 emit identical-shape records?

</details>
