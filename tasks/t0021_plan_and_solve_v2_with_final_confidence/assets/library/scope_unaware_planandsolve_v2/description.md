---
spec_version: "2"
library_id: "scope_unaware_planandsolve_v2"
documented_by_task: "t0021_plan_and_solve_v2_with_final_confidence"
date_documented: "2026-05-01"
---
# Scope-Unaware Plan-and-Solve v2 (with final_confidence)

## Metadata

* **Name**: Scope-Unaware Plan-and-Solve v2 (with final_confidence)
* **Version**: 1
* **Task**: `t0021_plan_and_solve_v2_with_final_confidence`
* **Dependencies**: none beyond the standard library; transitively imports the v1 library
  `scope_unaware_planandsolve_v1` from `tasks/t0007_scope_unaware_planandsolve_library/`
* **Modules**: `code/planandsolve_v2.py`, `code/constants.py`, `code/paths.py`
* **Tests**: `code/test_planandsolve_v2.py` (16 unit tests, all passing)
* **Reference**: Xiong et al. 2024, "Can LLMs Express Their Uncertainty? An Empirical Evaluation of
  Confidence Elicitation in LLMs", section 3.2 (verbalized confidence, 0/0.5/1 anchors)

## Overview

This library extends the existing scope-unaware Plan-and-Solve agent (built in t0007) with a
verbalized `final_confidence` value on every trajectory it returns. The v1 agent already follows the
Plan-and-Solve protocol of Wang et al. (2023) and produces a six-field per-step trajectory record
`(turn_index, granularity, thought, action, observation, confidence)`; the v1 confidence slot is
unused. The v2 agent issues an additional confidence-elicitation call after the answer is produced,
following the Xiong et al. 2024 section 3.2 black-box protocol — the model rates its own answer on a
`[0.0, 1.0]` scale anchored at `0` (definitely wrong), `0.5` (completely unsure), and `1`
(definitely correct). The parsed value is attached to the finishing trajectory record and to a new
top-level `AgentResultV2.final_confidence` field.

The library composes rather than forks the v1 module. The v1 entry point `PlanAndSolveAgent` is left
untouched and remains importable from
`tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve`. v2 imports v1 symbols and runs
them unchanged, then layers the confidence call on top. This avoids the immutability violation that
would result from editing v1 in place — t0010's matched-mismatch agent imports the v1 schema and
would break otherwise.

The library also exposes `elicit_final_confidence(...)` and `parse_final_confidence(...)` as public
helpers so the t0021 smoke harness (and any downstream user) can elicit the same field on
non-Plan-and-Solve agents — for example wrapping the t0006 `ScopeAwareReactAgent` (Condition A) and
the t0010 `MatchedMismatchAgent` (Condition C) so all three Conditions A/B/C carry the field for
paired analysis.

## API Reference

All public symbols live in `code/planandsolve_v2.py`.

### Data classes

```python
@dataclass(frozen=True, slots=True)
class TrajectoryRecordV2:
    turn_index: int
    granularity: str
    thought: str
    action: str
    observation: str
    confidence: float | None       # v1 per-step slot (still unused; matches v1 schema)
    final_confidence: float | None # populated only on the finishing record
```

```python
@dataclass(frozen=True, slots=True)
class AgentResultV2:
    final_answer: str | None
    trajectory: list[TrajectoryRecordV2]
    plan: list[str]
    final_confidence: float | None             # in [0.0, 1.0] or None on double parse failure
    final_confidence_parse_failures: int       # 0 first-try, 1 retry success, 2 double failure
```

### Functions

```python
def parse_final_confidence(text: str) -> float | None:
    """Strict regex parser. Match `\\b(0(?:\\.\\d+)?|1(?:\\.0+)?)\\b`, take the LAST match,
    clamp the result to [0.0, 1.0]. Return None when no numeric token is found."""
```

