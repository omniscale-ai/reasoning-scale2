"""Truncated judge sample selector (t0020).

Filters the truncated annotator output to rows with `hierarchy_completeness == True`. The set of
target indices is fixed by the t0014 sonnet judge sample (20 rows); we drop rows where the haiku
truncated annotator failed (call-failure or parse-failure).
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from tasks.t0020_v2_truncation_vs_schema_ablation.code.paths import (
    T0014_SONNET_JUDGE_SAMPLE_PATH,
    V2_TRUNCATED_JUDGE_SAMPLE_OUTPUT,
    V2_TRUNCATED_RAW_OUTPUT,
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


def _write_jsonl(*, path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False))
            f.write("\n")


def select_sample() -> list[dict[str, Any]]:
    annotated_rows = _load_jsonl(path=V2_TRUNCATED_RAW_OUTPUT)
    annotated_by_index: dict[int, dict[str, Any]] = {
        int(r["_pilot_row_index"]): r for r in annotated_rows
    }

    sonnet_sample_rows = _load_jsonl(path=T0014_SONNET_JUDGE_SAMPLE_PATH)
    target_indices: list[int] = [int(r["_pilot_row_index"]) for r in sonnet_sample_rows]

    sample: list[dict[str, Any]] = []
    missing: list[int] = []
    incomplete: list[int] = []
    for idx in target_indices:
        annotated_row = annotated_by_index.get(idx)
        if annotated_row is None:
            missing.append(idx)
            continue
        if not annotated_row.get("hierarchy_completeness"):
            incomplete.append(idx)
            continue
        sample.append(annotated_row)

    _write_jsonl(path=V2_TRUNCATED_JUDGE_SAMPLE_OUTPUT, rows=sample)
    print(
        f"Wrote {V2_TRUNCATED_JUDGE_SAMPLE_OUTPUT} with {len(sample)} rows "
        f"(target={len(target_indices)}, missing={len(missing)}, incomplete={len(incomplete)})."
    )
    counts: dict[str, int] = defaultdict(int)
    for row in sample:
        counts[row.get("benchmark", "")] += 1
    for bench, count in sorted(counts.items()):
        print(f"  {bench}: {count}")
    if missing:
        print(f"  missing _pilot_row_index in v2-truncated annotated: {missing}")
    if incomplete:
        print(f"  incomplete v2-truncated hierarchies (call/parse failures): {incomplete}")
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description="Select truncated judge sample")
    parser.parse_args()
    select_sample()


if __name__ == "__main__":
    main()
