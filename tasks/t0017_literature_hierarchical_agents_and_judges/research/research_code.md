---
spec_version: "1"
task_id: "t0017_literature_hierarchical_agents_and_judges"
research_stage: "code"
tasks_reviewed: 3
tasks_cited: 3
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-05-01"
status: "complete"
---
## Task Objective

Identify any prior code, libraries, datasets, or other assets in this project that could inform the
current literature-survey task. The survey covers hierarchical / granularity-aware LLM agents,
LLM-as-judge methodology, and the foundational options framework. Its outputs are paper assets and
synthesis documents — there is no implementation beyond running the `/add-paper` skill.

## Library Landscape

The library aggregator
(`uv run python -u -m arf.scripts.aggregators.aggregate_libraries --format json`) reports
`library_count: 0`. No project-internal libraries have been registered yet under `assets/library/`,
so there is nothing to import or extend. Adjacent project utilities used during the task are
framework code, not registered libraries:

* `arf.scripts.utils.doi_to_slug` — canonical DOI-to-folder-name conversion. Confirms that
  parenthesised DOIs are rejected and require the `no-doi_` fallback (relevant for `Sutton1999`).
* `meta.asset_types.paper.verificator` — the canonical paper-asset verifier invoked in Phase 6 of
  `/add-paper`. Used once per paper.
* `arf.scripts.aggregators.aggregate_papers` — used to confirm pre-existing-corpus non-overlap with
  the ten target papers.

## Key Findings

* **No reusable project library was found.** This task is pure metadata + summary work; it produces
  ten paper assets and a synthesis document, no library, model, or dataset.
* **One top-level dependency was added.** `pypdf` was added as a dev dependency to `pyproject.toml`
  (and `uv.lock` was regenerated) so the per-paper agent could extract full PDF text for the Sutton
  1999 summary. Per CLAUDE.md rule 3 this is a permitted top-level change. The dependency now stays
  installed and benefits any future literature-survey or full-text-extraction task.
* **Three prior tasks are conceptually adjacent.** t0009 (hierarchical annotation v2), t0014 (v2
  annotator sonnet rerun), and t0012 (phase-2 ABC smoke) are the tasks whose findings this survey
  most directly strengthens or informs (see the "Pointers Back to Backlog" section in
  `results/results_summary.md`). None of them produced reusable code for the literature-survey
  workflow itself.

## Reusable Code and Assets

* `arf.scripts.utils.doi_to_slug` — invoked once per DOI; no modifications needed.
* `meta.asset_types.paper.verificator` — invoked once per paper; no modifications needed.
* `arf/skills/add-paper/SKILL.md` — the canonical workflow used ten times in parallel; no
  modifications needed.
* `pypdf` (added as a dev dependency) — installed once at the top level; available to any future
  task that needs PDF text extraction.

No task-specific Python code (under `tasks/<task_id>/code/`) was written for this task.

## Lessons Learned

* The `/add-paper` skill scales cleanly to ten parallel runs; each per-paper agent is independent
  and there are no cross-paper write conflicts.
* For papers older than the modern arXiv era, the per-paper agent benefits from full-PDF text
  extraction (via `pypdf`) over abstract-only summarisation. The Sutton 1999 summary is materially
  better for it.
* Initial category assignments are easy to get wrong on prompting / reasoning-structure papers
  (`Zhou2024b`'s SELF-DISCOVER initially used invented slugs). Always pass the per-paper agent the
  output of `aggregate_categories --format json` and require category slugs to come from
  `meta/categories/`.

## Recommendations for This Task

1. Do not create a `tasks/t0017_.../code/` directory; this is a literature-survey task with no
   implementation.
2. Run `verify_paper_asset` once per paper, then re-run `aggregate_papers` and
   `aggregate_categories` after all ten papers are added to confirm shared-corpus integrity.
3. Future literature-survey tasks should reuse the now-installed `pypdf` dependency rather than
   reinstall it.
4. Future summarisation tasks that need to extract text from older paywalled papers should follow
   the `Sutton1999` pattern: use a public mirror for download, preserve the original DOI in
   `details.json`, and use the `no-doi_` fallback only when the DOI itself is invalid for slug
   conversion.

## Task Index

* [`t0009_hierarchical_annotation_v2`] — strengthened by P1 (`Gao2026`), P2 (`Zhou2024` ArCHer), P3
  (`Wen2024`), and P10 (`Sutton1999`); reinforced by P7 (`Li2024`) and P8 (`Ma2024`).
* [`t0014_v2_annotator_sonnet_rerun`] — strengthened by `Gao2026` Proposition 1 (bias-variance
  argument for mid-granularity preference signals).
* [`t0012_phase2_abc_smoke_frontierscience`] — informed by P10 (options framework as ABC frame), P7
  (error taxonomy), and P8 (progress-rate metric).
