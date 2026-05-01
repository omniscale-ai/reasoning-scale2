---
spec_version: "3"
paper_id: "10.48550_arXiv.2310.04406"
citation_key: "Zhou2024a"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models

## Metadata

* **File**: `files/zhou_2024_lats-agent-tree-search.pdf`
* **Published**: 2024 (ICML 2024; arXiv v1 Oct 2023, v3 Jun 2024)
* **Authors**: Andy Zhou (UIUC, Lapis Labs), Kai Yan (UIUC), Michal Shlapentokh-Rothman (UIUC),
  Haohan Wang (UIUC), Yu-Xiong Wang (UIUC)
* **Venue**: ICML 2024 (PMLR 235)
* **DOI**: `10.48550/arXiv.2310.04406`

## Abstract

While language models (LMs) have shown potential across a range of decision-making tasks, their
reliance on simple acting processes limits their broad deployment as autonomous agents. In this
paper, we introduce Language Agent Tree Search (LATS) -- the first general framework that synergizes
the capabilities of LMs in reasoning, acting, and planning. By leveraging the in-context learning
ability of LMs, we integrate Monte Carlo Tree Search into LATS to enable LMs as agents, along with
LM-powered value functions and self-reflections for proficient exploration and enhanced
decision-making. A key feature of our approach is the incorporation of an environment for external
feedback, which offers a more deliberate and adaptive problem-solving mechanism that surpasses the
constraints of existing techniques. Our experimental evaluation across diverse domains, including
programming, interactive question-answering (QA), web navigation, and math, validates the
effectiveness and generality of LATS in decision-making while maintaining competitive or improved
reasoning performance. Notably, LATS achieves state-of-the-art pass@1 accuracy (92.7%) for
programming on HumanEval with GPT-4 and demonstrates gradient-free performance (average score of
75.9) comparable to gradient-based fine-tuning for web navigation on WebShop with GPT-3.5.

## Overview

LATS unifies three previously fragmented strands of LM research -- internal reasoning (CoT, ToT,
RAP, self-consistency), external acting (ReAct, Reflexion, AdaPlanner), and planning via search --
into a single framework that wraps an LM agent in a Monte Carlo Tree Search (MCTS) loop. The core
observation is that the typical bottleneck of MCTS in reinforcement learning, namely the need for an
environment model that can revert to arbitrary states, does not apply to most LM tasks: the agent
can simply re-feed an earlier prompt prefix to recover a prior state. This makes MCTS naturally
applicable as an inference-time planner for LM agents.

The framework keeps every node in the tree as a triple of accumulated input, actions, and
observations, and uses the same LM in three distinct roles -- policy, value function, and reflection
generator. After each rollout, environment feedback (e.g., HotPotQA correctness, HumanEval test
output, WebShop reward, compiler errors) is backpropagated through the tree, while failed
trajectories are summarized into verbal self-reflections that are inserted as additional context for
later iterations. This couples search, external grounding, and Reflexion-style self-improvement into
one mechanism.

LATS is evaluated across HotPotQA (multi-hop QA), HumanEval and MBPP (programming), WebShop (web
navigation), and Game of 24 (math). In every domain it outperforms strong specialized baselines
including ReAct, Reflexion, ToT, and RAP, achieving 92.7% pass@1 on HumanEval with GPT-4 -- a
state-of-the-art result at submission time -- while also expanding fewer nodes than competing
tree-search methods upon success.

## Architecture, Models and Methods

LATS instantiates an MCTS variant with six operations: selection, expansion, evaluation, simulation,
backpropagation, and reflection. Each tree node `s = [x, a_{1..i}, o_{1..i}]` records the original
input plus the action and observation history. The action space follows ReAct, combining real
environment commands with free-form thought tokens; in pure-reasoning settings it falls back to CoT.
At each iteration the algorithm walks the tree using the UCT rule
`UCT(s) = V(s) + w * sqrt(ln N(p) / N(s))`, expands the chosen leaf by sampling `n` actions from the
LM, gathers environment observations, evaluates each child, and simulates downward until a terminal
node.

The value function is a novel hybrid `V(s) = lambda * LM(s) + (1 - lambda) * SC(s)`, mixing an
LM-as-judge correctness score (1-10 scale, prompted explicitly to reason then output a final score)
with a self-consistency term over repeated samples. `lambda = 0.5` is used for HotPotQA and Game of
24, `lambda = 0.8` for HumanEval, MBPP, and WebShop. Backpropagation updates each visited node's
value with the running average `V(s_i) <- (V_old(s_i)(N(s_i)-1) + r) / N(s_i)`. When a trajectory
ends in failure, the LM is prompted with the full trace to produce a verbal reflection, which is
stored in long-term memory and fed back into subsequent rollouts.

