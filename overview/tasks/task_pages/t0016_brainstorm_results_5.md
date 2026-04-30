# ✅ Brainstorm session 5: prune backlog after t0014 deconfound

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0016_brainstorm_results_5` |
| **Status** | ✅ completed |
| **Started** | 2026-04-30T22:00:00Z |
| **Completed** | 2026-04-30T22:30:00Z |
| **Duration** | 30m |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0016_brainstorm_results_5/`](../../../tasks/t0016_brainstorm_results_5/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0016_brainstorm_results_5/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0016_brainstorm_results_5/task_description.md)*

# Brainstorm Session 5: Prune Backlog After t0014 Deconfound

## Context

Session 5 ran on 2026-04-30 immediately after `t0014_v2_annotator_sonnet_rerun` and
`t0015_correct_proxy_benchmark_labels` merged. `t0012_phase2_abc_smoke_frontierscience` is in
progress; this session deliberately does not perturb it.

## Headline Inputs

`t0014` decomposed t0009's published +58 pp v2-vs-v1 judge-accept-rate gain into a **+57 pp
schema-only** delta and a **−1 pp model-only** delta. The annotator-model swap from haiku to
sonnet contributes essentially zero of the gain; the v2 tree schema accounts for nearly all of
it. The +57 pp schema-only delta also bundles a truncation fix (v1 had a 1500-character
`task_excerpt` truncation that v2 removed), which `compare_literature.md` flags as a real
confound.

`t0015` wrote a single corrections-overlay file relabelling 52 of 115 v2 rows: 26 `m2w_*` rows
from `WorkArena++` to `Mind2Web`, and 26 `he_*` rows from `tau-bench` to `HumanEval`.

## Decisions

This session is pure backlog cleanup. No new tasks. No task cancellations. No task updates.
Only suggestion-status corrections.

### Reject (3)

* **S-0005-04** — superseded by t0015 (proxy benchmark naming corrected) and by the inline
  task_id de-duplication fix in t0009.
* **S-0005-05** — duplicate of S-0009-03 (single-blind human review with Cohen's kappa serves
  the same role).
* **S-0014-04** — this is a project-level decision, not a task. The +57 pp schema / −1 pp
  model split already establishes haiku-default as the right policy; recorded as project
  policy rather than executed as a task.

### Reprioritize (5)

* **S-0009-04** medium → **high** — the per-benchmark pattern in t0014 (+100 pp on long-input
  benchmarks vs +13–17 pp on short ones) is exactly what the truncation hypothesis predicts.
  Splitting the schema-only +57 pp into "tree shape" vs "no truncation" is now load-bearing
  for the science.
* **S-0002-09** medium → low — infrastructure chore (re-fetch 11 PDFs with git LFS); low
  signal for the science.
* **S-0006-02** medium → low — async ScopeAwareReactAgent is performance optimization, not
  science; Phase 2 does not need it.
* **S-0011-02** medium → low — provider-specific calibration prompt variants; Phase 2
  currently uses Anthropic only, so variant work is premature.
* **S-0014-05** medium → low — re-running 3 FrontierScience-Olympiad sonnet timeouts only
  recovers 3 rows; n=20 → 23 does not materially change Wilson CIs on the existing
  decomposition.

## Out of Scope

* Creating new tasks (deferred to session 6 once t0012 lands).
* Modifying t0012's in-progress state.
* Replacing the proxy rows with native WorkArena++ / tau-bench data (S-0015-01 remains active
  at medium priority for a future session).

## Outputs

* 8 correction files in `corrections/` against six prior tasks.
* No new suggestions.
* No new assets.
* Updated effective suggestion view: 3 fewer active, 5 with revised priority.

</details>

## Research

* [`research_code.md`](../../../tasks/t0016_brainstorm_results_5/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0016_brainstorm_results_5/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0016_brainstorm_results_5/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0016_brainstorm_results_5/results/results_summary.md)*

# Results Summary: t0016_brainstorm_results_5

## Summary

Brainstorm session 5 was a pure backlog cleanup pass after t0014 (v2 sonnet rerun deconfound)
and t0015 (proxy benchmark relabel) merged. Eight corrections were issued: three rejections,
five priority changes. No new tasks were created and no existing tasks were modified.

## Session Overview

* **Session number**: 5
* **Date**: 2026-04-30
* **Duration**: ~30 minutes
* **Mode**: Pure cleanup (no new tasks, no task updates)
* **Researcher budget envelope**: < $5 total (no API spend; planning only)

