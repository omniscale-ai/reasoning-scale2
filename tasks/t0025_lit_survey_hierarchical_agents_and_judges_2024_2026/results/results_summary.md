---
spec_version: "2"
task_id: "t0025_lit_survey_hierarchical_agents_and_judges_2024_2026"
date_completed: "2026-05-01"
status: "complete"
---
# Results Summary: Best-Available Answers to RQ1-RQ5

## Summary

This task was re-scoped after the implementation prestep discovered that all 10 originally planned
paper assets already exist under `t0017_literature_hierarchical_agents_and_judges`. Rather than
duplicate them, the task now answers the project's five Research Questions (RQ1-RQ5) directly, using
the existing t0017 paper summaries plus prior project findings from t0014, t0019, and t0020 as
evidence. The headline finding is that **RQ1 and RQ4 have strong external-literature support,
RQ2/RQ3/RQ5 have only partial support**, and **none of the five RQs has yet been answered with
direct empirical project data on the runtime A/B/C agent conditioning** because the project's Phase
2 experiment (the cancelled t0023 ABC sonnet run, $40-45 estimate) has not yet been executed. The
most important Brainstorm-Session-8 input from this synthesis is the residual- uncertainty list at
the end of `results/results_detailed.md`, which scopes a minimum-viable Phase 2 design within the
~$23 budget remaining after this task.

## Methodology

* No remote compute. No paid LLM calls beyond the synthesis sub-agent (~$0.20).
* Evidence base: 10 paper summaries under
  `tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md`
  (citation keys: Gao2026, Zhou2024 [ArCHer], Wen2024, Sutton1999, Wu2024, Zhou2024a [LATS],
  Zhou2024b [SELF-DISCOVER], Li2024 [Embodied Agent Interface], Ma2024 [AgentBoard], Jung2024
  [Trust or Escalate]).
* Prior-project evidence: `t0014/results/results_summary.md`, `t0019/results/results_summary.md`,
  `t0020/results/results_summary.md`.
* Cross-tabulation produced by a single sub-agent (general-purpose) and recorded in the per-RQ
  subsections of `results/results_detailed.md`.

## Metrics

This is a synthesis task with no new empirical measurements; the headline numbers below are the
strongest external-literature data points cited in support of each RQ verdict. The project itself
has produced **zero** direct runtime A/B/C measurements bearing on RQ1-RQ5 to date.

* **RQ1 — strongest external support**: Gao2026 HPL beats IPR by **+3.97 abs** on Qwen2.5-7B
  averaged across ALFWorld / WebShop / InterCode-SQL.
* **RQ2 — strongest external support**: Jung2024 calibrated abstention cuts ECE from **0.217 ->
  0.095** on TL;DR (GPT-4).
* **RQ3 — strongest external support**: Sutton1999 interruption theorem (formal; switching from
  option mu to a primitive when **Q^mu(s, mu) < V^mu(s)** is a strict policy improvement).
* **RQ4 — strongest external support**: Wen2024 POAD wins **7/8** unseen VirtualHome scenarios; the
  gap to baselines widens with action length.
* **RQ5 — strongest external support**: Wen2024 NTPO (mismatched gamma_w < 1) underperforms **both**
  action-level TWOSOME and POAD baselines, with the gap widening as action length grows.
* **Project-internal direct evidence on RQ1-RQ5 at runtime**: **0 measurements**. The closest
  empirical signals (t0014 schema-effect **+57 pp**, t0019 judge-anchoring inflation **+33 pp**, and
  t0020 pure-schema delta **+57 pp**) are all annotation-time or judging-time, not runtime A/B/C.
* **Verdict distribution across the 5 RQs**: 2 strong external support (RQ1, RQ4), 3 partial support
  (RQ2, RQ3, RQ5), 0 contradictory.

## Per-RQ Verdicts

### RQ1. Does explicit granularity conditioning yield higher final task success?

**Verdict: strong external-literature support; no direct project evidence yet.** Five independent
works show explicit granularity / structure conditioning beats uniform baselines. Gao2026 (HPL)
beats SFT/ETO/IPR by **+3.97** absolute on the Qwen2.5-7B average across ALFWorld / WebShop /
InterCode-SQL, with the ablation localising the gain to the group-level (= subtask-level) DPO term.
Zhou2024 (ArCHer) reports ~100x sample efficiency over PPO and a GPT-2 ArCHer beating GPT-3.5
prompting on WebShop. Zhou2024b (SELF-DISCOVER) lifts T4D from 40 to 69 (PaLM 2-L) and 52 to 85
(GPT-4) over uniform CoT — the closest analog to scope-aware vs scope-unaware prompting. Sutton1999
supplies the theoretical floor: SMDP planning with options reaches optimal value in 2 iterations vs
the gridworld diameter. The project's t0014/t0020 findings show the v2 tree (hierarchical)
annotation schema is **+57 pp** more acceptable than the v1 flat schema with the annotator model
held constant, but this is an annotation-time signal, not a runtime A/B/C experiment.

