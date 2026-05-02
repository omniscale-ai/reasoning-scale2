"""Anthropic-backed model-call shim with cost tallying and retry-with-backoff."""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Final

from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.paths import (
    FORBIDDEN_HAIKU_MODEL_ID,
)

_TRANSPORT_ENV_VAR: Final[str] = "T0026_TRANSPORT"
_TRANSPORT_CLI: Final[str] = "cli"
_TRANSPORT_SDK: Final[str] = "sdk"
_DEFAULT_TRANSPORT: Final[str] = _TRANSPORT_CLI

_MAX_RETRIES: Final[int] = 2
_INITIAL_BACKOFF_SECONDS: Final[float] = 2.0
_MAX_BACKOFF_SECONDS: Final[float] = 8.0
_CLI_TIMEOUT_SECONDS: Final[float] = 180.0

SONNET_INPUT_PER_MTOK_USD: Final[float] = 3.0
SONNET_OUTPUT_PER_MTOK_USD: Final[float] = 15.0
OPUS_INPUT_PER_MTOK_USD: Final[float] = 15.0
OPUS_OUTPUT_PER_MTOK_USD: Final[float] = 75.0

_PRICE_TABLE: Final[dict[str, tuple[float, float]]] = {
    "claude-sonnet-4-6": (SONNET_INPUT_PER_MTOK_USD, SONNET_OUTPUT_PER_MTOK_USD),
    "claude-opus-4-7": (OPUS_INPUT_PER_MTOK_USD, OPUS_OUTPUT_PER_MTOK_USD),
}


def _published_price(*, model_id: str, prompt_tokens: int, completion_tokens: int) -> float:
    if model_id not in _PRICE_TABLE:
        return 0.0
    in_rate, out_rate = _PRICE_TABLE[model_id]
    return prompt_tokens * in_rate / 1_000_000.0 + completion_tokens * out_rate / 1_000_000.0


@dataclass(slots=True)
class CostTracker:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0
    n_calls: int = 0
    parse_failures: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, *, model_id: str, prompt_tokens: int, completion_tokens: int) -> None:
        with self._lock:
            self.prompt_tokens += prompt_tokens
            self.completion_tokens += completion_tokens
            self.cost_usd += _published_price(
                model_id=model_id,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            self.n_calls += 1

    def note_parse_failure(self) -> None:
        with self._lock:
            self.parse_failures += 1

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens,
                "cost_usd": self.cost_usd,
                "n_calls": self.n_calls,
                "parse_failures": self.parse_failures,
            }


def _selected_transport() -> str:
    raw = os.environ.get(_TRANSPORT_ENV_VAR, _DEFAULT_TRANSPORT).strip().lower()
    if raw not in {_TRANSPORT_CLI, _TRANSPORT_SDK}:
        raise ValueError(
            f"{_TRANSPORT_ENV_VAR} must be {_TRANSPORT_CLI!r} or {_TRANSPORT_SDK!r}; got {raw!r}"
        )
    return raw


