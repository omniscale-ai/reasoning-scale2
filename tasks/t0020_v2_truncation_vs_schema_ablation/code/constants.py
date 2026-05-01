"""Constants for the v2 truncation vs schema ablation pipeline (t0020).

This pipeline differs from t0009/t0014 in exactly one way: the `problem` text is truncated to
1500 chars in BOTH annotator and judge prompts (matching the canonical v1 truncation pattern from
t0005). Both annotator and judge are claude-haiku-4-5.

The 1500-char limit and `_truncate(text, *, limit) -> text[:limit] + "…"` helper are copied from
`tasks/t0005_hierarchical_annotation_pilot_v1/code/{constants.py,judge_runner.py}`.
"""

from __future__ import annotations

from typing import Final

# Both annotator and judge use haiku-4-5 in this condition.
ANNOTATOR_MODEL_ID: Final[str] = "claude-haiku-4-5"
JUDGE_MODEL_ID: Final[str] = "claude-haiku-4-5"

APPROX_CHARS_PER_TOKEN: Final[int] = 4

# Haiku 4.5 list price (USD per million tokens), correct at 2026-04-30.
HAIKU_INPUT_COST_PER_MTOK_USD: Final[float] = 0.80
HAIKU_OUTPUT_COST_PER_MTOK_USD: Final[float] = 4.00

# Hard caps. Empirical haiku cost from t0009 was ~$0.076/annotation and t0014 ~$0.07/judge call,
# but the dry-run on row 1 spent $0.16 (15.6k output tokens) because the claude CLI in agentic
# mode produces longer reasoning traces than bare-API invocations. Project per-task limit is $10
# with $51 budget left. Cap annotator at $4 (covers ~25 calls at the dry-run rate) and judge at
# $2 (judge prompts are smaller and produced ~$0.07/call in t0014). Total $6 per task.
ANNOTATOR_BUDGET_CAP_USD: Final[float] = 4.00
JUDGE_BUDGET_CAP_USD: Final[float] = 2.00

# Canonical v1 truncation limit (from t0005).
PROBLEM_EXCERPT_LIMIT: Final[int] = 1500


def _truncate(text: str, *, limit: int) -> str:
    """Hard-cut + ellipsis truncation, exactly as in t0005's judge_runner.py."""
    if len(text) <= limit:
        return text
    return text[:limit] + "…"


ANNOTATOR_SYSTEM_PROMPT: Final[str] = """\
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

# CRITICAL: the only structural change vs t0014 is that `problem` is replaced with a truncated
# excerpt and a header indicating the truncation. Caller passes `problem_excerpt` and `limit`.
ANNOTATOR_USER_TEMPLATE: Final[str] = """\
Benchmark: {benchmark}
Domain: {domain}

Problem (truncated to {limit} chars):
{problem_excerpt}

Produce the v2 hierarchical decomposition JSON now."""

JUDGE_SYSTEM_PROMPT: Final[str] = """\
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

# CRITICAL: the judge sees the SAME truncated excerpt as the annotator did. Header indicates
# truncation explicitly so the judge does not penalize the annotator for missing tail content.
JUDGE_USER_TEMPLATE: Final[str] = """\
Benchmark: {benchmark}
Domain: {domain}

Problem (truncated to {limit} chars):
{problem_excerpt}

Candidate v2 hierarchy:
{hierarchy_json}

Candidate v2 gold_actions:
{gold_actions_json}

Output the JSON verdict now."""
