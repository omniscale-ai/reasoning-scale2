"""Tests for the scope-unaware Plan-and-Solve library.

The tests use a deterministic ``ScriptedModel`` so no LLM calls are made and the suite is free
to run in CI without API keys.
"""

from __future__ import annotations

import pytest

from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    GRANULARITY_UNSPECIFIED,
    TRAJECTORY_RECORD_FIELDS,
    AgentResult,
    MalformedPlanError,
    PlanAndSolveAgent,
    ScriptedModel,
    TrajectoryRecord,
    parse_plan,
)


def test_trajectory_record_fields_match_canonical_tuple() -> None:
    expected: tuple[str, ...] = (
        "turn_index",
        "granularity",
        "thought",
        "action",
        "observation",
        "confidence",
    )
    assert expected == TRAJECTORY_RECORD_FIELDS
    assert TrajectoryRecord.__dataclass_fields__.keys() == set(expected)


def test_parse_plan_simple() -> None:
    text = "1. Add the numbers.\n2. Multiply by two.\n3. Report the result."
    assert parse_plan(text) == [
        "Add the numbers.",
        "Multiply by two.",
        "Report the result.",
    ]


def test_parse_plan_continuation() -> None:
    text = (
        "Some preamble that should be ignored.\n"
        "1. Identify the operands\n"
        "   in the problem statement.\n"
        "2. Compute the sum of\n"
        "   the operands.\n"
    )
    assert parse_plan(text) == [
        "Identify the operands in the problem statement.",
        "Compute the sum of the operands.",
    ]


def test_parse_plan_paren_separator() -> None:
    text = "1) first\n2) second\n3) third\n"
    assert parse_plan(text) == ["first", "second", "third"]


def test_parse_plan_malformed_raises() -> None:
    with pytest.raises(MalformedPlanError):
        parse_plan("This is just prose with no numbered steps.\nNot a list at all.")


def test_scripted_model_round_trip() -> None:
    model = ScriptedModel(responses=["alpha", "beta", "gamma"])
    assert model("ignored") == "alpha"
    assert model("ignored") == "beta"
    assert model("ignored") == "gamma"
    with pytest.raises(IndexError):
        model("ignored")


def _two_step_calculator_responses() -> list[str]:
    return [
        # planner output
        "1. Add the numbers two and three.\n2. Report the result as the final answer.",
        # executor turn 1: call the add tool
        "Action: add | Args: 2,3",
        # executor turn 2: emit the final answer
        "FINAL_ANSWER: 5",
    ]


def test_sequential_execution() -> None:
    def add_tool(args: str) -> str:
        a_text, b_text = args.split(",")
        return str(int(a_text) + int(b_text))

    agent = PlanAndSolveAgent(
        model_call=ScriptedModel(responses=_two_step_calculator_responses()),
        tool_registry={"add": add_tool},
    )
    result: AgentResult = agent.run(problem="What is two plus three?")
    assert result.final_answer == "5"
    assert result.plan == [
        "Add the numbers two and three.",
        "Report the result as the final answer.",
    ]
    assert len(result.trajectory) == 2
    assert result.trajectory[0].action == "add(2,3)"
    assert result.trajectory[0].observation == "5"
    assert result.trajectory[1].action == "finish"
    assert result.trajectory[1].observation == "5"


def test_granularity_unspecified() -> None:
    agent = PlanAndSolveAgent(
        model_call=ScriptedModel(responses=_two_step_calculator_responses()),
        tool_registry={
            "add": lambda args: str(sum(int(x) for x in args.split(","))),
        },
    )
    result = agent.run(problem="What is two plus three?")
    for record in result.trajectory:
        assert record.granularity == GRANULARITY_UNSPECIFIED
        assert record.granularity == "unspecified"


def test_finish_detection_final_answer() -> None:
    # planner output produces three steps but the executor returns FINAL_ANSWER on step 1.
    responses: list[str] = [
        "1. Look at the problem.\n2. Think about it.\n3. Write down the answer.",
        "FINAL_ANSWER: 42",
    ]
    agent = PlanAndSolveAgent(
        model_call=ScriptedModel(responses=responses),
        tool_registry={},
    )
    result = agent.run(problem="What is the answer to the ultimate question?")
    assert result.final_answer == "42"
    # Loop should have terminated after the first executor call, not run all three plan steps.
    assert len(result.trajectory) == 1


def test_trajectory_schema_parity() -> None:
    """Sister task t0006 must conform to this schema; assert the fields are stable."""

    record = TrajectoryRecord(
        turn_index=0,
        granularity="unspecified",
        thought="t",
        action="a",
        observation="o",
        confidence=0.5,
    )
    # Field names and order match TRAJECTORY_RECORD_FIELDS.
    assert tuple(record.__dataclass_fields__.keys()) == TRAJECTORY_RECORD_FIELDS
    # Fields are correctly typed and accessible.
    assert record.turn_index == 0
    assert record.granularity == "unspecified"
    assert record.confidence == 0.5


def test_thought_only_step() -> None:
    """A plan step that needs no tool call should still produce a trajectory record."""

    responses = [
        "1. Plan a thought.\n2. Conclude with the answer.",
        "THOUGHT_ONLY: I will conclude that 7 is the answer.",
        "FINAL_ANSWER: 7",
    ]
    agent = PlanAndSolveAgent(
        model_call=ScriptedModel(responses=responses),
        tool_registry={},
    )
    result = agent.run(problem="Pick the answer.")
    assert result.final_answer == "7"
    assert len(result.trajectory) == 2
    assert result.trajectory[0].action == "thought_only"
    assert result.trajectory[0].observation == ""
    assert result.trajectory[1].action == "finish"


def test_unknown_tool_yields_error_observation() -> None:
    responses = [
        "1. Try to call a missing tool.\n2. Surrender.",
        "Action: nonexistent | Args: anything",
        "FINAL_ANSWER: gave up",
    ]
    agent = PlanAndSolveAgent(
        model_call=ScriptedModel(responses=responses),
        tool_registry={},
    )
    result = agent.run(problem="Demonstrate error recovery.")
    assert result.final_answer == "gave up"
    assert "ERROR: tool 'nonexistent' not found" in result.trajectory[0].observation


def test_max_steps_halts_loop() -> None:
    # Plan with 5 steps, each executor returns THOUGHT_ONLY, max_steps=2 stops after step 2.
    responses = [
        "1. a\n2. b\n3. c\n4. d\n5. e",
        "THOUGHT_ONLY: t1",
        "THOUGHT_ONLY: t2",
    ]
    agent = PlanAndSolveAgent(
        model_call=ScriptedModel(responses=responses),
        tool_registry={},
        max_steps=2,
    )
    result = agent.run(problem="Test halt.")
    assert result.final_answer is None
    assert len(result.trajectory) == 2


def test_malformed_planner_output_propagates() -> None:
    """When the planner returns no numbered steps, ``run`` raises MalformedPlanError."""

    agent = PlanAndSolveAgent(
        model_call=ScriptedModel(responses=["I refuse to make a plan."]),
        tool_registry={},
    )
    with pytest.raises(MalformedPlanError):
        agent.run(problem="Anything.")
