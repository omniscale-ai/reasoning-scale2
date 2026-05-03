# Answers by Date Added

3 answer(s) grouped by creation date.

[Back to all answers](../README.md)

---

## 2026-05-03 (1)

<details>
<summary><strong>Which RQ1 execution path do we follow under the permanent
no-Anthropic constraint: (a) existing-results-only verdict, (b) local /
open-weight rerun, (c) alternative paid provider, or (d) project-level
underpowered / provider-blocked stop?</strong></summary>

**Confidence**: high

Option (a), the existing-results-only verdict, is the right path. The t0031 re-derivation
already yields the formal RQ1 conclusion at $0 with arm-labelling comparability with t0027 /
t0028 preserved by construction: 12 / 130 = 9.23% discordance, 6 arm-A wins and 6 arm-B wins,
two-sided exact-binomial McNemar p = 1.0000, with a SWE-bench arm-B advantage and a
FrontierScience arm-A advantage that cancel in aggregate. Options (b) and (c) replace the
policy under each arm label and turn any rerun into a verdict on a new experiment, while
option (d) forecloses the verdict that (a) can deliver immediately.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/full_answer.md) |
| **ID** | [`no-anthropic-rq1-path-a`](../../../tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/) |
| **Question** | Which RQ1 execution path do we follow under the permanent no-Anthropic constraint: (a) existing-results-only verdict, (b) local / open-weight rerun, (c) alternative paid provider, or (d) project-level underpowered / provider-blocked stop? |
| **Methods** | `code-experiment`, `internet` |
| **Confidence** | high |
| **Date created** | 2026-05-03 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |
| **Paper sources** | — |
| **Task sources** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md), [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md), [`t0028_brainstorm_results_8`](../../../overview/tasks/task_pages/t0028_brainstorm_results_8.md), [`t0029_rq1_discordance_rich_resample`](../../../overview/tasks/task_pages/t0029_rq1_discordance_rich_resample.md), [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **URL sources** | [url 1](https://openai.com/api/pricing/), [url 2](https://ai.google.dev/gemini-api/docs/pricing), [url 3](https://www.anthropic.com/pricing) |
| **Created by** | [`t0032_no_anthropic_rq1_path_decision`](../../../overview/tasks/task_pages/t0032_no_anthropic_rq1_path_decision.md) |

</details>

## 2026-05-01 (2)

<details>
<summary><strong>Does the v2 schema retain a 30+ pp accept-rate delta over v1 under
a substantive judge and under a sonnet judge, or is the +57 pp t0014
headline an artefact of haiku judge anchoring?</strong></summary>

**Confidence**: low

The evidence is mixed. Under substantive-sonnet the schema-only delta is +24.6 pp and under
model-rotated-sonnet it is +37.3 pp, vs the t0014 baseline of +58.0 pp. The +57 pp headline
does not cleanly survive a stronger judge, but neither does it collapse below +30 pp on both
configurations; the answer depends on which sonnet judge configuration is treated as
canonical.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/full_answer.md) |
| **ID** | [`does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges`](../../../tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/) |
| **Question** | Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive judge and under a sonnet judge, or is the +57 pp t0014 headline an artefact of haiku judge anchoring? |
| **Methods** | `code-experiment` |
| **Confidence** | low |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |
| **Paper sources** | — |
| **Task sources** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **URL sources** | — |
| **Created by** | [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |

</details>

<details>
<summary><strong>How much of the +57 pp v2-tree-full vs v1-flat-truncated
acceptance-rate gap on the matched t0014 pool is due to the v2 tree schema
itself versus the full (untruncated) problem text?</strong></summary>

**Confidence**: medium

The v2 tree schema explains essentially all of the gap: switching from flat-v1 to tree-v2
while holding the 1500-char truncation constant lifts the haiku judge accept rate from 33% to
90%, a +57 pp jump (95% Wilson CI on the difference: +23 pp to +77 pp). Adding the full
untruncated problem text on top of the v2 schema lifts accept from 90% to 95%, a further +5 pp
(95% CI -15 pp to +26 pp), which is not statistically significant. The headline +62 pp v2-full
vs v1-truncated gap is therefore ~92% pure-schema and ~8% pure-text-length on the 20-row
matched pool.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0020_v2_truncation_vs_schema_ablation/assets/answer/decomposition-v2-schema-vs-truncation/full_answer.md) |
| **ID** | [`decomposition-v2-schema-vs-truncation`](../../../tasks/t0020_v2_truncation_vs_schema_ablation/assets/answer/decomposition-v2-schema-vs-truncation/) |
| **Question** | How much of the +57 pp v2-tree-full vs v1-flat-truncated acceptance-rate gap on the matched t0014 pool is due to the v2 tree schema itself versus the full (untruncated) problem text? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-01 |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Paper sources** | — |
| **Task sources** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **URL sources** | — |
| **Created by** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |

</details>
