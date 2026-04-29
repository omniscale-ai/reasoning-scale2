"""Scope-unaware Plan-and-Solve agent (condition B baseline).

This module adapts the LangChain Plan-and-Execute reference implementation of the Plan-and-Solve
prompting technique by Wang et al. (arXiv:2305.04091, ACL 2023). It is the canonical scope-unaware
(B) baseline for the project's A-vs-B-vs-C comparison: every trajectory record sets the
``granularity`` field to the literal string ``"unspecified"`` because the model is never told to
label its own steps with explicit granularity tags.

The trajectory record schema is intentionally identical to the schema produced by the
scope-aware (A) library ``scope_aware_react_v1`` (task t0006). Sister task t0006 must conform to
the schema defined here when its branch reaches implementation.

License attribution: the algorithmic structure (planner LLM, free-form numbered plan, sequential
executor LLM, finish-token detection) is adapted from the LangChain ``langchain_experimental``
Plan-and-Execute module, which is licensed under Apache 2.0. The PS+ prompt template is quoted
verbatim from Wang et al. (2023).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

# --------------------------------------------------------------------------------------------------
# Public constants
# --------------------------------------------------------------------------------------------------


PS_PLUS_INSTRUCTION: str = (
    "Let's first understand the problem, extract relevant variables and their corresponding "
    "numerals, and make and devise a complete plan. Then, let's carry out the plan, calculate "
    "intermediate variables (pay attention to correct numerical calculation and commonsense), "
    "solve the problem step by step, and show the answer."
)
"""Verbatim PS+ instruction from Wang et al. (2023), arXiv:2305.04091."""


PLAN_PROMPT_TEMPLATE: str = (
    "Q: {problem}\n"
    "A: " + PS_PLUS_INSTRUCTION + "\n\n"
    "Write the plan as a numbered list, one step per line, in the form '1. ...', '2. ...', "
    "etc. Then stop."
)
"""Prompt sent to the planner model to produce a free-form numbered plan."""


EXECUTE_PROMPT_TEMPLATE: str = (
    "You are executing a previously written plan to solve the following problem.\n\n"
    "Problem: {problem}\n\n"
    "Full plan:\n{plan_text}\n\n"
    "Steps completed so far:\n{completed_log}\n\n"
    "Current step ({step_number} of {total_steps}): {step_text}\n\n"
    "Available tools: {tools}\n\n"
    "Respond in exactly one of these forms:\n"
    "  Action: <tool_name> | Args: <args>\n"
    "  FINAL_ANSWER: <answer>\n"
    "  THOUGHT_ONLY: <thought>   (use when no tool call is needed for this step)\n"
)
"""Prompt sent to the executor model for each plan step."""


GRANULARITY_UNSPECIFIED: str = "unspecified"
"""Literal granularity label written to every trajectory record produced by this library."""


TRAJECTORY_RECORD_FIELDS: tuple[str, ...] = (
    "turn_index",
    "granularity",
    "thought",
    "action",
    "observation",
    "confidence",
)
"""Canonical ordered tuple of trajectory record field names.

