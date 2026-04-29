---
spec_version: "2"
library_id: "scope_aware_react_v1"
documented_by_task: "t0006_scope_aware_react_library"
date_documented: "2026-04-29"
---
# Scope-Aware ReAct Agent

## Metadata

* **Name**: Scope-Aware ReAct Agent
* **Version**: 0.1.0
* **Task**: `t0006_scope_aware_react_library`
* **Dependencies**: standard library only
* **Modules**: `code/scope_aware_react.py`, `code/constants.py`, `code/paths.py`
* **Tests**: `code/test_scope_aware_react.py` (8 deterministic unit tests)

## Overview

This library implements the *scope-aware (A) condition* of the granularity-conditioning project. It
extends the canonical ReAct prompting paradigm ([Yao2022]) with an explicit per-turn granularity tag
drawn from the literal set `{global, subtask, atomic}`. Every Thought emission is prefixed with the
active tag; the agent loops Thought / Action / Observation turns by calling an injected `model_call`
callable; and every turn writes a structured record to a JSONL trajectory file.

The library is the substrate for every Phase 2 A-condition experiment in this project. It is
intentionally framework-free (no LangChain, no LiteLLM): callers wire in their own `model_call` and
`tool_registry`. For deterministic unit tests, the library ships a `ScriptedModel` helper that
replays a list of pre-recorded model completions without making any live API call.

The trajectory schema is the load-bearing contract between this library and the sister
Plan-and-Solve library (`t0007_scope_unaware_planandsolve_library`). Both libraries emit JSONL
records with the same six fields so the Phase 2 evaluator can ingest A-condition and B-condition
trajectories with one parser. The schema is documented in the dedicated `Trajectory Log Schema`
subsection below.

## API Reference

All public symbols live in `tasks.t0006_scope_aware_react_library.code.scope_aware_react`.
Field-name and granularity constants live in `tasks.t0006_scope_aware_react_library.code.constants`.

### `class ScopeAwareReactAgent`

```python
ScopeAwareReactAgent(
    *,
    problem: str,
    granularity: Granularity,           # Literal["global", "subtask", "atomic"]
    tool_registry: ToolRegistry,        # Mapping[str, Callable[..., Any]]
    model_call: ModelCall,              # Callable[[str], str]
    trajectory_path: Path,
    max_turns: int = 20,
    default_granularity_on_missing_tag: Granularity = "atomic",
)
```

Construct an agent bound to one problem and one fixed granularity. `tool_registry` is a mapping from
tool name to a Python callable that accepts keyword arguments and returns any value (the return
value is `str()`-ified into the trajectory `observation` field). `model_call` is a unary callable
that takes the assembled prompt and returns the model's raw text completion. `trajectory_path` is
created (with parent directories) and opened for writing the JSONL log.

`run() -> AgentResult` runs the Thought / Action / Observation loop until either the model emits a
`Finish` action or `max_turns` is reached. It returns an `AgentResult`.

`last_prompt -> str | None` (read-only property) returns the most recent prompt sent to the model.
Useful for tests and for debugging prompt drift.

`trajectory_path -> Path` (read-only property) returns the path the trajectory was written to.

### `class ScriptedModel`

```python
ScriptedModel(*, script: list[str])
```

Deterministic test helper. Each call returns the next entry from `script`; an exhausted script
raises `IndexError` with a clear message. Exposes `calls_made: int` and `reset() -> None` for
multi-run tests. Intended for unit tests only; production code should pass a real model wrapper.

### `class TrajectoryRecord`

```python
@dataclass(frozen=True, slots=True)
class TrajectoryRecord:
    turn_index: int
    granularity: str          # "global" | "subtask" | "atomic"
    thought: str
    action: dict[str, Any]    # {"name": str, "args": dict[str, Any]}
    observation: str
    confidence: float | None  # in [0.0, 1.0]; None when omitted by the model
```

The canonical record. The agent constructs and yields one of these per turn into the trajectory log.

### `class Action`

```python
@dataclass(frozen=True, slots=True)
class Action:
    name: str
    args: dict[str, Any]
```

A parsed Action. `name == "Finish"` terminates the loop; the answer is read from `args["answer"]`.
Any other `name` is dispatched through `tool_registry`.

