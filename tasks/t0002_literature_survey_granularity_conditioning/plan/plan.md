---
spec_version: "2"
task_id: "t0002_literature_survey_granularity_conditioning"
date_completed: "2026-04-29"
status: "complete"
---
## Objective

Produce a literature survey of at least 10 paper assets covering four threads — granularity / scope
conditioning of LLM agents, hierarchical task decomposition, uncertainty calibration with
overconfident error rate, and the four roadmap benchmarks (FrontierScience-Olympiad, WorkArena++,
SWE-bench Verified, tau-bench) — and synthesize the survey into `results/results_summary.md` and
`results/results_detailed.md`. Done means: every discovered paper from
`research/research_internet.md` `## Discovered Papers` has a corresponding paper asset under
`assets/paper/<paper_id>/` that passes the v3 paper-asset verificator, and the synthesis documents
cite each paper at least once with thread-by-thread takeaways and Phase 2 recommendations.

## Task Requirement Checklist

The operative task text from `task.json` plus `task_description.md`:

```text
Literature survey: granularity conditioning and hierarchical agents
Survey literature on granularity/scope conditioning, hierarchical task decomposition, and
uncertainty calibration for LLM agents.
expected_assets: { "paper": 10 }
task_types: [ "literature-survey" ]
```

```text
[task_description.md] Scope: granularity conditioning, hierarchical decomposition, calibration,
four roadmap benchmarks (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench).
Expected outputs: ≥10 paper assets; research/research_papers.md; research/research_internet.md;
results/results_summary.md with thread-by-thread takeaways; results/suggestions.json with
follow-up ideas.
```

Concrete requirements:

* **REQ-1**: Produce at least 10 paper assets under `assets/paper/<paper_id>/` covering the four
  survey threads. Satisfied by Step 2; evidence is the count from `aggregate_papers.py` filtered to
  `--ids` matching the discovered list.
* **REQ-2**: Each paper asset must conform to the v3 paper-asset specification — `details.json`,
  canonical summary document, and `files/` (or `.gitkeep` plus failure reason). Satisfied by Step 2
  with `verify_paper_asset.py` per paper.
* **REQ-3**: Distribute coverage across the four threads (granularity conditioning, hierarchical
  decomposition, calibration, four roadmap benchmarks). Satisfied by Step 2 selecting at least 2
  papers per thread.
* **REQ-4**: Tag every paper with at least one project category from `meta/categories/`. Satisfied
  by Step 2; evidence is each `details.json` `categories` array.
* **REQ-5**: Synthesize findings into a thread-by-thread `results/results_summary.md`. Satisfied by
  Step 3 in the orchestrator results stage.
* **REQ-6**: Surface follow-up suggestions for the next brainstorm into `results/suggestions.json`.
  Satisfied by the suggestions stage handled by execute-task, not by this plan.
* **REQ-7**: Stay under the 5 USD per-task soft cap and the 10 USD hard cap. Satisfied by Step 1
  budget gate plus the Cost Estimation section below.

## Approach

The implementation is **entirely orchestrator-driven** through the `/add-paper` skill — there is no
task-local Python code. For each of the 11 papers in `research/research_internet.md`
`## Discovered Papers`, the orchestrator spawns a `/add-paper` subagent that downloads the PDF,
extracts metadata, and writes both `details.json` and the canonical summary document. The
orchestrator runs at most 3 such subagents in parallel to respect Anthropic API rate limits and the
5 USD soft cap. Tagging follows the suggested-category list in `research_internet.md`, drawn
exclusively from the nine slugs in `meta/categories/`.

**Alternatives considered**: A batched script that downloads all 11 PDFs in a single shot and writes
their summaries from a single context was considered and rejected. Per-paper subagents are the
framework norm (see CLAUDE.md rule 9 and execute-task SKILL.md "spawn one subagent per asset"); a
batched script would defeat asset-isolation, would not let `verify_paper_asset.py` run between
papers, and would require task-local code that `research_code.md` explicitly recommends against.

