"""Centralized path constants for the t0026 phase-2 A/B/C runtime."""

from __future__ import annotations

from pathlib import Path
from typing import Final

TASK_ID: Final[str] = "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
SEED: Final[int] = 20260502

REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
TASK_ROOT: Final[Path] = REPO_ROOT / "tasks" / TASK_ID

DATA_DIR: Final[Path] = TASK_ROOT / "data"
PREFLIGHT_DIR: Final[Path] = DATA_DIR / "preflight"
RUNS_DIR: Final[Path] = DATA_DIR / "runs"
JUDGES_DIR: Final[Path] = DATA_DIR / "judges"

INSTANCE_MANIFEST_PATH: Final[Path] = DATA_DIR / "instance_manifest.json"
COST_REESTIMATE_PATH: Final[Path] = DATA_DIR / "cost_reestimate.json"
SMOKE_TEST_PATH: Final[Path] = DATA_DIR / "smoke_test.json"
CALIBRATION_PATH: Final[Path] = DATA_DIR / "calibration.json"
MCNEMAR_RESULTS_PATH: Final[Path] = DATA_DIR / "mcnemar_results.json"
JUDGE_AGREEMENT_PATH: Final[Path] = DATA_DIR / "judge_agreement.json"

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

ASSETS_PREDICTIONS_DIR: Final[Path] = TASK_ROOT / "assets" / "predictions"
PREDICTIONS_A_DIR: Final[Path] = ASSETS_PREDICTIONS_DIR / "a-scope-aware"
PREDICTIONS_B_DIR: Final[Path] = ASSETS_PREDICTIONS_DIR / "b-plan-and-solve"
PREDICTIONS_C_DIR: Final[Path] = ASSETS_PREDICTIONS_DIR / "c-mismatched"

RESULTS_DIR: Final[Path] = TASK_ROOT / "results"

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

PREFLIGHT_PER_SUBSET: Final[int] = 5
HARD_BUDGET_CAP_USD: Final[float] = 145.0
