# ✅ Literature: Hierarchical Agents and LLM-as-Judge

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0017_literature_hierarchical_agents_and_judges` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T00:00:00Z |
| **Completed** | 2026-05-01T01:40:00Z |
| **Duration** | 1h 40m |
| **Task types** | `literature-survey` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`granularity-conditioning`](../../by-category/granularity-conditioning.md), [`hierarchical-planning`](../../by-category/hierarchical-planning.md), [`uncertainty-calibration`](../../by-category/uncertainty-calibration.md) |
| **Expected assets** | 10 paper |
| **Step progress** | 3/3 |
| **Task folder** | [`t0017_literature_hierarchical_agents_and_judges/`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/task_description.md)*

# Literature: Hierarchical Agents and LLM-as-Judge

## Motivation

The post-t0014 state of this project leaves several open questions that the existing
literature likely speaks to directly:

* The v2 schema win demonstrated that *annotation granularity* matters far more than the
  annotator model swap. Recent work on hierarchical / granularity-aware agents in RL and
  preference learning is the closest external analogue.
* Open suggestions about multi-judge agreement studies (S-0009-03) and calibration of LLM
  judges call for a direct read of the "Trust or Escalate" line of work on judges with
  provable agreement guarantees.
* Several agent-evaluation suggestions in the backlog target benchmarks we have not yet
  adopted; AgentBoard and Embodied Agent Interface are the canonical references to compare
  against.
* A short theory anchor in the options framework (Sutton, Precup & Singh 1999) is useful as
  the foundational reference for any hierarchical-action discussion in our own writing.

This task is a focused, single-pass literature survey: download, read, and summarize a curated
set of ten papers as paper assets, then stop. It is *not* an experiment, baseline, or
brainstorm — its only deliverable is the ten paper assets and a brief synthesis in
`results_detailed.md`.

## Scope

Add the following ten papers as paper assets under `assets/paper/<paper_id>/`, each with
`details.json`, the canonical summary document, and the downloaded file (or a documented
download failure):

### Hierarchical / granularity-aware agents

* P1: *Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
  Agents* — ICLR 2026.
* P2: *ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL* — ICML 2024.
* P3: *Reinforcing LLM Agents via Policy Optimization with Action Decomposition* — NeurIPS
  2024.
* P10: *Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement
  Learning* — Sutton, Precup & Singh, Artificial Intelligence 1999. Theory anchor for the
  options framework; a brief summary is sufficient.

### Search and planning structure

* P4: *Can Graph Learning Improve Planning in LLM-based Agents?* — NeurIPS 2024.
* P5: *LATS: Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language
  Models* — ICML 2024.

### Reasoning structure discovery

* P6: *SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures* — NeurIPS 2024.

### Agent benchmarks

* P7: *Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making* — NeurIPS
  2024.
* P8: *AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents* — NeurIPS 2024
  Datasets and Benchmarks.

### LLM-as-judge methodology

* P9: *Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement*.

## Approach

The task uses the standard `/add-paper` skill once per paper. For each paper:

* Resolve identity (DOI or arXiv ID), check no duplicate already exists in the project, gather
  full metadata (CrossRef + Semantic Scholar + OpenAlex), download the PDF, write
  `details.json`, read the paper, and write the canonical summary document with all nine
  mandatory sections.
* When download fails (paywall, no public version), still produce metadata and an
  abstract-based summary, with `download_status: "failed"` and a populated
  `download_failure_reason`.
* Run the paper-asset verificator after each addition.

After all ten papers are added, write a brief synthesis (`results_detailed.md`) grouping
findings by the five themes above and identifying which suggestions in our backlog the survey
strengthens or weakens. The synthesis should be at most one page; this task is not a
meta-review.

## Expected Outputs

* `assets/paper/<paper_id>/` for each of the ten papers, passing `verify_paper_asset.py` with
  zero errors.
* `results/results_summary.md` and `results/results_detailed.md` — a short synthesis grouped
  by theme, with explicit pointers to the suggestions and prior tasks each paper informs.
* `results/suggestions.json` containing any new suggestions that emerge from the reading
  (likely experiment ideas connecting hierarchical-RL findings to our annotation/calibration
  agenda).

## Compute and Budget

No GPU compute. Costs are limited to API calls during paper download (CrossRef, Semantic
Scholar, OpenAlex are free) and any LLM-assisted summarization that runs through the standard
agent context — well under \$5 total.

## Dependencies

None. Literature surveys are independent and should run in isolation. The task does not block
on any in-flight work.

## Risks and Fallbacks

* *Paper unavailable for download* — proceed with abstract-based summary per the paper-asset
  specification. This is acceptable for at most two of the ten; if more fail, escalate to the
  researcher rather than producing many low-quality summaries.
* *DOI mismatch or duplicate detection* — if a paper is already in the project, skip it and
  note the existing `paper_id` in the synthesis.

## Verification Criteria

* `assets/paper/` contains exactly ten subfolders, each passing `verify_paper_asset.py`.
* Every paper asset has `summary_path` populated and the canonical summary document contains
  all nine mandatory sections.
* `results/results_detailed.md` references each of the ten papers by `citation_key` at least
  once.
* `results/suggestions.json` is valid even if empty (`{"suggestions": []}`).

## Cross-References

* **Source suggestion** — none. This task originates from the t0016 brainstorm follow-up,
  where the researcher requested a focused read on this slice of the literature.
* **Prior tasks whose findings this informs** — t0009 (hierarchical annotation v2), t0014 (v2
  annotator sonnet rerun), t0012 (phase-2 ABC smoke), and the open suggestions S-0009-03
  (multi- judge agreement) and S-0009-04 (truncation/schema deconfound).

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| paper | [Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2310.04406/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2310.04406/summary.md) |
| paper | [AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2401.13178/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2401.13178/summary.md) |
| paper | [SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.03620/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.03620/summary.md) |
| paper | [ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.19446/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.19446/summary.md) |
| paper | [Reinforcing Language Agents via Policy Optimization with Action Decomposition](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.15821/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.15821/summary.md) |
| paper | [Can Graph Learning Improve Planning in LLM-based Agents?](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.19119/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.19119/summary.md) |
| paper | [Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2407.18370/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2407.18370/summary.md) |
| paper | [Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2410.07166/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2410.07166/summary.md) |
| paper | [Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/no-doi_Gao2026_hierarchical-preference-learning-llm-agents/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/no-doi_Gao2026_hierarchical-preference-learning-llm-agents/summary.md) |
| paper | [Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement learning](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/no-doi_Sutton1999_options-framework/) | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/no-doi_Sutton1999_options-framework/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Adopt Trust-or-Escalate selective evaluation for the multi-judge
agreement study</strong> (S-0017-01)</summary>

**Kind**: evaluation | **Priority**: high

S-0009-03 calls for a multi-judge agreement study; Jung2024 ("Trust or Escalate", ICLR 2025)
provides the right primitive. Implement a selective-judging pipeline with two ingredients: (1)
Simulated Annotators on top of the project's existing judge LLM to produce ensemble-based
confidence scores, and (2) a calibrated abstention threshold using fixed-sequence testing
(Bauer 1991, Bates et al. 2021) so the pipeline ships with a finite-sample, distribution-free
guarantee on human-judge agreement. Empirically Jung2024 shows that 75% of pairwise judging on
ChatArena can be delegated to Mistral-7B/GPT-3.5 while preserving an 80% human-agreement floor
that GPT-4 alone never reaches, so this is also a cost-reduction path for any large-scale
annotation rerun. Deliverable: a small library that wraps the existing judge call with
confidence + abstain semantics, exposed to t0009-style annotation tasks.

</details>

<details>
<summary><strong>Adopt AgentBoard progress-rate metric and EAI error taxonomy in
the next ABC-condition run</strong> (S-0017-02)</summary>

**Kind**: evaluation | **Priority**: medium

t0012's smoke showed that all three ABC conditions hit the floor on FrontierScience-Olympiad
with claude-haiku-4-5 (A: 2.5%, B: 0%, C: 0%), so binary task success cannot distinguish the
conditions. Ma2024 (AgentBoard, NeurIPS 2024 D&B) defines a subgoal-coverage "progress rate"
with Pearson rho > 0.95 against humans across 1013 environments; Li2024 (Embodied Agent
Interface, NeurIPS 2024) defines a fine-grained error taxonomy (hallucination, affordance,
missing/extra/wrong-order steps, precondition/effect errors) that attributes failures to
specific modes. Adopt both: progress rate becomes a stronger Metric 1 candidate than binary
success, and the EAI taxonomy becomes the per-row diagnostic when scope-aware (A) and
scope-mismatched (C) conditions diverge. This is a precondition for S-0012-02 (sonnet
confirmatory run) producing legible results. Estimated effort: 1-2 days of
metric-implementation work.

</details>

<details>
<summary><strong>Use SELF-DISCOVER reasoning scaffolds as the scope-aware (A)
condition prompt template</strong> (S-0017-03)</summary>

**Kind**: technique | **Priority**: medium

Zhou2024b (SELF-DISCOVER, NeurIPS 2024) shows that a task-conditioned reasoning structure --
selected from atomic reasoning modules and composed once per task type, then re-used across
instances -- transfers across model families and outperforms CoT-Self-Consistency at 10-40x
lower inference cost. The IMPLEMENT step (explicit JSON key-value scaffold) is the largest
ablation contributor. This is a near-zero-cost upgrade to our scope-aware (A) condition
prompt: produce one SELF-DISCOVER structure per benchmark family (FrontierScience-Olympiad,
SWE-bench Verified, tau-bench, WorkArena++), then re-use it across all rows of that family.
Predicts a measurable improvement on RQ1/RQ5 even without re-running annotation. Out of scope:
any retraining; this is purely a prompting change.

</details>

## Research

* [`research_code.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/results/results_summary.md)*