**Task types**: `literature-survey`, as already declared in `task.json`. The Planning Guidelines in
`meta/task_types/literature-survey/instruction.md` specify (a) checking the corpus before each add
(achieved by Step 1), (b) using `/add-paper` per paper (Step 2), and (c) producing a synthesis that
goes beyond a per-paper list (Step 3).

## Cost Estimation

| Item | Cost | Notes |
| --- | --- | --- |
| Anthropic API per paper summary | ~$0.30 | 11 papers × ~$0.30 each = ~$3.30 |
| Aggregator + verificator runs | $0.00 | local Python |
| Synthesis writing in results stage | ~$0.10 | brief Anthropic usage |
| **Estimated total** | **~$3.40** | well under $5 soft cap |

The project budget shows $100 total with $0 spent and a $10 per-task default. The $3.40 estimate is
comfortably below both the $5 task-description budget and the $10 per-task limit. The
`available_services` list contains only `anthropic_api`, so all costs flow through Anthropic.

## Step by Step

1. **Pre-flight: empty-corpus and category check.** Run
   `uv run python -u -m arf.scripts.aggregators.aggregate_papers --format json --detail short`.
   Confirm `paper_count == 0` (empty corpus, so no duplication risk). Run `ls meta/categories/` to
   confirm the nine project categories exist. If either check fails, halt and create an intervention
   file. Satisfies REQ-1 prerequisite.

2. **Add 11 paper assets via `/add-paper`.** For each paper in `research/research_internet.md`
   `## Discovered Papers`, spawn a `/add-paper` subagent (max 3 in parallel). Pass
   `--task-id t0002_literature_survey_granularity_conditioning` and the paper's arXiv ID or DOI from
   the discovered-papers list. Suggested categories per paper come from the same list and are taken
   exclusively from `meta/categories/`. After each subagent finishes, run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id $TASK_ID -- uv run python -m arf.scripts.verificators.verify_paper_asset --task-id $TASK_ID <paper_id>`.
   The expected output is the verificator printing PASSED with zero errors. If a download fails, the
   `/add-paper` skill writes `download_status: "failed"` and a `download_failure_reason`, and the
   asset is still committed. Satisfies REQ-1, REQ-2, REQ-3, REQ-4. The 11 papers are:

   * `2411.04872` (Glazer2024, FrontierMath) — categories: benchmark-frontierscience,
     agent-evaluation
   * `2403.07718` (Drouin2024, WorkArena) — categories: benchmark-workarena, agent-evaluation
   * `2407.05291` (Boisvert2024, WorkArena++) — categories: benchmark-workarena,
     hierarchical-planning, agent-evaluation
   * `2310.06770` (Jimenez2024, SWE-bench) — categories: benchmark-swebench, agent-evaluation
   * `https://openai.com/index/introducing-swe-bench-verified/` (SWE-Verified-2024) — categories:
     benchmark-swebench, benchmark-annotation, agent-evaluation
   * `2406.12045` (Yao2024, tau-bench) — categories: benchmark-taubench, agent-evaluation
   * `2210.03629` (Yao2022, ReAct) — categories: granularity-conditioning, hierarchical-planning
   * `2305.04091` (Wang2023, Plan-and-Solve) — categories: granularity-conditioning,
     hierarchical-planning
   * `2303.11366` (Shinn2023, Reflexion) — categories: hierarchical-planning,
     granularity-conditioning
   * `2205.10625` (Zhou2022, Least-to-Most) — categories: hierarchical-planning,
     granularity-conditioning
   * `2306.13063` (Xiong2024, LLM Confidence Elicitation) — categories: uncertainty-calibration,
     agent-evaluation
   * (Optional 12th) `2201.11903` (Wei2022, Chain-of-Thought) — categories:
     granularity-conditioning, hierarchical-planning. Adds the canonical CoT baseline if budget
     allows.

