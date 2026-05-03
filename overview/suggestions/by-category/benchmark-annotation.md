# Suggestions: `benchmark-annotation`

22 suggestion(s) in category
[`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) **16 open** (3 high,
8 medium, 5 low), **6 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>🔧 <strong>Adopt a haiku-default annotation policy for Phase 2: model swap
is not justified</strong> (S-0014-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-04` |
| **Kind** | technique |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Under the t0014 measurement, haiku and sonnet annotators produce statistically
indistinguishable accept rates under the v2 tree schema (90% sonnet vs 91% haiku, CIs overlap
completely). Sonnet annotation costs ~$0.20 per call vs haiku ~$0.02 per call (10x via Claude
Code CLI; 7-8x via direct API). For Phase 2 ABC/main-experiment annotation budgets in the
$50-200 range, the cost differential dominates: a 200-row sonnet annotation pass would cost
$40 vs $5 for haiku, with no measurable accept-rate benefit. Adopt haiku as the default
annotator unless and until S-0014-02 or S-0014-03 surfaces a real sonnet advantage masked by
judge bias.

</details>

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
<summary>🧪 <strong>Rotate the judge model to test the haiku-vs-haiku familial bias
hypothesis on the model-only delta</strong> (S-0014-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The model-only delta of -1 pp sits below Xiong2024's lower edge (0 pp). Xiong2024 documents
that judges trained on the same model family as the annotator show a small positive familial
bias (~5-10 pp). Our judge is held on haiku to keep apples-to-apples with t0009/t0005, which
means v2-haiku has a familial-agreement advantage over v2-sonnet. Re-judge the same 20-row
v2-sonnet sample and 23-row v2-haiku sample with claude-sonnet-4-6 as the judge instead of
haiku. If the model-only delta swings positive (e.g., +5-10 pp) under the sonnet judge, the
haiku-vs-haiku familial bias is masking a real sonnet annotator advantage. If it stays near
zero, sonnet really does provide no annotator-quality lift on this composite. Cost ~$2 with
sonnet judge on 43 rows.

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
<summary>📂 <strong>Remediate proxy benchmark naming and task_id
non-uniqueness</strong> (S-0005-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

The pilot file uses tau-bench and WorkArena++ as proxies but task_id prefixes are still `he_*`
(HumanEval) and `m2w_*` (Mind2Web) from earlier drafts; additionally 14 of 115 task_ids are
duplicated. Re-key the source data with synthetic per-row UUIDs and align task_id prefixes
with the actual benchmark slugs (`tau_*`, `wa_*`).

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

## Low Priority

<details>
<summary>📊 <strong>Add a row-level original_benchmark provenance field to future
relabel corrections</strong> (S-0015-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

The t0015 overlay rewrites the per-row benchmark string but does not preserve the original
proxy label inside the row. A reader inspecting only the effective JSONL cannot tell that the
row was previously labeled differently — provenance lives only in the corrections overlay's
description.md. For future relabel corrections, the framework would benefit from a soft
convention where the corrected row carries an original_benchmark field (or, more generally,
original_<field> for any field rewritten by a corrections overlay). This makes per-row
provenance auditable without round-tripping through the corrections file. The task should: (1)
propose the convention as a small extension to the corrections specification, (2) update the
dataset-asset verificator to surface a warning when an overlay rewrites a per-row field
without preserving the original, and (3) backfill the convention into the t0015 overlay.

</details>

<details>
<summary>📊 <strong>Cost-quality Pareto chart across t0009/t0014/t0020 to inform
downstream task budgets</strong> (S-0020-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

Three conditions now exist on the same 20-row pool: v1-flat-truncated (cheap, low quality),
v2-tree-truncated (cheap, high quality), v2-tree-full (expensive, slightly higher quality). A
Pareto chart with cost-per-row on the x-axis and accept rate on the y-axis would crisply
communicate that v2-tree-truncated is on the Pareto frontier and v2-tree-full is dominated by
it once the +5 pp gain is weighed against the ~2x cost. Useful as input to the t0022 ABC
harness budget planning.

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

<details>
<summary>🧪 <strong>Re-run the three FrontierScience-Olympiad sonnet timeouts under a
longer CLI timeout to recover the missing rows</strong> (S-0014-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

Three FrontierScience-Olympiad rows (pilot indices 7, 8, 14) timed out at the 300s Claude Code
CLI ceiling during the sonnet annotation pass. They were dropped from the judge sample,
reducing FS sample size from 6 (t0009 v2-haiku) to 3 (t0014 v2-sonnet). The +33 pp model-only
delta on FS (67% v2-haiku vs 100% v2-sonnet, n=6 vs n=3) is therefore on a smaller sample than
the other benchmarks. Re-run those three rows with a 600s or 900s CLI timeout (or via direct
Anthropic API which has no per-call wall-clock cap) and re-judge. If all three pass, FS
aggregate v2-sonnet stays at 100% on n=6 and the +33 pp model-only delta becomes more
credible. Cost <$1.

</details>

<details>
<summary>🧪 <strong>Truncation-budget sweep to map the marginal value of additional
context</strong> (S-0020-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) |

t0020 shows 1500 chars is sufficient on 3 of 4 benchmarks but loses ~17 pp on SWE-bench
Verified. A finer truncation grid (500 / 1000 / 1500 / 2500 / 5000 / full) on a
SWE-bench-heavy pool would map where the marginal value of additional context drops to zero.
This is a single-condition sweep (v2 schema held constant; only the truncation budget varies)
so the cost scales linearly with the number of budget points. Estimated cost: 6 budgets x 20
SWE-bench rows x 2 calls per row x ~$0.07 = ~$17.

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
<summary>✅ <s>Re-run LLM-as-judge with full problem text (no truncation)</s> —
covered by <a
href="../../../tasks/t0009_hierarchical_annotation_v2/"><code>t0009_hierarchical_annotation_v2</code></a>
(S-0005-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

The v1 judge sees only the first 1500 chars of each problem. Three of four needs-revision
verdicts on FrontierScience-Olympiad rows complain about content not present in the truncated
excerpt. Re-run the audit using the full problem text (or a structured per-section summary)
and compare accept rates. Predict an absolute accept-rate increase of >=15 percentage points
on FrontierScience-Olympiad.

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
