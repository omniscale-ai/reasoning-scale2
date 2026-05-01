# Papers: `hierarchical-planning` (14)

14 papers across 5 year(s).

[Back to all papers](../README.md)

---

## 2026 (1)

<details>
<summary>🏤 Solving the Granularity Mismatch: Hierarchical Preference Learning for
Long-Horizon LLM Agents — Gao et al., 2026</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_Gao2026_hierarchical-preference-learning-llm-agents` |
| **Authors** | Heyang Gao, Zexu Sun, Erxue Min, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Xu Chen |
| **Venue** | ICLR 2026 (conference) |
| **DOI** | — |
| **URL** | https://openreview.net/forum?id=s8usvGHYlk |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/no-doi_Gao2026_hierarchical-preference-learning-llm-agents/summary.md) |

Gao et al. tackle a real and well-defined problem in offline alignment of long-horizon LLM
agents: trajectory-level DPO is too coarse to attribute failure to a specific sub-task, and
step-level DPO is too noisy to capture the value of multi-step behaviour. They name this the
granularity mismatch and frame their solution, Hierarchical Preference Learning (HPL), as a
multi-resolution loss combined with a structured training schedule, rather than a single new
objective.

Methodologically, HPL has four moving parts: an LLM-driven segmenter that splits expert
trajectories into semantically coherent action groups, a procedure that generates contrasting
suboptimal groups via behaviour-cloned rollouts, a hierarchical DPO loss that sums
trajectory-, step-, and group-level DPO terms, and a dual-layer curriculum that orders
preference pairs by group length and reward gap. The curriculum runs in three phases and is
shown to be necessary in ablations. A bias-variance proposition gives theoretical grounding to
the choice of group-level granularity.

The empirical story is unambiguous. On three standard agent benchmarks (ALFWorld, WebShop,
InterCode-SQL) and two base models (Qwen2.5-1.5B / 7B), HPL beats SFT, ETO, and IPR. The
Qwen2.5-7B average rises from 63.84 (IPR) to 67.81 (HPL), with the largest gain on ALFWorld
seen (+10.71) and unseen (+8.96). Ablations cleanly localise the gain: the group-level DPO
term is the single most important component, the semantic segmenter beats fixed-length
alternatives, and the two-axis curriculum contributes about a full average point.

For this project, HPL is directly relevant in three ways. First, the granularity-mismatch
framing maps onto our scope-aware / scope-unaware / scope-mismatched conditions: HPL's group
level is exactly the subtask level in our hierarchy. Second, semantic action-group
segmentation is a methodology we can borrow when annotating gold actions at the subtask level
on FrontierScience-Olympiad, WorkArena++, tau-bench, and SWE-bench Verified. Third, HPL
provides a recent, strong, reproducible baseline if any downstream task in our pipeline trains
a scope-aware policy. Limitations: HPL relies on GPT-4o for segmentation (cost and licence
implications) and on the existence of expert demonstrations, neither of which transfers
automatically to settings without high-quality demos.

</details>

## 2024 (8)

<details>
<summary>🏤 AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents —
Ma et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2401.13178` |
| **Authors** | Chang Ma, Junlei Zhang, Zhihao Zhu, Cheng Yang, Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng Kong, Junxian He |
| **Venue** | NeurIPS 2024 Datasets and Benchmarks (conference) |
| **DOI** | `10.48550/arXiv.2401.13178` |
| **URL** | https://arxiv.org/abs/2401.13178 |
| **Date added** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2401.13178/summary.md) |

Ma et al. introduce AgentBoard, a NeurIPS 2024 Datasets-and-Benchmarks oral that addresses two
fundamental measurement problems in LLM-agent evaluation: incompatible task interfaces across
existing benchmarks and the loss of information caused by reporting only end-of-trajectory
success rate. The authors argue, with evidence, that current open-weight LLMs cluster at
near-zero success on hard agent tasks, so any "progress" between models is invisible. They
propose a unified POMDP formulation, nine carefully curated text-only multi-round
partially-observable environments (AlfWorld, ScienceWorld, BabyAI, Jericho, PDDL, WebShop,
WebArena, Tool-Query, Tool-Operation), and a fine-grained progress-rate metric defined per
interaction step.

Methodologically, the progress rate has two forms (continuous state-similarity and discrete
subgoal-coverage). Subgoal sequences were hand-annotated for all 1013 environments and about
5% of problems were edited so each goal admits a unique ordering. A 60-trajectory-per-task
user study with four expert raters gives Pearson rho > 0.95 between human and automatic
progress, validating the metric. The benchmark ships with an open-source W&B visualisation
panel that breaks performance down by sub-skill (memory, planning, world modelling,
self-reflection, grounding, spatial navigation), by easy/hard difficulty (defined by subgoal
count), and by step number.

