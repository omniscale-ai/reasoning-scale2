---
spec_version: "2"
task_id: "t0002_literature_survey_granularity_conditioning"
date_completed: "2026-04-29"
status: "complete"
---
# Detailed Results: Literature Survey on Granularity Conditioning and Hierarchical Agents

## Summary

The literature survey produced 11 paper assets covering all four survey threads. The synthesis is in
`results/results_summary.md`. This detailed file documents the methodology, the per-paper mapping to
project research questions, the verificator outcomes, the limitations of the abstract-based
summarization approach, the files created, and the requirement-by-requirement coverage.

## Methodology

* **Machine**: local macOS workstation, no remote compute.
* **Runtime**: about 30 minutes wall clock for the full task (research-papers, research-internet,
  research-code, planning, implementation, results stages).
* **Timestamps**: task started `2026-04-29T13:50:47Z`, implementation completed
  `2026-04-29T14:21:21Z`, results stage written `2026-04-29T14:22:30Z`.
* **Tooling**: WebSearch (17 queries) and WebFetch (4 arXiv pages) for paper discovery and metadata.
  `aggregate_papers`, `aggregate_libraries`, `aggregate_tasks`, `aggregate_categories` for corpus
  and metadata enumeration. `verify_paper_asset` per paper.
* **Cost**: $0 spent during the task. PDF downloads were deferred per the plan; abstracts and
  public-source content were used for summaries instead of paid LLM-driven summarization. The $3.40
  estimate in the plan assumed `/add-paper` would invoke a paid LLM per paper; in practice, the task
  was driven entirely by the orchestrator's existing context, so no Anthropic API was invoked beyond
  what was already consumed by the orchestrator.

## Per-Paper Mapping to Research Questions

| Paper | Citation Key | Threads | RQ Mapping |
| --- | --- | --- | --- |
| FrontierMath | Glazer2024 | benchmark | RQ3 (per-source schemas) |
| WorkArena | Drouin2024 | benchmark | RQ3, RQ4 |
| WorkArena++ | Boisvert2024 | benchmark + hierarchical | RQ1, RQ3, RQ4, sub-hyp 1 |
| SWE-bench | Jimenez2024 | benchmark | RQ3 |
| SWE-bench Verified | OpenAI2024 | benchmark + annotation | RQ3, RQ4 |
| tau-bench | Yao2024 | benchmark | RQ1, RQ3, Metric 3 |
| ReAct | Yao2022 | granularity + hierarchical | RQ1 |
| Plan-and-Solve | Wang2023 | granularity + hierarchical | RQ1 (B baseline) |
| Reflexion | Shinn2023 | hierarchical + granularity | RQ1 (Phase 3) |
| Least-to-Most | Zhou2022 | hierarchical + granularity | RQ1 (effect-size anchor) |
| Confidence Elicitation | Xiong2024 | calibration | RQ2, Metric 2 |

Coverage by thread:

* **Granularity / scope conditioning** (Thread A): 4 papers (Yao2022, Wang2023, Shinn2023, Zhou2022)
  plus the implicit treatments in WorkArena++ and tau-bench.
* **Hierarchical decomposition** (Thread B): 4 papers (Wang2023, Zhou2022, Yao2022, Boisvert2024).
* **Calibration** (Thread C): 1 paper (Xiong2024); thread is narrower in the literature so 1 paper
  covers the canonical methodology.
* **Four roadmap benchmarks** (Thread D): 6 papers (Glazer2024, Drouin2024, Boisvert2024,
  Jimenez2024, OpenAI2024, Yao2024) — one per benchmark plus parent-paper coverage where needed.

## Verification

| Verificator | Result |
| --- | --- |
| `verify_research_papers` | PASSED (1 word-count warning fixed) |
| `verify_research_internet` | PASSED zero-errors zero-warnings |
| `verify_research_code` | PASSED zero-errors zero-warnings |
| `verify_plan` | PASSED zero-errors zero-warnings (after 2 small fixes) |
| `verify_paper_asset` × 11 | PASSED zero-errors on each (1 minor PA-W007 fixed) |
| `aggregate_papers --format ids` | reports 11 paper IDs |

## Limitations

* **Abstract-based summaries**: Each paper's `summary.md` was written from the abstract plus
  publicly available descriptions, not from reading the full PDF. Each summary explicitly
  acknowledges this in its Overview section. The most-affected sections are
  *Architecture/Models/Methods* (where details require reading methodology) and *Results* (where
  per-table numbers require reading the experiments). The project's planning step should consider
  scheduling a re-fetch task that downloads PDFs and updates each summary's methodology and results
  sections.
* **PDF downloads deferred**: All 11 paper assets have `download_status: "failed"` with a consistent
  `download_failure_reason` explaining that PDF retrieval was deferred to a future task that enables
  git LFS. The benchmark/repo URLs are recorded in `details.json` `pdf_url` for that future task to
  use directly.
