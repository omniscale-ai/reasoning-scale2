---
spec_version: "3"
paper_id: "10.48550_arXiv.2410.07166"
citation_key: "Li2024"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making

## Metadata

* **File**: `files/li_2024_embodied-agent-interface.pdf`
* **Published**: 2024-10-09 (arXiv); NeurIPS 2024 D&B Track (Oral)
* **Authors**: Manling Li 🇺🇸, Shiyu Zhao 🇺🇸, Qineng Wang 🇺🇸, Kangrui Wang 🇺🇸, Yu Zhou 🇺🇸, Sanjana
  Srivastava 🇺🇸, Cem Gokmen 🇺🇸, Tony Lee 🇺🇸, Li Erran Li 🇺🇸, Ruohan Zhang 🇺🇸, Weiyu Liu 🇺🇸, Percy
  Liang 🇺🇸, Li Fei-Fei 🇺🇸, Jiayuan Mao 🇺🇸, Jiajun Wu 🇺🇸
* **Venue**: NeurIPS 2024 (Datasets and Benchmarks Track, Oral)
* **DOI**: `10.48550/arXiv.2410.07166`

## Abstract

We aim to evaluate Large Language Models (LLMs) for embodied decision making. While a significant
body of work has been leveraging LLMs for decision making in embodied environments, we still lack a
systematic understanding of their performance because they are usually applied in different domains,
for different purposes, and built based on different inputs and outputs. Furthermore, existing
evaluations tend to rely solely on a final success rate, making it difficult to pinpoint what
ability is missing in LLMs and where the problem lies, which in turn blocks embodied agents from
leveraging LLMs effectively and selectively. To address these limitations, we propose a generalized
interface (Embodied Agent Interface) that supports the formalization of various types of tasks and
input-output specifications of LLM-based modules. Specifically, it allows us to unify
1. a broad set of embodied decision-making tasks involving both state and temporally extended goals,
   2\) four commonly-used LLM-based modules for decision making: goal interpretation, subgoal
   decomposition, action sequencing, and transition modeling, and 3) a collection of fine-grained
   metrics which break down evaluation into various types of errors, such as hallucination errors,
   affordance errors, various types of planning errors, etc. Overall, our benchmark offers a
   comprehensive assessment of LLMs' performance for different subtasks, pinpointing the strengths
   and weaknesses in LLM-powered embodied AI systems, and providing insights for effective and
   selective use of LLMs in embodied decision making.

## Overview

This paper introduces Embodied Agent Interface (EAI), a unified evaluation framework for Large
Language Models acting as decision-making components inside embodied agents. The motivation is that
prior LLM-for-embodied-AI evaluations are heterogeneous: they use different simulators, different
input-output schemas, different definitions of success, and they typically report only a single
end-to-end success rate. Such aggregate scores conceal which sub-skill (parsing the instruction,
proposing a plan, picking individual actions, modeling state changes) actually fails, so it is
impossible to know whether a new model improves embodied agents because it understands goals better,
plans more reliably, or simply hallucinates fewer object names.

EAI addresses this by formalizing embodied tasks in the Planning Domain Definition Language (PDDL)
style — every task is specified as an initial symbolic state plus a goal expressed as a logical
formula over object states, spatial relations, or temporally extended action goals (LTL). Every LLM
call is expressed as one of four canonical modules with strict input and output types, so any LLM
can be plugged in for any module without bespoke prompting glue. The benchmark instantiates this
interface on two well-known embodied simulators, BEHAVIOR (BDDL, complex household activities) and
VirtualHome (script-based household tasks), giving researchers a common, decoupled, error-typed
yardstick rather than a black-box success number.

The authors evaluate eighteen LLMs spanning proprietary frontier models (GPT-4, GPT-4o, o1-preview,
Claude-3 Opus, Claude-3.5 Sonnet, Gemini 1.5 Pro/Flash) and open-weight models (Llama-3 family,
Mistral, Cohere, etc.) across all four modules. The headline finding is that o1-preview, the only
explicitly reasoning-trained model in the lineup at submission time, is best or near-best on every
module — establishing inference-time reasoning, not raw scale, as the principal driver of embodied
decision quality.

## Architecture, Models and Methods

EAI decomposes any embodied decision-making pipeline into four LLM-based modules with formal
signatures. **Goal interpretation** maps a natural-language instruction plus the current symbolic
scene to a goal formula over predicates (object states such as `cooked(steak)`, spatial relations
such as `inside(milk, fridge)`, and temporally extended action goals encoded as LTL formulas).
**Subgoal decomposition** takes the interpreted goal and produces an ordered sequence of
intermediate symbolic states. **Action sequencing** generates an executable action plan in the
simulator's API. **Transition modeling** asks the LLM to predict, in PDDL operator form, the
preconditions and effects of each action so a symbolic planner can use the LLM as a learned world
model.

