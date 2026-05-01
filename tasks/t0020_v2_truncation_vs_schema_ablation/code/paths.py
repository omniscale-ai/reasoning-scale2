"""Centralized path constants for the v2 truncation vs schema ablation pipeline (t0020)."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path("tasks/t0020_v2_truncation_vs_schema_ablation")

# v1 source: full 115-row jsonl with one judge_verdict per row for the 12 v1-judged rows.
V1_INPUT_PATH: Path = Path(
    "tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/"
    "hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl"
)

# Reference: v2-haiku 23-row judge sample plus its outcomes (read-only).
V2_HAIKU_JUDGE_OUTCOMES_PATH: Path = Path(
    "tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_outcomes.jsonl"
)
V2_HAIKU_JUDGE_SAMPLE_PATH: Path = Path(
    "tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_sample.jsonl"
)

# Reference: t0014 sonnet 20-row matched pool (defines the rows we re-annotate here).
T0014_SONNET_JUDGE_SAMPLE_PATH: Path = Path(
    "tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_sample.jsonl"
)

OUTPUTS_DIR: Path = TASK_ROOT / "code" / "_outputs"

# Truncated annotator outputs.
V2_TRUNCATED_RAW_OUTPUT: Path = OUTPUTS_DIR / "v2_truncated_annotated.jsonl"
V2_TRUNCATED_ANNOTATOR_COSTS_PATH: Path = OUTPUTS_DIR / "v2_truncated_annotator_costs.json"

# Truncated judge outputs.
V2_TRUNCATED_JUDGE_SAMPLE_OUTPUT: Path = OUTPUTS_DIR / "v2_truncated_judge_sample.jsonl"
V2_TRUNCATED_JUDGE_OUTCOMES_PATH: Path = OUTPUTS_DIR / "v2_truncated_judge_outcomes.jsonl"
V2_TRUNCATED_JUDGE_COSTS_PATH: Path = OUTPUTS_DIR / "v2_truncated_judge_costs.json"

# Three-way comparison outputs.
THREE_WAY_COMPARISON_JSON: Path = OUTPUTS_DIR / "three_way_comparison.json"
THREE_WAY_TABLE_MD: Path = OUTPUTS_DIR / "three_way_table.md"

# Predictions asset directory (per task description).
PREDICTIONS_ASSET_DIR: Path = TASK_ROOT / "assets" / "predictions" / "v2-truncated-ablation"
PREDICTIONS_FILES_DIR: Path = PREDICTIONS_ASSET_DIR / "files"
PREDICTIONS_JSONL: Path = PREDICTIONS_FILES_DIR / "v2-truncated-predictions.jsonl"
PREDICTIONS_DETAILS_JSON: Path = PREDICTIONS_ASSET_DIR / "details.json"
PREDICTIONS_DESCRIPTION_MD: Path = PREDICTIONS_ASSET_DIR / "description.md"

# Answer asset directory.
ANSWER_ASSET_DIR: Path = TASK_ROOT / "assets" / "answer" / "decomposition-v2-schema-vs-truncation"
ANSWER_DETAILS_JSON: Path = ANSWER_ASSET_DIR / "details.json"
ANSWER_DESCRIPTION_MD: Path = ANSWER_ASSET_DIR / "description.md"
ANSWER_SHORT_MD: Path = ANSWER_ASSET_DIR / "short_answer.md"
ANSWER_FULL_MD: Path = ANSWER_ASSET_DIR / "full_answer.md"

# Charts directory.
RESULTS_IMAGES_DIR: Path = TASK_ROOT / "results" / "images"

# Final results files.
RESULTS_DIR: Path = TASK_ROOT / "results"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
SUGGESTIONS_JSON: Path = RESULTS_DIR / "suggestions.json"
RESULTS_SUMMARY_MD: Path = RESULTS_DIR / "results_summary.md"
RESULTS_DETAILED_MD: Path = RESULTS_DIR / "results_detailed.md"
REMOTE_MACHINES_USED_JSON: Path = RESULTS_DIR / "remote_machines_used.json"
