---
spec_version: "2"
library_id: "matched_mismatch_v1"
documented_by_task: "t0010_matched_mismatch_library"
date_documented: "2026-04-29"
---
# Matched-Mismatch Agent (v1)

## Metadata

* **Name**: Matched-Mismatch Agent (v1)
* **Version**: 0.1.0
* **Task**: `t0010_matched_mismatch_library`
* **Module**: `code/matched_mismatch.py`
* **Tests**: `code/test_matched_mismatch.py`
* **Dependencies**: none beyond the Python 3.12+ standard library and the two sister libraries
  `tasks.t0006_scope_aware_react_library` and `tasks.t0007_scope_unaware_planandsolve_library`
* **Reference papers**: Yao et al., "ReAct" (arXiv:2210.03629); Wang et al., "Plan-and-Solve
  Prompting" (arXiv:2305.04091); Shinn et al., "Reflexion" (arXiv:2303.11366)

## Overview

This library implements **condition C** of the project's A-vs-B-vs-C scope-conditioning comparison.
Condition A (`scope_aware_react_v1`, t0006) emits the *correct* granularity tag at every step;
condition B (`scope_unaware_planandsolve_v1`, t0007) emits the literal `"unspecified"` tag at every
step; condition C — implemented here — emits a *deliberately incorrect* granularity tag at every
step, drawn from one of two strategies:

* `random`: pick uniformly from `{global, subtask, atomic} \ correct_tag`. This is the
  weak-perturbation control.
* `adversarial`: pick the most distant tag (`global → atomic`, `atomic → global`,
  `subtask → atomic`). This is the strong-perturbation probe, mirroring the mismatched-context
  ablation pattern from Reflexion (Shinn et al., 2023).

The wrapper walks a v2 hierarchy from t0009 in canonical phase order: `global` first, then for each
subtask the subtask itself followed by its atomics, then any cross-cutting `global_atomics` last.
Per phase it dispatches one model call via the chosen delegate's prompt format and output parser,
substitutes the wrong granularity tag, and emits one `MatchedMismatchRecord`. The first six fields
of the record are exactly `TRAJECTORY_RECORD_FIELDS` from t0007 — same names, same order, same types
— so a Phase 2 evaluation harness can read all three condition's trajectories through one schema.
The seventh field, `extras`, carries the correct tag under the well-known key `_correct_granularity`
for downstream evaluators that need to compute the per-step mismatch contribution.

The wrapper's design isolates the perturbation to the *logged* tag: the model itself still reasons
under the correct tag in its prompt, so observed metric drops in t0012 will reflect the log-side
mismatch effect rather than a confounded "what the model sees vs. what we record" axis.

## API Reference

### `class MatchedMismatchAgent`

```python
@dataclass(slots=True)
class MatchedMismatchAgent:
    model_call: Callable[[str], str]
    tool_registry: Mapping[str, Callable[..., Any]]
    delegate: Literal["scope_aware_react", "scope_unaware_planandsolve"]
    mismatch_strategy: Literal["random", "adversarial"]
    seed: int = 0

    def run(
        self,
        *,
        problem: str,
        annotation: Mapping[str, Any],
    ) -> AgentRunResult: ...
```

Drives one matched-mismatch run over a v2 annotation tree. `model_call` is called once per phase.
`tool_registry`'s callable signature must match the chosen delegate: t0006-style
`tool(**action.args)` for `delegate="scope_aware_react"`, t0007-style `tool(args_str)` for
`delegate="scope_unaware_planandsolve"`. `seed` makes `mismatch_strategy="random"` runs
deterministic. Raises `ValueError` if `mismatch_strategy` or `delegate` is not a documented literal.

### `class MatchedMismatchRecord`

```python
@dataclass(frozen=True, slots=True)
class MatchedMismatchRecord:
    turn_index: int
    granularity: str            # the WRONG tag
    thought: str
    action: str
    observation: str
    confidence: float | None
    extras: dict[str, str]      # carries _correct_granularity, phase_kind, delegate, mismatch_strategy
```

The first six fields are exactly `TRAJECTORY_RECORD_FIELDS`. `extras` is the seventh, appended
field; downstream consumers that read only the canonical six see a normal trajectory record.
`extras` carries:

* `_correct_granularity`: the granularity tag that *would* have been emitted by a matched- condition
  agent for this step (from `Phase.correct_tag`).
* `phase_kind`: which structural slot the step came from (`"global"`, `"subtask"`, `"atomic"`, or
  `"global_atomic"`).
* `delegate`: the delegate the wrapper used.
* `mismatch_strategy`: the strategy the wrapper used.

### `class AgentRunResult`

```python
@dataclass(frozen=True, slots=True)
class AgentRunResult:
    final_answer: str | None
    trajectory: list[MatchedMismatchRecord]
    phases: list[Phase]
```

`final_answer` is `None` if no phase emitted a final answer; `trajectory` lists one record per
executed phase; `phases` lists every phase yielded by `iter_phases` (so callers can compare intended
vs. executed walks).

