"""Row pool loader for t0019.

Reads the three input JSONL files (v2-sonnet, v2-haiku-corrected, v1-sonnet-with-judge), filters to
rows with a non-null `judge_verdict`, applies the t0015 benchmark-label correction overlay
automatically (by reading the corrected file rather than the raw t0009 source for v2-haiku), and
normalizes every selected row into a `PoolRow` frozen dataclass.

The v1-sonnet rows lack a `_pilot_row_index`. We synthesize a stable row id by ordinal position in
the file, prefixed with the annotator label so it cannot collide with the v2 indices.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0019_v2_judge_calibration_sonnet.code.constants import (
    ANNOTATOR_V1_SONNET,
    ANNOTATOR_V2_HAIKU,
    ANNOTATOR_V2_SONNET,
)
from tasks.t0019_v2_judge_calibration_sonnet.code.paths import (
    V1_SONNET_INPUT_PATH,
    V2_HAIKU_CORRECTED_INPUT_PATH,
    V2_SONNET_INPUT_PATH,
)


@dataclass(frozen=True, slots=True)
class PoolRow:
    pool_row_id: str
    annotator: str
    task_id: str
    benchmark: str
    domain: str
    problem: str
    hierarchy: dict[str, Any]
    gold_actions: dict[str, Any]
    baseline_verdict: str
    source_file: str


def _read_jsonl(*, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if len(stripped) == 0:
                continue
            rows.append(json.loads(stripped))
    return rows


def _normalize_v2_row(*, raw: dict[str, Any], annotator: str, source_file: str) -> PoolRow | None:
    verdict = raw.get("judge_verdict")
    if verdict is None:
        return None
    pilot_idx = raw.get("_pilot_row_index")
    if not isinstance(pilot_idx, int):
        return None
    pool_row_id = f"{annotator}-{pilot_idx:04d}"
    hierarchy_raw = raw.get("hierarchy")
    gold_actions_raw = raw.get("gold_actions")
    hierarchy: dict[str, Any] = hierarchy_raw if isinstance(hierarchy_raw, dict) else {}
    gold_actions: dict[str, Any] = gold_actions_raw if isinstance(gold_actions_raw, dict) else {}
    return PoolRow(
        pool_row_id=pool_row_id,
        annotator=annotator,
        task_id=str(raw.get("task_id", "")),
        benchmark=str(raw.get("benchmark", "")),
        domain=str(raw.get("domain", "")),
        problem=str(raw.get("problem", "")),
        hierarchy=hierarchy,
        gold_actions=gold_actions,
        baseline_verdict=str(verdict).strip().lower(),
        source_file=source_file,
    )


def _normalize_v1_row(*, raw: dict[str, Any], ordinal: int, source_file: str) -> PoolRow | None:
    verdict = raw.get("judge_verdict")
    if verdict is None:
        return None
    pool_row_id = f"{ANNOTATOR_V1_SONNET}-{ordinal:04d}"
    hierarchy_raw = raw.get("hierarchy")
    gold_actions_raw = raw.get("gold_actions")
    hierarchy: dict[str, Any] = hierarchy_raw if isinstance(hierarchy_raw, dict) else {}
    gold_actions: dict[str, Any] = gold_actions_raw if isinstance(gold_actions_raw, dict) else {}
    return PoolRow(
        pool_row_id=pool_row_id,
        annotator=ANNOTATOR_V1_SONNET,
        task_id=str(raw.get("task_id", "")),
        benchmark=str(raw.get("benchmark", "")),
        domain=str(raw.get("domain", "")),
        problem=str(raw.get("problem", "")),
        hierarchy=hierarchy,
        gold_actions=gold_actions,
        baseline_verdict=str(verdict).strip().lower(),
        source_file=source_file,
    )


def load_pool() -> list[PoolRow]:
    """Load the full 55-row pool: 20 v2-sonnet + 23 v2-haiku + 12 v1-sonnet."""
    sonnet_rows = _read_jsonl(path=V2_SONNET_INPUT_PATH)
    haiku_rows = _read_jsonl(path=V2_HAIKU_CORRECTED_INPUT_PATH)
    v1_rows = _read_jsonl(path=V1_SONNET_INPUT_PATH)

    pool: list[PoolRow] = []
    for raw in sonnet_rows:
        norm = _normalize_v2_row(
            raw=raw,
            annotator=ANNOTATOR_V2_SONNET,
            source_file=str(V2_SONNET_INPUT_PATH),
        )
        if norm is not None:
            pool.append(norm)
    for raw in haiku_rows:
        norm = _normalize_v2_row(
            raw=raw,
            annotator=ANNOTATOR_V2_HAIKU,
            source_file=str(V2_HAIKU_CORRECTED_INPUT_PATH),
        )
        if norm is not None:
            pool.append(norm)
    ordinal = 0
    for raw in v1_rows:
        norm = _normalize_v1_row(
            raw=raw,
            ordinal=ordinal,
            source_file=str(V1_SONNET_INPUT_PATH),
        )
        if norm is not None:
            pool.append(norm)
            ordinal += 1
    return pool


def main() -> None:
    pool = load_pool()
    by_annot: dict[str, int] = {}
    for row in pool:
        by_annot[row.annotator] = by_annot.get(row.annotator, 0) + 1
    print(f"Loaded {len(pool)} pool rows.")
    for k, v in sorted(by_annot.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
