# ⏹ Tasks: Not Started

2 tasks. ⏹ **2 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0003 — <strong>Download benchmark subsets for the four roadmap
sources</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0003_download_benchmark_subsets` |
| **Status** | not_started |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 4 dataset |
| **Source suggestion** | — |
| **Task types** | [`download-dataset`](../../../meta/task_types/download-dataset/) |
| **Task page** | [Download benchmark subsets for the four roadmap sources](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Task folder** | [`t0003_download_benchmark_subsets/`](../../../tasks/t0003_download_benchmark_subsets/) |

# Download Benchmark Subsets

## Motivation

Phase 1 (annotation) and Phase 2 (baseline scope-aware vs. scope-unaware experiment) both
depend on having local, reproducible subsets of the four roadmap benchmarks. The existing
pilot annotation data uses HumanEval and Mind2Web proxies for tau-bench and WorkArena++
because the real benchmarks were "unavailable on HF" at original-annotation time. This task
either resolves that gap by acquiring the real benchmarks or, if access is genuinely
unavailable, documents the decision to keep proxies and freezes the choice for Phase 2.

## Scope

Acquire four benchmark subsets, each targeted at multi-step tasks of 4-8 decisions per task to
match the project's stated difficulty range:

* FrontierScience-Olympiad — full official distribution path; subset by domain to match the
  pilot's physics / chemistry / biology focus.
* WorkArena++ — official distribution. If genuinely inaccessible (gated, retired, dataset
  moved), document the access attempt and keep the Mind2Web proxy already present in the
  pilot.
* SWE-bench Verified — official Princeton/HF distribution; subset to instances that map
  cleanly onto the project's three-level hierarchy.
* tau-bench — official distribution. If genuinely inaccessible, keep the HumanEval proxy with
  documented justification.

Out of scope: full benchmark execution harnesses (those belong in later experiment-run tasks),
custom annotation (that belongs in T3 hierarchical-annotation pilot), and modifications of
benchmark data (subsetting only, no relabelling).

## Approach

1. For each benchmark, attempt the official distribution path documented in its source paper
   or GitHub README. Cache successful downloads under the task's
   `assets/dataset/<slug>/files/`.
2. Subset to 4-8 decisions per task using whatever per-instance step or step-count metadata
   the benchmark provides. If no such metadata exists, sample uniformly and document the
   sampling seed.
3. Produce one dataset asset per benchmark with `details.json` describing source URL, version,
   license, sample count, and subset selection criteria.
4. If a benchmark is inaccessible, write the access attempt log to the dataset asset's
   `details.json` with `download_status: "failed"` and a clear `download_failure_reason`. The
   project's policy in this case is to keep the existing pilot proxy and not block on access.
5. Emit follow-up suggestions for any benchmark whose access pathway is non-obvious or whose
   subsetting choice deserves a Phase 2 sensitivity check.

## Expected Outputs

* Four dataset assets under
  `assets/dataset/{frontierscience,workarena_plus_plus,swebench_verified, taubench}/` with
  `details.json` and `files/` directories (or empty `files/` plus a clear failed status if
  inaccessible).
* `results/results_summary.md` with a per-benchmark access status, sample count, and any
  subset decisions.
* `results/suggestions.json` flagging any benchmarks where the proxy choice is now permanent.

## Compute and Budget

No GPU. No paid API calls anticipated. All work is local downloads and metadata writing.
Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. Independent of T1.
* Cross-references: existing pilot annotation data at
  `project/data/annotation_pilot/tasks_annotated.jsonl` documents the proxy decisions this
  task must either resolve or formalise.

</details>

<details>
<summary>⏹ 0002 — <strong>Literature survey: granularity conditioning and
hierarchical agents</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_granularity_conditioning` |
| **Status** | not_started |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 10 paper |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Task page** | [Literature survey: granularity conditioning and hierarchical agents](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Task folder** | [`t0002_literature_survey_granularity_conditioning/`](../../../tasks/t0002_literature_survey_granularity_conditioning/) |

# Literature Survey: Granularity Conditioning and Hierarchical Agents

## Motivation

The project's central hypothesis is that explicitly conditioning an LLM agent on its current
operating granularity (global / subtask / atomic) improves task success, calibration, and
request-vs-act discrimination. Before designing the Phase 2 baseline experiment we need
literature grounding on three threads: how prior work has framed and operationalised
"granularity" or "scope" labels for hierarchical agents, what hierarchical task decomposition
schemas exist in the four benchmark sources, and which uncertainty-calibration metrics have
been used in agent settings (in particular, definitions and prior measurements of the
overconfident error rate). The survey output anchors every later planning decision and lets us
cite prior work in the Phase 4 paper-ready report.

## Scope

* Granularity / scope / scale conditioning in LLM agents and prompt engineering. Include any
  work that varies the level of abstraction at which an agent receives its instructions, even
  if the authors do not use the word "granularity".
* Hierarchical task decomposition: papers proposing two-, three-, or n-level decompositions
  for benchmarks similar to those in this project (FrontierScience-Olympiad, WorkArena++,
  SWE-bench Verified, tau-bench).
* Uncertainty calibration in LLM agents: confidence elicitation methods, definitions of
  overconfident error rate, calibration plots and metrics, and prior reports on how
  calibration changes with prompt design.
* The four roadmap benchmarks themselves: their official task structures, scoring conventions,
  and any published results that bracket what counts as competitive performance.

Out of scope: training-time techniques (RL, gradient-based fine-tuning), non-English
benchmarks, production deployment papers — all consistent with the project's Out of Scope
section.

## Approach

1. Run the standard `/research-papers` and `/research-internet` stages with the three thread
   queries above. Use the `download-paper` skill for any candidate paper found via search.
2. Produce paper assets under `assets/paper/` for at least 10 highly relevant papers, each
   with a summary that conforms to the paper asset specification.
3. Aggregate findings into `research/research_papers.md` with a section per thread:
   granularity conditioning, hierarchical decomposition, calibration metrics, benchmark
   grounding.
4. Connect each thread back to the project's research questions and explicitly flag (a) any
   prior work that already answers a research question, (b) any methodological choices the
   survey resolves for Phase 2, and (c) any open questions to surface as suggestions.

## Expected Outputs

* At least 10 paper assets under `assets/paper/<paper_id>/` with `details.json`, summary, and
  PDF or markdown file.
* `research/research_papers.md` and `research/research_internet.md` synthesising the survey.
* `results/results_summary.md` with a thread-by-thread takeaway and explicit follow-up
  suggestions for the next brainstorm session (typically: which benchmarks to deprioritise,
  which conditioning prompts to adopt, which calibration metric to register as a project
  metric).
* `results/suggestions.json` with concrete follow-up ideas surfaced by the survey.

## Compute and Budget

No GPU. Anthropic API only (the project's `available_services` list dropped `openai_api` until
an API key is provided). Estimated cost: under 5 USD for paper summarisation through Claude.

## Dependencies and Cross-References

* No task dependencies. Independent of T2.
* Reads `project/description.md` for research questions and success criteria.
* The project's pre-existing `project/data/annotation_pilot/tasks_annotated.jsonl` should be
  inspected during the survey to ground discussion of benchmark coverage.

## Key Questions

1. What prior work explicitly compares scope-aware vs. scope-unaware vs. scope-mismatched LLM
   agents on multi-step benchmarks, and what effect sizes did they report?
2. What definitions of "overconfident error rate" exist in the agent calibration literature,
   and which is most appropriate for our Metric 2 specification?
3. What hierarchical decomposition schemas are already published for FrontierScience-Olympiad,
   WorkArena++, SWE-bench Verified, and tau-bench, and how do they map to our global / subtask
   / atomic split?
4. Are the WorkArena++ and tau-bench benchmarks truly inaccessible (as the existing pilot data
   suggests), or are there standard distribution channels we missed?

</details>
