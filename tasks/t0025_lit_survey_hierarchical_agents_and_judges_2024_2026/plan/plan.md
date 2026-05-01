# Plan: t0025 Literature Survey — Hierarchical Agents and LLM-as-Judge (2024-2026)

## Objective

Add 10 paper assets covering hierarchical / granularity-aware LLM agents, search and planning
structure, reasoning structure discovery, agent benchmarks, the foundational options framework, and
LLM-as-judge methodology. Produce a synthesis writeup that maps the survey findings to the project's
RQ1, RQ2, RQ4, and RQ5 so Brainstorm Session 8 can scope the next agent-iteration experiment within
the remaining budget.

## Approach

The 10 target papers are enumerated in `task_description.md`. Each paper goes through the canonical
`/add-paper` skill: identity resolution → metadata collection → PDF download → `details.json` →
canonical `summary.md` with all 9 mandatory sections → `verify_paper_asset`.

Per-paper invocations are independent and run as parallel sub-agents. Concurrency is capped at 3
sub-agents at a time so that category-creation (see below) and the `details.json` writes do not
collide. Failed downloads (paywalled, withdrawn, or unfindable) fall back to abstract-based
summaries with `download_status: "failed"` per the `add-paper` Phase 3 fallback. The hard kill
switch from `task_description.md` (halt if > 2 of 10 fail) is enforced after the second failure.

After all 10 paper assets are added and pass `verify_paper_asset`, the implementation step writes
two synthesis documents:

* `results/results_summary.md` — per-paper one-paragraph takeaway, cross-paper synthesis, and a
  "next-experiment design candidates" section explicitly mapping findings to RQ1, RQ2, RQ4, RQ5.
* `results/results_detailed.md` — theme-grouped synthesis with a comparison table of the surveyed
  methods against the t0014, t0019, t0020 findings (judge anchoring on model identity, v2 schema
  effect collapse under stronger judges, granularity-conditioning effects).

### Category Plan

The project's existing categories include `hierarchical-planning`, `agent-evaluation`,
`granularity-conditioning`, and `uncertainty-calibration`, which cover most of the surveyed work.
The following four categories are missing and must be created via `/add-category` before any paper
asset is written, so per-paper sub-agents do not race on category creation:

* `llm-as-judge` — covers Trust or Escalate; future tasks on judge calibration will reuse it.
* `reasoning-structure` — covers SELF-DISCOVER and any future reasoning-structure work.
* `agent-planning` — covers LATS and GraphPlanner; complements `hierarchical-planning` (which is
  about the three-level annotation hierarchy specific to this project).
* `reinforcement-learning` — covers ArCHer, the action-decomposition paper, and the options-
  framework anchor.

### Per-Paper Mapping

| # | Paper | Theme | Categories |
| --- | --- | --- | --- |
| 1 | Solving the Granularity Mismatch (ICLR 2026) | Hierarchical agents | hierarchical-planning, granularity-conditioning, reinforcement-learning |
| 2 | ArCHer (ICML 2024) | Hierarchical agents | hierarchical-planning, reinforcement-learning |
| 3 | Action Decomposition (NeurIPS 2024) | Hierarchical agents | hierarchical-planning, reinforcement-learning |
| 4 | Sutton, Precup & Singh 1999 (options) | Foundational theory | reinforcement-learning, hierarchical-planning |
| 5 | Graph Learning for Planning (NeurIPS 2024) | Search/planning | agent-planning, hierarchical-planning |
| 6 | LATS (ICML 2024) | Search/planning | agent-planning, reinforcement-learning |
| 7 | SELF-DISCOVER (NeurIPS 2024) | Reasoning structure | reasoning-structure |
| 8 | Embodied Agent Interface (NeurIPS 2024) | Agent benchmark | agent-evaluation, hierarchical-planning |
| 9 | AgentBoard (NeurIPS 2024 D&B) | Agent benchmark | agent-evaluation |
| 10 | Trust or Escalate | LLM-as-judge | llm-as-judge, uncertainty-calibration |

## Cost Estimation

Total: ~$3, with hard cap at $5 after 5 papers.

* PDF downloads: free (CrossRef / Semantic Scholar / OpenAlex / arXiv).
* Paper reading + summarization: 10 papers × ~$0.20-0.30 per paper ≈ $2-3.
* Synthesis writeup: ~$0.30.
* Buffer: ~$0.30.

Project budget remaining at task start: ~$26 (well above the $5 cap). The cost gate is unlikely to
fire but is monitored after each paper.

## Step by Step

The remaining steps after `planning` are:

1. **Implementation (step 9)**:
   * Create the 4 missing categories via `/add-category`.
   * For each of the 10 papers, spawn an `/add-paper` sub-agent. Run at most 3 sub-agents in
     parallel.
   * After each paper, the sub-agent runs `verify_paper_asset` itself and fixes errors.
   * Track download successes and failures. If > 2 of 10 fail to download, halt the parallel batch
     and produce a triage note.
   * After all 10 paper assets exist and verify, write `results/results_summary.md` and
     `results/results_detailed.md` using the contents of every `summary.md`.

2. **Results (step 12)**: Run `verify_task_results` and fix any errors.

3. **Suggestions (step 14)**: Write `results/suggestions.json` with follow-up suggestions for
   experiments motivated by the survey, using the suggestion specification.

4. **Reporting (step 15)**: Push the branch, open the PR, run the pre-merge verificator, address any
   errors, merge, refresh the overview/.

## Remote Machines

None. All work runs locally against external APIs (CrossRef, Semantic Scholar, OpenAlex, arXiv) and
the LLM API.

## Assets Needed

None. The survey reads only published literature; no upstream task assets are required.

## Expected Assets

10 paper assets in `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/assets/paper/`,
each passing `verify_paper_asset` with zero errors. The `task.json` `expected_assets` field is
`{"paper": 10}`.

## Time Estimation

~4-6 hours of agent execution (10 papers × ~30-40 min each). Wall-clock with 3-way parallelism is
~2-3 hours. Synthesis writeup ~30 min.

## Risks & Fallbacks

* **Risk**: Paywall blocks more than 2 papers. **Fallback**: Write abstract-based summaries with
  `download_status: "failed"` and `download_failure_reason` populated, per `add-paper` Phase 3.
* **Risk**: A paper turns out to be unrelated after reading. **Fallback**: Keep the asset (it is
  still documented project knowledge) and note the irrelevance in the synthesis.
* **Risk**: Multiple parallel paper-add agents collide on category creation. **Fallback**:
  Pre-create the four missing categories before the parallel batch begins; the rest of the asset
  construction is independent.
* **Risk**: A specific paper (e.g., the Sutton-Precup-Singh 1999 options framework) is hard to reach
  via DOI resolution. **Fallback**: Use the `no-doi_AuthorYear_slug` paper-ID convention and
  download from arXiv mirrors or institutional repositories; if unreachable, fall back to abstract-
  based summary.

## Verification Criteria

* All 10 paper assets pass `verify_paper_asset` with zero errors.
* `verify_task_results` passes for the task.
* `verify_logs` passes for all step folders.
* `results_summary.md` explicitly maps survey findings to RQ1, RQ2, RQ4, RQ5 design implications for
  Brainstorm Session 8.
* `results_detailed.md` contains a comparison table of the surveyed methods against the t0014,
  t0019, t0020 findings.
* `verify_task_file` passes; `expected_assets["paper"] == 10`.
* `verify_pr_premerge` passes before the merge.
