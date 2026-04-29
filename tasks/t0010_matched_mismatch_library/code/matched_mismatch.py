"""Matched-mismatch agent library (condition C of the project's A-vs-B-vs-C comparison).

This module wraps either the scope-aware ReAct delegate (t0006's `scope_aware_react_v1`) or the
scope-unaware Plan-and-Solve delegate (t0007's `scope_unaware_planandsolve_v1`) with a layer that
walks a v2-shaped annotation tree (from t0009) in canonical phase order and substitutes a
*deliberately incorrect* granularity tag at each step. The wrapper exposes two strategies:

* ``random``: pick uniformly from ``{global, subtask, atomic} \\ correct_tag``.
* ``adversarial``: pick the most distant tag (``global → atomic``, ``atomic → global``,
  ``subtask → atomic``).

The trajectory record schema is the canonical six-field schema exposed by t0007 as
``TRAJECTORY_RECORD_FIELDS``. The matched-mismatch wrapper does NOT mutate that schema. Instead it
emits :class:`MatchedMismatchRecord`, whose first six fields are identical (same names, same
order, same types) and which adds an ``extras`` mapping carrying the *correct* granularity under
the well-known key ``_correct_granularity``. Downstream evaluators that read only the canonical
six fields therefore see a normal trajectory with a "wrong" granularity tag; evaluators that opt
into ``extras`` can recover the per-step mismatch contribution.

The module imports nothing beyond the Python 3.12+ standard library and the two sister libraries
t0006 / t0007. Tests use the two libraries' :class:`ScriptedModel` helpers, so the suite runs
without API keys or network access.
"""

from __future__ import annotations

import random
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from typing import Any, Final, Literal, assert_never

from tasks.t0006_scope_aware_react_library.code.constants import (
    GRANULARITY_ATOMIC,
    GRANULARITY_GLOBAL,
    GRANULARITY_SUBTASK,
)
from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    Action,
    MalformedActionError,
)
from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    _parse_model_output as _parse_react_output,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    EXECUTE_PROMPT_TEMPLATE,
    PLAN_PROMPT_TEMPLATE,
    TRAJECTORY_RECORD_FIELDS,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    _parse_executor_output as _parse_planandsolve_output,
)

# --------------------------------------------------------------------------------------------------
# Public constants
# --------------------------------------------------------------------------------------------------


GRANULARITY_VALUES: Final[tuple[str, str, str]] = (
    GRANULARITY_GLOBAL,
    GRANULARITY_SUBTASK,
    GRANULARITY_ATOMIC,
)
"""Canonical ordered tuple of allowed granularity tags."""


ADVERSARIAL_MAP: Final[dict[str, str]] = {
    GRANULARITY_GLOBAL: GRANULARITY_ATOMIC,
    GRANULARITY_ATOMIC: GRANULARITY_GLOBAL,
    GRANULARITY_SUBTASK: GRANULARITY_ATOMIC,
}
"""Most-distant-tag map.

`subtask` is equidistant from `global` and `atomic`; we choose `atomic` consistently with the
project's planning literature where the global-vs-atomic axis is the primary variable. Pin this
choice via :func:`pick_mismatch_tag` and :func:`test_adversarial_strategy_correctness` so a future
change is detected immediately.
"""


CORRECT_GRANULARITY_EXTRAS_KEY: Final[str] = "_correct_granularity"
"""Well-known key under which :class:`MatchedMismatchRecord` ``extras`` carries the correct tag."""


_TRAJECTORY_FIELDS_EXPECTED: Final[tuple[str, ...]] = (
    "turn_index",
    "granularity",
    "thought",
    "action",
    "observation",
    "confidence",
)
assert TRAJECTORY_RECORD_FIELDS == _TRAJECTORY_FIELDS_EXPECTED, (
    "matched_mismatch_v1 requires t0007's TRAJECTORY_RECORD_FIELDS to be exactly "
    f"{_TRAJECTORY_FIELDS_EXPECTED}, got {TRAJECTORY_RECORD_FIELDS!r}. "
    "If t0007 changes the schema, this library must be coordinated with that change."
)


