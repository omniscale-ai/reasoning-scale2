# Category: Agent Evaluation

Running the A/B/C conditions against annotated tasks and computing the three project metrics.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (14)](../papers/by-category/agent-evaluation.md) | [Answers
(2)](../answers/by-category/agent-evaluation.md) | [Suggestions
(59)](../suggestions/by-category/agent-evaluation.md) | [Datasets
(4)](../datasets/by-category/agent-evaluation.md) | [Libraries
(7)](../libraries/by-category/agent-evaluation.md) | [Predictions
(10)](../predictions/by-category/agent-evaluation.md)

---

## Papers (14)

<details>
<summary>🏤 <strong>WorkArena++: Towards Compositional Planning and Reasoning-based
Common Knowledge Work Tasks</strong> — Boisvert et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2407.05291` |
| **Authors** | Léo Boisvert, Megh Thakkar, Maxime Gasse, Massimo Caccia, Thibault Le Sellier De Chezelles, Quentin Cappart, Nicolas Chapados, Alexandre Lacoste, Alexandre Drouin |
| **Venue** | NeurIPS 2024 Datasets and Benchmarks Track (conference) |
| **DOI** | `10.48550/arXiv.2407.05291` |
| **URL** | https://arxiv.org/abs/2407.05291 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-workarena`](../../meta/categories/benchmark-workarena/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/summary.md) |

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

<details>
<summary>🏤 <strong>WorkArena: How Capable Are Web Agents at Solving Common Knowledge
Work Tasks?</strong> — Drouin et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2403.07718` |
| **Authors** | Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H. Laradji, Manuel Del Verme, Tom Marty, Léo Boisvert, Megh Thakkar, Quentin Cappart, David Vazquez, Nicolas Chapados, Alexandre Lacoste |
| **Venue** | ICML 2024 (conference) |
| **DOI** | `10.48550/arXiv.2403.07718` |
| **URL** | https://arxiv.org/abs/2403.07718 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-workarena`](../../meta/categories/benchmark-workarena/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2403.07718/summary.md) |

WorkArena introduces a remote-hosted benchmark of 33 enterprise-grade web tasks built on the
ServiceNow platform, accompanied by BrowserGym — a reusable Python environment for web-agent
evaluation. The motivation is that prior web-agent benchmarks (MiniWoB, WebShop) lack the
complexity of modern enterprise software, where agents must navigate content management
systems, intricate forms, custom layouts, and modal popups.

Methodologically, the paper instantiates 33 task families with 19,912 unique parameterized
instances, evaluates them via BrowserGym's standardized action and observation API, and grades
success by inspecting the resulting database state. Evaluation is reported as `pass@1`, with
the state-of-the-art proprietary model (GPT-4) and the strongest open-source model
(Llama3-70B) as the two anchor points.

The headline finding is a **24.8 absolute** gap between GPT-4 (**42.7%**) and
Llama3-70B-instruct (**17.9%**), demonstrating that current open-source agents lag
substantially on enterprise workflows. Even the best result leaves a considerable distance to
full task automation.

For the granularity-aware hierarchical agents project, WorkArena is the atomic layer
WorkArena++ composes. The project should reuse BrowserGym for compatibility, treat WorkArena
tasks as sanity-check material rather than primary evaluation, and prefer GPT-4-class models
for the Phase 2 baseline. The open-vs-closed-source gap is large enough that mixing model
classes in the composite benchmark would conflate model effects with prompt effects — a hazard
the planning step must address.

</details>

<details>
<summary>📝 <strong>FrontierMath: A Benchmark for Evaluating Advanced Mathematical
Reasoning in AI</strong> — Glazer et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2411.04872` |
| **Authors** | Elliot Glazer, Ege Erdil, Tamay Besiroglu, Diego Chicharro, Evan Chen, Alex Gunning, Caroline Falkman Olsson, Jean-Stanislas Denain, Anson Ho, Emily de Oliveira Santos, Olli Järviniemi, Matthew Barnett, Robert Sandler, Matej Vrzala, Jaime Sevilla, Qiuyu Ren, Elizabeth Pratt, Lionel Levine, Grant Barkley, Natalie Stewart, Bogdan Grechuk, Tetiana Grechuk, Shreepranav Varma Enugandla, Mark Wildon |
| **Venue** | arXiv preprint (preprint) |
| **DOI** | `10.48550/arXiv.2411.04872` |
| **URL** | https://arxiv.org/abs/2411.04872 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2411.04872/summary.md) |

The paper introduces FrontierMath, a research-mathematician-grade math reasoning benchmark
designed to evaluate frontier LLMs on problems that require hours to days of human expert
effort. The motivation is the saturation of prior math benchmarks (GSM8K, MATH) by SOTA models
and the contamination risk of using publicly available problems for evaluation.

The benchmark is built by commissioning hundreds of original, unpublished problems from expert
mathematicians, with programmatic answer-checking that scales to repeated automated runs.
Problems span number theory, real analysis, algebraic geometry, and category theory;
difficulty tiers cover undergraduate through research level. Endorsements from Fields
Medalists (Tao, Gowers, Borcherds) characterize the upper-tier problems as exceptionally
challenging.

The headline result is that current state-of-the-art models solve **under 2% of problems** at
release, revealing a large gap between AI and expert-mathematician performance. This is the
hardest published math benchmark to date.

For the granularity-aware hierarchical agents project, FrontierMath is the canonical
instantiation of the FrontierScience-Olympiad slot named in `project/description.md`. The <2%
baseline means the benchmark contributes mainly to the failure tail of the composite Phase 2
benchmark, and any per-condition (scope-aware vs. scope-unaware) effect must be measured
against a near-zero floor — which makes per-source stratification mandatory. Access via Epoch
AI's evaluation pipeline is a known operational risk for the t0003 download-dataset task.

</details>

<details>
<summary>🏤 <strong>SWE-bench: Can Language Models Resolve Real-World GitHub
Issues?</strong> — Jimenez et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2310.06770` |
| **Authors** | Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan |
| **Venue** | ICLR 2024 (oral) (conference) |
| **DOI** | `10.48550/arXiv.2310.06770` |
| **URL** | https://arxiv.org/abs/2310.06770 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-swebench`](../../meta/categories/benchmark-swebench/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2310.06770/summary.md) |

SWE-bench introduces a real-world software-engineering evaluation framework where 2,294
problems are sourced from genuine GitHub issues in 12 popular Python repositories. The
motivation is that prior code-generation benchmarks (HumanEval, MBPP) test isolated
function-level capability and saturate quickly with frontier models, while real software
engineering requires multi-file coordination, long codebase context, and resolution of issues
whose correct fix is judged by existing test suites.

Methodologically, each problem provides the full repository state at the issue's commit, the
issue text, and the held-out gold patch from the merged PR. Models generate a patch; success
is measured by running the test suite (including tests added in the resolving PR) inside a
Docker-isolated environment. The original paper evaluates Claude 2, GPT-4, and a fine-tuned
SWE-Llama, with the best baseline (Claude 2) resolving only **1.96%** of issues.

Since the original paper, the benchmark has spawned three notable subsets — SWE-bench Verified
(500 instances, human-validated by OpenAI), SWE-bench Lite (300 instances), and SWE-bench
Multimodal. Modern models score far above the original baseline on Verified: Claude Mythos
Preview at **93.9%** (April 2026), illustrating how fast the field has moved.

