---
spec_version: "2"
library_id: "scope_unaware_planandsolve_v1"
documented_by_task: "t0007_scope_unaware_planandsolve_library"
date_documented: "2026-04-29"
---
# Scope-Unaware Plan-and-Solve Agent (v1)

## Metadata

* **Name**: Scope-Unaware Plan-and-Solve Agent (v1)
* **Version**: 0.1.0
* **Task**: `t0007_scope_unaware_planandsolve_library`
* **Module**: `code/planandsolve.py`
* **Tests**: `code/test_planandsolve.py`
* **Dependencies**: none beyond the Python 3.12+ standard library
* **Reference paper**: Wang et al., "Plan-and-Solve Prompting", arXiv:2305.04091, ACL 2023
* **Reference implementation**: LangChain `langchain_experimental.plan_and_execute` (Apache-2.0)

## Overview

This library is the canonical scope-unaware (B) baseline agent for the project's A-vs-B-vs-C
comparison. It exposes a single class, `PlanAndSolveAgent`, that adapts the LangChain
Plan-and-Execute reference implementation of Wang et al.'s Plan-and-Solve (PS) prompting technique.
The agent (1) calls a planner LLM with the verbatim PS+ instruction to produce a free-form numbered
plan, (2) parses the plan with a regex over `^\s*\d+[\.\)]\s+(.+)$`, (3) calls an executor LLM once
per plan step, and (4) terminates when the executor emits `FINAL_ANSWER:` or the plan is exhausted
(or `max_steps` is reached).

The library deliberately mirrors the trajectory record schema produced by the project's scope-aware
(A) library, `scope_aware_react_v1`, so that a Phase 2 evaluation harness can swap between A and B
by changing only the import line. The `granularity` field of every trajectory record produced by
this library is the literal string `"unspecified"` because the model is never asked to label its own
steps with explicit granularity tags.

The deterministic-test mode is a `ScriptedModel` callable that returns pre-recorded responses from a
list. This eliminates LLM cost during testing and is sufficient for the entire 14-test pytest suite
that ships with the library.

## API Reference

### `class PlanAndSolveAgent`

```python
PlanAndSolveAgent(
    model_call: Callable[[str], str],
    tool_registry: dict[str, Callable[[str], str]],
    max_steps: int = 32,
    granularity_label: str = "unspecified",
)
```

The main entry point. `model_call` is invoked once for the planner prompt and once per plan step for
the executor prompt. `tool_registry` maps tool name to a callable taking an argument string and
returning an observation string; it may be empty.

```python
PlanAndSolveAgent.run(problem: str) -> AgentResult
```

Drive one full plan-then-execute loop. Raises `MalformedPlanError` if the planner returned no
numbered steps.

### `class AgentResult`

A frozen dataclass with three fields:

* `final_answer: str | None` — the executor's `FINAL_ANSWER:` payload, or `None` if the loop
  exhausted the plan without a final answer.
* `trajectory: list[TrajectoryRecord]` — one record per executor turn, in order.
* `plan: list[str]` — the parsed plan steps.

### `class TrajectoryRecord`

A frozen, slotted dataclass whose field tuple is exposed at module level as
`TRAJECTORY_RECORD_FIELDS`. The schema (see `## Trajectory Schema` below) is the canonical schema
for both this library and t0006's `scope_aware_react_v1`.

### `class ScriptedModel`

```python
ScriptedModel(responses: list[str])
```

Deterministic-test fake. Calling it advances a cursor through the response list; raises `IndexError`
once exhausted. Compatible with `PlanAndSolveAgent`'s `model_call` parameter.

### `function parse_plan`

```python
parse_plan(text: str) -> list[str]
```

Parse free-form numbered plan text into an ordered list of step strings. Lines that do not match the
numbered-prefix regex are concatenated to the previous step. Raises `MalformedPlanError` on zero
matches.

### `class MalformedPlanError`

Raised when the planner output yields zero numbered steps. Subclasses `ValueError` so callers can
catch with `except ValueError` if they prefer.

### Module-level constants

* `PS_PLUS_INSTRUCTION` — verbatim PS+ instruction string from Wang et al. (2023).
* `PLAN_PROMPT_TEMPLATE` — full planner prompt with a `{problem}` placeholder.
* `EXECUTE_PROMPT_TEMPLATE` — executor prompt with placeholders for problem, plan, completed log,
  step number, total steps, step text, and tool list.
* `GRANULARITY_UNSPECIFIED` — the string `"unspecified"`, used as the default `granularity_label`.
* `TRAJECTORY_RECORD_FIELDS` — canonical ordered tuple of trajectory record field names.

## Usage Examples

The simplest end-to-end usage with deterministic-test mode:

```python
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    PlanAndSolveAgent,
    ScriptedModel,
)


def add_tool(args: str) -> str:
    a, b = args.split(",")
    return str(int(a) + int(b))


agent = PlanAndSolveAgent(
    model_call=ScriptedModel(
        responses=[
            "1. Add the two numbers.\n2. Report the result.",
            "Action: add | Args: 2,3",
            "FINAL_ANSWER: 5",
        ]
    ),
    tool_registry={"add": add_tool},
)

result = agent.run(problem="What is 2 + 3?")
print(result.final_answer)        # "5"
print(len(result.trajectory))     # 2
print(result.trajectory[0].granularity)  # "unspecified"
```

To use a real LLM, replace `ScriptedModel(...)` with any callable taking a prompt string and
returning a response string (e.g., a wrapper around the OpenAI Chat Completions API).

## Dependencies

No external dependencies. The library uses only the Python 3.12+ standard library (`dataclasses`,
`re`, `collections.abc`).