# --------------------------------------------------------------------------------------------------
# Public type aliases
# --------------------------------------------------------------------------------------------------


type MismatchStrategy = Literal["random", "adversarial"]
"""How a wrong granularity tag is chosen at each step."""


type Delegate = Literal["scope_aware_react", "scope_unaware_planandsolve"]
"""Which sister library's prompt format / output parser to use for each phase."""


type Granularity = Literal["global", "subtask", "atomic"]
"""Allowed granularity values; identical to t0006's :data:`Granularity`."""


type Tool = Any
"""Tool callables; left untyped so both t0006-style and t0007-style tool registries pass through."""


type ToolRegistry = Mapping[str, Tool]
"""Mapping of tool name to a tool callable."""


type ModelCall = Any
"""Callable that takes a prompt string and returns a model-response string."""


# --------------------------------------------------------------------------------------------------
# Public dataclasses
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Phase:
    """One step of the canonical phase-ordered walk over a v2 annotation tree.

    ``kind`` is one of ``{"global", "subtask", "atomic", "global_atomic"}`` and identifies the
    structural slot the step occupies in the annotation. ``correct_tag`` is the granularity tag
    that *would* be used by a matched-condition agent; the matched-mismatch wrapper substitutes a
    wrong tag for logging purposes. ``payload`` is the textual content drawn from the annotation
    (the global summary, the subtask description, or the atomic step description).
    """

    kind: str
    correct_tag: str
    payload: str


@dataclass(frozen=True, slots=True)
class MatchedMismatchRecord:
    """One emitted trajectory record.

    The first six fields match :data:`TRAJECTORY_RECORD_FIELDS` exactly (same names, same order)
    so consumers that read only the canonical schema see a normal trajectory record. ``extras``
    carries the per-step correct tag under :data:`CORRECT_GRANULARITY_EXTRAS_KEY` and may carry
    additional debugging information.
    """

    turn_index: int
    granularity: str
    thought: str
    action: str
    observation: str
    confidence: float | None
    extras: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AgentRunResult:
    """Aggregate output of one :meth:`MatchedMismatchAgent.run` invocation."""

    final_answer: str | None
    trajectory: list[MatchedMismatchRecord]
    phases: list[Phase]


# --------------------------------------------------------------------------------------------------
# Phase walk and tag picker
# --------------------------------------------------------------------------------------------------


_GLOBAL_KEY: Final[str] = "global"
_SUBTASKS_KEY: Final[str] = "subtasks"
_SUBTASK_KEY: Final[str] = "subtask"
_ATOMICS_KEY: Final[str] = "atomics"
_GLOBAL_ATOMICS_KEY: Final[str] = "global_atomics"
_HIERARCHY_KEY: Final[str] = "hierarchy"


def _resolve_hierarchy(*, annotation: Mapping[str, Any]) -> Mapping[str, Any]:
    """Accept either the full v2 annotation row or the inner ``hierarchy`` dict directly."""
    if _HIERARCHY_KEY in annotation:
        inner: object = annotation[_HIERARCHY_KEY]
        if not isinstance(inner, Mapping):
            raise TypeError(f"`hierarchy` must be a Mapping, got {type(inner).__name__}: {inner!r}")
        return inner
    return annotation