For the granularity-aware hierarchical agents project, SWE-bench Verified is the canonical
atomic-execution slot in the four-source composite. The project should adopt the Verified
subset (500 instances) for Phase 2 evaluation, support multi-file edits in the scope-aware (A)
condition's ATOMIC prompt, and stratify metrics per source benchmark — the >90% achievable
baseline on Verified would otherwise drown out FrontierMath's <2% baseline.

</details>

<details>
<summary>🏤 <strong>Trust or Escalate: LLM Judges with Provable Guarantees for Human
Agreement</strong> — Jung et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2407.18370` |
| **Authors** | Jaehun Jung, Faeze Brahman, Yejin Choi |
| **Venue** | ICLR 2025 (conference) |
| **DOI** | `10.48550/arXiv.2407.18370` |
| **URL** | https://arxiv.org/abs/2407.18370 |
| **Date added** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2407.18370/summary.md) |

Jung, Brahman, and Choi address a central reliability gap in LLM-as-judge evaluation: when
used at scale to grade pairs of model generations, even GPT-4-class judges have no provable
bound on their agreement with humans, yet downstream leaderboards and benchmarks treat their
verdicts as ground truth. The authors reframe evaluation as a **selective classification with
risk control** problem, deriving a fixed-sequence multiple-testing procedure that calibrates a
confidence threshold lambda on a small human-labeled calibration set and yields an exact
binomial upper bound on selective disagreement risk.

Methodologically, the paper contributes three components. **Selective evaluation** provides
the formal P(agreement | non-abstention) >= 1 - alpha guarantee; **Simulated Annotators**
produces high-quality unsupervised confidence estimates by prompting the judge with diverse
few-shot annotator personas and aggregating cross-simulation agreement; and **Cascaded
Selective Evaluation** chains weak-to-strong judges so that easy instances are decided cheaply
and only hard instances escalate, with the risk-control proof composing across cascade stages.

Empirically, on TL;DR, ChatArena, and Auto-J, the cascade achieves 90%+ guarantee success rate
at target agreement levels (0.85, 0.9) where GPT-4 alone has 0% guarantee success rate.
Coverage remains in the 55-65% range, but the routing concentrates GPT-4 calls on the hardest
17-44% of instances, cutting evaluation cost by 78-87% versus a GPT-4-only baseline. Simulated
Annotators roughly halves ECE for GPT-4 (0.217 to 0.095 on AlpacaEval) and improves both ECE
and accuracy for Mistral-7B (ECE 0.374 to 0.075). The abstention policy correlates with
human-perceived subjectivity (IAA 0.815 abstained vs. 0.902 evaluated) rather than shallow
features.

For this project on hierarchical agents and judges, the paper is highly load-bearing. It
supplies (i) a formal abstention/escalation primitive directly applicable to agent-as-judge
evaluation of multi-step trajectories, (ii) Simulated Annotators as a strong, cheap baseline
confidence measure to compare any new uncertainty methods against, and (iii) a worked-out
cost-vs-coverage trade-off showing that mixed cascades can deliver higher empirical
reliability than monolithic GPT-4 judging at a fraction of the API cost. Adopting calibrated
selective evaluation should be a default for any judge-driven metric we report.

</details>

<details>
<summary>🏤 <strong>Embodied Agent Interface: Benchmarking LLMs for Embodied Decision
Making</strong> — Li et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2410.07166` |
| **Authors** | Manling Li, Shiyu Zhao, Qineng Wang, Kangrui Wang, Yu Zhou, Sanjana Srivastava, Cem Gokmen, Tony Lee, Li Erran Li, Ruohan Zhang, Weiyu Liu, Percy Liang, Li Fei-Fei, Jiayuan Mao, Jiajun Wu |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2410.07166` |
| **URL** | https://arxiv.org/abs/2410.07166 |
| **Date added** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2410.07166/summary.md) |

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
<summary>🏤 <strong>AgentBoard: An Analytical Evaluation Board of Multi-turn LLM
Agents</strong> — Ma et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2401.13178` |
| **Authors** | Chang Ma, Junlei Zhang, Zhihao Zhu, Cheng Yang, Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng Kong, Junxian He |
| **Venue** | NeurIPS 2024 Datasets and Benchmarks (conference) |
| **DOI** | `10.48550/arXiv.2401.13178` |
| **URL** | https://arxiv.org/abs/2401.13178 |
| **Date added** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2401.13178/summary.md) |

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
<summary>📋 <strong>Introducing SWE-bench Verified</strong> — team, 2024</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_OpenAI2024_swe-bench-verified` |
| **Authors** | OpenAI Preparedness team |
| **Venue** | OpenAI technical card (institutional, not peer-reviewed) (technical_report) |
| **DOI** | — |
| **URL** | https://openai.com/index/introducing-swe-bench-verified/ |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-swebench`](../../meta/categories/benchmark-swebench/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/no-doi_OpenAI2024_swe-bench-verified/summary.md) |

SWE-bench Verified is a 500-instance human-validated subset of SWE-bench produced by OpenAI's
Preparedness team in collaboration with the original SWE-bench authors. The motivation is that
the parent benchmark of 2,294 problems contains some items with ambiguous issue descriptions
or flaky tests, which add noise to capability measurements at the frontier.

Methodologically, 93 expert software engineers each reviewed candidate problems on three axes:
(a) clear instructions, (b) correct test patches, (c) reproducible environments. Three
independent reviewers per problem; only problems passing all three axes from all three
reviewers were included. The harness, Docker images, and resolve@1 scoring are identical to
the parent benchmark.

The headline outcome is that Verified has become the de facto standard subset for measuring
frontier autonomous-software-engineering capability in 2024-2026. Modern models score far
above the parent benchmark's 1.96% Claude 2 baseline — Claude Mythos Preview leads at
**93.9%** (April 2026). OpenAI's own April 2026 commentary noted that this saturation may
limit Verified's usefulness as a frontier-capability measurement going forward.

For the granularity-aware hierarchical agents project, SWE-bench Verified is the canonical
atomic-execution slot in the Phase 2 composite benchmark. Its 500-instance size is tractable
for multiple-condition evaluation, the human validation removes benchmark noise, and
stratified reporting is essential because Verified's >90%-achievable ceiling would otherwise
drown out FrontierMath's <2% baseline. The project should plan a fallback to SWE-bench
Multimodal or SWE-bench Pro if Verified saturates further before Phase 2 completes.

</details>

