# Answers (2)

2 answer(s).

**Browse by view**: By category: [`agent-evaluation`](by-category/agent-evaluation.md),
[`benchmark-annotation`](by-category/benchmark-annotation.md),
[`hierarchical-planning`](by-category/hierarchical-planning.md),
[`uncertainty-calibration`](by-category/uncertainty-calibration.md); [By date
added](by-date-added/README.md)

---

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
| **Full answer** | [`full_answer.md`](../../tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/full_answer.md) |
| **ID** | [`does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges`](../../tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/) |
| **Question** | Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive judge and under a sonnet judge, or is the +57 pp t0014 headline an artefact of haiku judge anchoring? |
| **Methods** | `code-experiment` |
| **Confidence** | low |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |
| **Paper sources** | — |
| **Task sources** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **URL sources** | — |
| **Created by** | [`t0019_v2_judge_calibration_sonnet`](../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |

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
| **Full answer** | [`full_answer.md`](../../tasks/t0020_v2_truncation_vs_schema_ablation/assets/answer/decomposition-v2-schema-vs-truncation/full_answer.md) |
| **ID** | [`decomposition-v2-schema-vs-truncation`](../../tasks/t0020_v2_truncation_vs_schema_ablation/assets/answer/decomposition-v2-schema-vs-truncation/) |
| **Question** | How much of the +57 pp v2-tree-full vs v1-flat-truncated acceptance-rate gap on the matched t0014 pool is due to the v2 tree schema itself versus the full (untruncated) problem text? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-01 |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Paper sources** | — |
| **Task sources** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **URL sources** | — |
| **Created by** | [`t0020_v2_truncation_vs_schema_ablation`](../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |

</details>