# Results Summary: Literature Survey on Hierarchical Agents and LLM-as-Judge

## Summary

Completed a literature survey of ten papers covering hierarchical / granularity-aware LLM
agents, search-and-planning structure, reasoning-structure discovery, agent benchmarks, and
LLM-as-judge methodology — plus the foundational options-framework paper (Sutton 1999) as a
brief theory anchor. All ten paper assets pass the v3 paper-asset verificator with zero errors
and zero warnings. The synthesis below groups findings by the five themes defined in
`task_description.md` and identifies which backlog suggestions and prior tasks the survey
strengthens or weakens.

## Metrics

* **10 paper assets created** out of a 10-paper target — meets `expected_assets.paper = 10`
  exactly.
* **5 of 5 themes covered** with at least 1 paper each: hierarchical / granularity-aware
  agents (4 papers — Gao2026, Zhou2024, Wen2024, Sutton1999), search and planning structure (2
  papers — Wu2024, Zhou2024a), reasoning-structure discovery (1 paper — Zhou2024b), agent
  benchmarks (2 papers — Li2024, Ma2024), LLM-as-judge methodology (1 paper — Jung2024).
* **0 errors and 0 warnings** across 10 verifier runs after the initial PA-W005 cleanup on
  `Zhou2024b` invented category slugs.