<details>
<summary>🏤 <strong>Can Graph Learning Improve Planning in LLM-based Agents?</strong>
— Wu et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2405.19119` |
| **Authors** | Xixi Wu, Yifei Shen, Caihua Shan, Kaitao Song, Siwei Wang, Bohang Zhang, Jiarui Feng, Hong Cheng, Wei Chen, Yun Xiong, Dongsheng Li |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2405.19119` |
| **URL** | https://arxiv.org/abs/2405.19119 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.19119/summary.md) |

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
<summary>🏤 <strong>Can LLMs Express Their Uncertainty? An Empirical Evaluation of
Confidence Elicitation in LLMs</strong> — Xiong et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2306.13063` |
| **Authors** | Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, Bryan Hooi |
| **Venue** | ICLR 2024 (conference) |
| **DOI** | `10.48550/arXiv.2306.13063` |
| **URL** | https://arxiv.org/abs/2306.13063 |
| **Date added** | 2026-04-29 |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md) |

Xiong et al. address the calibration gap in modern LLMs: verbalized confidence is
systematically higher than actual accuracy, making it an unreliable signal for any system that
needs to abstain or escalate based on uncertainty. The motivation is that previous calibration
methods relied on white-box access to internal logits or model fine-tuning, neither of which
is available for closed-source commercial APIs.

Methodologically, the paper proposes a three-component black-box framework: prompting strategy
(vanilla, human-inspired, CoT, self-probing) × sampling method (single, multiple temperature,
multiple prompts) × aggregation technique (mean, majority vote, self-consistency). The
cross-product is benchmarked on five datasets across reasoning, math, code, factual recall,
and ethics, using five widely-used LLMs (GPT-4, GPT-3.5, LLaMA 2 Chat at three sizes).

The headline findings are (a) LLMs are systematically overconfident when verbalizing
confidence, (b) self-consistency aggregation beats single-sample confidence by **+2 to +8 ECE
points**, (c) larger models calibrate better, (d) human-inspired prompting ("low / medium /
high with justification") outperforms numeric confidence, (e) CoT confidence sometimes worsens
calibration counterintuitively.

For the granularity-aware hierarchical agents project, this paper is the canonical calibration
reference for Metric 2 (overconfident error rate). The project should adopt verbalized
confidence + 3-sample self-consistency aggregation as its operational definition, define
overconfident error as `incorrect AND high_confidence`, and report bucketed ECE plots
alongside single-number ECE. The human-inspired prompt is recommended for the scope-aware (A)
condition's confidence elicitation.

</details>

<details>
<summary>📝 <strong>tau-bench: A Benchmark for Tool-Agent-User Interaction in
Real-World Domains</strong> — Yao et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2406.12045` |
| **Authors** | Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan |
| **Venue** | arXiv preprint (preprint) |
| **DOI** | `10.48550/arXiv.2406.12045` |
| **URL** | https://arxiv.org/abs/2406.12045 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-taubench`](../../meta/categories/benchmark-taubench/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2406.12045/summary.md) |

tau-bench introduces a tool-agent-user interaction benchmark in two simulated customer-service
domains (retail and airline). The motivation is that prior tool-use benchmarks fail to test
two critical capabilities for production agents: dynamic interaction with a human user
(simulated here by another LLM) and adherence to domain-specific policy documents that
constrain allowable actions.

Methodologically, each task pairs a user-goal database state, an LLM-roleplayed user persona,
and a policy document. The agent conducts a multi-turn conversation, calls tools as needed,
and attempts to reach the goal state without policy violations. Evaluation compares the final
database state with the annotated goal. The novel pass^k metric runs `k` independent rollouts
and measures the fraction of tasks where every rollout succeeds — exposing inconsistency that
pass@1 hides.

The headline finding is that even state-of-the-art models (GPT-4o) achieve **under 50%
pass@1** and **pass^8 below 25% in retail**, indicating that current frontier agents are both
moderately-capable and substantially unreliable. The gap between pass@1 and pass^8 is the core
diagnostic.

For the granularity-aware hierarchical agents project, tau-bench is the canonical
request-vs-act benchmark — most of its failures stem from agents that proceed without
sufficient information rather than asking the simulated user. This makes tau-bench the primary
test bed for Metric 3. The project should also adopt the pass^k metric as a project-wide
reliability signal, especially in the Phase 4 paper-ready report where overall claims about
scope-conditioning gains must be robust to single-rollout luck.

</details>

<details>
<summary>🏤 <strong>ArCHer: Training Language Model Agents via Hierarchical
Multi-Turn RL</strong> — Zhou et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2402.19446` |
| **Authors** | Yifei Zhou, Andrea Zanette, Jiayi Pan, Sergey Levine, Aviral Kumar |
| **Venue** | ICML 2024 (conference) |
| **DOI** | `10.48550/arXiv.2402.19446` |
| **URL** | https://arxiv.org/abs/2402.19446 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.19446/summary.md) |

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
<summary>🏤 <strong>Language Agent Tree Search Unifies Reasoning, Acting, and
Planning in Language Models</strong> — Zhou et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2310.04406` |
| **Authors** | Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, Yu-Xiong Wang |
| **Venue** | ICML 2024 (conference) |
| **DOI** | `10.48550/arXiv.2310.04406` |
| **URL** | https://arxiv.org/abs/2310.04406 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2310.04406/summary.md) |

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
<summary>🏤 <strong>SELF-DISCOVER: Large Language Models Self-Compose Reasoning
Structures</strong> — Zhou et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2402.03620` |
| **Authors** | Pei Zhou, Jay Pujara, Xiang Ren, Xinyun Chen, Heng-Tze Cheng, Quoc V. Le, Ed H. Chi, Denny Zhou, Swaroop Mishra, Huaixiu Steven Zheng |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2402.03620` |
| **URL** | https://arxiv.org/abs/2402.03620 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.03620/summary.md) |

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

## Tasks (2)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |
| 0017 | [Literature: Hierarchical Agents and LLM-as-Judge](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) | completed | 2026-05-01 01:40 |

## Answers (2)

<details>
<summary><strong>Which RQ1 execution path do we follow under the permanent
no-Anthropic constraint: (a) existing-results-only verdict, (b) local /
open-weight rerun, (c) alternative paid provider, or (d) project-level
underpowered / provider-blocked stop?</strong></summary>

**Confidence**: high | **Date**: 2026-05-03 | **Full answer**:
[`no-anthropic-rq1-path-a`](../../tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/)

Option (a), the existing-results-only verdict, is the right path. The t0031 re-derivation
already yields the formal RQ1 conclusion at $0 with arm-labelling comparability with t0027 /
t0028 preserved by construction: 12 / 130 = 9.23% discordance, 6 arm-A wins and 6 arm-B wins,
two-sided exact-binomial McNemar p = 1.0000, with a SWE-bench arm-B advantage and a
FrontierScience arm-A advantage that cancel in aggregate. Options (b) and (c) replace the
policy under each arm label and turn any rerun into a verdict on a new experiment, while
option (d) forecloses the verdict that (a) can deliver immediately.

</details>

<details>
<summary><strong>Does the v2 schema retain a 30+ pp accept-rate delta over v1 under
a substantive judge and under a sonnet judge, or is the +57 pp t0014
headline an artefact of haiku judge anchoring?</strong></summary>

**Confidence**: low | **Date**: 2026-05-01 | **Full answer**:
[`does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges`](../../tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/)

The evidence is mixed. Under substantive-sonnet the schema-only delta is +24.6 pp and under
model-rotated-sonnet it is +37.3 pp, vs the t0014 baseline of +58.0 pp. The +57 pp headline
does not cleanly survive a stronger judge, but neither does it collapse below +30 pp on both
configurations; the answer depends on which sonnet judge configuration is treated as
canonical.

</details>

## Suggestions (49 open, 10 closed)

<details>
<summary>🧪 <strong>Give matched_mismatch a structurally distinct adversarial
behavior, not just a v3 delegation</strong> (S-0027-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-03 | **Source**:
[t0027_phase2_5_abc_rerun_with_fixed_b_and_c](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/)

matched_mismatch_v2 now delegates to plan_and_solve_v3 instead of A's scope_aware_react (the
structural fix this task implemented), but C and B agree on 125 of 130 paired outcomes
(discordant 4/5, McNemar p=1.0). C is effectively B-with-a-perturbed-strategy-label — the
adversarial signal is too weak to move the success rate. Redesign the wrapper to inject a
meaningfully different scaffold over v3: either a self-consistency vote across 3 sampled
plans, a chain-of-thought decomposition over the plan steps, or an explicit adversarial
critique loop before the action stage. Re-run B vs C on the same paired set to test whether a
stronger structural difference produces a discordance pattern that can move McNemar.

</details>