Inputs and outputs are strictly typed: domain files give predicates and action schemas, problem
files give the initial state, and outputs are parsed against PDDL/BDDL grammars. Failures are
classified before scoring, distinguishing parsing/grammar errors from semantic errors. Parsing
errors are reported separately so a model that emits malformed JSON does not get conflated with one
that emits valid but wrong plans.

The benchmark combines two simulators. **VirtualHome** contributes 26 task categories, 338 task
instructions, 801 goals (340 state, 299 relation, 162 action), 338 reference trajectories of 8.76
steps on average, and 33 transition models. **BEHAVIOR** contributes 100 tasks, 100 instructions,
673 goals (153 state, 520 relation), 100 trajectories of 14.6 steps on average, and 30 transition
models. Eighteen LLMs are evaluated under matched prompts and few-shot exemplars, with
greedy/temperature-zero decoding and a fixed retry budget for parse failures. Module-level scoring
uses precision/recall/F1 over predicted goal literals, action-sequencing goal success rate (Goal SR)
and execution success rate (Exec SR), subgoal decomposition success against ground-truth
intermediate states, and operator F1 over preconditions and effects for transition modeling. A
fine-grained error taxonomy — hallucination (predicates or objects that do not exist), affordance
violations, missing steps, wrong order, additional unnecessary steps, missing preconditions/effects
— is computed automatically from the symbolic checks.

## Results

* **Action sequencing on BEHAVIOR**: o1-preview tops the leaderboard with **81.0% goal SR** and
  **91.0% execution SR**, well above other models; on VirtualHome it reaches **71.1% goal SR**,
  again the best of the eighteen LLMs evaluated.
* **Goal interpretation**: best precision on VirtualHome lands in the **35.2%-47.2%** range
  (o1-preview / Gemini 1.5 Pro), while BEHAVIOR recall climbs much higher to **78.8%-93.4%**,
  showing that BEHAVIOR's mostly-relational goals are easier to recover than VirtualHome's mixed
  state/relation/action goals.
* **Subgoal decomposition**: o1-preview and Gemini 1.5 Flash lead, hitting roughly **89.4% goal SR**
  on VirtualHome but only **57.0% execution SR** on BEHAVIOR, exposing a sharp drop when
  intermediate states must be both correct and executable.
* **Transition modeling**: Claude-3.5 Sonnet and o1-preview lead, with up to **78.8% F1** on
  BEHAVIOR object-state effects and **95.3% F1** on object-orientation effects; relational effects
  are much harder than unary state effects.
* **Open vs. proprietary gap**: open-weight models (Llama-3-8B, Mistral) suffer materially higher
  grammar/parsing error rates and visibly lower goal SR on action sequencing across both simulators,
  especially as plan length grows beyond ~10 steps.
* **Difficulty scaling**: success rates degrade sharply with the number of goal literals and the
  length of the reference trajectory; BEHAVIOR's longer 14.6-step trajectories drive most of the
  difficulty gap relative to VirtualHome's 8.76-step ones.
* **Error mix**: hallucinated predicates and affordance violations dominate failures on VirtualHome,
  while missing-step and wrong-order errors dominate on BEHAVIOR — the same model fails differently
  on different simulators.
* **Reasoning-time models win**: o1-preview's lead is consistent across all four modules, the first
  systematic evidence in this domain that test-time reasoning helps embodied planning more than
  parameter count.

## Innovations

### A Unified, Typed Interface for LLM-Based Embodied Modules

Prior benchmarks treat the LLM as a black box ending in a success or failure. EAI defines four
canonical modules (goal interpretation, subgoal decomposition, action sequencing, transition
modeling) with strict PDDL/LTL input-output types, so any LLM can be slotted into any module and
compared apples-to-apples. This decoupling is what makes the rest of the contribution possible.

### Fine-Grained Symbolic Error Taxonomy

Instead of a single success rate, EAI computes hallucination, affordance, missing-step, wrong-order,
additional-step, missing-precondition, and missing-effect errors automatically from symbolic checks
against ground-truth domain and problem files. The same final-success number can hide very different
failure profiles, and the taxonomy lets practitioners diagnose which sub-skill to fix.

### Joint Evaluation Across BEHAVIOR and VirtualHome

The benchmark unifies two simulators with very different goal distributions (BEHAVIOR is
relation-heavy and long-horizon, VirtualHome is state/action-mixed and shorter) under one interface.
Cross-simulator evaluation exposes that LLM rankings are not stable across goal distributions, which
is invisible in single-simulator benchmarks.

### Modular Plug-In Evaluation of Reasoning Models

EAI is the first embodied benchmark to evaluate o1-preview head-to-head against frontier
non-reasoning models module-by-module, providing the first quantitative evidence that test-time
reasoning specifically improves embodied planning rather than general language quality.