### RQ2. Does explicit granularity conditioning reduce overconfident error rate?

**Verdict: partial external-literature support; project has direct calibration evidence pointing the
other direction at judging time.** Wu2024 (graph-augmented planning) drops hallucination from
**24.3% to <1%** on UltraTool by restricting candidate sets via dependency graphs. Jung2024 (Trust
or Escalate) halves ECE on TL;DR (**0.217 -> 0.095** for GPT-4) using calibrated abstention.
Zhou2024a (LATS) confirms the LM-judge value head is the largest single contributor to gain (-0.26
EM in ablation). However, **no paper measures "overconfident error rate" as defined by this
project** (incorrect actions taken with high agent-self-reported confidence under explicit
granularity conditioning), and the project's t0019 finding is that judge anchoring on model identity
inflates the schema effect by ~**+33 pp** (haiku judge: +58 pp; sonnet substantive judge: +24.6 pp),
which signals that calibration of the *evaluator* is itself non-trivial and may confound any RQ2
measurement that uses the haiku judge.

### RQ3. On low-level tasks, does granularity conditioning improve "execute-now vs request-info" accuracy?

**Verdict: partial support — strong formal primitives, weak direct evidence.** Sutton1999's
**interruption theorem** (switching from option mu to a primitive when Q^mu(s, mu) < V^mu(s)
strictly improves the policy) is the formal counterpart of the execute-now-vs-request-info decision.
Jung2024 supplies a calibrated "trust or escalate" primitive with provable P(judge=human |
non-abstain) >= 1 - alpha. Zhou2024 (ArCHer) reports gains widening on hidden-information tasks.
**No paper directly evaluates the project's specific framing** ("can execute now" vs "must request
information" distinguished by the agent itself on low-level tasks), so the closest empirical signal
is indirect.

### RQ4. Are gains concentrated in info-asymmetric states (sub-hypothesis 1)?

**Verdict: strong external-literature support; no direct project evidence yet.** Four works document
a clean monotonic relationship between local-information demand and the gain from granularity-aware
structure. Zhou2024 (ArCHer) shows the gap to PPO **widens with horizon length**. Wu2024 shows
graph-restriction gain **scales with task-graph size**. Wen2024 (POAD) proves discrepancy between
token- and action-level Bellman backups grows with action length: small on Overcooked, large on
DataSciCoding (where POAD wins all 6 datasets). Li2024 isolates transition modeling — the most
info-local module — as the worst-performing across all evaluated LLMs (<=78.8% F1). Sutton1999
furnishes the theoretical version: option benefits concentrate when goals lie inside option-internal
states. The project's own annotation-acceptance gap is largest on FrontierScience-Olympiad (+100 pp)
and WorkArena++ (+100 pp) — the two benchmarks with the longest horizons — consistent with the
prediction, though again at annotation time.

### RQ5. Do scope-mismatched agents perform strictly worse than both A and B (sub-hypothesis 2)?

**Verdict: partial support; the strict-double-inequality form is undertested.** Wen2024 provides the
cleanest case: NTPO (mismatched gamma_w < 1) underperforms **both** action-level TWOSOME and POAD,
with the gap widening as action length grows. Sutton1999 gives a corroborating example: H-only
options can underperform A-only when the goal is misaligned with option structure (mismatched scope
strictly worse than the unaware baseline). Zhou2024b (SELF-DISCOVER) shows IMPLEMENT-stage ablation
(structure mismatch) drops accuracy below SELECT-only. **No paper directly tests "strictly worse
than both A and B simultaneously"** under the project's exact prompting framing, so the strict form
of RQ5 remains an open empirical question.

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
* `verify_task_file` passes for the re-scoped `task.json` (`expected_assets: {}`,
  `task_types: ["literature-survey", "answer-question"]`, `status: in_progress` until reporting
  completes).
* No new asset folders, so no per-asset verificator invocations are required.

## Files Created

* `results/results_summary.md` (this file).
* `results/results_detailed.md` (full per-RQ evidence and next-experiment-design candidates).

## Next Steps

The Brainstorm-Session-8 input is the **residual-uncertainty list** in `results/results_detailed.md`
§ Next-Experiment Design Candidates. Three candidate Phase 2 designs are scoped within the remaining
~$23 budget; the recommended ranking is in the same section.
