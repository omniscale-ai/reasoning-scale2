---
spec_version: "2"
dataset_id: "workarena-plus-plus-subset"
summarized_by_task: "t0003_download_benchmark_subsets"
date_summarized: "2026-04-29"
---
# WorkArena++ Compositional Task Manifest

## Metadata

* **Name**: WorkArena++ compositional task manifest
* **Year**: 2024
* **Authors**: Léo Boisvert et al. (ServiceNow Research)
* **License**: parent WorkArena Apache-2.0 license
* **Access**: restricted (full instantiation requires a live ServiceNow developer instance and a
  gated HuggingFace dataset)
* **Size**: 42 compositional task class lists exported from the upstream `curriculum.py` manifest

## Overview

WorkArena++ (Boisvert et al. 2024, arXiv:2407.05291) is a benchmark of compositional knowledge-work
tasks built from 33 atomic ServiceNow operations. Running a single task end-to-end requires (a) a
live ServiceNow developer instance, (b) gated access to the `ServiceNow/WorkArena-Instances`
HuggingFace dataset, and (c) the `browsergym-workarena` Python harness with Playwright. None of
these are available within this task's local-only download budget, so this dataset asset packages
the **compositional task class manifest** extracted from the upstream
`tasks/compositional/utils/curriculum.py` source file. The manifest gives Phase 2 the canonical task
taxonomy without needing to instantiate any task — every name listed is a class group representing a
distinct WorkArena++ compositional task family. The existing pilot Mind2Web proxy remains the
de-facto Phase 2 fallback for end-to-end execution until upstream access is resolved.

## Content & Annotation

The `files/workarena-plus-plus-task-manifest.json` file lists every task class group imported by the
upstream `curriculum.py`. Each entry is a string identifier (e.g., `DASH_AND_ORDER`,
`NAVIGATE_AND_CREATE_TASKS`) that maps to a Python class list in the
`browsergym.workarena.tasks.compositional` package. Task instances are not enumerated (that requires
the live ServiceNow instance and the gated HF dataset). The files `files/upstream/curriculum.py`,
`files/upstream/compositional__init__.py`, and `files/upstream/README.md` preserve the upstream
source verbatim so downstream tasks can re-extract richer metadata (per-class skill annotations,
level breakdowns) without re-fetching from GitHub.

## Statistics

| Metric | Value |
| --- | --- |
| Compositional task class lists | 42 |
| Atomic operations (per upstream paper) | 33 |
| Compositional tasks (per upstream paper, both L2 and L3 levels) | ~682 |
| Source file | `tasks/compositional/utils/curriculum.py` |
| Download method | urllib.request.urlretrieve from https://raw.githubusercontent.com/ServiceNow/WorkArena/main/src/browsergym/workarena/tasks/compositional/utils/curriculum.py |

### Task class list manifest

* `DASH_AND_ORDER`
* `DASH_COMPUTE_MEAN_AND_ORDER`
* `DASH_COMPUTE_MEDIAN_AND_ORDER`
* `DASH_COMPUTE_MODE_AND_ORDER`
* `DASH_AND_CREATE_INCIDENT`
* `DASH_COMPUTE_AND_CREATE_INCIDENT`
* `DASH_AND_CREATE_PROBLEM`
* `DASH_COMPUTE_AND_CREATE_PROBLEM`
* `DASH_COMPUTE_MIN_FILTER_LIST`
* `DASH_COMPUTE_MAX_FILTER_LIST`
* `DASH_COMPUTE_MEAN_FILTER_LIST`
* `DASH_COMPUTE_MEDIAN_FILTER_LIST`
* `DASH_COMPUTE_MODE_FILTER_LIST`
* `DASH_AND_REQUEST`
* `DASH_COMPUTE_MEAN_AND_REQUEST`
* `DASH_COMPUTE_MEDIAN_AND_REQUEST`
* `DASH_COMPUTE_MODE_AND_REQUEST`
* `EXPENSE_MANAGEMENT_TASKS`
* `FIND_AND_ORDER_ITEM_TASKS`
* `SMALL_BASE_SCHEDULING_TASKS`
* `LARGE_BASE_SCHEDULING_TASKS`
* `SMALL_TIGHT_SCHEDULING_TASKS`
* `LARGE_TIGHT_SCHEDULING_TASKS`
* `MARK_DUPLICATE_PROBLEMS_TASKS`
* `MAXIMIZE_INVESTMENT_RETURN_TASKS`
* `NAVIGATE_AND_CREATE_TASKS`
* `NAVIGATE_AND_FILTER_TASKS`
* `NAVIGATE_AND_ORDER_TASKS`
* `NAVIGATE_AND_SORT_TASKS`
* `INFEASIBLE_NAVIGATE_AND_CREATE_WITH_REASON`
* `INFEASIBLE_NAVIGATE_AND_CREATE`
* `INFEASIBLE_NAVIGATE_AND_ORDER_WITH_REASON`
* `INFEASIBLE_NAVIGATE_AND_ORDER`
* `INFEASIBLE_NAVIGATE_AND_FILTER_WITH_REASON`
* `INFEASIBLE_NAVIGATE_AND_FILTER`
* `INFEASIBLE_NAVIGATE_AND_SORT_WITH_REASON`
* `INFEASIBLE_NAVIGATE_AND_SORT`
* `OFFBOARD_USER_TASKS`
* `ONBOARD_USER_TASKS`
* `WARRANTY_CHECK_TASKS`
* `WORK_ASSIGNMENT_TASKS`
* `WORKLOAD_BALANCING_TASKS`

### Subset rule

All compositional task class lists from the upstream curriculum are kept. The canonical 4-8
decisions per task filter cannot be applied at this layer because instantiated task instances (with
concrete action sequences) are not available without ServiceNow + HF access. Phase 2 must apply the
filter at instance time once full upstream access is resolved.

## Usage Notes

Load with the Python standard library:

```python
import json
with open('files/workarena-plus-plus-subset-task-manifest.json') as fh:
    task_class_lists = json.load(fh)
```

To actually run any of these tasks end-to-end, install `browsergym-workarena`, follow the upstream
README to (a) request access to `ServiceNow/WorkArena-Instances` on HuggingFace and (b) provision a
ServiceNow developer instance, then dispatch tasks via the BrowserGym `make()` API. None of those
operations are required to use this manifest as a taxonomy reference.

## Main Ideas

* WorkArena++ end-to-end execution is gated on ServiceNow + HF access; this asset documents the
  access barrier and packages the upstream taxonomy without crossing it.
* The pilot Mind2Web proxy remains the operative Phase 2 fallback for knowledge-worker compositional
  tasks until upstream access is resolved.
* The 4-8 decisions per task filter must be deferred to instance time — the upstream curriculum
  manifest is at the task-class level, not the task-instance level.
* The upstream license is permissive (Apache-2.0) but the live ServiceNow developer instance is the
  binding access cost in practical terms.

## Summary

This dataset asset packages the WorkArena++ compositional task class manifest (42 task class lists)
extracted from the upstream `tasks/compositional/utils/curriculum.py` source. End-to-end task
instantiation requires a live ServiceNow developer instance plus access to the
`ServiceNow/WorkArena-Instances` gated HuggingFace dataset; this access is treated as out of scope
for this download task and is documented as a project follow-up.

For this project, the asset gives Phase 2 the canonical WorkArena++ task taxonomy and preserves the
upstream source files for traceability. The pilot Mind2Web proxy remains the actual end-to-end test
bed for compositional knowledge-worker tasks until the access barriers are resolved.
