"""Centralized path constants for t0021 Plan-and-Solve v2 with final_confidence.

All file/dir locations consumed or produced by the task live here so paths can be reasoned about
in one place (per the project Python style guide).
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]

TASK_ROOT: Final[Path] = REPO_ROOT / "tasks" / "t0021_plan_and_solve_v2_with_final_confidence"

# Source dataset (read-only) — t0009 hierarchical annotation v2
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

# Library asset
LIBRARY_DIR: Final[Path] = TASK_ROOT / "assets" / "library" / "scope_unaware_planandsolve_v2"
LIBRARY_FILES_DIR: Final[Path] = LIBRARY_DIR / "files"
LIBRARY_PROMPTS_DIR: Final[Path] = LIBRARY_FILES_DIR / "prompts"
LIBRARY_DETAILS_PATH: Final[Path] = LIBRARY_DIR / "details.json"
LIBRARY_DESCRIPTION_PATH: Final[Path] = LIBRARY_DIR / "description.md"
LIBRARY_PROMPT_PATH: Final[Path] = LIBRARY_PROMPTS_DIR / "confidence_prompt.txt"

# Results / outputs
RESULTS_DIR: Final[Path] = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Final[Path] = RESULTS_DIR / "images"
METRICS_PATH: Final[Path] = RESULTS_DIR / "metrics.json"
COSTS_PATH: Final[Path] = RESULTS_DIR / "costs.json"
SMOKE_PREDICTIONS_PATH: Final[Path] = RESULTS_DIR / "smoke_predictions.jsonl"
SMOKE_REPORT_PATH: Final[Path] = RESULTS_DIR / "smoke_report.json"

# Cost log (per-call) and judge log
COST_LOG_PATH: Final[Path] = RESULTS_DIR / "_call_log.jsonl"
JUDGE_LOG_PATH: Final[Path] = RESULTS_DIR / "_judge_log.jsonl"
