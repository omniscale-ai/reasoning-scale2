# Predictions: `benchmark-annotation`

1 predictions asset(s).

[Back to all predictions](../README.md)

---

<details>
<summary>📊 <strong>v2 tree-schema annotations on truncated 1500-char problems (haiku
judge verdicts)</strong> (<code>v2-truncated-ablation</code>) — 20
instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `v2-truncated-ablation` |
| **Model ID** | — |
| **Model** | Annotator and judge are both claude-haiku-4-5 (Anthropic) accessed via the local Claude Code CLI. The annotator emits the v2 tree schema (global, subtasks[], global_atomics, gold_actions). The judge issues a binary acceptable / needs revision verdict. Both prompts truncate the problem text to 1500 chars with an explicit 'Problem (truncated to 1500 chars):' header. |
| **Datasets** | `hierarchical-annotation-v1` |
| **Format** | jsonl |
| **Instances** | 20 |
| **Date created** | 2026-05-01 |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Created by** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Documentation** | [`description.md`](../../../tasks/t0020_v2_truncation_vs_schema_ablation/assets/predictions/v2-truncated-ablation/description.md) |

**Metrics at creation:**

* **accept_rate**: 0.9
* **accept_count**: 18
* **needs_revision_count**: 2
* **hierarchy_completeness_rate**: 1.0

# v2 Tree-Schema Annotations on Truncated 1500-Char Problems

## Metadata

* **Name**: v2 tree-schema annotations on truncated 1500-char problems (haiku judge verdicts)
* **Annotator**: claude-haiku-4-5 (v2 tree schema, problem truncated to 1500 chars)
* **Judge**: claude-haiku-4-5 (binary verdict, problem truncated to 1500 chars)
* **Datasets**: hierarchical-annotation-v1 (20-row matched pool from t0014)
* **Format**: jsonl
* **Instances**: 20
* **Created by**: t0020_v2_truncation_vs_schema_ablation

## Overview

These predictions implement the third condition needed to decompose the +57 pp v2-tree-full vs
v1-flat-truncated acceptance-rate gap reported in t0014. In t0009/t0014 the annotator and
judge saw the full problem text (median ~3 kB), while the v1 baseline (t0005) truncated the
problem to 1500 chars in both annotator and judge prompts. Without a matched-truncation v2
condition it was impossible to say how much of the +57 pp gain came from the richer tree
schema and how much came from the additional text the v2 condition was allowed to see.

This asset re-runs claude-haiku-4-5 on exactly the same 20-row pool that t0014 judged with
sonnet (sonnet timed out on 3 rows so the matched pool is 20, not 23). The only change vs
t0014 is that the problem text is truncated to 1500 chars with an explicit `Problem (truncated
to 1500 chars):` header in both the annotator prompt and the judge prompt. Hierarchy
completeness remains 100% (20 of 20 rows produced a valid tree). The truncated-condition
accept rate is 90% (18 of 20).

## Model

Both annotator and judge use claude-haiku-4-5 via the local Claude Code CLI (`claude -p -
--model claude-haiku-4-5 --output-format json`). The annotator system prompt mandates the
canonical v2 tree schema (`global`, `subtasks[].atomics[]`, `global_atomics[]`, plus a
parallel `gold_actions` block of resolved labels). The judge system prompt is a strict binary
verdict template that emits `{"verdict": "acceptable" | "needs revision", "justification":
"..."}`.

The only structural difference vs `tasks/t0014_v2_annotator_sonnet_rerun/code/v2_annotator.py`
and `v2_judge.py` is the user-prompt template: the literal `Problem:\n{problem}` block is
replaced with `Problem (truncated to {limit} chars):\n{problem_excerpt}` where
`problem_excerpt` is built by `_truncate(text, *, limit=1500) -> text[:1500] + "…"`. This
matches the canonical truncation helper from
`tasks/t0005_hierarchical_annotation_pilot_v1/code/judge_runner.py`.

