# Brainstorm Session 5: Prune Backlog After t0014 Deconfound

## Context

Session 5 ran on 2026-04-30 immediately after `t0014_v2_annotator_sonnet_rerun` and
`t0015_correct_proxy_benchmark_labels` merged. `t0012_phase2_abc_smoke_frontierscience` is in
progress; this session deliberately does not perturb it.

## Headline Inputs

`t0014` decomposed t0009's published +58 pp v2-vs-v1 judge-accept-rate gain into a **+57 pp
schema-only** delta and a **−1 pp model-only** delta. The annotator-model swap from haiku to sonnet
contributes essentially zero of the gain; the v2 tree schema accounts for nearly all of it. The +57
pp schema-only delta also bundles a truncation fix (v1 had a 1500-character `task_excerpt`
truncation that v2 removed), which `compare_literature.md` flags as a real confound.

`t0015` wrote a single corrections-overlay file relabelling 52 of 115 v2 rows: 26 `m2w_*` rows from
`WorkArena++` to `Mind2Web`, and 26 `he_*` rows from `tau-bench` to `HumanEval`.

## Decisions

This session is pure backlog cleanup. No new tasks. No task cancellations. No task updates. Only
suggestion-status corrections.

### Reject (3)

* **S-0005-04** — superseded by t0015 (proxy benchmark naming corrected) and by the inline task_id
  de-duplication fix in t0009.
* **S-0005-05** — duplicate of S-0009-03 (single-blind human review with Cohen's kappa serves the
  same role).
* **S-0014-04** — this is a project-level decision, not a task. The +57 pp schema / −1 pp model
  split already establishes haiku-default as the right policy; recorded as project policy rather
  than executed as a task.

### Reprioritize (5)

* **S-0009-04** medium → **high** — the per-benchmark pattern in t0014 (+100 pp on long-input
  benchmarks vs +13–17 pp on short ones) is exactly what the truncation hypothesis predicts.
  Splitting the schema-only +57 pp into "tree shape" vs "no truncation" is now load-bearing for the
  science.
* **S-0002-09** medium → low — infrastructure chore (re-fetch 11 PDFs with git LFS); low signal for
  the science.
* **S-0006-02** medium → low — async ScopeAwareReactAgent is performance optimization, not science;
  Phase 2 does not need it.
* **S-0011-02** medium → low — provider-specific calibration prompt variants; Phase 2 currently uses
  Anthropic only, so variant work is premature.
* **S-0014-05** medium → low — re-running 3 FrontierScience-Olympiad sonnet timeouts only recovers 3
  rows; n=20 → 23 does not materially change Wilson CIs on the existing decomposition.

## Out of Scope

* Creating new tasks (deferred to session 6 once t0012 lands).
* Modifying t0012's in-progress state.
* Replacing the proxy rows with native WorkArena++ / tau-bench data (S-0015-01 remains active at
  medium priority for a future session).

## Outputs

* 8 correction files in `corrections/` against six prior tasks.
* No new suggestions.
* No new assets.
* Updated effective suggestion view: 3 fewer active, 5 with revised priority.
