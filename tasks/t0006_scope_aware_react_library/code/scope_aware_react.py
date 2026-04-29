"""Scope-aware ReAct agent (condition A of the granularity-conditioning project).

This module implements the canonical ReAct Thought / Action / Observation loop ([Yao2022])
extended with an explicit per-turn granularity tag drawn from
`{global, subtask, atomic}`. Every Thought emission is prefixed with the active tag, and every
turn writes a structured record to a JSONL trajectory file. The trajectory schema is the contract
between this library and the sister Plan-and-Solve library
(`t0007_scope_unaware_planandsolve_library`).

The library is intentionally framework-free: the only runtime dependency is the Python standard
library. Callers inject a `model_call` callable (typically wrapping an OpenAI / Anthropic /
local-model API) and a tool registry. For deterministic unit tests, a `ScriptedModel` helper is
provided that replays pre-recorded model outputs without making any live API call.

Prompt template adapted from the LangChain project (Apache License 2.0). See
`assets/library/scope_aware_react_v1/description.md` for the full attribution.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from tasks.t0006_scope_aware_react_library.code.constants import (
    ACTION_ARGS_FIELD,
    ACTION_NAME_FIELD,
    ACTION_PREFIX,
    CONFIDENCE_PREFIX,
    DEFAULT_GRANULARITY_ON_MISSING_TAG,
    DEFAULT_MAX_TURNS,
    FIELD_ACTION,
    FIELD_CONFIDENCE,
    FIELD_GRANULARITY,
    FIELD_OBSERVATION,
    FIELD_THOUGHT,
    FIELD_TURN_INDEX,
    FINISH_ACTION_NAME,
    FINISH_ANSWER_KEY,
    GRANULARITY_TAG_CLOSE,
    GRANULARITY_TAG_OPEN,
    GRANULARITY_VALUES,
    LANGCHAIN_REACT_ATTRIBUTION,
    OBSERVATION_PARSE_ERROR,
    OBSERVATION_TAG_MISSING_WARNING,
    OBSERVATION_UNKNOWN_TOOL,
    THOUGHT_PREFIX,
)

# ----------------------------------------------------------------------------
# Public type aliases and dataclasses
# ----------------------------------------------------------------------------

type Granularity = Literal["global", "subtask", "atomic"]
type ToolCallable = Callable[..., Any]
type ToolRegistry = Mapping[str, ToolCallable]
type ModelCall = Callable[[str], str]


@dataclass(frozen=True, slots=True)
class Action:
    """A parsed Action emitted by the model.

    `name` is the tool name (or `"Finish"` to terminate). `args` is a mapping of named arguments
    to pass to the tool callable. `args` is always a dict — empty dict when the model emits no
    args.
    """

    name: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TrajectoryRecord:
    """One JSONL record written per Thought / Action / Observation turn.

    All six fields are always present so downstream consumers (calibration, evaluation,
    visualization) never have to special-case missing keys. `confidence` is `None` when the model
    omitted the `Confidence:` line; `thought` is `""` only when parsing failed entirely.
    """

    turn_index: int
    granularity: str
    thought: str
    action: dict[str, Any]
    observation: str
    confidence: float | None


class MalformedActionError(ValueError):
    """Raised internally when the model's `Action:` line is not parseable JSON.

    Surfaces as an observation of `OBSERVATION_PARSE_ERROR` in the trajectory log; the agent
    continues and gives the model another turn to recover.
    """


# ----------------------------------------------------------------------------
# Deterministic model helper for unit tests
# ----------------------------------------------------------------------------


class ScriptedModel:
    """Replay a fixed list of strings as if they were model completions.

    Each call to `__call__` returns the next entry from the script. Raises `IndexError` if the
    script is exhausted, which surfaces in tests as a clear "model ran out of scripted output"
    failure rather than silent infinite-loop behaviour.
    """

    def __init__(self, *, script: list[str]) -> None:
        assert len(script) > 0, "scripted model must have at least one canned response"
        self._script: list[str] = list(script)
        self._index: int = 0

    def __call__(self, prompt: str) -> str:  # noqa: ARG002 — prompt logged elsewhere
        if self._index >= len(self._script):
            raise IndexError(
                f"ScriptedModel exhausted after {self._index} calls; "
                f"add more entries to the script."
            )
        response: str = self._script[self._index]
        self._index += 1
        return response

    @property
    def calls_made(self) -> int:
        return self._index

    def reset(self) -> None:
        self._index = 0


# ----------------------------------------------------------------------------
# Prompt assembly
# ----------------------------------------------------------------------------


def _build_system_prompt(*, granularity: Granularity) -> str:
    return (
        "You are a scope-aware ReAct agent. On every turn, emit exactly one block of three "
        "lines:\n"
        f"  Thought: <{granularity}> <free-form reasoning at the {granularity} level>\n"
        '  Action: {"name": "<tool_name>", "args": {...}}\n'
        "  Confidence: <integer 0-100>\n"
        f"The current granularity is {granularity}. Always prefix the Thought with "
        f"`<{granularity}>` so the trajectory logger captures the active scope. To stop, emit "
        'an Action with name "Finish" and an "answer" arg.\n\n'
        f"({LANGCHAIN_REACT_ATTRIBUTION})\n"
    )


def _render_history(*, records: list[TrajectoryRecord]) -> str:
    if len(records) == 0:
        return ""
    lines: list[str] = []
    for record in records:
        lines.append(f"Thought: <{record.granularity}> {record.thought}")
        lines.append(f"Action: {json.dumps(record.action)}")
        if record.confidence is not None:
            lines.append(f"Confidence: {int(round(record.confidence * 100))}")
        lines.append(f"Observation: {record.observation}")
    return "\n".join(lines) + "\n"


def _build_prompt(
    *,
    granularity: Granularity,
    problem: str,
    history: list[TrajectoryRecord],
) -> str:
    system: str = _build_system_prompt(granularity=granularity)
    transcript: str = _render_history(records=history)
    return (
        f"{system}\n"
        f"Problem: {problem}\n\n"
        f"{transcript}"
        "Continue with the next Thought / Action / Confidence block.\n"
    )


# ----------------------------------------------------------------------------
# Output parsing
# ----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ParsedOutput:
    granularity: str
    thought: str
    action: Action
    confidence: float | None
    tag_was_missing: bool


def _strip_known_prefix(*, line: str, prefix: str) -> str:
    if line.startswith(prefix):
        return line[len(prefix) :].strip()
    return line.strip()


def _extract_granularity_tag(*, thought_text: str) -> tuple[str, str, bool]:
    text: str = thought_text.strip()
    if text.startswith(GRANULARITY_TAG_OPEN):
        close_idx: int = text.find(GRANULARITY_TAG_CLOSE)
        if close_idx > 0:
            tag: str = text[1:close_idx].strip().lower()
            if tag in GRANULARITY_VALUES:
                remainder: str = text[close_idx + 1 :].strip()
                return tag, remainder, False
    return DEFAULT_GRANULARITY_ON_MISSING_TAG, text, True


def _parse_confidence(*, line: str) -> float | None:
    raw: str = _strip_known_prefix(line=line, prefix=CONFIDENCE_PREFIX)
    if len(raw) == 0:
        return None
    try:
        value: float = float(raw)
    except ValueError:
        return None
    if value < 0.0 or value > 100.0:
        return None
    return value / 100.0


def _parse_action(*, line: str) -> Action:
    raw: str = _strip_known_prefix(line=line, prefix=ACTION_PREFIX)
    try:
        parsed: object = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise MalformedActionError(f"Action line is not valid JSON: {raw!r}") from exc
    if not isinstance(parsed, dict):
        raise MalformedActionError(f"Action JSON must be an object, got {type(parsed).__name__}.")
    if ACTION_NAME_FIELD not in parsed:
        raise MalformedActionError(
            f"Action JSON missing required field {ACTION_NAME_FIELD!r}: {parsed!r}"
        )
    name: object = parsed[ACTION_NAME_FIELD]
    if not isinstance(name, str):
        raise MalformedActionError(f"Action name must be a string, got {type(name).__name__}.")
    args_obj: object = parsed.get(ACTION_ARGS_FIELD, {})
    if not isinstance(args_obj, dict):
        raise MalformedActionError(f"Action args must be an object, got {type(args_obj).__name__}.")
    return Action(name=name, args=dict(args_obj))


def _parse_model_output(*, raw: str) -> ParsedOutput:
    """Parse one model completion into a ParsedOutput record.

    The parser is tolerant: it scans the raw string line-by-line looking for `Thought:`,
    `Action:`, and `Confidence:` prefixes anywhere in the text. Lines without these prefixes are
    ignored. Missing `Thought:` falls back to an empty string. Missing `Action:` raises
    `MalformedActionError`. Missing `Confidence:` is recorded as `None`.
    """

    thought_line: str | None = None
    action_line: str | None = None
    confidence_line: str | None = None
    for raw_line in raw.splitlines():
        stripped: str = raw_line.strip()
        if stripped.startswith(THOUGHT_PREFIX) and thought_line is None:
            thought_line = stripped
        elif stripped.startswith(ACTION_PREFIX) and action_line is None:
            action_line = stripped
        elif stripped.startswith(CONFIDENCE_PREFIX) and confidence_line is None:
            confidence_line = stripped
    if action_line is None:
        raise MalformedActionError(f"Model output missing required `{ACTION_PREFIX}` line: {raw!r}")
    raw_thought: str = (
        _strip_known_prefix(line=thought_line, prefix=THOUGHT_PREFIX) if thought_line else ""
    )
    granularity, thought_clean, tag_missing = _extract_granularity_tag(thought_text=raw_thought)
    action: Action = _parse_action(line=action_line)
    confidence: float | None = (
        _parse_confidence(line=confidence_line) if confidence_line is not None else None
    )
    return ParsedOutput(
        granularity=granularity,
        thought=thought_clean,
        action=action,
        confidence=confidence,
        tag_was_missing=tag_missing,
    )


# ----------------------------------------------------------------------------
# Trajectory writer
# ----------------------------------------------------------------------------


class TrajectoryWriter:
    """Append-only JSONL writer with one record per turn and explicit flush per write."""

    def __init__(self, *, path: Path) -> None:
        self._path: Path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._fp = self._path.open(mode="w", encoding="utf-8")

    def write(self, *, record: TrajectoryRecord) -> None:
        payload: dict[str, Any] = asdict(record)
        # Re-key payload using the canonical field-name constants to keep the schema explicit.
        ordered: dict[str, Any] = {
            FIELD_TURN_INDEX: payload["turn_index"],
            FIELD_GRANULARITY: payload["granularity"],
            FIELD_THOUGHT: payload["thought"],
            FIELD_ACTION: payload["action"],
            FIELD_OBSERVATION: payload["observation"],
            FIELD_CONFIDENCE: payload["confidence"],
        }
        self._fp.write(json.dumps(ordered, ensure_ascii=False))
        self._fp.write("\n")
        self._fp.flush()

    def close(self) -> None:
        if not self._fp.closed:
            self._fp.close()

    def __enter__(self) -> TrajectoryWriter:
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()


# ----------------------------------------------------------------------------
# Agent
# ----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AgentResult:
    """Outcome of one `ScopeAwareReactAgent.run()` call."""

    answer: str | None
    finished: bool
    turns: int
    trajectory: list[TrajectoryRecord]


class ScopeAwareReactAgent:
    """Run the scope-aware ReAct loop with a fixed granularity for all turns."""

    def __init__(
        self,
        *,
        problem: str,
        granularity: Granularity,
        tool_registry: ToolRegistry,
        model_call: ModelCall,
        trajectory_path: Path,
        max_turns: int = DEFAULT_MAX_TURNS,
        default_granularity_on_missing_tag: Granularity = DEFAULT_GRANULARITY_ON_MISSING_TAG,
    ) -> None:
        assert granularity in GRANULARITY_VALUES, (
            f"granularity must be one of {GRANULARITY_VALUES}, got {granularity!r}"
        )
        assert default_granularity_on_missing_tag in GRANULARITY_VALUES, (
            "default_granularity_on_missing_tag must be a valid Granularity literal"
        )
        assert max_turns > 0, "max_turns must be positive"
        self._problem: str = problem
        self._granularity: Granularity = granularity
        self._tool_registry: ToolRegistry = tool_registry
        self._model_call: ModelCall = model_call
        self._trajectory_path: Path = trajectory_path
        self._max_turns: int = max_turns
        self._default_on_missing: Granularity = default_granularity_on_missing_tag
        self._last_prompt: str | None = None

    # --- introspection helpers (used by tests; @property is field access only) -------

    @property
    def last_prompt(self) -> str | None:
        return self._last_prompt

    @property
    def trajectory_path(self) -> Path:
        return self._trajectory_path

    # --- core loop ------------------------------------------------------------------

    def _dispatch_action(self, *, action: Action) -> str:
        if action.name == FINISH_ACTION_NAME:
            answer_obj: object = action.args.get(FINISH_ANSWER_KEY, "")
            return str(answer_obj)
        tool: ToolCallable | None = self._tool_registry.get(action.name)
        if tool is None:
            return OBSERVATION_UNKNOWN_TOOL
        try:
            result: Any = tool(**action.args)
        except Exception as exc:  # noqa: BLE001 — observed by the agent; do not abort the run
            return f"<tool_error:{type(exc).__name__}:{exc}>"
        return str(result)

    def run(self) -> AgentResult:
        history: list[TrajectoryRecord] = []
        finished: bool = False
        answer: str | None = None
        with TrajectoryWriter(path=self._trajectory_path) as writer:
            for turn_index in range(self._max_turns):
                prompt: str = _build_prompt(
                    granularity=self._granularity,
                    problem=self._problem,
                    history=history,
                )
                self._last_prompt = prompt
                raw_output: str = self._model_call(prompt)
                try:
                    parsed: ParsedOutput = _parse_model_output(raw=raw_output)
                except MalformedActionError as exc:
                    record: TrajectoryRecord = TrajectoryRecord(
                        turn_index=turn_index,
                        granularity=self._granularity,
                        thought="",
                        action={ACTION_NAME_FIELD: "<unparsed>", ACTION_ARGS_FIELD: {}},
                        observation=f"{OBSERVATION_PARSE_ERROR}:{exc}",
                        confidence=None,
                    )
                    history.append(record)
                    writer.write(record=record)
                    continue
                # Granularity reconciliation: if the model omitted the tag, fall back to the
                # configured default and record a warning observation that downstream calibration
                # code can detect without parsing strings.
                effective_granularity: str
                observation_prefix: str = ""
                if parsed.tag_was_missing:
                    effective_granularity = self._default_on_missing
                    observation_prefix = OBSERVATION_TAG_MISSING_WARNING + ":"
                else:
                    effective_granularity = parsed.granularity
                if parsed.action.name == FINISH_ACTION_NAME:
                    finished = True
                    answer = self._dispatch_action(action=parsed.action)
                    observation: str = observation_prefix + answer
                    record = TrajectoryRecord(
                        turn_index=turn_index,
                        granularity=effective_granularity,
                        thought=parsed.thought,
                        action={
                            ACTION_NAME_FIELD: parsed.action.name,
                            ACTION_ARGS_FIELD: dict(parsed.action.args),
                        },
                        observation=observation,
                        confidence=parsed.confidence,
                    )
                    history.append(record)
                    writer.write(record=record)
                    break
                observation = observation_prefix + self._dispatch_action(action=parsed.action)
                record = TrajectoryRecord(
                    turn_index=turn_index,
                    granularity=effective_granularity,
                    thought=parsed.thought,
                    action={
                        ACTION_NAME_FIELD: parsed.action.name,
                        ACTION_ARGS_FIELD: dict(parsed.action.args),
                    },
                    observation=observation,
                    confidence=parsed.confidence,
                )
                history.append(record)
                writer.write(record=record)
        return AgentResult(
            answer=answer,
            finished=finished,
            turns=len(history),
            trajectory=list(history),
        )
