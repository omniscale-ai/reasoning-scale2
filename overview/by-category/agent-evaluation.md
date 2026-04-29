# Category: Agent Evaluation

Running the A/B/C conditions against annotated tasks and computing the three project metrics.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (7)](../papers/by-category/agent-evaluation.md) | [Suggestions
(14)](../suggestions/by-category/agent-evaluation.md) | [Datasets
(1)](../datasets/by-category/agent-evaluation.md) | [Libraries
(3)](../libraries/by-category/agent-evaluation.md)

---

## Papers (7)

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

## Tasks (1)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |

## Answers (0)

No answers in this category.

## Suggestions (11 open, 3 closed)

<details>
<summary>📊 <strong>Register pass^k as a project metric for reliability
reporting</strong> (S-0002-01)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-04-29 | **Source**:
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

**Kind**: library | **Priority**: high | **Date**: 2026-04-29 | **Source**:
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

**Kind**: library | **Priority**: high | **Date**: 2026-04-29 | **Source**:
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

**Kind**: library | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
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

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-29 | **Source**:
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
