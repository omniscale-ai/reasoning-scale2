"""Constants for the hierarchical annotation pilot v1 task."""

from __future__ import annotations

from typing import Final

# Benchmark slugs as they appear in the imported pilot file.
BENCHMARK_FRONTIER: Final[str] = "FrontierScience-Olympiad"
BENCHMARK_SWEBENCH: Final[str] = "SWE-bench Verified"
BENCHMARK_TAUBENCH: Final[str] = "tau-bench"
BENCHMARK_WORKARENA: Final[str] = "WorkArena++"

ALL_BENCHMARKS: Final[tuple[str, ...]] = (
    BENCHMARK_FRONTIER,
    BENCHMARK_SWEBENCH,
    BENCHMARK_TAUBENCH,
    BENCHMARK_WORKARENA,
)

# Node types observed in the input data and how they map to the project's
# three-level hierarchy.
NODE_TYPE_STRATEGIC: Final[str] = "strategic"
NODE_TYPE_CONCEPTUAL: Final[str] = "conceptual"
NODE_TYPE_COMPUTATIONAL: Final[str] = "computational"
NODE_TYPE_VERIFICATION: Final[str] = "verification"

ATOMIC_NODE_TYPES: Final[frozenset[str]] = frozenset(
    {NODE_TYPE_COMPUTATIONAL, NODE_TYPE_VERIFICATION},
)

# Judge configuration.
JUDGE_MODEL_ID: Final[str] = "claude-haiku-4-5-20251001"
JUDGE_PROBLEM_EXCERPT_LIMIT: Final[int] = 1500
JUDGE_BUDGET_CAP_USD: Final[float] = 5.0
JUDGE_RANDOM_SEED: Final[int] = 42
JUDGE_ROWS_PER_BENCHMARK: Final[int] = 3

# Verbalized-confidence prompt template (Xiong2023). The judge must respond
# with strict JSON that python json.loads can parse.
JUDGE_SYSTEM_PROMPT: Final[str] = (
    "You audit hierarchical decompositions of benchmark agent tasks. "
    "Respond with strict JSON only — no markdown fences, no prose."
)
JUDGE_USER_PROMPT_TEMPLATE: Final[str] = (
    "You are auditing a hierarchical decomposition of a benchmark task.\n"
    "Benchmark: {benchmark}\n"
    "Domain: {domain}\n"
    "Problem (truncated to {limit} chars):\n{problem_excerpt}\n\n"
    "Proposed hierarchy:\n"
    "  global: {global_label}\n"
    "  subtasks: {subtasks_joined}\n"
    "  atomic actions: {atomic_joined}\n\n"
    "Question: Is this decomposition acceptable as a global / subtask / atomic\n"
    "labelling of the problem? Respond with strict JSON of the form\n"
    '{{"verdict": "acceptable" | "needs revision",\n'
    '  "justification": "<one sentence>"}}\n'
    "Output ONLY the JSON object."
)

# Approximate cost per 1M tokens for claude-haiku-4-5-20251001. These are used
# as a defensive cap; the runner reads token counts from the CLI's JSON output
# when available. When unavailable, it estimates from string length.
HAIKU_INPUT_COST_PER_MTOK_USD: Final[float] = 1.0
HAIKU_OUTPUT_COST_PER_MTOK_USD: Final[float] = 5.0
APPROX_CHARS_PER_TOKEN: Final[int] = 4

# Dataset asset metadata.
DATASET_ID: Final[str] = "hierarchical-annotation-v1"
DATASET_NAME: Final[str] = "Hierarchical Annotation v1 (115-row pilot audit)"
DATASET_VERSION: Final[str] = "v1"
DATASET_LICENSE: Final[str] = "inherited-per-row"
DATASET_ACCESS_KIND: Final[str] = "restricted"
DATASET_CATEGORIES: Final[tuple[str, ...]] = (
    "hierarchical-planning",
    "benchmark-annotation",
    "agent-evaluation",
)
TASK_ID: Final[str] = "t0005_hierarchical_annotation_pilot_v1"
DATE_TODAY_ISO: Final[str] = "2026-04-29"
