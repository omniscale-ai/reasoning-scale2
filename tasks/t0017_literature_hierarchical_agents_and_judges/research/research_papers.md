---
spec_version: "1"
task_id: "t0017_literature_hierarchical_agents_and_judges"
research_stage: "papers"
papers_reviewed: 0
papers_cited: 0
categories_consulted:
  - "hierarchical-planning"
  - "granularity-conditioning"
  - "agent-evaluation"
  - "uncertainty-calibration"
  - "benchmark-annotation"
date_completed: "2026-05-01"
status: "partial"
---
## Task Objective

Identify the seed of relevant prior work already in this project before adding the ten target papers
(P1-P10) on hierarchical / granularity-aware LLM agents and LLM-as-judge methodology, so that the
new survey extends rather than duplicates existing assets. The task scope, defined in
`task_description.md`, covers five themes: hierarchical / granularity-aware agents (P1, P2, P3,
P10), search-and-planning structure (P4, P5), reasoning-structure discovery (P6), agent benchmarks
(P7, P8), and LLM-as-judge methodology (P9).

## Category Selection Rationale

Five project categories from `meta/categories/` map to the survey's five themes. The core
methodological themes are `hierarchical-planning` (P1-P3, P10 plus the search papers P4, P5),
`granularity-conditioning` (P1, P3, P10 — granularity of preference signals and credit assignment),
and `uncertainty-calibration` (P9 — calibrated thresholds for selective judging). The benchmark
themes are `agent-evaluation` (P7, P8 — fine-grained taxonomy and progress-rate metric) and
`benchmark-annotation` (P8 — large-scale subgoal annotation methodology). Categories
`benchmark-frontierscience`, `benchmark-workarena`, `benchmark-swebench`, and `benchmark-taubench`
were not consulted because the four roadmap benchmarks are out of scope for this survey.

## Key Findings

### Existing Project Corpus Has No Overlap With the Ten Target Papers

`aggregate_papers --format json --detail short` was run before any `/add-paper` invocation. None of
the ten target papers (P1-P10) was present in the project. The pre-existing paper corpus is
concentrated on benchmark-design and annotation-methodology references seeded by t0002, t0007, and
t0009; it does not include the hierarchical-RL, search, reasoning-structure, embodied-agent, or
LLM-as-judge references this task targets. No deduplication corrections were needed and no prior
paper had to be cited to inform the new additions.

### Identity Resolution Used the Canonical Slug Utility With Two Documented Fallbacks

For each of the ten papers, the resolved DOI (or arXiv-derived DOI) was compared against every
existing `paper_id` and `title` (lower-cased, stripped of punctuation). All ten resolved IDs were
new. Eight papers received a canonical DOI-based slug from `arf.scripts.utils.doi_to_slug`. Two used
the `no-doi_<Author><Year>_<slug>` fallback per the v3 paper specification: `Sutton1999` because its
DOI `10.1016/S0004-3702(99)00052-1` contains parentheses that the slug utility rejects, and
`Gao2026` (HPL, ICLR 2026) because the paper has no registered DOI yet. The canonical DOI is
preserved in `details.json` for `Sutton1999`; for `Gao2026` the DOI field is `null` and the
OpenReview URL is preserved in the `url` field.

### Synthesis Across the Existing Corpus Was Not Possible

Because no prior paper in the project's existing corpus falls within the five themes of this survey,
this stage cannot perform cross-paper synthesis from the existing corpus. The synthesis sections
that would normally appear here — scope-by-scope contrasts, cross-paper coverage analysis, and
citation-graph notes — are deferred to the analysis step that consumes the ten new paper assets
directly. The `status: partial` frontmatter flag reflects this honest gap.

## Methodology Insights

* The aggregator-first deduplication step is critical and inexpensive. Running `aggregate_papers`
  before `/add-paper` adds about 2 seconds and prevents the entire ten-paper-adds-already-present
  failure mode that wastes much more time downstream.
* The two non-DOI cases (`Sutton1999`, `Gao2026`) confirm that the `no-doi_<Author><Year>_<slug>`
  fallback is the correct default for both pre-DOI-era refereed papers and newest-conference papers
  that have not yet been assigned a DOI.
* `pypdf` was the only added dependency for this task, used by the per-paper agent that summarised
  Sutton 1999 from the full text rather than the abstract. Per CLAUDE.md rule 3, top-level Python
  tooling files are the only legitimate non-task changes.

## Gaps and Limitations

* This research-papers stage cannot synthesise across an existing corpus — the prior corpus does not
  overlap the survey scope. The synthesis sections that would normally appear here are deferred to
  the analysis step which works directly off the ten new paper assets.
* The survey is restricted to ten papers chosen at the start of the task; it is not exhaustive. A
  follow-up task could add 2024-2026 papers on inverse-RL judges, judge ensembles beyond `Jung2024`,
  and additional embodied-agent benchmarks beyond `Li2024` and `Ma2024`.

## Recommendations for This Task

1. Skip cross-paper synthesis at the research-papers stage; defer all synthesis to the analysis
   stage that consumes the ten new paper assets.
2. Use `/add-paper` in parallel for all ten papers; expected wall-clock with parallel execution is
   under 20 minutes.
3. For the two non-DOI papers, use `no-doi_<Author><Year>_<slug>` and preserve the raw DOI string in
   `details.json` `doi` (where available, e.g., `10.1016/S0004-3702(99)00052-1` for Sutton 1999).
4. After all ten paper additions, re-run `meta.asset_types.paper.verificator` per paper and the
   project-level aggregators (`aggregate_papers`, `aggregate_categories`) to confirm nothing in the
   shared corpus drifted.

## Paper Index

The corpus did not contain any of the ten target papers before this task. The Paper Index for the
ten new assets is the at-a-glance table in `results/results_detailed.md`. The full per-paper
metadata lives in `assets/paper/<paper_id>/details.json` and the canonical summaries in
`assets/paper/<paper_id>/summary.md`.