### `class AgentResult`

```python
@dataclass(frozen=True, slots=True)
class AgentResult:
    answer: str | None        # the Finish payload; None if max_turns hit before Finish
    finished: bool            # True iff the agent emitted Finish
    turns: int                # number of records written to the trajectory log
    trajectory: list[TrajectoryRecord]
```

Returned by `ScopeAwareReactAgent.run()`. `finished == False` together with `answer is None` means
the agent hit `max_turns` without ever seeing a `Finish` action.

### `class MalformedActionError`

Subclass of `ValueError`. Raised internally by the parser when the model emits a non-JSON `Action:`
line or an Action JSON missing the `name` field. The agent loop catches this and surfaces it in the
trajectory as `observation = "<parse_error>:<message>"`; the run continues. Exported in case
downstream code wants to construct or assert on the same exception type.

### Trajectory Log Schema

The trajectory file is line-delimited JSON (JSONL). One record is written per Thought / Action /
Observation turn. The six fields are constants in `constants.py` (re-keyed to ensure identical
ordering across this library and t0007):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_index` | int (>=0) | Zero-based turn number. Strictly increasing within one run. |
| `granularity` | str | One of `"global"`, `"subtask"`, `"atomic"`. The active scope for this turn. |
| `thought` | str | Free-form Thought emitted by the model, with the granularity tag stripped. |
| `action` | dict | `{"name": str, "args": dict[str, Any]}`. `name == "Finish"` terminates. |
| `observation` | str | Tool output (or marker: `<parse_error>`, `<unknown_tool>`, `<tag_missing_defaulted_to_atomic>:...`). |
| `confidence` | float \| null | Verbalized confidence in `[0.0, 1.0]` (model emits 0-100; library divides by 100). |

Sister-task contract: `t0007_scope_unaware_planandsolve_library` emits records of this exact shape.
The B-condition wrapper sets `granularity` to `"subtask"` for every record (the natural
Plan-and-Solve default) and otherwise mirrors the schema field-for-field. If t0007 lands first, this
library adopts whatever schema it ships; if t0006 lands first (this PR), t0007 mirrors the schema
documented above.

## Usage Examples

### Minimal: scripted Finish

```python
from pathlib import Path

from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    ScopeAwareReactAgent,
    ScriptedModel,
)

agent = ScopeAwareReactAgent(
    problem="Return the answer 'ok'.",
    granularity="atomic",
    tool_registry={},
    model_call=ScriptedModel(
        script=[
            'Thought: <atomic> Nothing to do.\n'
            'Action: {"name": "Finish", "args": {"answer": "ok"}}\n'
            'Confidence: 90'
        ]
    ),
    trajectory_path=Path("/tmp/example_trajectory.jsonl"),
)
result = agent.run()
assert result.finished is True
assert result.answer == "ok"
```

### Realistic: tool dispatch then Finish

```python
from pathlib import Path

from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    ScopeAwareReactAgent,
    ScriptedModel,
)

def lookup_capital(*, country: str) -> str:
    return {"France": "Paris", "Japan": "Tokyo"}.get(country, "unknown")

scripted_outputs = [
    'Thought: <subtask> Look up the capital of France.\n'
    'Action: {"name": "lookup_capital", "args": {"country": "France"}}\n'
    'Confidence: 70',
    'Thought: <subtask> The capital is Paris.\n'
    'Action: {"name": "Finish", "args": {"answer": "Paris"}}\n'
    'Confidence: 95',
]

