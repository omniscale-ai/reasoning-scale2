"""Unit tests for the v2 matched-mismatch wrapper that delegates to ``PlanAndSolveAgentV3``.

Two cases are covered:

* ``test_run_perturbs_granularity_with_nonempty_phase_walk`` — the v2 hierarchy yields a non-empty
  phase walk; the wrapper replaces every record's ``granularity`` with the adversarial label
  derived from the corresponding phase's ``correct_tag``.
* ``test_run_uses_default_atomic_when_phase_walk_is_empty`` — the annotation has no parseable
  phases; every record is tagged with the literal ``"atomic"`` (the fixed adversarial default).

Both tests use the deterministic :class:`ScriptedModel` fake from t0007 so no network/API calls are
made. Each test also asserts the v3-shaped trajectory record schema (``TrajectoryRecordV2``) is
preserved end-to-end and that the ``delegate`` field on the result equals
``"scope_unaware_planandsolve_v3"`` — the structural fix mandated by S-0026-02.
"""

from __future__ import annotations

from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import ScriptedModel
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    TrajectoryRecordV2,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.matched_mismatch_v2 import (
    DELEGATE_PLAN_AND_SOLVE_V3,
    MatchedMismatchV2Agent,
)

_VALID_PLAN_TEXT: str = "1. Restate the problem.\n2. Compute the answer.\n"


def _executor_finish_response(*, answer: str = "42") -> str:
    return f"FINAL_ANSWER: {answer}"


def _confidence_response() -> str:
    return "0.7"


def test_run_perturbs_granularity_with_nonempty_phase_walk() -> None:
    annotation: dict[str, object] = {
        "hierarchy": {
            "global": "Restate and solve the multiplication problem.",
            "subtasks": [
                {
                    "subtask": "Identify the operands and the operator.",
                    "atomics": [
                        "Read the two operands.",
                        "Read the operator symbol.",
                    ],
                },
            ],
            "global_atomics": [],
        }
    }
    model = ScriptedModel(
        responses=[
            _VALID_PLAN_TEXT,
            _executor_finish_response(answer="42"),
            _confidence_response(),
        ]
    )
    agent = MatchedMismatchV2Agent(model_call=model, tool_registry={})
    result = agent.run(problem="What is 6 times 7?", annotation=annotation)

    assert result.delegate == DELEGATE_PLAN_AND_SOLVE_V3
    assert result.final_answer == "42"
    assert result.plan == ["Restate the problem.", "Compute the answer."]
    # The PnS-v3 trajectory is one record per executed step; with two plan steps and the v1 executor
    # finishing on the first step (FINAL_ANSWER short-circuit), we expect at least one record.
    assert len(result.trajectory) >= 1
    # Phase walk: global, subtask, atomic, atomic. Adversarial map: global->atomic, subtask->atomic,
    # atomic->global. Every record's granularity must therefore be either "atomic" or "global"
    # (never the original "unspecified" or any matched tag).
    for record in result.trajectory:
        assert isinstance(record, TrajectoryRecordV2)
        assert record.granularity in {"atomic", "global"}
    # The very first record must correspond to phase index 0 == global, mapped to atomic.
    assert result.trajectory[0].granularity == "atomic"
    # And the un-perturbed phase walk is exposed for downstream consumers.
    assert len(result.phases) == 4
    assert [p.correct_tag for p in result.phases] == [
        "global",
        "subtask",
        "atomic",
        "atomic",
    ]


def test_run_uses_default_atomic_when_phase_walk_is_empty() -> None:
    annotation: dict[str, object] = {
        "hierarchy": {
            "global": "",
            "subtasks": [],
            "global_atomics": [],
        }
    }
    model = ScriptedModel(
        responses=[
            _VALID_PLAN_TEXT,
            _executor_finish_response(answer="42"),
            _confidence_response(),
        ]
    )
    agent = MatchedMismatchV2Agent(model_call=model, tool_registry={})
    result = agent.run(problem="What is 6 times 7?", annotation=annotation)

    assert result.delegate == DELEGATE_PLAN_AND_SOLVE_V3
    assert result.final_answer == "42"
    assert len(result.phases) == 0
    assert len(result.trajectory) >= 1
    for record in result.trajectory:
        assert isinstance(record, TrajectoryRecordV2)
        assert record.granularity == "atomic"
