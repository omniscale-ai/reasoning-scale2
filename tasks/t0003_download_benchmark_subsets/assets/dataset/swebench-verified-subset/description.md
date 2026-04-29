---
spec_version: "2"
dataset_id: "swebench-verified-subset"
summarized_by_task: "t0003_download_benchmark_subsets"
date_summarized: "2026-04-29"
---
# SWE-bench Verified Subset (4-8 hunks)

## Metadata

* **Name**: SWE-bench Verified subset (4-8 hunks)
* **Year**: 2024
* **Authors**: Carlos E. Jimenez et al. (parent SWE-bench); the OpenAI Verified curation team
  (Verified)
* **License**: MIT (parent SWE-bench license)
* **Access**: public (HuggingFace `princeton-nlp/SWE-bench_Verified`)
* **Size**: 60 instances (filtered from 500 Verified)

## Overview

This subset of SWE-bench Verified contains GitHub-issue-driven repository patch tasks where the gold
patch has between 4 and 8 diff hunks (the canonical 4-8 decisions per task range). SWE-bench
Verified is the 500-instance human-validated subset of the parent SWE-bench (Jimenez et al. 2023)
released by OpenAI in 2024. Each instance gives an LLM agent a real GitHub issue plus the
corresponding repository at a specific commit, and asks for a patch that passes a hidden test suite.
The full 500 Verified instances have hunk counts ranging from 1 to 45 with a long tail; filtering to
4-8 hunks selects medium-complexity tasks that map cleanly onto the project's three-level hierarchy:
the issue text is the global intent, the FAIL_TO_PASS test names are the subtask gates, and each
diff hunk is one atomic edit decision.

## Content & Annotation

Every row preserves the upstream Verified schema: `instance_id`, `repo`, `base_commit`, `patch`
(gold patch), `test_patch` (gold test diff), `problem_statement` (the GitHub issue body),
`hints_text`, `created_at`, `version`, `FAIL_TO_PASS` (string-encoded list of pytest IDs that should
now pass), `PASS_TO_PASS` (regression tests that must still pass), `environment_setup_commit`, and
`difficulty` (one of `<15 min fix`, `15 min - 1 hour`, `1-4 hours`, `>4 hours`). The annotation is
the gold patch produced by the original GitHub PR author and validated by OpenAI's Verified curation
pass.

## Statistics

| Metric | Value |
| --- | --- |
| Verified total | 500 |
| Subset (4-8 hunks) | 60 |

### Per-hunk-count distribution within subset

| Hunks | Instances |
| --- | --- |
| 4 | 24 |
| 5 | 12 |
| 6 | 14 |
| 7 | 7 |
| 8 | 3 |

### Top repositories in subset

| Repo | Instances |
| --- | --- |
| django/django | 19 |
| sympy/sympy | 8 |
| pydata/xarray | 6 |
| scikit-learn/scikit-learn | 6 |
| pylint-dev/pylint | 5 |
| sphinx-doc/sphinx | 5 |
| pytest-dev/pytest | 4 |
| astropy/astropy | 3 |
| matplotlib/matplotlib | 3 |
| mwaskom/seaborn | 1 |

### Difficulty in subset

| Difficulty | Instances |
| --- | --- |
| 1-4 hours | 19 |
| 15 min - 1 hour | 35 |
| <15 min fix | 5 |
| >4 hours | 1 |

### Subset rule

Instances are kept iff the gold `patch` field contains between 4 and 8 `@@ -` hunk headers
(inclusive). Hunk count is the natural per-instance decision count for SWE-bench: each hunk
corresponds to one localized edit the agent must produce. No random sampling is performed.

## Usage Notes

Load with pyarrow:

```python
import pyarrow.parquet as pq
t = pq.read_table('files/swebench-verified-subset.parquet')
rows = t.to_pylist()  # list[dict]
```

Or as JSONL via the bundled lightweight `swebench-verified-subset.jsonl` (one parsed row per line).
The parquet preserves binary encoding for `patch`/`test_patch`; the JSONL converts those fields to
plain UTF-8 strings. FAIL_TO_PASS and PASS_TO_PASS arrive as JSON-encoded strings; decode with
`json.loads(row['FAIL_TO_PASS'])` to get the list.

## Main Ideas

* The 4-8-hunk filter selects medium-complexity SWE-bench Verified tasks that are large enough to
  exercise multi-step reasoning but small enough to fit in a single agent context window without
  aggressive truncation.
* Each diff hunk maps one-to-one onto an atomic edit decision in the project's three-level hierarchy
  (global issue intent -> FAIL_TO_PASS subtask gates -> per-hunk atomic edits).
* The subset preserves the upstream license (MIT), schema, and instance IDs, so any Phase 2 result
  on this subset can be cross-referenced against the public princeton-nlp/SWE-bench_Verified
  leaderboard.
* Difficulty distribution within the subset is dominated by `15 min - 1 hour` and `<15 min fix`
  tasks, matching the project's wall-clock budget for per-instance runs.

## Summary

This SWE-bench Verified subset contains 60 GitHub-issue-driven patch tasks filtered from the
500-instance Verified release to those whose gold patch has 4 to 8 diff hunks (the project's
canonical multi-step decision range). Each row preserves the upstream Verified schema verbatim,
including problem statement, gold patch, test patch, and the FAIL_TO_PASS / PASS_TO_PASS test name
lists.

For this project, the subset is the primary atomic-execution test bed for the scope-aware vs.
scope-unaware Phase 2 comparison. The hunk-count filter ensures every instance offers between 4 and
8 atomic edit decisions, and the upstream Verified license (MIT) plus stable instance IDs let us
publish results that interoperate with the public SWE-bench leaderboard.
