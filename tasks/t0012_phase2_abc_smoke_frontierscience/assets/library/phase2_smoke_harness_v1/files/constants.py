"""Constants for the phase2 A/B/C smoke harness."""

from __future__ import annotations

from typing import Final

# ---- Dataset filtering ---------------------------------------------------------------------------

BENCHMARK_FILTER: Final[str] = "FrontierScience-Olympiad"

# ---- Models --------------------------------------------------------------------------------------
# The previous run paid ~$0.10/call because the local Claude Code CLI's default system prompt
# (~50k tokens) is cache-created on every invocation. ``model_call.py`` now overrides this with
# ``--system-prompt`` + ``--tools ""`` + ``--setting-sources ""`` which drops per-call cost to
# ~$0.004 with cache reuse (25× reduction). With that knob in place, Sonnet would still cost ~5×
# more than Haiku per call. Plan recommended ``claude-sonnet-4-6-20251001`` for the agent and
# ``claude-haiku-4-5-20251001`` for the judge; we keep Haiku for the agent in the smoke run for
# safety margin and document this in ``results/results_detailed.md`` and the predictions-asset
# descriptions. Multi-provider replication (Sonnet + Gemini + GPT-5) is queued as a follow-up
# suggestion.

MODEL_AGENT: Final[str] = "claude-haiku-4-5"
MODEL_JUDGE: Final[str] = "claude-haiku-4-5"

# ---- Budget --------------------------------------------------------------------------------------

BUDGET_CAP_USD: Final[float] = 20.0

# ---- Confidence ----------------------------------------------------------------------------------

HIGH_CONFIDENCE_THRESHOLD: Final[float] = 0.75

# ---- Agent loop ----------------------------------------------------------------------------------

# Plan called for max_turns=12. With per-call cost reduced to ~$0.004 via the system-prompt knob
# (see ``model_call.py``), max_turns=8 keeps us comfortably in budget: 40 rows * 3 conditions * 8
# turns ≈ 960 calls + ~120 judge calls ≈ 1080 calls at $0.004 ≈ $4.30. The budget halt at $20 cap
# still enforces a hard stop in case of cache-miss spikes.
MAX_TURNS: Final[int] = 8

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
