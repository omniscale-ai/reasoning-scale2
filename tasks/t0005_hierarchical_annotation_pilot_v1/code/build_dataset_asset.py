"""Step 5: build the hierarchical-annotation-v1 dataset asset.

Reads `code/_outputs/mapped_with_judge.jsonl`, copies it to the asset's
`files/` directory, and writes `details.json` and `description.md` per the
v2 dataset asset specification.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from tasks.t0005_hierarchical_annotation_pilot_v1.code.constants import (
    DATASET_ACCESS_KIND,
    DATASET_CATEGORIES,
    DATASET_ID,
    DATASET_LICENSE,
    DATASET_NAME,
    DATASET_VERSION,
    DATE_TODAY_ISO,
    TASK_ID,
)
from tasks.t0005_hierarchical_annotation_pilot_v1.code.paths import (
    DATASET_ASSET_DIR,
    DATASET_DESCRIPTION_PATH,
    DATASET_DETAILS_PATH,
    DATASET_FILE_PATH,
    DATASET_FILES_DIR,
    MAPPED_WITH_JUDGE_OUTPUT,
)


def _load_jsonl(*, path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def _compute_summary_stats(*, rows: list[dict[str, Any]]) -> dict[str, Any]:
    bench_counts: dict[str, int] = {}
    bench_complete: dict[str, int] = {}
    bench_judged: dict[str, int] = {}
    bench_accept: dict[str, int] = {}
    domain_counts: dict[str, int] = {}
    atomic_lengths: list[int] = []

    for row in rows:
        bench = row["benchmark"]
        bench_counts[bench] = bench_counts.get(bench, 0) + 1
        if row.get("hierarchy_completeness"):
            bench_complete[bench] = bench_complete.get(bench, 0) + 1
        domain = row.get("domain", "")
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
        atomic_lengths.append(len(row["hierarchy"]["atomic"]))

        verdict = row.get("judge_verdict")
        if verdict is not None:
            bench_judged[bench] = bench_judged.get(bench, 0) + 1
            if verdict == "acceptable":
                bench_accept[bench] = bench_accept.get(bench, 0) + 1

    return {
        "row_count": len(rows),
        "bench_counts": bench_counts,
        "bench_complete": bench_complete,
        "bench_judged": bench_judged,
        "bench_accept": bench_accept,
        "domain_counts": domain_counts,
        "avg_atomic_length": (sum(atomic_lengths) / len(atomic_lengths) if atomic_lengths else 0.0),
    }


def _build_details_json(*, stats: dict[str, Any]) -> dict[str, Any]:
    bench_counts = stats["bench_counts"]
    bench_summary = ", ".join(f"{name}={count}" for name, count in sorted(bench_counts.items()))
    return {
        "spec_version": "2",
        "dataset_id": DATASET_ID,
        "name": DATASET_NAME,
        "version": DATASET_VERSION,
        "short_description": (
            "Three-level (global / subtask / atomic) hierarchical annotation of 115 benchmark "
            "tasks drawn from FrontierScience-Olympiad, SWE-bench Verified, tau-bench, and "
            "WorkArena++. Includes a 12-row LLM-as-judge spot-check."
        ),
        "description_path": "description.md",
        "source_paper_id": None,
        "url": None,
        "download_url": None,
        "year": 2026,
        "date_published": DATE_TODAY_ISO,
        "authors": [
            {
                "name": "Glite ARF reasoning-scale project",
                "country": None,
                "institution": None,
                "orcid": None,
            }
        ],
        "institutions": [],
        "license": DATASET_LICENSE,
        "access_kind": DATASET_ACCESS_KIND,
        "size_description": (
            f"{stats['row_count']} rows total ({bench_summary}); each row carries a "
            "global / subtask / atomic hierarchy and gold-action triple. Twelve rows "
            "(three per benchmark) carry an LLM-as-judge verdict."
        ),
        "files": [
            {
                "path": "files/hierarchical_annotation_v1.jsonl",
                "description": (
                    "115-row JSONL with the canonical hierarchical annotation schema "
                    "and judge verdicts merged in for the 12 sampled rows."
                ),
                "format": "jsonl",
            }
        ],
        "categories": list(DATASET_CATEGORIES),
    }


def _build_description_md(*, stats: dict[str, Any]) -> str:
    bench_counts = stats["bench_counts"]
    bench_complete = stats["bench_complete"]
    bench_accept = stats["bench_accept"]
    bench_judged = stats["bench_judged"]

    def _completeness_pct(name: str) -> str:
        total = bench_counts.get(name, 0)
        if total == 0:
            return "n/a"
        return f"{100.0 * bench_complete.get(name, 0) / total:.1f}%"

    def _accept_pct(name: str) -> str:
        judged = bench_judged.get(name, 0)
        if judged == 0:
            return "n/a"
        accepted = bench_accept.get(name, 0)
        pct = 100.0 * accepted / judged
        return f"{pct:.1f}% ({accepted}/{judged})"

    def _row(name: str) -> str:
        total = bench_counts.get(name, 0)
        return f"| {name} | {total} | {_completeness_pct(name)} | {_accept_pct(name)} |"

    rows_per_bench_table = "\n".join(_row(name) for name in sorted(bench_counts.keys()))

    return f"""---
spec_version: "2"
dataset_id: "{DATASET_ID}"
summarized_by_task: "{TASK_ID}"
date_summarized: "{DATE_TODAY_ISO}"
---

# {DATASET_NAME}

## Metadata

