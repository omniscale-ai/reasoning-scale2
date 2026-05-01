# Suggestions: `hierarchical-planning`

22 suggestion(s) in category
[`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) **15 open** (3
high, 9 medium, 3 low), **7 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>📂 <strong>Hierarchical annotation v2: scale to >=200 rows with full human
review</strong> (S-0005-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Extend the v1 pilot to >=200 rows by re-running the upstream pilot pipeline with a stricter
retry policy (eliminate the 11 FrontierScience-Olympiad rows where steps==null), then perform
a full human-rater review of every row. Compute inter-rater agreement (Krippendorff's alpha or
Cohen's kappa) between the human rater and the LLM annotator.

</details>

<details>
<summary>🧪 <strong>Phase 2 A-vs-B-vs-C evaluation harness</strong> (S-0007-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0007_scope_unaware_planandsolve_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

Build the experiment harness that runs all three libraries (scope_aware_react_v1,
scope_unaware_planandsolve_v1, and the planned matched-mismatch library) on a fixed benchmark
slice with a single shared LLM provider, recording trajectory_records.jsonl per condition and
computing the registered metrics task_success_rate, avg_decisions_per_task, and
overconfident_error_rate per condition. The harness must depend on this library only via the
trajectory schema, never via internal helpers, to preserve isolation.

</details>

<details>
<summary>🧪 <strong>Re-judge the remaining 8 v1 paired rows to tighten the
pure-schema CI</strong> (S-0020-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The pure-schema delta CI (+22.5 to +77.5 pp) is dominated by the v1 sample size (n=12) because
t0005 only judged 12 of the 20 paired rows in its subsampled pool. Re-running the t0005 v1
judge on the remaining 8 paired indices (rows that t0014 judged but t0005 did not) would
extend v1 from n=12 to n=20 with no new annotation calls and tighten the pure-schema CI from a
half-width of ~28 pp to ~14 pp. Cost is ~8 haiku judge calls (~$0.50). This is the cheapest
possible follow-up that materially improves statistical power.

</details>

## Medium Priority

<details>
<summary>🔧 <strong>Add a gold_actions structural-mirror validator for non-empty
global_atomics</strong> (S-0009-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-02` |
| **Kind** | technique |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

The two needs-revision rows on FrontierScience-Olympiad both failed for the same reason: the
annotator emitted hierarchy.global_atomics correctly but produced gold_actions.global_atomics
empty or merged into a subtask. This is a structural-mirror inconsistency, not a content
error. Add a post-parse validator to v2_annotator.py that detects this pattern, re-prompts the
model on just the gold_actions block (or rejects the row to the parse-failure bucket), and
logs the rate. This should bring the FrontierScience-Olympiad accept rate from 67% to ~100%
with zero additional model cost on the happy path.

</details>

<details>
<summary>🧪 <strong>Derive step graphs for FrontierScience-Olympiad rows</strong>
(S-0003-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

FrontierScience-Olympiad pilot rows currently lack per-instance step graphs because Olympiad
solutions are graded as final answers. Run a hierarchical-annotation task that decomposes each
problem into global / subtask / atomic steps with gold actions at each level, so Phase 2 can
apply the canonical 4-8 decisions filter consistently across all four benchmarks.

</details>

<details>
<summary>📂 <strong>Expand the v2 dataset from 115 rows to >=200 rows by sampling
additional benchmark instances</strong> (S-0009-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-05` |
| **Kind** | dataset |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The Phase 1 success criterion is >=100 annotated tasks per condition; v2 is at 115 which is
just over the threshold. The downstream Phase 2 experiments need stratification by difficulty
AND by benchmark, which becomes statistically thin at 5-6 rows per stratum. Expand to >=200
rows by sampling 20-25 additional rows from each of the four benchmarks (especially the
smaller ones: SWE-bench Verified, tau-bench). Re-use v2_annotator.py at the same haiku-CLI
rate, ~$5-6 added cost. Inherits S-0005-01.

</details>

<details>
<summary>🔧 <strong>Reconcile WorkArena++ flat-action sequences with the three-level
schema</strong> (S-0005-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-03` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/) |

The judge rejected all three WorkArena++ rows because the upstream annotation lacks
`conceptual` nodes, causing the mapper to emit empty subtask lists. Investigate whether the
WorkArena++ source carries an implicit subtask boundary (e.g., screen transitions) that can be
detected automatically, or alternatively change the v2 schema to accept flat atomic-only rows
as a distinct hierarchy_kind. Document the chosen approach and update the mapper.

</details>

<details>
<summary>📂 <strong>Replace Mind2Web/HumanEval proxy rows with native WorkArena++
and tau-bench data</strong> (S-0015-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Variant a of S-0009-06 (now folded into this follow-up). The 26 m2w_* rows in the v2
hierarchical-annotation dataset are Mind2Web data used as a proxy for the gated WorkArena++
split, and the 26 he_* rows are HumanEval data used as a proxy for the gated tau-bench split.
t0015 corrected the labels but did not replace the underlying data. This task should (1)
obtain access to a real WorkArena++ split and a real tau-bench split (both currently gated;
expect a registration / agreement step that must be tracked as an intervention), (2)
re-annotate 26 + 26 rows under the v2 tree schema using the same haiku annotator and judge as
t0009 to keep variant b apples-to-apples, and (3) issue a corrections-overlay against
hierarchical-annotation-v2 that swaps the proxy rows for the native rows. Out of scope: any
change to the FrontierScience-Olympiad or SWE-bench Verified rows.

</details>

<details>
<summary>📊 <strong>Run a single-blind human review pass on the 115 v2 rows and
report human-vs-judge agreement (Cohen's kappa)</strong> (S-0009-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

v2 is judged only by a single LLM call per row. The dataset is 'LLM-judge-acceptable' but not
'human-validated'. To upgrade to v3, recruit 1-2 human annotators to review the same 23-row
stratified sample (or all 115 rows for higher precision) and emit acceptable/needs-revision
verdicts. Compute Cohen's kappa between human and the haiku judge to estimate how much of the
+58% v2-vs-v1 aggregate gain is real quality vs judge-LLM agreement-with-itself. Budget
estimate: 4-6 hours of human review time at $50/hour = $200-300.

</details>

<details>
<summary>🧪 <strong>Scale the truncated-v2 condition to n=80 to detect a true +5 pp
pure-text effect if it exists</strong> (S-0020-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The pure-text delta on this run is +5 pp with a CI of [-15, +26] pp at n=20. To resolve
whether the true pure-text effect is zero, +5 pp, or larger, the experiment needs n>=80 per
condition (Newcombe-Wilson half-width drops to ~10 pp at n=80 vs ~20 pp at n=20). This
requires running the v2 annotator and judge on 60 additional matched rows from the same
hierarchical-annotation-v1 source dataset, with both truncated and full conditions. Estimated
cost: 60 haiku annotations + 120 haiku judge verdicts at ~$0.07/call = ~$13. The result would
either confirm the schema-dominance claim with tight bounds or upgrade pure-text to a
meaningful contributor.

</details>

<details>
<summary>🧪 <strong>Scope a v3 schema iteration motivated by per-benchmark
schema-only deltas, not aggregate</strong> (S-0014-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

The aggregate schema-only delta is +57 pp (90% v2-sonnet vs 33% v1-sonnet) but the
per-benchmark split is bimodal: FrontierScience-Olympiad and WorkArena++ are at +100 pp (0% ->
100%), while SWE-bench Verified and tau-bench are at +13-17 pp (67% -> 80-83%). The +100 pp
cells suggest the v2 tree schema converts unsolvable v1 outputs into acceptable v2 outputs,
but this is potentially confounded with the truncation fix bundled into v2 (S-0009-04). The
+13-17 pp cells suggest a real but modest schema improvement on benchmarks where v1 was
already adequate. A v3 schema should target SWE/tau-style structured-action tasks specifically
— e.g., add explicit precondition/postcondition fields to atomics, since the SWE/tau cells
already saturate the high-level subtask abstraction.

</details>

<details>
<summary>📊 <strong>Sonnet judge rerun on the v2-tree-truncated condition to confirm
schema effect is not haiku-specific</strong> (S-0020-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

All three conditions in t0020 use a haiku judge for fairness, but this means the result is
haiku-judge accept rates rather than ground-truth quality. A sonnet rerun on the
v2-tree-truncated annotations (existing 20 rows, no new annotator calls) would confirm whether
the +57 pp pure-schema effect is robust to a stronger judge or whether it shrinks. t0014
already showed sonnet times out on some rows, so the rerun should set max_turns conservatively
and accept timeouts as null verdicts rather than retries. Estimated cost ~$3-5 sonnet judge.

</details>

## Low Priority

<details>
<summary>🧪 <strong>Defer Reflexion-style episodic memory to a Phase 3
ablation</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2303.11366`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Reflexion [Shinn2023] adds verbal self-reflection across trials and reaches 91% pass@1 on
HumanEval vs. 80% for vanilla GPT-4. Including episodic memory in Phase 2 would conflate scope
conditioning with cross-trial memory. Schedule a dedicated Phase 3 ablation that tests whether
Reflexion-style memory adds further gains on top of the scope-aware (A) condition established
in Phase 2.

</details>

<details>
<summary>🔧 <strong>Extend the library to support a granularity that varies within
a single run</strong> (S-0006-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-05` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Currently ScopeAwareReactAgent takes one fixed granularity for an entire run. A natural
extension is to let the agent emit a granularity transition (e.g., start global, drop to
subtask once a plan is established, drop to atomic during execution). Add a model-driven mode
where the parser also accepts <transition_to:subtask> markers and the agent updates the active
granularity per turn. This is a research extension worth Phase 2 ablation.

</details>

<details>
<summary>📊 <strong>Re-download Wang2023 PDF and verify the verbatim PS+ prompt
text</strong> (S-0007-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0007_scope_unaware_planandsolve_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The PS+ instruction string in scope_unaware_planandsolve_v1 was sourced through the t0002
paper summary, which was itself grounded only in the abstract because the PDF download failed
in t0002. A small download-paper task should re-attempt the download against arXiv:2305.04091
and verify that the prompt text in code/planandsolve.py matches the published version
verbatim. If it diverges, file a correction.

</details>

## Closed

<details>
<summary>✅ <s>Add an ablation: tree-schema-with-truncated-text to isolate the
truncation fix from the schema upgrade</s> — covered by <a
href="../../../tasks/t0020_v2_truncation_vs_schema_ablation/"><code>t0020_v2_truncation_vs_schema_ablation</code></a>
(S-0009-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0009_hierarchical_annotation_v2/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

v2 changed two things at once: schema (flat -> tree) and text completeness (truncated 1500
chars -> full). On FrontierScience-Olympiad and WorkArena++ the +67% and +100% deltas could be
entirely from the truncation fix (Xiong2024's prediction) or entirely from the schema upgrade.
Run a third condition: the v2 tree schema but truncate the problem to 1500 chars in both the
annotator and judge prompts. If accept rate drops materially below v2-full-text on
FrontierScience-Olympiad, truncation is the dominant cause; if it stays at v2-full-text
levels, the schema is the dominant cause. Cost ~$2 with haiku.

</details>

<details>
<summary>✅ <s>Implement matched-mismatch (C) library on top of
scope_unaware_planandsolve_v1</s> — covered by <a
href="../../../tasks/t0010_matched_mismatch_library/"><code>t0010_matched_mismatch_library</code></a>
(S-0007-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Create a third agent library that wraps scope_unaware_planandsolve_v1 (or
scope_aware_react_v1) with a tag-classifier that retroactively labels each step's granularity,
producing the matched-mismatch (C) condition for the project's A-vs-B-vs-C comparison. Reuse
this task's TRAJECTORY_RECORD_FIELDS export so all three libraries share the same trajectory
schema. The classifier should be a small fine-tuned model or heuristic so the task is
local-only and deterministic.

</details>

<details>
<summary>✅ <s>Implement Plan-and-Solve as the canonical scope-unaware (B)
baseline</s> — covered by <a
href="../../../tasks/t0007_scope_unaware_planandsolve_library/"><code>t0007_scope_unaware_planandsolve_library</code></a>
(S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Plan-and-Solve [Wang2023] is the strongest published prompt-only baseline that does not
condition on explicit granularity tags. The project should reuse LangChain's Plan-and-Execute
implementation rather than reimplementing from scratch. This task would adapt the LangChain
implementation to the project's task harness, log both stages (plan and solve) separately, and
produce a 10-instance validation run on the composite benchmark to confirm the baseline beats
vanilla Zero-shot-CoT.

</details>

<details>
<summary>✅ <s>Implement scope-aware (A) as ReAct extended with explicit granularity
tags</s> — covered by <a
href="../../../tasks/t0006_scope_aware_react_library/"><code>t0006_scope_aware_react_library</code></a>
(S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2210.03629`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The scope-aware (A) condition can be implemented as ReAct [Yao2022] extended with a per-token
granularity tag from the set {global, subtask, atomic}. This task would specify the prompt
template per granularity, the tagging logic that decides which granularity is active at each
LLM call, and a logging schema that records the active granularity for every action so
post-hoc per-granularity analysis is possible. Replicate Least-to-Most's solution-reuse
pattern [Zhou2022] inside the implementation.

</details>

<details>
<summary>✅ <s>Re-run v2 annotator with claude-sonnet-4-6 via direct API to
disentangle schema vs model effect</s> — covered by <a
href="../../../tasks/t0014_v2_annotator_sonnet_rerun/"><code>t0014_v2_annotator_sonnet_rerun</code></a>
(S-0009-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The v2 annotator was switched from sonnet to haiku to fit the $15 task budget under Claude
Code CLI overhead. The v2-vs-v1 accept rate delta therefore conflates the schema upgrade (flat
-> tree) with a model downgrade (sonnet -> haiku). Re-run all 115 rows on claude-sonnet-4-6
using the direct Anthropic API (no CLI), where per-call cost is ~$0.02 and 115 rows costs
~$2.30. Compare the resulting per-benchmark accept rate against both v1 (sonnet, flat) and
v2-haiku (haiku, tree) to attribute the +33% to +100% deltas between schema and model
contributions.

</details>

<details>
<summary>✅ <s>Run a Phase 1 pilot annotation on 20 tasks before scaling to 100</s> —
covered by <a
href="../../../tasks/t0005_hierarchical_annotation_pilot_v1/"><code>t0005_hierarchical_annotation_pilot_v1</code></a>
(S-0002-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-08` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The project's success criteria require 100 tasks annotated at three granularity levels. Before
scaling, run a 20-task pilot to validate the annotation schema, measure inter-annotator
agreement, and refine the rubric. WorkArena++ [Boisvert2024] offers the cleanest
atomic-vs-compositional structure for the pilot; its synthetic trace generator can supply gold
atomic actions, leaving manual annotation effort focused on global and subtask levels.

</details>

<details>
<summary>✅ <s>Stress-test the +57 pp schema-only delta with a stricter substantive
judge</s> — covered by <a
href="../../../tasks/t0019_v2_judge_calibration_sonnet/"><code>t0019_v2_judge_calibration_sonnet</code></a>
(S-0014-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The schema-only delta of +57 pp is well above Zhou2022's +16 pp and Boisvert2024's +25 pp
published bands. One plausible cause is judge anchoring on tree shape: the haiku judge may be
partially scoring 'did the model produce a parseable tree with subtask-to-atomic edges' rather
than 'is the decomposition substantively right'. Replace the haiku judge with a substantive
critic prompt that simulates execution ('verify each atomic, executed in order, would actually
solve the problem') and re-judge the same 20-row sample under all three conditions (v1-sonnet,
v2-haiku, v2-sonnet). If schema-only drops materially below +57 pp under the substantive
judge, the gap to literature was judge anchoring; if schema-only stays near +57 pp, the schema
is doing real work. Cost ~$3 with sonnet judge.

</details>
