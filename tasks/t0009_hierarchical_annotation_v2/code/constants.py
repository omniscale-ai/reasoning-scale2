"""Constants for the v2 hierarchical annotation pipeline.

All cost numbers are official Anthropic prices for the dated model snapshots used here. Token
counts are character-based estimates when the CLI does not return usage info.
"""

from __future__ import annotations

ANNOTATOR_MODEL_ID: str = "claude-haiku-4-5"
JUDGE_MODEL_ID: str = "claude-haiku-4-5"

APPROX_CHARS_PER_TOKEN: int = 4

# Sonnet 4.6 list price (USD per million tokens), correct at 2026-04-29. Retained for
# documentation; v2 ultimately uses Haiku for the annotator because the Claude Code CLI overhead
# (system-prompt cache creation per invocation) makes Sonnet ~$0.30 / call, which would bust
# the $15 task-description budget at 115 rows.
SONNET_INPUT_COST_PER_MTOK_USD: float = 3.00
SONNET_OUTPUT_COST_PER_MTOK_USD: float = 15.00

# Haiku 4.5 list price (USD per million tokens).
HAIKU_INPUT_COST_PER_MTOK_USD: float = 0.80
HAIKU_OUTPUT_COST_PER_MTOK_USD: float = 4.00

# Hard caps. Both the annotator and judge use Haiku via the Claude Code CLI. Empirical per-call
# cost is ~$0.06-0.12 due to the CLI's persistent system-prompt cache creation at every invocation.
ANNOTATOR_BUDGET_CAP_USD: float = 13.00
JUDGE_BUDGET_CAP_USD: float = 2.00

SAMPLE_SEED: int = 42

# Stratified judge sample size per benchmark. Totals 23 (>= 20% of 115).
JUDGE_SAMPLE_PER_BENCHMARK: dict[str, int] = {
    "FrontierScience-Olympiad": 6,
    "SWE-bench Verified": 6,
    "WorkArena++": 6,
    "tau-bench": 5,
}

ANNOTATOR_SYSTEM_PROMPT: str = """\
You are a senior research-engineer annotator producing hierarchical decompositions of benchmark \
tasks. You output ONLY a single JSON object that strictly conforms to this schema:

{
  "global": "<one-sentence top-level approach>",
  "subtasks": [
    {"subtask": "<subtask description>", "atomics": ["<atomic step>", ...]},
    ...
  ],
  "global_atomics": ["<cross-cutting atomic step>", ...],
  "gold_actions": {
    "global": "<resolved global action - the concrete thing the agent does>",
    "subtasks": [
      {"subtask": "<resolved subtask action>", "atomics": ["<resolved atomic action>", ...]},
      ...
    ],
    "global_atomics": ["<resolved cross-cutting atomic action>", ...]
  }
}

Decomposition rules:
- "global" is one sentence describing the overall plan.
- Each "subtask" is a concrete intermediate goal needed to achieve "global".
- "atomics" under a subtask are the concrete one-step actions an agent would take to complete \
that subtask.
- "global_atomics" are atomic steps that do not belong to any single subtask: typically final \
verification, sanity checks, or cross-cutting concerns.
- "gold_actions" mirrors the structure but contains the resolved/concrete action labels - the \
specific computations, code, queries, or experiments. Each "subtasks[i]" must align by index with \
"hierarchy.subtasks[i]".
- Output 2-6 subtasks for normal problems. Each subtask should have 1-5 atomics.
- Use 0-3 global_atomics depending on problem.
- Strings should be specific and operational, not vague ("compute the determinant of M" not \
"do calculations").

Output ONLY the JSON object, with no prose before or after, no markdown fencing.
"""

ANNOTATOR_USER_TEMPLATE: str = """\
Benchmark: {benchmark}
Domain: {domain}

Problem:
{problem}

Produce the v2 hierarchical decomposition JSON now."""

JUDGE_SYSTEM_PROMPT: str = """\
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

JUDGE_USER_TEMPLATE: str = """\
Benchmark: {benchmark}
Domain: {domain}

Full problem:
{problem}

Candidate v2 hierarchy:
{hierarchy_json}

Candidate v2 gold_actions:
{gold_actions_json}

Output the JSON verdict now."""

DATASET_CATEGORIES: list[str] = [
    "hierarchical-planning",
    "benchmark-annotation",
    "agent-evaluation",
    "granularity-conditioning",
]
