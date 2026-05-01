"""Judge runner for t0019.

Two transports are supported, selected via the ``JUDGE_TRANSPORT`` environment variable:

* ``cli`` (default) — invoke the local ``claude`` CLI as a subprocess. This routes the call
  through the user's Claude Code subscription, which is the only path with Sonnet quota in this
  environment. We capture stdout, parse the JSON envelope, extract the assistant text plus the
  envelope-reported ``total_cost_usd``, and return the same ``JudgeOutcome`` shape the rest of the
  pipeline expects. See ``intervention/critical_step_blocked.md`` for the rationale.
* ``sdk`` — call ``anthropic.Anthropic().messages.create(...)`` directly. Kept as a future-proof
  fallback for when a project Anthropic API key with Sonnet quota becomes available; switching back
  is a one-line env flip rather than a rewrite.

The runner is idempotent by ``pool_row_id`` + ``prompt_kind`` — re-running skips already-judged
rows. A ``threading.Event halt`` guards the budget cap.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess  # noqa: S404 — local trusted CLI; full command is constructed from constants.
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TextIO

from tasks.t0019_v2_judge_calibration_sonnet.code.constants import (
    BUDGET_CAP_USD,
    JUDGE_MODEL_ID,
    SONNET_INPUT_COST_PER_MTOK_USD,
    SONNET_OUTPUT_COST_PER_MTOK_USD,
)
from tasks.t0019_v2_judge_calibration_sonnet.code.data_loader import PoolRow
from tasks.t0019_v2_judge_calibration_sonnet.code.parse import ParsedVerdict, parse_verdict

_TRANSPORT_CLI: str = "cli"
_TRANSPORT_SDK: str = "sdk"


def _selected_transport() -> str:
    raw = os.environ.get("JUDGE_TRANSPORT", _TRANSPORT_CLI).strip().lower()
    if raw not in {_TRANSPORT_CLI, _TRANSPORT_SDK}:
        raise ValueError(
            f"JUDGE_TRANSPORT must be {_TRANSPORT_CLI!r} or {_TRANSPORT_SDK!r}; got {raw!r}"
        )
    return raw


@dataclass(frozen=True, slots=True)
class CallResult:
    text: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    elapsed_seconds: float


@dataclass(frozen=True, slots=True)
class JudgeOutcome:
    pool_row_id: str
    annotator: str
    task_id: str
    benchmark: str
    domain: str
    prompt_kind: str
    judge_model: str
    verdict: str | None
    justification: str | None
    sub_scores: dict[str, int] | None
    parse_status: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    elapsed_seconds: float


@dataclass(slots=True)
class RunStats:
    rows_judged: int = 0
    rows_skipped: int = 0
    rows_acceptable: int = 0
    rows_needs_revision: int = 0
    rows_parse_failure: int = 0
    rows_call_failure: int = 0
    total_cost_usd: float = 0.0
    total_elapsed_seconds: float = 0.0
    per_call: list[dict[str, Any]] = field(default_factory=list)


def _model_cost_usd(*, input_tokens: int, output_tokens: int) -> float:
    """Fall-back per-call cost using sonnet rate cards. Used only when the CLI envelope or SDK
    response does not surface a usable cost field."""
    return (
        input_tokens * SONNET_INPUT_COST_PER_MTOK_USD / 1_000_000.0
        + output_tokens * SONNET_OUTPUT_COST_PER_MTOK_USD / 1_000_000.0
    )


_CLI_TIMEOUT_SECONDS: float = 120.0
_MAX_RETRIES: int = 3
_INITIAL_BACKOFF_SECONDS: float = 2.0


# ---- CLI transport --------------------------------------------------------------------------


def _estimate_tokens(text: str) -> int:
    """Rough token-count estimate used as a fallback when the CLI envelope omits usage."""
    return max(1, len(text) // 4)


def _call_claude_cli(*, system_prompt: str, user_prompt: str, model: str) -> CallResult:
    """Invoke the local ``claude`` CLI subprocess and parse the JSON envelope.

    The CLI does not expose a system-prompt flag in ``-p`` mode, so we inline the system prompt
    inside ``<system>...</system>`` tags at the top of the user input — same convention as t0014's
    judge code path (``tasks/t0014_v2_annotator_sonnet_rerun/code/v2_judge.py``).
    """
    full_prompt = f"<system>\n{system_prompt}\n</system>\n\n{user_prompt}"
    cmd = [
        "claude",
        "-p",
        "-",
        "--model",
        model,
        "--output-format",
        "json",
    ]
    started = time.time()
    backoff = _INITIAL_BACKOFF_SECONDS
    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            completed = subprocess.run(  # noqa: S603 — local trusted CLI
                cmd,
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=_CLI_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            last_exc = exc
            if attempt == _MAX_RETRIES - 1:
                raise
            print(
                f"  [retry] CLI timeout attempt={attempt + 1}/{_MAX_RETRIES}; "
                f"sleeping {backoff:.1f}s"
            )
            time.sleep(backoff)
            backoff *= 2.0
            continue
        if completed.returncode != 0:
            stderr_snippet = (completed.stderr or "").strip()[:500]
            raise RuntimeError(
                f"claude CLI exited {completed.returncode}: {stderr_snippet or '(no stderr)'}"
            )
        raw_stdout = completed.stdout.strip()
        if len(raw_stdout) == 0:
            raise RuntimeError("claude CLI returned empty output")

        elapsed = time.time() - started

        text = raw_stdout
        input_tokens = _estimate_tokens(full_prompt)
        output_tokens = _estimate_tokens(text)
        cost_usd = _model_cost_usd(input_tokens=input_tokens, output_tokens=output_tokens)
        try:
            envelope = json.loads(raw_stdout)
        except json.JSONDecodeError:
            return CallResult(
                text=text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd,
                elapsed_seconds=elapsed,
            )
        if isinstance(envelope, dict):
            if envelope.get("is_error") is True:
                err_text = str(envelope.get("result", "")).strip() or "claude CLI reported is_error"
                raise RuntimeError(f"claude CLI envelope error: {err_text[:300]}")
            if isinstance(envelope.get("result"), str):
                text = envelope["result"]
                output_tokens = _estimate_tokens(text)
            usage = envelope.get("usage")
            if isinstance(usage, dict):
                usage_input = usage.get("input_tokens")
                usage_output = usage.get("output_tokens")
                if isinstance(usage_input, int):
                    input_tokens = usage_input
                if isinstance(usage_output, int):
                    output_tokens = usage_output
            envelope_cost = envelope.get("total_cost_usd")
            if isinstance(envelope_cost, int | float):
                cost_usd = float(envelope_cost)
        return CallResult(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
            elapsed_seconds=elapsed,
        )
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("claude CLI call failed with no exception")


# ---- SDK transport (fallback) --------------------------------------------------------------


def _call_sdk(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str,
    max_tokens: int,
) -> CallResult:
    """Anthropic SDK call. Used when ``JUDGE_TRANSPORT=sdk``; not the default in this environment.

    Imported lazily so the CLI path does not pay the SDK import cost.
    """
    import anthropic  # noqa: PLC0415 — lazy import: only used when SDK transport is selected.

    client = anthropic.Anthropic()
    started = time.time()
    backoff = _INITIAL_BACKOFF_SECONDS
    response = None
    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            break
        except (anthropic.RateLimitError, anthropic.APIConnectionError) as exc:
            last_exc = exc
            if attempt == _MAX_RETRIES - 1:
                raise
            print(
                f"  [retry] {type(exc).__name__} attempt={attempt + 1}/{_MAX_RETRIES}; "
                f"sleeping {backoff:.1f}s"
            )
            time.sleep(backoff)
            backoff *= 2.0
        except anthropic.APIStatusError as exc:
            if exc.status_code in (500, 502, 503, 504, 529) and attempt < _MAX_RETRIES - 1:
                last_exc = exc
                print(
                    f"  [retry] {type(exc).__name__} status={exc.status_code} "
                    f"attempt={attempt + 1}/{_MAX_RETRIES}; sleeping {backoff:.1f}s"
                )
                time.sleep(backoff)
                backoff *= 2.0
                continue
            raise
    if response is None:
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("Anthropic SDK call failed without an exception")
    elapsed = time.time() - started
    text_parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(getattr(block, "text", ""))
    text = "".join(text_parts)
    input_tokens = int(getattr(response.usage, "input_tokens", 0))
    output_tokens = int(getattr(response.usage, "output_tokens", 0))
    cost_usd = _model_cost_usd(input_tokens=input_tokens, output_tokens=output_tokens)
    return CallResult(
        text=text,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=cost_usd,
        elapsed_seconds=elapsed,
    )


def call_judge(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str,
    max_tokens: int = 900,
    transport: str | None = None,
) -> CallResult:
    """Dispatch to the configured transport."""
    selected = transport if transport is not None else _selected_transport()
    if selected == _TRANSPORT_CLI:
        return _call_claude_cli(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
        )
    return _call_sdk(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        max_tokens=max_tokens,
    )


def _format_user_prompt(*, row: PoolRow, user_template: str) -> str:
    return user_template.format(
        benchmark=row.benchmark,
        domain=row.domain,
        problem=row.problem,
        hierarchy_json=json.dumps(row.hierarchy, ensure_ascii=False, indent=2),
        gold_actions_json=json.dumps(row.gold_actions, ensure_ascii=False, indent=2),
    )


def judge_one(
    *,
    row: PoolRow,
    prompt_kind: str,
    model: str,
    system_prompt: str,
    user_template: str,
    transport: str | None = None,
) -> JudgeOutcome:
    user_prompt = _format_user_prompt(row=row, user_template=user_template)
    try:
        call = call_judge(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            transport=transport,
        )
    except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
        return JudgeOutcome(
            pool_row_id=row.pool_row_id,
            annotator=row.annotator,
            task_id=row.task_id,
            benchmark=row.benchmark,
            domain=row.domain,
            prompt_kind=prompt_kind,
            judge_model=model,
            verdict=None,
            justification=None,
            sub_scores=None,
            parse_status=f"call-failure: {exc.__class__.__name__}: {str(exc)[:200]}",
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
            elapsed_seconds=0.0,
        )
    except Exception as exc:  # noqa: BLE001 — the SDK exception classes vary; we treat any
        # unexpected failure as a call failure rather than crashing the whole run.
        return JudgeOutcome(
            pool_row_id=row.pool_row_id,
            annotator=row.annotator,
            task_id=row.task_id,
            benchmark=row.benchmark,
            domain=row.domain,
            prompt_kind=prompt_kind,
            judge_model=model,
            verdict=None,
            justification=None,
            sub_scores=None,
            parse_status=f"call-failure: {exc.__class__.__name__}: {str(exc)[:200]}",
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
            elapsed_seconds=0.0,
        )
    parsed: ParsedVerdict = parse_verdict(raw_text=call.text)
    return JudgeOutcome(
        pool_row_id=row.pool_row_id,
        annotator=row.annotator,
        task_id=row.task_id,
        benchmark=row.benchmark,
        domain=row.domain,
        prompt_kind=prompt_kind,
        judge_model=model,
        verdict=parsed.verdict,
        justification=parsed.justification,
        sub_scores=parsed.sub_scores,
        parse_status=parsed.parse_status,
        input_tokens=call.input_tokens,
        output_tokens=call.output_tokens,
        cost_usd=call.cost_usd,
        elapsed_seconds=call.elapsed_seconds,
    )


def _existing_outcomes(*, path: Path) -> dict[str, dict[str, Any]]:
    """Return prior outcomes keyed by ``pool_row_id`` so failed retries can be replaced."""
    if not path.exists():
        return {}
    seen: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if len(stripped) == 0:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            row_id = row.get("pool_row_id")
            if isinstance(row_id, str):
                seen[row_id] = row
    return seen


def _outcome_to_dict(outcome: JudgeOutcome) -> dict[str, Any]:
    return {
        "pool_row_id": outcome.pool_row_id,
        "annotator": outcome.annotator,
        "task_id": outcome.task_id,
        "benchmark": outcome.benchmark,
        "domain": outcome.domain,
        "prompt_kind": outcome.prompt_kind,
        "judge_model": outcome.judge_model,
        "verdict": outcome.verdict,
        "justification": outcome.justification,
        "sub_scores": outcome.sub_scores,
        "parse_status": outcome.parse_status,
        "input_tokens": outcome.input_tokens,
        "output_tokens": outcome.output_tokens,
        "cost_usd": outcome.cost_usd,
        "elapsed_seconds": outcome.elapsed_seconds,
    }


def _record(
    *,
    stats: RunStats,
    outcome: JudgeOutcome,
    out_f: TextIO,
    total: int,
) -> None:
    stats.total_cost_usd += outcome.cost_usd
    stats.total_elapsed_seconds += outcome.elapsed_seconds
    stats.rows_judged += 1
    if outcome.verdict == "acceptable":
        stats.rows_acceptable += 1
    elif outcome.verdict == "needs revision":
        stats.rows_needs_revision += 1
    elif outcome.parse_status.startswith("parse-failure"):
        stats.rows_parse_failure += 1
    elif outcome.parse_status.startswith("call-failure"):
        stats.rows_call_failure += 1

    record = _outcome_to_dict(outcome)
    stats.per_call.append(record)
    print(
        f"[{stats.rows_judged}/{total}] {outcome.pool_row_id} {outcome.benchmark[:25]:25s} "
        f"verdict={outcome.verdict} cost=${outcome.cost_usd:.4f} "
        f"elapsed={outcome.elapsed_seconds:.2f}s running=${stats.total_cost_usd:.4f}"
    )
    out_f.write(json.dumps(record, ensure_ascii=False))
    out_f.write("\n")
    out_f.flush()


def _is_successful(*, outcome_dict: dict[str, Any]) -> bool:
    """A previously persisted outcome counts as resumable only if it was a successful judge call.
    Failed call rows are treated as not-yet-judged so we can retry them on resume."""
    parse_status = outcome_dict.get("parse_status")
    if not isinstance(parse_status, str):
        return False
    return not parse_status.startswith("call-failure")


def _rewrite_filtered(*, path: Path, exclude_ids: set[str]) -> None:
    """Rewrite ``path`` removing any rows whose ``pool_row_id`` is in ``exclude_ids``."""
    if not path.exists() or len(exclude_ids) == 0:
        return
    keep: list[str] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if len(stripped) == 0:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            row_id = row.get("pool_row_id")
            if isinstance(row_id, str) and row_id in exclude_ids:
                continue
            keep.append(stripped)
    with path.open("w", encoding="utf-8") as f:
        for line in keep:
            f.write(line)
            f.write("\n")


def run_pool(
    *,
    pool: list[PoolRow],
    prompt_kind: str,
    model: str,
    system_prompt: str,
    user_template: str,
    output_jsonl_path: Path,
    max_workers: int = 4,
    budget_cap_usd: float = BUDGET_CAP_USD,
    limit: int | None = None,
    transport: str | None = None,
) -> RunStats:
    output_jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    existing = _existing_outcomes(path=output_jsonl_path)
    failed_to_purge: set[str] = {
        row_id for row_id, outcome in existing.items() if not _is_successful(outcome_dict=outcome)
    }
    if len(failed_to_purge) > 0:
        print(
            f"Purging {len(failed_to_purge)} failed prior outcomes from {output_jsonl_path.name} "
            f"so they can be retried."
        )
        _rewrite_filtered(path=output_jsonl_path, exclude_ids=failed_to_purge)
        for row_id in failed_to_purge:
            existing.pop(row_id, None)
    target = pool if limit is None else pool[:limit]
    pending = [row for row in target if row.pool_row_id not in existing]
    stats = RunStats()
    stats.rows_skipped = len(target) - len(pending)
    if len(pending) == 0:
        print(f"All {len(target)} target rows already judged for prompt_kind={prompt_kind}.")
        return stats

    if len(existing) > 0:
        print(f"Resuming: {len(existing)} prior outcomes; {len(pending)} pending.")

    selected_transport = transport if transport is not None else _selected_transport()
    print(f"Using transport: {selected_transport}")

    write_lock = threading.Lock()
    halt = threading.Event()

    def _do_one(row: PoolRow) -> JudgeOutcome:
        if halt.is_set():
            return JudgeOutcome(
                pool_row_id=row.pool_row_id,
                annotator=row.annotator,
                task_id=row.task_id,
                benchmark=row.benchmark,
                domain=row.domain,
                prompt_kind=prompt_kind,
                judge_model=model,
                verdict=None,
                justification=None,
                sub_scores=None,
                parse_status="halted-budget-cap",
                input_tokens=0,
                output_tokens=0,
                cost_usd=0.0,
                elapsed_seconds=0.0,
            )
        return judge_one(
            row=row,
            prompt_kind=prompt_kind,
            model=model,
            system_prompt=system_prompt,
            user_template=user_template,
            transport=selected_transport,
        )

    with (
        output_jsonl_path.open("a", encoding="utf-8") as out_f,
        ThreadPoolExecutor(max_workers=max_workers) as executor,
    ):
        futures = {executor.submit(_do_one, row): row.pool_row_id for row in pending}
        for fut in as_completed(futures):
            outcome = fut.result()
            with write_lock:
                if outcome.parse_status == "halted-budget-cap":
                    continue
                _record(stats=stats, outcome=outcome, out_f=out_f, total=len(target))
                if stats.total_cost_usd >= budget_cap_usd:
                    print(
                        f"BUDGET CAP REACHED at running_total=${stats.total_cost_usd:.4f}; "
                        f"halting new submissions."
                    )
                    halt.set()
    return stats


def make_arg_parser(*, description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only the first N rows of the pool (validation gate uses 5).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Concurrent worker threads (default 2; the CLI subprocess is heavy).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=JUDGE_MODEL_ID,
        help=f"Anthropic model id (default {JUDGE_MODEL_ID}).",
    )
    parser.add_argument(
        "--transport",
        type=str,
        default=None,
        choices=["cli", "sdk"],
        help=(
            "Override the JUDGE_TRANSPORT env var. Default is `cli` (subscription-routed Sonnet "
            "quota); `sdk` requires a project Anthropic API key with Sonnet access."
        ),
    )
    parser.add_argument(
        "--budget-cap",
        type=float,
        default=BUDGET_CAP_USD,
        help=(
            f"Halt new submissions once running cost reaches this many USD "
            f"(default {BUDGET_CAP_USD:.2f})."
        ),
    )
    return parser