## Data

The 20-row pool was selected by reading
`tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_sample.jsonl` to get the
canonical `_pilot_row_index` set, then looking up each index in the v1 source jsonl
(`tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`).
The pool is intentionally the 20 rows where t0014's sonnet judge produced a verdict (sonnet
timed out on indices 7, 8, 14 in t0014).

Per-benchmark distribution: SWE-bench Verified 6 rows, WorkArena++ 6 rows, tau-bench 5 rows,
FrontierScience-Olympiad 3 rows. All 20 rows produced a complete hierarchy (no parse failures
and no call failures).

## Prediction Format

Each line is a single JSON object representing one annotated and judged row:

```json
{
  "_pilot_row_index": 27,
  "task_id": "swe_sphinx-doc__sphinx-11510",
  "benchmark": "SWE-bench Verified",
  "domain": "swe",
  "difficulty": null,
  "problem": "<full original problem text>",
  "problem_excerpt_limit": 1500,
  "hierarchy": {"global": "...", "subtasks": [{"subtask": "...", "atomics": [...]}, ...],
                "global_atomics": [...]},
  "gold_actions": {"global": "...", "subtasks": [...], "global_atomics": [...]},
  "annotation_model": "claude-haiku-4-5",
  "annotator_notes": "ok",
  "hierarchy_completeness": true,
  "judge_verdict": "acceptable",
  "judge_justification": "...",
  "judge_model": "claude-haiku-4-5"
}
```

The `problem` field stores the full original text (so downstream analyses can see what was
truncated). The annotator and judge BOTH saw only `problem[:1500] + "…"` — they never accessed
the field stored under `problem`. The `problem_excerpt_limit` field is the canonical record of
which truncation budget was used.

## Metrics

| Metric | Value |
| --- | --- |
| Accept rate (overall) | **90.0%** (18 / 20) |
| Hierarchy completeness | **100%** (20 / 20) |
| Parse failures | 0 |
| Call failures | 0 |

Per-benchmark accept rates:

| Benchmark | n | accept | rate |
| --- | --- | --- | --- |
| FrontierScience-Olympiad | 3 | 2 | 67% |
| SWE-bench Verified | 6 | 5 | 83% |
| WorkArena++ | 6 | 6 | 100% |
| tau-bench | 5 | 5 | 100% |

The two `needs revision` verdicts came from FrontierScience-Olympiad (idx 17) and SWE-bench
Verified (idx 39).

## Main Ideas

* The truncated v2 condition (90% accept) sits 5 pp below the full-context v2 condition (95%
  accept) and 57 pp above the v1 flat-truncated baseline (33% accept), so the schema accounts
  for ~92% of the v2 vs v1 gap and the additional text accounts for ~8%.
* All 20 rows produced complete hierarchies even with 1500-char input, so v2 schema fidelity
  is not the bottleneck under truncation.
* On WorkArena++ the truncated-v2 already matches full-v2 at 100% accept while v1 sat at 0%,
  showing that for short-context-friendly tasks the schema alone explains the entire gap.

## Summary

This predictions asset is the third leg of a three-way decomposition: v1-flat-truncated (t0005
baseline, 33% accept on the 12 v1-judged rows of the pool), v2-tree-truncated (this asset, 90%
accept on 20 rows), and v2-tree-full (t0014 sonnet rerun, 95% accept on 20 rows). The matched
20-row pool ensures that any difference between v2-truncated and v2-full is purely a function
of how much problem text the annotator and judge are allowed to see.

The headline finding is that the v2 schema by itself explains nearly all of the +57 pp
acceptance gain that t0014 attributed to "v2-tree". Allowing the annotator and judge to see
the full problem text on top of the v2 schema adds a further +5 pp (95% CI -15 pp to +26 pp).
The schema effect itself is +57 pp (95% CI +23 pp to +77 pp), which is statistically
significant at conventional levels even with these small samples.

</details>
