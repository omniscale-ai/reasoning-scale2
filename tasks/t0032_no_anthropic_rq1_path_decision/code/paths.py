from __future__ import annotations

from pathlib import Path

# Repository root is four levels up from this file:
# tasks/t0032_.../code/paths.py -> tasks/t0032_.../code -> tasks/t0032_... -> tasks -> repo root
REPO_ROOT: Path = Path(__file__).resolve().parents[3]

# This task folder
TASK_ID: str = "t0032_no_anthropic_rq1_path_decision"
TASK_DIR: Path = REPO_ROOT / "tasks" / TASK_ID
CODE_DIR: Path = TASK_DIR / "code"

# Upstream input JSON sidecars
T0031_DATA_DIR: Path = REPO_ROOT / "tasks" / "t0031_rq1_rq4_no_new_api_salvage" / "results" / "data"
RQ1_POWER_GRID_PATH: Path = T0031_DATA_DIR / "rq1_power_grid.json"
RQ4_STRATIFICATION_PATH: Path = T0031_DATA_DIR / "rq4_stratification.json"
LOG_AUDIT_PATH: Path = T0031_DATA_DIR / "log_audit.json"

T0026_COSTS_PATH: Path = (
    REPO_ROOT / "tasks" / "t0026_phase2_abc_runtime_n147_for_rq1_rq5" / "results" / "costs.json"
)
T0027_COSTS_PATH: Path = (
    REPO_ROOT / "tasks" / "t0027_phase2_5_abc_rerun_with_fixed_b_and_c" / "results" / "costs.json"
)

# Outputs produced by this task's code
DECISION_INPUTS_PATH: Path = CODE_DIR / "decision_inputs.json"
COMPARISON_TABLE_PATH: Path = CODE_DIR / "comparison_table.md"
