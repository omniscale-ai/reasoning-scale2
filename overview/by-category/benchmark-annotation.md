# Category: Benchmark Annotation

Manual or LLM-assisted gold-action annotation across the three granularity levels.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (1)](../papers/by-category/benchmark-annotation.md) | [Suggestions
(13)](../suggestions/by-category/benchmark-annotation.md) | [Datasets
(3)](../datasets/by-category/benchmark-annotation.md)

---

## Papers (1)

<details>
<summary>📋 <strong>Introducing SWE-bench Verified</strong> — team, 2024</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_OpenAI2024_swe-bench-verified` |
| **Authors** | OpenAI Preparedness team |
| **Venue** | OpenAI technical card (institutional, not peer-reviewed) (technical_report) |
| **DOI** | — |
| **URL** | https://openai.com/index/introducing-swe-bench-verified/ |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-swebench`](../../meta/categories/benchmark-swebench/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/no-doi_OpenAI2024_swe-bench-verified/summary.md) |

SWE-bench Verified is a 500-instance human-validated subset of SWE-bench produced by OpenAI's
Preparedness team in collaboration with the original SWE-bench authors. The motivation is that
the parent benchmark of 2,294 problems contains some items with ambiguous issue descriptions
or flaky tests, which add noise to capability measurements at the frontier.

Methodologically, 93 expert software engineers each reviewed candidate problems on three axes:
(a) clear instructions, (b) correct test patches, (c) reproducible environments. Three
independent reviewers per problem; only problems passing all three axes from all three
reviewers were included. The harness, Docker images, and resolve@1 scoring are identical to
the parent benchmark.

The headline outcome is that Verified has become the de facto standard subset for measuring
frontier autonomous-software-engineering capability in 2024-2026. Modern models score far
above the parent benchmark's 1.96% Claude 2 baseline — Claude Mythos Preview leads at
**93.9%** (April 2026). OpenAI's own April 2026 commentary noted that this saturation may
limit Verified's usefulness as a frontier-capability measurement going forward.

For the granularity-aware hierarchical agents project, SWE-bench Verified is the canonical
atomic-execution slot in the Phase 2 composite benchmark. Its 500-instance size is tractable
for multiple-condition evaluation, the human validation removes benchmark noise, and
stratified reporting is essential because Verified's >90%-achievable ceiling would otherwise
drown out FrontierMath's <2% baseline. The project should plan a fallback to SWE-bench
Multimodal or SWE-bench Pro if Verified saturates further before Phase 2 completes.

</details>

## Tasks (1)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |

## Answers (0)

No answers in this category.

## Suggestions (9 open, 4 closed)

<details>
<summary>🔧 <strong>Add a gold_actions structural-mirror validator for non-empty
global_atomics</strong> (S-0009-02)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

The two needs-revision rows on FrontierScience-Olympiad both failed for the same reason: the
annotator emitted hierarchy.global_atomics correctly but produced gold_actions.global_atomics
empty or merged into a subtask. This is a structural-mirror inconsistency, not a content
error. Add a post-parse validator to v2_annotator.py that detects this pattern, re-prompts the
model on just the gold_actions block (or rejects the row to the parse-failure bucket), and
logs the rate. This should bring the FrontierScience-Olympiad accept rate from 67% to ~100%
with zero additional model cost on the happy path.

</details>

<details>
<summary>📊 <strong>Run a single-blind human review pass on the 115 v2 rows and
report human-vs-judge agreement (Cohen's kappa)</strong> (S-0009-03)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

v2 is judged only by a single LLM call per row. The dataset is 'LLM-judge-acceptable' but not
'human-validated'. To upgrade to v3, recruit 1-2 human annotators to review the same 23-row
stratified sample (or all 115 rows for higher precision) and emit acceptable/needs-revision
verdicts. Compute Cohen's kappa between human and the haiku judge to estimate how much of the
+58% v2-vs-v1 aggregate gain is real quality vs judge-LLM agreement-with-itself. Budget
estimate: 4-6 hours of human review time at $50/hour = $200-300.

</details>

<details>
<summary>🧪 <strong>Add an ablation: tree-schema-with-truncated-text to isolate the
truncation fix from the schema upgrade</strong> (S-0009-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

v2 changed two things at once: schema (flat -> tree) and text completeness (truncated 1500
chars -> full). On FrontierScience-Olympiad and WorkArena++ the +67% and +100% deltas could be
entirely from the truncation fix (Xiong2024's prediction) or entirely from the schema upgrade.
Run a third condition: the v2 tree schema but truncate the problem to 1500 chars in both the
annotator and judge prompts. If accept rate drops materially below v2-full-text on
FrontierScience-Olympiad, truncation is the dominant cause; if it stays at v2-full-text
levels, the schema is the dominant cause. Cost ~$2 with haiku.

</details>

<details>
<summary>📂 <strong>Expand the v2 dataset from 115 rows to >=200 rows by sampling
additional benchmark instances</strong> (S-0009-05)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

The Phase 1 success criterion is >=100 annotated tasks per condition; v2 is at 115 which is
just over the threshold. The downstream Phase 2 experiments need stratification by difficulty
AND by benchmark, which becomes statistically thin at 5-6 rows per stratum. Expand to >=200
rows by sampling 20-25 additional rows from each of the four benchmarks (especially the
smaller ones: SWE-bench Verified, tau-bench). Re-use v2_annotator.py at the same haiku-CLI
rate, ~$5-6 added cost. Inherits S-0005-01.

</details>

<details>
<summary>📂 <strong>Replace Mind2Web/HumanEval proxy rows with native WorkArena++
and tau-bench data</strong> (S-0015-01)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0015_correct_proxy_benchmark_labels](../../tasks/t0015_correct_proxy_benchmark_labels/)

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
<summary>📊 <strong>Add a row-level original_benchmark provenance field to future
relabel corrections</strong> (S-0015-02)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-30 | **Source**:
[t0015_correct_proxy_benchmark_labels](../../tasks/t0015_correct_proxy_benchmark_labels/)

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
<summary>🧪 <strong>Derive step graphs for FrontierScience-Olympiad rows</strong>
(S-0003-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0003_download_benchmark_subsets](../../tasks/t0003_download_benchmark_subsets/)

FrontierScience-Olympiad pilot rows currently lack per-instance step graphs because Olympiad
solutions are graded as final answers. Run a hierarchical-annotation task that decomposes each
problem into global / subtask / atomic steps with gold actions at each level, so Phase 2 can
apply the canonical 4-8 decisions filter consistently across all four benchmarks.

</details>

<details>
<summary>📂 <strong>Hierarchical annotation v2: scale to >=200 rows with full human
review</strong> (S-0005-01)</summary>

**Kind**: dataset | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

Extend the v1 pilot to >=200 rows by re-running the upstream pilot pipeline with a stricter
retry policy (eliminate the 11 FrontierScience-Olympiad rows where steps==null), then perform
a full human-rater review of every row. Compute inter-rater agreement (Krippendorff's alpha or
Cohen's kappa) between the human rater and the LLM annotator.

</details>

<details>
<summary>📂 <strong>Remediate proxy benchmark naming and task_id
non-uniqueness</strong> (S-0005-04)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

The pilot file uses tau-bench and WorkArena++ as proxies but task_id prefixes are still `he_*`
(HumanEval) and `m2w_*` (Mind2Web) from earlier drafts; additionally 14 of 115 task_ids are
duplicated. Re-key the source data with synthetic per-row UUIDs and align task_id prefixes
with the actual benchmark slugs (`tau_*`, `wa_*`).

</details>
