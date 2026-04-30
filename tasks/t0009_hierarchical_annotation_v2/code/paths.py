"""Centralized path constants for the v2 hierarchical annotation pipeline."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path("tasks/t0009_hierarchical_annotation_v2")

V1_INPUT_PATH: Path = Path(
    "tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/"
    "hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl"
)

OUTPUTS_DIR: Path = TASK_ROOT / "code" / "_outputs"

V2_RAW_OUTPUT: Path = OUTPUTS_DIR / "v2_annotated.jsonl"
V2_ANNOTATOR_COSTS_PATH: Path = OUTPUTS_DIR / "v2_annotator_costs.json"

V2_JUDGE_SAMPLE_OUTPUT: Path = OUTPUTS_DIR / "v2_judge_sample.jsonl"
V2_JUDGE_OUTCOMES_PATH: Path = OUTPUTS_DIR / "v2_judge_outcomes.jsonl"
V2_JUDGE_COSTS_PATH: Path = OUTPUTS_DIR / "v2_judge_costs.json"

V1_VS_V2_COMPARISON_JSON: Path = OUTPUTS_DIR / "v1_vs_v2_comparison.json"
V1_VS_V2_TABLE_MD: Path = OUTPUTS_DIR / "v1_vs_v2_table.md"

DATASET_ASSET_DIR: Path = TASK_ROOT / "assets" / "dataset" / "hierarchical-annotation-v2"
DATASET_FILES_DIR: Path = DATASET_ASSET_DIR / "files"
V2_FINAL_JSONL: Path = DATASET_FILES_DIR / "hierarchical_annotation_v2.jsonl"
DATASET_DETAILS_JSON: Path = DATASET_ASSET_DIR / "details.json"
DATASET_DESCRIPTION_MD: Path = DATASET_ASSET_DIR / "description.md"
