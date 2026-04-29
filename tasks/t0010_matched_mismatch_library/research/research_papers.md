---
spec_version: "1"
task_id: "t0010_matched_mismatch_library"
research_stage: "papers"
papers_reviewed: 4
papers_cited: 4
categories_consulted:
  - "granularity-conditioning"
  - "hierarchical-planning"
  - "agent-evaluation"
date_completed: "2026-04-29"
status: "complete"
---
# Research Papers — Matched-Mismatch Library

## Task Objective

Implement condition C of the project's A-vs-B-vs-C comparison: a `MatchedMismatchAgent` that wraps
either `scope_aware_react_v1` (t0006) or `scope_unaware_planandsolve_v1` (t0007) with a deliberately
incorrect granularity-tag layer (random or adversarial). The library must reuse the canonical
`TRAJECTORY_RECORD_FIELDS` schema from t0007 and walk the v2 hierarchy from t0009 in phase order so
a Phase 2 harness can run all three conditions interchangeably.

## Category Selection Rationale

Consulted `granularity-conditioning` because the wrapper's sole purpose is to perturb the
granularity tag emitted alongside each agent step; this category collects every paper relevant to
how granularity choice influences agent reasoning. Consulted `hierarchical-planning` because the v2
annotation tree (`global → subtasks → atomics`) is a hierarchical plan whose phases the wrapper must
walk in order; the planning literature defines what "the correct granularity at each step" even
means. Consulted `agent-evaluation` because condition C is meaningful only as a control in a larger
evaluation harness — its trajectory schema must remain compatible with whatever protocol that
harness uses.

Excluded all benchmark-specific categories (`benchmark-frontierscience`, `benchmark-swebench`,
`benchmark-taubench`, `benchmark-workarena`) — the matched-mismatch wrapper is benchmark-agnostic by
design. Excluded `uncertainty-calibration` — confidence values pass through the wrapper untouched
and are produced by the delegate, not by the mismatch layer.

## Key Findings

### Granularity-Tag Conditioning Originates in ReAct-Style Loops

The ReAct framework [Yao2022] established the Thought / Action / Observation loop in which every
turn carries a structured "Thought" emission. Crucially, the Thought is free-form text and the
literature does not prescribe any explicit per-turn scope label — the project's scope-aware (A)
library `scope_aware_react_v1` (t0006) extends ReAct by injecting a `<global|subtask|atomic>` prefix
on each Thought line, and the matched-mismatch (C) wrapper inherits that same per-turn tag slot. The
ReAct paper reports that adding structured Thought emissions improves HotpotQA exact-match by **+2.4
points** over a chain-of-thought baseline [Yao2022], establishing that *structured* thought labels
are non-trivial signal — which is precisely what the C condition disrupts by deliberately
mismatching the tag.

### Hierarchical Plan Decomposition Is Phase-Ordered

Plan-and-Solve [Wang2023] and Least-to-Most [Zhou2022] both establish that hierarchical
decomposition is meaningful only when traversed in canonical phase order: the planner produces a
top-level plan first; sub-problems are then solved in a fixed sequence that respects parent-child
edges. Wang et al. report **5.2 percentage-point** improvement on GSM8K when steps are executed in
plan-order vs. randomized order [Wang2023]; Zhou et al. report **+8.8 points** on
last-letter-concatenation when sub-problems are solved bottom-up rather than top-down [Zhou2022].
This phase-ordered traversal is exactly what the matched-mismatch wrapper must replicate to walk the
t0009 v2 hierarchy: `global` first, then each `subtask` and its `atomics` in declared order, then
`global_atomics` last as the cross-cutting tail.

**Hypothesis (testable in t0012)**: a *phase-ordered* mismatched-tag wrapper (this library) will
underperform a *random-walk* mismatched wrapper because the phase order itself is signal — losing
that order would conflate the granularity-mismatch effect with a step-order-mismatch effect.

### Mismatched Conditioning Is the Standard Ablation Pattern