def iter_phases(annotation: Mapping[str, Any]) -> Iterator[Phase]:
    """Yield :class:`Phase` objects in canonical phase order.

    The canonical walk is:

    1. ``global`` (one step, ``kind="global"``, ``correct_tag="global"``).
    2. For each subtask in declared order:

       a. The subtask itself (``kind="subtask"``, ``correct_tag="subtask"``).
       b. Each of its atomics in declared order (``kind="atomic"``,
          ``correct_tag="atomic"``).

    3. Each ``global_atomic`` in declared order (``kind="global_atomic"``,
       ``correct_tag="atomic"`` — cross-cutting atomics are still atomic for the
       mismatch policy).

    Missing optional slots (no ``global``, empty ``subtasks``, missing ``global_atomics``) are
    skipped silently — this matches t0009's documented permissive shape.
    """
    hierarchy: Mapping[str, Any] = _resolve_hierarchy(annotation=annotation)
    global_text_obj: object = hierarchy.get(_GLOBAL_KEY)
    if isinstance(global_text_obj, str) and len(global_text_obj) > 0:
        yield Phase(
            kind=_GLOBAL_KEY,
            correct_tag=GRANULARITY_GLOBAL,
            payload=global_text_obj,
        )
    subtasks_obj: object = hierarchy.get(_SUBTASKS_KEY, [])
    if isinstance(subtasks_obj, list):
        for subtask_entry in subtasks_obj:
            if not isinstance(subtask_entry, Mapping):
                continue
            subtask_text_obj: object = subtask_entry.get(_SUBTASK_KEY)
            if isinstance(subtask_text_obj, str) and len(subtask_text_obj) > 0:
                yield Phase(
                    kind=_SUBTASK_KEY,
                    correct_tag=GRANULARITY_SUBTASK,
                    payload=subtask_text_obj,
                )
            atomics_obj: object = subtask_entry.get(_ATOMICS_KEY, [])
            if isinstance(atomics_obj, list):
                for atomic_text in atomics_obj:
                    if isinstance(atomic_text, str) and len(atomic_text) > 0:
                        yield Phase(
                            kind="atomic",
                            correct_tag=GRANULARITY_ATOMIC,
                            payload=atomic_text,
                        )
    global_atomics_obj: object = hierarchy.get(_GLOBAL_ATOMICS_KEY, [])
    if isinstance(global_atomics_obj, list):
        for atomic_text in global_atomics_obj:
            if isinstance(atomic_text, str) and len(atomic_text) > 0:
                yield Phase(
                    kind="global_atomic",
                    correct_tag=GRANULARITY_ATOMIC,
                    payload=atomic_text,
                )


def pick_mismatch_tag(
    correct_tag: str,
    *,
    strategy: MismatchStrategy,
    rng: random.Random,
) -> str:
    """Return a granularity tag that is guaranteed to differ from ``correct_tag``.

    For ``strategy="random"`` the result is sampled uniformly from
    ``GRANULARITY_VALUES \\ {correct_tag}``. For ``strategy="adversarial"`` the result is the
    fixed entry from :data:`ADVERSARIAL_MAP`.

    Raises:
        ValueError: if ``correct_tag`` is not a member of :data:`GRANULARITY_VALUES` or if
            ``strategy`` is not one of the documented literals.
    """
    if correct_tag not in GRANULARITY_VALUES:
        raise ValueError(f"correct_tag must be one of {GRANULARITY_VALUES}, got {correct_tag!r}.")
    if strategy == "random":
        wrong_choices: list[str] = [tag for tag in GRANULARITY_VALUES if tag != correct_tag]
        assert len(wrong_choices) == 2, "exactly two wrong tags must remain"
        return rng.choice(wrong_choices)
    if strategy == "adversarial":
        return ADVERSARIAL_MAP[correct_tag]
    assert_never(strategy)


# --------------------------------------------------------------------------------------------------
# Per-phase prompt + parsing dispatch
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _ParsedPhaseResult:
    """Internal: one phase's parsed model output before granularity substitution."""

    thought: str
    action: str
    observation: str
    confidence: float | None
    final_answer: str | None


