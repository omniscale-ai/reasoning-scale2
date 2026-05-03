"""Plan-and-Solve v3: fault-tolerant plan parser fork of v2 (S-0026-01).

This module wraps the existing v2 Plan-and-Solve agent (``planandsolve_v2`` from task t0021) with a
robust plan-parsing path. The only behavioural change relative to v2 is the planner step: when the
v1 ``parse_plan`` raises :class:`MalformedPlanError`, v3 issues up to two recovery calls before
giving up.

The fallback chain is bounded:

1. **First attempt** — call the model with the standard ``PLAN_PROMPT_TEMPLATE`` and parse with the
   v1 numbered-list regex. If :func:`parse_plan` succeeds, we are done.
2. **Re-prompt attempt** — if parsing fails, call the model again with an explicit error message
   that quotes the bad output and re-states the strict format requirement
   (:data:`REPROMPT_PLAN_PROMPT_TEMPLATE`). Parse again with the same regex.
3. **JSON-fallback attempt** — if the re-prompt also fails, call the model a third time with a
   schema prompt that requires a single JSON array of step strings
   (:data:`JSON_PLAN_PROMPT_TEMPLATE`). Extract the first JSON array from the response, validate
   that all elements are non-empty strings, and use that as the plan. The trajectory records the
   parser-recovery path that succeeded.
4. If all three attempts fail, the agent re-raises :class:`MalformedPlanError` as today, so the
   caller can still measure the residual parser-failure rate.

All other v2 behaviour (verbalized confidence, trajectory schema, decision-log shape) is preserved
unchanged. The v3 trajectory record is identical to :class:`TrajectoryRecordV2`. The v3 agent
result adds two diagnostic counters (``plan_parser_recovery_path``, ``plan_parser_attempts``) so the
task harness can measure how often each recovery path fired.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Final, Literal

from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    GRANULARITY_UNSPECIFIED,
    PLAN_PROMPT_TEMPLATE,
    MalformedPlanError,
    PlanAndSolveAgent,
    parse_plan,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    AgentResult as AgentResultV1,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    TrajectoryRecord as TrajectoryRecordV1,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    TrajectoryRecordV2,
    elicit_final_confidence,
)

# --------------------------------------------------------------------------------------------------
# Type aliases
# --------------------------------------------------------------------------------------------------


type ModelCall = Callable[[str], str]
"""Callable that takes a prompt and returns a model response."""


type Tool = Callable[[str], str]
"""Callable that takes an argument string and returns an observation string."""


type ToolRegistry = dict[str, Tool]
"""Mapping of tool name to a callable returning an observation string."""


type ParserRecoveryPath = Literal["clean", "reprompt", "json_fallback", "all_failed"]


# --------------------------------------------------------------------------------------------------
# Public constants
# --------------------------------------------------------------------------------------------------


REPROMPT_PLAN_PROMPT_TEMPLATE: Final[str] = (
    "Your previous response did not contain a parseable numbered plan.\n\n"
    "Your previous response (truncated):\n{bad_output}\n\n"
    "Problem:\n{problem}\n\n"
    "Write the plan again. The required format is a numbered list, one step per line, "
    "starting with '1.', '2.', '3.', etc. Each step must be on its own line and start with the "
    "number followed by a period or close-paren. Do not include any preamble or commentary "
    "before step '1.'. After the last step, stop.\n\n"
    "Example of the required format:\n"
    "1. Restate the problem.\n"
    "2. Identify the unknowns.\n"
    "3. Compute the answer.\n\n"
    "Now write the plan:"
)
"""Re-prompt sent to the planner when the first response fails to parse."""


JSON_PLAN_PROMPT_TEMPLATE: Final[str] = (
    "Output a plan as JSON. Output ONLY a JSON object with a single key 'steps' whose value is "
    "an array of non-empty step strings. Do not output anything else.\n\n"
    "Problem:\n{problem}\n\n"
    "Required output format (this exact JSON shape, with your own steps):\n"
    '{{"steps": ["restate the problem", "identify unknowns", "compute the answer"]}}\n\n'
    "Now output the JSON object for this problem:"
)
"""Structured-output fallback prompt requiring a JSON object with a 'steps' array."""


_BAD_OUTPUT_TRUNCATE_LIMIT: Final[int] = 600
"""Maximum number of characters of the bad output to quote back in the re-prompt."""


_PARSER_PATH_CLEAN: Final[str] = "clean"
_PARSER_PATH_REPROMPT: Final[str] = "reprompt"
_PARSER_PATH_JSON_FALLBACK: Final[str] = "json_fallback"
_PARSER_PATH_ALL_FAILED: Final[str] = "all_failed"


_JSON_OBJECT_RE: Final[re.Pattern[str]] = re.compile(r"\{.*\}", re.DOTALL)
"""Greedy match for a JSON object anywhere in the response."""


_JSON_ARRAY_RE: Final[re.Pattern[str]] = re.compile(r"\[.*\]", re.DOTALL)
"""Greedy match for a JSON array anywhere in the response (fallback)."""


# --------------------------------------------------------------------------------------------------
# Data classes
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AgentResultV3:
    """Aggregate output of a single ``PlanAndSolveAgentV3.run`` invocation.

    ``plan_parser_recovery_path`` is one of:
    * ``"clean"`` — the first numbered-list parse succeeded.
    * ``"reprompt"`` — the first parse failed; the re-prompt parse succeeded.
    * ``"json_fallback"`` — both prior parses failed; the JSON-fallback parse succeeded.
    * ``"all_failed"`` — all three attempts failed and ``MalformedPlanError`` was re-raised.

    ``plan_parser_attempts`` counts the number of model calls spent on planning (1, 2, or 3).
    """

    final_answer: str | None
    trajectory: list[TrajectoryRecordV2]
    plan: list[str]
    final_confidence: float | None
    final_confidence_parse_failures: int
    plan_parser_recovery_path: str
    plan_parser_attempts: int


# --------------------------------------------------------------------------------------------------
# Plan-parser fault tolerance
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _RobustPlanResult:
    plan_text: str
    plan: list[str]
    recovery_path: str
    attempts: int


def _try_parse_json_plan(*, raw: str) -> list[str] | None:
    """Extract a plan from a JSON-mode response. Accepts ``{"steps": [...]}`` or a bare ``[...]``.

    Returns ``None`` when no parseable JSON plan can be extracted.
    """
    obj_match = _JSON_OBJECT_RE.search(raw)
    candidates: list[str] = []
    if obj_match is not None:
        candidates.append(obj_match.group(0))
    arr_match = _JSON_ARRAY_RE.search(raw)
    if arr_match is not None:
        candidates.append(arr_match.group(0))
    for snippet in candidates:
        try:
            parsed = json.loads(snippet)
        except json.JSONDecodeError:
            continue
        steps_obj: object
        if isinstance(parsed, dict) and "steps" in parsed:
            steps_obj = parsed["steps"]
        elif isinstance(parsed, list):
            steps_obj = parsed
        else:
            continue
        if not isinstance(steps_obj, list):
            continue
        cleaned: list[str] = []
        for step in steps_obj:
            if not isinstance(step, str):
                cleaned = []
                break
            stripped = step.strip()
            if len(stripped) == 0:
                cleaned = []
                break
            cleaned.append(stripped)
        if len(cleaned) > 0:
            return cleaned
    return None


def _robust_parse_plan(
    *,
    model_call: ModelCall,
    problem: str,
) -> _RobustPlanResult:
    """Issue planner calls with up to two recovery attempts; raise ``MalformedPlanError`` on triple.

    Sequence:
    1. Standard plan prompt + numbered-list parse.
    2. On failure: re-prompt with explicit error feedback + numbered-list parse.
    3. On failure: JSON-fallback prompt + JSON-array parse.

    Returns the first successful :class:`_RobustPlanResult`. If all three attempts fail, raises
    :class:`MalformedPlanError`. The ``plan_text`` field on the returned result is the raw model
    response from the *successful* call (so the executor sees the same plan_text it would have
    seen in v1/v2 when the first attempt succeeds).
    """
    # Attempt 1 — clean path.
    first_response = model_call(PLAN_PROMPT_TEMPLATE.format(problem=problem))
    try:
        plan = parse_plan(first_response)
    except MalformedPlanError:
        pass
    else:
        return _RobustPlanResult(
            plan_text=first_response,
            plan=plan,
            recovery_path=_PARSER_PATH_CLEAN,
            attempts=1,
        )

    # Attempt 2 — re-prompt with explicit error feedback.
    bad_excerpt = first_response.strip()[:_BAD_OUTPUT_TRUNCATE_LIMIT]
    reprompt_response = model_call(
        REPROMPT_PLAN_PROMPT_TEMPLATE.format(bad_output=bad_excerpt, problem=problem)
    )
    try:
        plan = parse_plan(reprompt_response)
    except MalformedPlanError:
        pass
    else:
        return _RobustPlanResult(
            plan_text=reprompt_response,
            plan=plan,
            recovery_path=_PARSER_PATH_REPROMPT,
            attempts=2,
        )

    # Attempt 3 — JSON-fallback.
    json_response = model_call(JSON_PLAN_PROMPT_TEMPLATE.format(problem=problem))
    json_plan = _try_parse_json_plan(raw=json_response)
    if json_plan is not None:
        # Synthesize a plan_text in the standard numbered-list format so the executor prompt
        # downstream sees the same shape it expects.
        synthesized = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(json_plan))
        return _RobustPlanResult(
            plan_text=synthesized,
            plan=json_plan,
            recovery_path=_PARSER_PATH_JSON_FALLBACK,
            attempts=3,
        )
    raise MalformedPlanError(
        "Plan parser failed after one re-prompt and one JSON-fallback attempt."
    )


# --------------------------------------------------------------------------------------------------
# Agent
# --------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class PlanAndSolveAgentV3:
    """Plan-and-Solve v3 agent: v2 with a fault-tolerant plan parser.

    The agent first issues a robust plan call (standard / re-prompt / JSON-fallback), then runs the
    v1 executor loop unchanged with the recovered plan, then issues the v2 verbalized-confidence
    call. The trajectory schema and final-confidence semantics are identical to v2; only the
    planning prefix is different.

    Args:
        model_call: callable taking a prompt and returning a model response string.
        tool_registry: mapping of tool name to a callable returning an observation string. May be
            empty for problems that need no external tools.
        max_steps: maximum number of plan steps to execute before forcibly halting. Defaults to
            ``32`` (matches v1).
    """

    model_call: ModelCall
    tool_registry: ToolRegistry = field(default_factory=dict)
    max_steps: int = 32

    def run(self, problem: str) -> AgentResultV3:
        try:
            plan_result = _robust_parse_plan(model_call=self.model_call, problem=problem)
        except MalformedPlanError:
            return AgentResultV3(
                final_answer=None,
                trajectory=[],
                plan=[],
                final_confidence=None,
                final_confidence_parse_failures=0,
                plan_parser_recovery_path=_PARSER_PATH_ALL_FAILED,
                plan_parser_attempts=3,
            )

        v1_agent = PlanAndSolveAgent(
            model_call=self.model_call,
            tool_registry=self.tool_registry,
            max_steps=self.max_steps,
            granularity_label=GRANULARITY_UNSPECIFIED,
        )
        v1_result = _execute_with_recovered_plan(
            v1_agent=v1_agent,
            problem=problem,
            plan_text=plan_result.plan_text,
            plan=plan_result.plan,
        )

        final_answer = v1_result.final_answer
        confidence_value: float | None
        parse_failures: int
        if final_answer is None:
            confidence_value = None
            parse_failures = 0
        else:
            confidence_value, parse_failures = elicit_final_confidence(
                model_call=self.model_call,
                problem=problem,
                final_answer=final_answer,
            )
        v3_trajectory = _attach_final_confidence_v3(
            v1_records=v1_result.trajectory,
            final_confidence=confidence_value,
        )
        return AgentResultV3(
            final_answer=final_answer,
            trajectory=v3_trajectory,
            plan=v1_result.plan,
            final_confidence=confidence_value,
            final_confidence_parse_failures=parse_failures,
            plan_parser_recovery_path=plan_result.recovery_path,
            plan_parser_attempts=plan_result.attempts,
        )


def _execute_with_recovered_plan(
    *,
    v1_agent: PlanAndSolveAgent,
    problem: str,
    plan_text: str,
    plan: list[str],
) -> AgentResultV1:
    """Drive the v1 executor loop using a pre-parsed plan, bypassing v1's planner call.

    The v1 agent's ``run`` method always calls the planner itself, so we cannot reuse it directly
    when the v3 robust parser already produced the plan. Instead, we monkey-patch the ``model_call``
    on a temporary local v1 agent so the first call returns the recovered ``plan_text`` and
    subsequent calls fall through to the original model. This avoids forking the entire v1 loop.
    """
    underlying = v1_agent.model_call
    served = {"served": False}

    def _patched_model_call(prompt: str) -> str:
        # The first call inside v1.run is the planner call; serve our recovered plan_text.
        if not served["served"]:
            served["served"] = True
            return plan_text
        return underlying(prompt)

    v1_agent.model_call = _patched_model_call
    try:
        v1_result = v1_agent.run(problem=problem)
    finally:
        v1_agent.model_call = underlying
    # Replace the parsed plan with our authoritative one (they must already be identical, but this
    # guards against any post-parse normalization drift in v1.parse_plan).
    return AgentResultV1(
        final_answer=v1_result.final_answer,
        trajectory=v1_result.trajectory,
        plan=plan,
    )


def _attach_final_confidence_v3(
    *,
    v1_records: list[TrajectoryRecordV1],
    final_confidence: float | None,
) -> list[TrajectoryRecordV2]:
    """Wrap v1 trajectory records as :class:`TrajectoryRecordV2`; attach confidence to finishing.

    Same semantics as v2's ``_attach_final_confidence`` (kept private inside v2). Reproduced here
    so v3 has no private-symbol dependency on v2.
    """
    finish_indices = [i for i, r in enumerate(v1_records) if r.action == "finish"]
    target_index: int | None
    if len(finish_indices) > 0:
        target_index = finish_indices[-1]
    elif len(v1_records) > 0:
        target_index = len(v1_records) - 1
    else:
        target_index = None
    out: list[TrajectoryRecordV2] = []
    for i, record in enumerate(v1_records):
        attached: float | None = final_confidence if i == target_index else None
        out.append(
            TrajectoryRecordV2(
                turn_index=record.turn_index,
                granularity=record.granularity,
                thought=record.thought,
                action=record.action,
                observation=record.observation,
                confidence=record.confidence,
                final_confidence=attached,
            )
        )
    return out


# --------------------------------------------------------------------------------------------------
# Re-exports
# --------------------------------------------------------------------------------------------------


__all__ = [
    "JSON_PLAN_PROMPT_TEMPLATE",
    "REPROMPT_PLAN_PROMPT_TEMPLATE",
    "AgentResultV3",
    "PlanAndSolveAgentV3",
    "_robust_parse_plan",
]