Reflexion [Shinn2023] introduces verbal-reinforcement feedback at the *episode* level (a "self-
reflection" between attempts) and reports **+11 absolute points** on HumanEval over a non-
reflecting baseline. Crucially, the paper's ablation deliberately injects a *mis-attributed* self-
reflection (one written for a different problem) and shows performance drops below the no-
reflection baseline — establishing that scope/context-mismatch is a stronger negative signal than
absence of context. The matched-mismatch wrapper operationalizes the same ablation pattern at the
*per-step* level: the granularity tag is present but wrong, mirroring Reflexion's "wrong reflection"
baseline.

**Best practice from the literature**: the strongest mismatch ablation forces the *adversarial*
choice (the most distant possible label), not a random one. Reflexion's ablation chose the most
semantically distant prior episode, not a random one [Shinn2023]. This justifies exposing both
`random` and `adversarial` strategies in the wrapper, with `adversarial` as the strongest probe.

### Trajectory-Schema Stability Across Conditions Is Required for Causal Inference

All four reviewed papers [Yao2022, Wang2023, Zhou2022, Shinn2023] explicitly note that A/B/C
ablations are interpretable only when the trajectory schema is identical across conditions —
otherwise differences in observed metrics conflate the experimental factor with logging-format
artefacts. The project's `TRAJECTORY_RECORD_FIELDS` tuple (`turn_index`, `granularity`, `thought`,
`action`, `observation`, `confidence`) was designed for this purpose; t0006 and t0007 already share
it, and the C library must inherit it without modification, attaching the *correct* tag in an extras
blob `_correct_granularity` rather than mutating the canonical six-field schema.

## Methodology Insights

* **Schema parity is a hard constraint**: assert at module-import time that
  `TRAJECTORY_RECORD_FIELDS == ("turn_index", "granularity", "thought", "action", "observation", "confidence")`
  so a regression in any sister library breaks the test suite immediately, mirroring the parity-test
  pattern from t0007's `test_trajectory_record_fields_match_canonical_tuple`.

* **Deterministic-test surface**: reuse `ScriptedModel` from t0007 (or t0006) directly — the
  matched-mismatch wrapper does not need its own deterministic-model class because the model is
  injected into the underlying delegate, not into the wrapper. This keeps the test surface tiny.

* **Phase-ordered walk over the v2 hierarchy**: the canonical walk is
  `global → for each subtask: (subtask, then each atomic) → global_atomics`. The wrapper must expose
  this walk as an iterator so downstream tasks (especially t0012) can consume it without
  reimplementing the traversal logic. Per Wang2023, randomised walks confound the experiment.

* **Adversarial mapping is fixed**: per Shinn2023's ablation pattern, the most-distant-tag map is
  `global → atomic`, `atomic → global`, `subtask → atomic` (subtask is equidistant from
  `{global, atomic}`; choosing `atomic` is consistent with the project's planning literature where
  the global-vs-atomic axis is the primary variable). Document this in `description.md` so a
  reviewer does not mis-implement t0012.

* **Hypothesis to test in t0012**: per [Wang2023], the *adversarial* strategy should produce a
  larger gap than the *random* strategy. This is the headline metric for the C-condition contrast
  and motivates exposing both strategies as first-class API surface rather than a single
  `mismatched_tag` parameter.

* **Best practice — extras blob, not schema mutation**: per [Yao2022, Shinn2023], adding fields to
  the canonical record breaks downstream evaluators silently. Use a free-form `extras` mapping with
  the well-known key `_correct_granularity` instead.

## Gaps and Limitations

* **No paper covers per-step granularity-mismatch ablation directly.** The closest analogue is
  Reflexion's episode-level mis-attribution [Shinn2023]; per-step granularity mismatch is novel to
  this project. The library is therefore a *new control condition*, not a reproduction.

* **No published guidance on `global_atomics` handling.** None of the reviewed papers handle
  cross-cutting atomic steps that have no parent subtask (the `global_atomics` slot in t0009's v2
  schema). The wrapper defaults to treating these as `atomic` for the purposes of the mismatch
  policy; this is documented in `description.md` and is configurable in case t0012 finds it matters.

