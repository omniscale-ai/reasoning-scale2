"""Step 3 + 4: LLM-as-judge runner.

Calls the local `claude` CLI (Claude Code) with `--print --output-format json
--model claude-haiku-4-5-20251001` to audit a stratified sample of mapped
rows. Persists per-call costs to `code/_outputs/judge_costs.json` and merges
verdicts back into mapped rows, writing
`code/_outputs/mapped_with_judge.jsonl`.

Notes:

* Uses the local `claude` CLI to avoid requiring an explicit
  `ANTHROPIC_API_KEY` in `.env`.
* Single-shot verbalized-confidence prompt per Xiong2023.
* Budget cap enforced via running-total check after every call.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0005_hierarchical_annotation_pilot_v1.code.constants import (
    APPROX_CHARS_PER_TOKEN,
    HAIKU_INPUT_COST_PER_MTOK_USD,
    HAIKU_OUTPUT_COST_PER_MTOK_USD,
    JUDGE_BUDGET_CAP_USD,
    JUDGE_MODEL_ID,
    JUDGE_PROBLEM_EXCERPT_LIMIT,
    JUDGE_SYSTEM_PROMPT,
    JUDGE_USER_PROMPT_TEMPLATE,
)
from tasks.t0005_hierarchical_annotation_pilot_v1.code.paths import (
    JUDGE_COSTS_OUTPUT,
    JUDGE_SAMPLE_OUTPUT,
    MAPPED_OUTPUT,
    MAPPED_WITH_JUDGE_OUTPUT,
)


@dataclass(frozen=True, slots=True)
class JudgeOutcome:
    task_id: str
    pilot_row_index: int
    verdict: str | None
    justification: str | None
    notes: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


def _truncate(text: str, *, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "…"


def _build_prompt(*, row: dict[str, Any]) -> str:
    hierarchy = row["hierarchy"]
    subtasks = hierarchy["subtask"] or []
    atomic = hierarchy["atomic"] or []
    return JUDGE_USER_PROMPT_TEMPLATE.format(
        benchmark=row.get("benchmark", "?"),
        domain=row.get("domain", "?"),
        limit=JUDGE_PROBLEM_EXCERPT_LIMIT,
        problem_excerpt=_truncate(row.get("problem", ""), limit=JUDGE_PROBLEM_EXCERPT_LIMIT),
        global_label=hierarchy.get("global") or "(none)",
        subtasks_joined=" | ".join(subtasks) if subtasks else "(none)",
        atomic_joined=" | ".join(atomic) if atomic else "(none)",
    )


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // APPROX_CHARS_PER_TOKEN)


def _cost_usd(*, input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens * HAIKU_INPUT_COST_PER_MTOK_USD / 1_000_000.0
        + output_tokens * HAIKU_OUTPUT_COST_PER_MTOK_USD / 1_000_000.0
    )


def _call_claude_cli(*, prompt: str) -> tuple[str, int, int]:
    """Invoke the `claude` CLI with the given prompt.

    Returns the raw assistant text plus token counts when the CLI exposes
    them in JSON output. Falls back to character-based estimates otherwise.
    """

    full_prompt = f"<system>\n{JUDGE_SYSTEM_PROMPT}\n</system>\n\n{prompt}"
    cmd = [
        "claude",
        "-p",
        "-",
        "--model",
        JUDGE_MODEL_ID,
        "--output-format",
        "json",
    ]
    completed = subprocess.run(  # noqa: S603 — local trusted CLI
        cmd,
        input=full_prompt,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()[:300]
        raise RuntimeError(
            f"claude CLI exited {completed.returncode}: {stderr or '(no stderr)'}",
        )

    raw_stdout = completed.stdout.strip()
    if not raw_stdout:
        raise RuntimeError("claude CLI returned empty output")

    text = raw_stdout
    input_tokens = _estimate_tokens(full_prompt)
    output_tokens = _estimate_tokens(text)

    # If the CLI honoured --output-format json, the stdout itself is JSON
    # with `result` and `usage` keys.
    try:
        envelope = json.loads(raw_stdout)
    except json.JSONDecodeError:
        return text, input_tokens, output_tokens

    if isinstance(envelope, dict):
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

    return text, input_tokens, output_tokens


def _parse_verdict(*, raw_text: str) -> tuple[str | None, str | None, str]:
    """Parse the JSON verdict from the model's text output.

    Returns (verdict, justification, notes).
    """

    text = raw_text.strip()
    # Strip optional markdown fencing the model may add.
    if text.startswith("```"):
        text = text.strip("`")
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

    try:
        payload = json.loads(text)
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
        return None, justification, f"parse-failure: invalid verdict '{verdict_raw}'"

    return verdict_normalised, justification.strip(), "ok"


def judge_one(*, row: dict[str, Any]) -> JudgeOutcome:
    prompt = _build_prompt(row=row)
    text, input_tokens, output_tokens = _call_claude_cli(prompt=prompt)
    verdict, justification, notes = _parse_verdict(raw_text=text)
    pilot_row_index = int(row.get("_pilot_row_index", -1))
    return JudgeOutcome(
        task_id=str(row["task_id"]),
        pilot_row_index=pilot_row_index,
        verdict=verdict,
        justification=justification,
        notes=notes,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=_cost_usd(input_tokens=input_tokens, output_tokens=output_tokens),
    )


def _load_jsonl(*, path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def _write_jsonl(*, path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False))
            f.write("\n")


def main() -> None:
    sample_rows = _load_jsonl(path=JUDGE_SAMPLE_OUTPUT)
    mapped_rows = _load_jsonl(path=MAPPED_OUTPUT)

    outcomes: list[JudgeOutcome] = []
    running_cost = 0.0
    for index, row in enumerate(sample_rows, start=1):
        if running_cost >= JUDGE_BUDGET_CAP_USD:
            print(f"BUDGET CAP REACHED at row {index}; halting.")
            break
        try:
            outcome = judge_one(row=row)
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            outcome = JudgeOutcome(
                task_id=str(row["task_id"]),
                pilot_row_index=int(row.get("_pilot_row_index", -1)),
                verdict=None,
                justification=None,
                notes=f"call-failure: {exc}",
                input_tokens=0,
                output_tokens=0,
                cost_usd=0.0,
            )
        running_cost += outcome.cost_usd
        outcomes.append(outcome)
        print(
            f"[{index}/{len(sample_rows)}] {outcome.task_id} (idx {outcome.pilot_row_index}) "
            f"-> verdict={outcome.verdict} cost={outcome.cost_usd:.4f} "
            f"running_total={running_cost:.4f}",
        )

    # Merge verdicts back into mapped rows by row index (task_ids may repeat
    # across the source pilot file, so task_id is not a unique key).
    verdict_by_row_index: dict[int, JudgeOutcome] = {
        o.pilot_row_index: o for o in outcomes if o.pilot_row_index >= 0
    }
    for row_idx, row in enumerate(mapped_rows):
        outcome = verdict_by_row_index.get(row_idx)
        if outcome is None:
            continue
        row["judge_verdict"] = outcome.verdict
        row["judge_notes"] = outcome.justification or outcome.notes

    _write_jsonl(path=MAPPED_WITH_JUDGE_OUTPUT, rows=mapped_rows)

    JUDGE_COSTS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with JUDGE_COSTS_OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "model": JUDGE_MODEL_ID,
                "rows_judged": len(outcomes),
                "running_cost_usd": running_cost,
                "budget_cap_usd": JUDGE_BUDGET_CAP_USD,
                "per_call": [
                    {
                        "task_id": o.task_id,
                        "pilot_row_index": o.pilot_row_index,
                        "verdict": o.verdict,
                        "notes": o.notes,
                        "input_tokens": o.input_tokens,
                        "output_tokens": o.output_tokens,
                        "cost_usd": o.cost_usd,
                    }
                    for o in outcomes
                ],
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(
        f"Wrote {MAPPED_WITH_JUDGE_OUTPUT}\n"
        f"Wrote {JUDGE_COSTS_OUTPUT}\n"
        f"Total cost: ${running_cost:.4f}",
    )


if __name__ == "__main__":
    main()
