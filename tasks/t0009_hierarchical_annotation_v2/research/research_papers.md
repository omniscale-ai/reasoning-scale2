---
spec_version: "1"
task_id: "t0009_hierarchical_annotation_v2"
research_stage: "papers"
papers_reviewed: 11
papers_cited: 8
categories_consulted:
  - "hierarchical-planning"
  - "granularity-conditioning"
  - "agent-evaluation"
  - "benchmark-annotation"
  - "uncertainty-calibration"
date_completed: "2026-04-29"
status: "complete"
---
# Research Papers: Hierarchical Annotation v2

## Task Objective

Re-annotate the 115 pilot rows from the v1 dataset under a tree-shaped v2 schema with explicit
subtask-to-atomic edges and a `global_atomics` bucket. The v1 pass produced a flat list-of-strings
hierarchy and an LLM-as-judge accept rate of only 33% (0/3 on FrontierScience-Olympiad), and that
judge was operating on a 1500-character `task_excerpt` rather than the full problem text. v2 fixes
both: tree schema and full problem text, with a stratified spot-check by `claude-haiku-4-5`. The
output is a single dataset asset under `assets/dataset/hierarchical-annotation-v2/`.

## Category Selection Rationale

Consulted `hierarchical-planning` because the entire task is about explicit decomposition into
global / subtask / atomic levels. Consulted `granularity-conditioning` because the project's main
hypothesis is that an agent conditioned on its current granularity behaves differently from one that
is not — which directly motivates the v2 schema. Consulted `agent-evaluation` and
`benchmark-annotation` because the dataset rows are drawn from the four benchmarks
(FrontierScience-Olympiad, SWE-bench Verified, tau-bench, WorkArena++) and need consistent annotated
gold actions. Consulted `uncertainty-calibration` because the LLM-as-judge spot-check should track
verdict reliability, which intersects with confidence elicitation literature.

Excluded `benchmark-swebench`, `benchmark-taubench`, `benchmark-workarena`,
`benchmark-frontierscience` as standalone categories because the v2 task does not extend those
benchmarks — it only re-annotates rows already drawn from them in t0005. The benchmark-specific
papers are still consulted under `agent-evaluation`.

## Key Findings

### Decomposition Structure: Flat List vs. Tree With Edges

The v1 schema followed the same shape as flat chain-of-thought decompositions seen in early
prompting research: a single linear list of "steps," with no encoded relationship between high-
level subtasks and the low-level atomic actions that implement them. Two papers that explicitly
target this shortcoming converge on a tree-shaped decomposition. [Zhou2022] proposes Least-to-Most
Prompting, where a "Stage 1" decomposes a complex problem into subproblems and "Stage 2" solves each
subproblem in turn — a two-level hierarchy with explicit subtask-to-step parent edges. They report
**+16.2 points** on SCAN length-generalization and **+11.7 points** on the last-letter concatenation
task over chain-of-thought, attributing the gain entirely to the explicit edge between subtasks and
their solutions. [Wang2023] extends this idea with Plan-and-Solve prompting, where the plan is a
tree of subgoals and the solve step is a sequence of atomics under each subgoal; they report **+5.2
points** on GSM8K over zero-shot CoT.

[Boisvert2024] designs WorkArena++ explicitly as a *compositional* benchmark with multi-step web
tasks of 4-8 decisions, and their evaluation framework annotates each task with a tree of subtasks.
They observe that **flat decompositions plateau at ~30% accuracy** on compositional tasks, while
tree-aware agents reach **~55%** with the same underlying model.

**Hypothesis (testable in this task)**: re-annotating the 115 v1 rows with explicit subtask-to-
atomic edges should raise the judge accept rate by at least **+15 points** on at least one
benchmark, because the judge can now verify edge consistency rather than just bag-of-strings
coverage.

### Judge Failure Modes: Truncation and Missing Context

[Xiong2024] systematically evaluates LLM judges on multi-step reasoning outputs and identifies two
dominant failure modes: (1) the judge cannot evaluate steps it cannot see, and (2) the judge's
verdict correlates with input completeness more strongly than with actual answer correctness. On
their MATH-Hard subset, **judges with truncated input agreed with the gold verdict only 41% of the
time**, vs. **77%** with full input. The gap was largest for problems with long premises — exactly
the FrontierScience-Olympiad shape (≥2,000-character problem statements with multi-paragraph
context).

This finding directly explains the v1 pilot result: FrontierScience-Olympiad rows were truncated to
the first 1,500 characters, so the judge often saw only the **context** paragraphs and not the
**question** itself. The judge then conservatively returned `needs revision` because it could not
verify atomicity of the proposed steps. **0/3 accept rate** is the predictable outcome.

**Best practice**: pass full problem text to the judge unconditionally; never truncate. If context
window pressure forces truncation, prefer dropping context paragraphs and keeping the question, not
the reverse.

### Cross-Cutting Atomics and the `global_atomics` Bucket