The empirical findings are that GPT-4 leads at **70.0% progress / 47.9% success**, followed by
Claude 2 (**48.9% / 26.2%**) and Gemini-1.5-Flash (**43.5% / 20.6%**); open-weight models lag
substantially with the strongest (Llama3-70b at **41.9% / 20.2%**) still well below GPT-4.
Critical analyses show that progress rate separates models that look indistinguishable under
success rate (Llama2-13b vs Mistral-7b), that all models drop sharply on hard examples (GPT-4
success: 85.0% to 24.9%), that open-weight models plateau by step 6 while frontier models
continue progressing through step 30, and that code-pretrained open-weight LLMs (CodeLlama,
Lemur) outperform their non-code counterparts.

For this project, AgentBoard is highly relevant in three ways. First, the progress-rate
construction is a direct candidate for our task-success metric (Metric 1), giving us a
continuous, per-step comparable signal across A/B/C conditions instead of a binary outcome.
Second, the subgoal-annotation methodology - per-environment manual labelling, uniqueness
editing, multi-stage verification, and a four-author user study - is a working template for
the >=100-task annotated benchmark this project must build over SWE-bench Verified, tau-bench,
WorkArena++, and FrontierScience. Third, the easy/hard split by subgoal count and the
long-range progress-curve analysis suggest concrete reporting patterns for our
hierarchical-planning experiments. The limitations the authors acknowledge - reliance on human
subgoal annotation and simulated rather than real-world environments - are exactly the cost we
will inherit, and the absence of a granularity-conditioning treatment in their design is
precisely the gap our project intends to fill.

</details>