* **Name**: {DATASET_NAME}
* **Year**: 2026
* **Authors**: Glite ARF reasoning-scale project
* **License**: {DATASET_LICENSE}
* **Access**: {DATASET_ACCESS_KIND}
* **Size**: {stats["row_count"]} rows; one row per benchmark task

## Overview

This dataset is the v1 hierarchical-annotation pilot of the Glite ARF reasoning-scale project. It
takes the 115 LLM-annotated rows produced by `project/code/scripts/collect_and_annotate.py` and
projects each row's `steps.nodes` graph onto the project's three-level global / subtask / atomic
schema using a deterministic mapper. A 12-row LLM-as-judge spot-check (3 rows per benchmark) using
`claude-haiku-4-5-20251001` provides an external quality estimate.

The dataset feeds Phase 2 and Phase 3 scope-conditioning experiments. It is the canonical
gold-action source until a larger v2 (>=200 rows with full human review) is produced.

## Content & Annotation

Each row follows the canonical schema:

```json
{{
  "task_id": "<benchmark prefix + uuid>",
  "benchmark": "FrontierScience-Olympiad" | "SWE-bench Verified" | "tau-bench" | "WorkArena++",
  "domain": "<benchmark-specific category, e.g. physics or sales>",
  "difficulty": {{...}},
  "problem": "<full problem statement>",
  "hierarchy": {{
    "global": "<short label of the high-level plan move> | null",
    "subtask": ["<conceptual subtask labels in id order>", ...],
    "atomic":  ["<computational + verification action labels in id order>", ...]
  }},
  "gold_actions": {{ ... mirrors hierarchy but uses the longer 'detail' field ... }},
  "annotation_model": "claude-sonnet-4-6",
  "judge_verdict": "acceptable" | "needs revision" | null,
  "judge_notes": "<one-sentence justification or null>",
  "hierarchy_completeness": true | false
}}
```

Mapper rules:

* **`global`**: text from the lowest-id `strategic` node, falling back to the first node by id when
  none exists, and `null` when the input row's `steps` is `null` (LLM annotation failure).
* **`subtask`**: list of `conceptual` node labels in id order; falls back to `strategic` nodes
  beyond the first when no conceptual nodes are present.
* **`atomic`**: `computational` and `verification` nodes in id order.

`hierarchy_completeness` is `true` iff `global is not None` and `len(atomic) > 0`.

## Statistics

| Benchmark | Row count | Hierarchy completeness | Judge accept rate |
| --- | --- | --- | --- |
{rows_per_bench_table}

* **Mean atomic actions per task**: {stats["avg_atomic_length"]:.2f}
* **Total rows**: {stats["row_count"]}

## Usage Notes

Load with `jsonlines` or pandas (`pd.read_json(..., lines=True)`). Filter by
`hierarchy_completeness == true` if downstream consumers need only fully-decomposed rows. The judge
verdict is populated only on the stratified sample (12 rows total); for all other rows
`judge_verdict` is `null` — this is by design.

Known quirks:

* FrontierScience-Olympiad has 11 rows with `steps == null` due to upstream LLM annotation
  failures. These rows are preserved with `hierarchy_completeness == false` and a `null` global
  label so downstream tasks can re-annotate without re-running the original pipeline.
* The pilot file's "agentic proxies" are tau-bench and WorkArena++ (not HumanEval-proxy and
  Mind2Web-proxy as one earlier draft of the task description named them).

## Main Ideas

* The deterministic mapper exploits the existing `type` field (`strategic`, `conceptual`,
  `computational`, `verification`) so no extra LLM cost is needed for the mapping itself; the
  external judge check is what guards quality.
* A small (12-row) stratified judge sample is sufficient to surface schema bugs because
  hierarchy errors tend to be systematic across rows of the same benchmark.
* Empty `subtask` lists are valid v1 output: when the upstream annotator produced a flat list of
  computational nodes without conceptual abstractions, the mapper preserves that flatness rather
  than inventing subtask boundaries.

## Summary

The hierarchical-annotation-v1 dataset converts 115 LLM-annotated benchmark tasks into a uniform
global / subtask / atomic schema using a deterministic Python mapper, and supplements that with a
12-row LLM-as-judge audit. It is the input to all Phase 2 / Phase 3 scope-conditioning experiments
in the project.

For the project, this asset is the first concrete instantiation of the project's hierarchical
schema. Its main limitations — the small sample size, the reliance on a single annotator
(`claude-sonnet-4-6`), and the absence of human-rater agreement — are deferred to a v2 task that
will scale to >=200 rows and add human review.
"""


def main() -> None:
    if not MAPPED_WITH_JUDGE_OUTPUT.exists():
        raise SystemExit(
            f"Expected {MAPPED_WITH_JUDGE_OUTPUT} to exist before building the asset; "
            "run the judge_runner first.",
        )

    rows = _load_jsonl(path=MAPPED_WITH_JUDGE_OUTPUT)
    stats = _compute_summary_stats(rows=rows)

    DATASET_FILES_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(MAPPED_WITH_JUDGE_OUTPUT, DATASET_FILE_PATH)

    details = _build_details_json(stats=stats)
    DATASET_DETAILS_PATH.write_text(
        json.dumps(details, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    DATASET_DESCRIPTION_PATH.write_text(
        _build_description_md(stats=stats),
        encoding="utf-8",
    )

    print(f"Wrote {DATASET_FILE_PATH} ({stats['row_count']} rows)")
    print(f"Wrote {DATASET_DETAILS_PATH}")
    print(f"Wrote {DATASET_DESCRIPTION_PATH}")
    print(f"Asset folder: {DATASET_ASSET_DIR}")


if __name__ == "__main__":
    main()