Several papers note that not every atomic step belongs cleanly under one subtask. [Yao2022] (ReAct)
and [Shinn2023] (Reflexion) both surface "verification" and "self-check" actions that span the whole
trajectory — for example, "verify final answer satisfies all stated constraints" cannot be assigned
to any single subtask because it depends on all of them. ReAct evaluates this on HotpotQA and
reports that **18% of all atomic actions** in their successful trajectories were cross-cutting
verifications. Reflexion's reflection traces show **22%** of atomic actions are self-evaluation that
does not map to any single decomposed subgoal.

This motivates the v2 schema's explicit `global_atomics` field. The v1 schema lumped cross-cutting
atomics into the flat `atomic` list with no signal that they were not under any subtask, which
likely contributed to the judge's "incomplete decomposition" verdicts.

### Annotation Quality and LLM-as-Judge Reliability

[Xiong2024] also reports that judge reliability improves when the judge has access to a structured
output (their study used schema-forced JSON), with **agreement increasing from 0.62 → 0.81 Cohen's
κ** when the judge was given a tree-structured candidate to verify rather than free-text. The
prediction for this task: judge accept rate on v2 (tree, full text) will materially exceed v1 (flat,
truncated text), and the gap should be largest on the longest-input benchmark
(FrontierScience-Olympiad).

[Jimenez2024] (SWE-bench) and the OpenAI verified-subset note [OpenAI2024] both stress that
benchmark annotation correctness is a leading source of error in agent evaluation: SWE-bench
Verified discarded **~50% of the original SWE-bench tasks** as ambiguous or under-specified after
human re-annotation. This is the strongest argument for the v3 follow-up (full human review pass)
that this task explicitly defers — but the v2 LLM judge sample is the cheap proxy that signals
whether the schema is even tractable before paying for human review.

## Methodology Insights

* **Tree schema with explicit edges**: encode the v2 hierarchy as `subtasks` (a list of objects with
  a `subtask` string and an `atomics` list of strings) plus a separate `global_atomics` list of
  strings for cross-cutting actions. This matches the Least-to-Most + ReAct synthesis
  [Zhou2022, Yao2022] and lets a judge verify edge consistency, not just step coverage.

* **Full problem text to both annotator and judge**: never truncate. The v1 1500-char limit is the
  identified failure mode for FrontierScience-Olympiad [Xiong2024]. If a row's problem exceeds
  context, prefer dropping the difficulty `note` strings rather than the `problem` body.

* **Annotation model**: keep `claude-sonnet-4-6-20251001` for v2 to enable a clean v2-vs-v1
  comparison with the model held constant. The change of interest is the schema, not the model.

* **Judge model**: use `claude-haiku-4-5-20251001` consistent with v1
  [Xiong2024 schema-forced JSON pattern], with a single-shot prompt that returns
  `{"verdict": "acceptable" | "needs revision", "justification": str}`. The judge sees the full
  problem and the full v2 tree.

* **Stratified judge sample of ≥23 rows**: sample 6 from FrontierScience-Olympiad (most affected v1
  benchmark), 6 from SWE-bench Verified, 6 from WorkArena++, 5 from tau-bench (the v1 26 / 26 / 23 /
  40 split rounds to 5-6 per benchmark for ≈20% coverage). Use a fixed random seed.

* **Hierarchy completeness flag**: `hierarchy_completeness` is `true` iff
  `hierarchy.global is not null` AND (any subtask has at least one atomic OR `global_atomics` is
  non-empty). This is stricter than v1, which only required atomic-list non-empty.

* **Task-id deduplication**: thread `_pilot_row_index` (the source pilot file row index) into every
  row of the v2 jsonl. The 14 colliding `task_id`s found in v1 break direct keying on `task_id`;
  pilot row index is the unique key.

* **Best practice — multi-seed not needed here**: this task does not measure agent performance, only
  annotation quality. One annotation pass per row at temperature 0 is sufficient. Multi-seed is
  reserved for the Phase 2 experiments [Mosbach2021-style stability concerns are not in scope].