<details>
<summary>🧪 <strong>Ablate the planner: run plan_and_solve_v3 with an empty/identity
plan to isolate planner contribution</strong> (S-0027-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-03 | **Source**:
[t0027_phase2_5_abc_rerun_with_fixed_b_and_c](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/)

RQ1 came back as A=B at 4.62% on the 130-paired set, which is consistent with two competing
hypotheses: (1) the plan-and-solve scaffold adds zero value over scope_aware_react on this
dataset blend, or (2) the planner prompt is actively harmful and is being rescued by the
bounded recovery chain. Run a B-prime variant that uses plan_and_solve_v3's
parse/recovery/action machinery but replaces the planner output with a single identity step
('execute the requested task'), then compare B-prime vs B vs A on the same 130-paired set. If
B-prime ≈ B ≈ A, the planner is neutral; if B-prime ≈ A but B > A, the planner is helpful; if
B-prime > B ≈ A, the planner is actively harmful.

</details>

<details>
<summary>🔧 <strong>Instrument recovery_path unconditionally and audit the ~30
'unknown' trajectories per variant</strong> (S-0027-04)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-05-03 | **Source**:
[t0027_phase2_5_abc_rerun_with_fixed_b_and_c](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/)

Recovery-path telemetry is incomplete: B has 75 clean / 14 reprompt / 11 json_fallback / 1
all_failed and 29 'unknown', and C has 70 / 18 / 7 / 2 and 33 'unknown'. The 'unknown' bucket
is an instrumentation gap (the recovery_path field is not unconditionally written), not a
parser failure (raised_malformed_plan_error is 0/130 for both). Patch plan_and_solve_v3 to
emit recovery_path on every trajectory and re-run a small replay over the existing trajectory
artifacts to backfill the field for completed runs. Report the corrected distribution and
check whether the 29/33 currently-unknown trajectories are dominated by the clean path (most
likely) or by silent fallbacks.

</details>

<details>
<summary>📊 <strong>Build a discordance-rich paired sample to gain power for RQ1
and RQ5</strong> (S-0027-05)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-03 | **Source**:
[t0027_phase2_5_abc_rerun_with_fixed_b_and_c](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/)

On the current 130-paired set, RQ1 has only 6 discordant pairs (3 A-only + 3 B-only) and RQ5
has only 5 (1 B-only + 4 C-only) — McNemar power is at the floor by construction. Aggregate
the per-instance success bits from t0022 (A vs B), t0023 (sonnet swebench), t0026 (full
A/B/C), and now t0027 to build a discordance-rich paired set: select 130 instances where the
two variants disagreed in at least one prior run. Re-run A vs B and B vs C on that set under
claude-sonnet-4-6 and report whether the McNemar p-values move off symmetric. This decouples
'no detectable effect' from 'underpowered test' for the next iteration.

</details>

<details>
<summary>📚 <strong>Promote bounded plan-parse recovery into every other scaffold
in the library</strong> (S-0027-06)</summary>

**Kind**: library | **Priority**: low | **Date**: 2026-05-03 | **Source**:
[t0027_phase2_5_abc_rerun_with_fixed_b_and_c](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/)

plan_and_solve_v3's 3-attempt recovery chain (clean → reprompt → JSON-mode → degenerate plan)
eliminated parser failures (12% in t0026 → 0% in t0027) without measurable cost (~$10 for 130
instances). The same parse-failure path exists in scope_aware_react (multi-tool JSON), in
scratchpad-style ablations, and in any future scaffold that asks the model for structured
intermediate output. Refactor the recovery chain into a shared utility under assets/library/
and adopt it in every scaffold that does structured-output parsing, then verify on a small
sweep that no new scaffold emits raised_malformed_plan_error.

</details>

<details>
<summary>📊 <strong>Close t0029 / t0030 via correction as no-longer-actionable under
no-Anthropic constraint</strong> (S-0032-01)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-03 | **Source**:
[t0032_no_anthropic_rq1_path_decision](../../tasks/t0032_no_anthropic_rq1_path_decision/)

Now that t0032 locks in option (a) — existing-results-only verdict — as the recommended RQ1
execution path, t0029 (rerun B+C at the 218-pair cap) and t0030 (B-only matched-mismatch
follow-up) are no longer actionable. Both rely on Sonnet via the Anthropic API, which the
project memory marks as permanently unavailable. Emit a downstream correction task that flips
both task statuses to 'cancelled' with a rationale referencing t0032's verdict and the
no-Anthropic constraint, so aggregators stop surfacing them as outstanding work.

</details>

<details>
<summary>🧪 <strong>Spend released RQ1 budget on cost-tracker fix, bootstrap CIs, and
RQ4 stratification follow-ups</strong> (S-0032-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-03 | **Source**:
[t0032_no_anthropic_rq1_path_decision](../../tasks/t0032_no_anthropic_rq1_path_decision/)

With option (a) locked in, the ~$26.54 reserved for the t0029 218-pair rerun is released.
Reinvest it in three cost-free or near-zero analyses directly motivated by t0032's
creative-thinking pass: (1) implement S-0031-03 to fix per-instance cost tracking so future
paired runs report Sonnet cost reliably; (2) compute 95% bootstrap confidence intervals around
the per-stratum McNemar cells from t0031 (SWE-bench 6/0, FrontierScience 0/5, tau-bench 1 of
84) to harden the conclusion that arms differ qualitatively by benchmark; (3) re-stratify the
existing 130-pair t0031 sample by trace length / tool-call count for the RQ4
efficiency-vs-accuracy story without any new paid API call.

</details>

<details>
<summary>📊 <strong>Qualitative trajectory typology of the 12 t0031 discordant
pairs</strong> (S-0032-03)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-03 | **Source**:
[t0032_no_anthropic_rq1_path_decision](../../tasks/t0032_no_anthropic_rq1_path_decision/)

Build a small qualitative typology of the 12 discordant paired instances from t0031 (6 a_only
+ 6 b_only) to characterise how plan-and-solve_v3 (arm A) and matched_mismatch_v2 (arm B)
diverge on the same instance. Tag each discordant pair by failure mode (planning error, tool
misuse, retrieval gap, formatting, etc.) and benchmark stratum. The output is one short
markdown asset; the task is zero-cost (reads existing trajectories from t0026/t0027) and feeds
back into RQ1 reporting and future agent-design suggestions.

</details>

<details>
<summary>🧪 <strong>Reframe the matched-mismatch wrapper so C is structurally
distinct from A</strong> (S-0026-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-02 | **Source**:
[t0026_phase2_abc_runtime_n147_for_rq1_rq5](../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/)

Variant C beat B (paired McNemar p = 0.019) but only because the 'adversarial' wrapper
delegates to scope_aware_react with a perturbed strategy label, making C structurally
A-with-noise rather than B-with-extra-degradation. Redesign the matched-mismatch interface so
the adversarial variant operates on top of B's plan-and-solve scaffold, not A's, then re-run
the B vs C pair on the same paired set to test whether the inversion survives.

</details>

<details>
<summary>📊 <strong>Wire a real Tau-bench tool registry to escape the harness
floor</strong> (S-0026-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0026_phase2_abc_runtime_n147_for_rq1_rq5](../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/)

Tau-bench numbers in this sweep are a harness floor, not a benchmark score: A=0.0%, B=2.3%,
C=10.3% on a stub python_exec only. Port the published Tau-bench retail/airline tool stack (or
a minimal viable subset) into the harness and rerun the A/B/C grid on the Tau-bench subset
(n=87). The Tau-bench leg of the comparison currently dominates the absolute-rate gap with
literature.

</details>

<details>
<summary>🧪 <strong>Run the same A/B/C grid on Opus to test whether scaffold rankings
are model-invariant</strong> (S-0026-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0026_phase2_abc_runtime_n147_for_rq1_rq5](../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/)

All current results are Sonnet-only. The C > B inversion may flip on a stronger model where
B's plan parser sees fewer malformed plans and where C's longer reasoning chains finish more
often. Repeat the 130-instance paired sweep with claude-opus-4-7 as the model under test
(judges remain sonnet primary + opus inter-judge) and report whether mcnemar_p_a_vs_b and
mcnemar_p_b_vs_c keep the same sign.

</details>

<details>
<summary>🔧 <strong>Recover the 17 missing instances per variant for a full N=147
paired set</strong> (S-0026-06)</summary>

**Kind**: technique | **Priority**: low | **Date**: 2026-05-02 | **Source**:
[t0026_phase2_abc_runtime_n147_for_rq1_rq5](../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/)

The resumable-checkpoint path filtered 17 instances per variant from a corrupted earlier run,
dropping the paired sample from N=147 to N=130. Add a 'force-rerun' flag to full_runner.py
that re-emits trajectories for those ids and rerun A/B/C on the missing 17. The McNemar tests
are statistically valid as-is, but the absolute success rates would be unbiased on the full
N=147.

</details>

<details>
<summary>🧪 <strong>Add tool use (search, code execution) to the smoke harness for
FrontierScience-Olympiad</strong> (S-0012-03)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0012_phase2_abc_smoke_frontierscience](../../tasks/t0012_phase2_abc_smoke_frontierscience/)

The smoke ran with calculator+finish only. FrontierScience-Olympiad requires multi-step
numerical computation, retrieval, and code execution for most problems. Adding a Python code
execution tool and a retrieval tool would lift accuracy above the current floor and make
A-vs-B-vs-C differences observable even on haiku. Cost per row would increase by ~2-5x but
confirmatory N would decrease proportionally.

</details>

<details>
<summary>🧪 <strong>Multi-provider replication: run Phase 2 harness with GPT-4o and
Gemini 1.5 Pro</strong> (S-0012-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0012_phase2_abc_smoke_frontierscience](../../tasks/t0012_phase2_abc_smoke_frontierscience/)

The smoke used only claude-haiku-4-5. Replicating on GPT-4o and Gemini 1.5 Pro (both now
available via project API keys) would test whether the granularity conditioning effect is
model-specific or generalizes across providers. The harness's model_call.py abstraction layer
makes this a configuration change rather than a code change. Defer until the confirmatory N
result is available from S-0012-02 to avoid spending budget before the primary hypothesis is
tested.

</details>

<details>
<summary>📊 <strong>Adopt Trust-or-Escalate selective evaluation for the multi-judge
agreement study</strong> (S-0017-01)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0017_literature_hierarchical_agents_and_judges](../../tasks/t0017_literature_hierarchical_agents_and_judges/)

S-0009-03 calls for a multi-judge agreement study; Jung2024 ("Trust or Escalate", ICLR 2025)
provides the right primitive. Implement a selective-judging pipeline with two ingredients: (1)
Simulated Annotators on top of the project's existing judge LLM to produce ensemble-based
confidence scores, and (2) a calibrated abstention threshold using fixed-sequence testing
(Bauer 1991, Bates et al. 2021) so the pipeline ships with a finite-sample, distribution-free
guarantee on human-judge agreement. Empirically Jung2024 shows that 75% of pairwise judging on
ChatArena can be delegated to Mistral-7B/GPT-3.5 while preserving an 80% human-agreement floor
that GPT-4 alone never reaches, so this is also a cost-reduction path for any large-scale
annotation rerun. Deliverable: a small library that wraps the existing judge call with
confidence + abstain semantics, exposed to t0009-style annotation tasks.

</details>

<details>
<summary>🔧 <strong>Use SELF-DISCOVER reasoning scaffolds as the scope-aware (A)
condition prompt template</strong> (S-0017-03)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0017_literature_hierarchical_agents_and_judges](../../tasks/t0017_literature_hierarchical_agents_and_judges/)