Default hyperparameters are `n = 5` children per expansion, exploration weight `w = 1`, and
trajectory budget `k = 50` (HotPotQA), `k = 8` (HumanEval/MBPP), `k = 30` (WebShop, Game of 24).
Maximum depths are 6 (HotPotQA), 8 (HumanEval), 15 (WebShop), and 5 (Game of 24). Backbone models
are GPT-3.5 and GPT-4 accessed through the OpenAI API; no parameters are updated, so LATS is a pure
inference-time, gradient-free method.

## Results

* **HumanEval pass@1**: LATS reaches **92.7%** with GPT-4 (vs Reflexion 91.0, base GPT-4 80.1) and
  **83.8%** with GPT-3.5 (vs Reflexion 68.1, RAP 63.1, ToT 54.4, CoT 46.9).
* **MBPP pass@1** with GPT-3.5: LATS **81.1%** vs RAP 71.4, Reflexion 70.0, ReAct 67.0, ToT 65.8,
  CoT 54.9.
* **HotPotQA EM** with GPT-3.5: reasoning-only LATS(CoT) **0.62**; acting LATS(ReAct) **0.63**;
  combined LATS(CoT+ReAct) **0.71**, doubling ReAct's 0.32 baseline and exceeding RAP's 0.54.
* **WebShop**: LATS **75.9** average score and **38.0** success rate, beating Reflexion (64.2 /
  35.0) and even gradient-based fine-tuning (67.5 / 45.0) on score, though still below human experts
  (82.1 / 59.6).
* **Game of 24** with GPT-3.5: LATS(CoT) **0.44** success rate vs RAP 0.40, ToT 0.20, Reflexion
  0.12, CoT 0.08.
* **Efficiency on HotPotQA at k=50**: LATS uses **66.65** average expanded nodes vs RAP 70.60 and
  ToT 84.05 while achieving higher accuracy (0.61 vs 0.54 vs 0.49); the gap grows for smaller `k`.
* **Token cost on HotPotQA upon success**: LATS 173,290 tokens vs RAP 176,500 vs ToT 210,215 -- same
  asymptotic `O(kn)` complexity but lower constants.
* **Ablations on HotPotQA**: removing the LM value function drops EM by **0.26**; replacing MCTS
  with DFS drops by **0.21**; removing self-reflection drops by **0.05**; lowering `w` from 1.0 to
  0.5 drops EM from 0.63 to 0.55.

## Innovations

### MCTS Adapted to Language Agents

LATS is the first work to integrate the full six-operation MCTS loop (selection, expansion,
evaluation, simulation, backpropagation, reflection) with an LM-as-agent setup that consumes real
environment observations. Unlike RAP, which requires the LM to act as a learned world model, LATS
directly queries the environment, eliminating the world-model bottleneck and making it applicable to
any environment that supports state reversion via prompt replay.

### Hybrid LM-as-Judge plus Self-Consistency Value Function

The proposed `V(s) = lambda * LM(s) + (1 - lambda) * SC(s)` combines an LM correctness score (with
chain-of-thought rationale) with a self-consistency frequency over repeated rollouts. Ablations show
LM scoring is the single most important component (0.26 EM drop when removed); self-consistency adds
a smaller but reliable boost (0.04 on Game of 24). This is one of the earliest concrete realizations
of an LM-as-judge value function used inside an MCTS planner for agent tasks.

### Unified Reasoning + Acting + Planning + Reflection

Table 1 of the paper places LATS in a quadrant where it is the only method to combine reasoning,
acting, planning, self-reflection, and external memory simultaneously, generalizing CoT, ReAct, ToT,
RAP, Reflexion, and Self-Refine. The paper also introduces a hybrid CoT+ReAct base agent that falls
back from internal reasoning to retrieval only on failure, mirroring a human "look it up if unsure"
heuristic.

### Reflection-as-Backprop-Signal

Failed terminal trajectories trigger an LM-generated natural-language reflection that is stored in
long-term memory and prepended to subsequent rollouts. This effectively turns Reflexion's
trial-by-trial improvement into a per-node semantic gradient that complements scalar UCT updates.

## Datasets