def _build_react_phase_prompt(
    *,
    problem: str,
    correct_tag: str,
    phase_kind: str,
    payload: str,
    history: list[MatchedMismatchRecord],
    tool_names: str,
) -> str:
    """ReAct-style prompt for one phase. The prompt itself uses the *correct* tag — only the

    logged record carries the wrong tag.
    """
    history_lines: list[str] = []
    for record in history:
        history_lines.append(f"Thought: <{record.granularity}> {record.thought}")
        history_lines.append(f"Action: {record.action}")
        history_lines.append(f"Observation: {record.observation}")
    transcript: str = "\n".join(history_lines) + ("\n" if history_lines else "")
    return (
        f"You are a scope-aware ReAct agent. The current phase is {phase_kind!r} at granularity "
        f"{correct_tag!r}. On every turn emit exactly one block of three lines:\n"
        f"  Thought: <{correct_tag}> <free-form reasoning at the {correct_tag} level>\n"
        '  Action: {"name": "<tool_name>", "args": {...}}\n'
        "  Confidence: <integer 0-100>\n\n"
        f"Problem: {problem}\n"
        f"Phase payload: {payload}\n"
        f"Available tools: {tool_names}\n\n"
        f"{transcript}"
        "Continue with the next Thought / Action / Confidence block.\n"
    )


def _build_planandsolve_phase_prompt(
    *,
    problem: str,
    correct_tag: str,
    phase_kind: str,
    payload: str,
    completed_log_lines: list[str],
    tool_names: str,
    step_number: int,
    total_steps: int,
) -> str:
    """Plan-and-Solve-style prompt for one phase.

    Reuses t0007's ``PLAN_PROMPT_TEMPLATE`` / ``EXECUTE_PROMPT_TEMPLATE`` shape but specialises
    the executor prompt for one phase at a time — the wrapper itself drives the v2-hierarchy walk
    in lieu of calling the delegate's planner.
    """
    completed_log: str = "\n".join(completed_log_lines) if completed_log_lines else "(none)"
    return EXECUTE_PROMPT_TEMPLATE.format(
        problem=problem,
        plan_text=PLAN_PROMPT_TEMPLATE.format(problem=problem),
        completed_log=completed_log,
        step_number=step_number,
        total_steps=total_steps,
        step_text=f"[{phase_kind}@{correct_tag}] {payload}",
        tools=tool_names,
    )


def _dispatch_react_action(*, action: Action, tool_registry: ToolRegistry) -> tuple[str, str]:
    """Run a parsed ReAct :class:`Action` against the tool registry; return ``(action_str, obs)``.

    Mirrors t0006's :class:`ScopeAwareReactAgent._dispatch_action` but flattens the action to a
    single string so it fits the canonical six-field schema, where ``action`` is ``str``.
    """
    name: str = action.name
    args_repr: str = ",".join(f"{k}={v}" for k, v in action.args.items())
    if name == "Finish":
        answer_obj: object = action.args.get("answer", "")
        return ("finish", str(answer_obj))
    tool: Any = tool_registry.get(name)
    if tool is None:
        return (
            f"{name}({args_repr})",
            f"ERROR: tool '{name}' not found in registry",
        )
    try:
        observation_obj: Any = tool(**action.args)
    except Exception as exc:  # noqa: BLE001 — surface as observation, do not abort
        return (
            f"{name}({args_repr})",
            f"ERROR: {type(exc).__name__}: {exc}",
        )
    return (f"{name}({args_repr})", str(observation_obj))