```python
def elicit_final_confidence(
    *,
    model_call: Callable[[str], str],
    problem: str,
    final_answer: str,
) -> tuple[float | None, int]:
    """Issue the Xiong2024 verbalized-confidence prompt with one retry on parse failure.
    Returns (value, parse_failures) where parse_failures is 0 on first-try success, 1 on
    retry success, and 2 on double failure (in which case value is None)."""
```

### Agent class

```python
@dataclass(slots=True)
class PlanAndSolveAgentV2:
    model_call: Callable[[str], str]
    tool_registry: dict[str, Callable[[str], str]] = field(default_factory=dict)
    max_steps: int = 32

    def run(self, problem: str) -> AgentResultV2:
        """Run the v1 Plan-and-Solve agent unchanged, then issue one verbalized-confidence
        call (with one retry) and attach the parsed value to the finishing TrajectoryRecordV2
        and to AgentResultV2.final_confidence."""
```

### Public constants

* `CONFIDENCE_PROMPT_TEMPLATE: str` — verbatim Xiong2024 §3.2 prompt with 0/0.5/1 anchors.
* `CONFIDENCE_RETRY_PROMPT_TEMPLATE: str` — stricter retry prompt asking for one number on its own
  line.
* `TRAJECTORY_RECORD_V2_FIELDS: tuple[str, ...]` — canonical ordered tuple of v2 trajectory record
  field names (six v1 fields + `final_confidence`).

### Behavioral guarantees

* When the v1 agent returns no answer (`final_answer is None`), no confidence call is issued and the
  result has `final_confidence=None` and `final_confidence_parse_failures=0`.
* When the parsed value is non-`None`, it is always in `[0.0, 1.0]`.
* The confidence field appears only on the finishing trajectory record (action == "finish"). All
  earlier records have `final_confidence=None`.

## Usage Examples

End-to-end with a real model call (Claude Code CLI via the shared `model_call` helper):

```python
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.model_call import (
    CostTracker,
    make_model_call,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    PlanAndSolveAgentV2,
)

cost_tracker = CostTracker(cap_usd=1.00)
model_call = make_model_call(model="claude-haiku-4-5", cost_tracker=cost_tracker)

agent = PlanAndSolveAgentV2(model_call=model_call, tool_registry={}, max_steps=8)
result = agent.run(problem="Compute the integral of x^2 from 0 to 3.")

print(result.final_answer)             # e.g., "9"
print(result.final_confidence)         # e.g., 0.85
print(result.final_confidence_parse_failures)  # 0
print(result.trajectory[-1].final_confidence)  # 0.85 — only the finishing record has it
```

Reusing only the confidence helper to elicit the field on a different agent (e.g., the t0006
ScopeAware ReAct agent for Condition A or the t0010 MatchedMismatch agent for Condition C):

```python
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    elicit_final_confidence,
)

# After your agent has produced `final_answer`:
value, parse_failures = elicit_final_confidence(
    model_call=model_call,
    problem=problem_text,
    final_answer=final_answer,
)
# value in [0.0, 1.0] or None; parse_failures in {0, 1, 2}
```

Deterministic offline testing with `ScriptedModel`:

```python
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import ScriptedModel
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    PlanAndSolveAgentV2,
)

model = ScriptedModel(responses=[
    "1. Compute 2+2.\n",                          # plan
    "Thought: trivial.\nFINAL_ANSWER: 4\n",       # execute
    "Confidence: 0.8\n",                           # confidence call
])
agent = PlanAndSolveAgentV2(model_call=model, tool_registry={}, max_steps=4)
result = agent.run(problem="What is 2+2?")
assert result.final_confidence == 0.8
assert result.final_confidence_parse_failures == 0
```

## Dependencies

No external dependencies beyond the standard library. The library transitively imports the v1
library `scope_unaware_planandsolve_v1` (from t0007). Both libraries are part of this project; no
PyPI packages are required.

## Testing

Run the 16 unit tests with:

```bash
uv run pytest tasks/t0021_plan_and_solve_v2_with_final_confidence/code/test_planandsolve_v2.py -v
```