3. **Cross-corpus verification gate.** Run
   `uv run python -u -m arf.scripts.aggregators.aggregate_papers --format json --detail short` and
   confirm `paper_count >= 10`. Spot-check one paper folder with `ls assets/paper/<paper_id>/` to
   confirm the trio (`details.json`, summary.md, `files/`). Satisfies REQ-1, REQ-2.

The Step by Step ends here. All later writing is handled by the orchestrator's analysis and
reporting steps and is out of scope for this plan.

## Remote Machines

None required. All work runs locally; the only paid resource is the Anthropic API.

## Assets Needed

* `research/research_internet.md` `## Discovered Papers` (already produced) — input list of 11
  papers to add.
* `meta/categories/` — closed list of nine project categories used for tagging.
* Anthropic API access via the `available_services` declaration in `project/budget.json`.
* Internet access to arXiv, OpenAI blog (for the SWE-bench Verified card), and Sierra-research
  GitHub.

## Expected Assets

* 11 paper assets (10 minimum + 1 optional CoT baseline) under
  `tasks/t0002_*/assets/paper/<paper_id>/` matching the v3 paper-asset specification. This matches
  `task.json` `expected_assets: { "paper": 10 }` with one above the minimum to reduce risk if any
  single download fails.

## Time Estimation

* Research (already completed in steps 4-6 of the orchestrator): n/a.
* Implementation (Step 2 here): ~25 minutes wall clock with 3-way parallel `/add-paper` subagents,
  ~5 USD budget cap as a hard upper bound.
* Verification (Step 3 here): ~2 minutes.
* Synthesis writing in the orchestrator's results stage: ~10 minutes.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| arXiv PDF download failure | Medium | Low | Mark `download_status: "failed"` per the v3 spec and continue; abstract still appears in summary. |
| Anthropic API rate limiting | Low | Delays | Cap parallelism at 3 subagents; use exponential backoff. |
| Budget overrun above 5 USD soft cap | Low | Reporting flag | Stop after 11 papers; the 12th CoT paper is conditional on remaining headroom. |
| `verify_paper_asset` reports a missing field | Medium | Re-run | Re-invoke `/add-paper` for the offending paper or hand-edit `details.json`. |
| SWE-bench Verified is a blog card without a DOI | High (already known) | Low | Use the `no-doi_OpenAI2024_swe-bench-verified` slug and `download_status: "failed"` if the static HTML is not retrievable. |
| One discovered paper duplicates another after slug normalization | Low | Loss of one slot | Run `aggregate_papers.py` between adds and skip the duplicate. |

## Verification Criteria

* `uv run python -u -m arf.scripts.aggregators.aggregate_papers --format json --detail short`
  reports `paper_count >= 10`. Confirms REQ-1.
* For every paper folder under `assets/paper/`,
  `uv run python -m arf.scripts.utils.run_with_logs --task-id $TASK_ID -- uv run python -m arf.scripts.verificators.verify_paper_asset --task-id $TASK_ID <paper_id>`
  exits with zero errors. Confirms REQ-2.
* Each `details.json` `categories` array is non-empty and every value matches a folder under
  `meta/categories/`. Quick check:
  `python3 -c "import json,glob; ok=all(json.load(open(p))['categories'] for p in glob.glob('tasks/t0002_*/assets/paper/*/details.json')); print(ok)"`
  prints `True`. Confirms REQ-4.
* Coverage by thread: at least one paper tagged `benchmark-frontierscience`, one tagged
  `benchmark-workarena`, one tagged `benchmark-swebench`, one tagged `benchmark-taubench`, two
  tagged `granularity-conditioning` or `hierarchical-planning`, and one tagged
  `uncertainty-calibration`. Confirms REQ-3.
* `tasks/t0002_*/results/results_summary.md` exists, contains a `## Synthesis` or thread-by-thread
  takeaways section, and cites every paper asset at least once. Confirms REQ-5.