def _estimate_tokens(*, text: str) -> int:
    return max(1, len(text) // 4)


def _invoke_cli(*, prompt: str, model_id: str, max_tokens: int) -> tuple[str, int, int]:
    _ = max_tokens
    cmd: list[str] = [
        "claude",
        "-p",
        "-",
        "--model",
        model_id,
        "--output-format",
        "json",
    ]
    completed = subprocess.run(  # noqa: S603 — local trusted CLI
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=_CLI_TIMEOUT_SECONDS,
        check=False,
    )
    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()[:500]
        raise RuntimeError(f"claude CLI exited {completed.returncode}: {stderr or '(no stderr)'}")
    raw_stdout = (completed.stdout or "").strip()
    if len(raw_stdout) == 0:
        raise RuntimeError("claude CLI returned empty stdout")
    try:
        envelope = json.loads(raw_stdout)
    except json.JSONDecodeError:
        return (
            raw_stdout,
            _estimate_tokens(text=prompt),
            _estimate_tokens(text=raw_stdout),
        )
    if not isinstance(envelope, dict):
        return (
            raw_stdout,
            _estimate_tokens(text=prompt),
            _estimate_tokens(text=raw_stdout),
        )
    if envelope.get("is_error") is True:
        err = str(envelope.get("result", "")).strip()
        raise RuntimeError(f"claude CLI envelope is_error: {err[:300]}")
    text_obj = envelope.get("result", "")
    text = text_obj if isinstance(text_obj, str) else raw_stdout
    usage = envelope.get("usage", {})
    if isinstance(usage, dict):
        in_tok_obj = usage.get("input_tokens", _estimate_tokens(text=prompt))
        out_tok_obj = usage.get("output_tokens", _estimate_tokens(text=text))
        in_tok = (
            int(in_tok_obj)
            if isinstance(in_tok_obj, int | float)
            else _estimate_tokens(text=prompt)
        )
        out_tok = (
            int(out_tok_obj)
            if isinstance(out_tok_obj, int | float)
            else _estimate_tokens(text=text)
        )
    else:
        in_tok = _estimate_tokens(text=prompt)
        out_tok = _estimate_tokens(text=text)
    return text, in_tok, out_tok


def _invoke_sdk(*, prompt: str, model_id: str, max_tokens: int) -> tuple[str, int, int]:
    import anthropic  # noqa: PLC0415 — lazy import; only used when SDK transport is selected

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text_parts: list[str] = []
    for block in response.content:
        block_type = getattr(block, "type", None)
        if block_type == "text":
            text_parts.append(getattr(block, "text", ""))
    text = "".join(text_parts)
    usage = response.usage
    in_tok = int(getattr(usage, "input_tokens", 0))
    out_tok = int(getattr(usage, "output_tokens", 0))
    return text, in_tok, out_tok


def _retryable_invoke(
    *,
    prompt: str,
    model_id: str,
    max_tokens: int,
    transport: str,
) -> tuple[str, int, int]:
    backoff = _INITIAL_BACKOFF_SECONDS
    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            if transport == _TRANSPORT_CLI:
                return _invoke_cli(prompt=prompt, model_id=model_id, max_tokens=max_tokens)
            return _invoke_sdk(prompt=prompt, model_id=model_id, max_tokens=max_tokens)
        except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
            last_exc = exc
            if attempt + 1 >= _MAX_RETRIES:
                raise
            time.sleep(min(backoff, _MAX_BACKOFF_SECONDS))
            backoff *= 2.0
        except Exception as exc:
            last_exc = exc
            transient = False
            try:
                import anthropic  # noqa: PLC0415

                if isinstance(exc, anthropic.RateLimitError | anthropic.APIConnectionError):
                    transient = True
                if isinstance(exc, anthropic.APIStatusError) and exc.status_code in (
                    500,
                    502,
                    503,
                    504,
                    529,
                ):
                    transient = True
            except ImportError:
                pass
            if not transient or attempt + 1 >= _MAX_RETRIES:
                raise
            time.sleep(min(backoff, _MAX_BACKOFF_SECONDS))
            backoff *= 2.0
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("retry loop terminated without raising")


def make_model_call(
    *,
    model_id: str,
    cost_tracker: CostTracker,
    max_tokens: int = 4096,
    secondary_cost_tracker: CostTracker | None = None,
) -> Callable[[str], str]:
    assert model_id != FORBIDDEN_HAIKU_MODEL_ID, (
        f"haiku model {FORBIDDEN_HAIKU_MODEL_ID!r} is forbidden by t0019 calibration finding"
    )
    transport = _selected_transport()

    def call(prompt: str) -> str:
        if not isinstance(prompt, str):
            raise TypeError(f"prompt must be a string, got {type(prompt).__name__}")
        if len(prompt) == 0:
            raise ValueError("prompt must be non-empty")
        text, in_tok, out_tok = _retryable_invoke(
            prompt=prompt,
            model_id=model_id,
            max_tokens=max_tokens,
            transport=transport,
        )
        cost_tracker.record(
            model_id=model_id,
            prompt_tokens=in_tok,
            completion_tokens=out_tok,
        )
        if secondary_cost_tracker is not None:
            secondary_cost_tracker.record(
                model_id=model_id,
                prompt_tokens=in_tok,
                completion_tokens=out_tok,
            )
        return text

    return call