agent = ScopeAwareReactAgent(
    problem="What is the capital of France?",
    granularity="subtask",
    tool_registry={"lookup_capital": lookup_capital},
    model_call=ScriptedModel(script=scripted_outputs),
    trajectory_path=Path("/tmp/capital_trajectory.jsonl"),
    max_turns=5,
)
result = agent.run()
assert result.finished is True
assert result.answer == "Paris"
assert result.turns == 2
# Inspect the JSONL file:
import json
records = [json.loads(line) for line in Path("/tmp/capital_trajectory.jsonl").read_text().splitlines()]
assert records[0]["action"] == {"name": "lookup_capital", "args": {"country": "France"}}
assert records[0]["observation"] == "Paris"
```

In production, replace `ScriptedModel` with a callable that wraps your real LLM client (OpenAI,
Anthropic, local-server, etc.) — any function with signature `(prompt: str) -> str` works.

## Dependencies

The library uses only the Python standard library (`json`, `pathlib`, `dataclasses`,
`collections.abc`, `typing`). There are no third-party runtime dependencies. Tests require `pytest`,
which is already in the project's dev dependencies.

**Attribution**: The agent's prompt template is adapted from the
[LangChain project](https://github.com/langchain-ai/langchain), licensed under the Apache License
2.0. The verbatim attribution string lives in `constants.py` as `LANGCHAIN_REACT_ATTRIBUTION` and is
included in every system prompt the agent emits, so downstream consumers automatically satisfy the
Apache-2.0 NOTICE requirement.

## Testing

Run the library's tests from the repo root:

```bash
uv run pytest tasks/t0006_scope_aware_react_library/code/ -v
```

The test file `code/test_scope_aware_react.py` contains 8 deterministic unit tests that exercise:

* `test_tag_injection_in_prompt` — system prompt mentions the active granularity literal.
* `test_action_parsing_round_trip` — action JSON is parsed and dispatched to the right tool.
* `test_finish_terminates_loop` — Finish stops the loop with leftover script entries unconsumed.
* `test_malformed_action_recovery` — invalid Action JSON yields `<parse_error>` and the loop
  continues.
* `test_trajectory_log_schema` — every JSONL record contains the six canonical fields.
* `test_missing_tag_defaults_to_atomic` — when the tag is missing the agent falls back to `"atomic"`
  and emits `<tag_missing_defaulted_to_atomic>` as the observation prefix.
* `test_max_turns_safety_cap` — the agent stops at `max_turns` even without a Finish action.
* `test_unknown_tool_is_observed_not_raised` — unknown tool name yields `<unknown_tool>` instead of
  raising.

All tests pass deterministically; no live API call is made by any test.

## Main Ideas

* **Granularity is a single token, not a structural change**: the Thought template prepends
  `<global>` / `<subtask>` / `<atomic>` to the model's reasoning, and the trajectory log records the
  active tag per turn. The rest of the ReAct loop is unchanged.
* **The trajectory schema is a contract, not a convention**: the six fields
  (`turn_index, granularity, thought, action, observation, confidence`) are fixed and frozen. t0007
  mirrors them exactly so the Phase 2 evaluator can ingest both conditions with one parser.
* **Determinism is wired in via `ScriptedModel`**: every test uses pre-recorded model outputs. No
  live LLM call ever runs in CI.
* **Failure paths surface in observations**: malformed Action JSON, unknown tools, and missing
  granularity tags each produce a structured observation marker so downstream evaluators can detect
  them without parsing free-form error text.
* **No third-party runtime dependency**: the library is intentionally light. The LangChain prompt is
  reused via a verbatim attribution string, not by importing the framework.

## Summary

This library implements the scope-aware (A) condition of the granularity-conditioning project as a
thin, framework-free extension of the canonical ReAct prompting loop. It introduces a single new
conceptual element — an explicit per-turn granularity tag — and bakes it into both the prompt and
the trajectory log. The agent runs Thought / Action / Observation turns until a `Finish` action
terminates the loop, writing one JSONL record per turn with six canonical fields.

The library is the substrate for every Phase 2 A-condition experiment in this project. It pairs with
the sister Plan-and-Solve library (`t0007_scope_unaware_planandsolve_library`) which emits the same
schema for the matched B baseline. Together the two libraries let the Phase 2 evaluator compare A
and B trajectories with one parser and one set of metrics. Benchmark-specific tool registries are
explicitly out of scope for this task and are deferred to a follow-up library task — callers supply
any tool registry that maps `name` to `Callable`.

Limitations and future work: the library is synchronous and single-threaded; the parser is tolerant
but assumes English-language Thought / Action prefixes; confidence is currently a single scalar per
turn (no per-claim breakdown); and the agent supports a fixed granularity for all turns (the
experiment that varies granularity within a run is left for Phase 2). Each of these gaps is captured
in `results/suggestions.json`.
