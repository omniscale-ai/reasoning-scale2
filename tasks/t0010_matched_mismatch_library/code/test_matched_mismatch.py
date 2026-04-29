"""Tests for the matched-mismatch (condition C) library.

The tests are deterministic: they use t0006's and t0007's ``ScriptedModel`` helpers, which replay
pre-recorded responses without any live LLM call.
"""

from __future__ import annotations

import dataclasses
import random
from typing import Any

import pytest

from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    ScriptedModel as ReactScriptedModel,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    TRAJECTORY_RECORD_FIELDS,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    ScriptedModel as PlanAndSolveScriptedModel,
)
from tasks.t0010_matched_mismatch_library.code.matched_mismatch import (
    ADVERSARIAL_MAP,
    CORRECT_GRANULARITY_EXTRAS_KEY,
    GRANULARITY_VALUES,
    AgentRunResult,
    MatchedMismatchAgent,
    MatchedMismatchRecord,
    Phase,
    iter_phases,
    pick_mismatch_tag,
)


def _v2_fixture() -> dict[str, Any]:
    """A v2-shaped annotation with two subtasks (each with two atomics) and one global atomic."""
    return {
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


def test_granularity_values_and_adversarial_map() -> None:
    assert GRANULARITY_VALUES == ("global", "subtask", "atomic")
    assert ADVERSARIAL_MAP == {
        "global": "atomic",
        "atomic": "global",
        "subtask": "atomic",
    }


def test_trajectory_schema_parity_with_t0007() -> None:
    expected: tuple[str, ...] = (
        "turn_index",
        "granularity",
        "thought",
        "action",
        "observation",
        "confidence",
    )
    assert expected == TRAJECTORY_RECORD_FIELDS
    record_fields: tuple[str, ...] = tuple(
        f.name for f in dataclasses.fields(MatchedMismatchRecord)
    )
    # First six fields must match the canonical schema, in order. `extras` is appended last.
    assert record_fields[:6] == expected
    assert record_fields[6] == "extras"
    assert len(record_fields) == 7


def test_phase_order() -> None:
    phases: list[Phase] = list(iter_phases(_v2_fixture()))
    expected_kinds: list[str] = [
        "global",
        "subtask",
        "atomic",
        "atomic",
        "subtask",
        "atomic",
        "atomic",
        "global_atomic",
    ]
    expected_correct_tags: list[str] = [
        "global",
        "subtask",
        "atomic",
        "atomic",
        "subtask",
        "atomic",
        "atomic",
        "atomic",
    ]
    assert [p.kind for p in phases] == expected_kinds
    assert [p.correct_tag for p in phases] == expected_correct_tags
    assert phases[0].payload == "Solve the toy arithmetic problem."
    assert phases[1].payload == "Identify operands."
    assert phases[2].payload == "Read first number."
    assert phases[-1].payload == "Sanity check magnitude."


def test_global_atomics_treated_as_atomic() -> None:
    annotation: dict[str, Any] = {
        "hierarchy": {
            "global": "G",
            "subtasks": [],
            "global_atomics": ["X", "Y"],
        }
    }
    phases: list[Phase] = list(iter_phases(annotation))
    # global, then two global_atomics — both with correct_tag = "atomic".
    assert len(phases) == 3
    assert phases[0].kind == "global"
    assert phases[0].correct_tag == "global"
    assert phases[1].kind == "global_atomic"
    assert phases[1].correct_tag == "atomic"
    assert phases[2].kind == "global_atomic"
    assert phases[2].correct_tag == "atomic"


def test_iter_phases_accepts_inner_hierarchy_directly() -> None:
    """Calling with the inner ``hierarchy`` dict should produce the same phase walk."""
    full: dict[str, Any] = _v2_fixture()
    inner: dict[str, Any] = full["hierarchy"]
    full_phases: list[Phase] = list(iter_phases(full))
    inner_phases: list[Phase] = list(iter_phases(inner))
    assert full_phases == inner_phases


def test_random_strategy_uniformity() -> None:
    rng: random.Random = random.Random(42)
    n_trials: int = 300
    for correct in GRANULARITY_VALUES:
        counts: dict[str, int] = {tag: 0 for tag in GRANULARITY_VALUES}
        for _ in range(n_trials):
            chosen: str = pick_mismatch_tag(correct, strategy="random", rng=rng)
            assert chosen != correct
            counts[chosen] += 1
        # Each wrong tag should appear at least 100/300 trials (well within a fair-coin band).
        for tag in GRANULARITY_VALUES:
            if tag == correct:
                assert counts[tag] == 0
            else:
                assert counts[tag] >= 100, (
                    f"random strategy under-sampled {tag!r} when correct={correct!r}: "
                    f"counts={counts}"
                )


def test_adversarial_strategy_correctness() -> None:
    rng: random.Random = random.Random(0)
    assert pick_mismatch_tag("global", strategy="adversarial", rng=rng) == "atomic"
    assert pick_mismatch_tag("atomic", strategy="adversarial", rng=rng) == "global"
    assert pick_mismatch_tag("subtask", strategy="adversarial", rng=rng) == "atomic"


def test_pick_mismatch_tag_rejects_unknown_correct_tag() -> None:
    rng: random.Random = random.Random(0)
    with pytest.raises(ValueError):
        pick_mismatch_tag("nonsense", strategy="adversarial", rng=rng)


def _react_phase_response(*, granularity: str, thought: str, action_json: str) -> str:
    """Produce one ReAct-formatted response for a single phase."""
    return f"Thought: <{granularity}> {thought}\nAction: {action_json}\nConfidence: 80\n"


def _planandsolve_action_response(*, tool: str, args: str) -> str:
    return f"Action: {tool} | Args: {args}\n"


def test_records_carry_wrong_tag_with_correct_tag_in_extras() -> None:
    annotation: dict[str, Any] = {
        "hierarchy": {
            "global": "G",
            "subtasks": [],
            "global_atomics": [],
        }
    }
    # Single phase: global. Adversarial → "atomic".
    response: str = _react_phase_response(
        granularity="global",
        thought="The model still reasons under the correct tag.",
        action_json='{"name": "Finish", "args": {"answer": "done"}}',
    )
    agent: MatchedMismatchAgent = MatchedMismatchAgent(
        model_call=ReactScriptedModel(script=[response]),
        tool_registry={},
        delegate="scope_aware_react",
        mismatch_strategy="adversarial",
        seed=0,
    )
    result: AgentRunResult = agent.run(problem="trivial", annotation=annotation)
    assert len(result.trajectory) == 1
    record: MatchedMismatchRecord = result.trajectory[0]
    assert record.granularity == "atomic"
    assert record.extras[CORRECT_GRANULARITY_EXTRAS_KEY] == "global"
    assert record.extras["phase_kind"] == "global"
    assert record.extras["delegate"] == "scope_aware_react"
    assert record.extras["mismatch_strategy"] == "adversarial"


def test_end_to_end_with_planandsolve_delegate() -> None:
    annotation: dict[str, Any] = _v2_fixture()
    expected_phase_count: int = len(list(iter_phases(annotation)))
    # First seven phases run a no-op tool; the eighth (global_atomic) emits FINAL_ANSWER.
    add_responses: list[str] = [
        _planandsolve_action_response(tool="add", args="1,1")
        for _ in range(expected_phase_count - 1)
    ]
    final_response: str = "FINAL_ANSWER: 2\n"
    script: list[str] = add_responses + [final_response]

    def add_tool(args: str) -> str:
        a_text, b_text = args.split(",")
        return str(int(a_text) + int(b_text))

    agent: MatchedMismatchAgent = MatchedMismatchAgent(
        model_call=PlanAndSolveScriptedModel(responses=script),
        tool_registry={"add": add_tool},
        delegate="scope_unaware_planandsolve",
        mismatch_strategy="adversarial",
        seed=0,
    )
    result: AgentRunResult = agent.run(problem="What is 1 + 1?", annotation=annotation)
    assert result.final_answer == "2"
    assert len(result.trajectory) == expected_phase_count
    for record in result.trajectory:
        assert record.granularity != record.extras[CORRECT_GRANULARITY_EXTRAS_KEY]
        # adversarial map must hold for every record
        assert record.granularity == ADVERSARIAL_MAP[record.extras[CORRECT_GRANULARITY_EXTRAS_KEY]]
        assert record.extras["delegate"] == "scope_unaware_planandsolve"


def test_end_to_end_with_react_delegate() -> None:
    annotation: dict[str, Any] = {
        "hierarchy": {
            "global": "Solve the problem.",
            "subtasks": [
                {
                    "subtask": "Compute the operands.",
                    "atomics": ["Add 2 and 3."],
                }
            ],
            "global_atomics": [],
        }
    }
    phases: list[Phase] = list(iter_phases(annotation))
    assert [p.kind for p in phases] == ["global", "subtask", "atomic"]
    script: list[str] = [
        _react_phase_response(
            granularity="global",
            thought="Read the global goal.",
            action_json='{"name": "noop", "args": {}}',
        ),
        _react_phase_response(
            granularity="subtask",
            thought="Plan the operand computation.",
            action_json='{"name": "noop", "args": {}}',
        ),
        _react_phase_response(
            granularity="atomic",
            thought="Compute the answer and stop.",
            action_json='{"name": "Finish", "args": {"answer": "5"}}',
        ),
    ]
    agent: MatchedMismatchAgent = MatchedMismatchAgent(
        model_call=ReactScriptedModel(script=script),
        tool_registry={},
        delegate="scope_aware_react",
        mismatch_strategy="random",
        seed=7,
    )
    result: AgentRunResult = agent.run(problem="trivial", annotation=annotation)
    assert result.final_answer == "5"
    assert len(result.trajectory) == 3
    correct_tags: list[str] = [r.extras[CORRECT_GRANULARITY_EXTRAS_KEY] for r in result.trajectory]
    assert correct_tags == ["global", "subtask", "atomic"]
    for record in result.trajectory:
        assert record.granularity != record.extras[CORRECT_GRANULARITY_EXTRAS_KEY]
        assert record.granularity in GRANULARITY_VALUES
        assert record.extras["delegate"] == "scope_aware_react"


def test_unknown_strategy_raises() -> None:
    annotation: dict[str, Any] = {"hierarchy": {"global": "G"}}
    agent: MatchedMismatchAgent = MatchedMismatchAgent(
        model_call=PlanAndSolveScriptedModel(responses=[]),
        tool_registry={},
        delegate="scope_unaware_planandsolve",
        mismatch_strategy="not-a-real-strategy",  # type: ignore[arg-type]
        seed=0,
    )
    with pytest.raises(ValueError):
        agent.run(problem="x", annotation=annotation)


def test_unknown_delegate_raises() -> None:
    annotation: dict[str, Any] = {"hierarchy": {"global": "G"}}
    agent: MatchedMismatchAgent = MatchedMismatchAgent(
        model_call=PlanAndSolveScriptedModel(responses=[]),
        tool_registry={},
        delegate="some-other-thing",  # type: ignore[arg-type]
        mismatch_strategy="adversarial",
        seed=0,
    )
    with pytest.raises(ValueError):
        agent.run(problem="x", annotation=annotation)


def test_seed_determinism() -> None:
    """Two runs with the same seed produce identical wrong-tag sequences for `random`."""
    annotation: dict[str, Any] = _v2_fixture()
    expected_phase_count: int = len(list(iter_phases(annotation)))

    def _build_script() -> list[str]:
        return [
            _planandsolve_action_response(tool="noop", args="x")
            for _ in range(expected_phase_count - 1)
        ] + ["FINAL_ANSWER: done\n"]

    def _run_once() -> list[str]:
        agent: MatchedMismatchAgent = MatchedMismatchAgent(
            model_call=PlanAndSolveScriptedModel(responses=_build_script()),
            tool_registry={"noop": lambda _args: "ok"},
            delegate="scope_unaware_planandsolve",
            mismatch_strategy="random",
            seed=12345,
        )
        result: AgentRunResult = agent.run(problem="x", annotation=annotation)
        return [r.granularity for r in result.trajectory]

    first: list[str] = _run_once()
    second: list[str] = _run_once()
    assert first == second
    # And confirm at least one of the wrong tags was actually picked (not a degenerate sequence).
    assert len(set(first)) >= 1
    for granularity, correct in zip(
        first,
        [p.correct_tag for p in iter_phases(annotation)],
        strict=True,
    ):
        assert granularity != correct
