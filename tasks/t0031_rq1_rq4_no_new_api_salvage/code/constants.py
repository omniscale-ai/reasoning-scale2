from enum import StrEnum

# Column names appearing in the JSONL prediction rows.
INSTANCE_ID: str = "instance_id"
SUBSET: str = "subset"
VARIANT: str = "variant"
JUDGE_SUCCESS: str = "judge_sonnet_success"
RECOVERY_PATH: str = "plan_parser_recovery_path"
COST_USD: str = "cost_usd"


class ArmKind(StrEnum):
    ARM_A = "arm_a"
    ARM_B = "arm_b"
    ARM_C = "arm_c"


class SubsetKind(StrEnum):
    SWEBENCH = "swebench"
    FRONTSCI = "frontsci"
    TAUBENCH = "taubench"


class RecoveryPath(StrEnum):
    CLEAN = "clean"
    REPROMPT = "reprompt"
    JSON_FALLBACK = "json_fallback"
    ALL_FAILED = "all_failed"
    UNKNOWN = "unknown"


# t0029 power-analysis parameters (from t0029 task_description.md).
HARD_CAP_USD: float = 35.00
COST_PER_PAIR_USD: float = 0.16
DISCORDANCE_TARGET: int = 30
B_WINS_GRID: tuple[float, ...] = (0.55, 0.60, 0.65, 0.70, 0.75, 0.80)
ALPHA: float = 0.05

# t0027 paired set size.
EXISTING_PAIRED_N: int = 130
EXISTING_PER_SUBSET: dict[str, int] = {
    SubsetKind.SWEBENCH.value: 20,
    SubsetKind.FRONTSCI.value: 26,
    SubsetKind.TAUBENCH.value: 84,
}

# Subset display order (used for table rows and chart subplot order).
SUBSET_ORDER: tuple[str, ...] = (
    SubsetKind.SWEBENCH.value,
    SubsetKind.FRONTSCI.value,
    SubsetKind.TAUBENCH.value,
)

# Pre-fix (t0026) hard-failure aggregates documented in t0026/results/results_detailed.md.
T0026_HARD_FAILURES_PRE_FIX: dict[str, dict[str, int]] = {
    # In t0026 internal labelling: A = scope-aware (=> arm_b after t0031 inversion).
    "a_t0026_scope_aware": {
        "timeouts": 12,
        "runtime_errors": 1,
        "malformed_plan_errors": 0,
        "total": 13,
        "n_attempted": 147,
    },
    # In t0026 internal labelling: B = plan-and-solve v2 (=> arm_a after t0031 inversion).
    "b_t0026_plan_and_solve_v2": {
        "timeouts": 22,
        "runtime_errors": 2,
        "malformed_plan_errors": 16,
        "total": 40,
        "n_attempted": 147,
    },
    # In t0026 internal labelling: C = mismatched-strategy.
    "c_t0026_mismatched": {
        "timeouts": 43,
        "runtime_errors": 1,
        "malformed_plan_errors": 0,
        "total": 44,
        "n_attempted": 147,
    },
}
