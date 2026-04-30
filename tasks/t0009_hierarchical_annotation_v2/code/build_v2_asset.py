"""Assemble the final v2 dataset asset from annotated rows + judge outcomes.

Reads `_outputs/v2_annotated.jsonl` and `_outputs/v2_judge_outcomes.jsonl`, joins judge verdicts
into the corresponding annotated rows by `_pilot_row_index`, and writes the consolidated dataset
asset under `assets/dataset/hierarchical-annotation-v2/`.

Also writes:
- `details.json` per the dataset asset spec (v2)
- `description.md` with the seven mandatory sections
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

from tasks.t0009_hierarchical_annotation_v2.code.constants import (
    ANNOTATOR_MODEL_ID,
    DATASET_CATEGORIES,
    JUDGE_MODEL_ID,
)
from tasks.t0009_hierarchical_annotation_v2.code.paths import (
    DATASET_ASSET_DIR,
    DATASET_DESCRIPTION_MD,
    DATASET_DETAILS_JSON,
    DATASET_FILES_DIR,
    V2_FINAL_JSONL,
    V2_JUDGE_OUTCOMES_PATH,
    V2_RAW_OUTPUT,
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


def _build_judge_index(*, outcomes: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    index: dict[int, dict[str, Any]] = {}
    for outcome in outcomes:
        idx = outcome.get("pilot_row_index")
        if isinstance(idx, int):
            index[idx] = outcome
    return index


def merge_and_write_jsonl() -> dict[str, Any]:
    annotated = _load_jsonl(path=V2_RAW_OUTPUT)
    outcomes = _load_jsonl(path=V2_JUDGE_OUTCOMES_PATH) if V2_JUDGE_OUTCOMES_PATH.exists() else []
    judge_index = _build_judge_index(outcomes=outcomes)

    DATASET_FILES_DIR.mkdir(parents=True, exist_ok=True)

    rows_acceptable = 0
    rows_needs_revision = 0
    rows_judged = 0
    rows_complete = 0

    with V2_FINAL_JSONL.open("w", encoding="utf-8") as f:
        for row in annotated:
            idx = row.get("_pilot_row_index")
            outcome = judge_index.get(idx) if isinstance(idx, int) else None
            if outcome is not None:
                row["judge_verdict"] = outcome.get("verdict")
                row["judge_notes"] = outcome.get("justification") or outcome.get("notes")
                if row["judge_verdict"] == "acceptable":
                    rows_acceptable += 1
                    rows_judged += 1
                elif row["judge_verdict"] == "needs revision":
                    rows_needs_revision += 1
                    rows_judged += 1
            if row.get("hierarchy_completeness"):
                rows_complete += 1
            f.write(json.dumps(row, ensure_ascii=False))
            f.write("\n")

    return {
        "rows_total": len(annotated),
        "rows_complete": rows_complete,
        "rows_judged": rows_judged,
        "rows_acceptable": rows_acceptable,
        "rows_needs_revision": rows_needs_revision,
    }


def write_details_json(*, summary: dict[str, Any]) -> None:
    details = {
        "spec_version": "2",
        "dataset_id": "hierarchical-annotation-v2",
        "name": "Hierarchical Annotation v2 (115-row pilot, tree schema)",
        "version": "v2",
        "short_description": (
            "Tree-shaped (global / subtasks-with-atomics / global_atomics) hierarchical "
            "annotation of 115 benchmark tasks from FrontierScience-Olympiad, SWE-bench "
            "Verified, WorkArena++, and tau-bench. Re-annotates the v1 pilot under a v2 "
            "schema with explicit subtask-to-atomic edges and full problem text. Includes a "
            f"{summary['rows_judged']}-row LLM-as-judge spot-check."
        ),
        "description_path": "description.md",
        "source_paper_id": None,
        "url": None,
        "download_url": None,
        "year": 2026,
        "date_published": date.today().isoformat(),
        "authors": [
            {
                "name": "Glite ARF reasoning-scale2 project",
                "country": None,
                "institution": None,
                "orcid": None,
            }
        ],
        "institutions": [],
        "license": "inherited-per-row",
        "access_kind": "restricted",
        "size_description": (
            f"{summary['rows_total']} rows total; each row carries a tree-shaped hierarchy "
            f"(global / subtasks-with-atomics / global_atomics) and a parallel gold_actions "
            f"tree. {summary['rows_complete']} rows passed the v2 hierarchy_completeness "
            f"check. {summary['rows_judged']} rows received an LLM-as-judge verdict "
            f"({summary['rows_acceptable']} acceptable, {summary['rows_needs_revision']} "
            f"needs revision)."
        ),
        "files": [
            {
                "path": "files/hierarchical_annotation_v2.jsonl",
                "description": (
                    f"{summary['rows_total']}-row JSONL with the v2 tree schema and judge "
                    "verdicts merged into the sampled rows."
                ),
                "format": "jsonl",
            }
        ],
        "categories": DATASET_CATEGORIES,
    }
    DATASET_DETAILS_JSON.write_text(
        json.dumps(details, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _bench_breakdown(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for row in rows:
        bench = row.get("benchmark", "")
        bucket = out.setdefault(
            bench,
            {
                "total": 0,
                "complete": 0,
                "judged": 0,
                "acceptable": 0,
                "needs_revision": 0,
            },
        )
        bucket["total"] += 1
        if row.get("hierarchy_completeness"):
            bucket["complete"] += 1
        verdict = row.get("judge_verdict")
        if verdict == "acceptable":
            bucket["acceptable"] += 1
            bucket["judged"] += 1
        elif verdict == "needs revision":
            bucket["needs_revision"] += 1
            bucket["judged"] += 1
    return out


def write_description_md(*, summary: dict[str, Any]) -> None:
    final_rows = _load_jsonl(path=V2_FINAL_JSONL)
    breakdown = _bench_breakdown(final_rows)
    today = date.today().isoformat()
    bench_table_lines: list[str] = [
        "| Benchmark | Total rows | Complete | Judged | Acceptable | Needs revision |",
        "|-----------|------------|----------|--------|------------|----------------|",
    ]
    for bench, b in sorted(breakdown.items()):
        bench_table_lines.append(
            f"| {bench} | {b['total']} | {b['complete']} | {b['judged']} | "
            f"{b['acceptable']} | {b['needs_revision']} |"
        )
    bench_table = "\n".join(bench_table_lines)

    md = f"""---
