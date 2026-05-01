"""Centralized file paths for t0019 v2 judge calibration with sonnet."""

from __future__ import annotations

from pathlib import Path

# Repo root (the worktree). Calculated relative to this file: tasks/t0019.../code/paths.py.
REPO_ROOT: Path = Path(__file__).resolve().parents[3]

TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0019_v2_judge_calibration_sonnet"

# Inputs (read-only).
V2_SONNET_INPUT_PATH: Path = (
    REPO_ROOT
    / "tasks"
    / "t0014_v2_annotator_sonnet_rerun"
    / "assets"
    / "dataset"
    / "hierarchical-annotation-v2-sonnet"
    / "files"
    / "hierarchical_annotation_v2_sonnet.jsonl"
)
V2_HAIKU_CORRECTED_INPUT_PATH: Path = (
    REPO_ROOT
    / "tasks"
    / "t0015_correct_proxy_benchmark_labels"
    / "assets"
    / "dataset"
    / "hierarchical-annotation-v2-relabeled"
    / "files"
    / "hierarchical_annotation_v2_relabeled.jsonl"
)
V1_SONNET_INPUT_PATH: Path = (
    REPO_ROOT
    / "tasks"
    / "t0005_hierarchical_annotation_pilot_v1"
    / "code"
    / "_outputs"
    / "mapped_with_judge.jsonl"
)

# Working outputs (intermediate JSONL).
OUTPUTS_DIR: Path = TASK_ROOT / "data"
SUBSTANTIVE_OUTCOMES_PATH: Path = OUTPUTS_DIR / "substantive_outcomes.jsonl"
MODEL_ROTATED_OUTCOMES_PATH: Path = OUTPUTS_DIR / "model_rotated_outcomes.jsonl"
RUN_LOG_PATH: Path = OUTPUTS_DIR / "run_log.txt"
COMPUTED_STATS_PATH: Path = OUTPUTS_DIR / "computed_stats.json"

# Predictions asset.
PREDICTIONS_ID: str = "v2-judge-calibration"
PREDICTIONS_ASSET_DIR: Path = TASK_ROOT / "assets" / "predictions" / PREDICTIONS_ID
PREDICTIONS_FILES_DIR: Path = PREDICTIONS_ASSET_DIR / "files"
PREDICTIONS_JSONL_PATH: Path = PREDICTIONS_FILES_DIR / "predictions.jsonl"
PREDICTIONS_DETAILS_PATH: Path = PREDICTIONS_ASSET_DIR / "details.json"
PREDICTIONS_DESCRIPTION_PATH: Path = PREDICTIONS_ASSET_DIR / "description.md"

# Answer asset.
ANSWER_ID: str = "does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges"
ANSWER_ASSET_DIR: Path = TASK_ROOT / "assets" / "answer" / ANSWER_ID
ANSWER_DETAILS_PATH: Path = ANSWER_ASSET_DIR / "details.json"
ANSWER_SHORT_PATH: Path = ANSWER_ASSET_DIR / "short_answer.md"
ANSWER_FULL_PATH: Path = ANSWER_ASSET_DIR / "full_answer.md"

# Results.
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"
METRICS_JSON_PATH: Path = RESULTS_DIR / "metrics.json"
ACCEPT_RATE_CHART_PATH: Path = RESULTS_IMAGES_DIR / "accept_rate_3x3.png"
SCHEMA_DELTA_CHART_PATH: Path = RESULTS_IMAGES_DIR / "schema_only_delta_by_judge.png"
