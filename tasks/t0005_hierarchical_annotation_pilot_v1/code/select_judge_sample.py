"""Step 4: stratified sampling of mapped rows for the LLM-as-judge spot-check.

Selects exactly `JUDGE_ROWS_PER_BENCHMARK` rows per benchmark (12 total). Uses
`JUDGE_RANDOM_SEED` for reproducibility. Within each benchmark, prefers rows
with `hierarchy_completeness == True` and a non-empty `atomic` list, but
includes at least one incomplete row when one exists for that benchmark so the
judge sees both shapes.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

from tasks.t0005_hierarchical_annotation_pilot_v1.code.constants import (
    ALL_BENCHMARKS,
    JUDGE_RANDOM_SEED,
    JUDGE_ROWS_PER_BENCHMARK,
)
from tasks.t0005_hierarchical_annotation_pilot_v1.code.paths import (
    JUDGE_SAMPLE_OUTPUT,
    MAPPED_OUTPUT,
)


@dataclass(frozen=True, slots=True)
class _RowRef:
    line_index: int
    benchmark: str
    completeness: bool


def _load_row_refs(*, mapped_path: Path) -> list[_RowRef]:
    refs: list[_RowRef] = []
    with mapped_path.open(encoding="utf-8") as f:
        for line_index, raw in enumerate(f):
            row = json.loads(raw)
            refs.append(
                _RowRef(
                    line_index=line_index,
                    benchmark=str(row.get("benchmark", "")),
                    completeness=bool(row.get("hierarchy_completeness")),
                ),
            )
    return refs


def _select_for_benchmark(
    *,
    refs: list[_RowRef],
    benchmark: str,
    rng: random.Random,
) -> list[int]:
    bench_refs = [r for r in refs if r.benchmark == benchmark]
    if len(bench_refs) <= JUDGE_ROWS_PER_BENCHMARK:
        return [r.line_index for r in bench_refs]

    complete = [r for r in bench_refs if r.completeness]
    incomplete = [r for r in bench_refs if not r.completeness]

    selection: list[_RowRef] = []
    if incomplete:
        # Include one incomplete row when at least one exists.
        selection.append(rng.choice(incomplete))

    pool = complete if complete else bench_refs
    remaining_target = JUDGE_ROWS_PER_BENCHMARK - len(selection)
    pool_minus_selection = [r for r in pool if r not in selection]
    rng.shuffle(pool_minus_selection)
    selection.extend(pool_minus_selection[:remaining_target])

    # Pad if still short (very small pool edge case).
    if len(selection) < JUDGE_ROWS_PER_BENCHMARK:
        leftovers = [r for r in bench_refs if r not in selection]
        rng.shuffle(leftovers)
        selection.extend(leftovers[: JUDGE_ROWS_PER_BENCHMARK - len(selection)])

    return [r.line_index for r in selection[:JUDGE_ROWS_PER_BENCHMARK]]


def main() -> None:
    rng = random.Random(JUDGE_RANDOM_SEED)
    refs = _load_row_refs(mapped_path=MAPPED_OUTPUT)
    selected_indices: set[int] = set()
    for benchmark in ALL_BENCHMARKS:
        selected_indices.update(
            _select_for_benchmark(refs=refs, benchmark=benchmark, rng=rng),
        )

    with MAPPED_OUTPUT.open(encoding="utf-8") as f:
        all_rows = [json.loads(line) for line in f]

    selected_rows: list[dict[str, object]] = []
    for idx, row in enumerate(all_rows):
        if idx in selected_indices:
            row_with_index = dict(row)
            row_with_index["_pilot_row_index"] = idx
            selected_rows.append(row_with_index)

    JUDGE_SAMPLE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with JUDGE_SAMPLE_OUTPUT.open("w", encoding="utf-8") as out:
        for row in selected_rows:
            out.write(json.dumps(row, ensure_ascii=False))
            out.write("\n")

    print(f"Selected {len(selected_rows)} rows -> {JUDGE_SAMPLE_OUTPUT}")
    bench_counts: dict[str, int] = {}
    for row in selected_rows:
        bench_counts[row["benchmark"]] = bench_counts.get(row["benchmark"], 0) + 1
    print(f"Per-benchmark counts: {bench_counts}")


if __name__ == "__main__":
    main()
