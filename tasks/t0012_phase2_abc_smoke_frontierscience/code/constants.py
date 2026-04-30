"""Constants for the phase2 A/B/C smoke harness."""

from __future__ import annotations

from typing import Final

# ---- Dataset filtering ---------------------------------------------------------------------------

BENCHMARK_FILTER: Final[str] = "FrontierScience-Olympiad"

# ---- Models --------------------------------------------------------------------------------------
# IMPORTANT: per-call cost via the local `claude` CLI is dominated by Claude Code's massive system
# prompt cache (~$0.04-0.08/call regardless of our prompt size). To stay under the $20 budget cap
# at N=40 rows × 3 conditions × ~6 turns per row + judge calls (~840 calls total at ~$0.08/call =
# ~$67), the smoke harness uses Haiku for BOTH the agent and the judge. This is a deliberate
# deviation from `plan/plan.md` (which recommended Sonnet for the agent runs) and is documented in
# `results/results_detailed.md` § Methodology and the predictions-asset descriptions. Sonnet was
# attempted in the t0009 dry-run and similarly fell back to Haiku for the same budget reason.

MODEL_AGENT: Final[str] = "claude-haiku-4-5"
MODEL_JUDGE: Final[str] = "claude-haiku-4-5"

# ---- Budget --------------------------------------------------------------------------------------

BUDGET_CAP_USD: Final[float] = 20.0

# ---- Confidence ----------------------------------------------------------------------------------

HIGH_CONFIDENCE_THRESHOLD: Final[float] = 0.75

# ---- Agent loop ----------------------------------------------------------------------------------

# Plan called for max_turns=12, but per-call budget pressure forces a tighter bound. With Haiku at
# ~$0.05-0.08/call, max_turns=4 keeps us in budget at N=40 (40 * 3 * 4 = 480 agent calls + ~120
# judge calls = ~600 calls at ~$0.06 each = ~$36 worst case; halt enforcement keeps it under $20).
MAX_TURNS: Final[int] = 4

RANDOM_SEED: Final[int] = 42

# ---- CLI invocation ------------------------------------------------------------------------------

CLAUDE_CLI: Final[str] = "claude"
CLI_TIMEOUT_SECONDS: Final[int] = 180

# ---- Variant labels (must match registered metric variant_id format) -----------------------------

VARIANT_A: Final[str] = "condition_a_scope_aware"
VARIANT_B: Final[str] = "condition_b_scope_unaware"
VARIANT_C: Final[str] = "condition_c_scope_mismatched"

CONDITION_A_LABEL: Final[str] = "Condition A: scope-aware ReAct"
CONDITION_B_LABEL: Final[str] = "Condition B: scope-unaware Plan-and-Solve"
CONDITION_C_LABEL: Final[str] = "Condition C: scope-mismatched (random)"

# ---- Metric keys (registered in meta/metrics/) ---------------------------------------------------

METRIC_TASK_SUCCESS_RATE: Final[str] = "task_success_rate"
METRIC_OVERCONFIDENT_ERROR_RATE: Final[str] = "overconfident_error_rate"
METRIC_AVG_DECISIONS_PER_TASK: Final[str] = "avg_decisions_per_task"

# ---- Trajectory schema (canonical t0006/t0007/t0010 six-field schema) ----------------------------

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
PRED_FIELD_CONDITION: Final[str] = "condition"