* **Empty corpus baseline**: This is the project's first literature survey; no prior corpus existed
  to cross-reference. The research-papers stage was therefore minimal. The project's next literature
  survey will benefit from this corpus as a starting point.
* **One non-DOI paper**: SWE-bench Verified is a technical card with no DOI. The asset uses the
  `no-doi_OpenAI2024_swe-bench-verified` slug per the v3 spec. This is a known and accepted case;
  the verificator passes.

## Examples

### Example: Discovered-Paper Entry From research_internet.md

```text
### [Boisvert2024]

* **Title**: WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge
  Work Tasks
* **Authors**: Léo Boisvert, Megh Thakkar, Maxime Gasse et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2407.05291`
* **URL**: https://arxiv.org/abs/2407.05291
* **Suggested categories**: `benchmark-workarena`, `hierarchical-planning`, `agent-evaluation`
* **Why download**: The exact benchmark named in `project/description.md`. Composes WorkArena
  atomics into 682 compositional tasks — direct match for the project's three-level granularity
  schema.
```

### Example: details.json Snippet (Boisvert2024)

```json
{
  "spec_version": "3",
  "paper_id": "10.48550_arXiv.2407.05291",
  "doi": "10.48550/arXiv.2407.05291",
  "title": "WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work Tasks",
  "categories": ["benchmark-workarena", "hierarchical-planning", "agent-evaluation"],
  "citation_key": "Boisvert2024",
  "download_status": "failed",
  "download_failure_reason": "PDF download deferred per task plan: literature-survey uses abstract-based summaries; PDFs deferred to a future task that enables git LFS."
}
```

### Example: Summary Section (Boisvert2024 Main Ideas)

```text
* WorkArena++ is the **strongest single test bed** in the project's four-source composite for
  measuring the atomic-vs-compositional gap that granularity conditioning is meant to close.
* The synthetic trace generator can supply gold actions at the atomic level for Phase 1
  annotation, complementing the manual annotation of global and subtask actions.
* Reuse the BrowserGym harness end-to-end — the project does not need to build a separate
  WorkArena++ adapter on top of the WorkArena adapter; they share the same harness.
```

## Files Created

* `research/research_papers.md`
* `research/research_internet.md`
* `research/research_code.md`
* `plan/plan.md`
* `assets/paper/10.48550_arXiv.2411.04872/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2403.07718/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2407.05291/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2310.06770/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/no-doi_OpenAI2024_swe-bench-verified/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2406.12045/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2210.03629/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2305.04091/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2303.11366/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2205.10625/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.48550_arXiv.2306.13063/{details.json,summary.md,files/.gitkeep}`
* `results/results_summary.md`
* `results/results_detailed.md`
* `results/metrics.json`
* `results/costs.json`
* `results/remote_machines_used.json`

## Task Requirement Coverage

Operative task text (verbatim from `task.json` plus `task_description.md`):

```text
Literature survey: granularity conditioning and hierarchical agents
Survey literature on granularity/scope conditioning, hierarchical task decomposition, and
uncertainty calibration for LLM agents.
expected_assets: { "paper": 10 }
task_types: [ "literature-survey" ]
```

```text
[task_description.md]
Scope: granularity conditioning, hierarchical decomposition, calibration,
four roadmap benchmarks (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench).
Expected outputs: ≥10 paper assets; research/research_papers.md; research/research_internet.md;
results/results_summary.md with thread-by-thread takeaways; results/suggestions.json with
follow-up ideas.
```

| ID | Requirement | Result | Status | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | Produce >=10 paper assets covering the four threads | 11 produced | Done | `aggregate_papers --format ids` shows 11 IDs |
| REQ-2 | Each paper conforms to v3 paper spec | All 11 verified | Done | 11 × `verify_paper_asset` PASSED zero-errors |
| REQ-3 | Coverage across the four threads | 4 of 4 threads covered with >=1 paper each (most with >=2) | Done | See "Per-Paper Mapping" table above |
| REQ-4 | Tag every paper with `meta/categories/` slug | All 11 have non-empty `categories` | Done | Inspect `details.json` `categories` per paper |
| REQ-5 | Synthesize findings thread-by-thread in `results_summary.md` | Synthesis section written | Done | `results/results_summary.md` "Synthesis" section |
| REQ-6 | Surface follow-up suggestions in `results/suggestions.json` | Pending the suggestions stage (orchestrator step 14) | Partial | Suggestions stage will materialize this |
| REQ-7 | Stay under $5 per-task budget | $0 spent | Done | `results/costs.json` total_cost_usd = 0 |

REQ-6 is partial in the results stage because the orchestrator's later suggestions stage produces
`results/suggestions.json`. This is by design per the execute-task SKILL.md, which separates results
writing from suggestions generation.