Zhou2024b (SELF-DISCOVER, NeurIPS 2024) shows that a task-conditioned reasoning structure --
selected from atomic reasoning modules and composed once per task type, then re-used across
instances -- transfers across model families and outperforms CoT-Self-Consistency at 10-40x
lower inference cost. The IMPLEMENT step (explicit JSON key-value scaffold) is the largest
ablation contributor. This is a near-zero-cost upgrade to our scope-aware (A) condition
prompt: produce one SELF-DISCOVER structure per benchmark family (FrontierScience-Olympiad,
SWE-bench Verified, tau-bench, WorkArena++), then re-use it across all rows of that family.
Predicts a measurable improvement on RQ1/RQ5 even without re-running annotation. Out of scope:
any retraining; this is purely a prompting change.

</details>

<details>
<summary>🧪 <strong>Confirmatory v2 vs v1 schema sweep with fresh annotations and
a third sonnet judge</strong> (S-0019-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0019_v2_judge_calibration_sonnet](../../tasks/t0019_v2_judge_calibration_sonnet/)

Run a confirmatory experiment that re-annotates a fresh n>=80 row pool (not the t0014 pool)
under the v1 and v2 schemas with claude-sonnet-4-6 as annotator, then judges with three
independent sonnet configurations: substantive critic, model-rotated original prompt, and a
new criterion-decomposed rubric judge. The current task left the +24.6 / +37.3 pp delta band
unsettled because the two judge configurations disagreed on the +30 pp threshold and the pool
overlapped with t0014. A fresh-pool replication at the planned n>=80 would tighten the
per-cell Wilson CIs from +/-24 pp to +/-11 pp, enough to either reset the headline below +30
pp or commit it above +45 pp.

</details>

<details>
<summary>📚 <strong>Provision a sonnet-quota Anthropic API key to drop per-call cost
~7x</strong> (S-0019-02)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0019_v2_judge_calibration_sonnet](../../tasks/t0019_v2_judge_calibration_sonnet/)

Acquire an Anthropic API key with claude-sonnet-4-6 quota and switch JUDGE_TRANSPORT back from
the claude CLI subprocess to the Anthropic SDK. The current OAuth-issued key in this
environment lacks sonnet quota, forcing the CLI fallback at ~$0.18/call (cache-creation
overhead) instead of the ~$0.024/call SDK + cache-hit projection. Provisioning a
sonnet-capable key would let S-0019-01's confirmatory sweep run within the original $5 budget
envelope and unblock larger-n experiments without per-task cap raises. This is a project-level
service request, not a research experiment.

</details>

<details>
<summary>📊 <strong>Substantive critic vs original prompt: 50-row prompt-only
ablation at fixed model</strong> (S-0019-03)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0019_v2_judge_calibration_sonnet](../../tasks/t0019_v2_judge_calibration_sonnet/)

Run a focused n=50 ablation that holds the judge model fixed at claude-sonnet-4-6 and varies
only the system prompt between the substantive critic (with simulate-execution instruction)
and the original t0014 prompt. The current task found a Cohen's kappa of 0.626 between the two
prompts on the same model, with one row (v2-haiku-0007) where the substantive prompt caught a
dimensional-analysis error the original prompt missed and two rows (v1-sonnet-0002,
v1-sonnet-0004) where the substantive prompt accepted structural-but-executable trees the
original rejected. A larger ablation would quantify how often each prompt mode wins, which
would inform whether the substantive critic should become the production judge or stay as a
stricter audit.