* **3 new follow-up suggestions** drafted (S-0017-01, S-0017-02, S-0017-03), all tied to
  existing backlog items.

## Headline Synthesis

* **Granularity is a first-class research lever, not an annotation detail.** Three modern
  papers (`Gao2026`, `Zhou2024` ArCHer, `Wen2024`) and one foundational paper (`Sutton1999`)
  all argue independently that mid-granularity action units beat both pure trajectory-level
  and pure token-level signals on long-horizon agent tasks. This *strengthens* the central
  claim of t0009 (hierarchical annotation v2) and the v2 schema win observed in t0014.
* **Hierarchical agents have a single formal foundation.** `Sutton1999` gives the options /
  semi-MDP framework that subsumes `Zhou2024` (utterance-level critic + token-level actor) and
  `Wen2024` (intra-action `gamma_w = 1` keeps token-level updates consistent with the original
  MDP). Use the options framework as the theory anchor in any project paper that justifies
  scope-aware (A) vs scope-mismatched (C) conditioning.
* **Selective LLM-as-judge with calibration thresholds is the right primitive for our judge
  pipeline.** `Jung2024` ("Trust or Escalate") provides distribution-free, finite-sample
  guarantees on human-judge agreement and shows that 75% of pairwise judging on ChatArena can
  be delegated to Mistral-7B/GPT-3.5 while preserving an 80% human-agreement floor. This
  *strengthens* S-0009-03 (multi-judge agreement study) and gives us a concrete recipe for
  cost-bounded judge cascades.

## Theme 1: Hierarchical / Granularity-Aware Agents (P1, P2, P3, P10)