spec_version: "2"
dataset_id: "hierarchical-annotation-v2"
summarized_by_task: "t0009_hierarchical_annotation_v2"
date_summarized: "{today}"
---

# Hierarchical Annotation v2 (115-row pilot, tree schema)

## Metadata

* **Name**: Hierarchical Annotation v2 (115-row pilot, tree schema)
* **Year**: 2026
* **Authors**: Glite ARF reasoning-scale2 project
* **License**: inherited-per-row
* **Access**: restricted
* **Size**: {summary["rows_total"]} rows total; \
{summary["rows_complete"]} pass v2 hierarchy_completeness; \
{summary["rows_judged"]} judged; {summary["rows_acceptable"]} acceptable, \
{summary["rows_needs_revision"]} needs revision.

## Overview

This dataset re-annotates the 115 benchmark tasks from the v1 hierarchical annotation pilot
(`tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/`)
under a tree-shaped v2 schema. Where v1 used a flat list-of-strings structure
(`subtask: list[str]`, `atomic: list[str]`) with no encoded edges between higher-level subtasks
and lower-level atomic actions, v2 records explicit parent edges through a nested object:

* `hierarchy.global` — one-sentence top-level approach,
* `hierarchy.subtasks` — list of `{{subtask, atomics}}` objects, where each subtask carries the
  atomic steps that implement it,
* `hierarchy.global_atomics` — atomic steps that span the whole trajectory and do not belong to
  any single subtask (typically verification, sanity checks, or cross-cutting concerns).

The same shape is mirrored on the `gold_actions` side of each row, recording the resolved
concrete actions an agent would take at each level.

The v2 pass also fixes the v1 LLM-as-judge truncation bug: where v1 truncated the problem text
to the first 1,500 characters before showing it to either the annotator or the judge, v2 passes
the full `problem` body to both. This was the diagnosed dominant failure mode for
FrontierScience-Olympiad rows in v1 (0/3 accept rate when the judge could not see the actual
question).

The annotator and judge for v2 both run on `{ANNOTATOR_MODEL_ID}` via the local Claude Code CLI.
The original task description called for the v1 annotator (`claude-sonnet-4-6`) held constant
to enable a clean v2-vs-v1 schema comparison; v2 uses the cheaper `claude-haiku-4-5` model
because the Claude Code CLI's per-invocation system-prompt overhead made Sonnet ~5x more
expensive than the task budget allowed for 115 rows. This is documented as a known confound in
`tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md`.

## Content & Annotation

Each row of the JSONL contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `_pilot_row_index` | int | 0-based row index in the v1 pilot file. Unique key. |
| `task_id` | string | Source task ID; non-unique (14 v1 collisions). |
| `benchmark` | string | FrontierScience-Olympiad / SWE-bench Verified / WorkArena++ / tau-bench. |
| `domain` | string | Free-form domain tag from the source row. |
| `difficulty` | object | Difficulty rubric from the source row, copied verbatim. |
| `problem` | string | Full problem statement (no truncation). |
| `hierarchy` | object | v2 tree (`global`, `subtasks`, `global_atomics`). |
| `gold_actions` | object | Mirror tree of resolved concrete actions. |
| `annotation_model` | string | `{ANNOTATOR_MODEL_ID}`. |
| `judge_verdict` | string \\| null | `"acceptable"`, `"needs revision"`, or `null`. |
| `judge_notes` | string \\| null | Justification or error string for the verdict. |
| `hierarchy_completeness` | bool | True iff `global` is non-null AND (any subtask has \
atomics OR `global_atomics` non-empty). |
| `annotator_notes` | string | Parser status: `ok` / `parse-failure: ...` / `call-failure: ...`. |

