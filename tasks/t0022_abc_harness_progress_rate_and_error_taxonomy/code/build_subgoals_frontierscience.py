"""Build the FrontierScience-Olympiad subgoal JSON from t0012 gold annotations.

Reads the t0012 prediction JSONLs (which carry `gold_answer` fields containing the
official hierarchical decomposition with GLOBAL / SUBTASK / ATOM lines) and emits
one EnvironmentSubgoals entry per unique task_id, taking the SUBTASK lines as the
intermediate-milestone subgoal list.

Output format (matches the schema documented in plan.md Step 7):

    [
      {
        "environment_id": "fs_<uuid>",
        "subgoals": [
          {"id": "g1", "description": "<SUBTASK summary>"},
          ...
        ]
      },
      ...
    ]

Run via:
    uv run python -m \\
        tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.build_subgoals_frontierscience
"""  # noqa: E501

from __future__ import annotations

import json
from typing import Any

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.paths import (
    LIBRARY_ASSET_FILES_DIR,
    SUBGOALS_FRONTIERSCIENCE_JSON,
    T0012_PRED_A,
    T0012_PRED_B,
    T0012_PRED_C,
)

MIN_SUBGOALS_PER_TASK: int = 3
MAX_SUBGOALS_PER_TASK: int = 5
MAX_DESCRIPTION_CHARS: int = 240


def _parse_subtasks_from_gold(*, gold_answer: str) -> list[str]:
    """Return SUBTASK descriptions from a FrontierScience gold-answer block."""
    subtasks: list[str] = []
    for raw_line in gold_answer.splitlines():
        line = raw_line.strip()
        if line.startswith("SUBTASK:"):
            description = line[len("SUBTASK:") :].strip()
            if description:
                subtasks.append(description)
    return subtasks


def _truncate(*, text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def _select_subgoals(*, subtasks: list[str]) -> list[str]:
    """Trim to a manageable count per environment."""
    if len(subtasks) <= MAX_SUBGOALS_PER_TASK:
        return subtasks
    # Take first, last, and evenly-spaced middle entries to preserve coverage.
    chosen_indices: list[int] = [0]
    step = (len(subtasks) - 1) / (MAX_SUBGOALS_PER_TASK - 1)
    for i in range(1, MAX_SUBGOALS_PER_TASK - 1):
        chosen_indices.append(round(i * step))
    chosen_indices.append(len(subtasks) - 1)
    # De-dup while preserving order.
    seen: set[int] = set()
    unique_indices: list[int] = []
    for idx in chosen_indices:
        if idx not in seen:
            seen.add(idx)
            unique_indices.append(idx)
    return [subtasks[i] for i in unique_indices]


def _build_one(*, task_id: str, gold_answer: str) -> dict[str, Any] | None:
    subtasks = _parse_subtasks_from_gold(gold_answer=gold_answer)
    if len(subtasks) == 0:
        return None
    selected = _select_subgoals(subtasks=subtasks)
    if len(selected) < MIN_SUBGOALS_PER_TASK:
        # Pad by re-using the first subtask if needed; this should not happen often,
        # but guarantees the schema invariant min >= 3.
        while len(selected) < MIN_SUBGOALS_PER_TASK:
            selected.append(selected[-1])
    return {
        "environment_id": task_id,
        "subgoals": [
            {
                "id": f"g{i + 1}",
                "description": _truncate(text=desc, max_chars=MAX_DESCRIPTION_CHARS),
            }
            for i, desc in enumerate(selected)
        ],
    }


def main() -> None:
    seen: set[str] = set()
    environments: list[dict[str, Any]] = []
    for path in (T0012_PRED_A, T0012_PRED_B, T0012_PRED_C):
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                task_id = row.get("task_id")
                gold = row.get("gold_answer", "")
                if not isinstance(task_id, str) or task_id in seen:
                    continue
                if not isinstance(gold, str) or len(gold) == 0:
                    continue
                env = _build_one(task_id=task_id, gold_answer=gold)
                if env is None:
                    continue
                seen.add(task_id)
                environments.append(env)
    LIBRARY_ASSET_FILES_DIR.mkdir(parents=True, exist_ok=True)
    SUBGOALS_FRONTIERSCIENCE_JSON.write_text(
        json.dumps(environments, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(environments)} environments to {SUBGOALS_FRONTIERSCIENCE_JSON}")
    sub_counts = [len(e["subgoals"]) for e in environments]
    if len(sub_counts) > 0:
        mean_subgoals = sum(sub_counts) / len(sub_counts)
        print(
            f"  subgoals/env: min={min(sub_counts)} max={max(sub_counts)} mean={mean_subgoals:.1f}"
        )


if __name__ == "__main__":
    main()
