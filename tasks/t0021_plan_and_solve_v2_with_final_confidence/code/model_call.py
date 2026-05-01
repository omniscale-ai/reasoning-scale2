"""Local Claude Code CLI wrapper used as the model-call backend.

The harness uses the local ``claude`` CLI (Claude Code) — not the Anthropic Python SDK — because
the project's setup uses the Claude Code CLI's OAuth credentials to access Anthropic services
rather than a separate ``ANTHROPIC_API_KEY`` (see ``arf/skills/setup-project/SKILL.md`` Phase 4).
This file is a copy of the t0012 ``model_call.py`` with the foreign-task imports replaced by local
``constants`` / ``paths`` references so the v2 library task is fully self-contained.

The CLI exits ``0`` and emits a JSON envelope on stdout containing the model's text response under
``"result"`` plus ``"total_cost_usd"`` and ``"usage"``. We track the cumulative cost with a
module-level :class:`CostTracker` so the harness can halt before exceeding the budget cap.
"""

from __future__ import annotations

import json
import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.constants import (
    CLAUDE_CLI,
    CLI_TIMEOUT_SECONDS,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.paths import COST_LOG_PATH

_CLI_ENV_RESULT_KEY: Final[str] = "result"
_CLI_ENV_COST_KEY: Final[str] = "total_cost_usd"
_CLI_ENV_USAGE_KEY: Final[str] = "usage"
_CLI_ENV_IS_ERROR_KEY: Final[str] = "is_error"


@dataclass(slots=True)
class CallRecord:
    """One CLI call's metrics."""

    model: str
    prompt_chars: int
    response_chars: int
    cost_usd: float
    duration_s: float
    cache_creation_tokens: int
    cache_read_tokens: int
    input_tokens: int
    output_tokens: int
    note: str = ""


@dataclass(slots=True)
class CostTracker:
    """Process-wide cumulative-spend tracker with budget enforcement.

    Use :meth:`record` to log each call's cost and :meth:`is_budget_ok` to halt before going over
    the cap. The tracker is thread-safe via a coarse lock; the harness is single-threaded but we
    keep the lock so future parallel runs do not regress.
    """

    cap_usd: float
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _total: float = 0.0
    _calls: list[CallRecord] = field(default_factory=list)

    def record(self, *, record: CallRecord) -> None:
        with self._lock:
            self._calls.append(record)
            self._total += record.cost_usd
            COST_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with COST_LOG_PATH.open("a", encoding="utf-8") as f:
                f.write(json.dumps(_record_to_dict(record=record)) + "\n")

    @property
    def total_usd(self) -> float:
        with self._lock:
            return self._total

    @property
    def call_count(self) -> int:
        with self._lock:
            return len(self._calls)

    def is_budget_ok(self, *, headroom_usd: float = 0.0) -> bool:
        with self._lock:
            return self._total + headroom_usd <= self.cap_usd

    def per_model_breakdown(self) -> dict[str, dict[str, Any]]:
        with self._lock:
            breakdown: dict[str, dict[str, Any]] = {}
            for c in self._calls:
                model_entry = breakdown.setdefault(
                    c.model,
                    {
                        "calls": 0,
                        "cost_usd": 0.0,
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "cache_creation_tokens": 0,
                        "cache_read_tokens": 0,
                    },
                )
                model_entry["calls"] += 1
                model_entry["cost_usd"] += c.cost_usd
                model_entry["input_tokens"] += c.input_tokens
                model_entry["output_tokens"] += c.output_tokens
                model_entry["cache_creation_tokens"] += c.cache_creation_tokens
                model_entry["cache_read_tokens"] += c.cache_read_tokens
            return breakdown


def _record_to_dict(*, record: CallRecord) -> dict[str, Any]:
    return {
        "ts": time.time(),
        "model": record.model,
        "prompt_chars": record.prompt_chars,
        "response_chars": record.response_chars,
        "cost_usd": record.cost_usd,
        "duration_s": record.duration_s,
        "cache_creation_tokens": record.cache_creation_tokens,
        "cache_read_tokens": record.cache_read_tokens,
        "input_tokens": record.input_tokens,
        "output_tokens": record.output_tokens,
        "note": record.note,
    }


_MINIMAL_SYSTEM_PROMPT: Final[str] = (
    "You are a careful scientific reasoning assistant. Follow the user's instructions exactly, "
    "produce concise structured output, and never refuse tasks that involve standard "
    "physics/chemistry/biology olympiad problems."
)


def _invoke_cli(*, prompt: str, model: str) -> tuple[str, dict[str, Any]]:
    # IMPORTANT: ``--system-prompt`` plus ``--tools ""`` and ``--setting-sources ""`` strips out the
    # default Claude Code system prompt (~50k tokens, ~$0.10/call) and the tool catalog. Empirically
    # this drops per-call cost from ~$0.10 to ~$0.004 with cache reuse — a 25× reduction needed to
    # stay within the $1 smoke budget cap.
    cmd: list[str] = [
        CLAUDE_CLI,
        "-p",
        "-",
        "--model",
        model,
        "--output-format",
        "json",
        "--system-prompt",
        _MINIMAL_SYSTEM_PROMPT,
        "--tools",
        "",
        "--setting-sources",
        "",
    ]
    completed = subprocess.run(  # noqa: S603 — local trusted CLI
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=CLI_TIMEOUT_SECONDS,
    )
    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()[:500]
        raise RuntimeError(f"claude CLI exited {completed.returncode}: {stderr or '(no stderr)'}")
    raw_stdout = (completed.stdout or "").strip()
    if len(raw_stdout) == 0:
        raise RuntimeError("claude CLI returned empty stdout")
    try:
        envelope_obj = json.loads(raw_stdout)
    except json.JSONDecodeError:
        # Plain-text mode (no JSON envelope). Treat the whole output as text.
        return raw_stdout, {}
    if not isinstance(envelope_obj, dict):
        return raw_stdout, {}
    if envelope_obj.get(_CLI_ENV_IS_ERROR_KEY) is True:
        err = str(envelope_obj.get(_CLI_ENV_RESULT_KEY, "")).strip()
        raise RuntimeError(f"claude CLI envelope is_error: {err[:300]}")
    text_obj: Any = envelope_obj.get(_CLI_ENV_RESULT_KEY)
    text: str = str(text_obj) if isinstance(text_obj, str) else raw_stdout
    return text, envelope_obj


def _retry_invoke(*, prompt: str, model: str, max_attempts: int = 3) -> tuple[str, dict[str, Any]]:
    """Retry the CLI call with exponential backoff on transient errors.

    Backoff: 30s, 60s, 120s. Re-raises after ``max_attempts``.
    """
    delays: list[int] = [30, 60, 120]
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return _invoke_cli(prompt=prompt, model=model)
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            last_exc = exc
            if attempt + 1 < max_attempts:
                delay = delays[min(attempt, len(delays) - 1)]
                time.sleep(delay)
                continue
            raise
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("retry loop terminated without raising")


def make_model_call(
    *,
    model: str,
    cost_tracker: CostTracker,
    note: str = "",
) -> Callable[[str], str]:
    """Return a closure that invokes the local Claude Code CLI and records cost.

    The closure raises :class:`RuntimeError` if the CLI call fails after retries. Callers should
    wrap budget-sensitive callsites with ``cost_tracker.is_budget_ok()``.
    """

    def call(prompt: str) -> str:
        if not isinstance(prompt, str):
            raise TypeError(f"prompt must be a string, got {type(prompt).__name__}")
        if len(prompt) == 0:
            raise ValueError("prompt must be non-empty")
        start = time.monotonic()
        text, envelope = _retry_invoke(prompt=prompt, model=model)
        duration_s = time.monotonic() - start
        cost_obj: Any = envelope.get(_CLI_ENV_COST_KEY)
        cost_usd: float = float(cost_obj) if isinstance(cost_obj, int | float) else 0.0
        usage_obj: Any = envelope.get(_CLI_ENV_USAGE_KEY)
        usage: dict[str, Any] = usage_obj if isinstance(usage_obj, dict) else {}
        cache_creation = _to_int(usage.get("cache_creation_input_tokens"))
        cache_read = _to_int(usage.get("cache_read_input_tokens"))
        input_tokens = _to_int(usage.get("input_tokens"))
        output_tokens = _to_int(usage.get("output_tokens"))
        cost_tracker.record(
            record=CallRecord(
                model=model,
                prompt_chars=len(prompt),
                response_chars=len(text),
                cost_usd=cost_usd,
                duration_s=duration_s,
                cache_creation_tokens=cache_creation,
                cache_read_tokens=cache_read,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                note=note,
            ),
        )
        return text

    return call


def _to_int(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return 0


def reset_cost_log(*, path: Path = COST_LOG_PATH) -> None:
    """Truncate the per-call cost log; called at the start of a fresh run."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