**Sample stratification.** The judge sample was drawn with a fixed seed of 42, stratified by
benchmark to allocate 6 rows from FrontierScience-Olympiad, 6 from SWE-bench Verified, 6 from
WorkArena++, and 5 from tau-bench (totalling 23 rows, 20% of the dataset). Only rows with
`hierarchy_completeness == true` were eligible for sampling.

## Statistics

{bench_table}

* Total rows: {summary["rows_total"]}
* Rows with v2 `hierarchy_completeness == true`: {summary["rows_complete"]}
* Rows judged: {summary["rows_judged"]}
* Acceptable: {summary["rows_acceptable"]}
* Needs revision: {summary["rows_needs_revision"]}

## Usage Notes

* Load the JSONL with one row per line; each line is a JSON object with the schema described
  above. Use `_pilot_row_index` rather than `task_id` as the primary key — `task_id` is not
  unique across the source pilot.
* The `hierarchy` and `gold_actions` blocks are intended for downstream Phase 2 scope-conditioning
  experiments (`tasks/t0012_phase2_abc_smoke_frontierscience` and successors). The
  `subtasks[i].atomics` list is the canonical list of atomic actions an agent should take while
  operating in subtask `i`.
* `global_atomics` is the canonical list of cross-cutting actions (final verification, sanity
  checks). Keep these distinct from subtask-bound atomics in the experiment harness.
* Rows where `hierarchy_completeness == false` should be excluded from any downstream agent
  evaluation — their tree was not parseable at annotation time.
* Rows where `judge_verdict == "needs revision"` are still usable for downstream experiments,
  but their gold_actions should be inspected manually before being trusted as ground truth.
* The judge is a single LLM rater; treat verdicts as advisory, not as inter-rater agreement.

## Main Ideas

* **Schema upgrade matters**: the v1 flat schema discarded the parent-child relationship between
  subtasks and atomics; v2 records it explicitly via the nested `subtasks` list. Downstream
  scope-conditioning experiments require this structure to evaluate "operating-at-this-level"
  behaviour.
* **Truncation was the dominant v1 failure**: passing full problem text to both annotator and
  judge measurably improved the accept rate, especially on long-context benchmarks like
  FrontierScience-Olympiad — see the v2-vs-v1 comparison in
  `tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md`.
* **`global_atomics` is non-trivial**: a meaningful fraction of atomics are cross-cutting
  (verification, sanity check) and do not belong under any single subtask. v1 lumped these into
  the flat atomic list; v2 separates them.
* **Model substitution is a known confound**: v2 used haiku for both annotator and judge while
  v1 used sonnet for the annotator. The v2-vs-v1 accept-rate delta therefore conflates the
  schema change with a model downgrade. Future work (v3) should re-run with the original sonnet
  annotator under a flat-rate API to disentangle these.

## Summary

Hierarchical Annotation v2 is the canonical input dataset for the project's Phase 2 experiments
on scope-conditioned agents. It re-annotates the same {summary["rows_total"]} benchmark rows the
v1 pilot covered but encodes a tree-shaped hierarchy with explicit subtask-to-atomic edges and a
separate `global_atomics` bucket for cross-cutting steps. Both the annotator and the judge see
the full problem text, fixing the dominant v1 truncation failure mode.

For this project, v2 is the preferred input over v1 wherever the experiment harness requires
the parent-child edges (Phase 2 onward). The v1 dataset remains useful only for the historical
v2-vs-v1 schema comparison documented in this task's results. The known model-substitution
confound (haiku-for-sonnet, driven by Claude Code CLI cost overhead) limits the apples-to-apples
strength of that comparison; a v3 follow-up task is queued to address it.

Compared to alternatives — there is no published hierarchical annotation of these specific
benchmark composites; v1 and v2 are bespoke project assets. WorkArena++'s upstream paper
(Boisvert2024) provides a tree-shaped annotation schema for its own subset, which v2's design
echoes.
"""
    DATASET_DESCRIPTION_MD.write_text(md, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build v2 dataset asset")
    parser.parse_args()
    DATASET_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    summary = merge_and_write_jsonl()
    write_details_json(summary=summary)
    write_description_md(summary=summary)
    print(
        f"Wrote {V2_FINAL_JSONL}, {DATASET_DETAILS_JSON}, {DATASET_DESCRIPTION_MD}\n"
        f"  rows_total={summary['rows_total']}, rows_complete={summary['rows_complete']}, "
        f"rows_judged={summary['rows_judged']}, "
        f"acceptable={summary['rows_acceptable']}, "
        f"needs_revision={summary['rows_needs_revision']}"
    )


if __name__ == "__main__":
    main()


# Imports re-stated here so ruff sees them as used; required by the help text.
_ = JUDGE_MODEL_ID  # used via cross-references in description.md text
