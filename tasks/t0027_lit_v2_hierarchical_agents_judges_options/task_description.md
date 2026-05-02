# Literature Survey v2: Hierarchical Agents, Judges, Options Framework

## Motivation

This survey assembles ten papers — nine recent (2024-2026) and one foundational (1999) — that
together cover the three areas the project's next iteration must address:

1. **Hierarchical / granularity-aware LLM agents** — directly relevant to the project's central
   hypothesis that scope-aware agents (variant A) outperform scope-unaware (variant B) and
   scope-mismatched (variant C) agents. Recent 2024-2026 work on hierarchical preference learning,
   hierarchical multi-turn RL, and policy optimization with action decomposition gives us concrete
   architectures and training recipes to compare against the project's prompt-only conditioning.
2. **Search and planning structure for agents** — graph-based planners and tree-search controllers
   (LATS) inform whether the project should add explicit search/backtracking in v3 of the agents.
3. **Reasoning structure discovery** — SELF-DISCOVER illustrates self-composing reasoning
   structures, which is a relevant baseline for the v2 plan-and-solve agent's reasoning-structure
   choices.
4. **Agent benchmarks** — Embodied Agent Interface and AgentBoard formalize what the project's own
   benchmark composition (SWE-bench Verified + Tau-bench + FrontierScience-Olympiad) should report,
   especially around subgoal progress and error taxonomy (already partially adopted in t0022).
5. **LLM-as-judge methodology** — "Trust or Escalate" gives a provable-guarantee framework for
   LLM-judge agreement with humans, directly informing the project's t0019/t0026 judge design and
   the planned RQ3 inter-judge work.
6. **Options framework as theoretical anchor** — Sutton, Precup & Singh 1999 provides the canonical
   options/SMDP foundation for hierarchical RL and grounds our prompt-level granularity hierarchy in
   a long-standing decision-theoretic framework.

## CRITICAL: All 10 Papers Already Exist in the Project

Before any implementation, note that **every paper on the list below has already been added to the
project by `t0017_literature_hierarchical_agents_and_judges`**. The aggregator
(`uv run python -u -m arf.scripts.aggregators.aggregate_papers --format ids`) confirms this.
Re-adding them under `tasks/t0027_.../assets/paper/` would duplicate existing assets and fail the
project's no-duplication invariant.

The implementation step must therefore **re-scope** this task at planning time. Two acceptable
re-scopings:

* **Option A — Synthesis-only** (recommended): leave the paper assets in their `t0017` home, set
  `expected_assets` to `{}` via a correction file, and produce a **v2 synthesis** in
  `results/results_summary.md` that goes beyond `t0017`'s synthesis by tying every paper to one of
  the project's three current pain points: (1) v3 prompt design for scope-aware vs scope-mismatched
  agents, (2) v3 calibration prompts for `final_confidence`, (3) v3 judge prompts that hit the
  "Trust or Escalate" threshold. The 10 papers below become the corpus for the synthesis; no new
  paper assets are produced.

* **Option B — Extend with additional papers**: keep `expected_assets: {"paper": 10}` but treat the
  10 listed papers as the **already-covered** subset and search arXiv / Semantic Scholar / Google
  Scholar for **10 additional 2024-2026 papers** on the same themes that t0017 missed. Examples
  worth scoping: papers on agent-judge calibration after late-2024, papers on options / hierarchical
  RL applied to LLMs in 2025-2026, papers on subgoal-progress metrics that extend AgentBoard, recent
  ICLR 2026 / NeurIPS 2025 work on agent annotation that follows the "Solving the Granularity
  Mismatch" thread.

Pick one option in the planning step and record the choice in `plan/plan.md`. Do NOT silently skip
the survey or silently re-add the existing papers.

## Existing Paper Coverage (from t0017)

The 10 papers in the user's request map to existing paper assets as follows:

| Theme | Paper | Existing paper_id (added by t0017) |
| --- | --- | --- |
| Hierarchical / granularity-aware | "Solving the Granularity Mismatch" (ICLR 2026) | `no-doi_Gao2026_hierarchical-preference-learning-llm-agents` |
| Hierarchical / granularity-aware | ArCHer (ICML 2024) | `10.48550_arXiv.2402.19446` |
| Hierarchical / granularity-aware | "Reinforcing LLM Agents via Policy Optimization with Action Decomposition" (NeurIPS 2024) | `10.48550_arXiv.2405.15821` |
| Search and planning | "Can Graph Learning Improve Planning in LLM-based Agents?" (NeurIPS 2024) | `10.48550_arXiv.2405.19119` |
| Search and planning | LATS: Language Agent Tree Search (ICML 2024) | `10.48550_arXiv.2310.04406` |
| Reasoning structure | SELF-DISCOVER (NeurIPS 2024) | `10.48550_arXiv.2402.03620` |
| Agent benchmarks | Embodied Agent Interface (NeurIPS 2024) | `10.48550_arXiv.2410.07166` |
| Agent benchmarks | AgentBoard (NeurIPS 2024 D&B) | `10.48550_arXiv.2401.13178` |
| LLM-as-judge | "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement" | `10.48550_arXiv.2407.18370` |
| Theory anchor | Sutton, Precup & Singh 1999 "Between MDPs and Semi-MDPs" | `no-doi_Sutton1999_options-framework` |

