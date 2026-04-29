"""Centralized file paths for the scope-aware ReAct library."""

from __future__ import annotations

from pathlib import Path

# Repo root: 3 levels up from this file
# (tasks/t0006_scope_aware_react_library/code/paths.py -> repo root)
REPO_ROOT: Path = Path(__file__).resolve().parents[3]

TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0006_scope_aware_react_library"
CODE_DIR: Path = TASK_ROOT / "code"
ASSETS_DIR: Path = TASK_ROOT / "assets"
LIBRARY_ASSET_DIR: Path = ASSETS_DIR / "library" / "scope_aware_react_v1"

# Default location for trajectory log files when callers do not pass an explicit path.
DEFAULT_TRAJECTORY_DIR: Path = TASK_ROOT / "results" / "trajectories"
