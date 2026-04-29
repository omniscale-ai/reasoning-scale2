# Hierarchical Annotation

## Planning Guidelines

* State which source benchmark(s) the task will draw from (FrontierScience-Olympiad, WorkArena++,
  SWE-bench Verified, or τ-bench) and how many tasks will be annotated.
* Cite or extend the existing annotation schema; never silently invent new granularity levels —
  global / subtask / atomic must be preserved.
* Budget LLM-assisted suggestion calls explicitly. Cap LLM spend per annotated task and record the
  cap in the plan's Cost Estimation section.
* Plan for at least one human review pass per annotated task, even when an LLM proposed the
  hierarchy.
* Define the gold-action exit criteria up front: what does it mean for an action label at each level
  to be "complete"? Tasks without explicit criteria produce non-comparable annotations.

## Implementation Guidelines

* Produce a dataset asset under `assets/dataset/<slug>/` whose rows include `task_id`, source
  benchmark, three-level hierarchy, and gold-action labels at each level.
* Reuse `project/code/scripts/collect_and_annotate.py` and `project/code/src/` modules where
  possible; treat them as imported legacy code, never modify them in place — wrap them.
* Log every LLM call through `arf/scripts/utils/run_with_logs.py`; record per-task LLM cost in
  `results/costs.json`.
* Report progress via the `annotation_count` metric only when that metric is registered for the
  project; otherwise report it in `results_detailed.md` and skip `metrics.json`.
* Produce inter-rater agreement when more than one annotator (human or LLM-as-judge) participates in
  the same items.

## Common Pitfalls

* Conflating subtask and atomic levels when the benchmark already provides a flat action trace —
  force a deliberate decision on where the boundary sits.
* Allowing the LLM-suggested hierarchy through without spot-checking — the suggestion model can
  silently drop required preconditions.
* Failing to record which LLM and prompt template produced each suggestion, which makes later
  ablations impossible.

## Related Skills

* `/research-papers` — survey hierarchical-annotation methods before locking the schema.
* `/planning` — produces `plan/plan.md` with explicit cost caps and exit criteria.
* `/implementation` — runs the annotation pipeline with logging.