* `Gao2026` (HPL, ICLR 2026) introduces hierarchical preference learning over LLM-clustered
  sub- task action groups; the bias-variance argument (Proposition 1) gives a principled
  reason to prefer mid-granularity signals when reward sparsity and trajectory length are
  large. Directly validates t0009's three-level (global / subtask / atomic) annotation schema.
* `Zhou2024` (ArCHer, ICML 2024) demonstrates hierarchical multi-turn RL with an
  utterance-level off-policy critic and a token-level on-policy actor; gains scale with model
  size from 100M to 7B parameters.
* `Wen2024` (POAD with BAD, NeurIPS 2024) formalises the right way to do token-level credit
  assignment under free-form action spaces: keep `gamma_w = 1` inside an action so the
  token-level update is consistent with the original MDP. Drops complexity from `O(|V|^|a|)`
  to `O(|a|*|V|)`.
* `Sutton1999` provides the SMDP / options framework that all three papers above implicitly
  use. The theory anchor enables our writing to reason about A/B/C conditions as different
  option-set policies over the same underlying MDP.

## Theme 2: Search and Planning Structure (P4, P5)

* `Wu2024` (NeurIPS 2024) reframes LLM-agent planning as graph decision-making, shows that
  even a parameter-free 1-hop SGC step over sentence embeddings beats most prompting
  baselines, and reduces hallucination from >20% to <1% by restricting the candidate set to
  actual graph nodes. Provides a strong "guardrail" template for any subtask-decomposition
  agent we build downstream.
* `Zhou2024a` (LATS, ICML 2024) unifies tree search with LM-as-judge value functions and
  verbal self-reflection. Tree search expands fewer nodes than alternatives (3.55 fewer than
  RAP, 12.12 fewer than ToT on HotPotQA) at higher accuracy. Useful as a strong planning
  baseline for scope-aware (A) condition agents in this project.

## Theme 3: Reasoning Structure Discovery (P6)

* `Zhou2024b` (SELF-DISCOVER, NeurIPS 2024) shows that **structure (what to think about) beats
  wording (what words to use)** for transfer across model families. The IMPLEMENT step
  (explicit JSON key-value scaffold) is the largest single contributor in ablations, beyond
  mere module selection. Gives a concrete prompting template for the scope-aware condition
  that does not require any retraining.

## Theme 4: Agent Benchmarks (P7, P8)

* `Li2024` (Embodied Agent Interface, NeurIPS 2024) decomposes embodied planning into four
  modules (goal interpretation / subgoal decomposition / action sequencing / transition
  modeling) and provides a fine-grained error taxonomy (hallucination, affordance,
  missing/extra/wrong-order steps, precondition/effect errors). The taxonomy is directly
  applicable to our scope-aware vs scope-mismatched condition diagnostics.
* `Ma2024` (AgentBoard, NeurIPS 2024 D&B) defines a "progress rate" that generalises to our
  three hierarchy levels and demonstrates large-scale subgoal annotation methodology (1013
  environments, Pearson rho > 0.95 against humans). The hard/easy split based on subgoal count
  and the six-dimensional sub-skill scoring are templates we should adopt for stratifying our
  results.

## Theme 5: LLM-as-Judge Methodology (P9)

* `Jung2024` (Trust or Escalate, ICLR 2025 Oral) introduces selective LLM judging with
  calibrated thresholds and distribution-free guarantees on human agreement. Simulated
  Annotators (ensemble-based confidence on top of any judge LLM) and judge cascades (route by
  confidence, escalate only when needed) are drop-in techniques that our calibration agenda
  can apply immediately.

## Pointers Back to Backlog Suggestions and Prior Tasks

* **t0009 (hierarchical annotation v2)** — *strengthened* by P1, P2, P3, P10 and reinforced by
  P7, P8. The granularity-mismatch argument is now backed by ICLR 2026, ICML 2024, NeurIPS
  2024, and the foundational AIJ 1999 paper.
* **t0014 (v2 annotator sonnet rerun)** — *strengthened* by P1's bias-variance argument: the
  v2 schema win demonstrates exactly the predicted advantage of mid-granularity over
  trajectory-level signals.
* **t0012 (phase-2 ABC smoke)** — *informed* by P10: the A/B/C conditions are best framed as
  different option-set policies over the same underlying MDP. P7 and P8 give error-taxonomy
  and progress-rate templates that should be adopted before scaling phase-2 beyond the smoke
  test.
