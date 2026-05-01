---
spec_version: "3"
paper_id: "10.48550_arXiv.2401.13178"
citation_key: "Ma2024"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents

## Metadata

* **File**: `files/ma_2024_agentboard.pdf`
* **Published**: 2024 (arXiv v2 December 2024; NeurIPS 2024 D&B Oral)
* **Authors**: Chang Ma 🇭🇰, Junlei Zhang 🇨🇳, Zhihao Zhu 🇨🇳, Cheng Yang 🇨🇳, Yujiu Yang 🇨🇳, Yaohui Jin
  🇨🇳, Zhenzhong Lan 🇨🇳, Lingpeng Kong 🇭🇰, Junxian He 🇭🇰
* **Venue**: NeurIPS 2024 Datasets and Benchmarks Track (Oral)
* **DOI**: `10.48550/arXiv.2401.13178`

## Abstract

Evaluating Large Language Models (LLMs) as general-purpose agents is essential for understanding
their capabilities and facilitating their integration into practical applications. However, the
evaluation process presents substantial challenges. A primary obstacle is the benchmarking of agent
performance across diverse scenarios within a unified framework, especially in maintaining
partially-observable environments and ensuring multi-round interactions. Moreover, current
evaluation frameworks mostly focus on the final success rate, revealing few insights during the
process and failing to provide a deep understanding of the model abilities. To address these
challenges, we introduce AgentBoard, a pioneering comprehensive benchmark and accompanied
open-source evaluation framework tailored to analytical evaluation of LLM agents. AgentBoard offers
a fine-grained progress rate metric that captures incremental advancements as well as a
comprehensive evaluation toolkit that features easy assessment of agents for multi-faceted analysis.
This not only sheds light on the capabilities and limitations of LLM agents but also propels the
interpretability of their performance to the forefront. Ultimately, AgentBoard serves as a step
towards demystifying agent behaviors and accelerating the development of stronger LLM agents.

## Overview

AgentBoard is a unified benchmark and analytical evaluation framework that targets a fundamental gap
in LLM-agent evaluation: prior benchmarks reduce performance to a single, end-of-trajectory success
rate, which collapses very different agent behaviors into the same number whenever success is rare.
The authors argue this is exactly the regime current open-weight LLMs operate in, so research
progress is invisible under the existing measurement instrument. AgentBoard's central contribution
is a fine-grained "progress rate" metric defined per interaction step, computed either as a
continuous matching score against the goal state or as the fraction of human-annotated subgoals
achieved so far. The framework wraps this metric in a unified POMDP-style API that imposes
multi-round, partially-observable interaction across all tasks.

The benchmark contains 9 tasks and 1013 environments spanning four families (embodied, game, web,
tool). Each task is either constructed or adapted to be text-only, multi-round, and partially
observable, and each is augmented with hand-annotated subgoal sequences. The authors evaluate 17
proprietary and open-weight LLMs and ship an open-source Weights&Biases panel that visualises
sub-skill scores, easy/hard splits, and long-range progress curves. The headline finding is that
GPT-4 (70.0% progress / 47.9% success) leads by a large margin, but progress rate exposes meaningful
differentiation among open-weight models that look indistinguishable under success rate alone.

## Architecture, Models and Methods

The interaction model is a partially observable Markov decision process tuple (g, S, A, O, T) with
goal g, state space S, action space A, observation space O, and deterministic transition T. The
agent maintains memory m_t = {o_0, a_0, ..., o_t} and selects an action a_t under policy pi. A
"reflex" act-only prompting strategy is used as the canonical baseline (one-shot in-context example,
sliding-window memory following LangChain), and ReAct-style prompting is provided as an ablation.
The sliding window allows runs to continue past the context limit, in contrast to prior benchmarks
that abort.

The progress rate has two forms: a continuous similarity function f(s_i, g) in [0, 1] for tasks with
comparable states (PDDL, WebShop, Sheet operations), or the fraction of matched subgoals (1/K) sum
f(s_i, g_k) for tasks with discrete subgoal sequences (AlfWorld, ScienceWorld, BabyAI, Jericho,
Tool-Query, Tool-Operation Todo, WebArena). Subgoal matching uses regular-expression predicates
against the trajectory state. The authors manually edited 5% of problems so each final goal admits a
unique subgoal ordering, while still permitting diverse trajectories.

Annotation: subgoals were authored by paper authors and verified through multi-stage review. A
60-trajectory-per-task user study compared four-author human progress scores against automatic
progress rate; Pearson rho exceeds 0.95 on every task and Fleiss' kappa is in the
substantial-agreement range (0.73-0.91). Hardware/compute is not the focus, but vLLM
(PagedAttention) is used for open-weight inference. They evaluate 17 LLMs sorted by average success
rate: GPT-4, Claude 2, Gemini-1.5-Flash, Claude-3-Haiku, Llama3-70b, GPT-3.5-Turbo, xLAM-70b,
DeepSeek-67b, Text-Davinci-003, GPT-3.5-Turbo-16k, AgentLM-70b, Lemur-70b, CodeLlama-34b, Llama3-8b,
CodeLlama-13b, Llama2-70b, Mistral-7b, Vicuna-13b-16k, Llama2-13b. Six sub-skills are scored:
memory, planning, world modelling, self-reflection, grounding, and spatial navigation. Easy/hard
splits are defined by the number of subgoals or conditions per environment.