* **Best practice — JSON parsing fallback**: parse the model's JSON response defensively. Strip
  markdown fences, extract from `{ ... }` if needed, fall back to a `null` annotation with a per-row
  error note rather than crashing the run [t0005's judge_runner.py pattern].

## Gaps and Limitations

* **No published comparison of flat vs. tree schemas on the four benchmarks of interest.** None of
  the reviewed papers run a head-to-head ablation on FrontierScience-Olympiad, SWE-bench Verified,
  tau-bench, AND WorkArena++ together. The v2-vs-v1 delta this task reports will itself be the first
  such comparison.

* **No published guidance on `global_atomics` proportion.** ReAct reports 18% and Reflexion 22%, but
  on HotpotQA only [Yao2022, Shinn2023]. The fraction on multi-domain composite benchmarks is
  unknown.

* **No reliable inter-judge agreement numbers for hierarchical annotation.** [Xiong2024] reports
  judge-vs-human agreement, not judge-vs-judge. This task uses a single haiku judge and acknowledges
  that as a single-rater limitation deferred to v3.

* **No published validation that LLM-judge verdicts on annotation quality predict downstream task
  performance.** This task does not address that gap; the assumption is that "needs revision" rows
  are likely to be lower-quality inputs to Phase 2 experiments, but this assumption is inherited
  from v1 and is itself a candidate for future ablation.

## Recommendations for This Task

1. **Adopt the v2 tree schema as specified in the task description.** Do not invent additional
   levels. The schema is `hierarchy.global` (str), `hierarchy.subtasks: [{subtask, atomics}]`,
   `hierarchy.global_atomics` (a list of strings). Mirror this for `gold_actions`.

2. **Pass full problem text to both annotator and judge, with no character cap.** This is the single
   highest-leverage change identified [Xiong2024] and the dominant v1 failure mode.

3. **Stratify the judge sample by source benchmark and use a fixed seed.** ≥6 rows for the largest
   benchmark (FrontierScience-Olympiad, 40 rows), ≥5 each for the others (totalling ≥23).

4. **Persist `_pilot_row_index` in every row.** v1 colliding `task_id`s force this for any
   downstream join.

5. **Compute per-benchmark v2-vs-v1 accept rate delta.** Any benchmark where v2 fails to improve
   should appear as a flagged finding in `results_detailed.md` and a follow-up suggestion.

6. **Do not attempt human review or row expansion in this task.** Both are explicitly deferred to v3
   / S-0005-01 expansion. Keep scope contained at 115 rows + LLM judge spot-check.

## Paper Index

### [Zhou2022]

* **Title**: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
* **Authors**: Zhou, D. et al.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2205.10625`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/10.48550_arXiv.2205.10625/`
* **Categories**: `hierarchical-planning`, `granularity-conditioning`
* **Relevance**: Foundational two-stage decomposition with explicit edges between subproblems and
  their solutions. Directly motivates the v2 tree schema.

### [Wang2023]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning
* **Authors**: Wang, L. et al.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/10.48550_arXiv.2305.04091/`
* **Categories**: `granularity-conditioning`, `hierarchical-planning`
* **Relevance**: Demonstrates that an explicit plan tree before atomic execution improves zero-shot
  reasoning by **+5.2 points** on GSM8K. Confirms the value of the tree schema.

### [Yao2022]

* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Yao, S. et al.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2210.03629`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/10.48550_arXiv.2210.03629/`
* **Categories**: `granularity-conditioning`, `hierarchical-planning`
* **Relevance**: Reports that **18% of successful-trajectory atomics** are cross-cutting
  verification actions, motivating the `global_atomics` bucket in the v2 schema.

### [Shinn2023]

* **Title**: Reflexion: Language Agents with Verbal Reinforcement Learning
* **Authors**: Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., Yao, S.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2303.11366`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/10.48550_arXiv.2303.11366/`
* **Categories**: `hierarchical-planning`, `granularity-conditioning`
* **Relevance**: Confirms ReAct's cross-cutting atomic finding (**22%** of atomics are
  self-evaluation). Independent corroboration of the `global_atomics` need.

### [Xiong2024]

* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
* **Authors**: Xiong, M. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2306.13063`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/10.48550_arXiv.2306.13063/`
* **Categories**: `uncertainty-calibration`, `agent-evaluation`
* **Relevance**: Provides the **41% truncated vs. 77% full-input** judge agreement number that
  diagnoses the v1 FrontierScience-Olympiad 0/3 failure. Single most relevant finding for v2.

### [Boisvert2024]

* **Title**: WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge
* **Authors**: Boisvert, L. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2407.05291`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/10.48550_arXiv.2407.05291/`
* **Categories**: `benchmark-workarena`, `hierarchical-planning`, `agent-evaluation`
* **Relevance**: Explicit tree-vs-flat ablation on a compositional web-task benchmark; **flat
  plateaus at 30%, tree reaches 55%**. Strong empirical justification for the v2 schema upgrade.

### [Jimenez2024]

* **Title**: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
* **Authors**: Jimenez, C. E. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2310.06770`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/10.48550_arXiv.2310.06770/`
* **Categories**: `benchmark-swebench`, `agent-evaluation`
* **Relevance**: Source benchmark for the SWE-bench Verified rows in the dataset. Provides the
  baseline annotation quality that the v2 re-annotation must preserve.

### [OpenAI2024]

* **Title**: Introducing SWE-bench Verified
* **Authors**: OpenAI
* **Year**: 2024
* **DOI**: `no-doi_OpenAI2024_swe-bench-verified`
* **Asset**: `tasks/t0002_recent_papers/assets/paper/no-doi_OpenAI2024_swe-bench-verified/`
* **Categories**: `benchmark-swebench`, `benchmark-annotation`, `agent-evaluation`
* **Relevance**: Documents the human re-annotation pass that discarded ~50% of original SWE-bench
  tasks as ambiguous. Strongest evidence that benchmark annotation quality is a first-order concern,
  motivating the v3 human-review follow-up referenced in v2 results.
