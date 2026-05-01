"""Constants for t0019 v2 judge calibration with sonnet.

Pricing and model identifiers are fixed at the time of this task and must not be modified during a
run. The substantive critic prompt extends the original t0014 judge prompt with an explicit
"simulate execution" instruction; the model-rotated configuration uses the original t0014 judge
prompt verbatim with a Sonnet model swap.
"""

from __future__ import annotations

# Models.
JUDGE_MODEL_ID: str = "claude-sonnet-4-6"
HAIKU_MODEL_ID: str = "claude-haiku-4-5"

# Sonnet 4.6 pricing (USD per million tokens), correct at 2026-04-30.
SONNET_INPUT_COST_PER_MTOK_USD: float = 3.00
SONNET_OUTPUT_COST_PER_MTOK_USD: float = 15.00

# Hard budget cap for this task (USD).
# Raised from $4.50 to $20.00 per intervention/critical_step_blocked.md option 2 (CLI fallback at
# ~$0.16/call). The OAuth-issued ANTHROPIC_API_KEY in this environment is provisioned only for
# claude-haiku-4-5 quota; all sonnet/opus tiers return 429 immediately. Switching to the local
# `claude` CLI subprocess via the user's Claude Code subscription unblocks Sonnet but charges
# cache-creation tokens on every invocation (~41K tokens at sonnet input rates on the first call,
# dropping on subsequent calls thanks to prompt caching).
BUDGET_CAP_USD: float = 20.00

# Validation gate thresholds.
VALIDATION_LIMIT: int = 5
# Per-call cost cap raised in lock-step with the budget bump: the CLI fallback's first call
# was $0.16 in the intervention probe; we keep some headroom above that.
VALIDATION_PER_CALL_COST_CAP_USD: float = 0.20

# Annotator labels used as variant dimensions.
ANNOTATOR_V1_SONNET: str = "v1-sonnet"
ANNOTATOR_V2_HAIKU: str = "v2-haiku"
ANNOTATOR_V2_SONNET: str = "v2-sonnet"

# Judge configuration labels.
JUDGE_ORIGINAL_HAIKU: str = "original-haiku"
JUDGE_SUBSTANTIVE: str = "substantive-sonnet"
JUDGE_MODEL_ROTATED: str = "model-rotated-sonnet"

# Prompt-version short codes used in predictions JSONL.
PROMPT_KIND_ORIGINAL: str = "original_haiku"
PROMPT_KIND_SUBSTANTIVE: str = "substantive"
PROMPT_KIND_MODEL_ROTATED: str = "model_rotated"

VERDICT_ACCEPTABLE: str = "acceptable"
VERDICT_NEEDS_REVISION: str = "needs revision"

# Original t0014 judge prompts (verbatim copies for the model-rotated config).
ORIGINAL_JUDGE_SYSTEM_PROMPT: str = """\
You are an expert reviewer evaluating hierarchical decompositions of benchmark problems. \
You output ONLY a single JSON object: {"verdict": "acceptable" | "needs revision", \
"justification": "<one to two sentences>"}.

A decomposition is "acceptable" if:
- "global" captures the overall plan in one sentence,
- the union of subtasks covers what the problem actually asks for,
- atomics under each subtask are operational steps that, executed in order, would complete \
that subtask,
- "global_atomics" contains only steps that genuinely cross subtasks (verification, final \
checks, etc.),
- gold_actions mirrors the same structure with specific resolved actions.

It "needs revision" if any of the above fail clearly.

Output ONLY the JSON object, with no prose before or after, no markdown fencing.
"""

ORIGINAL_JUDGE_USER_TEMPLATE: str = """\
Benchmark: {benchmark}
Domain: {domain}

Full problem:
{problem}

Candidate v2 hierarchy:
{hierarchy_json}

Candidate v2 gold_actions:
{gold_actions_json}

Output the JSON verdict now."""

# Substantive critic system prompt. Extends the original with explicit simulate-execution
# instructions and an optional sub_scores schema.
SUBSTANTIVE_JUDGE_SYSTEM_PROMPT: str = """\
You are an expert reviewer evaluating hierarchical decompositions of benchmark problems. \
You output ONLY a single JSON object: {"verdict": "acceptable" | "needs revision", \
"justification": "<one to two sentences>", "sub_scores": {"coverage": 0|1, \
"executable": 0|1, "gold_actions_consistency": 0|1}}.

A decomposition is "acceptable" if:
- "global" captures the overall plan in one sentence,
- the union of subtasks covers what the problem actually asks for,
- atomics under each subtask are operational steps that, executed in order, would complete \
that subtask,
- "global_atomics" contains only steps that genuinely cross subtasks (verification, final \
checks, etc.),
- gold_actions mirrors the same structure with specific resolved actions.

Before deciding, mentally simulate executing the atomics in the listed order against the \
original problem statement. Mark "acceptable" only if the simulated execution would actually \
solve the problem; mark "needs revision" if the simulated execution exposes any missing, \
incorrect, or non-operational step.

Sub-score definitions (each in {0, 1}):
- "coverage": 1 if the union of subtasks fully covers what the problem asks for, else 0.
- "executable": 1 if the atomics are concrete operational steps that the agent could actually \
perform in order, else 0.
- "gold_actions_consistency": 1 if gold_actions mirrors the hierarchy structure with specific \
resolved actions, else 0.

Output ONLY the JSON object, with no prose before or after, no markdown fencing.
"""

# Substantive prompt user-side template is identical to the original; only the system prompt
# differs.
SUBSTANTIVE_JUDGE_USER_TEMPLATE: str = ORIGINAL_JUDGE_USER_TEMPLATE