## Results

* GPT-4 leads with **70.0% progress / 47.9% success** averaged over 9 tasks; Claude 2 follows at
  **48.9% / 26.2%** and Gemini-1.5-Flash at **43.5% / 20.6%**.
* Open-weight models cluster much lower: Llama3-70b **41.9% / 20.2%**, DeepSeek-67b **38.5% /
  17.2%**, AgentLM-70b **33.3% / 14.7%**, Lemur-70b **30.8% / 8.3%**, Mistral-7b **24.6% / 3.9%**,
  Llama2-13b **18.9% / 2.1%**.
* Progress rate separates models that success rate cannot: Llama2-13b (2.1%) vs Mistral-7b (3.9%)
  look identical on success but differ by **5.7 progress points**; CodeLlama-34b's failure to emit
  the "finish" action gives it lower success but higher progress than CodeLlama-13b.
* All 17 models show large hard/easy degradation. GPT-4 drops from **79.2% to 62.7%** progress
  (-16.5) and from **85.0% to 24.9%** success (-60.1) between easy and hard splits.
* Long-range curves show GPT-4 and Claude 2 still improving at step 30 on AlfWorld and PDDL, while
  most open-weight models plateau by **step 6**.
* Grounding accuracy averages **85.6%** for GPT-4, **76.2%** for GPT-3.5-Turbo-16k, and only
  **43.8%** for Mistral-7b; ScienceWorld remains the hardest grounding task (GPT-4 only 22.8%).
* Coding-trained open-weight LLMs help: CodeLlama-34b beats Llama2-70b by **+6.2 progress points**;
  Lemur-70b (code-continued-pretrained) similarly outperforms Llama2-70b.
* Sub-skill radar plots show GPT-4 dominates all six dimensions; open-weight models are most
  deficient on world modelling and self-reflection.
* Human-vs-automatic progress correlation: Pearson rho in [0.95, 0.99] across 8 tasks (60
  trajectories each); Fleiss' kappa in [0.73, 0.91].

## Innovations

### Fine-Grained Progress Rate Metric

First agent benchmark to define a per-step progress metric that is unified across embodied, game,
web, and tool tasks. The metric uses two complementary forms (continuous matching f(s_i, g) and
discrete subgoal coverage), validated against four-author human ratings with Pearson rho > 0.95.

### Unified POMDP API for Heterogeneous Agent Tasks

Reformulates AlfWorld, ScienceWorld, BabyAI, Jericho, PDDL, WebShop, WebArena, Tool-Query, and
Tool-Operation as a single POMDP tuple with a shared action/observation interface, including
adaptations such as text-action BabyAI, rewritten Jericho goals (max 15 subgoals), expanded WebShop
error feedback, and re-annotated ScienceWorld subgoals.

### Hand-Annotated Subgoal Sequences with Uniqueness Editing

For all 1013 environments the authors annotate (or re-annotate) an ordered subgoal list and edit
about 5% of original problems so each final goal admits a unique subgoal ordering. This is the
prerequisite that makes the discrete progress metric well-defined and reproducible.

### Multi-Faceted Analytical Toolkit

Open-source W&B panel that visualises six sub-skill scores (memory, planning, world modelling,
self-reflection, grounding, spatial navigation), easy/hard breakdowns, long-range progress curves,
grounding accuracy, and trajectory traces. Goes beyond a single leaderboard number.

### Cross-Family LLM Sweep

Evaluates 17 proprietary and open-weight LLMs (including agent-specific xLAM-70b, AgentLM-70b,
Lemur-70b) on the same 9 tasks under the same prompting protocol, supporting cross-family claims
such as "code-pretrained open-weight LLMs are stronger agents".

## Datasets

The benchmark is a curated composite of nine environments, all repackaged into the AgentBoard
text-only multi-round POMDP format. Total of 1013 instances across the 9 tasks; per-task split sizes
are listed in Appendix Table 14 of the paper.

* **AlfWorld (ALF)** - household embodied tasks; subgoal-based progress rate.
* **ScienceWorld (SW)** - interactive scientific commonsense; re-annotated subgoals to fix sparsity.
* **BabyAI (BA)** - 20x20 grid navigation; converted from image+tensor to text actions and
  observations; re-annotated subgoals.
* **Jericho (JC)** - text-adventure games; goals rewritten so each finishes within 15 subgoals.
* **PDDL (PL)** - 4 PDDL planning games (Gripper, Barman, Blocksworld, Tyreworld); continuous
  matching score r_match.
* **WebShop (WS)** - e-commerce simulation with improved error feedback and expanded scoring.
* **WebArena (WA)** - real web environment; revised score combining URL match and content match
  computed step-by-step.
