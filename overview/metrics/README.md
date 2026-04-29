# Metrics (3)

## #️⃣ count (1)

<details>
<summary>#️⃣ <strong>Average Decisions per Task</strong>
(<code>avg_decisions_per_task</code>)</summary>

| Field | Value |
|---|---|
| **Key** | `avg_decisions_per_task` |
| **Unit** | count |
| **Value type** | float |
| **Datasets** | — |

Mean number of agent decisions executed per task in a run, reported per condition.
Informational diagnostic that exposes replanning behavior and depth of execution; not a
leaderboard metric.

</details>

## 📊 ratio (1)

<details>
<summary>📊 <strong>Overconfident Error Rate</strong>
(<code>overconfident_error_rate</code>)</summary>

| Field | Value |
|---|---|
| **Key** | `overconfident_error_rate` |
| **Unit** | ratio |
| **Value type** | float |
| **Datasets** | — |

Project Metric 2: fraction of incorrect actions taken with high model-reported confidence on
the composite annotated benchmark, reported per condition (A scope-aware, B scope-unaware, C
scope-mismatched). Lower values indicate better calibration.

</details>

## ✅ accuracy (1)

<details>
<summary>✅ <strong>Task Success Rate</strong> (<code>task_success_rate</code>)</summary>

| Field | Value |
|---|---|
| **Key** | `task_success_rate` |
| **Unit** | accuracy |
| **Value type** | float |
| **Datasets** | — |

Project Metric 1: normalized fraction of fully solved tasks (or binary success on the full
task) on the composite annotated benchmark, reported per condition (A scope-aware, B
scope-unaware, C scope-mismatched).

</details>
