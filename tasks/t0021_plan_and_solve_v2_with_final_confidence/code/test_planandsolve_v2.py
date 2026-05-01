"""Unit tests for the v2 Plan-and-Solve library with verbalized ``final_confidence``."""

from __future__ import annotations

from dataclasses import fields

from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    AgentResult as AgentResultV1,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    ScriptedModel,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    TRAJECTORY_RECORD_V2_FIELDS,
    AgentResultV2,
    PlanAndSolveAgentV2,
    TrajectoryRecordV2,
    elicit_final_confidence,
    parse_final_confidence,
)

# --------------------------------------------------------------------------------------------------
# parse_final_confidence
# --------------------------------------------------------------------------------------------------


def test_parse_final_confidence_picks_last_match() -> None:
    text = "I considered values 0.2 and 0.5 but my final answer is: Confidence: 0.8"
    assert parse_final_confidence(text) == 0.8


def test_parse_final_confidence_accepts_one() -> None:
    assert parse_final_confidence("1") == 1.0
    assert parse_final_confidence("Confidence: 1.0") == 1.0
    assert parse_final_confidence("Confidence: 1.000") == 1.0


def test_parse_final_confidence_accepts_zero() -> None:
    assert parse_final_confidence("0") == 0.0
    assert parse_final_confidence("Confidence: 0.0") == 0.0


def test_parse_final_confidence_returns_none_for_non_numeric() -> None:
    assert parse_final_confidence("I am pretty sure but not certain") is None
    assert parse_final_confidence("") is None


def test_parse_final_confidence_clamps_in_bounds() -> None:
    # The strict regex only matches numerals in [0, 1] directly; "1.5" matches the leading "1"
    # at the word boundary and returns 1.0, which is the safe clamp behaviour we want — never
    # exceed the documented range.
    assert parse_final_confidence("My confidence is 1.5") == 1.0
    assert parse_final_confidence("0.95 is high") == 0.95


def test_parse_final_confidence_takes_last_when_prose_has_numbers() -> None:
    text = "Step 1 was clear. Confidence: 0.7"
    # "1" is a valid 0/1 token but "0.7" comes later, so it wins.
    assert parse_final_confidence(text) == 0.7


# --------------------------------------------------------------------------------------------------
# elicit_final_confidence
# --------------------------------------------------------------------------------------------------


def test_elicit_returns_value_on_first_try() -> None:
    model = ScriptedModel(responses=["Confidence: 0.8"])
    value, failures = elicit_final_confidence(
        model_call=model,
        problem="What is 2+2?",
        final_answer="4",
    )
    assert value == 0.8
    assert failures == 0


def test_elicit_retries_once_on_first_parse_failure() -> None:
    model = ScriptedModel(responses=["uncertain", "0.6"])
    value, failures = elicit_final_confidence(
        model_call=model,
        problem="What is 2+2?",
        final_answer="4",
    )
    assert value == 0.6
    assert failures == 1


def test_elicit_returns_none_after_double_failure() -> None:
    model = ScriptedModel(responses=["I'm pretty sure", "still uncertain"])
    value, failures = elicit_final_confidence(
        model_call=model,
        problem="What is 2+2?",
        final_answer="4",
    )
    assert value is None
    assert failures == 2


# --------------------------------------------------------------------------------------------------
# PlanAndSolveAgentV2.run end-to-end with ScriptedModel
# --------------------------------------------------------------------------------------------------


def _scripted_run_with_confidence(*, confidence_responses: list[str]) -> AgentResultV2:
    """Build a ScriptedModel with one plan call, one execute call (FINAL_ANSWER), and the
    confidence responses provided by the test."""
    plan_response = "1. Compute 2+2.\n"
    execute_response = "Thought: trivial.\nFINAL_ANSWER: 4\n"
    responses = [plan_response, execute_response, *confidence_responses]
    model = ScriptedModel(responses=responses)
    agent = PlanAndSolveAgentV2(model_call=model, tool_registry={}, max_steps=4)
    return agent.run(problem="What is 2+2?")


def test_run_emits_field_when_parse_succeeds() -> None:
    result = _scripted_run_with_confidence(confidence_responses=["Confidence: 0.8"])
    assert result.final_answer == "4"
    assert result.final_confidence == 0.8
    assert result.final_confidence_parse_failures == 0
    # Last record (the finishing record) carries the value; earlier ones do not.
    assert len(result.trajectory) >= 1
    assert result.trajectory[-1].final_confidence == 0.8
    if len(result.trajectory) > 1:
        for rec in result.trajectory[:-1]:
            assert rec.final_confidence is None


def test_run_retries_once_then_parses() -> None:
    result = _scripted_run_with_confidence(confidence_responses=["uncertain", "0.6"])
    assert result.final_answer == "4"
    assert result.final_confidence == 0.6
    assert result.final_confidence_parse_failures == 1
    assert result.trajectory[-1].final_confidence == 0.6


def test_run_emits_null_when_parse_fails_twice() -> None:
    result = _scripted_run_with_confidence(
        confidence_responses=["I'm pretty sure", "still uncertain"]
    )
    assert result.final_answer == "4"
    assert result.final_confidence is None
    assert result.final_confidence_parse_failures == 2
    assert result.trajectory[-1].final_confidence is None


def test_run_skips_confidence_when_no_final_answer() -> None:
    """If the v1 agent never returns a FINAL_ANSWER, no confidence call is made and parse
    failures stay at 0 (the field is None because the answer itself is None)."""
    plan_response = "1. Step one.\n2. Step two.\n"
    execute_no_answer = "Thought: still thinking.\nTHOUGHT_ONLY: not done\n"
    responses = [plan_response, execute_no_answer, execute_no_answer]
    model = ScriptedModel(responses=responses)
    agent = PlanAndSolveAgentV2(model_call=model, tool_registry={}, max_steps=2)
    result = agent.run(problem="A long problem with no answer")
    assert result.final_answer is None
    assert result.final_confidence is None
    assert result.final_confidence_parse_failures == 0


# --------------------------------------------------------------------------------------------------
# Schema invariants
# --------------------------------------------------------------------------------------------------


def test_v1_legacy_schema_unchanged() -> None:
    """The v1 ``AgentResult`` must still expose ``(final_answer, trajectory, plan)`` — and crucially
    NOT ``final_confidence`` — so existing callers (e.g., t0010, t0012) keep working."""
    v1_field_names = tuple(f.name for f in fields(AgentResultV1))
    assert v1_field_names == ("final_answer", "trajectory", "plan")
    assert "final_confidence" not in v1_field_names


def test_trajectory_record_v2_has_seven_fields() -> None:
    field_names = tuple(f.name for f in fields(TrajectoryRecordV2))
    assert field_names == TRAJECTORY_RECORD_V2_FIELDS
    assert len(field_names) == 7
    assert field_names[-1] == "final_confidence"


def test_agent_result_v2_field_names() -> None:
    field_names = tuple(f.name for f in fields(AgentResultV2))
    assert field_names == (
        "final_answer",
        "trajectory",
        "plan",
        "final_confidence",
        "final_confidence_parse_failures",
    )
