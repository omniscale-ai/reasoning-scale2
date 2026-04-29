"""Centralized file paths for the benchmark-subset download task."""

from __future__ import annotations

from pathlib import Path

# Repo root: 3 levels up from this file
# (tasks/t0003_download_benchmark_subsets/code/paths.py -> repo root)
REPO_ROOT: Path = Path(__file__).resolve().parents[3]

TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0003_download_benchmark_subsets"
ASSETS_DIR: Path = TASK_ROOT / "assets"
DATASET_DIR: Path = ASSETS_DIR / "dataset"

CODE_DIR: Path = TASK_ROOT / "code"
ACCESS_STATUS_PATH: Path = CODE_DIR / "access_status.json"

PILOT_JSONL: Path = REPO_ROOT / "project" / "data" / "annotation_pilot" / "tasks_annotated.jsonl"

FRONTIERSCIENCE_DIR: Path = DATASET_DIR / "frontierscience-olympiad-subset"
WORKARENA_PP_DIR: Path = DATASET_DIR / "workarena-plus-plus-subset"
SWEBENCH_DIR: Path = DATASET_DIR / "swebench-verified-subset"
TAUBENCH_DIR: Path = DATASET_DIR / "taubench-subset"
