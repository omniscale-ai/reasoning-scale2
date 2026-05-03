---
spec_version: "2"
library_id: "matched_mismatch_v2"
documented_by_task: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
date_documented: "2026-05-02"
---
# Matched-Mismatch v2 (PlanAndSolveAgentV3 delegate)

## Metadata

* **Name**: Matched-Mismatch v2 (PlanAndSolveAgentV3 delegate)
* **Version**: 0.2.0
* **Task**: `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
* **Dependencies**: none beyond the project's existing libraries
  (`tasks.t0010_matched_mismatch_library`, `tasks.t0021_plan_and_solve_v2_with_final_confidence`,
  and the sibling `plan_and_solve_v3` library in this same task)
* **Modules**: `code/matched_mismatch_v2.py`
* **Tests**: `code/test_matched_mismatch_v2.py`

## Overview

Matched-Mismatch v2 is a fork of the t0010 matched-mismatch wrapper that fixes the structural defect
identified by suggestion **S-0026-02**: in t0026, variant C delegated to `scope_aware_react` (the
t0010 default), so its scaffold inherited variant **A**'s ReAct loop and merely tacked on
adversarially-perturbed granularity labels — not variant **B**'s plan-and-solve scaffold plus extra
label degradation. The paired McNemar B-vs-C significance therefore came from the scaffold
difference, not the label perturbation, mechanically rejecting RQ5 for the wrong reason.

This library retargets the wrapper at `PlanAndSolveAgentV3` (the fault-tolerant Plan-and-Solve fork
in this same task). The inner agent is now Plan-and-Solve, the trajectory record shape is the v2
record shape (`TrajectoryRecordV2` from `t0021`), and the adversarial-perturbation logic is
preserved verbatim from t0010. After this fix, variant C's trajectories share the
`plan_and_solve_v3` decision-log shape with variant B; the only systematic difference between B and
C is the granularity-label perturbation, which is exactly the contrast RQ5 wants to study.

The implementation is intentionally a thin post-processor:

1. Run `PlanAndSolveAgentV3` once on the whole problem; obtain its `AgentResultV3` and its
   `TrajectoryRecordV2` list.
2. Build a phase walk from the v2 hierarchy annotation via `iter_phases` (re-used verbatim from
   t0010).
3. For each record `i` in the v3 trajectory, look up `phases[min(i, P-1)].correct_tag` (where
   `P = len(phases)`) and apply the canonical adversarial map (`global → atomic`,
   `subtask → atomic`, `atomic → global`) to obtain a wrong tag. Overwrite the record's
   `granularity` field with that wrong tag. If the phase walk is empty, every record is tagged with
   the literal `"atomic"` (a fixed default; `"unspecified"` is not in the granularity vocabulary).

## API Reference

### `MatchedMismatchV2Agent`

```python
@dataclass(slots=True)
class MatchedMismatchV2Agent:
    model_call: Callable[[str], str]
    tool_registry: dict[str, Callable[[str], str]] = field(default_factory=dict)
    max_steps: int = 32
    mismatch_strategy: Literal["adversarial"] = "adversarial"
    seed: int = 0

    def run(self, *, problem: str, annotation: Mapping[str, Any]) -> AgentRunResultV2: ...
```

The `mismatch_strategy` is pinned to `"adversarial"` because the t0026 finding (S-0026-02) motivated
specifically this perturbation policy. Random perturbation is intentionally not supported in v2 —
the random strategy from t0010 stays available there for backward-compat. The `seed` field is
retained for API symmetry with the t0010 wrapper; the adversarial map is deterministic so the seed
is currently unused but kept for forward compatibility.

### `AgentRunResultV2`

```python
@dataclass(frozen=True, slots=True)
class AgentRunResultV2:
    final_answer: str | None
    trajectory: list[TrajectoryRecordV2]
    plan: list[str]
    final_confidence: float | None
    final_confidence_parse_failures: int
    plan_parser_recovery_path: str
    plan_parser_attempts: int
    phases: list[Phase]
    delegate: str
