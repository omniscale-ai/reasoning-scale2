# Task Success Rate

**Key**: `task_success_rate` | **Unit**: accuracy | **Results**: 25

[Back to all metrics](README.md)

| # | Task | Variant | Value |
|---|------|---------|-------|
| 1 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v2-sonnet judged by substantive-sonnet | **1.0** |
| 2 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v2-sonnet judged by model-rotated-sonnet | **1.0** |
| 3 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v2-haiku judged by model-rotated-sonnet | **0.9565** |
| 4 | [v2 Truncation vs Schema Ablation](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) | v2 tree schema, full untruncated problem text | **0.95** |
| 5 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v2-haiku judged by original-haiku | **0.913** |
| 6 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v2-haiku judged by substantive-sonnet | **0.913** |
| 7 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v2-sonnet judged by original-haiku | **0.9** |
| 8 | [v2 Truncation vs Schema Ablation](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) | v2 tree schema, problem truncated to 1500 chars | **0.9** |
| 9 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v1-sonnet judged by substantive-sonnet | **0.6667** |
| 10 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v1-sonnet judged by model-rotated-sonnet | **0.5833** |
| 11 | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) | v1-sonnet judged by original-haiku | **0.3333** |
| 12 | [v2 Truncation vs Schema Ablation](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) | v1 flat schema, problem truncated to 1500 chars | **0.3333** |
| 13 | [Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) | C — mismatched-strategy adversarial | **0.11564625850340136** |
| 14 | [Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) | C — matched_mismatch_v2 over plan_and_solve_v3 (adversarial) | **0.05384615384615385** |
| 15 | [Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) | A — scope-aware ReAct (reused from t0026) | **0.046153846153846156** |
| 16 | [Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) | B — plan_and_solve_v3 with bounded plan-recovery chain | **0.046153846153846156** |
| 17 | [Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) | A — scope-aware ReAct | **0.04081632653061224** |
| 18 | [Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) | B — Plan-and-Solve v2 | **0.04081632653061224** |
| 19 | [Phase 2 A/B/C smoke harness on FrontierScience subset](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) | Condition A: scope-aware ReAct | **0.025** |
| 20 | [Phase 2 A/B/C smoke harness on FrontierScience subset](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) | Condition B: scope-unaware Plan-and-Solve | **0.0** |
| 21 | [Phase 2 A/B/C smoke harness on FrontierScience subset](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) | Condition C: scope-mismatched (random) | **0.0** |
| 22 | [Plan-and-Solve v2 with final_confidence Field](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) | Condition A: scope-aware ReAct | **0.0** |
| 23 | [Plan-and-Solve v2 with final_confidence Field](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) | Condition B: scope-unaware Plan-and-Solve v2 | **0.0** |
| 24 | [Plan-and-Solve v2 with final_confidence Field](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) | Condition C: scope-mismatched (random) | **0.0** |
| 25 | [RQ1/RQ4 no-new-API preliminary salvage on existing t0026/t0027 outputs](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) | — | — |