## Decisions

### Rejections (3)

| Suggestion | Source task | Rationale |
| --- | --- | --- |
| S-0005-04 | t0005 | Superseded by t0015 proxy-relabel; remaining concerns are aggregator cosmetics |
| S-0005-05 | t0005 | Duplicate of S-0009-03 (multi-judge agreement, post-v2 scope) |
| S-0014-04 | t0014 | "Adopt haiku-default" is policy, not a task |

### Reprioritizations (5)

| Suggestion | Source task | From | To | Rationale |
| --- | --- | --- | --- | --- |
| S-0009-04 | t0009 | medium | high | t0014 per-benchmark deltas match truncation-hypothesis prediction |
| S-0002-09 | t0002 | medium | low | LFS re-fetch is hygiene; not on research critical path |
| S-0006-02 | t0006 | medium | low | Async ReactAgent is engineering optimization |
| S-0011-02 | t0011 | medium | low | Sequenced behind v2-annotator stability and schema deconfound |
| S-0014-05 | t0014 | medium | low | Three missing rows do not change headline finding |

## Metrics

| Metric | Value |
| --- | --- |
| Suggestions reviewed | 35 |
| Suggestions rejected | 3 |
| Suggestions reprioritized | 5 |
| New tasks created | 0 |
| Tasks cancelled | 0 |
| Tasks updated | 0 |
| Correction files written | 8 |

## Verification

* `verify_corrections t0016_brainstorm_results_5` → PASSED, no errors or warnings
* `verify_task_file t0016_brainstorm_results_5` → see verification log
* `verify_suggestions t0016_brainstorm_results_5` → see verification log
* `verify_logs t0016_brainstorm_results_5` → see verification log

## Next Steps

After merge, the suggestion aggregator overlay will reflect:

* 3 fewer active suggestions (rejected entries)
* S-0009-04 visible as the highest-priority truncation/schema deconfound experiment
* 4 fewer medium-priority items (now low)

The next suggestions-chooser run should pick up S-0009-04 as the leading high-priority
experiment given the truncation confound flagged in t0014's compare_literature.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0016_brainstorm_results_5/results/results_detailed.md)*

# Results Detailed: t0016_brainstorm_results_5

## Summary

Brainstorm session 5 produced 8 correction files that update the aggregated suggestion
overlay: 3 rejections and 5 priority reassignments. The session was triggered by completion of
t0014 (deconfound experiment that showed schema dominates: +57pp vs model swap -1pp) and t0015
(proxy benchmark label correction). No new tasks were created — the active backlog already
covers the next research moves once t0012 (in-progress) lands.

## Methodology

* Session conducted via `/human-brainstorm` skill (v9)
* Project state aggregated via:
  * `aggregate_tasks --format json --detail short`
  * `aggregate_suggestions --format json --detail short --uncovered`
  * `aggregate_suggestions --format json --detail full --uncovered --priority high`
  * `aggregate_answers --format json --detail full`
  * `aggregate_costs --format json --detail short`
* Completed-task results read selectively for t0014 and t0015 (post-last-brainstorm tasks)
* Independent priority reassessment performed before presentation, per skill v9 step 8
* No remote machines used
* No API spend (pure planning task)
* Machine: local development environment, darwin/arm64
* Started: 2026-04-30T22:00:00Z (approximate; brainstorm phase began earlier in session)
* Completed: 2026-04-30T22:30:00Z

## Metrics

See `metrics.json` (`{}` — brainstorm tasks register no project-level metrics) and
`results_summary.md` for the qualitative metrics table.

| Decision metric | Count |
| --- | --- |
| Suggestions reviewed | 35 |
| Rejected | 3 |
| Reprioritized to high | 1 |
| Reprioritized to low | 4 |
| Net active-suggestion change | -3 |
| Correction files written | 8 |

## Decision Detail

### Rejections

**S-0005-04 — Remediate proxy benchmark naming and task_id non-uniqueness**: t0015 already
corrected the 52 mislabeled rows via the corrections-overlay mechanism. The remaining concerns
are aggregator-side cosmetics (display names, task_id collisions) that do not warrant a
dedicated task.

**S-0005-05 — Multi-judge disagreement study on hierarchical annotation**: Duplicate of
S-0009-03, which proposes the same study with current (post-v2) scope. Keeping a single
canonical suggestion prevents backlog drift; the v1-era version is rejected in favor of the v2
successor.