<details>
<summary>🏤 ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL
— Zhou et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2402.19446` |
| **Authors** | Yifei Zhou, Andrea Zanette, Jiayi Pan, Sergey Levine, Aviral Kumar |
| **Venue** | ICML 2024 (conference) |
| **DOI** | `10.48550/arXiv.2402.19446` |
| **URL** | https://arxiv.org/abs/2402.19446 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.19446/summary.md) |

This paper develops ArCHer (Actor-Critic Framework with a Hierarchical Structure), a framework
for multi-turn reinforcement learning of language model agents. The motivation is that real
LLM agent tasks — web navigation, tool use, customer support, dialogue — involve long
horizons, hidden information that has to be acquired across turns, and rewards that arrive
only at the end of an episode, but the dominant LLM-RL recipes (PPO over flattened sequences,
RLHF-style single-turn optimization) handle none of these well. The authors argue that a
hierarchical framing is a natural fix that has been missing from the LLM-RL literature.

Methodologically, ArCHer runs two RL algorithms simultaneously at different time-scales. A
high-level off-policy critic, trained with temporal-difference learning, replay buffers, and
double-Q targets, learns Q- and V-functions over utterance-level state-action pairs. A
low-level on-policy token policy gradient (REINFORCE with optional baseline) updates the LLM
itself, using the high-level critic to produce a per-utterance advantage that is broadcast
over the utterance's tokens. This decoupling preserves the per-token expressivity that makes
LLM RL work while delegating long-horizon credit assignment to a tractable utterance-level
Bellman update.

The empirical evidence is striking. On Twenty Questions, Twenty Questions 10-word, Guess My
City, and WebShop, ArCHer matches or outperforms strong baselines (online PPO, online filtered
BC, CHAI) with roughly **100x fewer environment interactions** than online PPO. A GPT-2 actor
(~100M parameters) trained with ArCHer **beats GPT-3.5 with prompting** on WebShop.
Performance keeps improving as the actor is scaled from GPT-2 to Mistral-7B, suggesting the
framework composes cleanly with model scale rather than being a small-model artifact.

For the t0017 literature survey on hierarchical agents and judges, ArCHer is a load-bearing
reference. It provides direct evidence that explicit hierarchy in the action space — utterance
vs token — yields large practical gains, mirroring the global / subtask / atomic decomposition
used in this project's annotation schema. The two-level credit-assignment story is also the
right shape for the project's scope-aware vs scope-unaware experimental conditions: ArCHer is
essentially a "scope-aware" trainer that knows which level of the hierarchy each decision
lives at. The main caveats for downstream use are that all evaluation is on relatively
short-horizon text games (max ~20 turns), no SWE-bench or WorkArena-style benchmarks are
tested, and the critic is small (RoBERTa-base) which may not scale to harder reasoning agents.

</details>

<details>
<summary>🏤 Can Graph Learning Improve Planning in LLM-based Agents? — Wu et al.,
2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2405.19119` |
| **Authors** | Xixi Wu, Yifei Shen, Caihua Shan, Kaitao Song, Siwei Wang, Bohang Zhang, Jiarui Feng, Hong Cheng, Wei Chen, Yun Xiong, Dongsheng Li |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2405.19119` |
| **URL** | https://arxiv.org/abs/2405.19119 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.19119/summary.md) |

This paper studies LLM agent planning through the lens of graph learning. The authors observe
that breaking a user request into sub-tasks naturally produces a directed graph whose nodes
are tools or sub-tasks and whose edges are resource dependencies, and they prove two
theoretical limitations of pure LLM planners on this graph: a single-head attention layer
cannot retrieve neighbour information from a textually encoded graph, and auto-regressive
next-token loss induces spurious correlations between query tokens and node names. These
results motivate adding a graph-native inductive bias.

Methodologically, the paper introduces two integration recipes. A training-free design uses a
1-hop SGC propagation over frozen sentence embeddings to score candidate path nodes by
neighbour-aware cosine similarity to the user query — no parameters, no fine-tuning. A
training-required design trains a small GraphSAGE encoder with a Bayesian Personalised Ranking
loss on LLM-bootstrapped labels, in 3-15 minutes on a single GPU, then selects a connected
subgraph for multi-step planning. Both designs are evaluated on four TaskBench/RestBench
datasets and on UltraTool across six LLM backbones from GPT-4 to Mistral-7B.

The headline findings are that GNN augmentation lifts node F1 by up to ~20 absolute points on
HuggingFace, improves UltraTool plan accuracy by 9.05% on GPT-4-turbo, drops the hallucination
rate from over 20% to under 1%, and yields larger gains on bigger graphs and weaker LLMs.
Training cost is roughly 80x lower than fine-tuning the LLM baseline, and the
open-source-vs-proprietary gap narrows substantially after augmentation.

For our hierarchical-agents project this work is directly relevant. It provides a theoretical
justification and a cheap, well-tested mechanism for adding a structural verifier or "judge"
on top of an LLM planner, and it documents a scaling pattern (gain grows with graph size) that
argues for investing in graph-aware mechanisms as soon as the agent's tool or sub-task
catalogue is non-trivial. The dataset suite (TaskBench + UltraTool) is a strong candidate for
our own hierarchical-planning evaluations, and the SGC plug-in is a useful zero-cost baseline
to include in any LLM-judge or LLM-planner ablation we run.

</details>

<details>
<summary>🏤 Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making
— Li et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2410.07166` |
| **Authors** | Manling Li, Shiyu Zhao, Qineng Wang, Kangrui Wang, Yu Zhou, Sanjana Srivastava, Cem Gokmen, Tony Lee, Li Erran Li, Ruohan Zhang, Weiyu Liu, Percy Liang, Li Fei-Fei, Jiayuan Mao, Jiajun Wu |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2410.07166` |
| **URL** | https://arxiv.org/abs/2410.07166 |
| **Date added** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2410.07166/summary.md) |

Li et al. introduce Embodied Agent Interface (EAI), a unified PDDL/BDDL-grounded evaluation
framework for using LLMs as decision-making components in embodied agents. The motivation is
the fragmentation of prior work: papers run different LLMs on different simulators with
different input-output conventions and report only an end-to-end success rate, so it is
impossible to tell which sub-skill — instruction parsing, plan structuring, low-level action
choice, or world modeling — is actually limiting performance. EAI fixes the interface and the
metrics so that any LLM can be plugged into any of four canonical modules and scored with the
same fine-grained error taxonomy across two distinct simulators.

Methodologically, the framework formalizes every embodied task as an initial symbolic state
plus a goal formula over object states, relations, or LTL action sequences, and defines four
typed LLM modules: goal interpretation, subgoal decomposition, action sequencing, and
transition modeling. Each module's outputs are parsed and checked against ground-truth domains
and trajectories, with parse errors separated from semantic errors and a seven-way error
taxonomy (hallucination, affordance, missing-step, wrong-order, additional-step,
missing-precondition, missing-effect) computed automatically. The benchmark instantiates this
interface on VirtualHome (338 tasks, 801 goals, 8.76-step trajectories) and BEHAVIOR (100
tasks, 673 goals, 14.6-step trajectories) and evaluates eighteen LLMs.

The headline finding is that o1-preview, the only test-time reasoning model in the cohort,
dominates across all four modules — for example, **81.0% goal SR / 91.0% execution SR** on
BEHAVIOR action sequencing and **71.1% goal SR** on VirtualHome action sequencing —
establishing inference-time reasoning as the strongest predictor of embodied decision quality.
Open-weight models pay a large grammar-error tax and lag on long-horizon action sequencing,
while transition modeling is a notable weakness across the board: even the best models hit
only **78.8% F1** on BEHAVIOR object-state effects. Failure modes also differ by simulator,
with hallucination / affordance errors dominating on VirtualHome and missing-step /
wrong-order errors on BEHAVIOR.

For our project, EAI is directly relevant on three axes. First, its four-module decomposition
is a near-isomorphic precedent for our hierarchical-planning agent design and validates the
scope-conditioned A/B/C ablation: by typing each module's inputs and outputs we gain the same
diagnostic resolution. Second, its symbolic error taxonomy is the right shape for our
overconfident-error-rate metric and our scope-mismatched failure analysis; we should adopt
hallucination/affordance/missing-step labels in our annotation schema. Third, EAI's evidence
that test-time reasoning beats raw scale strongly motivates including reasoning-trained
backends as our default A-condition agent and ensures our judges and predictions cover both
reasoning and non-reasoning model families.

</details>

<details>
<summary>🏤 Language Agent Tree Search Unifies Reasoning, Acting, and Planning in
Language Models — Zhou et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2310.04406` |
| **Authors** | Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, Yu-Xiong Wang |
| **Venue** | ICML 2024 (conference) |
| **DOI** | `10.48550/arXiv.2310.04406` |
| **URL** | https://arxiv.org/abs/2310.04406 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2310.04406/summary.md) |

