"""Plan-and-Solve v2 with verbalized ``final_confidence`` (Xiong et al. 2024 §3.2).

This module wraps the existing v1 Plan-and-Solve agent (``scope_unaware_planandsolve_v1`` from task
t0007) with a single post-call verbalized-confidence elicitation step. The wrapper does not edit
the v1 module; it imports v1 symbols and re-runs them unchanged. After the v1 agent has produced
a final answer, the wrapper issues a separate confidence call following the Xiong2024 §3.2
black-box calibration protocol — the model is asked to rate its own answer between 0 and 1, where
0 means "this is wrong", 0.5 means "I am unsure", and 1 means "I am completely sure".

Public API:

* :func:`parse_final_confidence` — strict regex parser, last-match wins, clamped to ``[0.0, 1.0]``.
* :class:`TrajectoryRecordV2` — six v1 fields plus ``final_confidence: float | None``.
* :class:`AgentResultV2` — ``(final_answer, trajectory, plan, final_confidence,
  final_confidence_parse_failures)``.
* :data:`CONFIDENCE_PROMPT_TEMPLATE` — verbatim Xiong2024 §3.2 phrasing with 0/0.5/1 anchors.
* :data:`CONFIDENCE_RETRY_PROMPT_TEMPLATE` — stricter retry prompt asking for a single number on
  its own line.
* :func:`elicit_final_confidence` — issue the confidence call with a single retry on parse failure.
* :class:`PlanAndSolveAgentV2` — entry point with ``run(problem) -> AgentResultV2``.

The v1 entry point ``PlanAndSolveAgent`` is left untouched and remains importable from
``tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve``.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    PlanAndSolveAgent,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    TrajectoryRecord as TrajectoryRecordV1,
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


# --------------------------------------------------------------------------------------------------
# Public constants
# --------------------------------------------------------------------------------------------------


CONFIDENCE_PROMPT_TEMPLATE: str = (
    "You just answered the following problem.\n\n"
    "Problem:\n{problem}\n\n"
    "Your final answer:\n{final_answer}\n\n"
    "Now rate how confident you are that your final answer is correct. Output a single number "
    "between 0 and 1 on its own line, where:\n"
    "  0 means you are completely sure the answer is wrong,\n"
    "  0.5 means you are completely unsure,\n"
    "  1 means you are completely sure the answer is correct.\n\n"
    "Confidence (a single number between 0 and 1):"
)
"""Verbatim Xiong2024 §3.2 verbalized-confidence prompt with 0/0.5/1 anchor language."""


CONFIDENCE_RETRY_PROMPT_TEMPLATE: str = (
    "Your previous response did not contain a parseable confidence value.\n\n"
    "Problem:\n{problem}\n\n"
    "Your final answer:\n{final_answer}\n\n"
    "Output ONLY a single decimal number between 0 and 1 on its own line. No words, no "
    "explanation, no punctuation other than the decimal point.\n\n"
    "0 means definitely wrong, 0.5 means completely unsure, 1 means definitely correct.\n\n"
    "Confidence:"
)
"""Stricter retry prompt issued once after a parse failure."""


_CONFIDENCE_NUMBER_RE: re.Pattern[str] = re.compile(r"\b(0(?:\.\d+)?|1(?:\.0+)?)\b")
"""Regex matching exactly the decimals ``0``, ``0.x``, ``1``, ``1.0+``."""


TRAJECTORY_RECORD_V2_FIELDS: tuple[str, ...] = (
    "turn_index",
    "granularity",
    "thought",
    "action",
    "observation",
    "confidence",
    "final_confidence",
)
"""Canonical ordered tuple of v2 trajectory record field names.