def _run_react_phase(
    *,
    problem: str,
    phase: Phase,
    history: list[MatchedMismatchRecord],
    model_call: ModelCall,
    tool_registry: ToolRegistry,
) -> _ParsedPhaseResult:
    tool_names: str = ", ".join(sorted(tool_registry.keys())) or "(none)"
    prompt: str = _build_react_phase_prompt(
        problem=problem,
        correct_tag=phase.correct_tag,
        phase_kind=phase.kind,
        payload=phase.payload,
        history=history,
        tool_names=tool_names,
    )
    raw: str = model_call(prompt)
    try:
        parsed = _parse_react_output(raw=raw)
    except MalformedActionError as exc:
        return _ParsedPhaseResult(
            thought="",
            action="<unparsed>",
            observation=f"<parse_error>:{exc}",
            confidence=None,
            final_answer=None,
        )
    if parsed.action.name == "Finish":
        action_str, observation = _dispatch_react_action(
            action=parsed.action,
            tool_registry=tool_registry,
        )
        return _ParsedPhaseResult(
            thought=parsed.thought,
            action=action_str,
            observation=observation,
            confidence=parsed.confidence,
            final_answer=observation,
        )
    action_str, observation = _dispatch_react_action(
        action=parsed.action,
        tool_registry=tool_registry,
    )
    return _ParsedPhaseResult(
        thought=parsed.thought,
        action=action_str,
        observation=observation,
        confidence=parsed.confidence,
        final_answer=None,
    )


def _run_planandsolve_phase(
    *,
    problem: str,
    phase: Phase,
    completed_log_lines: list[str],
    step_number: int,
    total_steps: int,
    model_call: ModelCall,
    tool_registry: ToolRegistry,
) -> _ParsedPhaseResult:
    tool_names: str = ", ".join(sorted(tool_registry.keys())) or "(none)"
    prompt: str = _build_planandsolve_phase_prompt(
        problem=problem,
        correct_tag=phase.correct_tag,
        phase_kind=phase.kind,
        payload=phase.payload,
        completed_log_lines=completed_log_lines,
        tool_names=tool_names,
        step_number=step_number,
        total_steps=total_steps,
    )
    raw: str = model_call(prompt)
    parsed = _parse_planandsolve_output(raw)
    if parsed.final_answer is not None:
        return _ParsedPhaseResult(
            thought=parsed.thought,
            action="finish",
            observation=parsed.final_answer,
            confidence=None,
            final_answer=parsed.final_answer,
        )
    if parsed.tool_name is not None and parsed.tool_args is not None:
        tool: Any = tool_registry.get(parsed.tool_name)
        action_str: str = f"{parsed.tool_name}({parsed.tool_args})"
        if tool is None:
            return _ParsedPhaseResult(
                thought=parsed.thought,
                action=action_str,
                observation=(
                    f"ERROR: tool '{parsed.tool_name}' not found in registry; "
                    f"available: {tool_names}"
                ),
                confidence=None,
                final_answer=None,
            )
        try:
            observation_obj: Any = tool(parsed.tool_args)
        except Exception as exc:  # noqa: BLE001 — surface as observation, do not abort
            return _ParsedPhaseResult(
                thought=parsed.thought,
                action=action_str,
                observation=f"ERROR: {type(exc).__name__}: {exc}",
                confidence=None,
                final_answer=None,
            )
        return _ParsedPhaseResult(
            thought=parsed.thought,
            action=action_str,
            observation=str(observation_obj),
            confidence=None,
            final_answer=None,
        )
    return _ParsedPhaseResult(
        thought=parsed.thought,
        action="thought_only",
        observation="",
        confidence=None,
        final_answer=None,
    )