Zhou et al. introduce LATS, an inference-time framework that unifies LM-based reasoning,
acting, and planning by wrapping a ReAct-style agent in a Monte Carlo Tree Search loop. The
paper situates itself against a fragmented prior literature -- CoT and self-consistency for
reasoning, ReAct and Reflexion for acting, ToT and RAP for planning -- and shows that no
existing method combines all of reasoning, acting, planning, self-reflection, and external
memory. LATS fills that gap by treating the LM simultaneously as policy, state evaluator, and
reflection generator, and by exploiting the under-appreciated fact that LM environments allow
trivial state reversion via prompt replay.

Methodologically the work contributes a six-operation MCTS adaptation (selection, expansion,
evaluation, simulation, backpropagation, reflection), a hybrid LM-score plus self-consistency
value function, and a memory of natural-language reflections that act as a semantic gradient
signal across rollouts. All operations are realized through prompting GPT-3.5 or GPT-4 with no
fine-tuning, making LATS gradient-free and immediately portable to any tool-using LM.
Hyperparameters are deliberately small: `n = 5` children, `w = 1`, and budgets of `k = 8` to
`k = 50` rollouts.

The empirical findings are strong and consistent across four very different benchmarks. LATS
sets the state of the art on HumanEval pass@1 at 92.7% with GPT-4, doubles ReAct on HotPotQA,
beats gradient-based fine-tuning on WebShop score, and outperforms reasoning-specific methods
on Game of 24\. Ablations confirm that every component matters: removing the LM value function
costs 0.26 EM, swapping MCTS for DFS costs 0.21, and dropping reflection costs 0.05. Cost
analysis shows LATS expands fewer nodes and consumes fewer tokens than ToT or RAP for the same
`n` and `k`, partially offsetting its higher per-step compute relative to ReAct.

For this project, LATS is a foundational reference point for the "agents and judges"
literature survey: it operationalizes both hierarchical search-based planning over an LM agent
and an LM-as-judge value function inside the same loop, which are exactly the two threads the
t0017 survey is meant to map. Practical takeaways are (1) tree search with explicit external
feedback should be a baseline whenever the project benchmarks support state reversion, (2) the
LM-score-plus-self-consistency value function is a cheap, training-free judge worth
replicating in ablations, and (3) reflection memory is a small but reliable add-on for any
iterative-agent pipeline. Limitations to keep in mind are the assumption of reversible
environments and the non-trivial inference cost, both of which constrain when LATS should be
preferred over Reflexion or plain ReAct.

</details>

<details>
<summary>🏤 Reinforcing Language Agents via Policy Optimization with Action
Decomposition — Wen et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2405.15821` |
| **Authors** | Muning Wen, Ziyu Wan, Weinan Zhang, Jun Wang, Ying Wen |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2405.15821` |
| **URL** | https://arxiv.org/abs/2405.15821 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.15821/summary.md) |

