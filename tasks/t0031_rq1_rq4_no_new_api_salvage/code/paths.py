from pathlib import Path

# Repository roots.
# This file lives at:
#   <repo>/tasks/t0031_rq1_rq4_no_new_api_salvage/code/paths.py
# parents[0] = code/, parents[1] = task folder, parents[2] = tasks/, parents[3] = repo root.
WORKTREE_ROOT: Path = Path(__file__).resolve().parents[3]

# The main repo (read-only source of t0026 / t0027 outputs).
MAIN_REPO_ROOT: Path = Path("/Users/lysaniuk/Documents/reasoning-scale2")

# This task's folder (inside the worktree).
TASK_ROOT: Path = Path(__file__).resolve().parents[1]

# Inputs read from the main repo.
VARIANT_A_JSONL: Path = (
    MAIN_REPO_ROOT
    / "tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions"
    / "a-scope-aware/files/predictions_variant_a.jsonl"
)
VARIANT_B_JSONL: Path = (
    MAIN_REPO_ROOT
    / "tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions"
    / "abc-rerun-b/files/predictions_variant_b.jsonl"
)
VARIANT_C_JSONL: Path = (
    MAIN_REPO_ROOT
    / "tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions"
    / "abc-rerun-c/files/predictions_variant_c.jsonl"
)
PAIRED_MANIFEST_JSON: Path = (
    MAIN_REPO_ROOT / "tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/paired_manifest.json"
)
T0026_RESULTS_DETAILED: Path = (
    MAIN_REPO_ROOT / "tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/results_detailed.md"
)
T0027_RESULTS_DETAILED: Path = (
    MAIN_REPO_ROOT / "tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_detailed.md"
)
T0029_TASK_DESCRIPTION: Path = (
    MAIN_REPO_ROOT / "tasks/t0029_rq1_discordance_rich_resample/task_description.md"
)

# Output paths inside this task folder.
RESULTS_DIR: Path = TASK_ROOT / "results"
RESULTS_DATA_DIR: Path = RESULTS_DIR / "data"
RESULTS_IMAGES_DIR: Path = RESULTS_DIR / "images"

RQ4_JSON: Path = RESULTS_DATA_DIR / "rq4_stratification.json"
RQ1_POWER_JSON: Path = RESULTS_DATA_DIR / "rq1_power_grid.json"
LOG_AUDIT_JSON: Path = RESULTS_DATA_DIR / "log_audit.json"

RQ4_HEATMAP_PNG: Path = RESULTS_IMAGES_DIR / "rq4_stratification_heatmap.png"
RQ1_POWER_CURVE_PNG: Path = RESULTS_IMAGES_DIR / "rq1_power_curve.png"
LOG_AUDIT_BAR_PNG: Path = RESULTS_IMAGES_DIR / "log_audit_failure_breakdown.png"

# Standard ARF results files.
RESULTS_SUMMARY_MD: Path = RESULTS_DIR / "results_summary.md"
RESULTS_DETAILED_MD: Path = RESULTS_DIR / "results_detailed.md"
METRICS_JSON: Path = RESULTS_DIR / "metrics.json"
COSTS_JSON: Path = RESULTS_DIR / "costs.json"
REMOTE_MACHINES_JSON: Path = RESULTS_DIR / "remote_machines_used.json"
SUGGESTIONS_JSON: Path = RESULTS_DIR / "suggestions.json"