## Testing

Run the test suite with:

```bash
uv run pytest tasks/t0007_scope_unaware_planandsolve_library/code/
```

There are 14 test cases covering: trajectory record field tuple parity, plan parsing (simple,
continuation, paren separator, malformed), `ScriptedModel` round-trip, sequential execution with a
real tool, granularity label assertion, finish detection on `FINAL_ANSWER:`, schema parity
documentation, `THOUGHT_ONLY:` step recording, unknown-tool error recovery, `max_steps` halting, and
`MalformedPlanError` propagation through `run()`.

All tests use `ScriptedModel` so the suite runs without any API keys and without network access.

## Main Ideas

* The scope-unaware (B) condition is operationalized by setting `granularity_label = "unspecified"`
  on every trajectory record. There is no other implicit granularity bookkeeping in this library —
  A-vs-B is a one-line difference for the evaluation harness.

* The trajectory schema (`{turn_index, granularity, thought, action, observation, confidence}`) is
  shared with t0006's `scope_aware_react_v1`. `TRAJECTORY_RECORD_FIELDS` is exported so t0006 can
  `assert tuple(t0006_record.__dataclass_fields__.keys()) == TRAJECTORY_RECORD_FIELDS` at test time.

* Plan parsing is deliberately permissive: numbered prefixes `1.` and `1)` both work, leading
  whitespace is tolerated, and continuation lines are merged into the previous step. This matches
  the LangChain Plan-and-Execute reference implementation and is robust to minor formatting drift in
  real model output.

* Executor output is parsed for one of three forms — `Action:`, `FINAL_ANSWER:`, or `THOUGHT_ONLY:`
  — taking the first match. Unrecognized lines are accumulated as the `thought` field of the
  trajectory record, so no model output is silently lost.

* Errors are surfaced as observation strings rather than raised exceptions. An unknown tool name
  produces `observation = "ERROR: tool '...' not found in registry; available: ..."` so the
  trajectory captures the failure mode and the agent continues to the next plan step.

## Trajectory Schema

This is the canonical trajectory record schema for both condition B (this library) and condition A
(t0006's `scope_aware_react_v1`). Sister task t0006 must conform when its branch reaches
implementation.

| Field | Type | Description |
| --- | --- | --- |
| `turn_index` | `int` | Zero-based index of the executor turn within one trajectory. |
| `granularity` | `str` | Granularity tag for the step. `"unspecified"` for B; one of `"global"`, `"subtask"`, `"atomic"` for A. |
| `thought` | `str` | The free-form thought text the model emitted for this turn (anything before the structured `Action:`/`FINAL_ANSWER:`/`THOUGHT_ONLY:` line). |
| `action` | `str` | The action taken: either `"finish"`, `"thought_only"`, or `"<tool_name>(<args>)"`. |
| `observation` | `str` | The tool's return value, or the executor's `FINAL_ANSWER:` payload, or the error message if the tool failed. Empty string for `thought_only`. |
| `confidence` | `float \| None` | Optional self-reported confidence in `[0.0, 1.0]`. `None` when not available — never `0.0` for missing values. |

Example serialized record:

```json
{
  "turn_index": 0,
  "granularity": "unspecified",
  "thought": "I should call the calculator tool for this step.",
  "action": "add(2,3)",
  "observation": "5",
  "confidence": null
}
```

The Python tuple `TRAJECTORY_RECORD_FIELDS` exposes the field order so importers can assert parity:

```python
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    TRAJECTORY_RECORD_FIELDS,
)

assert TRAJECTORY_RECORD_FIELDS == (
    "turn_index", "granularity", "thought", "action", "observation", "confidence",
)
```

## License & Attribution

The algorithmic structure of this library — planner LLM, free-form numbered plan, sequential
executor LLM, finish-token detection — is adapted from the LangChain
`langchain_experimental.plan_and_execute` module, which is licensed under the **Apache License,
Version 2.0**. See <https://github.com/langchain-ai/langchain/blob/master/LICENSE> for the full
license text.

The PS+ instruction string is quoted verbatim from Wang, Lei et al., "Plan-and-Solve Prompting:
Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models," ACL 2023 (arXiv preprint
arXiv:2305.04091). The paper itself does not include a code license; only the instruction text is
reproduced.

The original code in this library — `parse_plan`, `_parse_executor_output`, the dataclass schemas,
the `ScriptedModel` deterministic-test mode, and the executor prompt template — is released under
the project's repository license. No LangChain code is copied verbatim; only the algorithmic
structure is reused.

## Summary

This library provides a deterministic, fully-testable Python implementation of the scope-unaware (B)
Plan-and-Solve baseline for the project's A-vs-B-vs-C comparison. It exposes a single top-level
class, `PlanAndSolveAgent`, that drives a planner-then-executor loop using a swappable `model_call`
callable. The trajectory record schema is identical to the schema produced by sister task t0006's
scope-aware library, so a Phase 2 evaluation harness can switch between A and B by changing one
import line.

Within the project, this library is the foundation for the Phase 2 B-condition evaluation. It will
also serve as the structural template for the planned matched-mismatch (C) library, which adds a
tag-classifier on top of the same plan-then-execute structure.

Limitations and known gaps: the executor prompt assumes a flat tool registry rather than a
hierarchical one; tool errors are surfaced as observation strings rather than raised exceptions
(this is by design but means callers must inspect observation strings to detect failures); the PS+
prompt template is a single string constant — task-specific prompt customization requires
subclassing or replacing the constant before instantiation; and the schema field set is fixed —
adding new fields (e.g., per-step latency) requires a coordinated change with t0006's
`scope_aware_react_v1` library.
