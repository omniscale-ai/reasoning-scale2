# Literature Survey: Granularity Conditioning and Hierarchical Agents

## Motivation

The project's central hypothesis is that explicitly conditioning an LLM agent on its current
operating granularity (global / subtask / atomic) improves task success, calibration, and
request-vs-act discrimination. Before designing the Phase 2 baseline experiment we need literature
grounding on three threads: how prior work has framed and operationalised "granularity" or "scope"
labels for hierarchical agents, what hierarchical task decomposition schemas exist in the four
benchmark sources, and which uncertainty-calibration metrics have been used in agent settings (in
particular, definitions and prior measurements of the overconfident error rate). The survey output
anchors every later planning decision and lets us cite prior work in the Phase 4 paper-ready report.

## Scope

* Granularity / scope / scale conditioning in LLM agents and prompt engineering. Include any work
  that varies the level of abstraction at which an agent receives its instructions, even if the
  authors do not use the word "granularity".
* Hierarchical task decomposition: papers proposing two-, three-, or n-level decompositions for
  benchmarks similar to those in this project (FrontierScience-Olympiad, WorkArena++, SWE-bench
  Verified, tau-bench).
* Uncertainty calibration in LLM agents: confidence elicitation methods, definitions of
  overconfident error rate, calibration plots and metrics, and prior reports on how calibration
  changes with prompt design.
* The four roadmap benchmarks themselves: their official task structures, scoring conventions, and
  any published results that bracket what counts as competitive performance.

Out of scope: training-time techniques (RL, gradient-based fine-tuning), non-English benchmarks,
production deployment papers — all consistent with the project's Out of Scope section.

## Approach

1. Run the standard `/research-papers` and `/research-internet` stages with the three thread queries
   above. Use the `download-paper` skill for any candidate paper found via search.
2. Produce paper assets under `assets/paper/` for at least 10 highly relevant papers, each with a
   summary that conforms to the paper asset specification.
3. Aggregate findings into `research/research_papers.md` with a section per thread: granularity
   conditioning, hierarchical decomposition, calibration metrics, benchmark grounding.
4. Connect each thread back to the project's research questions and explicitly flag (a) any prior
   work that already answers a research question, (b) any methodological choices the survey resolves
   for Phase 2, and (c) any open questions to surface as suggestions.

## Expected Outputs

* At least 10 paper assets under `assets/paper/<paper_id>/` with `details.json`, summary, and PDF or
  markdown file.
* `research/research_papers.md` and `research/research_internet.md` synthesising the survey.
* `results/results_summary.md` with a thread-by-thread takeaway and explicit follow-up suggestions
  for the next brainstorm session (typically: which benchmarks to deprioritise, which conditioning
  prompts to adopt, which calibration metric to register as a project metric).
* `results/suggestions.json` with concrete follow-up ideas surfaced by the survey.

## Compute and Budget

No GPU. Anthropic API only (the project's `available_services` list dropped `openai_api` until an
API key is provided). Estimated cost: under 5 USD for paper summarisation through Claude.

## Dependencies and Cross-References

* No task dependencies. Independent of T2.
* Reads `project/description.md` for research questions and success criteria.
* The project's pre-existing `project/data/annotation_pilot/tasks_annotated.jsonl` should be
  inspected during the survey to ground discussion of benchmark coverage.

## Key Questions

1. What prior work explicitly compares scope-aware vs. scope-unaware vs. scope-mismatched LLM agents
   on multi-step benchmarks, and what effect sizes did they report?
2. What definitions of "overconfident error rate" exist in the agent calibration literature, and
   which is most appropriate for our Metric 2 specification?
3. What hierarchical decomposition schemas are already published for FrontierScience-Olympiad,
   WorkArena++, SWE-bench Verified, and tau-bench, and how do they map to our global / subtask /
   atomic split?
4. Are the WorkArena++ and tau-bench benchmarks truly inaccessible (as the existing pilot data
   suggests), or are there standard distribution channels we missed?