**S-0014-04 — Adopt haiku-default annotation policy for Phase 2**: Standing project decision,
not a task or asset. The empirical basis (model swap = -1pp, schema swap = +57pp) is
established by t0014; the policy is implicit in current task plans.

### Reprioritizations

**S-0009-04 (medium → high) — Tree-schema-with-truncated-text ablation**: t0014's
per-benchmark deltas (+100pp on long-input benchmarks vs +13-17pp on short ones) are exactly
the pattern the truncation hypothesis predicts. This deconfound is now load-bearing for
interpreting the v1->v2 headline.

**S-0002-09 (medium → low) — Re-fetch paper PDFs with git LFS**: Hygiene work, not on the
research critical path. Active annotation/eval lines work from abstracts and existing
summaries.

**S-0006-02 (medium → low) — Async ScopeAwareReactAgent variant**: Engineering optimization.
Not on the critical path until throughput becomes a measured bottleneck.

**S-0011-02 (medium → low) — Provider-specific calibration prompt variants**: Downstream of
stable v2-annotator results across the full proxy benchmark. With t0012 in-progress and
S-0009-04 now high, this is sequenced later.

**S-0014-05 (medium → low) — Re-run three FrontierScience-Olympiad sonnet timeouts**:
Bookkeeping that does not change the headline finding. Existing 52/55 row coverage already
supports the result.

## Limitations

* Priority changes update aggregated overlay; they do not move work into the chooser queue
  automatically
* No new tasks means t0014's truncation-confound flag remains unresolved until S-0009-04 is
  picked up by the next chooser run
* t0012 is still in_progress; this brainstorm intentionally avoided perturbing its inputs

## Files Created

| Path | Purpose |
| --- | --- |
| `task.json` | Task metadata (status: completed, 14 dependencies) |
| `task_description.md` | Long-form session description |
| `step_tracker.json` | 4 steps, all completed |
| `plan/plan.md` | Standard plan sections (planning-only task) |
| `research/research_papers.md` | Standard sections, no research required |
| `research/research_internet.md` | Standard sections, no research required |
| `research/research_code.md` | Standard sections, no research required |
| `corrections/suggestion_S-0005-04.json` | Reject: superseded by t0015 |
| `corrections/suggestion_S-0005-05.json` | Reject: duplicate of S-0009-03 |
| `corrections/suggestion_S-0014-04.json` | Reject: policy, not a task |
| `corrections/suggestion_S-0009-04.json` | Reprioritize: medium → high |
| `corrections/suggestion_S-0002-09.json` | Reprioritize: medium → low |
| `corrections/suggestion_S-0006-02.json` | Reprioritize: medium → low |
| `corrections/suggestion_S-0011-02.json` | Reprioritize: medium → low |
| `corrections/suggestion_S-0014-05.json` | Reprioritize: medium → low |
| `results/results_summary.md` | This file's compact counterpart |
| `results/results_detailed.md` | This file |
| `results/metrics.json` | `{}` (brainstorm tasks have no project metrics) |
| `results/costs.json` | Zero spend |
| `results/remote_machines_used.json` | `[]` |
| `results/suggestions.json` | `[]` (no new suggestions) |
| `logs/session_log.md` | Session transcript and capture |
| `logs/steps/001_review-project-state/step_log.md` | Phase 1 log |
| `logs/steps/002_discuss-decisions/step_log.md` | Phase 2 log |
| `logs/steps/003_apply-decisions/step_log.md` | Phase 5 log |
| `logs/steps/004_finalize/step_log.md` | Phase 6 log |

## Verification

Each verificator was run as the final gate before PR creation:

* `uv run python -u -m arf.scripts.verificators.verify_task_file t0016_brainstorm_results_5`
* `uv run python -u -m arf.scripts.verificators.verify_corrections t0016_brainstorm_results_5`
* `uv run python -u -m arf.scripts.verificators.verify_suggestions t0016_brainstorm_results_5`
* `uv run python -u -m arf.scripts.verificators.verify_logs t0016_brainstorm_results_5`

All passed before PR submission. The pre-merge verificator was run after PR creation.

## Next Steps

After merge, the next suggestions-chooser run should surface S-0009-04 as the highest-priority
remaining experiment. The truncation/schema deconfound is the next research-question-advancing
move; t0012 (Phase 2 ABC smoke test) continues independently in its own branch.

</details>
