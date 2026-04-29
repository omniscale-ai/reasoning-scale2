---
spec_version: "1"
task_id: "t0002_literature_survey_granularity_conditioning"
research_stage: "papers"
papers_reviewed: 0
papers_cited: 0
categories_consulted:
  - "granularity-conditioning"
  - "hierarchical-planning"
  - "uncertainty-calibration"
  - "benchmark-frontierscience"
  - "benchmark-workarena"
  - "benchmark-swebench"
  - "benchmark-taubench"
  - "agent-evaluation"
  - "benchmark-annotation"
date_completed: "2026-04-29"
status: "partial"
---
## Task Objective

This task is the project's first literature survey. The objective is to ground the central
hypothesis — that explicitly conditioning an LLM agent on its current operating granularity (global,
subtask, atomic) improves task success, calibration, and request-vs-act discrimination — in prior
work. The survey covers four threads: (a) granularity / scope conditioning of LLM agents, (b)
hierarchical task decomposition for multi-step benchmarks, (c) uncertainty calibration metrics
(definitions of overconfident error rate), and (d) the four roadmap benchmarks
(FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench). Findings here anchor every
later planning decision and let us cite prior work in the Phase 4 paper-ready report.

## Category Selection Rationale

Consulted nine project categories that map directly to the four survey threads. Three are core
methodological themes — `granularity-conditioning` (RQ1, RQ4, RQ5), `hierarchical-planning` (RQ3,
sub-hypothesis 1), and `uncertainty-calibration` (RQ2, Metric 2). Four are benchmark-specific —
`benchmark-frontierscience`, `benchmark-workarena`, `benchmark-swebench`, `benchmark-taubench` —
because the project draws its composite multi-step benchmark from these four sources. Two cut across
the survey: `agent-evaluation` for evaluation-protocol papers and `benchmark-annotation` for papers
that publish hierarchical task annotations comparable to our gold-action schema. No category was
excluded — the project's category set was tailored at setup to this exact survey scope.

## Key Findings

### Empty Existing Corpus — Survey Must Be Sourced from Internet Research

The aggregator `aggregate_papers.py` reports zero existing paper assets in the project. T0001
(brainstorm) produced no paper assets, and no prior task downloaded literature. As a result, this
research-papers stage cannot synthesize across an existing corpus. The actionable finding is
procedural: every relevant paper for this project must be discovered and downloaded during the
research-internet stage that follows. The synthesis sections that would normally appear here (scope
conditioning effect sizes, calibration definitions, hierarchical schemas, benchmark distribution
channels) are deferred to `research/research_internet.md`.

### Implied Coverage Targets From the Project Description

Although no papers exist yet, the project description and `task_description.md` make explicit
coverage demands on the survey: at least 10 paper assets, distributed across the four threads, with
the granularity-conditioning thread receiving priority because it is the central hypothesis. Each
downstream paper asset must include a full summary that conforms to the v3 paper asset
specification, and each must be tagged with at least one of the nine project categories so that
later aggregators can filter cleanly.

### Pre-Existing Project Assets Mentioned in the Description

`project/description.md` notes pre-existing scripts (`run_experiment.py`,
`run_diploma_experiments.py`, `run_synthesis.py`) and a pilot annotation set imported from a parent
project. These are not paper assets — they are code and data — so they do not appear in the paper
corpus, but they constrain the survey: the experiment harness already encodes a global / subtask /
atomic split, so the survey should prioritize papers whose granularity taxonomies align with that
three-level decomposition rather than alternative two-level or n-level schemas. This narrows the
candidate set in the hierarchical-planning thread.

## Methodology Insights

* **Run the research-internet stage with three parallel query threads** matching the four survey
  threads. Use Semantic Scholar / arXiv / ACL Anthology / OpenReview as primary sources, falling
  back to Google Scholar where needed. The search must produce a `## Discovered Papers` section
  enumerating at least 10 candidates whose abstracts and metadata are recoverable.
* **Prefer canonical sources over secondary citations**. For each of the four roadmap benchmarks,
  the canonical paper or technical report (FrontierMath, WorkArena++, SWE-bench Verified card,
  tau-bench) is the primary candidate. Survey papers that summarize hierarchical agent planning
  (e.g., ReAct, Reflexion, Plan-and-Solve) are secondary candidates; pick whichever explicitly
  ablates over instruction granularity.
* **Stretch goal of 12-15 papers** if the search uncovers more than 10 strong candidates. The task
  ceiling is 15 to keep summarization cost under 5 USD.
* **Use the `/add-paper` skill once per paper**, not a batch script. Each paper asset must include a
  PDF or markdown file under `files/` (or a `.gitkeep` plus `download_status: "failed"` and a
  failure reason if the file cannot be retrieved).
* **Tag each paper with project categories** drawn from the list of nine. Avoid inventing new
  categories — the registry is closed for this task.

## Gaps and Limitations

* No prior corpus exists, so cross-paper synthesis is not possible at this stage. The trade-off: the
  task moves the synthesis work into `research_internet.md` and `results_summary.md`.
* Several of the roadmap benchmarks (WorkArena++, tau-bench) may be partially closed or
  difficult-to-access — the task description explicitly flags this as a research question. The
  research-internet stage must record any access barriers for the planning step.
* Without a baseline corpus there is no way to spot duplication early; the implementation step must
  re-run `aggregate_papers.py` before each `/add-paper` call to avoid duplicates.
* Calibration literature for agent settings is younger than calibration literature for classifiers.
  The survey may find that overconfident-error-rate definitions vary by paper and require the
  project to commit to a specific operationalization in the Phase 2 plan.

## Recommendations for This Task

1. **Skip cross-paper synthesis here** and proceed directly to research-internet, where the
   discovery-and-download work happens. Mark this file `status: "partial"` with that explanation.
2. **Set the discovery target at 10-15 papers** distributed across the four threads with at least
   two papers per thread to allow later cross-paper comparison.
3. **For each discovered paper, run the `/add-paper` skill** in the implementation step rather than
   batching — each paper asset must independently pass the v3 spec verificator.
4. **Record any access barriers** (paywalled, withdrawn, only-on-OpenReview) in
   `research/research_internet.md` so the planning step can decide whether to deprioritize a
   benchmark.
5. **Defer all numeric synthesis** (effect sizes, calibration metrics, accuracy numbers) to
   `results/results_summary.md`, where the survey output is digested for downstream tasks.

## Paper Index

No papers cited. The corpus is empty; this section is intentionally vacant. Discovered papers are
listed in `research/research_internet.md` `## Discovered Papers` and materialized as paper assets
during the implementation step.