* **S-0009-03 (multi-judge agreement)** — *strengthened* by P9. The Trust-or-Escalate
  selective evaluation framework directly addresses the calibration question.
* **S-0009-04 (truncation/schema deconfound)** — *informed* (not directly strengthened or
  weakened): P1, P2, P3, P10 imply the schema effect is not just truncation; the granularity-
  mismatch effect is real even at full context. Worth re-reading P1's bias-variance analysis
  when designing the deconfound experiment.

## Verification

* `assets/paper/` contains exactly ten subfolders.
* All ten paper-asset folders pass `meta.asset_types.paper.verificator` with zero errors and
  zero warnings.
* Each paper has `summary_path: "summary.md"` populated and a canonical summary covering all
  nine mandatory sections.
* `results/results_detailed.md` references every paper by `citation_key`.
* `results/suggestions.json` is valid (one new suggestion proposed, see below).

## Files Created

* Ten paper-asset folders under `assets/paper/`.
* `plan/plan.md`, `research/research_*.md`, `step_tracker.json`, `logs/session_log.md`,
  `logs/steps/{001_research,002_analysis,003_reporting}/step_log.md`.
* `results/{results_summary.md,results_detailed.md,metrics.json,suggestions.json,costs.json,
  remote_machines_used.json}`.

## Next Steps and Suggestions

* Adopt `Ma2024`'s progress-rate metric and `Li2024`'s error taxonomy in the next iteration of
  the ABC-condition smoke (see `results/suggestions.json` for the formal entry).
* Adopt `Jung2024`'s selective-evaluation framework as the first concrete step on S-0009-03.
* Cite `Sutton1999` as the theory anchor in any future write-up that motivates the scope-aware
  / scope-mismatched distinction.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0017_literature_hierarchical_agents_and_judges"
date_completed: "2026-05-01" status: "complete" ---
# Detailed Results: Literature Survey on Hierarchical Agents and LLM-as-Judge

## Summary

This file extends `results_summary.md` with one paragraph per paper plus an at-a-glance table.
Each paper is referenced by its `citation_key` from `details.json`. The synthesis grouped by
five themes is in `results/results_summary.md`. This detailed file documents the methodology,
the per-theme paper notes, the backlog mapping, the verificator outcomes, the limitations of
the abstract-and-text-based summarisation approach, and the files created.

## Methodology

* **Machine**: local macOS workstation, no remote compute.
* **Runtime**: about 100 minutes wall clock for the full task (research, analysis, reporting).
  Step 1 (research) ran 60 minutes with ten parallel `/add-paper` agents; step 2 (analysis)
  ran 20 minutes; step 3 (reporting) ran 20 minutes.
* **Timestamps**: task started `2026-05-01T00:00:00Z`, ended `2026-05-01T01:40:00Z`.
* **Tooling**: `/add-paper` skill (×10 in parallel) drove identity resolution (CrossRef +
  Semantic Scholar + OpenAlex + arXiv), PDF download, `details.json` generation, and
  nine-section summary writing. `meta.asset_types.paper.verificator` was run once per paper.
* **Cost**: $0.00 spent during the task. The metadata APIs are free; PDF downloads have no
  marginal cost beyond agent time. No paid LLM API or remote GPU was used.

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

* **`Gao2026`** introduces hierarchical preference learning (HPL) with mid-granularity
  sub-task groups identified by an LLM, plus a curriculum that starts with short, high-margin
  pairs and progresses to long, low-margin ones. Proposition 1's bias-variance argument is the
  cleanest theoretical justification we have for preferring mid-granularity signals on
  long-horizon tasks with sparse rewards. Strengthens t0009 and t0014.
* **`Zhou2024` (ArCHer)** decomposes multi-turn LLM-agent RL into an off-policy
  utterance-level critic and an on-policy token-level actor. Hierarchical decomposition scales
  with model size (100M -> 7B), evidence that hierarchical RL is not a small-model trick.
* **`Wen2024` (POAD with BAD)** establishes the correct way to do token-level credit
  assignment in free-form action spaces: keep `gamma_w = 1` inside an action so the
  token-level update is consistent with the original MDP. Reduces complexity from `O(|V|^|a|)`
  to `O(|a|*|V|)`. The discrepancy between action-level and naive token-level optimisation
  grows with action length, which is directly relevant to our scope-aware vs scope-mismatched
  conditions.
