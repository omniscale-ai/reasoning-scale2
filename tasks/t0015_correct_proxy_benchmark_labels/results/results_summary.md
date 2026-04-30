# Results Summary: Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Summary

Wrote a single corrections-overlay file (`corrections/dataset_hierarchical-annotation-v2.json`) that
relabels the **52** rows in the t0009 v2 hierarchical-annotation dataset whose `benchmark` field
referred to a gated proxy-target benchmark instead of the actual data source: **26** `m2w_*` rows
move from `WorkArena++` to `Mind2Web`, and **26** `he_*` rows move from `tau-bench` to `HumanEval`.
The `aggregate_datasets` overlay applies cleanly: the effective JSONL now carries the corrected
labels and the dataset metadata prose no longer mentions the wrong benchmark names.

## Metrics

* **Rows relabeled, total**: **52** of 115 (45.2%)
* **`WorkArena++` -> `Mind2Web`**: **26** rows (all rows whose `task_id` starts with `m2w_`)
* **`tau-bench` -> `HumanEval`**: **26** rows (all rows whose `task_id` starts with `he_`)
* **Rows unchanged**: **63** (40 `FrontierScience-Olympiad` + 23 `SWE-bench Verified`)
* **Effective JSONL distribution after overlay**: 40 / 23 / 26 / 26 (FrontierScience-Olympiad /
  SWE-bench Verified / Mind2Web / HumanEval)
* **Non-`benchmark` field diffs vs source**: **0**
* **Cost**: **$0** (local file authoring; no API or compute spend)

## Verification

* `verify_corrections t0015_correct_proxy_benchmark_labels` -> **PASSED** (0 errors, 0 warnings)
* `aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json` -> overlay
  applies; `description_path` resolves to t0015's relabeled `description.md`; `files[0].path`
  resolves to the relabeled JSONL; `short_description` and `size_description` no longer mention
  `WorkArena++` or `tau-bench`.
* Dataset asset verificator on `hierarchical-annotation-v2-relabeled` -> **PASSED** (0 errors, 2
  warnings inherited from the source schema: missing author country and 4-paragraph Summary shape).
* `verify_research_code` -> **PASSED** (0 errors, 0 warnings).
* `verify_plan` -> **PASSED** (0 errors, 0 warnings).
* `verify_task_folder` -> **PASSED** (0 errors, expected warnings about empty `logs/searches/` and
  `corrections/` populated mid-execution).
