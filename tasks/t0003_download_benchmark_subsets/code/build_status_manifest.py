"""Read each dataset asset's details.json and write code/access_status.json.

The orchestrator's results step consumes this manifest to populate the per-benchmark
status table in `results/results_summary.md` and to flag permanent-proxy decisions in
`results/suggestions.json`.
"""

from __future__ import annotations

import json
from pathlib import Path

from tasks.t0003_download_benchmark_subsets.code.constants import (
    FRONTIERSCIENCE_SLUG,
    SWEBENCH_SLUG,
    TAUBENCH_SLUG,
    WORKARENA_PP_SLUG,
)
from tasks.t0003_download_benchmark_subsets.code.paths import (
    ACCESS_STATUS_PATH,
    DATASET_DIR,
)


def _load_details(*, dataset_id: str) -> dict[str, object]:
    path: Path = DATASET_DIR / dataset_id / "details.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _row(*, dataset_id: str, subset_rule: str) -> dict[str, object]:
    details: dict[str, object] = _load_details(dataset_id=dataset_id)
    return {
        "dataset_id": dataset_id,
        "name": details.get("name"),
        "download_status": details.get("download_status"),
        "download_failure_reason": details.get("download_failure_reason"),
        "size_description": details.get("size_description"),
        "url": details.get("url"),
        "license": details.get("license"),
        "access_kind": details.get("access_kind"),
        "categories": details.get("categories"),
        "subset_rule": subset_rule,
    }


def build_status_manifest() -> dict[str, object]:
    rows: list[dict[str, object]] = [
        _row(
            dataset_id=FRONTIERSCIENCE_SLUG,
            subset_rule=(
                "all FrontierScience-Olympiad rows from pilot JSONL; "
                "domain-stratified across physics, chemistry, biology"
            ),
        ),
        _row(
            dataset_id=WORKARENA_PP_SLUG,
            subset_rule=(
                "compositional task class manifest extracted from upstream "
                "curriculum.py; instance-level filter deferred"
            ),
        ),
        _row(
            dataset_id=SWEBENCH_SLUG,
            subset_rule=("keep iff gold patch has between 4 and 8 `@@ -` hunks (inclusive)"),
        ),
        _row(
            dataset_id=TAUBENCH_SLUG,
            subset_rule=("keep iff gold action sequence has between 4 and 8 actions (inclusive)"),
        ),
    ]
    payload: dict[str, object] = {
        "task_id": "t0003_download_benchmark_subsets",
        "generated_at": "2026-04-29",
        "rows": rows,
    }
    ACCESS_STATUS_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload: dict[str, object] = build_status_manifest()
    print(json.dumps(payload, indent=2))