### `class Phase`

```python
@dataclass(frozen=True, slots=True)
class Phase:
    kind: str             # "global" | "subtask" | "atomic" | "global_atomic"
    correct_tag: str      # "global" | "subtask" | "atomic"
    payload: str          # the textual content drawn from the annotation
```

### `function iter_phases`

```python
def iter_phases(annotation: Mapping[str, Any]) -> Iterator[Phase]: ...
```

Walks the v2 hierarchy in canonical phase order. Accepts either the full v2 annotation row (with a
top-level `hierarchy` key) or the inner `hierarchy` mapping directly. Missing optional slots (empty
subtasks, missing global_atomics) are skipped silently.

### `function pick_mismatch_tag`

```python
def pick_mismatch_tag(
    correct_tag: str,
    *,
    strategy: Literal["random", "adversarial"],
    rng: random.Random,
) -> str: ...
```

Returns a granularity tag guaranteed to differ from `correct_tag`. Raises `ValueError` if
`correct_tag` is not in `GRANULARITY_VALUES`.

### Module-level constants

* `GRANULARITY_VALUES = ("global", "subtask", "atomic")` — canonical ordered tuple.
* `ADVERSARIAL_MAP = {"global": "atomic", "atomic": "global", "subtask": "atomic"}` — the
  most-distant-tag map. `subtask` is equidistant from `global` and `atomic`; we pick `atomic`
  consistently with the planning literature where the global-vs-atomic axis is the primary variable.
* `CORRECT_GRANULARITY_EXTRAS_KEY = "_correct_granularity"` — well-known key in
  `MatchedMismatchRecord.extras` carrying the correct tag.
* `TRAJECTORY_RECORD_FIELDS` — re-exported from t0007 for parity assertions.

### Adversarial Mapping Table

| Correct tag | Adversarial tag |
| --- | --- |
| `global` | `atomic` |
| `atomic` | `global` |
| `subtask` | `atomic` |

### `global_atomics` Handling

`Phase` objects emitted from items in the annotation's `global_atomics` list carry
`kind="global_atomic"` but `correct_tag="atomic"` — cross-cutting atomics are still atomic for the
mismatch policy. This decision is documented here and pinned by
`test_global_atomics_treated_as_atomic` so a future change is detected immediately.

## Usage Examples

End-to-end example using the t0007 Plan-and-Solve delegate and a deterministic
`PlanAndSolveScriptedModel`:

```python
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    ScriptedModel as PlanAndSolveScriptedModel,
)
from tasks.t0010_matched_mismatch_library.code.matched_mismatch import (
    ADVERSARIAL_MAP,
    CORRECT_GRANULARITY_EXTRAS_KEY,
    MatchedMismatchAgent,
)


annotation = {
    "task_id": "fixture-001",
    "benchmark": "synthetic",
    "hierarchy": {
        "global": "Solve the toy arithmetic problem.",
        "subtasks": [
            {
                "subtask": "Identify operands.",
                "atomics": ["Read first number.", "Read second number."],
            },
            {
                "subtask": "Compute the result.",
                "atomics": ["Add operands.", "Format the answer."],
            },
        ],
        "global_atomics": ["Sanity check magnitude."],
    },
}


def add_tool(args: str) -> str:
    a, b = args.split(",")
    return str(int(a) + int(b))


# Eight phases in `annotation`; the eighth emits the FINAL_ANSWER.
script = ["Action: add | Args: 1,1\n"] * 7 + ["FINAL_ANSWER: 2\n"]

agent = MatchedMismatchAgent(
    model_call=PlanAndSolveScriptedModel(responses=script),
    tool_registry={"add": add_tool},
    delegate="scope_unaware_planandsolve",
    mismatch_strategy="adversarial",
    seed=0,
)
result = agent.run(problem="What is 1 + 1?", annotation=annotation)
print(result.final_answer)                              # "2"
print(len(result.trajectory))                           # 8
for record in result.trajectory:
    correct = record.extras[CORRECT_GRANULARITY_EXTRAS_KEY]
    assert record.granularity == ADVERSARIAL_MAP[correct]
```

To use a real LLM, replace `PlanAndSolveScriptedModel(...)` with any callable taking a prompt string
and returning a response string. To switch delegates to the ReAct prompt/parser, pass
`delegate="scope_aware_react"` and supply a `tool_registry` whose callables accept keyword arguments
(`tool(**action.args)`).

## Dependencies

No external dependencies beyond:

* The Python 3.12+ standard library (`dataclasses`, `random`, `collections.abc`, `typing`).
* `tasks.t0006_scope_aware_react_library.code.scope_aware_react` — for the ReAct output parser and
  the `Action` dataclass.
* `tasks.t0006_scope_aware_react_library.code.constants` — for `GRANULARITY_GLOBAL`,
  `GRANULARITY_SUBTASK`, `GRANULARITY_ATOMIC`.