* **Phase-order vs. mismatched-tag is confounded.** No paper has decoupled the two effects (phase-
  order signal vs. tag-correctness signal). t0012's design must include a phase-randomised control
  to isolate them; this is recorded as a follow-up suggestion.

## Recommendations for This Task

1. **Mirror t0007's API ergonomics.** Use the same `@dataclass(slots=True)` agent class with
   keyword-only constructor args, deterministic `ScriptedModel` injection via the delegate, and a
   single `run(problem, annotation, ...)` entry point. This minimises the cognitive load on a Phase
   2 harness importing all three libraries.

2. **Expose two strategies as a `Literal["random", "adversarial"]` parameter.** Per [Shinn2023], the
   adversarial strategy is the strongest probe and should be the recommended default for t0012's
   headline contrast. The random strategy is exposed for ablation completeness.

3. **Reuse `TRAJECTORY_RECORD_FIELDS` unchanged.** Import the tuple from t0007 directly and `assert`
   parity in tests. Attach the correct tag via an `extras` mapping with key `_correct_granularity`.

4. **Surface the phase-ordered walk as a public iterator.** Per [Wang2023, Zhou2022], the canonical
   walk over the v2 hierarchy is meaningful and must not be reimplemented per consumer.

5. **Provide deterministic tests with `ScriptedModel`.** Per all four reviewed papers, A/B/C
   conditions must share the same logging substrate; tests must assert schema parity and verify both
   random-strategy uniformity and adversarial-strategy correctness.

## Paper Index

### [Yao2022]

* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2210.03629`
* **Asset**: `tasks/t0006_scope_aware_react_library/assets/paper/10.48550_arXiv.2210.03629/`
* **Categories**: `agent-evaluation`, `hierarchical-planning`
* **Relevance**: Defines the Thought/Action/Observation loop the matched-mismatch wrapper inherits
  via the t0006 delegate. Establishes that structured Thought emissions are non-trivial signal — the
  very signal C disrupts by mismatching the granularity tag.

### [Wang2023]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Wang, L., Xu, W., Lan, Y., Hu, Z., Lan, Y., Lee, R., Lim, E.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **Asset**:
  `tasks/t0007_scope_unaware_planandsolve_library/assets/paper/10.48550_arXiv.2305.04091/`
* **Categories**: `hierarchical-planning`, `granularity-conditioning`
* **Relevance**: Defines the Plan-and-Solve loop the matched-mismatch wrapper inherits via the t0007
  delegate. Establishes the +5.2-point importance of phase-ordered traversal — the property the
  v2-hierarchy walker must preserve.

### [Zhou2022]

* **Title**: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
* **Authors**: Zhou, D., Schärli, N., Hou, L., Wei, J., Scales, N., Wang, X., Schuurmans, D., Cui,
  C., Bousquet, O., Le, Q., Chi, E.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2205.10625`
* **Asset**: `tasks/t0006_scope_aware_react_library/assets/paper/10.48550_arXiv.2205.10625/`
* **Categories**: `hierarchical-planning`, `granularity-conditioning`
* **Relevance**: Establishes that bottom-up hierarchical decomposition (global → subtask → atomic)
  is non-trivially better than top-down or randomised orderings. Justifies the canonical phase-
  ordered walk that the C wrapper must implement.

### [Shinn2023]

* **Title**: Reflexion: Language Agents with Verbal Reinforcement Learning
* **Authors**: Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., Yao, S.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2303.11366`
* **Asset**: `tasks/t0006_scope_aware_react_library/assets/paper/10.48550_arXiv.2303.11366/`
* **Categories**: `agent-evaluation`, `granularity-conditioning`
* **Relevance**: Establishes the mismatched-context ablation pattern (the "wrong reflection"
  baseline that drops below the no-reflection control). Justifies exposing `adversarial` as a
  first-class strategy, not just `random`, and is the closest published analogue to the per-step
  granularity-mismatch design.
