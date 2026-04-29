"""Path constants for the metric2_calibration_aggregator_v1 library.

All filesystem paths used by this task's code live here so they can be referenced from a single
place. Paths are relative to the repository root unless explicitly absolute.
"""

from __future__ import annotations

from pathlib import Path

TASK_ID: str = "t0011_metric2_calibration_aggregator"
"""Task identifier; matches the task folder name."""

TASKS_ROOT: Path = Path("tasks")
"""Top-level directory containing all task folders."""

TASK_ROOT: Path = TASKS_ROOT / TASK_ID
"""Path to this task's folder, relative to the repository root."""

CODE_DIR: Path = TASK_ROOT / "code"
"""Path to this task's code directory."""

ASSETS_DIR: Path = TASK_ROOT / "assets"
"""Path to this task's assets directory."""

LIBRARY_ASSET_ROOT: Path = ASSETS_DIR / "library"
"""Path to this task's library assets root."""

LIBRARY_ID: str = "metric2_calibration_aggregator_v1"
"""Library asset slug for the calibration aggregator produced by this task."""

LIBRARY_ASSET_DIR: Path = LIBRARY_ASSET_ROOT / LIBRARY_ID
"""Path to this task's single library asset directory."""

LIBRARY_DETAILS_PATH: Path = LIBRARY_ASSET_DIR / "details.json"
"""Path to the library asset's details.json file."""

LIBRARY_DESCRIPTION_PATH: Path = LIBRARY_ASSET_DIR / "description.md"
"""Path to the library asset's description.md file."""
