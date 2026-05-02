"""Centralized path constants for the t0027 phase-2.5 A/B/C re-run.

Forked from t0026 with task-id rebased and additional re-run paths added. Variant A predictions are
not re-generated in this task; the t0026 A predictions are reused by reference (see
``T0026_PREDICTIONS_A_DIR``). Variants B and C are re-run with the new ``plan_and_solve_v3`` and
``matched_mismatch_v2`` libraries.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

TASK_ID: Final[str] = "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
SOURCE_TASK_ID: Final[str] = "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
SEED: Final[int] = 20260502

REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
TASK_ROOT: Final[Path] = REPO_ROOT / "tasks" / TASK_ID
SOURCE_TASK_ROOT: Final[Path] = REPO_ROOT / "tasks" / SOURCE_TASK_ID

DATA_DIR: Final[Path] = TASK_ROOT / "data"
PREFLIGHT_DIR: Final[Path] = DATA_DIR / "preflight"
RUNS_DIR: Final[Path] = DATA_DIR / "runs"
JUDGES_DIR: Final[Path] = DATA_DIR / "judges"

INSTANCE_MANIFEST_PATH: Final[Path] = DATA_DIR / "instance_manifest.json"
PAIRED_MANIFEST_PATH: Final[Path] = DATA_DIR / "paired_manifest.json"
PARSER_FAILURE_PATH: Final[Path] = DATA_DIR / "parser_failure_count.json"
SMOKE_TEST_PATH: Final[Path] = DATA_DIR / "smoke_test.json"
CALIBRATION_PATH: Final[Path] = DATA_DIR / "calibration.json"
MCNEMAR_RESULTS_PATH: Final[Path] = DATA_DIR / "mcnemar_results.json"

DATASETS_DIR: Final[Path] = (
    REPO_ROOT / "tasks" / "t0003_download_benchmark_subsets" / "assets" / "dataset"
)
SWEBENCH_JSONL_PATH: Final[Path] = (
    DATASETS_DIR / "swebench-verified-subset" / "files" / "swebench-verified-subset.jsonl"
)
TAUBENCH_JSONL_PATH: Final[Path] = (
    DATASETS_DIR / "taubench-subset" / "files" / "taubench-subset.jsonl"
)
FRONTIERSCIENCE_JSONL_PATH: Final[Path] = (
    DATASETS_DIR
    / "frontierscience-olympiad-subset"
    / "files"
    / "frontierscience-olympiad-subset.jsonl"
)

# Reused source assets from t0026.
T0026_PREDICTIONS_DIR: Final[Path] = SOURCE_TASK_ROOT / "assets" / "predictions"
T0026_PREDICTIONS_A_DIR: Final[Path] = T0026_PREDICTIONS_DIR / "a-scope-aware"
T0026_PREDICTIONS_B_DIR: Final[Path] = T0026_PREDICTIONS_DIR / "b-plan-and-solve"
T0026_PREDICTIONS_C_DIR: Final[Path] = T0026_PREDICTIONS_DIR / "c-mismatched"
T0026_PREDICTIONS_A_JSONL: Final[Path] = (
    T0026_PREDICTIONS_A_DIR / "files" / "predictions_variant_a.jsonl"
)
T0026_PREDICTIONS_B_JSONL: Final[Path] = (
    T0026_PREDICTIONS_B_DIR / "files" / "predictions_variant_b.jsonl"
)
T0026_PREDICTIONS_C_JSONL: Final[Path] = (
    T0026_PREDICTIONS_C_DIR / "files" / "predictions_variant_c.jsonl"
)
T0026_INSTANCE_MANIFEST_PATH: Final[Path] = SOURCE_TASK_ROOT / "data" / "instance_manifest.json"
T0026_CALIBRATION_PATH: Final[Path] = SOURCE_TASK_ROOT / "data" / "calibration.json"

ASSETS_PREDICTIONS_DIR: Final[Path] = TASK_ROOT / "assets" / "predictions"
PREDICTIONS_A_REUSED_DIR: Final[Path] = ASSETS_PREDICTIONS_DIR / "abc-rerun-a-reused"
PREDICTIONS_B_DIR: Final[Path] = ASSETS_PREDICTIONS_DIR / "abc-rerun-b"
PREDICTIONS_C_DIR: Final[Path] = ASSETS_PREDICTIONS_DIR / "abc-rerun-c"
PREDICTIONS_B_JSONL: Final[Path] = PREDICTIONS_B_DIR / "files" / "predictions_variant_b.jsonl"
PREDICTIONS_C_JSONL: Final[Path] = PREDICTIONS_C_DIR / "files" / "predictions_variant_c.jsonl"

ASSETS_LIBRARY_DIR: Final[Path] = TASK_ROOT / "assets" / "library"
LIBRARY_PNS_V3_DIR: Final[Path] = ASSETS_LIBRARY_DIR / "plan_and_solve_v3"
LIBRARY_MM_V2_DIR: Final[Path] = ASSETS_LIBRARY_DIR / "matched_mismatch_v2"

RESULTS_DIR: Final[Path] = TASK_ROOT / "results"
RESULTS_IMAGES_DIR: Final[Path] = RESULTS_DIR / "images"
METRICS_PATH: Final[Path] = RESULTS_DIR / "metrics.json"

SUBSET_SWEBENCH: Final[str] = "swebench"
SUBSET_TAUBENCH: Final[str] = "taubench"
SUBSET_FRONTSCI: Final[str] = "frontsci"

SUBSETS: Final[tuple[str, str, str]] = (SUBSET_SWEBENCH, SUBSET_TAUBENCH, SUBSET_FRONTSCI)

VARIANT_A: Final[str] = "a"
VARIANT_B: Final[str] = "b"
VARIANT_C: Final[str] = "c"
VARIANTS: Final[tuple[str, str, str]] = (VARIANT_A, VARIANT_B, VARIANT_C)

MODEL_UNDER_TEST: Final[str] = "claude-sonnet-4-6"
JUDGE_MODEL_PRIMARY: Final[str] = "claude-sonnet-4-6"
JUDGE_MODEL_INTER: Final[str] = "claude-opus-4-7"
FORBIDDEN_HAIKU_MODEL_ID: Final[str] = "claude-haiku-4-5"

N_SWEBENCH_TARGET: Final[int] = 20
N_TAUBENCH_TARGET: Final[int] = 87
N_FRONTSCI_TARGET: Final[int] = 40
N_TOTAL_TARGET: Final[int] = 147
N_PAIRED_EXPECTED: Final[int] = 130

PREFLIGHT_PER_SUBSET: Final[int] = 5
HARD_BUDGET_CAP_USD: Final[float] = 50.0
PER_STREAM_HARD_STOP_USD: Final[float] = 25.0