## Datasets

* **VirtualHome**: 26 task categories, 338 task instructions, 801 goals (340 state, 299 relation,
  162 action), 338 reference trajectories averaging 8.76 steps, 33 transition models. Public,
  research-license; built on top of the VirtualHome simulator (Puig et al.).
* **BEHAVIOR / BDDL**: 100 tasks, 100 instructions, 673 goals (153 state, 520 relation), 100
  reference trajectories averaging 14.6 steps, 30 transition models. Public, MIT license; built on
  top of the BEHAVIOR-1K activity suite from Stanford.
* The benchmark also packages PDDL/BDDL domain files, problem files, and a fine-grained scoring
  pipeline as a reproducible toolkit released at
  <https://github.com/embodied-agent-interface/embodied-agent-interface> alongside a HELM-style
  leaderboard.

## Main Ideas

* For this project, EAI's four-module decomposition (goal interpretation / subgoal decomposition /
  action sequencing / transition modeling) is a strong template for our hierarchical-planning
  agents: it directly maps onto our three-level hierarchy (strategic / subtask / atomic) plus a
  separate world-modeling head, and gives us a precedent for typed, decoupled module evaluation.
* The fine-grained error taxonomy (hallucination, affordance, missing/extra/wrong-order steps,
  precondition/effect errors) is exactly the kind of diagnostic breakdown we want to apply to our
  scope-aware vs. scope-mismatched conditions — it lets us attribute differences to specific failure
  modes rather than to overall success rate alone.
* The single most actionable empirical lesson for our agent design is that test-time reasoning
  (o1-style) buys substantially more embodied-planning quality than additional parameters, which
  argues for prioritizing reasoning-trained backends in our scope-aware A condition.
* BEHAVIOR vs. VirtualHome rankings differ for the same LLMs, so when we choose evaluation
  benchmarks we must include at least two structurally different sources to avoid optimizing to a
  single distribution — this validates our multi-source benchmark design (FrontierScience-Olympiad
  + WorkArena++ + tau-bench + SWE-bench).

## Summary

Li et al. introduce Embodied Agent Interface (EAI), a unified PDDL/BDDL-grounded evaluation
framework for using LLMs as decision-making components in embodied agents. The motivation is the
fragmentation of prior work: papers run different LLMs on different simulators with different
input-output conventions and report only an end-to-end success rate, so it is impossible to tell
which sub-skill — instruction parsing, plan structuring, low-level action choice, or world modeling
— is actually limiting performance. EAI fixes the interface and the metrics so that any LLM can be
plugged into any of four canonical modules and scored with the same fine-grained error taxonomy
across two distinct simulators.

Methodologically, the framework formalizes every embodied task as an initial symbolic state plus a
goal formula over object states, relations, or LTL action sequences, and defines four typed LLM
modules: goal interpretation, subgoal decomposition, action sequencing, and transition modeling.
Each module's outputs are parsed and checked against ground-truth domains and trajectories, with
parse errors separated from semantic errors and a seven-way error taxonomy (hallucination,
affordance, missing-step, wrong-order, additional-step, missing-precondition, missing-effect)
computed automatically. The benchmark instantiates this interface on VirtualHome (338 tasks, 801
goals, 8.76-step trajectories) and BEHAVIOR (100 tasks, 673 goals, 14.6-step trajectories) and
evaluates eighteen LLMs.

The headline finding is that o1-preview, the only test-time reasoning model in the cohort, dominates
across all four modules — for example, **81.0% goal SR / 91.0% execution SR** on BEHAVIOR action
sequencing and **71.1% goal SR** on VirtualHome action sequencing — establishing inference-time
reasoning as the strongest predictor of embodied decision quality. Open-weight models pay a large
grammar-error tax and lag on long-horizon action sequencing, while transition modeling is a notable
weakness across the board: even the best models hit only **78.8% F1** on BEHAVIOR object-state
effects. Failure modes also differ by simulator, with hallucination / affordance errors dominating
on VirtualHome and missing-step / wrong-order errors on BEHAVIOR.

For our project, EAI is directly relevant on three axes. First, its four-module decomposition is a
near-isomorphic precedent for our hierarchical-planning agent design and validates the
scope-conditioned A/B/C ablation: by typing each module's inputs and outputs we gain the same
diagnostic resolution. Second, its symbolic error taxonomy is the right shape for our
overconfident-error-rate metric and our scope-mismatched failure analysis; we should adopt
hallucination/affordance/missing-step labels in our annotation schema. Third, EAI's evidence that
test-time reasoning beats raw scale strongly motivates including reasoning-trained backends as our
default A-condition agent and ensures our judges and predictions cover both reasoning and
non-reasoning model families.