Sister task t0006 must import this constant and assert that its scope-aware (A) library exposes
the same tuple, so the two libraries are drop-in interchangeable for a Phase 2 evaluation harness.
"""


_PLAN_LINE_RE: re.Pattern[str] = re.compile(r"^\s*\d+[\.\)]\s+(.+)$")


# --------------------------------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------------------------------


class MalformedPlanError(ValueError):
    """Raised when ``parse_plan`` cannot extract any numbered steps from the planner output."""


# --------------------------------------------------------------------------------------------------
# Data classes
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TrajectoryRecord:
    """One step of a Plan-and-Solve trajectory.

    Field order matches ``TRAJECTORY_RECORD_FIELDS`` and the schema produced by the scope-aware
    (A) library ``scope_aware_react_v1``.
    """

    turn_index: int
    granularity: str
    thought: str
    action: str
    observation: str
    confidence: float | None


@dataclass(frozen=True, slots=True)
class AgentResult:
    """Aggregate output of a single ``PlanAndSolveAgent.run`` invocation."""

    final_answer: str | None
    trajectory: list[TrajectoryRecord]
    plan: list[str]


@dataclass(slots=True)
class ScriptedModel:
    """Deterministic-test fake that returns pre-recorded responses in order.

    The ``__call__`` signature matches ``ModelCall`` so a ``ScriptedModel`` can be passed directly
    as the ``model_call`` argument to ``PlanAndSolveAgent``.
    """

    responses: list[str]
    cursor: int = field(default=0)

    def __call__(self, prompt: str) -> str:  # noqa: ARG002 — prompt is intentionally ignored
        if self.cursor >= len(self.responses):
            raise IndexError("ScriptedModel exhausted: no more pre-recorded responses")
        response = self.responses[self.cursor]
        self.cursor += 1
        return response


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
# Plan parsing
# --------------------------------------------------------------------------------------------------


def parse_plan(text: str) -> list[str]:
    """Parse a free-form numbered plan into an ordered list of step strings.

    Recognized step prefixes are ``\\d+\\.`` and ``\\d+\\)`` at line start, with arbitrary
    leading whitespace. Lines that do not match the prefix regex are appended to the previous
    step (separated by a single space) so multi-line plan items are preserved.

    Raises:
        MalformedPlanError: if no numbered steps were found in ``text``.
    """
    steps: list[str] = []
    for raw_line in text.splitlines():
        match = _PLAN_LINE_RE.match(raw_line)
        if match is not None:
            steps.append(match.group(1).strip())
            continue
        stripped = raw_line.strip()
        if stripped == "":
            continue
        if len(steps) == 0:
            # Continuation lines before any numbered step are dropped (preamble).
            continue
        steps[-1] = f"{steps[-1]} {stripped}"
    if len(steps) == 0:
        raise MalformedPlanError(
            "No numbered plan steps were found in the planner output. "
            "Expected lines starting with '1.' or '1)'."
        )
    return steps


# --------------------------------------------------------------------------------------------------
# Executor output parsing
# --------------------------------------------------------------------------------------------------


_FINAL_ANSWER_RE: re.Pattern[str] = re.compile(r"^\s*FINAL_ANSWER:\s*(.*)$", re.IGNORECASE)
_ACTION_RE: re.Pattern[str] = re.compile(
    r"^\s*Action:\s*(?P<tool>[^|]+?)\s*\|\s*Args:\s*(?P<args>.*)$",
    re.IGNORECASE,
)
_THOUGHT_ONLY_RE: re.Pattern[str] = re.compile(r"^\s*THOUGHT_ONLY:\s*(.*)$", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class _ParsedExecutorOutput:
    final_answer: str | None
    tool_name: str | None
    tool_args: str | None
    thought: str


def _parse_executor_output(raw: str) -> _ParsedExecutorOutput:
    """Parse one executor model response into structured fields.

    Lines are scanned in order. The first ``FINAL_ANSWER:``/``Action:``/``THOUGHT_ONLY:`` match
    determines the outcome; everything before it is collected as the ``thought``.
    """
    thought_lines: list[str] = []
    for line in raw.splitlines():
        if (m_final := _FINAL_ANSWER_RE.match(line)) is not None:
            return _ParsedExecutorOutput(
                final_answer=m_final.group(1).strip(),
                tool_name=None,
                tool_args=None,
                thought="\n".join(thought_lines).strip(),
            )
        if (m_action := _ACTION_RE.match(line)) is not None:
            return _ParsedExecutorOutput(
                final_answer=None,
                tool_name=m_action.group("tool").strip(),
                tool_args=m_action.group("args").strip(),
                thought="\n".join(thought_lines).strip(),
            )
        if (m_thought := _THOUGHT_ONLY_RE.match(line)) is not None:
            return _ParsedExecutorOutput(
                final_answer=None,
                tool_name=None,
                tool_args=None,
                thought=m_thought.group(1).strip(),
            )
        thought_lines.append(line)
    return _ParsedExecutorOutput(
        final_answer=None,
        tool_name=None,
        tool_args=None,
        thought="\n".join(thought_lines).strip(),
    )


# --------------------------------------------------------------------------------------------------
# Agent
# --------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class PlanAndSolveAgent:
    """Plan-and-Solve agent (scope-unaware, condition B).

    Args:
        model_call: callable that takes a prompt and returns a model response. Use
            ``ScriptedModel`` for deterministic tests.
        tool_registry: mapping of tool name to a callable returning an observation string. The
            registry may be empty for problems that need no external tools.
        max_steps: maximum number of plan steps to execute before forcibly halting. Defaults to
            ``32``.
        granularity_label: literal string written to every trajectory record's ``granularity``
            field. Defaults to ``"unspecified"`` and should not be changed for the B condition.
    """

    model_call: ModelCall
    tool_registry: ToolRegistry
    max_steps: int = 32
    granularity_label: str = GRANULARITY_UNSPECIFIED

    def run(self, problem: str) -> AgentResult:
        plan_text = self.model_call(PLAN_PROMPT_TEMPLATE.format(problem=problem))
        plan = parse_plan(plan_text)
        trajectory: list[TrajectoryRecord] = []
        completed_log_lines: list[str] = []
        final_answer: str | None = None
        tool_names: str = ", ".join(sorted(self.tool_registry.keys())) or "(none)"
        total_steps: int = len(plan)

        for index, step_text in enumerate(plan):
            if index >= self.max_steps:
                break
            executor_prompt = EXECUTE_PROMPT_TEMPLATE.format(
                problem=problem,
                plan_text=plan_text.strip(),
                completed_log=(
                    "\n".join(completed_log_lines) if len(completed_log_lines) > 0 else "(none)"
                ),
                step_number=index + 1,
                total_steps=total_steps,
                step_text=step_text,
                tools=tool_names,
            )
            executor_response = self.model_call(executor_prompt)
            parsed = _parse_executor_output(executor_response)
            observation: str
            action: str
            if parsed.final_answer is not None:
                action = "finish"
                observation = parsed.final_answer
                trajectory.append(
                    TrajectoryRecord(
                        turn_index=index,
                        granularity=self.granularity_label,
                        thought=parsed.thought,
                        action=action,
                        observation=observation,
                        confidence=None,
                    )
                )
                final_answer = parsed.final_answer
                completed_log_lines.append(
                    f"{index + 1}. {step_text} -> FINAL_ANSWER: {parsed.final_answer}"
                )
                break
            if parsed.tool_name is not None and parsed.tool_args is not None:
                action = f"{parsed.tool_name}({parsed.tool_args})"
                tool = self.tool_registry.get(parsed.tool_name)
                if tool is None:
                    observation = (
                        f"ERROR: tool '{parsed.tool_name}' not found in registry; available: "
                        f"{tool_names}"
                    )
                else:
                    try:
                        observation = tool(parsed.tool_args)
                    except Exception as exc:  # noqa: BLE001 — surface tool errors as observations
                        observation = f"ERROR: {type(exc).__name__}: {exc}"
            else:
                action = "thought_only"
                observation = ""
            trajectory.append(
                TrajectoryRecord(
                    turn_index=index,
                    granularity=self.granularity_label,
                    thought=parsed.thought,
                    action=action,
                    observation=observation,
                    confidence=None,
                )
            )
            completed_log_lines.append(
                f"{index + 1}. {step_text} -> action={action}; observation={observation}"
            )

        return AgentResult(
            final_answer=final_answer,
            trajectory=trajectory,
            plan=plan,
        )
