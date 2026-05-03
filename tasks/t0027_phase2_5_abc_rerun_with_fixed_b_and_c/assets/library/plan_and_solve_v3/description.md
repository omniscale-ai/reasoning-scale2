---
spec_version: "2"
library_id: "plan_and_solve_v3"
documented_by_task: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
date_documented: "2026-05-02"
---
# Plan-and-Solve v3 (Fault-Tolerant Plan Parser)

## Metadata

* **Name**: Plan-and-Solve v3 (Fault-Tolerant Plan Parser)
* **Version**: 0.3.0
* **Task**: `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
* **Dependencies**: none beyond the project's existing libraries
  (`tasks.t0007_scope_unaware_planandsolve_library`,
  `tasks.t0021_plan_and_solve_v2_with_final_confidence`)
* **Modules**: `code/planandsolve_v3.py`
* **Tests**: `code/test_planandsolve_v3.py`

## Overview

Plan-and-Solve v3 is a fork of Plan-and-Solve v2
(`tasks.t0021_plan_and_solve_v2_with_final_confidence`) that adds a bounded fault-tolerance chain to
the plan parser. The motivation comes from suggestion **S-0026-01**: t0026 found that 16 of 130
paired runs of variant B (12%) collapsed to `MalformedPlanError`, dominating the A-vs-B paired
McNemar contingency table and rendering RQ1 unanswerable. The structural defect is that v2's planner
step issues a single model call to produce a numbered list, then runs a strict regex
(`^\s*\d+[\.\)]\s+(.+)$`) on the output. When the model emits prose instead of a numbered list,
parsing fails and the entire trajectory aborts.

v3 fixes this with a three-attempt fallback chain. The first attempt is the standard v1 plan prompt
\+ numbered-list parse. If that fails, v3 issues a re-prompt that quotes the bad response back to
the model with an explicit format reminder. If the re-prompt also fails, v3 issues a third prompt
that requires a JSON object with a `steps` array. Only if all three attempts fail does v3 re-raise
`MalformedPlanError` — the same shape today's harness already records.

All other v2 behaviour is preserved unchanged: the plan schema, the executor loop, the verbalized
final-confidence prompt with one retry, and the `TrajectoryRecordV2` schema. The only public surface
change is that `AgentResultV3` adds two diagnostic counters (`plan_parser_recovery_path`,
`plan_parser_attempts`) so the harness can measure how often each recovery path fires.

## API Reference

### `PlanAndSolveAgentV3`

```python
@dataclass(slots=True)
class PlanAndSolveAgentV3:
    model_call: Callable[[str], str]
    tool_registry: dict[str, Callable[[str], str]] = field(default_factory=dict)
    max_steps: int = 32

    def run(self, problem: str) -> AgentResultV3: ...
```

The agent first calls `_robust_parse_plan` to obtain a parsed plan; on success it then drives the v1
executor loop with the recovered plan and finally issues the v2 confidence call. Public-API shape is
identical to `PlanAndSolveAgentV2.run` except for the augmented result type.

### `AgentResultV3`

```python
@dataclass(frozen=True, slots=True)
class AgentResultV3:
    final_answer: str | None
    trajectory: list[TrajectoryRecordV2]
    plan: list[str]
    final_confidence: float | None
    final_confidence_parse_failures: int
    plan_parser_recovery_path: str  # "clean" | "reprompt" | "json_fallback" | "all_failed"
    plan_parser_attempts: int       # 1, 2, or 3
