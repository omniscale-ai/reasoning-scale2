---
spec_version: "1"
task_id: "t0002_literature_survey_granularity_conditioning"
research_stage: "code"
tasks_reviewed: 1
tasks_cited: 1
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-29"
status: "complete"
---
## Task Objective

Identify any prior code, libraries, datasets, or other assets in this project that could inform the
current literature-survey task. The current task surveys literature on granularity / scope
conditioning, hierarchical decomposition, calibration, and the four roadmap benchmarks; its outputs
are paper assets and a synthesis document, with no implementation beyond running the `/add-paper`
skill.

## Library Landscape

The library aggregator
(`uv run python -u -m arf.scripts.aggregators.aggregate_libraries --format json`) reports
`library_count: 0`. No libraries have been registered in `assets/library/` yet, so there is nothing
to import. None of the project's pre-existing scripts (mentioned in `project/description.md` as
`code/scripts/` and `code/src/`) are registered as ARF library assets, so they are off-limits for
cross-task import. They remain available as reference material outside the ARF task model but cannot
be imported from `tasks/t0002_*/code/`.

## Key Findings

### Only one prior task exists; it produced no reusable code

`aggregate_tasks.py` reports three tasks: t0001 (brainstorm, completed), the current t0002
(in_progress), and t0003 (`download_benchmark_subsets`, not_started). Only t0001 is completed and
available for inspection [t0001]. t0001 was a brainstorming session whose deliverable was the
suggestions JSON that scheduled this task and t0003. It produced no code, no libraries, no datasets,
and no paper assets. There is therefore no prior implementation work to leverage.

### The pre-existing `code/scripts/` and `data/annotation_pilot/` material is not ARF-managed

`project/description.md` records that the parent reasoning-scale project imported scripts (e.g.,
`run_experiment.py`, `run_diploma_experiments.py`) and a pilot annotation set. These live outside
the ARF task model and have not been registered as library or dataset assets. For the current
literature-survey task this material is irrelevant — the task does not run experiments — but it
constrains the planning step for future tasks: any future task that wants to run those scripts must
first register them as ARF assets via a write-library or download-dataset task, not by importing
them from the parent project tree.

### Implementation will be entirely orchestrator-driven via `/add-paper`

For this task, "implementation" means running the `/add-paper` skill once per discovered paper. The
skill itself lives under `arf/skills/add-paper/` and is therefore framework code, not task code. No
new Python files belong in `tasks/t0002_*/code/` for this task. The task's `code/` directory should
remain empty apart from the framework-mandated `__init__.py` and `.gitkeep`.

## Reusable Code and Assets

There is no reusable task-internal code to copy or import.

* **`/add-paper` skill** — `arf/skills/add-paper/` — framework skill, invoked via the orchestrator
  per discovered paper. Reuse method: invoke as a skill, not as importable code. Function
  signatures: documented in the skill's `SKILL.md`. Adaptation needed: pass the discovered paper's
  arXiv ID or DOI and the `--task-id t0002_literature_survey_granularity_conditioning` flag. Line
  count: not applicable (skill, not code).
* **`aggregate_papers.py`** — `arf/scripts/aggregators/aggregate_papers.py` — framework aggregator
  to verify each newly added paper landed in the corpus and to detect duplicates between
  `/add-paper` invocations. Reuse method: framework script invocation only.
* **`verify_paper_asset.py`** — `arf/scripts/verificators/verify_paper_asset.py` — framework
  verificator for each paper asset against the v3 spec. Reuse method: framework script invocation
  only.

No task-local `code/` files are needed for the literature survey.

## Lessons Learned

The brainstorming task t0001 is the only completed predecessor and offers two takeaways [t0001]:
first, the project's existing categories under `meta/categories/` (nine entries spanning the four
roadmap benchmarks plus three methodological themes plus two cross-cutting tags) were designed
precisely to support this survey, so paper-asset tagging should not introduce any new categories.
Second, t0001's suggestions JSON commits this task to a 10-paper minimum and a 5 USD budget cap;
both are non-negotiable for the implementation step.

## Recommendations for This Task

1. **Do not write any task-local code under `tasks/t0002_*/code/`.** The directory should remain
   empty (only framework-mandated `__init__.py` plus `.gitkeep`). All implementation work happens
   via skill invocations.
2. **Run `aggregate_papers.py` between `/add-paper` invocations** to detect duplicates and confirm
   each paper landed correctly.
3. **Run `verify_paper_asset.py` against each newly created paper asset** before moving to the next
   paper.
4. **Tag every paper asset with categories already in `meta/categories/`.** The nine existing slugs
   cover all four survey threads. Inventing new categories would require an `add-category` task and
   is out of scope.
5. **Defer all script reuse from `code/scripts/` to a future write-library task.** The current task
   should not touch the parent-project scripts at all.

## Task Index

### [t0001]

* **Task ID**: `t0001_brainstorm_results_1`
* **Name**: Brainstorm session 1: plan first project tasks
* **Status**: completed
* **Relevance**: Created the suggestion that scheduled this task; defined the 10-paper target, the 5
  USD budget cap, and the four-thread coverage. Also confirmed by negative result that no prior code
  or library assets exist for this task to leverage.
