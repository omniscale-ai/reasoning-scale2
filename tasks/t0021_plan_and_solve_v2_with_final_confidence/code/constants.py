"""Constants for the t0021 Plan-and-Solve v2 task and its smoke harness."""

from __future__ import annotations

from typing import Final

# ---- Dataset filtering ---------------------------------------------------------------------------

BENCHMARK_FILTER: Final[str] = "FrontierScience-Olympiad"

# ---- Models --------------------------------------------------------------------------------------

MODEL_AGENT: Final[str] = "claude-haiku-4-5"
MODEL_JUDGE: Final[str] = "claude-haiku-4-5"

# ---- Budget --------------------------------------------------------------------------------------

BUDGET_CAP_USD: Final[float] = 1.00
BUDGET_HEADROOM_USD: Final[float] = 0.05

# ---- Confidence ----------------------------------------------------------------------------------

HIGH_CONFIDENCE_THRESHOLD: Final[float] = 0.75

# ---- Agent loop ----------------------------------------------------------------------------------

MAX_TURNS: Final[int] = 4
RANDOM_SEED: Final[int] = 42

# ---- CLI invocation ------------------------------------------------------------------------------

CLAUDE_CLI: Final[str] = "claude"
CLI_TIMEOUT_SECONDS: Final[int] = 180

# ---- Smoke validation budgets --------------------------------------------------------------------

SMOKE_ROW_LIMIT: Final[int] = 5
PARSE_FAILURE_RATE_THRESHOLD: Final[float] = 0.20

# ---- Variant labels ------------------------------------------------------------------------------

VARIANT_A: Final[str] = "condition_a_scope_aware"
VARIANT_B: Final[str] = "condition_b_scope_unaware"
VARIANT_C: Final[str] = "condition_c_scope_mismatched"

CONDITION_A_LABEL: Final[str] = "Condition A: scope-aware ReAct"
CONDITION_B_LABEL: Final[str] = "Condition B: scope-unaware Plan-and-Solve v2"
CONDITION_C_LABEL: Final[str] = "Condition C: scope-mismatched (random)"

# ---- Metric keys ---------------------------------------------------------------------------------

METRIC_TASK_SUCCESS_RATE: Final[str] = "task_success_rate"
METRIC_OVERCONFIDENT_ERROR_RATE: Final[str] = "overconfident_error_rate"
METRIC_AVG_DECISIONS_PER_TASK: Final[str] = "avg_decisions_per_task"

# ---- Trajectory schema (canonical six-field schema) ----------------------------------------------

TRAJECTORY_FIELDS: Final[tuple[str, ...]] = (
    "turn_index",
    "granularity",
    "thought",
    "action",
    "observation",
    "confidence",
)

# ---- Per-row record fields written to predictions JSONL ------------------------------------------

PRED_FIELD_TASK_ID: Final[str] = "task_id"
PRED_FIELD_PROBLEM: Final[str] = "problem"
PRED_FIELD_GOLD: Final[str] = "gold_answer"
PRED_FIELD_FINAL: Final[str] = "final_answer"
PRED_FIELD_IS_CORRECT: Final[str] = "is_correct"
PRED_FIELD_TRAJECTORY: Final[str] = "trajectory"
PRED_FIELD_DECISION_COUNT: Final[str] = "decision_count"
PRED_FIELD_FINAL_CONFIDENCE: Final[str] = "final_confidence"
PRED_FIELD_FINAL_CONFIDENCE_PARSE_FAILURES: Final[str] = "final_confidence_parse_failures"
PRED_FIELD_CONDITION: Final[str] = "condition"