# --------------------------------------------------------------------------------------------------
# Agent
# --------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class MatchedMismatchAgent:
    """Condition-C agent: walks a v2 hierarchy and logs deliberately wrong granularity tags.

    Args:
        model_call: callable that takes a prompt string and returns a model response. For
            deterministic tests, pass an instance of t0006's or t0007's ``ScriptedModel``.
        tool_registry: mapping of tool name to a callable. The callable signature differs between
            delegates: t0006's ReAct delegate calls ``tool(**action.args)``; t0007's Plan-and-Solve
            delegate calls ``tool(args_str)``. Pick a registry shape compatible with the chosen
            delegate.
        delegate: which sister library's prompt format and output parser to use for each phase.
        mismatch_strategy: how a wrong granularity tag is chosen at each step.
        seed: seed for the internal :class:`random.Random` used by ``mismatch_strategy="random"``.
            Determinism is per-run: two runs with the same ``seed`` produce identical wrong-tag
            sequences.
    """

    model_call: ModelCall
    tool_registry: ToolRegistry
    delegate: Delegate
    mismatch_strategy: MismatchStrategy
    seed: int = 0

    def run(
        self,
        *,
        problem: str,
        annotation: Mapping[str, Any],
    ) -> AgentRunResult:
        """Drive one matched-mismatch run over the v2 ``annotation`` tree.

        Walks :func:`iter_phases` once; per phase, dispatches one model call via the chosen
        delegate's prompt format / parser, substitutes the wrong granularity tag, and emits one
        :class:`MatchedMismatchRecord`. Halts early when a phase emits a final answer.
        """
        if self.mismatch_strategy not in ("random", "adversarial"):
            raise ValueError(
                f"mismatch_strategy must be one of ('random', 'adversarial'), "
                f"got {self.mismatch_strategy!r}."
            )
        if self.delegate not in ("scope_aware_react", "scope_unaware_planandsolve"):
            raise ValueError(
                f"delegate must be one of ('scope_aware_react', 'scope_unaware_planandsolve'), "
                f"got {self.delegate!r}."
            )
        rng: random.Random = random.Random(self.seed)
        phases: list[Phase] = list(iter_phases(annotation))
        trajectory: list[MatchedMismatchRecord] = []
        completed_log_lines: list[str] = []
        final_answer: str | None = None
        total_steps: int = len(phases)

        for index, phase in enumerate(phases):
            phase_result: _ParsedPhaseResult
            if self.delegate == "scope_aware_react":
                phase_result = _run_react_phase(
                    problem=problem,
                    phase=phase,
                    history=trajectory,
                    model_call=self.model_call,
                    tool_registry=self.tool_registry,
                )
            elif self.delegate == "scope_unaware_planandsolve":
                phase_result = _run_planandsolve_phase(
                    problem=problem,
                    phase=phase,
                    completed_log_lines=completed_log_lines,
                    step_number=index + 1,
                    total_steps=total_steps,
                    model_call=self.model_call,
                    tool_registry=self.tool_registry,
                )
            else:
                assert_never(self.delegate)
            wrong_tag: str = pick_mismatch_tag(
                phase.correct_tag,
                strategy=self.mismatch_strategy,
                rng=rng,
            )
            extras: dict[str, str] = {
                CORRECT_GRANULARITY_EXTRAS_KEY: phase.correct_tag,
                "phase_kind": phase.kind,
                "delegate": self.delegate,
                "mismatch_strategy": self.mismatch_strategy,
            }
            record: MatchedMismatchRecord = MatchedMismatchRecord(
                turn_index=index,
                granularity=wrong_tag,
                thought=phase_result.thought,
                action=phase_result.action,
                observation=phase_result.observation,
                confidence=phase_result.confidence,
                extras=extras,
            )
            trajectory.append(record)
            completed_log_lines.append(
                f"{index + 1}. [{phase.kind}@{phase.correct_tag}->{wrong_tag}] "
                f"action={phase_result.action}; observation={phase_result.observation}"
            )
            if phase_result.final_answer is not None:
                final_answer = phase_result.final_answer
                break

        return AgentRunResult(
            final_answer=final_answer,
            trajectory=trajectory,
            phases=phases,
        )


# --------------------------------------------------------------------------------------------------
# Re-export for type-checker convenience
# --------------------------------------------------------------------------------------------------


__all__: Final[list[str]] = [
    "ADVERSARIAL_MAP",
    "AgentRunResult",
    "CORRECT_GRANULARITY_EXTRAS_KEY",
    "Delegate",
    "GRANULARITY_VALUES",
    "Granularity",
    "MatchedMismatchAgent",
    "MatchedMismatchRecord",
    "MismatchStrategy",
    "Phase",
    "TRAJECTORY_RECORD_FIELDS",
    "iter_phases",
    "pick_mismatch_tag",
]
