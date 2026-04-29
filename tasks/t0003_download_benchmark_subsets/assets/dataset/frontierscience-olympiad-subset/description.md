---
spec_version: "2"
dataset_id: "frontierscience-olympiad-subset"
summarized_by_task: "t0003_download_benchmark_subsets"
date_summarized: "2026-04-29"
---
# FrontierScience-Olympiad Subset (pilot v0)

## Metadata

* **Name**: FrontierScience-Olympiad subset (pilot v0)
* **Year**: 2026
* **Authors**: This project (subset packaging); original problems sourced from Olympiad-style
  FrontierScience problem repositories
* **License**: research-only
* **Access**: public (within this project's repository)
* **Size**: 40 problems across 3 domains (biology=15, chemistry=10, physics=15)

## Overview

This dataset packages the FrontierScience-Olympiad pilot rows as a reproducible v0 subset for the
project's three-level granularity-conditioning experiments. The pilot rows were annotated under task
t0001 (annotation pilot) using Olympiad-style problems from physics, chemistry, and biology. The
closest publicly named benchmark analogue is FrontierMath (Glazer et al. 2024, arXiv:2411.04872),
which is gated behind Epoch AI access; this access barrier was identified by the t0002 literature
survey and remains unresolved at the time of this task. Until full FrontierMath access is
negotiated, the pilot rows serve as the canonical FrontierScience-Olympiad subset for Phase 2 work.
Each row contains the full problem text, the gold solution, the problem domain, and the annotator's
pre-existing token-usage metadata. Domain coverage is intentionally balanced across physics,
chemistry, and biology to match the project's stated scope.

## Content & Annotation

Every row follows the pilot annotation schema with these fields: `task_id`, `benchmark` (always
`FrontierScience-Olympiad`), `domain` (one of physics, chemistry, biology), `problem` (full problem
statement), `solution` (gold reference solution, where annotated), `difficulty`, `metadata.subject`,
`metadata.source_id`, `annotation_model`, `annotated_at`, `errors`, `steps`, and `token_usage`. The
`steps` field is `null` for FrontierScience-Olympiad rows because Olympiad solutions are graded as
final answers rather than as multi-step graphs; the project will derive step graphs in the t-future
hierarchical-annotation tasks. Annotation was performed by the project's pilot LLM-assisted
pipeline; gold solutions come from the source problem set.

## Statistics

| Metric | Value |
| --- | --- |
| Total problems | 40 |
| Average problem length (chars) | 1514 |

### Per-domain breakdown

| Domain | Problems |
| --- | --- |
| biology | 15 |
| chemistry | 10 |
| physics | 15 |

### Subset rule

All FrontierScience-Olympiad rows from the pilot file are included. Per-instance step counts are not
available for FrontierScience-Olympiad, so the canonical 4-8 decisions per task filter cannot be
applied at row level; instead, the subset is domain-stratified across physics / chemistry / biology
to match the pilot focus. Future tasks that derive step graphs (hierarchical-annotation) can
re-subset using node counts.

## Usage Notes

Load with the Python standard library:

```python
import json
with open('files/frontierscience-olympiad-subset.jsonl') as fh:
    rows = [json.loads(line) for line in fh if line.strip()]
```

Each row is a dict with the schema described in the Content & Annotation section. The `solution`
field is plain text. The `metadata.source_id` field uniquely identifies the upstream Olympiad
problem and should be preserved for traceability.

## Main Ideas

* This v0 subset is the canonical reproducible FrontierScience-Olympiad source for the project until
  upstream Epoch AI / FrontierMath access is resolved.
* Domain coverage is balanced across physics, chemistry, and biology, matching the project's
  three-domain scope.
* Step graphs are not available at row level for FrontierScience-Olympiad — Phase 2 experiments must
  either treat each row as single-decision or derive step graphs in a follow-up
  hierarchical-annotation task before computing per-step metrics.
* This subset is fully self-contained and does not require any external network access to load or
  use.

## Summary

The FrontierScience-Olympiad subset (pilot v0) packages 40 Olympiad-style problems spanning physics,
chemistry, and biology, sourced from the project's pilot annotation run. Every row contains the full
problem text, gold solution, and annotation metadata. The subset is the canonical
FrontierScience-Olympiad source for the project's Phase 2 scope-aware vs. scope-unaware baseline
experiment.

FrontierMath itself (the closest publicly named analogue) remains gated behind Epoch AI access. The
v0 subset is therefore a pragmatic substitute that preserves Phase 2 reproducibility; a follow-up
suggestion will track the open access negotiation. The domain-stratified design ensures every
experiment can report per-domain metrics without needing to re-balance.