Wen et al. confront a structural tension in RL fine-tuning of LLM agents: action-level methods
(GLAM, TWOSOME) must hand-prune the action space and fail to assign credit to specific tokens
inside an action, while naive token-level methods that embed token generation into the MDP
implicitly assume that later tokens are more important than earlier ones. The paper makes this
informal complaint formal by deriving a closed-form expression for the discrepancy between
action-level and naive token-level Bellman updates, splitting the discount factor into gamma_a
and gamma_w and showing the discrepancy is proportional to (1 - gamma_w^{|a_t|-j}).

The fix is the Bellman backup with Action Decomposition (BAD): set gamma_w = 1 and only apply
gamma_a at the action boundary, which the authors prove recovers the action-level optimum
exactly while still giving per-token credit. They package BAD inside PPO as POAD, with a
critic loss that explicitly splits intra-action and inter-action errors and an actor loss that
uses per-token clipped ratios and GAE-estimated per-token advantages. The complexity drops
from O(|V|^|a|) to O(|a| * |V|).

Empirically, POAD wins on three families of tasks. On Overcooked and VirtualHome it converges
faster and more stably than TWOSOME and beats NTPO clearly. On 8 unseen Food Preparation
variants it wins 7 of 8 against TWOSOME, NTPO, and the LLaMA2-7B base model. Most importantly,
on the new DataSciCoding benchmark, where TWOSOME is inapplicable because the action space is
unrestricted, POAD-Best with CodeLLaMA-7B beats CAAFE with GPT-4 on every one of six datasets
while training in under three hours on a single A100. Ablations on gamma_w track the
theoretical prediction that the NTPO-vs-POAD gap widens as gamma_w drops, and the LLM
Evaluation Harness shows no loss of base language ability.

For our project, this paper is directly relevant in three ways. First, it gives the most
rigorous existing answer to "what is the right granularity for assigning credit inside an LLM
agent's action," which is the formal counterpart of the v2 hierarchical-annotation result from
t0009 and t0014. Second, the length-dependence of the action-level/token-level discrepancy
predicts that any scope-aware vs scope-mismatched ABC condition that varies action length will
see widening performance gaps under TWOSOME-style updates - a useful theoretical anchor for
our Phase 2 ABC analysis. Third, POAD's unrestricted-action-space results on DataSciCoding
suggest that, if we ever move beyond evaluation into RL fine-tuning of judges or agents,
BAD/POAD is the principled starting point. The main caveat is that POAD requires a
quantitative reward function, which is not available in our annotation-only pipeline; this
aligns with the authors' own listed limitation.

</details>

<details>
<summary>🏤 SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures
— Zhou et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2402.03620` |
| **Authors** | Pei Zhou, Jay Pujara, Xiang Ren, Xinyun Chen, Heng-Tze Cheng, Quoc V. Le, Ed H. Chi, Denny Zhou, Swaroop Mishra, Huaixiu Steven Zheng |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2402.03620` |
| **URL** | https://arxiv.org/abs/2402.03620 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.03620/summary.md) |

SELF-DISCOVER tackles the question of whether LLMs can themselves compose the right reasoning
program for a task instead of relying on a fixed prompting template. The authors argue that
single-shape methods like CoT and Plan-and-Solve are mismatched to many tasks, and that a
task's intrinsic reasoning structure is best discovered explicitly. Their framework supplies
the LLM with a pool of 39 atomic reasoning modules and three meta-prompts (SELECT, ADAPT,
IMPLEMENT) that pick, specialize, and lay out a JSON reasoning structure per task; this
structure is then reused across all instances of the task at no per-instance overhead beyond
plain CoT.

The methodology runs Stage 1 once per task (three inference calls) and Stage 2 once per
instance. Models tested are GPT-4, GPT-3.5, PaLM 2-L, and Llama-2-70B, evaluated on 23
BIG-Bench Hard tasks, the T4D grounded-agent task, and 200 MATH test problems. Baselines span
Direct, CoT, Plan-and- Solve, CoT-Self-Consistency, per-module majority voting, oracle
best-of-each-module, and the OPRO prompt optimizer. Ablations on SELECT/ADAPT/IMPLEMENT and a
transfer study from PaLM 2-L to GPT-4 and GPT-4 to Llama-2-70B round out the experiments.

Headline results: SELF-DISCOVER beats CoT by 6-7 absolute on BBH average and by 27-32 absolute
on T4D for both PaLM 2-L and GPT-4, and beats CoT-Self-Consistency and per-module majority
voting while using 10-40x fewer inference calls. On MATH the gain is modest (1-7 points), and
74.7% of remaining failures are downstream computation errors rather than structural reasoning
errors. Discovered structures transfer across model families with most of the gain retained,
indicating that reasoning structure is a portable abstraction.

