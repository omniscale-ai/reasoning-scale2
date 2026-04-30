# Datasets: `hierarchical-planning`

4 dataset(s).

[Back to all datasets](../README.md)

---

<details>
<summary>📂 <strong>Hierarchical Annotation v1 (115-row pilot audit) vv1</strong></summary>

| Field | Value |
|---|---|
| **ID** | `hierarchical-annotation-v1` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale project |
| **URL** | — |
| **License** | inherited-per-row |
| **Access** | restricted |
| **Size** | 115 rows total (FrontierScience-Olympiad=40, SWE-bench Verified=23, WorkArena++=26, tau-bench=26); each row carries a global / subtask / atomic hierarchy and gold-action triple. Twelve rows (three per benchmark) carry an LLM-as-judge verdict. |
| **Date added** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Description** | [`description.md`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/description.md) |
| **Summary** | Three-level (global / subtask / atomic) hierarchical annotation of 115 benchmark tasks drawn from FrontierScience-Olympiad, SWE-bench Verified, tau-bench, and WorkArena++. Includes a 12-row LLM-as-judge spot-check. |

</details>

<details>
<summary>📂 <strong>Hierarchical Annotation v2 (115-row pilot, tree schema)
vv2</strong></summary>

| Field | Value |
|---|---|
| **ID** | `hierarchical-annotation-v2` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale2 project |
| **URL** | — |
| **License** | inherited-per-row |
| **Access** | restricted |
| **Size** | 115 rows total; each row carries a tree-shaped hierarchy (global / subtasks-with-atomics / global_atomics) and a parallel gold_actions tree. 115 rows passed the v2 hierarchy_completeness check. 23 rows received an LLM-as-judge verdict (21 acceptable, 2 needs revision). Per-row benchmark labels: 40 FrontierScience-Olympiad, 23 SWE-bench Verified, 26 Mind2Web (proxy for WorkArena++), 26 HumanEval (proxy for tau-bench). |
| **Date added** | 2026-04-30 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Description** | [`description.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md) |
| **Summary** | Tree-shaped (global / subtasks-with-atomics / global_atomics) hierarchical annotation of 115 benchmark tasks from FrontierScience-Olympiad, SWE-bench Verified, Mind2Web (proxy for WorkArena++), and HumanEval (proxy for tau-bench). Re-annotates the v1 pilot under a v2 schema with explicit subtask-to-atomic edges and full problem text. Includes a 23-row LLM-as-judge spot-check. |

</details>

<details>
<summary>📂 <strong>Hierarchical Annotation v2 (115-row pilot, tree schema,
relabeled) vv2-relabeled</strong></summary>

| Field | Value |
|---|---|
| **ID** | `hierarchical-annotation-v2-relabeled` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale2 project |
| **URL** | — |
| **License** | inherited-per-row |
| **Access** | restricted |
| **Size** | 115 rows total; each row carries a tree-shaped hierarchy (global / subtasks-with-atomics / global_atomics) and a parallel gold_actions tree. 115 rows passed the v2 hierarchy_completeness check. 23 rows received an LLM-as-judge verdict (21 acceptable, 2 needs revision). Per-row benchmark labels: 40 FrontierScience-Olympiad, 23 SWE-bench Verified, 26 Mind2Web (proxy for WorkArena++), 26 HumanEval (proxy for tau-bench). |
| **Date added** | 2026-04-30 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Description** | [`description.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md) |
| **Summary** | Tree-shaped (global / subtasks-with-atomics / global_atomics) hierarchical annotation of 115 benchmark tasks from FrontierScience-Olympiad, SWE-bench Verified, Mind2Web (proxy for WorkArena++), and HumanEval (proxy for tau-bench). Same rows as the v2 source dataset; only the per-row benchmark label has been corrected to match the actual data source. Includes a 23-row LLM-as-judge spot-check. |

</details>

<details>
<summary>📂 <strong>Hierarchical Annotation v2-sonnet (115-row pilot, tree schema,
sonnet annotator) vv2-sonnet</strong></summary>

| Field | Value |
|---|---|
| **ID** | `hierarchical-annotation-v2-sonnet` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale2 project |
| **URL** | — |
| **License** | inherited-per-row |
| **Access** | restricted |
| **Size** | 115 rows total; each row carries a tree-shaped hierarchy (global / subtasks-with-atomics / global_atomics) and a parallel gold_actions tree, generated by claude-sonnet-4-6. 100 rows passed the v2 hierarchy_completeness check. 20 rows received an LLM-as-judge verdict from claude-haiku-4-5 (18 acceptable, 2 needs revision). |
| **Date added** | 2026-04-30 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Description** | [`description.md`](../../../tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet/description.md) |
| **Summary** | Sonnet-annotator re-run of the v2 tree-shaped hierarchical annotation of 115 benchmark tasks (FrontierScience-Olympiad, SWE-bench Verified, WorkArena++, tau-bench). Re-annotates the v1 pilot rows under the v2 tree schema with claude-sonnet-4-6 (haiku in t0009), keeping prompt and judge held constant. Includes a 20-row LLM-as-judge spot-check on the same 23-row stratified sample as t0009 (seed=42). |

</details>
