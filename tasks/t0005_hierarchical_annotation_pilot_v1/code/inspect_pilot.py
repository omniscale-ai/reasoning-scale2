"""Step 1: inspect the pilot file and confirm the granularity-label state.

Loads `project/data/annotation_pilot/tasks_annotated.jsonl` and prints
per-benchmark counts, key presence, node-type distribution, and the count of
rows with `errors` or `steps == null`. Read-only; emits no files.

Usage:
    uv run python -m tasks.t0005_hierarchical_annotation_pilot_v1.code.inspect_pilot
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from tasks.t0005_hierarchical_annotation_pilot_v1.code.paths import PILOT_INPUT


@dataclass(frozen=True, slots=True)
class PilotInspectionReport:
    total_rows: int
    rows_per_benchmark: dict[str, int]
    rows_with_errors: int
    rows_with_null_steps: int
    rows_with_explicit_hierarchy: int
    node_type_counts: dict[str, int]
    keys_observed: list[str]


def inspect_pilot(*, file_path: Path) -> PilotInspectionReport:
    rows_per_benchmark: Counter[str] = Counter()
    node_type_counts: Counter[str] = Counter()
    keys_observed: set[str] = set()
    rows_with_errors = 0
    rows_with_null_steps = 0
    rows_with_explicit_hierarchy = 0
    total = 0

    with file_path.open(encoding="utf-8") as f:
        for raw_line in f:
            row = json.loads(raw_line)
            total += 1
            keys_observed.update(row.keys())
            rows_per_benchmark[row.get("benchmark", "?")] += 1

            if row.get("errors"):
                rows_with_errors += 1

            steps = row.get("steps")
            if steps is None:
                rows_with_null_steps += 1
            elif isinstance(steps, dict) and isinstance(steps.get("nodes"), list):
                for node in steps["nodes"]:
                    node_type_counts[str(node.get("type", "?"))] += 1

            if "hierarchy" in row:
                rows_with_explicit_hierarchy += 1

    return PilotInspectionReport(
        total_rows=total,
        rows_per_benchmark=dict(rows_per_benchmark),
        rows_with_errors=rows_with_errors,
        rows_with_null_steps=rows_with_null_steps,
        rows_with_explicit_hierarchy=rows_with_explicit_hierarchy,
        node_type_counts=dict(node_type_counts),
        keys_observed=sorted(keys_observed),
    )


def main() -> None:
    report = inspect_pilot(file_path=PILOT_INPUT)
    print(
        json.dumps(
            {
                "total_rows": report.total_rows,
                "rows_per_benchmark": report.rows_per_benchmark,
                "rows_with_errors": report.rows_with_errors,
                "rows_with_null_steps": report.rows_with_null_steps,
                "rows_with_explicit_hierarchy": report.rows_with_explicit_hierarchy,
                "node_type_counts": report.node_type_counts,
                "keys_observed": report.keys_observed,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