* **`Sutton1999`** is the theory anchor. Options as `<I, pi, beta>` triples + the SMDP
  equivalence + interruption + subgoal pseudo-rewards all map directly onto our project's
  three-level hierarchy and ABC condition design.

### Theme 2: Search and Planning Structure

* **`Wu2024`** reframes LLM-agent planning as graph decision-making (path or subgraph
  selection). A parameter-free 1-hop SGC step over sentence embeddings already beats most
  prompting baselines; a small trained GraphSAGE adds another large jump for 3-15 minutes of
  GPU time. Restricting candidates to graph nodes drops hallucination rate from >20% to <1%.
* **`Zhou2024a` (LATS)** unifies MCTS, ReAct, and Reflexion with LM-as-judge value functions
  and verbal self-reflection. Achieves higher accuracy than alternatives while expanding fewer
  nodes (3.55 fewer than RAP, 12.12 fewer than ToT on HotPotQA). Useful as a strong planning
  baseline for the scope-aware (A) condition.

### Theme 3: Reasoning Structure Discovery

* **`Zhou2024b` (SELF-DISCOVER)** lets the LLM compose atomic reasoning modules into an
  explicit task-conditioned reasoning structure that is then re-used across instances of the
  same task. Improves GPT-4 and PaLM 2 by up to 32% on BigBench-Hard, agent reasoning, and
  MATH versus CoT, while requiring 10-40x fewer inference compute than CoT-Self-Consistency.
  Discovered structures transfer cleanly across model families, suggesting "what to think
  about" is a more portable abstraction than "what words to use".

### Theme 4: Agent Benchmarks

* **`Li2024` (EAI)** decomposes embodied planning into goal interpretation, subgoal
  decomposition, action sequencing, and transition modeling, and reports a fine-grained error
  taxonomy (hallucination, affordance, missing/extra/wrong-order steps, precondition/effect
  errors). The taxonomy is the strongest direct template for our ABC-condition diagnostics.
  EAI also shows test-time reasoning (o1-style) gives more embodied-planning quality than
  additional parameters on these benchmarks.
* **`Ma2024` (AgentBoard)** introduces "progress rate" as a single comparable scalar across
  benchmarks, with subgoal-level annotation across 1013 environments (Pearson rho > 0.95 vs
  humans). Demonstrates a hard/easy split based on subgoal count, six-dimensional sub-skill
  scoring, and that open-weight models plateau at about 6 steps - all directly relevant to our
  benchmark stratification choices.

### Theme 5: LLM-as-Judge Methodology

* **`Jung2024` (Trust or Escalate)** introduces selective LLM judging with calibrated
  thresholds and finite-sample, distribution-free guarantees on human agreement. Simulated
  Annotators is a drop-in ensemble-based confidence estimator that works on top of any judge
  LLM, and judge cascades convert "model choice" into "abstention policy". Empirically, 75% of
  pairwise judging on ChatArena can be handled by Mistral-7B or GPT-3.5 while preserving an
  80% human-agreement floor that GPT-4 alone never reaches. Directly strengthens S-0009-03.

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

* **Mixed-source summaries**: Eight of ten paper summaries were written from the full PDF
  content via `pypdf` extraction; one (`Sutton1999`) was sourced from a public university
  course mirror and summarised from full text; one (`Gao2026`) is the latest ICLR 2026
  accepted paper and was summarised from the camera-ready PDF available on OpenReview. All ten
  summaries are based on full-paper content, not abstracts only — this is a stronger evidence
  base than t0002's abstract-only summaries.
* **Two non-DOI papers**: `Sutton1999` uses the `no-doi_` fallback because its DOI contains
  parentheses that the canonical `doi_to_slug` utility rejects; `Gao2026` uses the `no-doi_`
  fallback because the paper has no registered DOI yet. Both cases are explicit in the v3
  paper specification.
* **Survey scope is bounded**: Only ten papers were added; a follow-up task could extend to
  inverse- RL judges, judge ensembles beyond `Jung2024`, and additional embodied-agent
  benchmarks beyond `Li2024` and `Ma2024`.
* **No quantitative benchmark**: This is a literature-survey task; there are no project-level
  metrics (`metrics.json` is `{}` and `costs.json` reports $0.00). Quantitative validation of
  any synthesis claim is the responsibility of follow-up experimental tasks (S-0017-01..03).

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

</details>
