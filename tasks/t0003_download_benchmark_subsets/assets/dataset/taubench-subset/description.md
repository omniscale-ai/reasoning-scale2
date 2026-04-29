---
spec_version: "2"
dataset_id: "taubench-subset"
summarized_by_task: "t0003_download_benchmark_subsets"
date_summarized: "2026-04-29"
---
# tau-bench Subset (4-8 actions)

## Metadata

* **Name**: tau-bench subset (4-8 actions)
* **Year**: 2024
* **Authors**: Shunyu Yao et al. (Sierra Research)
* **License**: MIT (parent tau-bench repository license)
* **Access**: public (GitHub `sierra-research/tau-bench`)
* **Size**: 87 tasks (filtered from 665 total)

## Overview

tau-bench (Yao et al. 2024, arXiv:2406.12045) is a tool-agent-user interaction benchmark spanning
two domains: airline customer service and retail returns/exchanges. Each task gives the agent a user
intent and a domain API; the agent must produce a sequence of API calls (`Action` objects) that
satisfies the user. The original benchmark ships task definitions as Python source files in the
upstream repository — this dataset asset extracts those task definitions without installing the
harness or calling any LLM, so the subset is a pure metadata export. Each subset row records the
domain, split (test or train), instruction text, gold action sequence (names only), and action
count. We filter to tasks whose gold sequence has 4 to 8 actions (the project's canonical multi-step
decision range).

## Content & Annotation

Each row has these fields: `domain` (`airline` or `retail`), `split` (`test` or `train`),
`task_index` (position in the upstream `TASKS` list), `annotator` (the upstream annotator id, where
present), `user_id` (the synthetic user id), `instruction` (the user's natural-language request),
`actions` (list of API call names in the gold sequence), `action_count` (length of `actions`), and
`outputs` (list of expected agent outputs, where annotated). The gold action sequence is what the
upstream project uses to grade an agent's pass/fail at the task level.

## Statistics

| Metric | Value |
| --- | --- |
| Total tasks across upstream Python files | 665 |
| Subset (4-8 actions) | 87 |

### Per-domain-split breakdown of subset

| Domain / split | Tasks |
| --- | --- |
| airline/test | 13 |
| retail/test | 50 |
| retail/train | 24 |

### Action-count distribution within subset

| Actions | Tasks |
| --- | --- |
| 4 | 24 |
| 5 | 24 |
| 6 | 23 |
| 7 | 13 |
| 8 | 3 |

### Subset rule

Tasks are kept iff the gold `actions` list has between 4 and 8 entries (inclusive). Action counts
are extracted from the upstream Python source files via the `ast` module — no installation required.

## Usage Notes

Load with the Python standard library:

```python
import json
with open('files/taubench-subset.jsonl') as fh:
    rows = [json.loads(line) for line in fh if line.strip()]
```

The full upstream Python source for each (domain, split) pair is preserved verbatim in
`files/upstream/<domain>__tasks_<split>.py` so downstream tasks can re-extract richer fields (action
kwargs, output shapes) without re-fetching from GitHub. Note that running tau-bench end-to-end
(instantiating the env and querying an LLM) still requires installing the harness and providing API
keys — this asset only captures the task metadata needed for the project's scope-aware vs
scope-unaware comparison.

## Main Ideas

* The action sequence length is the natural per-task decision count for tau-bench: each
  `Action(...)` call is one tool invocation the agent must produce.
* By extracting metadata from upstream source rather than installing the harness, this asset is
  fully reproducible, requires no API keys, and stays under 1 MB.
* The subset combines all available splits (test + train where present) so Phase 2 can use train
  tasks for prompt tuning and test tasks for unbiased evaluation if needed.
* Action kwargs (e.g., flight numbers, user IDs) are intentionally omitted from the subset rows to
  keep them small; the full upstream Python is preserved separately for agents that need the kwargs.

## Summary

This tau-bench subset contains 87 tasks from the upstream Sierra Research tau-bench repository,
filtered to the 4-8 actions per task range. Tasks span the airline customer-service and retail
return/exchange domains. Metadata is extracted from upstream Python source files using the `ast`
module, so this asset works fully offline once the source files are downloaded.

For this project, the subset is the primary tool-use multi-step test bed for the scope-aware vs.
scope-unaware Phase 2 comparison. The upstream MIT license and stable task indices preserve
interoperability with the public tau-bench leaderboard.