</details>

<details>
<summary>🧪 <strong>Cross-vendor judge: replicate the schema-only delta with GPT-4
and Gemini judges</strong> (S-0019-04)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0019_v2_judge_calibration_sonnet](../../tasks/t0019_v2_judge_calibration_sonnet/)

Test the family-bias hypothesis at the judge stage by re-judging the same 55-row pool under
GPT-4o and Gemini-2.5 with the same substantive critic prompt, and comparing the schema-only
delta to the +24.6 / +37.3 pp Anthropic numbers from this task. Xiong2024 reports
within-family acceptance bonuses of 5-10 pp; if the cross-vendor schema-only delta lands close
to the substantive-sonnet +24.6 pp, the v2-sonnet familial bias hypothesis (kappa=1.0 on the
v2-sonnet cell) gains support; if it lands close to +37 pp, prompt strictness dominates over
model family.

</details>

<details>
<summary>📊 <strong>Sonnet judge rerun on the v2-tree-truncated condition to confirm
schema effect is not haiku-specific</strong> (S-0020-02)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0020_v2_truncation_vs_schema_ablation](../../tasks/t0020_v2_truncation_vs_schema_ablation/)

All three conditions in t0020 use a haiku judge for fairness, but this means the result is
haiku-judge accept rates rather than ground-truth quality. A sonnet rerun on the
v2-tree-truncated annotations (existing 20 rows, no new annotator calls) would confirm whether
the +57 pp pure-schema effect is robust to a stronger judge or whether it shrinks. t0014
already showed sonnet times out on some rows, so the rerun should set max_turns conservatively
and accept timeouts as null verdicts rather than retries. Estimated cost ~$3-5 sonnet judge.

</details>

<details>
<summary>📊 <strong>Cost-quality Pareto chart across t0009/t0014/t0020 to inform
downstream task budgets</strong> (S-0020-05)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0020_v2_truncation_vs_schema_ablation](../../tasks/t0020_v2_truncation_vs_schema_ablation/)

Three conditions now exist on the same 20-row pool: v1-flat-truncated (cheap, low quality),
v2-tree-truncated (cheap, high quality), v2-tree-full (expensive, slightly higher quality). A
Pareto chart with cost-per-row on the x-axis and accept rate on the y-axis would crisply
communicate that v2-tree-truncated is on the Pareto frontier and v2-tree-full is dominated by
it once the +5 pp gain is weighed against the ~2x cost. Useful as input to the t0022 ABC
harness budget planning.

</details>

<details>
<summary>🧪 <strong>Investigate the 31-decision scope-mismatched trajectory at larger
sample size</strong> (S-0021-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0021_plan_and_solve_v2_with_final_confidence](../../tasks/t0021_plan_and_solve_v2_with_final_confidence/)

The n=1 smoke for Condition C (matched-mismatch wrapping scope_unaware_planandsolve_v2) used
31 decisions on a single FrontierScience-Olympiad row, vs 8 for B and 1 for A. At n=1 this is
one observation, but it is a strong signal that the matched-mismatch wrapper plus
contradictory granularity guidance can trigger a planning loop in the v1 Plan-and-Solve agent.
In t0023's larger run, log per-row decision counts and check whether C's distribution is
heavy-tailed compared to B; if it is, design a follow-up to root-cause whether the loop comes
from the wrapper, the scope mismatch, or the v1 planner itself.

</details>

<details>
<summary>📊 <strong>Track final_confidence vs correctness calibration on the t0023
confirmatory run</strong> (S-0021-02)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0021_plan_and_solve_v2_with_final_confidence](../../tasks/t0021_plan_and_solve_v2_with_final_confidence/)

The v2 library now emits final_confidence on every trajectory across all three conditions,
which unblocks paired calibration analysis. On t0023 (n>=157, sonnet), report per-condition
reliability diagrams (binned confidence vs empirical accuracy), Brier scores, and ECE in
addition to overconfident_error_rate. This will reveal whether the [0,1] field is actually
informative for the model or whether it collapses to a flat distribution near 0.7-0.9 (the
Xiong2024 haiku risk), and whether condition-vs-condition Metric 2 deltas reflect calibration
shifts or just accuracy shifts.

</details>

<details>
<summary>📚 <strong>Add a JSON-mode fallback path to the confidence elicitation if
larger runs hit the 20% parse-failure gate</strong> (S-0021-03)</summary>

**Kind**: library | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0021_plan_and_solve_v2_with_final_confidence](../../tasks/t0021_plan_and_solve_v2_with_final_confidence/)

The smoke parse-failure rate on haiku is 0/3 on n=1 x 3, so the strict regex parser is fine
for haiku at this scale. However, if the t0023 sonnet run or any future larger run pushes the
parse-failure rate above the documented 20% gate (REQ-10), the library should fall back to
JSON-mode output (e.g., a tool-use call returning {confidence: 0.85}) instead of free-form
text. Implement this as an opt-in path so the existing two-call protocol stays the default and
the JSON fallback only activates when the model demonstrably cannot produce parseable output.
Keep the verbalized prompt as the canonical Xiong2024 §3.2 protocol.

</details>

<details>
<summary>📚 <strong>Tighten budget-guard wrapper to skip-write fallback responses
to disk cache</strong> (S-0022-01)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0022_abc_harness_progress_rate_and_error_taxonomy](../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/)

When the budget guard returns a deterministic fallback ("no" for progress rate, "ok" for error
taxonomy), the current wrapper still calls cache_put on the response. As a result the disk
cache for t0022 grew to 2592 entries, ~80% of which are fallback strings rather than real
judge responses. Add a flag to judge_cache.cache_put that lets the budget-guarded wrapper
skip-write fallback values; this keeps the cache useful for t0023 instead of polluting it.
Trivially small change in code/judge_cache.py and code/replay_t0012.py; covers a real risk for
the t0023 confirmatory ABC re-run.

</details>

<details>
<summary>📊 <strong>Tighten FrontierScience-Olympiad subgoal lists by hand on a
5-task pilot before t0023</strong> (S-0022-02)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0022_abc_harness_progress_rate_and_error_taxonomy](../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/)

Current FrontierScience-Olympiad subgoals are derived mechanically from SUBTASK lines in t0012
gold answers (mean 4.6 per environment). On the 89-row replay, 73 of 89 trajectories scored
0.0 progress rate, suggesting the subgoals may be too coarse to register intermediate
progress. Hand-review subgoals for 5 randomly chosen environments, refining them into 3-5
verifiable intermediate states each (e.g., "derived intermediate equation X", "identified
relevant principle Y"). If hand-tightening doubles the non-zero rate, roll the recipe out to
all 26 environments before t0023 ships. Cheap and high-leverage for t0023 signal quality.

</details>

<details>
<summary>📊 <strong>Add finer-grained SWE-bench subgoals at the line-range and
AST-node level</strong> (S-0022-03)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0022_abc_harness_progress_rate_and_error_taxonomy](../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/)

