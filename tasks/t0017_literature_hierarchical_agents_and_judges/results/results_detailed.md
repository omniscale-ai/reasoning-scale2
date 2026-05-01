---
spec_version: "2"
task_id: "t0017_literature_hierarchical_agents_and_judges"
date_completed: "2026-05-01"
status: "complete"
---
# Detailed Results: Literature Survey on Hierarchical Agents and LLM-as-Judge

## Summary

This file extends `results_summary.md` with one paragraph per paper plus an at-a-glance table. Each
paper is referenced by its `citation_key` from `details.json`. The synthesis grouped by five themes
is in `results/results_summary.md`. This detailed file documents the methodology, the per-theme
paper notes, the backlog mapping, the verificator outcomes, the limitations of the
abstract-and-text-based summarisation approach, and the files created.

## Methodology

* **Machine**: local macOS workstation, no remote compute.
* **Runtime**: about 100 minutes wall clock for the full task (research, analysis, reporting). Step
  1 (research) ran 60 minutes with ten parallel `/add-paper` agents; step 2 (analysis) ran 20
  minutes; step 3 (reporting) ran 20 minutes.
* **Timestamps**: task started `2026-05-01T00:00:00Z`, ended `2026-05-01T01:40:00Z`.
* **Tooling**: `/add-paper` skill (×10 in parallel) drove identity resolution (CrossRef + Semantic
  Scholar + OpenAlex + arXiv), PDF download, `details.json` generation, and nine-section summary
  writing. `meta.asset_types.paper.verificator` was run once per paper.
* **Cost**: $0.00 spent during the task. The metadata APIs are free; PDF downloads have no marginal
  cost beyond agent time. No paid LLM API or remote GPU was used.

## At-a-glance Table

| Theme | Paper ID | Citation Key | Title (short) | Venue |
| --- | --- | --- | --- | --- |
| Hierarchical | `no-doi_Gao2026_hierarchical-preference-learning-llm-agents` | `Gao2026` | Solving the Granularity Mismatch | ICLR 2026 |
| Hierarchical | `10.48550_arXiv.2402.19446` | `Zhou2024` | ArCHer | ICML 2024 |
| Hierarchical | `10.48550_arXiv.2405.15821` | `Wen2024` | Action Decomposition (POAD/BAD) | NeurIPS 2024 |
| Hierarchical | `no-doi_Sutton1999_options-framework` | `Sutton1999` | Between MDPs and Semi-MDPs (options) | Artificial Intelligence (1999) |
| Search/Plan | `10.48550_arXiv.2405.19119` | `Wu2024` | Can Graph Learning Improve Planning? | NeurIPS 2024 |
| Search/Plan | `10.48550_arXiv.2310.04406` | `Zhou2024a` | LATS | ICML 2024 |
| Reasoning | `10.48550_arXiv.2402.03620` | `Zhou2024b` | SELF-DISCOVER | NeurIPS 2024 |
| Benchmark | `10.48550_arXiv.2410.07166` | `Li2024` | Embodied Agent Interface | NeurIPS 2024 |
| Benchmark | `10.48550_arXiv.2401.13178` | `Ma2024` | AgentBoard | NeurIPS 2024 D&B |
| Judge | `10.48550_arXiv.2407.18370` | `Jung2024` | Trust or Escalate | ICLR 2025 |

## Per-paper Notes

### Theme 1: Hierarchical / Granularity-Aware Agents

* **`Gao2026`** introduces hierarchical preference learning (HPL) with mid-granularity sub-task
  groups identified by an LLM, plus a curriculum that starts with short, high-margin pairs and
  progresses to long, low-margin ones. Proposition 1's bias-variance argument is the cleanest
  theoretical justification we have for preferring mid-granularity signals on long-horizon tasks
  with sparse rewards. Strengthens t0009 and t0014.
* **`Zhou2024` (ArCHer)** decomposes multi-turn LLM-agent RL into an off-policy utterance-level
  critic and an on-policy token-level actor. Hierarchical decomposition scales with model size (100M
  -> 7B), evidence that hierarchical RL is not a small-model trick.
* **`Wen2024` (POAD with BAD)** establishes the correct way to do token-level credit assignment in
  free-form action spaces: keep `gamma_w = 1` inside an action so the token-level update is
  consistent with the original MDP. Reduces complexity from `O(|V|^|a|)` to `O(|a|*|V|)`. The
  discrepancy between action-level and naive token-level optimisation grows with action length,
  which is directly relevant to our scope-aware vs scope-mismatched conditions.
* **`Sutton1999`** is the theory anchor. Options as `<I, pi, beta>` triples + the SMDP equivalence
  + interruption + subgoal pseudo-rewards all map directly onto our project's three-level hierarchy
    and ABC condition design.

### Theme 2: Search and Planning Structure

* **`Wu2024`** reframes LLM-agent planning as graph decision-making (path or subgraph selection). A
  parameter-free 1-hop SGC step over sentence embeddings already beats most prompting baselines; a
  small trained GraphSAGE adds another large jump for 3-15 minutes of GPU time. Restricting
  candidates to graph nodes drops hallucination rate from >20% to <1%.
