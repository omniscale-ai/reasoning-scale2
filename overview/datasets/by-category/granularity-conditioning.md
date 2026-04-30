# Datasets: `granularity-conditioning`

1 dataset(s).

[Back to all datasets](../README.md)

---

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
| **Size** | 115 rows total; each row carries a tree-shaped hierarchy (global / subtasks-with-atomics / global_atomics) and a parallel gold_actions tree. 115 rows passed the v2 hierarchy_completeness check. 23 rows received an LLM-as-judge verdict (21 acceptable, 2 needs revision). |
| **Date added** | 2026-04-30 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Description** | [`description.md`](../../../tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/description.md) |
| **Summary** | Tree-shaped (global / subtasks-with-atomics / global_atomics) hierarchical annotation of 115 benchmark tasks from FrontierScience-Olympiad, SWE-bench Verified, WorkArena++, and tau-bench. Re-annotates the v1 pilot under a v2 schema with explicit subtask-to-atomic edges and full problem text. Includes a 23-row LLM-as-judge spot-check. |

</details>