```

`plan_parser_recovery_path == "all_failed"` corresponds to today's `MalformedPlanError` failure mode
— `final_answer is None`, `trajectory == []`, and `plan_parser_attempts == 3`.

### `_robust_parse_plan(*, model_call, problem) -> _RobustPlanResult`

Standalone helper that issues up to three model calls and returns the first parseable plan with a
recovery-path label. The synthesized `plan_text` for the JSON-fallback branch is normalized back to
the canonical `1. ...\n2. ...` numbered-list format so the executor prompt downstream sees a shape
identical to the clean-path plan.

### Templates

* `REPROMPT_PLAN_PROMPT_TEMPLATE` — quotes the bad response (truncated at 600 chars) and re-states
  the strict format rules with a worked example.
* `JSON_PLAN_PROMPT_TEMPLATE` — requires a JSON object `{"steps": [...]}` with non-empty string
  elements.

## Usage Examples

```python
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.planandsolve_v3 import (
    PlanAndSolveAgentV3,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.anthropic_shim import (
    CostTracker,
    make_model_call,
)

cost_tracker = CostTracker()
model_call = make_model_call(
    model_id="claude-opus-4-7",
    cost_tracker=cost_tracker,
    max_tokens=4096,
)

agent = PlanAndSolveAgentV3(model_call=model_call, tool_registry={})
result = agent.run(problem="A cylinder of radius 3 cm and height 7 cm is filled with water...")

print(result.final_answer)
print(result.final_confidence)
print(result.plan_parser_recovery_path)  # one of "clean", "reprompt", "json_fallback", "all_failed"
```

## Dependencies

No external Python packages beyond the project's existing libraries. Imports v1 and v2 directly from
their task code paths:

* `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve` — provides `PlanAndSolveAgent`,
  `parse_plan`, `MalformedPlanError`, `PLAN_PROMPT_TEMPLATE`, `TrajectoryRecord`, `AgentResult`,
  `ScriptedModel`, and `GRANULARITY_UNSPECIFIED`.
* `tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2` — provides
  `TrajectoryRecordV2` and `elicit_final_confidence`.

## Testing

```bash
uv run pytest tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/test_planandsolve_v3.py
```

Tests cover all four recovery paths with the deterministic `ScriptedModel` fake from t0007: clean
parse, re-prompt success, JSON-fallback success, and triple-failure. There is no network or API call
in the test suite.

## Main Ideas

* **Bounded fallback chain.** The cost ceiling for parser recovery is exactly two extra model calls
  per failing instance — a re-prompt plus a JSON-mode call. This is small relative to the 10-15
  calls a successful trajectory consumes.
* **Same observable shape on success.** When recovery succeeds, downstream consumers see the same
  `plan` list, the same `TrajectoryRecordV2` records, the same `final_confidence`, and the same
  decision-log shape as v2. Only the new diagnostic fields differ.
* **Same observable shape on failure.** Triple-failure surfaces as `final_answer is None` and
  `trajectory == []` — the same outward shape as today's `MalformedPlanError`. The harness can still
  distinguish the two via `plan_parser_recovery_path == "all_failed"` if it wants.
* **No re-implementation of v1's executor loop.** The recovered plan is fed back into the unmodified
  v1 agent via a one-shot model-call patch (the patched call serves the recovered plan_text once,
  then falls through to the real model). This avoids forking v1's executor logic.
* **JSON-fallback is structurally simple.** The third prompt asks for `{"steps": [...]}` rather than
  full Anthropic structured-output / tool-use mode, so the same `make_model_call` shim works
  unchanged. Both `{"steps": [...]}` and bare `[...]` arrays are accepted.

## Summary

Plan-and-Solve v3 is a minimal, surgical fix to the parser fragility identified by S-0026-01. The
fork preserves every v1/v2 semantic and only adds a three-attempt plan-parser pipeline plus two
diagnostic counters. On the t0026 paired set the v3 harness will produce trajectories that either
look exactly like clean v2 trajectories (when the first attempt succeeds — expected on the vast
majority of instances) or carry one of three recovery labels.

The library is consumed by the t0027 re-run harness (variant B) and by the v2 wrapper
(`matched_mismatch_v2`, this same task) to ensure variant C delegates to the same fault-tolerant
scaffold rather than to ReAct. Acceptance gate: on the same 130 paired instances, fewer than 3
trajectories fail with `MalformedPlanError` (down from 16 in t0026); residual cause documented in
the results if the gate is missed.
