# Category: Hierarchical Planning

Decomposition of tasks into global plan, subtask, and atomic execution levels.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (5)](../papers/by-category/hierarchical-planning.md) | [Suggestions
(5)](../suggestions/by-category/hierarchical-planning.md)

---

## Papers (5)

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
<summary>🏤 <strong>Reflexion: Language Agents with Verbal Reinforcement
Learning</strong> — Shinn et al., 2023</summary>

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

<details>
<summary>🏤 <strong>Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought
Reasoning by Large Language Models</strong> — Wang et al., 2023</summary>

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
<summary>🏤 <strong>ReAct: Synergizing Reasoning and Acting in Language
Models</strong> — Yao et al., 2023</summary>

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
<summary>🏤 <strong>Least-to-Most Prompting Enables Complex Reasoning in Large
Language Models</strong> — Zhou et al., 2022</summary>

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

## Tasks (1)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |

## Answers (0)

No answers in this category.

## Suggestions (2 open, 3 closed)

<details>
<summary>🧪 <strong>Defer Reflexion-style episodic memory to a Phase 3
ablation</strong> (S-0002-10)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0002_literature_survey_granularity_conditioning](../../tasks/t0002_literature_survey_granularity_conditioning/)

Reflexion [Shinn2023] adds verbal self-reflection across trials and reaches 91% pass@1 on
HumanEval vs. 80% for vanilla GPT-4. Including episodic memory in Phase 2 would conflate scope
conditioning with cross-trial memory. Schedule a dedicated Phase 3 ablation that tests whether
Reflexion-style memory adds further gains on top of the scope-aware (A) condition established
in Phase 2.

</details>

<details>
<summary>🧪 <strong>Derive step graphs for FrontierScience-Olympiad rows</strong>
(S-0003-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0003_download_benchmark_subsets](../../tasks/t0003_download_benchmark_subsets/)

FrontierScience-Olympiad pilot rows currently lack per-instance step graphs because Olympiad
solutions are graded as final answers. Run a hierarchical-annotation task that decomposes each
problem into global / subtask / atomic steps with gold actions at each level, so Phase 2 can
apply the canonical 4-8 decisions filter consistently across all four benchmarks.

</details>
