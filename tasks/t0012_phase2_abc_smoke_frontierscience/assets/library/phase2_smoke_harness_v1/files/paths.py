"""Centralized path constants for the phase2 A/B/C smoke harness.

All file/dir locations consumed or produced by the harness live here so paths can be reasoned
about in one place (per the project Python style guide).
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]

TASK_ROOT: Final[Path] = REPO_ROOT / "tasks" / "t0012_phase2_abc_smoke_frontierscience"

V2_DATASET_PATH: Final[Path] = (
    REPO_ROOT
    / "tasks"
    / "t0009_hierarchical_annotation_v2"
    / "assets"
    / "dataset"
    / "hierarchical-annotation-v2"
    / "files"
    / "hierarchical_annotation_v2.jsonl"
)

# Predictions assets
ASSETS_PRED_DIR: Final[Path] = TASK_ROOT / "assets" / "predictions"
PREDICTIONS_A_DIR: Final[Path] = ASSETS_PRED_DIR / "phase2-smoke-a"
PREDICTIONS_B_DIR: Final[Path] = ASSETS_PRED_DIR / "phase2-smoke-b"
PREDICTIONS_C_DIR: Final[Path] = ASSETS_PRED_DIR / "phase2-smoke-c"

PREDICTIONS_A_FILE: Final[Path] = (
    PREDICTIONS_A_DIR / "files" / "predictions-frontierscience-olympiad.jsonl"
)
PREDICTIONS_B_FILE: Final[Path] = (
    PREDICTIONS_B_DIR / "files" / "predictions-frontierscience-olympiad.jsonl"
)
PREDICTIONS_C_FILE: Final[Path] = (
    PREDICTIONS_C_DIR / "files" / "predictions-frontierscience-olympiad.jsonl"
)

# Library asset
LIBRARY_DIR: Final[Path] = TASK_ROOT / "assets" / "library" / "phase2_smoke_harness_v1"

# Results / outputs
RESULTS_DIR: Final[Path] = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Final[Path] = RESULTS_DIR / "images"
METRICS_PATH: Final[Path] = RESULTS_DIR / "metrics.json"
INTERMEDIATE_STATS_PATH: Final[Path] = RESULTS_DIR / "_intermediate_stats.json"

# Per-condition intermediate state for resume support
INTERMEDIATE_A_PATH: Final[Path] = RESULTS_DIR / "_intermediate_a.json"
INTERMEDIATE_B_PATH: Final[Path] = RESULTS_DIR / "_intermediate_b.json"
INTERMEDIATE_C_PATH: Final[Path] = RESULTS_DIR / "_intermediate_c.json"

# Cost log
COST_LOG_PATH: Final[Path] = RESULTS_DIR / "_call_log.jsonl"

# Judge log
JUDGE_LOG_PATH: Final[Path] = RESULTS_DIR / "_judge_log.jsonl"
