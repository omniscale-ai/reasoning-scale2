"""Unit tests for the fault-tolerant plan parser in ``planandsolve_v3``.

Covers four cases:

* ``test_clean_parse_path`` — first attempt succeeds; only one model call is consumed.
* ``test_reprompt_recovery_path`` — first response is unparseable; the re-prompt response is a
  valid numbered list; recovery_path == ``"reprompt"``; attempts == 2.
* ``test_json_fallback_recovery_path`` — first two responses are unparseable; the third response
  is a JSON object; recovery_path == ``"json_fallback"``; attempts == 3.
* ``test_all_failed_path`` — all three responses unparseable; the agent returns
  ``recovery_path == "all_failed"`` with ``final_answer is None`` and an empty trajectory.

The tests use the ``ScriptedModel`` fake from t0007 so no network/API calls are made.
"""

from __future__ import annotations

import pytest

from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import ScriptedModel
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.planandsolve_v3 import (
    PlanAndSolveAgentV3,
    _robust_parse_plan,
)

_VALID_PLAN_TEXT: str = "1. Restate the problem.\n2. Compute the answer.\n"
_BAD_PLAN_TEXT: str = "Here is the plan: do step a then step b.\n"
_VALID_JSON_PLAN: str = '{"steps": ["restate the problem", "compute the answer"]}'


def _confidence_response() -> str:
    return "0.7"


def _executor_finish_response(*, answer: str = "42") -> str:
    return f"FINAL_ANSWER: {answer}"


def test_clean_parse_path() -> None:
    model = ScriptedModel(
        responses=[
            _VALID_PLAN_TEXT,
            _executor_finish_response(answer="42"),
            _confidence_response(),
        ]
    )
    agent = PlanAndSolveAgentV3(model_call=model, tool_registry={})
    result = agent.run(problem="What is 6 times 7?")
    assert result.plan_parser_recovery_path == "clean"
    assert result.plan_parser_attempts == 1
    assert result.plan == ["Restate the problem.", "Compute the answer."]
    assert result.final_answer == "42"
    assert result.final_confidence == pytest.approx(0.7)


def test_reprompt_recovery_path() -> None:
    model = ScriptedModel(
        responses=[
            _BAD_PLAN_TEXT,
            _VALID_PLAN_TEXT,
            _executor_finish_response(answer="42"),
            _confidence_response(),
        ]
    )
    agent = PlanAndSolveAgentV3(model_call=model, tool_registry={})
    result = agent.run(problem="What is 6 times 7?")
    assert result.plan_parser_recovery_path == "reprompt"
    assert result.plan_parser_attempts == 2
    assert result.plan == ["Restate the problem.", "Compute the answer."]
    assert result.final_answer == "42"


def test_json_fallback_recovery_path() -> None:
    model = ScriptedModel(
        responses=[
            _BAD_PLAN_TEXT,
            _BAD_PLAN_TEXT,
            _VALID_JSON_PLAN,
            _executor_finish_response(answer="42"),
            _confidence_response(),
        ]
    )
    agent = PlanAndSolveAgentV3(model_call=model, tool_registry={})
    result = agent.run(problem="What is 6 times 7?")
    assert result.plan_parser_recovery_path == "json_fallback"
    assert result.plan_parser_attempts == 3
    assert result.plan == ["restate the problem", "compute the answer"]
    assert result.final_answer == "42"


def test_all_failed_path() -> None:
    model = ScriptedModel(
        responses=[
            _BAD_PLAN_TEXT,
            _BAD_PLAN_TEXT,
            _BAD_PLAN_TEXT,
        ]
    )
    agent = PlanAndSolveAgentV3(model_call=model, tool_registry={})
    result = agent.run(problem="What is 6 times 7?")
    assert result.plan_parser_recovery_path == "all_failed"
    assert result.plan_parser_attempts == 3
    assert result.plan == []
    assert result.final_answer is None
    assert result.final_confidence is None


def test_robust_parse_plan_clean_returns_plan_text_verbatim() -> None:
    model = ScriptedModel(responses=[_VALID_PLAN_TEXT])
    result = _robust_parse_plan(model_call=model, problem="any")
    assert result.recovery_path == "clean"
    assert result.attempts == 1
    assert result.plan_text == _VALID_PLAN_TEXT
    assert result.plan == ["Restate the problem.", "Compute the answer."]