The planning step should `aggregate_papers --ids ...` against this list to confirm each asset is
intact (download_status, summary present) before deciding the re-scoping option.

## Themes (User-Provided Grouping)

* **Hierarchical / granularity-aware agents**: papers 1, 2, 3, 10 above (rows 1-3 + 10).
* **Search and planning structure**: papers 4, 5 (rows 4-5).
* **Reasoning structure discovery**: paper 6 (row 6).
* **Agent benchmarks**: papers 7, 8 (rows 7-8).
* **LLM-as-judge methodology**: paper 9 (row 9).

## Approach

### If Option A is chosen at planning time

1. Run `aggregate_papers --ids <all 10 ids>` and confirm every paper asset has
   `download_status: "success"` and a non-trivial summary document. Flag and re-summarize any paper
   that t0017 left in `download_status: "failed"`.
2. Write `results/results_summary.md` as a **v2 synthesis** (not a list of summaries) organized
   around three project pain points:
   * **A.1 — v3 scope conditioning prompts**: cite ArCHer, "Solving the Granularity Mismatch",
     "Action Decomposition", and the Sutton options-framework theory paper to extract concrete
     prompt-design recommendations for variant A vs C in the next experiment iteration.
   * **A.2 — v3 calibration**: cite "Trust or Escalate" + AgentBoard + Embodied Agent Interface
     (subgoal-progress framing) to extract concrete recommendations for the `final_confidence`
     prompt and for the 10-bin ECE reporting in the next iteration.
   * **A.3 — v3 judge design**: cite "Trust or Escalate" provable-guarantee framework, contrast with
     t0019's substantive-critic + model-rotation approach, and recommend whether to add escalation
     thresholds in the v3 judge.
3. File a correction (under `tasks/t0027_.../corrections/`) that updates `task.json`
   `expected_assets` to `{}` and updates the `short_description` to "Synthesis-only re-scope".
4. Do NOT add any paper assets under `tasks/t0027_.../assets/paper/`.

### If Option B is chosen at planning time

1. Spend a small budget (~1-2 hours of agent time) discovering 10 additional 2024-2026 papers on the
   same themes that t0017 missed. Use `aggregate_papers --format ids` to filter out duplicates.
2. For each new paper, follow the `/add-paper` skill: download (where possible), produce
   `details.json` and the canonical summary, run `verify_paper_asset`.
3. Produce `results/results_summary.md` as a **delta synthesis** that explains how the 10 new papers
   extend or correct the t0017 coverage on the five themes above.

## Expected Outputs

* `plan/plan.md` — planning step records the Option A/B choice with rationale.
* `results/results_summary.md` — synthesis document organized around v3 prompt design, v3
  calibration, and v3 judge design (Option A) or thematic delta over t0017 (Option B).
* `results/results_detailed.md` — per-paper notes that go beyond what t0017 already wrote.
* `assets/paper/*` — 0 papers (Option A, after correction) or 10 NEW papers (Option B). NEVER re-add
  the 10 listed papers; that would duplicate t0017's assets.
* `results/metrics.json` — empty `{}` is acceptable; literature surveys do not register quantitative
  metrics.
* `results/suggestions.json` — at least 3 suggestions for v3 experiment design that reference the
  surveyed papers explicitly.
* `results/costs.json` — track any internet/Anthropic API spend.

## Cost and Compute

* **Option A (synthesis only)**: under $5 — only LLM calls are for synthesis writing and reading.
* **Option B (10 additional papers)**: $20-40 — driven by paper search, download, and per-paper
  summary generation.
* No remote machines required either way.

## Dependencies

This task depends on `t0017_literature_hierarchical_agents_and_judges` because it reads paper assets
that `t0017` produced. No code dependencies. No data-pipeline dependencies.

## Verification

* The chosen option (A or B) is recorded in `plan/plan.md` with rationale.
* Every paper referenced in `results/results_summary.md` has a corresponding paper asset in either
  `t0017` (Option A) or `t0027` (Option B) — never fabricated.
* `verify_research_papers` (if applicable) and `verify_paper_asset` (Option B only) report zero
  errors.
* The v2 synthesis goes beyond `t0017`'s synthesis by anchoring every cited paper to a concrete
  next-iteration design recommendation. A reviewer reading only `results_summary.md` should be able
  to write the v3 experiment plan without further reading.

## Cross-References

* **t0017** (paper coverage): the source of all 10 paper assets and the prior synthesis.
* **t0019** (judge calibration): defines the substantive-critic + model-rotation judge that v3 judge
  design will revise based on the "Trust or Escalate" recommendations.
* **t0022** (ABC harness): already adopts AgentBoard subgoal-progress and Embodied Agent Interface
  error taxonomy; the v2 synthesis should evaluate whether the harness needs further changes for v3.
* **t0026** (Phase 2 A/B/C runtime): the in-flight experiment whose RQ1-RQ5 outcomes will, together
  with this v2 synthesis, drive the v3 design.
