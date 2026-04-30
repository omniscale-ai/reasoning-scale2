"""V2 hierarchical annotator: re-annotates v1 rows under a tree-shaped schema.

Reads `tasks/t0005_hierarchical_annotation_pilot_v1/.../hierarchical_annotation_v1.jsonl`
(115 rows), passes the FULL `problem` text plus benchmark/domain to claude-sonnet-4-6 via the
local `claude` CLI, parses the JSON tree response, and writes one v2-shaped row per input row to
`code/_outputs/v2_annotated.jsonl`.

Idempotence: existing rows in the output file are kept; only missing `_pilot_row_index` rows are
re-attempted on re-runs.

Budget: hard halt when running cost approaches `ANNOTATOR_BUDGET_CAP_USD`.
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

from tasks.t0014_v2_annotator_sonnet_rerun.code.constants import (
    ANNOTATOR_BUDGET_CAP_USD,
    ANNOTATOR_MODEL_ID,
    ANNOTATOR_SYSTEM_PROMPT,
    ANNOTATOR_USER_TEMPLATE,
    APPROX_CHARS_PER_TOKEN,
    SONNET_INPUT_COST_PER_MTOK_USD,
    SONNET_OUTPUT_COST_PER_MTOK_USD,
)
from tasks.t0014_v2_annotator_sonnet_rerun.code.paths import (
    OUTPUTS_DIR,
    V1_INPUT_PATH,
    V2_SONNET_ANNOTATOR_COSTS_PATH,
    V2_SONNET_RAW_OUTPUT,
)


@dataclass(frozen=True, slots=True)
class AnnotationOutcome:
    pilot_row_index: int
    task_id: str
    benchmark: str
    domain: str
    problem: str
    difficulty: Any
    raw_response: str
    parsed_hierarchy: dict[str, Any] | None
    parsed_gold_actions: dict[str, Any] | None
    notes: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


@dataclass(slots=True)
class RunStats:
    rows_annotated: int = 0
    rows_skipped: int = 0
    rows_with_parse_failure: int = 0
    rows_with_call_failure: int = 0
    rows_with_complete_hierarchy: int = 0
    total_cost_usd: float = 0.0
    per_call: list[dict[str, Any]] = field(default_factory=list)


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // APPROX_CHARS_PER_TOKEN)


def _cost_usd(*, input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens * SONNET_INPUT_COST_PER_MTOK_USD / 1_000_000.0
        + output_tokens * SONNET_OUTPUT_COST_PER_MTOK_USD / 1_000_000.0
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
        # Strip leading triple-backtick line.
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    return text


def _extract_first_json_object(text: str) -> str | None:
    """Best-effort: extract the first balanced top-level JSON object from text."""

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


def _parse_v2_response(raw_text: str) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str]:
    """Return (hierarchy, gold_actions, notes)."""

    snippet = _extract_first_json_object(raw_text)
    if snippet is None:
        return None, None, "parse-failure: no JSON object found"

    try:
        payload = json.loads(snippet)
    except json.JSONDecodeError as exc:
        return None, None, f"parse-failure: {exc}"

    if not isinstance(payload, dict):
        return None, None, "parse-failure: top-level value is not a JSON object"

    global_label = payload.get("global")
    subtasks_raw = payload.get("subtasks")
    global_atomics_raw = payload.get("global_atomics")
    gold_actions_raw = payload.get("gold_actions")

    if not isinstance(global_label, str):
        return None, None, "parse-failure: missing 'global' string"

    if not isinstance(subtasks_raw, list):
        return None, None, "parse-failure: missing 'subtasks' list"

    subtasks: list[dict[str, Any]] = []
    for entry in subtasks_raw:
        if not isinstance(entry, dict):
            return None, None, "parse-failure: subtasks[i] is not an object"
        sub = entry.get("subtask")
        atoms = entry.get("atomics")
        if not isinstance(sub, str) or not isinstance(atoms, list):
            return None, None, "parse-failure: subtask object missing required fields"
        subtasks.append(
            {
                "subtask": sub,
                "atomics": [str(a) for a in atoms if isinstance(a, str)],
            }
        )

    if not isinstance(global_atomics_raw, list):
        return None, None, "parse-failure: missing 'global_atomics' list"

    global_atomics: list[str] = [str(a) for a in global_atomics_raw if isinstance(a, str)]

    hierarchy: dict[str, Any] = {
        "global": global_label.strip() or None,
        "subtasks": subtasks,
        "global_atomics": global_atomics,
    }

    if hierarchy["global"] is None:
        return None, None, "parse-failure: 'global' is empty"

    # Gold actions: if missing or malformed, fall back to a copy of hierarchy.
    if isinstance(gold_actions_raw, dict):
        ga_global = gold_actions_raw.get("global")
        ga_subtasks_raw = gold_actions_raw.get("subtasks")
        ga_global_atomics_raw = gold_actions_raw.get("global_atomics")

        ga_subtasks: list[dict[str, Any]] = []
        if isinstance(ga_subtasks_raw, list):
            for entry in ga_subtasks_raw:
                if not isinstance(entry, dict):
                    continue
                sub = entry.get("subtask")
                atoms = entry.get("atomics")
                if isinstance(sub, str) and isinstance(atoms, list):
                    ga_subtasks.append(
                        {
                            "subtask": sub,
                            "atomics": [str(a) for a in atoms if isinstance(a, str)],
                        }
                    )

        gold_atomics: list[str] = []
        if isinstance(ga_global_atomics_raw, list):
            gold_atomics = [str(a) for a in ga_global_atomics_raw if isinstance(a, str)]

        gold_actions: dict[str, Any] = {
            "global": ga_global if isinstance(ga_global, str) else None,
            "subtasks": ga_subtasks,
            "global_atomics": gold_atomics,
        }
    else:
        gold_actions = {
            "global": hierarchy["global"],
            "subtasks": [
                {"subtask": s["subtask"], "atomics": list(s["atomics"])} for s in subtasks
            ],
            "global_atomics": list(global_atomics),
        }

    return hierarchy, gold_actions, "ok"


def _is_complete_hierarchy(hierarchy: dict[str, Any] | None) -> bool:
    if hierarchy is None:
        return False
    if hierarchy.get("global") is None:
        return False
    has_subtask_atomics = any(len(s.get("atomics", [])) > 0 for s in hierarchy.get("subtasks", []))
    has_global_atomics = len(hierarchy.get("global_atomics", [])) > 0
    return has_subtask_atomics or has_global_atomics


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
            idx = row.get("_pilot_row_index")
            if isinstance(idx, int):
                seen.add(idx)
    return seen


def _row_to_output(*, row: dict[str, Any], outcome: AnnotationOutcome) -> dict[str, Any]:
    completeness = _is_complete_hierarchy(outcome.parsed_hierarchy)
    if outcome.parsed_hierarchy is not None:
        hierarchy = outcome.parsed_hierarchy
    else:
        hierarchy = {"global": None, "subtasks": [], "global_atomics": []}
    if outcome.parsed_gold_actions is not None:
        gold_actions = outcome.parsed_gold_actions
    else:
        gold_actions = {"global": None, "subtasks": [], "global_atomics": []}
    return {
        "_pilot_row_index": outcome.pilot_row_index,
        "task_id": outcome.task_id,
        "benchmark": outcome.benchmark,
        "domain": outcome.domain,
        "difficulty": outcome.difficulty,
        "problem": outcome.problem,
        "hierarchy": hierarchy,
        "gold_actions": gold_actions,
        "annotation_model": ANNOTATOR_MODEL_ID,
        "judge_verdict": None,
        "judge_notes": None,
        "hierarchy_completeness": completeness,
        "annotator_notes": outcome.notes,
    }


def _annotate_one(*, pilot_row_index: int, row: dict[str, Any], model: str) -> AnnotationOutcome:
    benchmark = str(row.get("benchmark", ""))
    domain = str(row.get("domain", ""))
    problem = str(row.get("problem", ""))
    difficulty = row.get("difficulty")
    task_id = str(row.get("task_id", ""))
    user_prompt = ANNOTATOR_USER_TEMPLATE.format(
        benchmark=benchmark, domain=domain, problem=problem
    )
    call = _call_claude_cli(prompt=user_prompt, model=model, system_prompt=ANNOTATOR_SYSTEM_PROMPT)
    hierarchy, gold_actions, notes = _parse_v2_response(call.text)
    return AnnotationOutcome(
        pilot_row_index=pilot_row_index,
        task_id=task_id,
        benchmark=benchmark,
        domain=domain,
        problem=problem,
        difficulty=difficulty,
        raw_response=call.text,
        parsed_hierarchy=hierarchy,
        parsed_gold_actions=gold_actions,
        notes=notes,
        input_tokens=call.input_tokens,
        output_tokens=call.output_tokens,
        cost_usd=call.cost_usd,
    )


def _annotate_one_safe(
    *, pilot_row_index: int, row: dict[str, Any], model: str
) -> AnnotationOutcome:
    """Annotate one row, swallowing call/timeout errors into a notes field."""
    try:
        return _annotate_one(pilot_row_index=pilot_row_index, row=row, model=model)
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        return AnnotationOutcome(
            pilot_row_index=pilot_row_index,
            task_id=str(row.get("task_id", "")),
            benchmark=str(row.get("benchmark", "")),
            domain=str(row.get("domain", "")),
            problem=str(row.get("problem", "")),
            difficulty=row.get("difficulty"),
            raw_response="",
            parsed_hierarchy=None,
            parsed_gold_actions=None,
            notes=f"call-failure: {exc}",
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
        )


def run_annotator(*, limit: int | None, dry_run: bool, workers: int = 4) -> RunStats:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = _load_jsonl(path=V1_INPUT_PATH)
    print(f"Loaded {len(rows)} rows from {V1_INPUT_PATH}")
    existing = _load_existing_indices(path=V2_SONNET_RAW_OUTPUT)
    if existing:
        print(
            f"Found {len(existing)} already-annotated rows in "
            f"{V2_SONNET_RAW_OUTPUT}; skipping those."
        )

    stats = RunStats()
    target_rows = rows if limit is None else rows[:limit]
    pending: list[tuple[int, dict[str, Any]]] = [
        (idx, row) for idx, row in enumerate(target_rows) if idx not in existing
    ]
    stats.rows_skipped = len(existing)

    if not pending:
        print("All rows already annotated; nothing to do.")
        _write_costs(stats=stats)
        return stats

    if dry_run:
        # Sequential dry-run: run a few rows, halt on first parse failure.
        with V2_SONNET_RAW_OUTPUT.open("a", encoding="utf-8") as out_f:
            for pilot_row_index, row in pending:
                outcome = _annotate_one_safe(
                    pilot_row_index=pilot_row_index, row=row, model=ANNOTATOR_MODEL_ID
                )
                _record_outcome(
                    stats=stats, outcome=outcome, row=row, out_f=out_f, total=len(pending)
                )
                if outcome.notes.startswith("parse-failure"):
                    print(
                        "DRY-RUN: parse failure encountered; halting before full run.\n"
                        f"Raw response head:\n{outcome.raw_response[:500]}"
                    )
                    break
        _write_costs(stats=stats)
        return stats

    # Parallel mode: dispatch workers via ThreadPoolExecutor; serialize writes via a Lock.
    write_lock = threading.Lock()
    halt = threading.Event()

    def _do_one(*, pilot_row_index: int, row: dict[str, Any]) -> AnnotationOutcome:
        if halt.is_set():
            return AnnotationOutcome(
                pilot_row_index=pilot_row_index,
                task_id=str(row.get("task_id", "")),
                benchmark=str(row.get("benchmark", "")),
                domain=str(row.get("domain", "")),
                problem=str(row.get("problem", "")),
                difficulty=row.get("difficulty"),
                raw_response="",
                parsed_hierarchy=None,
                parsed_gold_actions=None,
                notes="halted-budget-cap",
                input_tokens=0,
                output_tokens=0,
                cost_usd=0.0,
            )
        return _annotate_one_safe(
            pilot_row_index=pilot_row_index, row=row, model=ANNOTATOR_MODEL_ID
        )

    with (
        V2_SONNET_RAW_OUTPUT.open("a", encoding="utf-8") as out_f,
        ThreadPoolExecutor(max_workers=workers) as executor,
    ):
        futures = {
            executor.submit(_do_one, pilot_row_index=idx, row=row): idx for idx, row in pending
        }
        for fut in as_completed(futures):
            outcome = fut.result()
            idx = futures[fut]
            row = target_rows[idx]
            with write_lock:
                if outcome.notes == "halted-budget-cap":
                    continue
                _record_outcome(
                    stats=stats,
                    outcome=outcome,
                    row=row,
                    out_f=out_f,
                    total=len(pending),
                )
                if stats.total_cost_usd >= ANNOTATOR_BUDGET_CAP_USD:
                    print(
                        f"BUDGET CAP REACHED at running_total="
                        f"${stats.total_cost_usd:.4f}; halting new submissions."
                    )
                    halt.set()
    _write_costs(stats=stats)
    return stats


def _record_outcome(
    *,
    stats: RunStats,
    outcome: AnnotationOutcome,
    row: dict[str, Any],
    out_f: Any,
    total: int,
) -> None:
    stats.total_cost_usd += outcome.cost_usd
    output_row = _row_to_output(row=row, outcome=outcome)

    if outcome.parsed_hierarchy is not None:
        stats.rows_annotated += 1
        if outcome.parsed_hierarchy.get("global") and _is_complete_hierarchy(
            outcome.parsed_hierarchy
        ):
            stats.rows_with_complete_hierarchy += 1
    elif outcome.notes.startswith("parse-failure"):
        stats.rows_with_parse_failure += 1
    elif outcome.notes.startswith("call-failure"):
        stats.rows_with_call_failure += 1

    stats.per_call.append(
        {
            "pilot_row_index": outcome.pilot_row_index,
            "task_id": outcome.task_id,
            "benchmark": outcome.benchmark,
            "input_tokens": outcome.input_tokens,
            "output_tokens": outcome.output_tokens,
            "cost_usd": outcome.cost_usd,
            "notes": outcome.notes,
        }
    )
    print(
        f"[idx={outcome.pilot_row_index} of {total}] {outcome.benchmark} "
        f"task_id={outcome.task_id[:30]} notes={outcome.notes[:30]} "
        f"cost=${outcome.cost_usd:.4f} running=${stats.total_cost_usd:.4f}"
    )
    out_f.write(json.dumps(output_row, ensure_ascii=False))
    out_f.write("\n")
    out_f.flush()


def _write_costs(*, stats: RunStats) -> None:
    V2_SONNET_ANNOTATOR_COSTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": ANNOTATOR_MODEL_ID,
        "rows_annotated": stats.rows_annotated,
        "rows_skipped": stats.rows_skipped,
        "rows_with_parse_failure": stats.rows_with_parse_failure,
        "rows_with_call_failure": stats.rows_with_call_failure,
        "rows_with_complete_hierarchy": stats.rows_with_complete_hierarchy,
        "total_cost_usd": stats.total_cost_usd,
        "budget_cap_usd": ANNOTATOR_BUDGET_CAP_USD,
        "per_call": stats.per_call,
    }
    # Merge into an existing file if present (idempotent re-runs append).
    if V2_SONNET_ANNOTATOR_COSTS_PATH.exists():
        try:
            previous = json.loads(V2_SONNET_ANNOTATOR_COSTS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = None
        if isinstance(previous, dict):
            payload["rows_annotated"] += int(previous.get("rows_annotated", 0))
            payload["rows_skipped"] += int(previous.get("rows_skipped", 0))
            payload["rows_with_parse_failure"] += int(previous.get("rows_with_parse_failure", 0))
            payload["rows_with_call_failure"] += int(previous.get("rows_with_call_failure", 0))
            payload["rows_with_complete_hierarchy"] += int(
                previous.get("rows_with_complete_hierarchy", 0)
            )
            payload["total_cost_usd"] += float(previous.get("total_cost_usd", 0.0))
            prev_calls = previous.get("per_call", [])
            if isinstance(prev_calls, list):
                payload["per_call"] = prev_calls + payload["per_call"]
    V2_SONNET_ANNOTATOR_COSTS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(
        f"Wrote {V2_SONNET_ANNOTATOR_COSTS_PATH} (running_total=${payload['total_cost_usd']:.4f}, "
        f"complete_rows={payload['rows_with_complete_hierarchy']})"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run v2 hierarchical annotator")
    parser.add_argument("--limit", type=int, default=None, help="Limit to first N rows")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Halt on first parse failure for inspection",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Concurrent worker threads (each calls the claude CLI)",
    )
    args = parser.parse_args()
    stats = run_annotator(limit=args.limit, dry_run=args.dry_run, workers=args.workers)
    print(
        f"DONE. annotated={stats.rows_annotated}, skipped={stats.rows_skipped}, "
        f"parse_failures={stats.rows_with_parse_failure}, "
        f"call_failures={stats.rows_with_call_failure}, "
        f"complete_hierarchy={stats.rows_with_complete_hierarchy}, "
        f"total_cost=${stats.total_cost_usd:.4f}"
    )


if __name__ == "__main__":
    main()