Six v1 fields plus the new ``final_confidence`` field.
"""


# --------------------------------------------------------------------------------------------------
# Data classes
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TrajectoryRecordV2:
    """One step of a Plan-and-Solve v2 trajectory.

    The first six fields match v1's :class:`TrajectoryRecord` exactly so consumers that read only
    the canonical six-field schema see a normal trajectory record. ``final_confidence`` carries
    the v2 verbalized-confidence value and is only populated on the *finishing* record (the record
    whose ``action == "finish"``); on all earlier records it is ``None``.
    """

    turn_index: int
    granularity: str
    thought: str
    action: str
    observation: str
    confidence: float | None
    final_confidence: float | None


@dataclass(frozen=True, slots=True)
class AgentResultV2:
    """Aggregate output of a single ``PlanAndSolveAgentV2.run`` invocation.

    ``final_confidence`` is the post-call verbalized confidence in ``[0.0, 1.0]``, or ``None`` when
    parsing failed both on the first attempt and on the retry. ``final_confidence_parse_failures``
    is the number of times the strict regex failed to extract a number from the model response
    (``0`` on first-try success, ``1`` on retry success, ``2`` on double failure).
    """

    final_answer: str | None
    trajectory: list[TrajectoryRecordV2]
    plan: list[str]
    final_confidence: float | None
    final_confidence_parse_failures: int


# --------------------------------------------------------------------------------------------------
# Confidence parsing
# --------------------------------------------------------------------------------------------------


def parse_final_confidence(text: str) -> float | None:
    """Extract a confidence value in ``[0.0, 1.0]`` from a model response.

    Strategy: scan the entire text for matches of ``\\b(0(?:\\.\\d+)?|1(?:\\.0+)?)\\b`` and take
    the *last* match (so trailing "Confidence: 0.8" wins over earlier in-prose mentions). The
    returned value is always already in ``[0.0, 1.0]`` because the regex only matches numerals in
    that closed range; we still clamp defensively to guard against future regex changes.

    Returns ``None`` when no numeric token is found.
    """
    matches = list(_CONFIDENCE_NUMBER_RE.finditer(text))
    if len(matches) == 0:
        return None
    raw_value = matches[-1].group(1)
    try:
        value = float(raw_value)
    except ValueError:
        return None
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


# --------------------------------------------------------------------------------------------------
# Confidence elicitation
# --------------------------------------------------------------------------------------------------


def elicit_final_confidence(
    *,
    model_call: ModelCall,
    problem: str,
    final_answer: str,
) -> tuple[float | None, int]:
    """Elicit a verbalized confidence value from the model with a single retry on parse failure.

    Issues the Xiong2024 §3.2 confidence prompt; if :func:`parse_final_confidence` returns
    ``None`` it issues a stricter retry prompt; if the retry also fails to parse it returns
    ``(None, 2)``. Otherwise returns ``(value, parse_failures_count)`` where the count is ``0`` on
    first-try success and ``1`` on retry success.
    """
    first_prompt = CONFIDENCE_PROMPT_TEMPLATE.format(problem=problem, final_answer=final_answer)
    first_response = model_call(first_prompt)
    first_value = parse_final_confidence(first_response)
    if first_value is not None:
        return (first_value, 0)
    retry_prompt = CONFIDENCE_RETRY_PROMPT_TEMPLATE.format(
        problem=problem, final_answer=final_answer
    )
    retry_response = model_call(retry_prompt)
    retry_value = parse_final_confidence(retry_response)
    if retry_value is not None:
        return (retry_value, 1)
    return (None, 2)


# --------------------------------------------------------------------------------------------------
# Agent
# --------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class PlanAndSolveAgentV2:
    """Plan-and-Solve v2 agent: composes v1, then issues a verbalized-confidence call.

    The wrapper runs an unmodified v1 :class:`PlanAndSolveAgent` to produce a final answer and
    trajectory, then issues a single post-call confidence prompt (with one retry) and attaches the
    parsed value to the finishing :class:`TrajectoryRecordV2`. All non-finishing records carry
    ``final_confidence=None``. The v1 agent is constructed lazily so passing a ``ScriptedModel``
    deterministic test fake still works.

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

    def run(self, problem: str) -> AgentResultV2:
        v1_agent = PlanAndSolveAgent(
            model_call=self.model_call,
            tool_registry=self.tool_registry,
            max_steps=self.max_steps,
        )
        v1_result = v1_agent.run(problem=problem)
        final_answer = v1_result.final_answer
        confidence_value: float | None
        parse_failures: int
        if final_answer is None:
            # The v1 agent never produced a finish action; do not call the confidence prompt
            # because there is nothing concrete to rate. Record this as zero parse failures.
            confidence_value = None
            parse_failures = 0
        else:
            confidence_value, parse_failures = elicit_final_confidence(
                model_call=self.model_call,
                problem=problem,
                final_answer=final_answer,
            )
        v2_trajectory = _attach_final_confidence(
            v1_records=v1_result.trajectory,
            final_confidence=confidence_value,
        )
        return AgentResultV2(
            final_answer=final_answer,
            trajectory=v2_trajectory,
            plan=v1_result.plan,
            final_confidence=confidence_value,
            final_confidence_parse_failures=parse_failures,
        )


def _attach_final_confidence(
    *,
    v1_records: list[TrajectoryRecordV1],
    final_confidence: float | None,
) -> list[TrajectoryRecordV2]:
    """Wrap v1 trajectory records as :class:`TrajectoryRecordV2`; attach value to finishing record.

    Only the *last* record whose ``action == "finish"`` carries the populated ``final_confidence``;
    all other records carry ``final_confidence=None``. If no record has ``action == "finish"``,
    the value is attached to the very last record (so the per-row JSONL extractor in the smoke
    harness can still find it via ``trajectory[-1]['final_confidence']``).
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
    "CONFIDENCE_PROMPT_TEMPLATE",
    "CONFIDENCE_RETRY_PROMPT_TEMPLATE",
    "TRAJECTORY_RECORD_V2_FIELDS",
    "AgentResultV2",
    "PlanAndSolveAgentV2",
    "TrajectoryRecordV2",
    "elicit_final_confidence",
    "parse_final_confidence",
]