* **`Zhou2024a` (LATS)** unifies MCTS, ReAct, and Reflexion with LM-as-judge value functions and
  verbal self-reflection. Achieves higher accuracy than alternatives while expanding fewer nodes
  (3.55 fewer than RAP, 12.12 fewer than ToT on HotPotQA). Useful as a strong planning baseline for
  the scope-aware (A) condition.

### Theme 3: Reasoning Structure Discovery

* **`Zhou2024b` (SELF-DISCOVER)** lets the LLM compose atomic reasoning modules into an explicit
  task-conditioned reasoning structure that is then re-used across instances of the same task.
  Improves GPT-4 and PaLM 2 by up to 32% on BigBench-Hard, agent reasoning, and MATH versus CoT,
  while requiring 10-40x fewer inference compute than CoT-Self-Consistency. Discovered structures
  transfer cleanly across model families, suggesting "what to think about" is a more portable
  abstraction than "what words to use".

### Theme 4: Agent Benchmarks

* **`Li2024` (EAI)** decomposes embodied planning into goal interpretation, subgoal decomposition,
  action sequencing, and transition modeling, and reports a fine-grained error taxonomy
  (hallucination, affordance, missing/extra/wrong-order steps, precondition/effect errors). The
  taxonomy is the strongest direct template for our ABC-condition diagnostics. EAI also shows
  test-time reasoning (o1-style) gives more embodied-planning quality than additional parameters on
  these benchmarks.
* **`Ma2024` (AgentBoard)** introduces "progress rate" as a single comparable scalar across
  benchmarks, with subgoal-level annotation across 1013 environments (Pearson rho > 0.95 vs humans).
  Demonstrates a hard/easy split based on subgoal count, six-dimensional sub-skill scoring, and that
  open-weight models plateau at about 6 steps - all directly relevant to our benchmark
  stratification choices.

### Theme 5: LLM-as-Judge Methodology

* **`Jung2024` (Trust or Escalate)** introduces selective LLM judging with calibrated thresholds and
  finite-sample, distribution-free guarantees on human agreement. Simulated Annotators is a drop-in
  ensemble-based confidence estimator that works on top of any judge LLM, and judge cascades convert
  "model choice" into "abstention policy". Empirically, 75% of pairwise judging on ChatArena can be
  handled by Mistral-7B or GPT-3.5 while preserving an 80% human-agreement floor that GPT-4 alone
  never reaches. Directly strengthens S-0009-03.

## Mapping to Backlog and Prior Tasks

| Backlog item | Effect of survey | Strongest evidence |
| --- | --- | --- |
| t0009 (hierarchical annotation v2) | Strengthens | `Gao2026`, `Zhou2024`, `Wen2024`, `Sutton1999` |
| t0014 (v2 annotator sonnet rerun) | Strengthens | `Gao2026` Proposition 1 |
| t0012 (phase-2 ABC smoke) | Informs | `Sutton1999` (options as A/B/C frame), `Li2024` taxonomy, `Ma2024` progress rate |
| S-0009-03 (multi-judge agreement) | Strengthens | `Jung2024` |
| S-0009-04 (truncation/schema deconfound) | Informs | `Gao2026`, `Wen2024` (granularity effect is real even at full context) |

## Verification

| Verificator | Result |
| --- | --- |
| `meta.asset_types.paper.verificator` × 10 | PASSED zero-errors zero-warnings on each paper after one PA-W005 cleanup on `Zhou2024b` (invented category slugs replaced with existing slugs from `meta/categories/`). |
| `verify_research_papers` | PASSED zero-errors zero-warnings. |
| `verify_research_internet` | PASSED zero-errors zero-warnings. |
| `verify_research_code` | PASSED with 3 minor word-count and ###-subsection warnings (literature-survey scope is intentionally light on code). |
| `verify_plan` | PASSED with 5 non-blocking warnings (frontmatter, short Remote Machines / Expected Assets sections, Risks bullets vs table, mention of orchestrator-managed files). |
| `verify_suggestions` | PASSED zero-errors zero-warnings. |
| `verify_corrections` | PASSED zero-errors zero-warnings. |
| `verify_logs` | PASSED with 3 non-blocking empty-folder warnings on `logs/commands/`, `logs/searches/`, `logs/sessions/`. |
| `verify_task_results` | PASSED. |
| `verify_task_file` | PASSED. |
| `aggregate_papers --format ids` | reports the 10 new paper IDs in the corpus. |

## Limitations

* **Mixed-source summaries**: Eight of ten paper summaries were written from the full PDF content
  via `pypdf` extraction; one (`Sutton1999`) was sourced from a public university course mirror and
  summarised from full text; one (`Gao2026`) is the latest ICLR 2026 accepted paper and was
  summarised from the camera-ready PDF available on OpenReview. All ten summaries are based on
  full-paper content, not abstracts only — this is a stronger evidence base than t0002's
  abstract-only summaries.