Current SWE-bench Verified Lite subgoals are file-level ("agent edit touches the same file as
a gold patch hunk"). This is a permissive subgoal that may not differentiate scope-aware from
scope-unaware agent behaviour as sharply as line-range or AST-node level subgoals would.
Implement a second subgoals JSON file with per-hunk line ranges parsed from the gold patch,
and a small AST-node helper that maps line ranges to the enclosing function/class. Compare
progress-rate distributions on the t0012 sample (or a fresh small SWE-bench eval) between the
two granularities. Useful Metric 1 calibration step independent of t0023.

</details>

<details>
<summary>📊 <strong>Spot-check Haiku judge calls against Sonnet on a 20-step
stratified sample</strong> (S-0022-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0022_abc_harness_progress_rate_and_error_taxonomy](../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/)

Both progress_rate and error_taxonomy judge calls default to claude-haiku-4-5 to keep t0023
cost bounded. Risk: haiku miscalibration could produce systematic bias on the error taxonomy
(e.g., over-classifying steps as "ok"). Build a small re-grading script that picks 20 steps
stratified by (condition, predicted label) and re-classifies them with claude-sonnet. Report
agreement rate per label. If overall agreement < 70% or any label has < 50% agreement,
escalate to sonnet for the headline t0023 numbers and document in t0023's Limitations.

</details>

<details>
<summary>🧪 <strong>Run t0023's confirmatory ABC re-run with N>=157 using
abc_harness_metrics</strong> (S-0022-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0022_abc_harness_progress_rate_and_error_taxonomy](../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/)

The whole purpose of t0022 is to make t0023's confirmatory N>=157 ABC re-run produce signal at
the floor where binary task success failed in t0012. Schedule t0023 to consume
abc_harness_metrics: import score_trajectory, log per-trajectory progress_rate and per-step
error labels into the existing harness output, and report progress-rate means and
error-distribution mixtures per ABC condition with bootstrap CIs. Reuse the cached judge
responses from t0022 to keep marginal cost low. This is the direct downstream consumer this
task was built for.

</details>

<details>
<summary>🧪 <strong>Phase 2 calibration-focused A/B with explicit confidence
elicitation (recommended Candidate 2)</strong> (S-0025-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0025_lit_survey_hierarchical_agents_and_judges_2024_2026](../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/)

Run a minimum-viable Phase 2 A vs B experiment on a 30-instance subset of the composite
benchmark, eliciting agent self-reported confidence at every action and using a sonnet rotated
judge plus programmatic graders to break the t0019 anchoring effect. Primary metrics:
normalized task success and overconfident-error-rate (incorrect actions taken with
self-reported confidence above a threshold). This is the cheapest design that produces RQ1 +
RQ2 evidence simultaneously and stays inside the ~$10-14 envelope of the remaining ~$23
budget.

</details>

<details>
<summary>📊 <strong>Adopt AgentBoard progress-rate as a secondary RQ1 metric
alongside binary task success</strong> (S-0025-02)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0025_lit_survey_hierarchical_agents_and_judges_2024_2026](../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/)

Ma2024 (AgentBoard) shows that pairs of models with identical binary success rates differ by
up to 5.7 progress-rate points (Llama2-13b vs Mistral-7b), revealing differences invisible in
success-only evaluation. Add progress-rate as Metric 1b for every Phase 2 A/B/C run so that
even runs that tie on success surface granularity-conditioning differences in mid-trajectory
behaviour.

</details>

<details>
<summary>🧪 <strong>Phase 2 three-arm A/B/C pilot at half scale to test the
strict-double-inequality form of RQ5</strong> (S-0025-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0025_lit_survey_hierarchical_agents_and_judges_2024_2026](../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/)

Wen2024 NTPO is the only paper that directly observes a mismatched-scope condition
underperforming both baselines, but it is in the RL fine-tuning regime, not prompting. To test
RQ5's strict double inequality (C < both A and B) under our prompting framing, run all three
arms on a half-scale (15-instance) subset of the composite benchmark, ~$15-20. Lower-priority
than S-0025-01 because RQ5 is a sub-hypothesis and the strict form is the most expensive to
falsify.

</details>

<details>
<summary>📊 <strong>Run a single-blind human review pass on the 115 v2 rows and
report human-vs-judge agreement (Cohen's kappa)</strong> (S-0009-03)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

v2 is judged only by a single LLM call per row. The dataset is 'LLM-judge-acceptable' but not
'human-validated'. To upgrade to v3, recruit 1-2 human annotators to review the same 23-row
stratified sample (or all 115 rows for higher precision) and emit acceptable/needs-revision
verdicts. Compute Cohen's kappa between human and the haiku judge to estimate how much of the
+58% v2-vs-v1 aggregate gain is real quality vs judge-LLM agreement-with-itself. Budget
estimate: 4-6 hours of human review time at $50/hour = $200-300.

</details>

<details>
<summary>📂 <strong>Expand the v2 dataset from 115 rows to >=200 rows by sampling
additional benchmark instances</strong> (S-0009-05)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

The Phase 1 success criterion is >=100 annotated tasks per condition; v2 is at 115 which is
just over the threshold. The downstream Phase 2 experiments need stratification by difficulty
AND by benchmark, which becomes statistically thin at 5-6 rows per stratum. Expand to >=200
rows by sampling 20-25 additional rows from each of the four benchmarks (especially the
smaller ones: SWE-bench Verified, tau-bench). Re-use v2_annotator.py at the same haiku-CLI
rate, ~$5-6 added cost. Inherits S-0005-01.

</details>

<details>
<summary>🧪 <strong>Rotate the judge model to test the haiku-vs-haiku familial bias
hypothesis on the model-only delta</strong> (S-0014-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-30 | **Source**:
[t0014_v2_annotator_sonnet_rerun](../../tasks/t0014_v2_annotator_sonnet_rerun/)

The model-only delta of -1 pp sits below Xiong2024's lower edge (0 pp). Xiong2024 documents
that judges trained on the same model family as the annotator show a small positive familial
bias (~5-10 pp). Our judge is held on haiku to keep apples-to-apples with t0009/t0005, which
means v2-haiku has a familial-agreement advantage over v2-sonnet. Re-judge the same 20-row
v2-sonnet sample and 23-row v2-haiku sample with claude-sonnet-4-6 as the judge instead of
haiku. If the model-only delta swings positive (e.g., +5-10 pp) under the sonnet judge, the
haiku-vs-haiku familial bias is masking a real sonnet annotator advantage. If it stays near
zero, sonnet really does provide no annotator-quality lift on this composite. Cost ~$2 with
sonnet judge on 43 rows.

</details>

<details>
<summary>🔧 <strong>Adopt a haiku-default annotation policy for Phase 2: model swap
is not justified</strong> (S-0014-04)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-30 | **Source**:
[t0014_v2_annotator_sonnet_rerun](../../tasks/t0014_v2_annotator_sonnet_rerun/)

Under the t0014 measurement, haiku and sonnet annotators produce statistically
indistinguishable accept rates under the v2 tree schema (90% sonnet vs 91% haiku, CIs overlap
completely). Sonnet annotation costs ~$0.20 per call vs haiku ~$0.02 per call (10x via Claude
Code CLI; 7-8x via direct API). For Phase 2 ABC/main-experiment annotation budgets in the
$50-200 range, the cost differential dominates: a 200-row sonnet annotation pass would cost
$40 vs $5 for haiku, with no measurable accept-rate benefit. Adopt haiku as the default
annotator unless and until S-0014-02 or S-0014-03 surfaces a real sonnet advantage masked by
judge bias.

</details>

<details>
<summary>📂 <strong>Replace Mind2Web/HumanEval proxy rows with native WorkArena++
and tau-bench data</strong> (S-0015-01)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0015_correct_proxy_benchmark_labels](../../tasks/t0015_correct_proxy_benchmark_labels/)

Variant a of S-0009-06 (now folded into this follow-up). The 26 m2w_* rows in the v2
hierarchical-annotation dataset are Mind2Web data used as a proxy for the gated WorkArena++
split, and the 26 he_* rows are HumanEval data used as a proxy for the gated tau-bench split.
t0015 corrected the labels but did not replace the underlying data. This task should (1)
obtain access to a real WorkArena++ split and a real tau-bench split (both currently gated;
expect a registration / agreement step that must be tracked as an intervention), (2)
re-annotate 26 + 26 rows under the v2 tree schema using the same haiku annotator and judge as
t0009 to keep variant b apples-to-apples, and (3) issue a corrections-overlay against
hierarchical-annotation-v2 that swaps the proxy rows for the native rows. Out of scope: any
change to the FrontierScience-Olympiad or SWE-bench Verified rows.

</details>

<details>
<summary>📊 <strong>Register pass^k as a project metric for reliability
reporting</strong> (S-0002-01)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0002_literature_survey_granularity_conditioning](../../tasks/t0002_literature_survey_granularity_conditioning/)

