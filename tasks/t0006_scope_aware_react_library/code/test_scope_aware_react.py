"""Deterministic unit tests for the scope-aware ReAct library.

All tests use `ScriptedModel` so no live API calls are made. The trajectory file is written to a
pytest-managed `tmp_path` and parsed back to verify schema integrity.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from tasks.t0006_scope_aware_react_library.code.constants import (
    DEFAULT_GRANULARITY_ON_MISSING_TAG,
    FIELD_ACTION,
    FIELD_CONFIDENCE,
    FIELD_GRANULARITY,
    FIELD_OBSERVATION,
    FIELD_THOUGHT,
    FIELD_TURN_INDEX,
    GRANULARITY_GLOBAL,
    GRANULARITY_SUBTASK,
    OBSERVATION_PARSE_ERROR,
    OBSERVATION_TAG_MISSING_WARNING,
    OBSERVATION_UNKNOWN_TOOL,
    TRAJECTORY_FIELDS,
)
from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    ScopeAwareReactAgent,
    ScriptedModel,
)


def _scripted_turn(*, tag: str, thought: str, action_json: str, confidence: int | None) -> str:
    lines: list[str] = [
        f"Thought: <{tag}> {thought}",
        f"Action: {action_json}",
    ]
    if confidence is not None:
        lines.append(f"Confidence: {confidence}")
    return "\n".join(lines)


def _read_trajectory(*, path: Path) -> list[dict[str, Any]]:
    text: str = path.read_text(encoding="utf-8")
    records: list[dict[str, Any]] = []
    for raw_line in text.splitlines():
        if len(raw_line.strip()) == 0:
            continue
        records.append(json.loads(raw_line))
    return records


def _echo_tool(*, value: str) -> str:
    return f"echoed:{value}"


def _make_agent(
    *,
    tmp_path: Path,
    granularity: str = GRANULARITY_SUBTASK,
    script: list[str],
    max_turns: int = 10,
) -> ScopeAwareReactAgent:
    trajectory_path: Path = tmp_path / "trajectory.jsonl"
    return ScopeAwareReactAgent(
        problem="Test problem statement.",
        granularity=granularity,  # type: ignore[arg-type]
        tool_registry={"echo": _echo_tool},
        model_call=ScriptedModel(script=script),
        trajectory_path=trajectory_path,
        max_turns=max_turns,
    )


def test_tag_injection_in_prompt(tmp_path: Path) -> None:
    """REQ-2: the active granularity must appear in the system prompt sent to the model."""
    script: list[str] = [
        _scripted_turn(
            tag=GRANULARITY_GLOBAL,
            thought="I am done.",
            action_json='{"name": "Finish", "args": {"answer": "ok"}}',
            confidence=80,
        )
    ]
    agent: ScopeAwareReactAgent = _make_agent(
        tmp_path=tmp_path, granularity=GRANULARITY_GLOBAL, script=script
    )
    result = agent.run()
    assert result.finished is True, "agent should terminate on Finish"
    assert agent.last_prompt is not None, "last_prompt should be captured"
    assert f"granularity is {GRANULARITY_GLOBAL}" in agent.last_prompt, (
        "system prompt must instruct the model with the active granularity"
    )
    assert f"<{GRANULARITY_GLOBAL}>" in agent.last_prompt, (
        "system prompt must show the literal tag the model should emit"
    )


def test_action_parsing_round_trip(tmp_path: Path) -> None:
    """REQ-3: action JSON is parsed and dispatched to the registered tool."""
    script: list[str] = [
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Call echo.",
            action_json='{"name": "echo", "args": {"value": "hello"}}',
            confidence=70,
        ),
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Done.",
            action_json='{"name": "Finish", "args": {"answer": "echoed:hello"}}',
            confidence=90,
        ),
    ]
    agent: ScopeAwareReactAgent = _make_agent(tmp_path=tmp_path, script=script)
    result = agent.run()
    assert result.finished is True
    assert result.answer == "echoed:hello"
    assert result.turns == 2
    assert result.trajectory[0].observation == "echoed:hello"


def test_finish_terminates_loop(tmp_path: Path) -> None:
    """REQ-3: Finish action stops the loop even when more script entries remain."""
    script: list[str] = [
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Stop here.",
            action_json='{"name": "Finish", "args": {"answer": "early"}}',
            confidence=55,
        ),
        # Extra entry should never be consumed.
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Should not be reached.",
            action_json='{"name": "echo", "args": {"value": "no"}}',
            confidence=10,
        ),
    ]
    agent: ScopeAwareReactAgent = _make_agent(tmp_path=tmp_path, script=script)
    result = agent.run()
    assert result.finished is True
    assert result.answer == "early"
    assert result.turns == 1


def test_malformed_action_recovery(tmp_path: Path) -> None:
    """REQ-6: malformed Action JSON is recorded and the loop continues."""
    script: list[str] = [
        # Malformed: missing closing brace.
        "Thought: <subtask> bad action\nAction: {not json\nConfidence: 30",
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Recovered.",
            action_json='{"name": "Finish", "args": {"answer": "recovered"}}',
            confidence=85,
        ),
    ]
    agent: ScopeAwareReactAgent = _make_agent(tmp_path=tmp_path, script=script)
    result = agent.run()
    assert result.finished is True
    assert result.answer == "recovered"
    assert result.turns == 2
    first_obs: str = result.trajectory[0].observation
    assert first_obs.startswith(OBSERVATION_PARSE_ERROR), (
        f"expected parse-error marker, got {first_obs!r}"
    )


def test_trajectory_log_schema(tmp_path: Path) -> None:
    """REQ-4: every JSONL record has the six canonical fields and round-trips through json.loads."""
    script: list[str] = [
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Step 1.",
            action_json='{"name": "echo", "args": {"value": "x"}}',
            confidence=42,
        ),
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Done.",
            action_json='{"name": "Finish", "args": {"answer": "x"}}',
            confidence=99,
        ),
    ]
    agent: ScopeAwareReactAgent = _make_agent(tmp_path=tmp_path, script=script)
    result = agent.run()
    records: list[dict[str, Any]] = _read_trajectory(path=agent.trajectory_path)
    assert len(records) == result.turns == 2
    for record in records:
        for field_name in TRAJECTORY_FIELDS:
            assert field_name in record, f"record missing field {field_name!r}: {record}"
        assert isinstance(record[FIELD_TURN_INDEX], int)
        assert isinstance(record[FIELD_GRANULARITY], str)
        assert isinstance(record[FIELD_THOUGHT], str)
        assert isinstance(record[FIELD_ACTION], dict)
        assert isinstance(record[FIELD_OBSERVATION], str)
        assert record[FIELD_CONFIDENCE] is None or isinstance(record[FIELD_CONFIDENCE], float)
    assert records[0][FIELD_CONFIDENCE] == pytest.approx(0.42)
    assert records[1][FIELD_CONFIDENCE] == pytest.approx(0.99)


def test_missing_tag_defaults_to_atomic(tmp_path: Path) -> None:
    """REQ-10: when the model omits the granularity tag, the agent falls back to atomic."""
    script: list[str] = [
        # Thought line without any <tag> prefix.
        "Thought: forgot the tag\n"
        'Action: {"name": "Finish", "args": {"answer": "tagless"}}\n'
        "Confidence: 50",
    ]
    agent: ScopeAwareReactAgent = _make_agent(tmp_path=tmp_path, script=script)
    result = agent.run()
    assert result.finished is True
    record = result.trajectory[0]
    assert record.granularity == DEFAULT_GRANULARITY_ON_MISSING_TAG
    assert record.observation.startswith(OBSERVATION_TAG_MISSING_WARNING)


def test_max_turns_safety_cap(tmp_path: Path) -> None:
    """REQ-3 corollary: agent stops after max_turns even if Finish is never emitted."""
    script: list[str] = [
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought=f"Turn {i}.",
            action_json='{"name": "echo", "args": {"value": "loop"}}',
            confidence=10,
        )
        for i in range(5)
    ]
    agent: ScopeAwareReactAgent = _make_agent(tmp_path=tmp_path, script=script, max_turns=3)
    result = agent.run()
    assert result.finished is False, "agent must not claim finish without Finish action"
    assert result.answer is None
    assert result.turns == 3


def test_unknown_tool_is_observed_not_raised(tmp_path: Path) -> None:
    """Robustness: an action whose tool name is not in the registry yields a marker observation."""
    script: list[str] = [
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Try unknown tool.",
            action_json='{"name": "ghost", "args": {"x": 1}}',
            confidence=20,
        ),
        _scripted_turn(
            tag=GRANULARITY_SUBTASK,
            thought="Bail.",
            action_json='{"name": "Finish", "args": {"answer": "bail"}}',
            confidence=20,
        ),
    ]
    agent: ScopeAwareReactAgent = _make_agent(tmp_path=tmp_path, script=script)
    result = agent.run()
    assert result.finished is True
    assert result.trajectory[0].observation == OBSERVATION_UNKNOWN_TOOL