* **Two non-DOI papers**: `Sutton1999` uses the `no-doi_` fallback because its DOI contains
  parentheses that the canonical `doi_to_slug` utility rejects; `Gao2026` uses the `no-doi_`
  fallback because the paper has no registered DOI yet. Both cases are explicit in the v3 paper
  specification.
* **Survey scope is bounded**: Only ten papers were added; a follow-up task could extend to inverse-
  RL judges, judge ensembles beyond `Jung2024`, and additional embodied-agent benchmarks beyond
  `Li2024` and `Ma2024`.
* **No quantitative benchmark**: This is a literature-survey task; there are no project-level
  metrics (`metrics.json` is `{}` and `costs.json` reports $0.00). Quantitative validation of any
  synthesis claim is the responsibility of follow-up experimental tasks (S-0017-01..03).

## Files Created

* Ten paper-asset folders under `assets/paper/`, each with `details.json`, nine-section
  `summary.md`, and at least one PDF in `files/`:
  * `assets/paper/10.48550_arXiv.2310.04406/` (Zhou2024a — LATS)
  * `assets/paper/10.48550_arXiv.2401.13178/` (Ma2024 — AgentBoard)
  * `assets/paper/10.48550_arXiv.2402.03620/` (Zhou2024b — SELF-DISCOVER)
  * `assets/paper/10.48550_arXiv.2402.19446/` (Zhou2024 — ArCHer)
  * `assets/paper/10.48550_arXiv.2405.15821/` (Wen2024 — POAD with BAD)
  * `assets/paper/10.48550_arXiv.2405.19119/` (Wu2024 — Graph Learning Planning)
  * `assets/paper/10.48550_arXiv.2407.18370/` (Jung2024 — Trust or Escalate)
  * `assets/paper/10.48550_arXiv.2410.07166/` (Li2024 — Embodied Agent Interface)
  * `assets/paper/no-doi_Gao2026_hierarchical-preference-learning-llm-agents/` (Gao2026 — HPL)
  * `assets/paper/no-doi_Sutton1999_options-framework/` (Sutton1999 — options framework)
* `plan/plan.md`
* `research/research_papers.md`, `research/research_internet.md`, `research/research_code.md`
* `step_tracker.json`
* `logs/session_log.md`
* `logs/steps/001_research/step_log.md`, `logs/steps/002_analysis/step_log.md`,
  `logs/steps/003_reporting/step_log.md`
* `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
  `results/suggestions.json`, `results/costs.json`, `results/remote_machines_used.json`
* Top-level dependency: `pypdf` added to `pyproject.toml` and `uv.lock` (per CLAUDE.md rule 3,
  top-level Python tooling files are the only legitimate non-task changes).

## Files Referenced

Each row in the at-a-glance table corresponds to `assets/paper/<paper_id>/details.json` and
`assets/paper/<paper_id>/summary.md`. Refer to the canonical summary for the full nine-section
write-up of each paper.

## Task Requirement Coverage

Operative task text (verbatim from `task.json` plus `task_description.md`):

```text
Literature: Hierarchical Agents and LLM-as-Judge
Literature survey of recent papers on hierarchical/granularity-aware LLM agents and
LLM-as-judge methodology, plus the foundational options-framework paper.
expected_assets: { "paper": 10 }
task_types: [ "literature-survey" ]
```

| ID | Requirement | Result | Status | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | Add 10 paper assets | 10 paper assets added | DONE | `assets/paper/` contains 10 subfolders; `aggregate_papers --format ids` lists all ten. |
| REQ-2 | Cover hierarchical / granularity-aware agents | 4 papers (P1, P2, P3, P10) | DONE | `Gao2026`, `Zhou2024`, `Wen2024`, `Sutton1999` summaries in `assets/paper/`. |
| REQ-3 | Cover search and planning structure | 2 papers (P4, P5) | DONE | `Wu2024`, `Zhou2024a` summaries in `assets/paper/`. |
| REQ-4 | Cover reasoning structure discovery | 1 paper (P6) | DONE | `Zhou2024b` summary in `assets/paper/`. |
| REQ-5 | Cover agent benchmarks | 2 papers (P7, P8) | DONE | `Li2024`, `Ma2024` summaries in `assets/paper/`. |
| REQ-6 | Cover LLM-as-judge methodology | 1 paper (P9) | DONE | `Jung2024` summary in `assets/paper/`. |
| REQ-7 | Synthesis grouped by 5 themes | 5-theme synthesis written | DONE | `results/results_summary.md` Theme 1-5 sections. |
| REQ-8 | Pointers to t0009, t0014, t0012, S-0009-03, S-0009-04 | All 5 referenced | DONE | "Pointers Back to Backlog Suggestions and Prior Tasks" in `results/results_summary.md`. |
| REQ-9 | Follow-up suggestions | 3 new suggestions drafted | DONE | `results/suggestions.json` (S-0017-01, S-0017-02, S-0017-03). |
| REQ-10 | Verifier passes on all paper assets | 10/10 zero-error zero-warning | DONE | `meta.asset_types.paper.verificator` per paper after PA-W005 cleanup on `Zhou2024b`. |