The tests cover:

* `parse_final_confidence` — last-match wins, accepts `0` and `1` and decimals like `0.95`, returns
  `None` for non-numeric input, clamps gracefully when the input straddles the bound (e.g., `1.5`
  matches the leading `1` and returns `1.0`).
* `elicit_final_confidence` — first-try success (`failures == 0`), single retry success
  (`failures == 1`), and double failure (`failures == 2` and value is `None`).
* `PlanAndSolveAgentV2.run` end-to-end with a `ScriptedModel` — confirms the field is populated on
  the finishing record, propagates retry semantics, and returns `None` cleanly when the v1 agent
  produces no answer.
* Schema invariants — v1 `AgentResult` still has `(final_answer, trajectory, plan)` and no
  `final_confidence` field, `TrajectoryRecordV2` has exactly seven fields, and `AgentResultV2` has
  the documented five fields.

A 5-row × 3-condition smoke validation harness (`code/run_smoke.py`) provides additional end-to-end
evidence using the local `claude` CLI on FrontierScience-Olympiad rows; see
`results/smoke_report.json` and `results/results_detailed.md`.

## Main Ideas

* **Compose, don't fork.** The v1 module from t0007 is unchanged. v2 imports v1 symbols and runs
  them unchanged, then layers a single post-call confidence elicitation on top. This protects t0010
  from breakage and respects the ARF immutability rule.
* **Two-call protocol with prompt-level conversation reconstruction.** The v1 model-call shape is
  stateless `Callable[[str], str]`. The confidence call therefore reconstructs the conversation in
  its prompt body ("Problem: ... Final answer: ... Confidence: ..."), which honors the Xiong2024
  spirit (the model rates its own answer without revising it) without requiring a chat-style API.
* **Strict regex parse with a single retry.** Use `\b(0(?:\.\d+)?|1(?:\.0+)?)\b` and pick the last
  match so trailing `Confidence: 0.8` wins over earlier in-prose mentions. On parse failure, retry
  once with a stricter prompt; on second failure, set `final_confidence=None` and increment
  `final_confidence_parse_failures`. This bounds cost at exactly two extra calls per row.
* **All three conditions carry the field.** A/B/C smoke conditions all wrap the same
  `elicit_final_confidence(...)` helper so paired calibration analysis is well-defined and Metric 2
  is comparable across conditions.

## Summary

This library ships a thin v2 wrapper around the existing scope-unaware Plan-and-Solve agent that
emits a verbalized `final_confidence` value on every result. The implementation strategy is
composition: v1 is imported unchanged, the v1 agent runs to produce an answer, and a single
post-call elicitation following the Xiong et al. 2024 section 3.2 black-box protocol attaches a
`[0.0, 1.0]` confidence (or `None` on double parse failure) to the finishing trajectory record and
to a new `AgentResultV2.final_confidence` slot.

Within the project, the library is the canonical scope-unaware agent for downstream calibration
work. The t0021 5×3 smoke harness uses it directly for Condition B (scope-unaware) and reuses the
public `elicit_final_confidence(...)` helper to attach the field to Condition A (scope-aware ReAct)
and Condition C (matched-mismatch). The smoke pipeline writes per-condition Metric 2
(`overconfident_error_rate`) values to `results/metrics.json` so downstream tasks (notably t0023 and
the calibration follow-ups) can consume calibrated trajectories without touching the v1 module.

Known limitations: the protocol issues a separate API call per row, doubling the per-row cost on the
confidence axis (one prompt for the answer, one for the confidence — plus at most one retry). The
strict regex deliberately accepts only numerals already in `[0, 1]`; out-of-bound values like `1.5`
are clamped to `1.0` because the regex matches the leading `1` at the word boundary. If the
parse-failure rate on a target model exceeds 20%, the smoke harness reports it in
`results/smoke_report.json` so the prompt can be tightened (or moved to JSON mode) in a follow-up
task.
