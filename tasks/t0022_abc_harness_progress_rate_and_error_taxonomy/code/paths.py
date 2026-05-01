"""Path constants for the abc_harness_metrics library.

All paths are absolute, computed relative to this file's location, so the
library works correctly regardless of the caller's current working directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---- Repository / task roots ----------------------------------------------------------------

# tasks/t0022_*/code/paths.py -> repo root is .parents[3]
REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]

TASK_ROOT: Final[Path] = REPO_ROOT / "tasks" / "t0022_abc_harness_progress_rate_and_error_taxonomy"

# ---- Code-internal directories --------------------------------------------------------------

CODE_DIR: Final[Path] = TASK_ROOT / "code"
JUDGE_CACHE_DIR: Final[Path] = CODE_DIR / "_cache"
COST_LOG_PATH: Final[Path] = CODE_DIR / "_cost_log.jsonl"

# ---- Replay-validation outputs --------------------------------------------------------------

REPLAY_SUMMARY_PATH: Final[Path] = CODE_DIR / "replay_summary.json"

# ---- t0012 prediction inputs ---------------------------------------------------------------

T0012_ROOT: Final[Path] = REPO_ROOT / "tasks" / "t0012_phase2_abc_smoke_frontierscience"
T0012_PREDICTIONS_DIR: Final[Path] = T0012_ROOT / "assets" / "predictions"
T0012_PRED_FILE: Final[str] = "predictions-frontierscience-olympiad.jsonl"

T0012_PRED_A: Final[Path] = T0012_PREDICTIONS_DIR / "phase2-smoke-a" / "files" / T0012_PRED_FILE
T0012_PRED_B: Final[Path] = T0012_PREDICTIONS_DIR / "phase2-smoke-b" / "files" / T0012_PRED_FILE
T0012_PRED_C: Final[Path] = T0012_PREDICTIONS_DIR / "phase2-smoke-c" / "files" / T0012_PRED_FILE

# ---- Library asset paths -------------------------------------------------------------------

LIBRARY_ASSET_ROOT: Final[Path] = TASK_ROOT / "assets" / "library" / "abc_harness_metrics"
LIBRARY_ASSET_FILES_DIR: Final[Path] = LIBRARY_ASSET_ROOT / "files"
LIBRARY_DETAILS_PATH: Final[Path] = LIBRARY_ASSET_ROOT / "details.json"
LIBRARY_DESCRIPTION_PATH: Final[Path] = LIBRARY_ASSET_ROOT / "description.md"

SUBGOALS_FRONTIERSCIENCE_JSON: Final[Path] = (
    LIBRARY_ASSET_FILES_DIR / "subgoals_frontierscience_olympiad.json"
)
SUBGOALS_SWEBENCH_JSON: Final[Path] = (
    LIBRARY_ASSET_FILES_DIR / "subgoals_swebench_verified_lite.json"
)
