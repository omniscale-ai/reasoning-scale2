"""Centralized path constants for the v2-sonnet hierarchical annotation pipeline (t0014)."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path("tasks/t0014_v2_annotator_sonnet_rerun")

V1_INPUT_PATH: Path = Path(
    "tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/"
    "hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl"
)

# Reference inputs from t0009 (read-only).
V2_HAIKU_INPUT_PATH: Path = Path(
    "tasks/t0009_hierarchical_annotation_v2/assets/dataset/"
    "hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl"
)
V2_HAIKU_JUDGE_OUTCOMES_PATH: Path = Path(
    "tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_outcomes.jsonl"
)
V2_HAIKU_JUDGE_SAMPLE_PATH: Path = Path(
    "tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_sample.jsonl"
)
V1_JUDGE_OUTCOMES_PATH: Path = Path(
    "tasks/t0005_hierarchical_annotation_pilot_v1/code/_outputs/judge_outcomes.jsonl"
)

OUTPUTS_DIR: Path = TASK_ROOT / "code" / "_outputs"

V2_SONNET_RAW_OUTPUT: Path = OUTPUTS_DIR / "v2_sonnet_annotated.jsonl"
V2_SONNET_ANNOTATOR_COSTS_PATH: Path = OUTPUTS_DIR / "v2_sonnet_annotator_costs.json"

V2_SONNET_JUDGE_SAMPLE_OUTPUT: Path = OUTPUTS_DIR / "v2_sonnet_judge_sample.jsonl"
V2_SONNET_JUDGE_OUTCOMES_PATH: Path = OUTPUTS_DIR / "v2_sonnet_judge_outcomes.jsonl"
V2_SONNET_JUDGE_COSTS_PATH: Path = OUTPUTS_DIR / "v2_sonnet_judge_costs.json"

# Three-way comparison outputs.
THREE_WAY_COMPARISON_JSON: Path = OUTPUTS_DIR / "three_way_comparison.json"
THREE_WAY_TABLE_MD: Path = OUTPUTS_DIR / "three_way_table.md"

DATASET_ASSET_DIR: Path = TASK_ROOT / "assets" / "dataset" / "hierarchical-annotation-v2-sonnet"
DATASET_FILES_DIR: Path = DATASET_ASSET_DIR / "files"
V2_SONNET_FINAL_JSONL: Path = DATASET_FILES_DIR / "hierarchical_annotation_v2_sonnet.jsonl"
DATASET_DETAILS_JSON: Path = DATASET_ASSET_DIR / "details.json"
DATASET_DESCRIPTION_MD: Path = DATASET_ASSET_DIR / "description.md"

# Charts directory under results/.
RESULTS_IMAGES_DIR: Path = TASK_ROOT / "results" / "images"
