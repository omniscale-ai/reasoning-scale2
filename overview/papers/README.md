# Papers (11)

11 papers across 3 year(s).

**Browse by view**: By category: [`agent-evaluation`](by-category/agent-evaluation.md),
[`benchmark-annotation`](by-category/benchmark-annotation.md),
[`benchmark-frontierscience`](by-category/benchmark-frontierscience.md),
[`benchmark-swebench`](by-category/benchmark-swebench.md),
[`benchmark-taubench`](by-category/benchmark-taubench.md),
[`benchmark-workarena`](by-category/benchmark-workarena.md),
[`granularity-conditioning`](by-category/granularity-conditioning.md),
[`hierarchical-planning`](by-category/hierarchical-planning.md),
[`uncertainty-calibration`](by-category/uncertainty-calibration.md); [By date
added](by-date-added/README.md)

---

## 2024 (7)

<details>
<summary>🏤 Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence
Elicitation in LLMs — Xiong et al., 2024</summary>

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
<summary>📝 FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning
in AI — Glazer et al., 2024</summary>

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
<summary>📋 Introducing SWE-bench Verified — team, 2024</summary>

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
<summary>🏤 SWE-bench: Can Language Models Resolve Real-World GitHub Issues? —
Jimenez et al., 2024</summary>

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
<summary>📝 tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World
Domains — Yao et al., 2024</summary>

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
<summary>🏤 WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work
Tasks? — Drouin et al., 2024</summary>

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
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/summary.md) |

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
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/summary.md) |

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
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/summary.md) |

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
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2205.10625/summary.md) |

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