For the t0017 hierarchical-agents-and-judges literature survey, this paper is directly
relevant because it operationalizes a hierarchical reasoning idea: a task-level "planner"
composes an explicit structure that an instance-level "executor" then fills in. It
demonstrates that explicit JSON-structured plans beat free-text plans, that task-level
meta-prompts amortize cleanly to per- instance cost, and that structured reasoning is more
transferable than wording. These findings support hierarchical-agent designs that separate
plan composition from plan execution and motivate judges that evaluate structural correctness
independently from value-filling correctness — the exact decomposition this project's
hierarchical-judge designs are exploring.

</details>

<details>
<summary>🏤 WorkArena++: Towards Compositional Planning and Reasoning-based Common
Knowledge Work Tasks — Boisvert et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2407.05291` |
| **Authors** | Léo Boisvert, Megh Thakkar, Maxime Gasse, Massimo Caccia, Thibault Le Sellier De Chezelles, Quentin Cappart, Nicolas Chapados, Alexandre Lacoste, Alexandre Drouin |
| **Venue** | NeurIPS 2024 Datasets and Benchmarks Track (conference) |
| **DOI** | `10.48550/arXiv.2407.05291` |
| **URL** | https://arxiv.org/abs/2407.05291 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/summary.md) |

WorkArena++ extends the 33 atomic WorkArena task families into 682 compositional
knowledge-work tasks evaluated on the same ServiceNow + BrowserGym substrate. The motivation
is that prior benchmarks measure either atomic or end-to-end success but rarely the gap
between the two — the gap that explains why agents that handle individual web actions still
cannot complete realistic enterprise workflows.

Methodologically, the paper composes WorkArena atomic operations into multi-step workflows
whose ground-truth solutions exercise five skill axes: planning, problem-solving,
logical/arithmetic reasoning, retrieval, and contextual understanding. Evaluation uses the
BrowserGym harness with SOTA LLMs, VLMs, and human workers as comparison points. A trace
generator produces synthetic gold action sequences for fine-tuning research.

The headline finding is a **considerable gap** to full automation across all evaluated
systems, with detailed per-skill breakdowns in the NeurIPS 2024 D&B paper. The
atomic-vs-compositional gap is the central observation — agents that succeed on individual web
actions consistently fail to coordinate them across a multi-step workflow.

For the granularity-aware hierarchical agents project, WorkArena++ is the most directly
relevant single benchmark. It is the strongest test bed for sub-hypothesis 1 (gains
concentrated where local execution needs information not needed for higher-level planning); it
shares a harness with WorkArena, lowering integration cost; and its synthetic trace generator
can supply gold atomic actions to complement the project's manual global/subtask annotation.
The project should treat WorkArena++ as the primary metric source for Phase 2 stratified
analysis.

</details>

## 2023 (3)

<details>
<summary>🏤 Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning
by Large Language Models — Wang et al., 2023</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2305.04091` |
| **Authors** | Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, Ee-Peng Lim |
| **Venue** | ACL 2023 (conference) |
| **DOI** | `10.48550/arXiv.2305.04091` |
| **URL** | https://arxiv.org/abs/2305.04091 |
| **Date added** | 2026-04-29 |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/summary.md) |

Plan-and-Solve (PS) prompting is a zero-shot prompting technique that explicitly forces a
language model to first produce a plan, then execute the plan step by step. The motivation is
that Zero-shot-CoT — while a powerful zero-shot baseline — exhibits three error modes:
calculation errors, missing-step errors, and semantic-misunderstanding errors. PS targets the
missing-step mode by demanding an explicit plan; PS+ extends to calculation errors via
additional in-prompt instructions to "pay attention to correct numerical calculation."

Methodologically, PS is a single-prompt template that instructs the model to plan-then-solve.
Evaluation covers ten datasets across arithmetic, commonsense, and symbolic reasoning, all in
zero-shot mode with GPT-3 text-davinci-003 as the primary model. PS+ adds more detailed
per-stage instructions.

The headline outcome is **consistent improvement over Zero-shot-CoT across all 10 datasets**,
with PS+ achieving **comparable performance to 8-shot manual CoT** on GSM8K (≈58% vs ≈57%) — a
strong zero-shot result that eliminates the manual exemplar-curation cost. PS+ is available in
LangChain core as Plan-and-Execute and has been adopted in production agent systems.

