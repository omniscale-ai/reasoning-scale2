"""Stratified judge sample selector.

Per the t0014 plan REQ-4, the model-only delta requires the SAME 23 ``_pilot_row_index`` values
that t0009 used. We therefore load t0009's persisted sample directly and intersect it with the
v2-sonnet rows that have complete hierarchies. Random reproduction by seed is unreliable here:
when a sonnet call-failure drops a FrontierScience row from the eligible bucket, ``random.sample``
draws a *different* set on the same seed, breaking the same-sample guarantee.

If a sample row is missing from v2-sonnet (e.g. the sonnet annotator failed on it), we drop that
row and log the divergence. Downstream (compute_stats.py) ingests the v2-sonnet judge outcomes for
whichever indices we managed to judge; the model-only delta is reported on the intersection.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from tasks.t0014_v2_annotator_sonnet_rerun.code.paths import (
    V2_HAIKU_JUDGE_SAMPLE_PATH,
    V2_SONNET_JUDGE_SAMPLE_OUTPUT,
    V2_SONNET_RAW_OUTPUT,
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
    sonnet_rows = _load_jsonl(path=V2_SONNET_RAW_OUTPUT)
    sonnet_by_index: dict[int, dict[str, Any]] = {
        int(r["_pilot_row_index"]): r for r in sonnet_rows
    }

    haiku_sample_rows = _load_jsonl(path=V2_HAIKU_JUDGE_SAMPLE_PATH)
    target_indices: list[int] = [int(r["_pilot_row_index"]) for r in haiku_sample_rows]

    sample: list[dict[str, Any]] = []
    missing: list[int] = []
    incomplete: list[int] = []
    for idx in target_indices:
        sonnet_row = sonnet_by_index.get(idx)
        if sonnet_row is None:
            missing.append(idx)
            continue
        if not sonnet_row.get("hierarchy_completeness"):
            incomplete.append(idx)
            continue
        sample.append(sonnet_row)

    _write_jsonl(path=V2_SONNET_JUDGE_SAMPLE_OUTPUT, rows=sample)
    print(
        f"Wrote {V2_SONNET_JUDGE_SAMPLE_OUTPUT} with {len(sample)} rows "
        f"(target={len(target_indices)}, missing={len(missing)}, incomplete={len(incomplete)})."
    )
    counts: dict[str, int] = defaultdict(int)
    for row in sample:
        counts[row.get("benchmark", "")] += 1
    for bench, count in sorted(counts.items()):
        print(f"  {bench}: {count}")
    if missing:
        print(f"  missing _pilot_row_index in v2-sonnet: {missing}")
    if incomplete:
        print(f"  incomplete v2-sonnet hierarchies (call-failures): {incomplete}")
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description="Select stratified judge sample")
    parser.parse_args()
    select_sample()


if __name__ == "__main__":
    main()
