"""Centralised path constants for the hierarchical annotation pilot v1 task."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = Path(__file__).resolve().parents[1]

PILOT_INPUT: Path = REPO_ROOT / "project" / "data" / "annotation_pilot" / "tasks_annotated.jsonl"

CODE_OUTPUTS_DIR: Path = TASK_ROOT / "code" / "_outputs"
MAPPED_OUTPUT: Path = CODE_OUTPUTS_DIR / "mapped.jsonl"
JUDGE_SAMPLE_OUTPUT: Path = CODE_OUTPUTS_DIR / "judge_sample.jsonl"
MAPPED_WITH_JUDGE_OUTPUT: Path = CODE_OUTPUTS_DIR / "mapped_with_judge.jsonl"
JUDGE_COSTS_OUTPUT: Path = CODE_OUTPUTS_DIR / "judge_costs.json"
STATS_OUTPUT: Path = CODE_OUTPUTS_DIR / "stats.json"

DATASET_ASSET_DIR: Path = TASK_ROOT / "assets" / "dataset" / "hierarchical-annotation-v1"
DATASET_FILES_DIR: Path = DATASET_ASSET_DIR / "files"
DATASET_FILE_PATH: Path = DATASET_FILES_DIR / "hierarchical_annotation_v1.jsonl"
DATASET_DETAILS_PATH: Path = DATASET_ASSET_DIR / "details.json"
DATASET_DESCRIPTION_PATH: Path = DATASET_ASSET_DIR / "description.md"

RESULTS_IMAGES_DIR: Path = TASK_ROOT / "results" / "images"
PER_BENCHMARK_CHART_PATH: Path = RESULTS_IMAGES_DIR / "per_benchmark_completeness.png"
ATOMIC_LENGTHS_CHART_PATH: Path = RESULTS_IMAGES_DIR / "atomic_lengths.png"