For the granularity-aware hierarchical agents project, PS is the canonical scope-unaware (B)
baseline for Phase 2. Its two-stage plan-then-solve structure is the closest published
analogue to the project's scope-aware (A) condition without the explicit granularity tags. The
project should reuse LangChain's Plan-and-Execute implementation, log both stages separately,
and measure how much of PS's gain over CoT comes from the plan-execute separation alone — that
delta is the lower bound for the scope-aware (A) condition's expected gain.

</details>

<details>
<summary>🏤 ReAct: Synergizing Reasoning and Acting in Language Models — Yao et al.,
2023</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2210.03629` |
| **Authors** | Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao |
| **Venue** | ICLR 2023 (conference) |
| **DOI** | `10.48550/arXiv.2210.03629` |
| **URL** | https://arxiv.org/abs/2210.03629 |
| **Date added** | 2026-04-29 |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/summary.md) |

ReAct introduces an agent prompting paradigm where the language model alternates between
Thought tokens (free-form reasoning) and Action tokens (calls to external tools or
environments). The motivation is that prior work treated reasoning (chain-of-thought) and
acting (tool-use) as separate problems, missing the synergy where reasoning helps the agent
track and update its plan while acting lets the agent ground its reasoning in real
information.

Methodologically, ReAct uses one or two in-context examples to teach the model the
Thought/Action/Observation pattern, then runs autoregressively until the model emits a Finish
action. No fine-tuning is required. The paper evaluates on HotpotQA, Fever (knowledge tasks)
and ALFWorld, WebShop (interactive decision-making tasks).

The headline result is **+34 absolute** success-rate improvement on ALFWorld and **+10
absolute** on WebShop, both compared to imitation and reinforcement-learning baselines. ReAct
also reduces hallucination on HotpotQA and improves fact-verification on Fever via Wikipedia
API grounding, with the bonus of producing human-interpretable trajectories.

For the granularity-aware hierarchical agents project, ReAct is the conceptual ancestor of the
three-level granularity schema. The project's scope-aware (A) condition can be implemented as
a ReAct extension with explicit per-token granularity tags, preserving ReAct's
interpretability while adding scope discipline. The +34 ALFWorld gain is the strongest
published evidence that prompt-only agent improvements can produce large absolute effect sizes
— the project's +5-to-+15 abs targets are conservative against this benchmark.

</details>

<details>
<summary>🏤 Reflexion: Language Agents with Verbal Reinforcement Learning — Shinn
et al., 2023</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2303.11366` |
| **Authors** | Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao |
| **Venue** | NeurIPS 2023 (conference) |
| **DOI** | `10.48550/arXiv.2303.11366` |
| **URL** | https://arxiv.org/abs/2303.11366 |
| **Date added** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/summary.md) |

Reflexion is a language-agent framework that adds a verbal self-reflection loop on top of
ReAct-style prompting agents. After each trial, the agent writes a free-form natural-language
critique of its own behavior, stores the critique in an episodic memory buffer, and uses the
buffer as additional context for the next trial. No model weights are updated — the learning
is entirely linguistic.

Methodologically, Reflexion has three components: an actor (ReAct policy), an evaluator
(scalar or free-form feedback), and a reflector (LLM in critique mode). The architecture is
evaluated on HumanEval coding, AlfWorld sequential decision-making, and HotpotQA reasoning,
with ablations on feedback type, feedback source, and reflection horizon.

The headline result is **91% pass@1 on HumanEval** with GPT-4 + Reflexion, an **+11 absolute**
gain over vanilla GPT-4 (80%) without any weight updates. Free-form text feedback outperforms
scalar feedback; internally simulated feedback is nearly as effective as external feedback;
last-trial reflection captures most of the gain.

For the granularity-aware hierarchical agents project, Reflexion's actor/evaluator/reflector
decomposition aligns with the global/subtask/atomic schema and is a strong template for the
scope-aware (A) condition's between-trial component. However, including cross-trial memory in
Phase 2 would conflate scope conditioning with episodic memory; Reflexion should be treated as
a Phase 3 ablation that tests whether memory adds gains *on top of* scope conditioning, not as
the Phase 2 baseline.

</details>

## 2022 (1)