* **Tool-Query (TQ)** - three sub-environments (Weather, Movie, Academia) requiring DB queries;
  subgoal annotated.
* **Tool-Operation (TO)** - Todo list management (subgoal-based) and Google Sheet operations
  (matching-score based on cell-level table comparison).

All environments are released open source under the AgentBoard repository
(https://github.com/hkust-nlp/AgentBoard) under permissive licences inherited from the upstream
benchmarks. The 60-trajectory-per-task human-evaluation set used for metric validation was collected
from four paper authors as raters using a 5-point scale {0%, 25%, 50%, 75%, 100%}.

## Main Ideas

* The "progress rate" idea generalises directly to this project's three-level hierarchy:
  subgoal-coverage progress at the global plan level, subtask-completion progress at the mid level,
  and fine-grained matching at atomic-execution level give a single comparable scalar across A
  (scope-aware), B (scope-unaware), and C (scope-mismatched) conditions. This is a stronger Metric 1
  candidate than binary task success.
* AgentBoard demonstrates the methodology for hand-annotating subgoals at scale (1013 environments,
  multi-stage review, Pearson rho > 0.95 against humans). The same pattern (manual annotation by
  authors plus uniqueness editing of about 5% of problems) is directly applicable to the >=100-task
  annotated set required by this project's success criteria.
* The hard/easy split based on subgoal count is a useful template for stratifying our results and is
  much more informative than overall accuracy when models cluster near 0% success.
* Re-annotation of existing benchmarks (BabyAI, ScienceWorld, Jericho) to enforce uniformity of
  subgoal sequences is a precedent for our annotations on top of SWE-bench Verified, tau-bench,
  WorkArena++, and FrontierScience.
* The six-dimensional sub-skill scoring (memory / planning / world modelling / self-reflection /
  grounding / spatial navigation) is a candidate template for analysing agent behaviour conditional
  on granularity in our hierarchical setup.
* Open-weight models plateau at about 6 steps; any longer-horizon experiment in this project should
  expect compounding-error effects and report progress curves rather than only end-of-trajectory
  metrics.

## Summary

Ma et al. introduce AgentBoard, a NeurIPS 2024 Datasets-and-Benchmarks oral that addresses two
fundamental measurement problems in LLM-agent evaluation: incompatible task interfaces across
existing benchmarks and the loss of information caused by reporting only end-of-trajectory success
rate. The authors argue, with evidence, that current open-weight LLMs cluster at near-zero success
on hard agent tasks, so any "progress" between models is invisible. They propose a unified POMDP
formulation, nine carefully curated text-only multi-round partially-observable environments
(AlfWorld, ScienceWorld, BabyAI, Jericho, PDDL, WebShop, WebArena, Tool-Query, Tool-Operation), and
a fine-grained progress-rate metric defined per interaction step.

Methodologically, the progress rate has two forms (continuous state-similarity and discrete
subgoal-coverage). Subgoal sequences were hand-annotated for all 1013 environments and about 5% of
problems were edited so each goal admits a unique ordering. A 60-trajectory-per-task user study with
four expert raters gives Pearson rho > 0.95 between human and automatic progress, validating the
metric. The benchmark ships with an open-source W&B visualisation panel that breaks performance down
by sub-skill (memory, planning, world modelling, self-reflection, grounding, spatial navigation), by
easy/hard difficulty (defined by subgoal count), and by step number.

The empirical findings are that GPT-4 leads at **70.0% progress / 47.9% success**, followed by
Claude 2 (**48.9% / 26.2%**) and Gemini-1.5-Flash (**43.5% / 20.6%**); open-weight models lag
substantially with the strongest (Llama3-70b at **41.9% / 20.2%**) still well below GPT-4. Critical
analyses show that progress rate separates models that look indistinguishable under success rate
(Llama2-13b vs Mistral-7b), that all models drop sharply on hard examples (GPT-4 success: 85.0% to
24.9%), that open-weight models plateau by step 6 while frontier models continue progressing through
step 30, and that code-pretrained open-weight LLMs (CodeLlama, Lemur) outperform their non-code
counterparts.

For this project, AgentBoard is highly relevant in three ways. First, the progress-rate construction
is a direct candidate for our task-success metric (Metric 1), giving us a continuous, per-step
comparable signal across A/B/C conditions instead of a binary outcome. Second, the
subgoal-annotation methodology - per-environment manual labelling, uniqueness editing, multi-stage
verification, and a four-author user study - is a working template for the >=100-task annotated
benchmark this project must build over SWE-bench Verified, tau-bench, WorkArena++, and
FrontierScience. Third, the easy/hard split by subgoal count and the long-range progress-curve
analysis suggest concrete reporting patterns for our hierarchical-planning experiments. The
limitations the authors acknowledge - reliance on human subgoal annotation and simulated rather than
real-world environments - are exactly the cost we will inherit, and the absence of a
granularity-conditioning treatment in their design is precisely the gap our project intends to fill.
