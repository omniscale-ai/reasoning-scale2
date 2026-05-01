"""V2 truncated LLM-as-judge runner (t0020).

Reads `_outputs/v2_truncated_judge_sample.jsonl` (the rows that survived annotation with complete
hierarchies), and calls claude-haiku-4-5 to verdict each one. The CRITICAL change vs t0009/t0014:
the judge sees the SAME 1500-char-truncated `problem` excerpt that the annotator saw, with a
header that explicitly states the truncation.

Idempotent: existing outcomes (keyed by `pilot_row_index`) are skipped.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tasks.t0020_v2_truncation_vs_schema_ablation.code.constants import (
    APPROX_CHARS_PER_TOKEN,
    HAIKU_INPUT_COST_PER_MTOK_USD,
    HAIKU_OUTPUT_COST_PER_MTOK_USD,
    JUDGE_BUDGET_CAP_USD,
    JUDGE_MODEL_ID,
    JUDGE_SYSTEM_PROMPT,
    JUDGE_USER_TEMPLATE,
    PROBLEM_EXCERPT_LIMIT,
    _truncate,
)
from tasks.t0020_v2_truncation_vs_schema_ablation.code.paths import (
    OUTPUTS_DIR,
    V2_TRUNCATED_JUDGE_COSTS_PATH,
    V2_TRUNCATED_JUDGE_OUTCOMES_PATH,
    V2_TRUNCATED_JUDGE_SAMPLE_OUTPUT,
)


@dataclass(frozen=True, slots=True)
class JudgeOutcome:
    pilot_row_index: int
    task_id: str
    benchmark: str
    verdict: str | None
    justification: str | None
    notes: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


@dataclass(slots=True)
class JudgeStats:
    rows_judged: int = 0
    rows_skipped: int = 0
    rows_acceptable: int = 0
    rows_needs_revision: int = 0
    rows_parse_failure: int = 0
    rows_call_failure: int = 0
    total_cost_usd: float = 0.0
    per_call: list[dict[str, Any]] = field(default_factory=list)


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // APPROX_CHARS_PER_TOKEN)


def _cost_usd(*, input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens * HAIKU_INPUT_COST_PER_MTOK_USD / 1_000_000.0
        + output_tokens * HAIKU_OUTPUT_COST_PER_MTOK_USD / 1_000_000.0
    )


@dataclass(frozen=True, slots=True)
class CliCallResult:
    text: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


def _call_claude_cli(*, prompt: str, model: str, system_prompt: str) -> CliCallResult:
    full_prompt = f"<system>\n{system_prompt}\n</system>\n\n{prompt}"
    cmd = [
        "claude",
        "-p",
        "-",
        "--model",
        model,
        "--output-format",
        "json",
    ]
    completed = subprocess.run(  # noqa: S603 — local trusted CLI
        cmd,
        input=full_prompt,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()[:500]
        raise RuntimeError(f"claude CLI exited {completed.returncode}: {stderr or '(no stderr)'}")
    raw_stdout = completed.stdout.strip()
    if not raw_stdout:
        raise RuntimeError("claude CLI returned empty output")

    text = raw_stdout
    input_tokens = _estimate_tokens(full_prompt)
    output_tokens = _estimate_tokens(text)
    cost_usd = _cost_usd(input_tokens=input_tokens, output_tokens=output_tokens)
    try:
        envelope = json.loads(raw_stdout)
    except json.JSONDecodeError:
        return CliCallResult(
            text=text, input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=cost_usd
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
    return CliCallResult(
        text=text, input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=cost_usd
    )


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    return text


def _extract_first_json_object(text: str) -> str | None:
    cleaned = _strip_fences(text)
    start = cleaned.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return cleaned[start : i + 1]
    return None


def _parse_verdict(*, raw_text: str) -> tuple[str | None, str | None, str]:
    snippet = _extract_first_json_object(raw_text)
    if snippet is None:
        return None, None, "parse-failure: no JSON object found"
    try:
        payload = json.loads(snippet)
    except json.JSONDecodeError as exc:
        return None, None, f"parse-failure: {exc}"
    if not isinstance(payload, dict):
        return None, None, "parse-failure: not a JSON object"
    verdict_raw = payload.get("verdict")
    justification = payload.get("justification")
    if not isinstance(verdict_raw, str) or not isinstance(justification, str):
        return None, None, "parse-failure: missing required fields"
    verdict_normalised = verdict_raw.strip().lower()
    if verdict_normalised not in {"acceptable", "needs revision"}:
        return None, justification.strip(), f"parse-failure: invalid verdict {verdict_raw!r}"
    return verdict_normalised, justification.strip(), "ok"


def _judge_one(*, row: dict[str, Any], model: str) -> JudgeOutcome:
    benchmark = str(row.get("benchmark", ""))
    domain = str(row.get("domain", ""))
    problem = str(row.get("problem", ""))
    pilot_row_index = int(row.get("_pilot_row_index", -1))
    task_id = str(row.get("task_id", ""))
    hierarchy = row.get("hierarchy", {})
    gold_actions = row.get("gold_actions", {})

    problem_excerpt = _truncate(problem, limit=PROBLEM_EXCERPT_LIMIT)
    prompt = JUDGE_USER_TEMPLATE.format(
        benchmark=benchmark,
        domain=domain,
        limit=PROBLEM_EXCERPT_LIMIT,
        problem_excerpt=problem_excerpt,
        hierarchy_json=json.dumps(hierarchy, ensure_ascii=False, indent=2),
        gold_actions_json=json.dumps(gold_actions, ensure_ascii=False, indent=2),
    )

    call = _call_claude_cli(prompt=prompt, model=model, system_prompt=JUDGE_SYSTEM_PROMPT)
    verdict, justification, notes = _parse_verdict(raw_text=call.text)

    return JudgeOutcome(
        pilot_row_index=pilot_row_index,
        task_id=task_id,
        benchmark=benchmark,
        verdict=verdict,
        justification=justification,
        notes=notes,
        input_tokens=call.input_tokens,
        output_tokens=call.output_tokens,
        cost_usd=call.cost_usd,
    )


def _load_jsonl(*, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _load_existing_indices(*, path: Path) -> set[int]:
    if not path.exists():
        return set()
    seen: set[int] = set()
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            idx = row.get("pilot_row_index")
            if isinstance(idx, int):
                seen.add(idx)
    return seen


def _judge_one_safe(*, row: dict[str, Any], model: str) -> JudgeOutcome:
    try:
        return _judge_one(row=row, model=model)
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        return JudgeOutcome(
            pilot_row_index=int(row.get("_pilot_row_index", -1)),
            task_id=str(row.get("task_id", "")),
            benchmark=str(row.get("benchmark", "")),
            verdict=None,
            justification=None,
            notes=f"call-failure: {exc}",
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
        )


def run_judge(*, limit: int | None, dry_run: bool, workers: int = 4) -> JudgeStats:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    sample = _load_jsonl(path=V2_TRUNCATED_JUDGE_SAMPLE_OUTPUT)
    existing = _load_existing_indices(path=V2_TRUNCATED_JUDGE_OUTCOMES_PATH)
    if existing:
        print(f"Found {len(existing)} prior judge outcomes; skipping those.")

    target = sample if limit is None else sample[:limit]
    stats = JudgeStats()
    pending = [
        (idx, row)
        for idx, row in enumerate(target)
        if int(row.get("_pilot_row_index", -1)) not in existing
    ]
    stats.rows_skipped = len(target) - len(pending)

    if not pending:
        print("All sample rows already judged; nothing to do.")
        _write_costs(stats=stats)
        return stats

    if dry_run:
        with V2_TRUNCATED_JUDGE_OUTCOMES_PATH.open("a", encoding="utf-8") as out_f:
            for _idx, row in pending:
                outcome = _judge_one_safe(row=row, model=JUDGE_MODEL_ID)
                _record_judge_outcome(stats=stats, outcome=outcome, out_f=out_f, total=len(target))
                if outcome.notes.startswith("parse-failure"):
                    print("DRY-RUN: parse failure; halting.")
                    break
        _write_costs(stats=stats)
        return stats

    write_lock = threading.Lock()
    halt = threading.Event()

    def _do_one(*, row: dict[str, Any]) -> JudgeOutcome:
        if halt.is_set():
            return JudgeOutcome(
                pilot_row_index=int(row.get("_pilot_row_index", -1)),
                task_id=str(row.get("task_id", "")),
                benchmark=str(row.get("benchmark", "")),
                verdict=None,
                justification=None,
                notes="halted-budget-cap",
                input_tokens=0,
                output_tokens=0,
                cost_usd=0.0,
            )
        return _judge_one_safe(row=row, model=JUDGE_MODEL_ID)

    with (
        V2_TRUNCATED_JUDGE_OUTCOMES_PATH.open("a", encoding="utf-8") as out_f,
        ThreadPoolExecutor(max_workers=workers) as executor,
    ):
        futures = {executor.submit(_do_one, row=row): idx for idx, row in pending}
        for fut in as_completed(futures):
            outcome = fut.result()
            with write_lock:
                if outcome.notes == "halted-budget-cap":
                    continue
                _record_judge_outcome(stats=stats, outcome=outcome, out_f=out_f, total=len(target))
                if stats.total_cost_usd >= JUDGE_BUDGET_CAP_USD:
                    print(
                        f"BUDGET CAP REACHED at running_total="
                        f"${stats.total_cost_usd:.4f}; halting new submissions."
                    )
                    halt.set()
    _write_costs(stats=stats)
    return stats


def _record_judge_outcome(
    *, stats: JudgeStats, outcome: JudgeOutcome, out_f: Any, total: int
) -> None:
    stats.total_cost_usd += outcome.cost_usd
    stats.rows_judged += 1
    if outcome.verdict == "acceptable":
        stats.rows_acceptable += 1
    elif outcome.verdict == "needs revision":
        stats.rows_needs_revision += 1
    elif outcome.notes.startswith("parse-failure"):
        stats.rows_parse_failure += 1
    elif outcome.notes.startswith("call-failure"):
        stats.rows_call_failure += 1

    stats.per_call.append(
        {
            "pilot_row_index": outcome.pilot_row_index,
            "task_id": outcome.task_id,
            "benchmark": outcome.benchmark,
            "verdict": outcome.verdict,
            "notes": outcome.notes,
            "cost_usd": outcome.cost_usd,
        }
    )

    print(
        f"[idx={outcome.pilot_row_index} of {total}] {outcome.benchmark} "
        f"task_id={outcome.task_id[:30]} verdict={outcome.verdict} "
        f"cost=${outcome.cost_usd:.4f} running=${stats.total_cost_usd:.4f}"
    )
    out_f.write(
        json.dumps(
            {
                "pilot_row_index": outcome.pilot_row_index,
                "task_id": outcome.task_id,
                "benchmark": outcome.benchmark,
                "verdict": outcome.verdict,
                "justification": outcome.justification,
                "notes": outcome.notes,
                "cost_usd": outcome.cost_usd,
            },
            ensure_ascii=False,
        )
    )
    out_f.write("\n")
    out_f.flush()


def _write_costs(*, stats: JudgeStats) -> None:
    V2_TRUNCATED_JUDGE_COSTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": JUDGE_MODEL_ID,
        "rows_judged": stats.rows_judged,
        "rows_skipped": stats.rows_skipped,
        "rows_acceptable": stats.rows_acceptable,
        "rows_needs_revision": stats.rows_needs_revision,
        "rows_parse_failure": stats.rows_parse_failure,
        "rows_call_failure": stats.rows_call_failure,
        "total_cost_usd": stats.total_cost_usd,
        "budget_cap_usd": JUDGE_BUDGET_CAP_USD,
        "problem_excerpt_limit": PROBLEM_EXCERPT_LIMIT,
        "per_call": stats.per_call,
    }
    if V2_TRUNCATED_JUDGE_COSTS_PATH.exists():
        try:
            previous = json.loads(V2_TRUNCATED_JUDGE_COSTS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = None
        if isinstance(previous, dict):
            payload["rows_judged"] += int(previous.get("rows_judged", 0))
            payload["rows_skipped"] += int(previous.get("rows_skipped", 0))
            payload["rows_acceptable"] += int(previous.get("rows_acceptable", 0))
            payload["rows_needs_revision"] += int(previous.get("rows_needs_revision", 0))
            payload["rows_parse_failure"] += int(previous.get("rows_parse_failure", 0))
            payload["rows_call_failure"] += int(previous.get("rows_call_failure", 0))
            payload["total_cost_usd"] += float(previous.get("total_cost_usd", 0.0))
            prev_calls = previous.get("per_call", [])
            if isinstance(prev_calls, list):
                payload["per_call"] = prev_calls + payload["per_call"]
    V2_TRUNCATED_JUDGE_COSTS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(
        f"Wrote {V2_TRUNCATED_JUDGE_COSTS_PATH} "
        f"(running_total=${payload['total_cost_usd']:.4f}, "
        f"acceptable={payload['rows_acceptable']}, "
        f"needs_revision={payload['rows_needs_revision']})"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v2 truncated LLM-as-judge")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    stats = run_judge(limit=args.limit, dry_run=args.dry_run, workers=args.workers)
    print(
        f"DONE. judged={stats.rows_judged}, skipped={stats.rows_skipped}, "
        f"acceptable={stats.rows_acceptable}, needs_revision={stats.rows_needs_revision}, "
        f"parse_failures={stats.rows_parse_failure}, "
        f"call_failures={stats.rows_call_failure}, "
        f"total_cost=${stats.total_cost_usd:.4f}"
    )


if __name__ == "__main__":
    main()