```

Identical to `AgentResultV3` plus two extra fields: `phases` carries the un-perturbed v2 phase walk
so downstream consumers can reconstruct each step's correct tag, and `delegate` is the literal
`"scope_unaware_planandsolve_v3"` used in the harness logs for symmetry with t0010 logging.

### `DELEGATE_PLAN_AND_SOLVE_V3`

String constant `"scope_unaware_planandsolve_v3"`. The single supported delegate id for v2.

## Adversarial-Perturbation Policy (verbatim from t0010)

* `global → atomic`
* `subtask → atomic`
* `atomic → global`

The label set is `{"global", "subtask", "atomic"}`. The mapping never produces the matched tag, so
every record carries a strictly wrong granularity label. The same map is re-imported from t0010 via
`ADVERSARIAL_MAP` rather than redefined, preventing drift between v1 and v2.

## Mapping Rule from PnS-v3 Trajectory Records to Perturbed Labels

If the v2 hierarchy yields a phase walk of length `P` (one phase per "step the model should have
done"), and the v3 trajectory has length `T`, then for each record at index `i` we consult
`phases[min(i, P-1)].correct_tag`, apply the adversarial map, and overwrite the record's
`granularity` field. If `P == 0` (annotation has no parseable phases), every record is given the
literal label `"atomic"` (a fixed adversarial default — `"unspecified"` does not exist in the
granularity vocabulary).

## Usage Examples

```python
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.matched_mismatch_v2 import (
    MatchedMismatchV2Agent,
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

agent = MatchedMismatchV2Agent(model_call=model_call, tool_registry={})
result = agent.run(
    problem="A cylinder of radius 3 cm and height 7 cm is filled with water...",
    annotation={"hierarchy": {"global": "...", "subtasks": [...], "global_atomics": []}},
)

assert result.delegate == "scope_unaware_planandsolve_v3"
print(result.final_answer)
print([r.granularity for r in result.trajectory])  # adversarially perturbed
```

## Dependencies

No external Python packages beyond the project's existing libraries. Imports the adversarial map,
phase walker, and `Phase` dataclass from t0010, the v2 trajectory record schema from t0021, and the
v3 agent from the sibling `plan_and_solve_v3` library:

* `tasks.t0010_matched_mismatch_library.code.matched_mismatch` — provides `ADVERSARIAL_MAP`,
  `GRANULARITY_VALUES`, `Phase`, and `iter_phases`.
* `tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2` — provides
  `TrajectoryRecordV2`.
* `tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.planandsolve_v3` — provides
  `PlanAndSolveAgentV3` and `AgentResultV3`.

## Testing

```bash
uv run pytest tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/test_matched_mismatch_v2.py
```

Two tests cover the perturbation policy with the deterministic `ScriptedModel` fake from t0007:
non-empty phase walk (granularity is overwritten with the adversarial map's outputs and the first
record corresponds to the `global` phase mapped to `"atomic"`) and empty phase walk (every record
gets the `"atomic"` default). There is no network or API call in the test suite.

## Main Ideas

* **Same external API as t0010, different inner scaffold.** The library exposes a single
  `MatchedMismatchV2Agent.run` entry point that returns a result whose trajectory is shaped exactly
  like a `PlanAndSolveAgentV3` trajectory, plus the un-perturbed phase walk for downstream
  inspection. The harness can swap in the v2 wrapper without touching prediction-asset shape.
* **Post-processing rather than per-phase prompting.** t0010 ran one model call per phase and
  emitted one record per phase. v2 runs the v3 agent once on the whole problem and then perturbs the
  resulting trajectory's `granularity` labels. This guarantees the trajectory shape matches B's,
  which is the contrast RQ5 actually needs.
* **Adversarial map is the single source of truth.** The perturbation rule is re-imported from t0010
  via `ADVERSARIAL_MAP`. There is no per-task copy of the rule. The seed and `mismatch_strategy`
  fields on the agent dataclass exist only for API symmetry with t0010; the implementation supports
  only the deterministic adversarial strategy.
* **Empty annotation falls back to a fixed label.** When the v2 hierarchy has no parseable phases,
  every record receives the literal `"atomic"` label. This is intentional: `"unspecified"` is not a
  member of `GRANULARITY_VALUES`, so emitting it would confuse downstream metric code that expects
  one of `{"global", "subtask", "atomic"}`.

## Summary

Matched-Mismatch v2 is the surgical fix to the t0026 variant-C delegate defect (S-0026-02). The
implementation is ~80 lines of code: it imports the adversarial map and phase walker from t0010
verbatim, runs `PlanAndSolveAgentV3` once on the full problem, and overwrites the resulting v2
trajectory records' `granularity` field using a per-index lookup into the v2 phase walk. The
external API is intentionally close to t0010's so the t0027 harness can drive the v2 wrapper with
the same per-instance wiring it uses for the v1 wrapper.

The library is consumed by the t0027 re-run harness for variant C only. Acceptance gate: on a
5-instance smoke from the FrontierScience subset, C produces trajectories with the
`plan_and_solve_v3` decision-log shape (not the t0010 ReAct shape). Verified by inspecting one
trajectory file per instance.
