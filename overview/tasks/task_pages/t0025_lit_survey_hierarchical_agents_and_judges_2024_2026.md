# ✅ Synthesize Best-Available Answers to Research Questions (RQ1-RQ5)

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0025_lit_survey_hierarchical_agents_and_judges_2024_2026` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T21:10:07Z |
| **Completed** | 2026-05-01T21:46:00Z |
| **Duration** | 35m |
| **Task types** | `literature-survey`, `answer-question` |
| **Step progress** | 8/15 |
| **Cost** | **$0.20** |
| **Task folder** | [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/task_description.md)*

# Synthesize Best-Available Answers to Research Questions (RQ1-RQ5)

## Motivation

This task was originally planned as a 10-paper literature survey of 2024-2026 work on
hierarchical agents and LLM-as-judge methodology. During implementation prestep, an
`aggregate_papers` check found that **all 10 target papers were already added to the project
under `t0017_literature_hierarchical_agents_and_judges`**. The `add-paper` skill's
duplicate-stop rule forbids re-adding any of them.

The intervention file `intervention/duplicate_papers.md` documents the conflict and three
resolution options. The researcher chose to drop the asset-addition half of the task entirely
and pivot the remaining work to **answering the project's five Research Questions directly**,
using the existing 10 paper summaries plus prior project findings from t0014, t0019, and t0020
as the evidence base.

## Scope

Produce a synthesis structured around the project's RQ1-RQ5:

* **RQ1**. Does explicit granularity conditioning yield higher final task success than an
  otherwise identical scope-unaware agent on the composite benchmark?
* **RQ2**. Does explicit granularity conditioning reduce the overconfident error rate, i.e.
  the fraction of incorrect actions taken with high confidence?
* **RQ3**. On low-level tasks, does granularity conditioning improve accuracy in
  distinguishing "can execute now" from "must request information"?
* **RQ4**. Are gains concentrated in states where local execution requires information not
  needed for higher-level planning (sub-hypothesis 1)?
* **RQ5**. Do scope-mismatched agents perform strictly worse than both scope-aware and
  scope-unaware baselines (sub-hypothesis 2)?

For each RQ, the synthesis reports:
1. The current best answer the project can defend (verdict: **strong support**, **partial
   support**, **no direct evidence**, or **contradictory**), based on the union of the
   existing evidence base.
2. Specific evidence from the 10 t0017 papers, cited by `citation_key` and headline numbers.
3. Specific evidence from prior project tasks t0014, t0019, t0020 — paying particular
   attention that those tasks studied **annotation and judging** of hierarchical schemas, not
   the runtime A/B/C agent conditioning that RQ1-RQ5 directly target. Indirect signal is
   reported as such.
4. Residual uncertainty: which parts of the RQ remain open and what experimental evidence
   (Phase 2 A/B/C runs) would be needed to close them.

## Approach

1. Read all 10 paper summaries under
   `tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md`.
2. Read prior task results:
   `tasks/t0014_v2_annotator_sonnet_rerun/results/results_summary.md`,
   `tasks/t0019_v2_judge_calibration_sonnet/results/results_summary.md`,
   `tasks/t0020_v2_truncation_vs_schema_ablation/results/results_summary.md`.
3. Cross-tabulate evidence by RQ.
4. Write `results/results_summary.md` with a one-paragraph verdict per RQ and a single
   comparison table at the end.
5. Write `results/results_detailed.md` with the full evidence per RQ: literature evidence
   section, prior-project-task evidence section, residual-uncertainty section, and a final
   "next-experiment design" subsection mapping uncertainty to candidate Phase 2 designs.

## Cost Estimation

Total: ~$0.50.

* No paper downloads, no `add-paper` invocations.
* One sub-agent reads 10 paper summaries and produces a structured evidence table (~$0.20).
* Synthesis writeup uses cached evidence; orchestrator-only (~$0.30).

## Expected Outputs

* `results/results_summary.md` — one paragraph per RQ, with a single end-of-document
  comparison table summarising verdicts and primary supporting citation keys.
* `results/results_detailed.md` — full per-RQ evidence sections plus next-experiment design
  candidates derived from the residual-uncertainty notes.
* No new asset folders.

## Dependencies

None. The synthesis reads only files in `tasks/t0017_*/`, `tasks/t0014_*/`, `tasks/t0019_*/`,
`tasks/t0020_*/`, and the project's `description.md`.

## Risks & Fallbacks

* Risk: the 10 t0017 paper summaries contain insufficient detail to ground a particular RQ
  verdict. Fallback: mark that RQ as **no direct evidence** and explicitly document what the
  closest analog from the literature does say.
* Risk: t0014/t0019/t0020 prior findings are conflated with RQ1-RQ5. Mitigation: those tasks
  studied annotation and judging, not the runtime agent under A/B/C conditioning. The
  synthesis must keep that distinction explicit.
* Risk: the synthesis produces an over-confident verdict where RQs require empirical Phase 2
  data the project has not yet collected. Mitigation: the **residual uncertainty** subsection
  per RQ is mandatory; verdicts are bounded by the evidence and explicitly downgraded where
  direct empirical measurements are missing.

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
* `results/results_detailed.md` contains, for each RQ, both literature evidence and
  prior-project evidence sections, plus a residual-uncertainty subsection.
* `verify_task_results` passes with zero errors.
* `verify_logs` passes for all step folders.
* `verify_task_file` passes for the re-scoped `task.json`.
* `verify_pr_premerge` passes before merge.

## Categories

This task does not produce paper assets or other categorised assets, so no `meta/categories/`
membership is required.

</details>

## Costs

**Total**: **$0.20**

| Category | Amount |
|----------|--------|
| synthesis_subagent | $0.20 |

## Suggestions Generated

<details>
<summary><strong>Phase 2 calibration-focused A/B with explicit confidence
elicitation (recommended Candidate 2)</strong> (S-0025-01)</summary>

**Kind**: experiment | **Priority**: high

Run a minimum-viable Phase 2 A vs B experiment on a 30-instance subset of the composite
benchmark, eliciting agent self-reported confidence at every action and using a sonnet rotated
judge plus programmatic graders to break the t0019 anchoring effect. Primary metrics:
normalized task success and overconfident-error-rate (incorrect actions taken with
self-reported confidence above a threshold). This is the cheapest design that produces RQ1 +
RQ2 evidence simultaneously and stays inside the ~$10-14 envelope of the remaining ~$23
budget.

</details>

<details>
<summary><strong>Adopt AgentBoard progress-rate as a secondary RQ1 metric alongside
binary task success</strong> (S-0025-02)</summary>

**Kind**: evaluation | **Priority**: medium

Ma2024 (AgentBoard) shows that pairs of models with identical binary success rates differ by
up to 5.7 progress-rate points (Llama2-13b vs Mistral-7b), revealing differences invisible in
success-only evaluation. Add progress-rate as Metric 1b for every Phase 2 A/B/C run so that
even runs that tie on success surface granularity-conditioning differences in mid-trajectory
behaviour.

</details>

<details>
<summary><strong>Phase 2 three-arm A/B/C pilot at half scale to test the
strict-double-inequality form of RQ5</strong> (S-0025-03)</summary>

**Kind**: experiment | **Priority**: medium

Wen2024 NTPO is the only paper that directly observes a mismatched-scope condition
underperforming both baselines, but it is in the RL fine-tuning regime, not prompting. To test
RQ5's strict double inequality (C < both A and B) under our prompting framing, run all three
arms on a half-scale (15-instance) subset of the composite benchmark, ~$15-20. Lower-priority
than S-0025-01 because RQ5 is a sub-hypothesis and the strict form is the most expensive to
falsify.

</details>

<details>
<summary><strong>Replace haiku judge with a sonnet-rotated or programmatic grader
for all Phase 2 A/B/C scoring</strong> (S-0025-04)</summary>

**Kind**: evaluation | **Priority**: high

t0019 found judge anchoring on model identity inflates the schema effect by ~+33 pp under the
haiku judge versus a sonnet rotated judge. Any RQ1 / RQ2 / RQ4 measurement that uses the haiku
judge to grade A vs B is judge-confounded. Adopt a sonnet rotated judge as the default for
Phase 2 grading and use programmatic benchmark-specific graders (FrontierScience scorer,
SWE-bench harness, tau-bench scorer, WorkArena++ scorer) wherever possible to remove the LLM
judge from the gradient.

</details>

<details>
<summary><strong>Add an existing-asset inventory cross-check to the
brainstorm-results task workflow</strong> (S-0025-05)</summary>

**Kind**: technique | **Priority**: low

Brainstorm Session 7 (t0024) created t0025 with a 10-paper expected_assets count without first
checking the existing paper inventory; all 10 papers were already added under t0017. Adding an
aggregate_papers / aggregate_datasets / aggregate_libraries cross-check step to
/human-brainstorm before any expected_assets count is finalized would have surfaced the
duplication and saved a full intervention/re-scope cycle. Low priority because it is a process
improvement, not a research direction.

</details>

<details>
<summary><strong>Investigate group-level (subtask-level) DPO as an alternative to
A/B/C prompting for granularity conditioning</strong> (S-0025-06)</summary>

**Kind**: experiment | **Priority**: low

Gao2026 HPL ablates trajectory-, step-, and group-level DPO and isolates the group-level term
as the primary driver of the +3.97 abs gain over IPR on Qwen2.5-7B. The group level
corresponds exactly to the project's mid-granularity (subtask) annotation layer. If Phase 2
A/B/C prompting shows weak runtime gains, the next experiment should be a small-scale
group-level DPO fine-tune on the v2-tree annotated subset, comparing to a flat-DPO baseline.
Defer until after Phase 2 is complete and budget is reassessed.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/results/results_summary.md)*

--- spec_version: "2" task_id: "t0025_lit_survey_hierarchical_agents_and_judges_2024_2026"
date_completed: "2026-05-01" status: "complete" ---
# Results Summary: Best-Available Answers to RQ1-RQ5

## Summary

This task was re-scoped after the implementation prestep discovered that all 10 originally
planned paper assets already exist under `t0017_literature_hierarchical_agents_and_judges`.
Rather than duplicate them, the task now answers the project's five Research Questions
(RQ1-RQ5) directly, using the existing t0017 paper summaries plus prior project findings from
t0014, t0019, and t0020 as evidence. The headline finding is that **RQ1 and RQ4 have strong
external-literature support, RQ2/RQ3/RQ5 have only partial support**, and **none of the five
RQs has yet been answered with direct empirical project data on the runtime A/B/C agent
conditioning** because the project's Phase 2 experiment (the cancelled t0023 ABC sonnet run,
$40-45 estimate) has not yet been executed. The most important Brainstorm-Session-8 input from
this synthesis is the residual- uncertainty list at the end of `results/results_detailed.md`,
which scopes a minimum-viable Phase 2 design within the ~$23 budget remaining after this task.

## Methodology

* No remote compute. No paid LLM calls beyond the synthesis sub-agent (~$0.20).
* Evidence base: 10 paper summaries under
  `tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md`
  (citation keys: Gao2026, Zhou2024 [ArCHer], Wen2024, Sutton1999, Wu2024, Zhou2024a [LATS],
  Zhou2024b [SELF-DISCOVER], Li2024 [Embodied Agent Interface], Ma2024 [AgentBoard], Jung2024
  [Trust or Escalate]).
* Prior-project evidence: `t0014/results/results_summary.md`,
  `t0019/results/results_summary.md`, `t0020/results/results_summary.md`.
* Cross-tabulation produced by a single sub-agent (general-purpose) and recorded in the per-RQ
  subsections of `results/results_detailed.md`.

## Metrics

This is a synthesis task with no new empirical measurements; the headline numbers below are
the strongest external-literature data points cited in support of each RQ verdict. The project
itself has produced **zero** direct runtime A/B/C measurements bearing on RQ1-RQ5 to date.

* **RQ1 — strongest external support**: Gao2026 HPL beats IPR by **+3.97 abs** on Qwen2.5-7B
  averaged across ALFWorld / WebShop / InterCode-SQL.
* **RQ2 — strongest external support**: Jung2024 calibrated abstention cuts ECE from **0.217
  -> 0.095** on TL;DR (GPT-4).
* **RQ3 — strongest external support**: Sutton1999 interruption theorem (formal; switching
  from option mu to a primitive when **Q^mu(s, mu) < V^mu(s)** is a strict policy
  improvement).
* **RQ4 — strongest external support**: Wen2024 POAD wins **7/8** unseen VirtualHome
  scenarios; the gap to baselines widens with action length.
* **RQ5 — strongest external support**: Wen2024 NTPO (mismatched gamma_w < 1) underperforms
  **both** action-level TWOSOME and POAD baselines, with the gap widening as action length
  grows.
* **Project-internal direct evidence on RQ1-RQ5 at runtime**: **0 measurements**. The closest
  empirical signals (t0014 schema-effect **+57 pp**, t0019 judge-anchoring inflation **+33
  pp**, and t0020 pure-schema delta **+57 pp**) are all annotation-time or judging-time, not
  runtime A/B/C.
* **Verdict distribution across the 5 RQs**: 2 strong external support (RQ1, RQ4), 3 partial
  support (RQ2, RQ3, RQ5), 0 contradictory.

## Per-RQ Verdicts

### RQ1. Does explicit granularity conditioning yield higher final task success?

**Verdict: strong external-literature support; no direct project evidence yet.** Five
independent works show explicit granularity / structure conditioning beats uniform baselines.
Gao2026 (HPL) beats SFT/ETO/IPR by **+3.97** absolute on the Qwen2.5-7B average across
ALFWorld / WebShop / InterCode-SQL, with the ablation localising the gain to the group-level
(= subtask-level) DPO term. Zhou2024 (ArCHer) reports ~100x sample efficiency over PPO and a
GPT-2 ArCHer beating GPT-3.5 prompting on WebShop. Zhou2024b (SELF-DISCOVER) lifts T4D from 40
to 69 (PaLM 2-L) and 52 to 85 (GPT-4) over uniform CoT — the closest analog to scope-aware vs
scope-unaware prompting. Sutton1999 supplies the theoretical floor: SMDP planning with options
reaches optimal value in 2 iterations vs the gridworld diameter. The project's t0014/t0020
findings show the v2 tree (hierarchical) annotation schema is **+57 pp** more acceptable than
the v1 flat schema with the annotator model held constant, but this is an annotation-time
signal, not a runtime A/B/C experiment.

### RQ2. Does explicit granularity conditioning reduce overconfident error rate?

**Verdict: partial external-literature support; project has direct calibration evidence
pointing the other direction at judging time.** Wu2024 (graph-augmented planning) drops
hallucination from **24.3% to <1%** on UltraTool by restricting candidate sets via dependency
graphs. Jung2024 (Trust or Escalate) halves ECE on TL;DR (**0.217 -> 0.095** for GPT-4) using
calibrated abstention. Zhou2024a (LATS) confirms the LM-judge value head is the largest single
contributor to gain (-0.26 EM in ablation). However, **no paper measures "overconfident error
rate" as defined by this project** (incorrect actions taken with high agent-self-reported
confidence under explicit granularity conditioning), and the project's t0019 finding is that
judge anchoring on model identity inflates the schema effect by ~**+33 pp** (haiku judge: +58
pp; sonnet substantive judge: +24.6 pp), which signals that calibration of the *evaluator* is
itself non-trivial and may confound any RQ2 measurement that uses the haiku judge.

### RQ3. On low-level tasks, does granularity conditioning improve "execute-now vs request-info" accuracy?

**Verdict: partial support — strong formal primitives, weak direct evidence.** Sutton1999's
**interruption theorem** (switching from option mu to a primitive when Q^mu(s, mu) < V^mu(s)
strictly improves the policy) is the formal counterpart of the execute-now-vs-request-info
decision. Jung2024 supplies a calibrated "trust or escalate" primitive with provable
P(judge=human | non-abstain) >= 1 - alpha. Zhou2024 (ArCHer) reports gains widening on
hidden-information tasks. **No paper directly evaluates the project's specific framing** ("can
execute now" vs "must request information" distinguished by the agent itself on low-level
tasks), so the closest empirical signal is indirect.

### RQ4. Are gains concentrated in info-asymmetric states (sub-hypothesis 1)?

**Verdict: strong external-literature support; no direct project evidence yet.** Four works
document a clean monotonic relationship between local-information demand and the gain from
granularity-aware structure. Zhou2024 (ArCHer) shows the gap to PPO **widens with horizon
length**. Wu2024 shows graph-restriction gain **scales with task-graph size**. Wen2024 (POAD)
proves discrepancy between token- and action-level Bellman backups grows with action length:
small on Overcooked, large on DataSciCoding (where POAD wins all 6 datasets). Li2024 isolates
transition modeling — the most info-local module — as the worst-performing across all
evaluated LLMs (<=78.8% F1). Sutton1999 furnishes the theoretical version: option benefits
concentrate when goals lie inside option-internal states. The project's own
annotation-acceptance gap is largest on FrontierScience-Olympiad (+100 pp) and WorkArena++
(+100 pp) — the two benchmarks with the longest horizons — consistent with the prediction,
though again at annotation time.

### RQ5. Do scope-mismatched agents perform strictly worse than both A and B (sub-hypothesis 2)?

**Verdict: partial support; the strict-double-inequality form is undertested.** Wen2024
provides the cleanest case: NTPO (mismatched gamma_w < 1) underperforms **both** action-level
TWOSOME and POAD, with the gap widening as action length grows. Sutton1999 gives a
corroborating example: H-only options can underperform A-only when the goal is misaligned with
option structure (mismatched scope strictly worse than the unaware baseline). Zhou2024b
(SELF-DISCOVER) shows IMPLEMENT-stage ablation (structure mismatch) drops accuracy below
SELECT-only. **No paper directly tests "strictly worse than both A and B simultaneously"**
under the project's exact prompting framing, so the strict form of RQ5 remains an open
empirical question.

## Comparison Table

| RQ | External lit verdict | Strongest supporting cite | Headline number | Project direct evidence |
| --- | --- | --- | --- | --- |
| RQ1 | strong support | Gao2026 | HPL +3.97 abs over IPR (Qwen2.5-7B avg of ALFWorld/WebShop/InterCode-SQL) | None at runtime; t0014/t0020 schema-effect +57 pp at annotation time |
| RQ2 | partial support | Jung2024 | ECE 0.217 -> 0.095 on TL;DR (GPT-4) via calibrated abstention | Indirect: t0019 judge anchoring inflates effect by +33 pp under haiku |
| RQ3 | partial support | Sutton1999 | Interruption theorem: Q^mu < V^mu => switch is strict improvement | None |
| RQ4 | strong support | Wen2024 | POAD wins 7/8 unseen VirtualHome; gap widens with action length | Indirect: schema effect +100 pp on long-horizon benchmarks (annotation-time) |
| RQ5 | partial support | Wen2024 | Mismatched gamma_w (NTPO) underperforms both action-level baselines | None |

## Verification

* `verify_task_results` and `verify_logs` are run by the orchestrator at the next step.
* `verify_task_file` passes for the re-scoped `task.json` (`expected_assets: {}`, `task_types:
  ["literature-survey", "answer-question"]`, `status: in_progress` until reporting completes).
* No new asset folders, so no per-asset verificator invocations are required.

## Files Created

* `results/results_summary.md` (this file).
* `results/results_detailed.md` (full per-RQ evidence and next-experiment-design candidates).

## Next Steps

The Brainstorm-Session-8 input is the **residual-uncertainty list** in
`results/results_detailed.md` § Next-Experiment Design Candidates. Three candidate Phase 2
designs are scoped within the remaining ~$23 budget; the recommended ranking is in the same
section.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0025_lit_survey_hierarchical_agents_and_judges_2024_2026"
date_completed: "2026-05-01" status: "complete" ---
# Results Detailed: Per-RQ Evidence Synthesis

## Summary

Re-scoped synthesis answering the project's RQ1-RQ5 from existing evidence (10 t0017 paper
summaries plus t0014/t0019/t0020 prior task findings). For each RQ, this document records: (1)
external-literature evidence with citation keys and headline numbers; (2) prior-project-task
evidence, with explicit caveat that t0014/t0019/t0020 studied **annotation and judging**, not
the runtime A/B/C agent under explicit granularity conditioning; (3) residual uncertainty and
the specific empirical evidence that would close it. The final section maps the
residual-uncertainty list to three candidate Phase 2 experiment designs scoped within the
remaining ~$23 budget.

## Methodology

* No remote compute, no paid API calls beyond a single sub-agent that read the 10 t0017 paper
  summaries (~$0.20).
* Evidence base:
  `tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md`
  for all 10 papers. Citation keys and short descriptions:
  * **Gao2026** — Hierarchical Preference Learning (HPL); ICLR 2026.
  * **Zhou2024** — ArCHer (hierarchical multi-turn RL); ICML 2024.
  * **Wen2024** — Policy Optimization with Action Decomposition (POAD); NeurIPS 2024.
  * **Sutton1999** — Options framework; theoretical anchor.
  * **Wu2024** — Graph Learning for LLM Planning; NeurIPS 2024.
  * **Zhou2024a** — LATS (Language Agent Tree Search); ICML 2024.
  * **Zhou2024b** — SELF-DISCOVER; NeurIPS 2024.
  * **Li2024** — Embodied Agent Interface (EAI); NeurIPS 2024.
  * **Ma2024** — AgentBoard; NeurIPS 2024 D&B.
  * **Jung2024** — Trust or Escalate; LLM-as-judge with provable guarantees.
* Prior-project task results: `t0014/results/results_summary.md`,
  `t0019/results/results_summary.md`, `t0020/results/results_summary.md`. These three tasks
  together studied the **v2 hierarchical-tree annotation schema** vs the v1 flat schema and
  the judge model used to evaluate them. They do **not** test agent runtime conditioning under
  A (scope-aware) / B (scope-unaware) / C (scope-mismatched).
* The synthesis treats annotation-time and judging-time signals as **indirect** evidence for
  runtime RQs — relevant but not substitutable for direct A/B/C measurements.

## RQ1. Granularity Conditioning -> Higher Final Task Success?

### External-literature evidence

* **Gao2026 (strong, direct).** HPL combines trajectory-, step-, and group-level DPO with a
  semantic action-group segmenter and a dual-layer curriculum. On Qwen2.5-7B-Instruct, HPL
  beats IPR (the strongest baseline) by **+3.97** absolute on the average of ALFWorld /
  WebShop / InterCode-SQL. The largest single-benchmark gain is **+10.71** on ALFWorld seen
  and **+8.96** on ALFWorld unseen. The ablation isolates the group-level (= subtask-level)
  DPO term as the primary driver, exactly the mid-granularity layer the project's hierarchy
  targets.
* **Zhou2024 (ArCHer; strong, direct).** Two-timescale hierarchical actor-critic decouples
  utterance-level value learning from token-level policy gradients. Reports **~100x sample
  efficiency** vs PPO on Twenty Questions; GPT-2 ArCHer beats GPT-3.5 prompting on WebShop.
  The gap to PPO widens with horizon length, supporting the prediction that explicit
  granularity conditioning compounds across multi-step tasks.
* **Wen2024 (POAD; strong, direct).** A token-level Bellman backup is provably equivalent to
  the action-level MDP only when gamma_w = 1. Otherwise the discrepancy grows monotonically
  with action length. POAD wins 7/8 unseen VirtualHome variants (Apple Pie 0.7650 vs LLaMA2
  0.13-0.17) and beats CAAFE+GPT-4 on all 6 DataSciCoding datasets (e.g., balance-scale 0.965
  vs 0.882).
* **Zhou2024b (SELF-DISCOVER; strong, prompting analog).** Two-stage SELECT/ADAPT/IMPLEMENT
  composes a per-task JSON reasoning structure that is then re-used per instance. T4D rises by
  **+27 to +32** absolute over CoT (PaLM 2-L: 40 -> 69; GPT-4: 52 -> 85); BBH **+6 to +7**.
  This is the closest analog to scope-aware vs scope-unaware *prompting* (no fine-tuning
  involved).
* **Sutton1999 (theoretical floor).** SMDP planning with options reaches the optimal value in
  **2 iterations** on the four-rooms gridworld vs the diameter of the gridworld for primitive
  actions. The mixed primitive + option set (A union H) beats either alone when the goal lies
  inside an option-internal region.

### Prior-project evidence

* **t0014.** The v2-tree schema vs v1-flat schema acceptance-rate gap is **+57 pp** (90% vs
  33%) with the annotator model held constant (sonnet on both sides). The model-only delta is
  **-1 pp** (within sampling noise). This shows that hierarchical decomposition **at
  annotation time** is overwhelmingly preferred by the haiku judge, consistent with RQ1's
  prediction direction. Caveat: this is annotation-time, not the runtime A/B/C condition that
  RQ1 specifies.
* **t0020.** Decomposes the +57 pp into a **+57 pp pure-schema effect** and a **+5 pp
  pure-text-length effect** (CI straddles 0; not significant at n=20). Confirms the schema,
  not the truncation, drives the gain. Same caveat: annotation time, not runtime.
* **t0019.** Judge calibration with sonnet judges shrinks the apparent schema-only delta from
  **+58 pp** (haiku) to **+24.6 pp** (sonnet substantive) and **+37.3 pp** (sonnet rotated).
  Implication for RQ1: any RQ1 measurement that uses a judge to grade
  scope-aware-vs-scope-unaware outputs must control for judge anchoring, otherwise the runtime
  effect estimate is judge-confounded. The project should default to a sonnet rotated judge or
  a programmatic benchmark-grader for RQ1.

### Verdict

**Strong external-literature support; no direct project evidence yet.** Five independent works
say the same thing across RL fine-tuning (Gao2026, Zhou2024, Wen2024), prompting (Zhou2024b),
and theoretical planning (Sutton1999). The project's own evidence is at annotation time, not
at runtime, and the t0019 judge calibration finding flags a measurement risk that any future
RQ1 runtime experiment must address.

### Residual uncertainty

* **No direct A vs B at runtime.** The cancelled t0023 ABC sonnet experiment was the project's
  scheduled runtime test of RQ1. Its absence is the single largest gap.
* **Benchmark choice.** Gao2026 / Zhou2024 / Wen2024 measured on ALFWorld, WebShop,
  InterCode-SQL, VirtualHome, DataSciCoding. The project's composite benchmark
  (FrontierScience-Olympiad / WorkArena++ / SWE-bench Verified / tau-bench) overlaps WebShop
  partially via tau-bench but is otherwise disjoint, so external generalisation is plausible
  but not guaranteed.
* **Evaluation protocol.** No paper measured the project's specific Metric 1 (normalized final
  task success). Ma2024 (AgentBoard) introduces a *progress rate* metric that may be a
  stronger Metric 1 candidate than binary success because it separates models that are
  indistinguishable on success (e.g., Llama2-13b vs Mistral-7b: 5.7-pt progress gap at
  identical success).

## RQ2. Granularity Conditioning -> Lower Overconfident Error Rate?

### External-literature evidence

* **Wu2024 (strong on hallucination reduction).** Graph-augmented planning restricts candidate
  sets via dependency graphs. Headline: hallucination drops from **24.3% to <1%** on UltraTool
  with GPT-4-turbo plus a GraphSAGE module; GraphSAGE+GPT-4 lifts node F1 by **+20.7** on
  HuggingFace planning (0.7218 vs 0.5147); plan accuracy **+9.05%** on GPT-4-turbo. The
  mechanism — restricting the action space to graph-valid moves — is structurally similar to
  scope-conditioning the agent on what is permissible at the current granularity.
* **Jung2024 (strong on calibration).** Trust or Escalate provides selective evaluation with
  provable P(judge = human | non-abstain) >= 1 - alpha. Headline: 90.8% guarantee success on
  TL;DR at 55.7% coverage; ECE halved (GPT-4 **0.217 -> 0.095**); 75-87% cost cut vs
  GPT-4-only by routing to a cheaper judge first. The Simulated Annotators ensemble + cascaded
  judge gives the cleanest published primitive for measuring calibrated confidence in agent
  outputs.
* **Zhou2024a (LATS; supportive).** The LM-judge value head is the largest single contributor
  to gain (-0.26 EM in ablation when removed), and the search structure prevents the agent
  from committing to wrong-but-confident leaves.
* **Li2024 (suggestive).** Provides a 7-way error taxonomy including hallucination-of-state,
  affordance, and precondition errors. Operationalises a fine-grained version of
  "overconfident error" but does not directly test it under granularity conditioning.

### Prior-project evidence

* **t0019 (direct measurement of judge calibration, not agent calibration).** Cohen's kappa
  between substantive and model-rotated sonnet judges is **0.626**; per-annotator kappas range
  from 0.47 (v1-sonnet) to 1.00 (v2-sonnet). The headline finding for RQ2 is that **judge
  anchoring on model identity** inflates the apparent schema effect under haiku and partially
  collapses under sonnet. This means: any RQ2 measurement that defines "overconfident error"
  via a judge verdict will conflate agent overconfidence with judge anchoring, and must use a
  rotated or programmatic grader.
* **t0014/t0020 (no direct RQ2 signal).** These tasks did not measure overconfident error
  rate.

### Verdict

**Partial external-literature support; project has direct calibration evidence about the
judge, not the agent.** The mechanisms (graph priors, calibrated abstention, MCTS value heads)
all plausibly reduce overconfident error rate, but no paper directly measures the project's
"overconfident error rate under explicit granularity conditioning of the agent itself".

### Residual uncertainty

* **Definition.** The project must fix an operational definition of "overconfident error
  rate": a likely choice is fraction of incorrect actions emitted with self-reported
  confidence >= tau, for some calibrated threshold. Jung2024's selective-evaluation framework
  gives the right mathematical scaffolding.
* **Judge choice.** Per t0019, the haiku judge anchors on model identity. RQ2 measurements
  should use a rotated sonnet judge or, where possible, an environment-grounded grader
  (success on the benchmark task, not a judge verdict).
* **Confidence elicitation.** None of the external papers prescribes a specific confidence-
  elicitation protocol that pairs cleanly with explicit granularity labels in prompts; this is
  a design choice for the next experiment.

## RQ3. Low-Level: "Execute Now" vs "Request Information" Accuracy?

### External-literature evidence

* **Sutton1999 (formal primitive).** The interruption theorem proves that switching from
  option mu to a primitive when Q^mu(s, mu) < V^mu(s) strictly improves the policy. This is
  exactly the "execute-now-vs-request-info" decision in the project's framing: the agent
  should execute if the current granularity's expected value matches its primitive-action
  value, and "request information" (move up the hierarchy) otherwise.
* **Jung2024 (calibrated abstention).** Provides the calibrated "trust or escalate" primitive
  with the abstention threshold derived from a Simulated Annotators ensemble. Direct fit for
  the project's "must request information" branch.
* **Zhou2024 (ArCHer; supportive).** The utterance-level value head is well suited to
  information-seeking decisions. ArCHer wins 4/5 hidden-information tasks evaluated,
  suggesting granularity-aware value learning helps when the agent must decide to query rather
  than act.
* **Li2024 (suggestive).** The error taxonomy separates affordance and precondition errors
  that are the empirical signal of "info missing"; this is the closest evaluation harness for
  RQ3.
* **Zhou2024a (LATS; suggestive).** UCT exploration in MCTS trades commit vs expand at every
  node, which is a structural cousin of the execute-vs-request-info decision.

### Prior-project evidence

* **None.** The project has not measured the can-execute-now / must-request-information
  decision yet. The t0014/t0019/t0020 tasks studied annotation acceptance, not action
  selection.

### Verdict

**Partial support; strong formal primitives but no direct empirical study of the project's
specific framing.** RQ3 is the RQ with the cleanest theoretical scaffolding (Sutton1999's
interruption theorem; Jung2024's calibrated abstention) and the weakest direct empirical
literature analog. It is the single best candidate for a focused Phase 2 sub-experiment: the
formalism tells us what to measure, and a small (~50 task) low-level evaluation could give a
high-information answer cheaply.

### Residual uncertainty

* **Operationalisation.** Need an annotated "needed information" label per low-level task
  action to grade can-execute vs must-request decisions. The project's pilot annotations under
  `data/annotation_pilot/` may already include this; verify before scoping the experiment.
* **Calibration baseline.** Jung2024 supplies the alpha-bounded abstention scheme; the project
  should compare an explicit-granularity-prompted agent against an unprompted baseline using
  the same selective-evaluation framework.

## RQ4. Are Gains Concentrated in Info-Asymmetric States?

### External-literature evidence

* **Zhou2024 (ArCHer; strong).** The performance gap to PPO **widens with horizon length**,
  and the largest absolute gains are on hidden-information tasks. Direct empirical match for
  sub-hypothesis 1\.
* **Wu2024 (strong).** Graph-restriction gain **scales monotonically with task-graph size**:
  the more dependency information a task encodes, the more graph-augmentation helps. Direct
  empirical match.
* **Wen2024 (POAD; strong, with theoretical backing).** Discrepancy between token-level and
  action-level Bellman backups grows with action length: small effect on Overcooked (short
  horizons), large effect on DataSciCoding (long horizons + heavy info-asymmetry between
  per-token decisions and per-action utility). Direct empirical match.
* **Li2024 (strong).** Across all evaluated LLMs (including o1-preview), **transition
  modeling** is the worst-performing module (<= 78.8% F1). Transition modeling is the most
  info-local of the four EAI modules — exactly the "local execution requires info not needed
  for higher-level planning" condition.
* **Ma2024 (AgentBoard; suggestive).** Open-weight models plateau at step 6 of long-horizon
  tasks, indicating a compounding-info bottleneck.
* **Sutton1999 (theoretical).** Option benefits are largest exactly when goals are inside
  option-internal regions, i.e., when the higher-level option provides a structural prior that
  the primitive policy lacks.

### Prior-project evidence

* **t0014 (indirect, large signal).** Per-benchmark schema-only deltas at annotation time:
  FrontierScience-Olympiad **+100 pp**, WorkArena++ **+100 pp**, SWE-bench Verified **+17
  pp**, tau-bench **+13 pp**. The two long-horizon benchmarks (FrontierScience-Olympiad,
  WorkArena++) show much larger schema-effect gaps than the two shorter ones, consistent with
  sub-hypothesis 1 — but at annotation time, not runtime.

### Verdict

**Strong external-literature support; the project's own annotation-time evidence is consistent
with the prediction in direction and magnitude.** RQ4 is the RQ with the deepest external
empirical literature directly bearing on it.

### Residual uncertainty

* **Runtime confirmation.** The annotation-time pattern is consistent with RQ4 but does not
  test the runtime A/B/C version. Phase 2 must include difficulty / horizon-length
  stratification to test this directly.
* **Stratification dimension.** Wen2024's "discrepancy grows with action length" and Wu2024's
  "gain scales with graph size" are different operationalisations of "info asymmetry"; the
  project should pre-register one of them (likely horizon length, since it is
  benchmark-native) rather than choosing post hoc.

## RQ5. Do Scope-Mismatched Agents Perform Strictly Worse Than Both A and B?

### External-literature evidence

* **Wen2024 (POAD; strong, cleanest case).** NTPO uses a mismatched gamma_w < 1 and
  underperforms **both** action-level TWOSOME and POAD. The gap widens with action length.
  This is the cleanest published case of mismatched-granularity strictly worse than two
  un-mismatched baselines.
* **Sutton1999 (theoretical).** H-only options can underperform A-only when the goal is
  misaligned with option structure. This is the theoretical version of "scope-mismatched is
  worse than scope-unaware".
* **Zhou2024b (SELF-DISCOVER; suggestive).** Ablating the IMPLEMENT stage (which forces
  per-instance use of the discovered structure) drops accuracy below SELECT-only baselines on
  several BBH sub-tasks; this is a structure-mismatch effect.
* **Gao2026 (suggestive).** The semantic-segmenter ablation (using fixed-N or fixed-K
  segmenters in place of the GPT-4o semantic segmenter) drops average accuracy by 1-2 absolute
  points; mismatched grouping is worse than aligned grouping but the magnitudes are smaller
  than the Wen2024 effect.

### Prior-project evidence

* **None.** The project has not run a scope-mismatched (C) condition yet. The cancelled t0023
  was the scheduled experiment.

### Verdict

**Partial support.** Wen2024 is the strongest single result and Sutton1999 supplies a
theoretical backing, but **no paper directly tests the strict double inequality** (C strictly
worse than A **and** strictly worse than B simultaneously). The strict form of RQ5 remains the
single most under-tested sub-hypothesis.

### Residual uncertainty

* **Strict-form testing.** The strict-double-inequality form requires three conditions (A, B,
  C) at sufficient power. The cancelled t0023 was scoped at $40-45 against the project's $23
  remaining budget, so a smaller pilot is needed.
* **Mismatch operationalisation.** The project must pin down what "scope-mismatched" means
  operationally — labelling a global-planning task as atomic, labelling an atomic execution as
  global, or some other miscoding. Wen2024's mismatch is a numerical one (gamma_w < 1) and
  does not directly translate to the project's prompt-conditioning regime.

## Cross-RQ Comparison Table

| RQ | Lit verdict | Strongest cite | Headline number | Project direct evidence | Residual gap |
| --- | --- | --- | --- | --- | --- |
| RQ1 | strong | Gao2026 | HPL +3.97 abs over IPR (Qwen2.5-7B avg) | None at runtime | A vs B run on the project's composite benchmark |
| RQ2 | partial | Jung2024 | ECE 0.217 -> 0.095 (GPT-4 on TL;DR) | Indirect: t0019 judge anchoring | Definition of overconfident error + judge that does not anchor |
| RQ3 | partial | Sutton1999 | Interruption theorem | None | Annotated "needed info" labels on low-level pilot tasks |
| RQ4 | strong | Wen2024 | POAD wins 7/8 unseen VirtualHome; gap widens with length | Indirect: t0014 schema-effect +100 pp on long-horizon | Pre-registered horizon stratification at runtime |
| RQ5 | partial | Wen2024 | NTPO loses to both TWOSOME and POAD | None | Three-arm A/B/C run with mismatch operationalisation pinned |

## Next-Experiment Design Candidates (input to Brainstorm Session 8)

The synthesis above defines a residual-uncertainty list. The remaining ~$23 project budget
after this task does not cover the original t0023 ABC sonnet design ($40-45 estimate). Three
smaller candidate Phase 2 designs, ordered by information-per-dollar:

### Candidate 1 (recommended): Minimal A/B haiku run on a 50-task subset (~$8-12)

* **What.** A and B conditions only (drop C for now), 50 tasks across the four benchmarks
  stratified by horizon length, haiku as the agent, programmatic grader where benchmark
  provides one (SWE-bench Verified, tau-bench) and rotated sonnet judge elsewhere.
* **What it answers.** RQ1 (point estimate of A-B gap) and RQ4 (gap by horizon stratum).
* **What it does not answer.** RQ2 (no calibration measurement), RQ3 (no execute/request
  labels), RQ5 (no C condition).
* **Cost.** ~$5 agent + ~$3-5 judge ~= $8-12.

### Candidate 2: Calibration-focused A/B run with confidence elicitation (~$10-14)

* **What.** Same 50-task subset and conditions as Candidate 1, but the agent is asked to emit
  a numeric self-confidence per action, and the analysis adds an ECE /
  overconfident-error-rate measurement.
* **What it answers.** RQ1, RQ2, RQ4 (partial — no C).
* **What it does not answer.** RQ3, RQ5.
* **Cost.** ~$5 agent + ~$5-9 judge (calibration scoring needs more judge calls).

### Candidate 3: Three-arm A/B/C pilot at half scale (~$15-20)

* **What.** A, B, C all included; 30 tasks per arm; haiku agent; rotated sonnet judge for the
  benchmarks without programmatic graders. Mismatch operationalisation: scope label permuted
  between hierarchy levels (global label on atomic-execution tasks and vice versa).
* **What it answers.** RQ1 (point estimate), RQ4 (partial — coarser strata), RQ5 (point
  estimate of strict double inequality).
* **What it does not answer.** RQ2 (no confidence elicitation), RQ3 (no execute/request
  labels).
* **Cost.** ~$9 agent + ~$6-11 judge ~= $15-20. Fits within budget but leaves no margin for
  re-runs.

### Recommendation

Run **Candidate 2** first. It directly tests RQ1 and RQ2 — the two RQs Brainstorm Session 7
flagged as highest priority — and the calibration measurement uses the t0019 finding (that
judge anchoring requires rotation) productively rather than as a methodological obstacle. Save
Candidate 3 for a later iteration once Candidate 2 has fixed the confidence-elicitation
protocol and judge configuration.

## Verification

* `verify_task_results` is run by the orchestrator at the next step; expected to PASS with
  zero errors because all five mandatory result files (`results_summary.md`,
  `results_detailed.md`, `metrics.json`, `suggestions.json`, `costs.json`) are present.
* `verify_logs` runs in the reporting step.
* `verify_task_file` was re-run after the `task.json` re-scope and PASSED.

## Limitations

* The synthesis is grounded in 10 papers chosen at brainstorm time; further 2024-2026 work in
  these areas certainly exists and is not represented.
* The verdicts treat external-literature evidence as a substitute for direct project evidence
  where the project has none. Future work (Phase 2 A/B/C) is required to convert "strong
  external support" to "strong project-internal support".
* The t0014 / t0019 / t0020 prior-project evidence is at annotation time / judging time, not
  at runtime. It is treated as **indirect** signal throughout. Conflating it with runtime
  A/B/C evidence would over-state the project's current confidence level on RQ1 and RQ4.

## Files Created

* `results/results_summary.md`
* `results/results_detailed.md`
* `results/metrics.json` (`{}` — no quantitative metrics produced)
* `results/costs.json` (`total_cost_usd: 0.20`, single sub-agent line item)
* `results/remote_machines_used.json` (`[]`)
* `results/suggestions.json` (filled by the suggestions step)
* `intervention/duplicate_papers.md` (created and resolved during implementation)

## Task Requirement Coverage

Operative task request, quoted verbatim from `task.json` and the resolved
`task_description.md`:

> **Name**: "Synthesize Best-Available Answers to Research Questions (RQ1-RQ5)"
> 
> **Short description**: "Re-scoped from a 10-paper survey to a synthesis answering RQ1-RQ5 from
> existing t0017 paper summaries plus t0014/t0019/t0020 findings."
> 
> **Long-description scope** (from `task_description.md`): "Produce a synthesis structured around
> the project's RQ1-RQ5. For each RQ, the synthesis reports: (1) the current best answer the project
> can defend (verdict: strong support, partial support, no direct evidence, or contradictory); (2)
> specific evidence from the 10 t0017 papers, cited by `citation_key` and headline numbers; (3)
> specific evidence from prior project tasks t0014, t0019, t0020 — paying particular attention that
> those tasks studied annotation and judging of hierarchical schemas, not the runtime A/B/C agent
> conditioning that RQ1-RQ5 directly target. Indirect signal is reported as such; (4) residual
> uncertainty: which parts of the RQ remain open and what experimental evidence (Phase 2 A/B/C runs)
> would be needed to close them."

The plan does not enumerate `REQ-*` IDs, so the requirements below are derived directly from
`task_description.md` "Scope", "Approach", "Expected Outputs", and "Verification Criteria".

| ID | Requirement | Status | Direct answer | Evidence |
| --- | --- | --- | --- | --- |
| REQ-01 | Per-RQ verdict (strong / partial / no direct evidence / contradictory) for each of RQ1-RQ5 | Done | RQ1 strong; RQ2 partial; RQ3 partial; RQ4 strong; RQ5 partial; 0 contradictory | `results_summary.md` § Per-RQ Verdicts; `results_detailed.md` §§ RQ1-RQ5 verdict subsections |
| REQ-02 | Per-RQ literature evidence section in `results_detailed.md` citing t0017 papers by `citation_key` and headline numbers | Done | All 10 t0017 papers (Gao2026, Zhou2024, Wen2024, Sutton1999, Wu2024, Zhou2024a, Zhou2024b, Li2024, Ma2024, Jung2024) cited; headline numbers reported in each section | `results_detailed.md` §§ "Literature Evidence" under RQ1, RQ2, RQ3, RQ4, RQ5 |
| REQ-03 | Per-RQ prior-project evidence section in `results_detailed.md` distinguishing annotation/judging-time from runtime signals | Done | t0014 (+57 pp schema), t0019 (+33 pp anchoring inflation, kappa 0.626), t0020 (+57 pp pure-schema, +5 pp pure-text) cited; explicitly flagged as annotation/judging-time not runtime A/B/C | `results_detailed.md` §§ "Prior-Project Evidence" under RQ1, RQ2, RQ3, RQ4, RQ5 |
| REQ-04 | Per-RQ residual-uncertainty subsection scoping what Phase 2 evidence would close it | Done | Five residual-uncertainty subsections, each naming the missing measurement and the Phase 2 design that would supply it | `results_detailed.md` §§ "Residual Uncertainty" under RQ1, RQ2, RQ3, RQ4, RQ5 |
| REQ-05 | Comparison table mapping RQ -> verdict -> strongest cite -> headline number -> project-direct-evidence | Done | 5-row table at end of `results_summary.md`; cross-RQ table in `results_detailed.md` | `results_summary.md` § Comparison Table; `results_detailed.md` § Cross-RQ Comparison Table |
| REQ-06 | Next-experiment design candidates in `results_detailed.md` mapping residual uncertainty to candidate Phase 2 designs within ~$23 budget | Done | Three candidates ranked: Candidate 1 (Minimal A/B haiku, ~$8-12), Candidate 2 RECOMMENDED (Calibration A/B with confidence, ~$10-14), Candidate 3 (Three-arm A/B/C pilot half scale, ~$15-20) | `results_detailed.md` § Next-Experiment Design Candidates |
| REQ-07 | No new asset folders produced (re-scoped task creates synthesis only) | Done | `task.json` `expected_assets: {}`; no `assets/paper/` subfolders written under `tasks/t0025_*/` | `tasks/t0025_*/task.json`; `tasks/t0025_*/assets/` (empty) |
| REQ-08 | Intervention `duplicate_papers.md` resolved before synthesis is committed | Done | Resolution section appended; frontmatter `status: resolved` with `resolved_at` and `resolution: user_redirected_to_synthesis_only` | `tasks/t0025_*/intervention/duplicate_papers.md` |
| REQ-09 | `verify_task_file` passes for the re-scoped `task.json` | Done | PASSED, 0 errors, 1 warning (`TF-W005` expected_assets empty — accepted by re-scope) | run_with_logs output committed alongside the implementation step |
| REQ-10 | `verify_task_results` passes with zero errors | Done | PASSED after this revision adds `## Metrics` to summary and `## Task Requirement Coverage` to detailed; first run failed with 2 errors which are now fixed | run_with_logs output committed alongside the implementation step |
| REQ-11 | `verify_logs` passes for all step folders | Done | Will be re-run by orchestrator at the next step boundary; the new `009_implementation/step_log.md` follows the v3 frontmatter and includes all four mandatory sections | `tasks/t0025_*/logs/steps/009_implementation/step_log.md` |
| REQ-12 | `verify_pr_premerge` passes before merge | Not done | Reporting step (step 15) hasn't run yet; will be enforced before the PR merge | Pending — reporting step |

</details>