* **HotPotQA** (Yang et al., 2018): 113k Wikipedia-based multi-hop QA pairs; LATS evaluates on a
  random 100-question subset. Public and freely available.
* **HumanEval** (Chen et al., 2021): 164 hand-written Python programming problems with docstrings,
  reference implementations, and ~7.7 unit tests per problem; full set used. Public.
* **MBPP** (Austin et al., 2022): 974 short Python functions with three test cases each; 397
  randomly sampled problems used. Public.
* **WebShop** (Yao et al., 2022): simulated e-commerce environment with 1.18M Amazon products, 12k
  crowdsourced instructions, structured-text observations; 50 instructions evaluated. Public, MIT
  license.
* **Game of 24** (Yao et al., 2023a): mathematical reasoning task that requires producing 24 from
  four input numbers using basic arithmetic; 50 games evaluated. Public.

## Main Ideas

* **MCTS is a near-free lunch for LM agents** when the environment supports prompt-replay state
  reversion -- which covers most code, web, QA, and tool-use settings -- so LATS-style planners are
  a natural fit for hierarchical-agent benchmarks in this project.
* **LM-as-judge value functions work**, and combining them with self-consistency gives a
  surprisingly strong heuristic without any learned critic; this is a useful blueprint for the
  judge-side experiments planned in t0017's downstream tasks.
* **Verbal self-reflection adds an orthogonal signal to scalar rewards** -- small individually (0.05
  EM on HotPotQA) but compatible with search and worth keeping when deploying agents in
  partially-observable environments.
* **Tree search expands fewer nodes than alternatives** (3.55 fewer than RAP, 12.12 fewer than ToT
  on HotPotQA) at higher accuracy, so when budgeting agent experiments LATS is competitive on cost
  with simpler tree methods despite the extra reflection overhead.
* **Limitations matter**: LATS assumes state reversibility and is more expensive than ReAct or
  Reflexion per task; for highly stochastic real-world environments or strict latency budgets it is
  not the right tool.

## Summary

Zhou et al. introduce LATS, an inference-time framework that unifies LM-based reasoning, acting, and
planning by wrapping a ReAct-style agent in a Monte Carlo Tree Search loop. The paper situates
itself against a fragmented prior literature -- CoT and self-consistency for reasoning, ReAct and
Reflexion for acting, ToT and RAP for planning -- and shows that no existing method combines all of
reasoning, acting, planning, self-reflection, and external memory. LATS fills that gap by treating
the LM simultaneously as policy, state evaluator, and reflection generator, and by exploiting the
under-appreciated fact that LM environments allow trivial state reversion via prompt replay.

Methodologically the work contributes a six-operation MCTS adaptation (selection, expansion,
evaluation, simulation, backpropagation, reflection), a hybrid LM-score plus self-consistency value
function, and a memory of natural-language reflections that act as a semantic gradient signal across
rollouts. All operations are realized through prompting GPT-3.5 or GPT-4 with no fine-tuning, making
LATS gradient-free and immediately portable to any tool-using LM. Hyperparameters are deliberately
small: `n = 5` children, `w = 1`, and budgets of `k = 8` to `k = 50` rollouts.

The empirical findings are strong and consistent across four very different benchmarks. LATS sets
the state of the art on HumanEval pass@1 at 92.7% with GPT-4, doubles ReAct on HotPotQA, beats
gradient-based fine-tuning on WebShop score, and outperforms reasoning-specific methods on Game of
24\. Ablations confirm that every component matters: removing the LM value function costs 0.26 EM,
swapping MCTS for DFS costs 0.21, and dropping reflection costs 0.05. Cost analysis shows LATS
expands fewer nodes and consumes fewer tokens than ToT or RAP for the same `n` and `k`, partially
offsetting its higher per-step compute relative to ReAct.

For this project, LATS is a foundational reference point for the "agents and judges" literature
survey: it operationalizes both hierarchical search-based planning over an LM agent and an
LM-as-judge value function inside the same loop, which are exactly the two threads the t0017 survey
is meant to map. Practical takeaways are (1) tree search with explicit external feedback should be a
baseline whenever the project benchmarks support state reversion, (2) the
LM-score-plus-self-consistency value function is a cheap, training-free judge worth replicating in
ablations, and (3) reflection memory is a small but reliable add-on for any iterative-agent
pipeline. Limitations to keep in mind are the assumption of reversible environments and the
non-trivial inference cost, both of which constrain when LATS should be preferred over Reflexion or
plain ReAct.
