# Synthesize Best-Available Answers to Research Questions (RQ1-RQ5)

## Motivation

This task was originally planned as a 10-paper literature survey of 2024-2026 work on hierarchical
agents and LLM-as-judge methodology. During implementation prestep, an `aggregate_papers` check
found that **all 10 target papers were already added to the project under
`t0017_literature_hierarchical_agents_and_judges`**. The `add-paper` skill's duplicate-stop rule
forbids re-adding any of them.

The intervention file `intervention/duplicate_papers.md` documents the conflict and three resolution
options. The researcher chose to drop the asset-addition half of the task entirely and pivot the
remaining work to **answering the project's five Research Questions directly**, using the existing
10 paper summaries plus prior project findings from t0014, t0019, and t0020 as the evidence base.

## Scope

Produce a synthesis structured around the project's RQ1-RQ5:

* **RQ1**. Does explicit granularity conditioning yield higher final task success than an otherwise
  identical scope-unaware agent on the composite benchmark?
* **RQ2**. Does explicit granularity conditioning reduce the overconfident error rate, i.e. the
  fraction of incorrect actions taken with high confidence?
* **RQ3**. On low-level tasks, does granularity conditioning improve accuracy in distinguishing "can
  execute now" from "must request information"?
* **RQ4**. Are gains concentrated in states where local execution requires information not needed
  for higher-level planning (sub-hypothesis 1)?
* **RQ5**. Do scope-mismatched agents perform strictly worse than both scope-aware and scope-unaware
  baselines (sub-hypothesis 2)?

For each RQ, the synthesis reports:
1. The current best answer the project can defend (verdict: **strong support**, **partial support**,
   **no direct evidence**, or **contradictory**), based on the union of the existing evidence base.
2. Specific evidence from the 10 t0017 papers, cited by `citation_key` and headline numbers.
3. Specific evidence from prior project tasks t0014, t0019, t0020 — paying particular attention that
   those tasks studied **annotation and judging** of hierarchical schemas, not the runtime A/B/C
   agent conditioning that RQ1-RQ5 directly target. Indirect signal is reported as such.
4. Residual uncertainty: which parts of the RQ remain open and what experimental evidence (Phase 2
   A/B/C runs) would be needed to close them.

## Approach

1. Read all 10 paper summaries under
   `tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md`.
2. Read prior task results: `tasks/t0014_v2_annotator_sonnet_rerun/results/results_summary.md`,
   `tasks/t0019_v2_judge_calibration_sonnet/results/results_summary.md`,
   `tasks/t0020_v2_truncation_vs_schema_ablation/results/results_summary.md`.
3. Cross-tabulate evidence by RQ.
4. Write `results/results_summary.md` with a one-paragraph verdict per RQ and a single comparison
   table at the end.
5. Write `results/results_detailed.md` with the full evidence per RQ: literature evidence section,
   prior-project-task evidence section, residual-uncertainty section, and a final "next-experiment
   design" subsection mapping uncertainty to candidate Phase 2 designs.

## Cost Estimation

Total: ~$0.50.

* No paper downloads, no `add-paper` invocations.
* One sub-agent reads 10 paper summaries and produces a structured evidence table (~$0.20).
* Synthesis writeup uses cached evidence; orchestrator-only (~$0.30).

## Expected Outputs

* `results/results_summary.md` — one paragraph per RQ, with a single end-of-document comparison
  table summarising verdicts and primary supporting citation keys.
* `results/results_detailed.md` — full per-RQ evidence sections plus next-experiment design
  candidates derived from the residual-uncertainty notes.
* No new asset folders.

## Dependencies

None. The synthesis reads only files in `tasks/t0017_*/`, `tasks/t0014_*/`, `tasks/t0019_*/`,
`tasks/t0020_*/`, and the project's `description.md`.

## Risks & Fallbacks

* Risk: the 10 t0017 paper summaries contain insufficient detail to ground a particular RQ verdict.
  Fallback: mark that RQ as **no direct evidence** and explicitly document what the closest analog
  from the literature does say.
* Risk: t0014/t0019/t0020 prior findings are conflated with RQ1-RQ5. Mitigation: those tasks studied
  annotation and judging, not the runtime agent under A/B/C conditioning. The synthesis must keep
  that distinction explicit.
* Risk: the synthesis produces an over-confident verdict where RQs require empirical Phase 2 data
  the project has not yet collected. Mitigation: the **residual uncertainty** subsection per RQ is
  mandatory; verdicts are bounded by the evidence and explicitly downgraded where direct empirical
  measurements are missing.

## Time Estimation

~30-45 minutes of agent execution.

## Assets Needed

None.

## Expected Assets

None. The deliverable is the synthesis written to `results/`.

## Remote Machines

None.

## Verification Criteria

* `results/results_summary.md` contains a section for each of RQ1, RQ2, RQ3, RQ4, RQ5 with an
  explicit verdict label and primary supporting citations.
* `results/results_detailed.md` contains, for each RQ, both literature evidence and prior-project
  evidence sections, plus a residual-uncertainty subsection.
* `verify_task_results` passes with zero errors.
* `verify_logs` passes for all step folders.
* `verify_task_file` passes for the re-scoped `task.json`.
* `verify_pr_premerge` passes before merge.

## Categories

This task does not produce paper assets or other categorised assets, so no `meta/categories/`
membership is required.