<details>
<summary>🏤 Least-to-Most Prompting Enables Complex Reasoning in Large Language
Models — Zhou et al., 2022</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2205.10625` |
| **Authors** | Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, Ed Chi |
| **Venue** | ICLR 2023 (conference) |
| **DOI** | `10.48550/arXiv.2205.10625` |
| **URL** | https://arxiv.org/abs/2205.10625 |
| **Date added** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2205.10625/summary.md) |

Least-to-Most (LtM) prompting is a two-stage prompting technique designed to overcome
chain-of- thought's easy-to-hard generalization gap. The first stage decomposes a complex
problem into a sequence of simpler subproblems ordered by difficulty; the second stage solves
each subproblem using the answers to previously solved subproblems as additional context. The
motivation is that CoT performs well on test problems similar to in-context exemplars but
degrades sharply when test problems are harder.

Methodologically, LtM uses the same model (GPT-3 code-davinci-002 in the headline experiments)
in two prompting modes: decomposition and sequential solving. Evaluation covers SCAN
(compositional generalization), GSM8K (math), MultiArith (math), DROP (reading comprehension),
and Last Letter Concatenation (symbolic).

The headline result is **>=99% accuracy on SCAN length-split** with **just 14 exemplars**, vs.
**16% with vanilla chain-of-thought** — a **+83 absolute** gain. Other tasks show smaller but
consistent gains, with the improvement scaling with the easy-to-hard difficulty gap between
exemplars and test problems.

For the granularity-aware hierarchical agents project, LtM is the strongest empirical anchor
for the scope-aware (A) condition's expected effect size on hierarchical tasks. The +83
absolute SCAN gain sets the aspirational ceiling; the project's +5-to-+15 abs target on the
four-source composite is conservative against this anchor. Solution-reuse — each subproblem
using prior solutions in its context — is a detail worth replicating in scope-aware (A); pure
decomposition without solution-reuse loses much of LtM's gain.

</details>

## 1999 (1)

<details>
<summary>📖 Between MDPs and semi-MDPs: A framework for temporal abstraction in
reinforcement learning — Sutton et al., 1999</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_Sutton1999_options-framework` |
| **Authors** | Richard S. Sutton, Doina Precup, Satinder Singh |
| **Venue** | Artificial Intelligence (journal) |
| **DOI** | `10.1016/S0004-3702(99)00052-1` |
| **URL** | https://www.sciencedirect.com/science/article/pii/S0004370299000521 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/no-doi_Sutton1999_options-framework/summary.md) |

Sutton, Precup, and Singh address a foundational gap in reinforcement learning theory:
classical MDPs operate at a single discrete time scale and cannot natively express temporally
extended courses of action like "drive to the airport" or "search a room". They propose the
*options framework*, in which an option `<I, pi, beta>` packages an initiation set, an
internal closed-loop policy, and a stochastic termination condition. Primitive actions become
one-step options, so the framework strictly extends - rather than replaces - the existing MDP
formalism. The motivation is to find the *minimal* extension that enables temporally abstract
knowledge while preserving every standard RL algorithm.

Methodologically, the authors prove that any MDP equipped with a fixed option set induces a
semi-Markov decision process (SMDP) at the option level, so SMDP value iteration and
Q-learning - including the multi-time discount model `r^o_s` and `p^o_{ss'} = sum_k p(s', k)
gamma^k` - apply unchanged. They then go beyond SMDP theory in three directions: (1) the
*interruption theorem* proves that switching options whenever `Q^mu(s, o) < V^mu(s)` strictly
improves the policy, (2) *intra-option learning* lets a single trajectory update value
estimates for every option whose policy is consistent with the observed action, and (3)
*subgoal-based improvement* shows that defining a per-option pseudo-reward and running policy
improvement against it yields strictly better options.

Empirically, in a 4-rooms gridworld with 8 hand-designed hallway options, synchronous value
iteration with options reaches the optimal value function in 2 iterations versus diameter-many
for primitives, and SMDP Q-learning attains the goal far faster on the very first episode. The
combined option set `A union H` works robustly even when the goal lies in a room interior,
where hallway-only planning is insufficient. A continuous 2-D navigation task illustrates that
the interruption theorem tightens trajectories around obstacles. The headline qualitative
result is that all of this is accomplished without committing to any particular hierarchy,
function approximator, or state abstraction.

For this project the paper is foundational. The three-level hierarchy (global / subtask /
atomic) is naturally expressed as options at different time scales, and conditions A/B/C can
be formalized as the *same* option library executed under different conditioning policies. The
interruption theorem provides theoretical backing for the "can-execute-now vs. must-request"
distinction (Metric 3): an agent that interrupts a subtask whenever continuing is dominated
makes better request decisions, and the resulting policy improvement is provably bounded below
by the SMDP-optimal policy. The intra-option learning result is relevant for any future task
that wants to learn from partial trajectories of agent runs, and the subgoal construction
gives a principled way to derive options from gold sub-actions produced during benchmark
annotation. We should treat this paper as the canonical reference whenever the project
formalizes the relationship between hierarchy levels and conditioning.

</details>