tau-bench [Yao2024] introduces pass^k, a metric that measures whether an agent succeeds across
k independent rollouts. The 25-percentage-point gap between pass@1 and pass^8 in retail
demonstrates that single-rollout pass@1 systematically overstates agent reliability. The
project should register a pass_at_k metric (with k=1, 8) under meta/metrics/ to complement
task_success_rate. This enables Phase 4 paper-ready claims to be robust to single-rollout
luck.

</details>

<details>
<summary>📚 <strong>Set up ServiceNow + BrowserGym harness shared by WorkArena and
WorkArena++</strong> (S-0002-03)</summary>

**Kind**: library | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0002_literature_survey_granularity_conditioning](../../tasks/t0002_literature_survey_granularity_conditioning/)

Both WorkArena [Drouin2024] and WorkArena++ [Boisvert2024] require a self-hosted ServiceNow
developer instance and the BrowserGym Python harness. This is a substantial infrastructure
task with credentials, container orchestration, and end-to-end smoke tests. Schedule it before
any task that needs WorkArena or WorkArena++ data so the harness is ready when Phase 1
annotation begins.

</details>

<details>
<summary>📊 <strong>Multi-judge disagreement study on hierarchical
annotation</strong> (S-0005-05)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

Run the same 12-row spot-check with two judge models (claude-haiku-4-5 + claude-sonnet-4-6)
and compute pairwise verdict agreement plus a confusion matrix. The v1 single-judge accept
rate of 33% may be miscalibrated; multi-judge agreement gives a more reliable quality
estimate. Estimated cost: ~$0.30 per run.

</details>

<details>
<summary>🧪 <strong>Use hierarchical-annotation-v1 to seed Phase 2 scope-conditioning
experiments</strong> (S-0005-06)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

The dataset asset is now ready for downstream consumption. Plan a baseline-evaluation task
that uses the 102 hierarchy-complete rows to compare scope-conditioned vs scope-unaware agent
prompts (B vs G/S/A from the project's research questions).

</details>

<details>
<summary>📚 <strong>Build benchmark-specific tool registries for the four roadmap
benchmarks</strong> (S-0006-01)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0006_scope_aware_react_library](../../tasks/t0006_scope_aware_react_library/)

scope_aware_react_v1 accepts an arbitrary tool_registry but ships none. Phase 2 needs
registries for FrontierScience-Olympiad (calculator, search, paper lookup), WorkArena++
(browser, form filler, table lookup), SWE-bench Verified (file read, file write, run tests,
git diff), and tau-bench (DB query, API call, customer-action stubs). Each should be its own
write-library task that imports scope_aware_react_v1 and registers a registry with consistent
naming conventions.

</details>

<details>
<summary>📚 <strong>Add an async ScopeAwareReactAgent variant for streaming and
parallel tool calls</strong> (S-0006-02)</summary>

**Kind**: library | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0006_scope_aware_react_library](../../tasks/t0006_scope_aware_react_library/)

The current agent is synchronous. Phase 2 experiments at scale will benefit from streaming
model output and from issuing multiple independent tool calls concurrently within a single
Thought block. Build async_scope_aware_react.py exposing AsyncScopeAwareReactAgent with an
async model_call signature and asyncio.gather over Action lists. Tests should use
AsyncScriptedModel mirroring the sync helper.

</details>

<details>
<summary>📊 <strong>Measure the missing-tag fallback rate against real LLMs</strong>
(S-0006-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0006_scope_aware_react_library](../../tasks/t0006_scope_aware_react_library/)

The library defaults to atomic when the model omits a granularity tag and emits a
tag_missing_defaulted_to_atomic warning observation. The deterministic tests cover the parser
path but the fallback rate against real LLMs (GPT-4o, Claude 3.7 Sonnet, Llama-3.1-70B) is
unknown. Build an evaluation task that runs each library at each granularity over N=20
problems per benchmark and reports the fallback rate alongside task success.

</details>

<details>
<summary>🧪 <strong>Phase 2 A-vs-B-vs-C evaluation harness</strong> (S-0007-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0007_scope_unaware_planandsolve_library](../../tasks/t0007_scope_unaware_planandsolve_library/)

Build the experiment harness that runs all three libraries (scope_aware_react_v1,
scope_unaware_planandsolve_v1, and the planned matched-mismatch library) on a fixed benchmark
slice with a single shared LLM provider, recording trajectory_records.jsonl per condition and
computing the registered metrics task_success_rate, avg_decisions_per_task, and
overconfident_error_rate per condition. The harness must depend on this library only via the
trajectory schema, never via internal helpers, to preserve isolation.

</details>

<details>
<summary>📊 <strong>Schema-parity dedup task between t0006 and t0007</strong>
(S-0007-03)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0007_scope_unaware_planandsolve_library](../../tasks/t0007_scope_unaware_planandsolve_library/)

After t0006 (scope_aware_react_v1) merges, run a small deduplication-style task that imports
both libraries' TRAJECTORY_RECORD_FIELDS tuples and asserts they are identical, plus a smoke
test that runs both libraries on the same toy problem and verifies the trajectory JSON shapes
round-trip through a single Pydantic loader. If they diverge, file a correction in the
later-merged task. This is the cheapest insurance against silent schema drift.

</details>

<details>
<summary>🧪 <strong>Add a uniform-random vs. adversarial vs. matched ablation to
t0012</strong> (S-0010-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0010_matched_mismatch_library](../../tasks/t0010_matched_mismatch_library/)

When t0012 runs the A-vs-B-vs-C harness, include three C-condition variants in addition to A
and B: matched_mismatch_v1 with mismatch_strategy='random' and seed=0, matched_mismatch_v1
with mismatch_strategy='adversarial', and a phase-randomised C control (random walk over the
v2 hierarchy with the correct tag). The three-way ablation decomposes the C-condition gap into
'phase order matters', 'any wrong tag matters', and 'most-distant wrong tag matters',
preventing the granularity-mismatch effect from being conflated with a step-order-mismatch
effect (see research_papers.md, Wang2023 and Zhou2022).

</details>

<details>
<summary>📊 <strong>Resolve the subtask-adversarial ambiguity with empirical
evidence</strong> (S-0010-03)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0010_matched_mismatch_library](../../tasks/t0010_matched_mismatch_library/)

ADVERSARIAL_MAP currently pins 'subtask -> atomic' because subtask is equidistant from global
and atomic. Run a small ablation in t0012 with both 'subtask -> atomic' and 'subtask ->
global' adversarial maps and report the per-step contribution. If the two choices differ
materially, document the chosen direction and the empirical justification in
matched_mismatch_v1's description.md. If they do not differ, lock the current choice and
remove the ambiguity note.

</details>