* `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve` — for
  `TRAJECTORY_RECORD_FIELDS`, the executor output parser, and the `EXECUTE_PROMPT_TEMPLATE` /
  `PLAN_PROMPT_TEMPLATE` strings.

These project-internal imports are stable: the libraries pin their public symbols and the
matched-mismatch module asserts schema parity at import time, so any drift in either delegate's
canonical schema raises `AssertionError` immediately.

## Testing

Run the test suite with:

```bash
uv run pytest tasks/t0010_matched_mismatch_library/code/ -v
```

There are 14 deterministic tests covering: granularity constants and the adversarial map, trajectory
schema parity with t0007, canonical phase order over a v2 fixture, `global_atomics → atomic`
handling, hierarchy-key vs. inner-mapping equivalence, random-strategy uniformity over 300 trials
per correct tag, adversarial-strategy correctness, input validation on `pick_mismatch_tag`,
extras-blob round-trip, end-to-end run with each of the two delegates, defensive validation on
unknown `mismatch_strategy` / `delegate`, and seed determinism.

All tests use the deterministic `ScriptedModel` helpers from t0006 and t0007 so the suite runs
without API keys and without network access.

## Main Ideas

* The wrapper perturbs only the *logged* granularity tag, never the prompt the model receives. This
  is the cleaner experimental design per Reflexion's mismatched-context ablation pattern: it
  isolates the log-side mismatch effect from any "what the model sees" confound.

* The trajectory record schema is preserved exactly. `MatchedMismatchRecord`'s first six fields
  match `TRAJECTORY_RECORD_FIELDS` in name, order, and type so a Phase 2 evaluator can read
  trajectories from all three conditions through one schema. The `extras` mapping is appended, not
  interleaved.

* Two strategies are exposed deliberately: `random` is a weak-perturbation control whose
  null-hypothesis equivalent is "the tag is random noise," while `adversarial` is the strong probe
  whose null-hypothesis equivalent is "the tag is actively misleading." Per Reflexion, the strongest
  mismatch ablation forces the most distant choice; this is the recommended default for t0012's
  headline contrast.

* The phase-ordered walk is a public iterator (`iter_phases`) so downstream tasks share one
  canonical traversal of the v2 hierarchy. Per Plan-and-Solve and Least-to-Most, the phase order
  itself is signal — losing it would conflate the granularity-mismatch effect with a
  step-order-mismatch effect.

* `subtask` is equidistant from `global` and `atomic` in the adversarial map; we pin
  `subtask → atomic`. This is documented in `description.md` and asserted in
  `test_adversarial_strategy_correctness` so a future change is detected.

## Trajectory Schema

The canonical six-field schema from t0007 is reused unchanged. `MatchedMismatchRecord` extends it
with one extra field `extras` whose well-known key `_correct_granularity` holds the correct tag.

| Field | Type | Description |
| --- | --- | --- |
| `turn_index` | `int` | Zero-based index of the executed phase. |
| `granularity` | `str` | The *wrong* granularity tag emitted for this step. |
| `thought` | `str` | The free-form thought text from the model. |
| `action` | `str` | The action: `"finish"`, `"thought_only"`, `"<tool>(<args>)"`, or `"<unparsed>"`. |
| `observation` | `str` | The tool's return value, the final answer, or the parse-error message. |
| `confidence` | `float \| None` | Optional self-reported confidence in `[0.0, 1.0]`; `None` when not available. |
| `extras` | `dict[str, str]` | At minimum: `{"_correct_granularity": <correct_tag>, "phase_kind": ..., "delegate": ..., "mismatch_strategy": ...}`. |

## Summary

This library is condition C of the project's A-vs-B-vs-C comparison. It wraps either of the sister
libraries (t0006's scope-aware ReAct or t0007's scope-unaware Plan-and-Solve) with a phase-ordered
walk over a v2 annotation tree from t0009 and substitutes a deliberately incorrect granularity tag
at each step. The trajectory schema is the canonical six-field schema from t0007, unchanged; the
per-step correct tag is recorded in an `extras` blob so downstream evaluators can compute the
per-step mismatch contribution.

Within the project, this library is the third leg of the Phase 2 evaluation harness designed by
t0012. The harness will compare A (scope-aware), B (scope-unaware), and C (matched-mismatch) on the
same annotation set with the same trajectory schema, isolating the effect of the granularity tag
from delegate-specific reasoning effects. The library exposes both `random` and `adversarial`
strategies so t0012 can run an ablation that decomposes the mismatch contribution into "any wrong
tag" vs. "the most distant wrong tag."

Limitations and known gaps: the wrapper drives the v2-walk loop itself rather than calling each
delegate's outer `run()` method, so any post-`run()` book-keeping the delegates do (writing a JSONL
trajectory file in t0006's case) is not propagated. If t0012 needs that side effect it must either
invoke the delegates directly or open an issue here. The wrapper also does not currently support
per-step strategy overrides — the strategy is a single literal that applies uniformly across all
phases. If t0012 finds it useful to inject targeted mismatches in specific phases, that should be
added in a v2 of this library.
