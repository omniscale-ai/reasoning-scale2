# Suggestions: `agent-evaluation`

18 suggestion(s) in category [`agent-evaluation`](../../../meta/categories/agent-evaluation/)
**13 open** (5 high, 6 medium, 2 low), **5 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>🧪 <strong>Add a uniform-random vs. adversarial vs. matched ablation to
t0012</strong> (S-0010-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0010_matched_mismatch_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

When t0012 runs the A-vs-B-vs-C harness, include three C-condition variants in addition to A
and B: matched_mismatch_v1 with mismatch_strategy='random' and seed=0, matched_mismatch_v1
with mismatch_strategy='adversarial', and a phase-randomised C control (random walk over the
v2 hierarchy with the correct tag). The three-way ablation decomposes the C-condition gap into
'phase order matters', 'any wrong tag matters', and 'most-distant wrong tag matters',
preventing the granularity-mismatch effect from being conflated with a step-order-mismatch
effect (see research_papers.md, Wang2023 and Zhou2022).

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
<summary>📚 <strong>Set up ServiceNow + BrowserGym harness shared by WorkArena and
WorkArena++</strong> (S-0002-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-03` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Both WorkArena [Drouin2024] and WorkArena++ [Boisvert2024] require a self-hosted ServiceNow
developer instance and the BrowserGym Python harness. This is a substantial infrastructure
task with credentials, container orchestration, and end-to-end smoke tests. Schedule it before
any task that needs WorkArena or WorkArena++ data so the harness is ready when Phase 1
annotation begins.

</details>

<details>
<summary>🧪 <strong>Use hierarchical-annotation-v1 to seed Phase 2 scope-conditioning
experiments</strong> (S-0005-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The dataset asset is now ready for downstream consumption. Plan a baseline-evaluation task
that uses the 102 hierarchy-complete rows to compare scope-conditioned vs scope-unaware agent
prompts (B vs G/S/A from the project's research questions).

</details>

## Medium Priority

<details>
<summary>📚 <strong>Add an async ScopeAwareReactAgent variant for streaming and
parallel tool calls</strong> (S-0006-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The current agent is synchronous. Phase 2 experiments at scale will benefit from streaming
model output and from issuing multiple independent tool calls concurrently within a single
Thought block. Build async_scope_aware_react.py exposing AsyncScopeAwareReactAgent with an
async model_call signature and asyncio.gather over Action lists. Tests should use
AsyncScriptedModel mirroring the sync helper.

</details>

<details>
<summary>📚 <strong>Build benchmark-specific tool registries for the four roadmap
benchmarks</strong> (S-0006-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/), [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/), [`benchmark-taubench`](../../../meta/categories/benchmark-taubench/) |

scope_aware_react_v1 accepts an arbitrary tool_registry but ships none. Phase 2 needs
registries for FrontierScience-Olympiad (calculator, search, paper lookup), WorkArena++
(browser, form filler, table lookup), SWE-bench Verified (file read, file write, run tests,
git diff), and tau-bench (DB query, API call, customer-action stubs). Each should be its own
write-library task that imports scope_aware_react_v1 and registers a registry with consistent
naming conventions.

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
<summary>📊 <strong>Measure the missing-tag fallback rate against real LLMs</strong>
(S-0006-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The library defaults to atomic when the model omits a granularity tag and emits a
tag_missing_defaulted_to_atomic warning observation. The deterministic tests cover the parser
path but the fallback rate against real LLMs (GPT-4o, Claude 3.7 Sonnet, Llama-3.1-70B) is
unknown. Build an evaluation task that runs each library at each granularity over N=20
problems per benchmark and reports the fallback rate alongside task success.

</details>

<details>
<summary>📊 <strong>Register pass^k as a project metric for reliability
reporting</strong> (S-0002-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2406.12045`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2406.12045/) |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-taubench`](../../../meta/categories/benchmark-taubench/) |

tau-bench [Yao2024] introduces pass^k, a metric that measures whether an agent succeeds across
k independent rollouts. The 25-percentage-point gap between pass@1 and pass^8 in retail
demonstrates that single-rollout pass@1 systematically overstates agent reliability. The
project should register a pass_at_k metric (with k=1, 8) under meta/metrics/ to complement
task_success_rate. This enables Phase 4 paper-ready claims to be robust to single-rollout
luck.

</details>

<details>
<summary>📊 <strong>Schema-parity dedup task between t0006 and t0007</strong>
(S-0007-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

After t0006 (scope_aware_react_v1) merges, run a small deduplication-style task that imports
both libraries' TRAJECTORY_RECORD_FIELDS tuples and asserts they are identical, plus a smoke
test that runs both libraries on the same toy problem and verifies the trajectory JSON shapes
round-trip through a single Pydantic loader. If they diverge, file a correction in the
later-merged task. This is the cheapest insurance against silent schema drift.

</details>

## Low Priority

<details>
<summary>📊 <strong>Multi-judge disagreement study on hierarchical
annotation</strong> (S-0005-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Run the same 12-row spot-check with two judge models (claude-haiku-4-5 + claude-sonnet-4-6)
and compute pairwise verdict agreement plus a confusion matrix. The v1 single-judge accept
rate of 33% may be miscalibrated; multi-judge agreement gives a more reliable quality
estimate. Estimated cost: ~$0.30 per run.

</details>

<details>
<summary>📊 <strong>Resolve the subtask-adversarial ambiguity with empirical
evidence</strong> (S-0010-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

ADVERSARIAL_MAP currently pins 'subtask -> atomic' because subtask is equidistant from global
and atomic. Run a small ablation in t0012 with both 'subtask -> atomic' and 'subtask ->
global' adversarial maps and report the per-step contribution. If the two choices differ
materially, document the chosen direction and the empirical justification in
matched_mismatch_v1's description.md. If they do not differ, lock the current choice and
remove the ambiguity note.

</details>

## Closed

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
<summary>✅ <s>Implement verbalized-confidence + 3-sample self-consistency aggregator
for Metric 2</s> — covered by <a
href="../../../tasks/t0011_metric2_calibration_aggregator/"><code>t0011_metric2_calibration_aggregator</code></a>
(S-0002-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Xiong2024 establishes that single-sample verbalized confidence is poorly calibrated and that
3-sample self-consistency aggregation reduces ECE by 2-8 points. The project should commit to
this protocol for Metric 2 (overconfident error rate). This task would specify the
human-inspired confidence prompt template (low/medium/high + brief justification), implement
the self-consistency aggregator, and validate calibration on a small held-out set before Phase
2 launches.

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
<summary>✅ <s>Replace the WorkArena++ proxy and HumanEval-as-tau-bench-proxy rows
with the actual benchmark data</s> — covered by <a
href="../../../tasks/t0015_correct_proxy_benchmark_labels/"><code>t0015_correct_proxy_benchmark_labels</code></a>
(S-0009-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-06` |
| **Kind** | dataset |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Inspecting the v1 (and now v2) rows shows the 'WorkArena++' rows are actually Mind2Web proxy
data and the 'tau-bench' rows are HumanEval proxy data — neither benchmark is loaded directly
because of access restrictions noted in the v1 task. For Phase 2 the benchmark provenance
matters: agent-evaluation results on Mind2Web do not generalize to WorkArena++. Either (a)
acquire WorkArena++ and tau-bench proper and re-annotate those rows, or (b) rename the
benchmark fields to match what is actually stored (Mind2Web, HumanEval) and update downstream
consumers. This is necessary before any Phase 2 paper claim about WorkArena++ performance.

</details>

<details>
<summary>✅ <s>Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience
subset</s> — covered by <a
href="../../../tasks/t0012_phase2_abc_smoke_frontierscience/"><code>t0012_phase2_abc_smoke_frontierscience</code></a>
(S-0006-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | [`10.48550_arXiv.2210.03629`](../../../tasks/t0006_scope_aware_react_library/assets/paper/10.48550_arXiv.2210.03629/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

scope_aware_react_v1 (A) and the in-progress scope_unaware_planandsolve_v1 (B) are now ready
as substrates. Run a controlled experiment on the t0003 FrontierScience subset with both
libraries plus a no-prompt-engineering baseline (C), measuring task_success_rate,
overconfident_error_rate, and avg_decisions_per_task across N=50 problems. Expected effect
size: +5 to +15 absolute success rate for A over B based on the Yao2022 ALFWorld result
anchor.

</details>
