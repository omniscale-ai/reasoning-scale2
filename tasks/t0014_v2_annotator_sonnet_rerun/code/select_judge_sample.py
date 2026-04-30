"""Stratified judge sample selector.

Reads the v2-annotated jsonl, partitions by `benchmark`, and uses a fixed-seeded random.Random
to draw `JUDGE_SAMPLE_PER_BENCHMARK[bench]` rows from each bucket without replacement. Only rows
with `hierarchy_completeness == True` are sampled (incomplete rows would distort the judge view).
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from tasks.t0014_v2_annotator_sonnet_rerun.code.constants import (
    JUDGE_SAMPLE_PER_BENCHMARK,
    SAMPLE_SEED,
)
from tasks.t0014_v2_annotator_sonnet_rerun.code.paths import (
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
    rows = _load_jsonl(path=V2_SONNET_RAW_OUTPUT)
    by_benchmark: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if not row.get("hierarchy_completeness"):
            continue
        by_benchmark[row.get("benchmark", "")].append(row)

    rng = random.Random(SAMPLE_SEED)  # noqa: S311 - reproducible sample, not crypto
    sample: list[dict[str, Any]] = []
    for benchmark, target in JUDGE_SAMPLE_PER_BENCHMARK.items():
        bucket = by_benchmark.get(benchmark, [])
        if len(bucket) < target:
            print(
                f"WARN: benchmark {benchmark!r} has only {len(bucket)} complete rows "
                f"(need {target}); using all of them."
            )
            sample.extend(bucket)
            continue
        chosen = rng.sample(bucket, target)
        sample.extend(chosen)

    _write_jsonl(path=V2_SONNET_JUDGE_SAMPLE_OUTPUT, rows=sample)
    print(f"Wrote {V2_SONNET_JUDGE_SAMPLE_OUTPUT} with {len(sample)} rows.")
    counts: dict[str, int] = defaultdict(int)
    for row in sample:
        counts[row.get("benchmark", "")] += 1
    for bench, count in sorted(counts.items()):
        print(f"  {bench}: {count}")
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description="Select stratified judge sample")
    parser.parse_args()
    select_sample()


if __name__ == "__main__":
    main()
