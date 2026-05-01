"""Constants for the abc_harness_metrics library."""

from __future__ import annotations

from typing import Final

# ---- Models ---------------------------------------------------------------------------------

JUDGE_MODEL_DEFAULT: Final[str] = "claude-haiku-4-5"
JUDGE_MODEL_FALLBACK: Final[str] = "claude-sonnet-4-5"

# ---- Budget ---------------------------------------------------------------------------------

MAX_BUDGET_USD: Final[float] = 2.00

# ---- CLI invocation -------------------------------------------------------------------------

CLAUDE_CLI: Final[str] = "claude"
CLI_TIMEOUT_SECONDS: Final[int] = 180

# ---- Prompt template keys (used for cache keying and prompt rendering) ----------------------

PROGRESS_RATE_PROMPT_KEY: Final[str] = "progress_rate.v1"
ERROR_TAXONOMY_PROMPT_KEY: Final[str] = "error_taxonomy.v1"

# ---- Progress-rate prompt (paraphrased from Ma2024 §C.2) -----------------------------------
# Ma2024 (AgentBoard, NeurIPS 2024 D&B): Pearson rho > 0.95 against humans on 1013 environments.
# We use the discrete-subgoal-coverage form: subgoal is hit iff some step in the trajectory
# materially advances toward the milestone described in the subgoal text. The judge returns a
# strict yes/no decision per (subgoal, step) pair.
PROGRESS_RATE_SYSTEM_PROMPT: Final[str] = (
    "You are a strict scientific reviewer judging whether one step of an agent trajectory hits "
    "a specific subgoal milestone. Output exactly one token: 'yes' if the step materially "
    "advances toward the subgoal as described, otherwise 'no'. No other text."
)

PROGRESS_RATE_USER_TEMPLATE: Final[str] = (
    "Subgoal description: {subgoal_description}\n\n"
    "Agent step:\n"
    "  thought: {thought}\n"
    "  action: {action}\n"
    "  observation: {observation}\n\n"
    "Does this step materially advance the subgoal? Answer 'yes' or 'no'."
)

# ---- Error-taxonomy prompt (paraphrased from Li2024 §A.4) ----------------------------------
# Li2024 (Embodied Agent Interface, NeurIPS 2024) defines six error labels for per-step
# attribution. We add an "ok" sentinel so the classifier can be applied to every step.
ERROR_TAXONOMY_SYSTEM_PROMPT: Final[str] = (
    "You are an embodied-agent error analyst. Classify the agent step into exactly one of "
    "these labels and emit only the label string:\n"
    "  - hallucination: the step references entities, tools, or facts that do not exist\n"
    "  - affordance: the step attempts an action incompatible with the environment\n"
    "  - missing_step: the step skips a prerequisite or omits a required action\n"
    "  - extra_step: the step is unnecessary or redundant given the goal\n"
    "  - wrong_order: the step is correct in isolation but executed at the wrong point\n"
    "  - precondition_or_effect: the step's stated precondition or effect is incorrect\n"
    "  - ok: the step is correct and well-grounded\n"
    "Output exactly one of: hallucination, affordance, missing_step, extra_step, wrong_order, "
    "precondition_or_effect, ok. No other text."
)

ERROR_TAXONOMY_USER_TEMPLATE: Final[str] = (
    "Environment state: {environment_state}\n\n"
    "Agent step:\n"
    "  thought: {thought}\n"
    "  action: {action}\n"
    "  observation: {observation}\n\n"
    "Classify this step."
)

# ---- Defaults --------------------------------------------------------------------------------

# When the judge response is ambiguous or unparseable, default to this label per t0022 spec.
DEFAULT_TIE_BREAK_LABEL: Final[str] = "precondition_or_effect"

# Truncation lengths for prompt fields to keep token costs predictable.
MAX_THOUGHT_CHARS: Final[int] = 800
MAX_ACTION_CHARS: Final[int] = 400
MAX_OBSERVATION_CHARS: Final[int] = 800
MAX_SUBGOAL_DESC_CHARS: Final[int] = 400
