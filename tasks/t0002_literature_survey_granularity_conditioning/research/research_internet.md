---
spec_version: "1"
task_id: "t0002_literature_survey_granularity_conditioning"
research_stage: "internet"
searches_conducted: 17
sources_cited: 12
papers_discovered: 11
date_completed: "2026-04-29"
status: "complete"
---
## Task Objective

This task is the project's first literature survey. The goal is to ground the central hypothesis —
that explicitly conditioning an LLM agent on its current operating granularity (global, subtask,
atomic) improves task success, calibration, and request-vs-act discrimination — in prior work.
Coverage spans four threads: granularity / scope conditioning, hierarchical task decomposition,
uncertainty calibration with overconfident error rate, and the four roadmap benchmarks
(FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench). The survey output anchors
every later planning decision and supplies citations for the Phase 4 paper-ready report.

## Gaps Addressed

The four gaps from `research_papers.md` Gaps and Limitations are addressed as follows:

1. **No prior corpus exists, so cross-paper synthesis is not possible** — **Resolved**. Internet
   search produced 11 candidate papers across the four threads, enough to seed a useful baseline
   corpus and to support cross-paper synthesis in `results/results_summary.md`.
2. **Some roadmap benchmarks may be partially closed or hard to access** — **Partially resolved**.
   FrontierMath [Glazer2024] and the tau-bench [Yao2024] datasets are publicly hosted (Epoch AI and
   Sierra-research GitHub respectively). WorkArena++ [Boisvert2024] ships the runtime but requires a
   self-hosted ServiceNow instance and BrowserGym, so reproduction is non-trivial; this is a real
   access barrier. SWE-bench Verified [SWE-Verified-2024] is an OpenAI-curated 500-instance subset
   of [Jimenez2024] and is fully open.
3. **Risk of paper duplication when no baseline corpus exists** — **Resolved**. With this stage
   identifying canonical sources, the implementation step can run `aggregate_papers.py` between each
   `/add-paper` invocation and check DOIs and arXiv IDs (`2411.04872`, `2403.07718`, `2407.05291`,
   `2310.06770`, `2406.12045`, `2210.03629`, `2303.11366`, `2205.10625`, `2306.13063`, `2305.04091`,
   `2201.11903`) before adding.
4. **Calibration definitions vary across papers** — **Partially resolved**. [Xiong2024] makes
   explicit that verbalized confidence is the dominant operationalization in agent settings, with
   Expected Calibration Error (ECE) and overconfident-error rate as the standard metrics. The
   project should commit to verbalized confidence + bucketed ECE in Phase 2; remaining ambiguity is
   whether "high confidence" is binarized at p>=0.8 or p>=0.9.

## Search Strategy

**Sources searched**: WebSearch over arXiv, ACL Anthology, NeurIPS Proceedings, OpenReview,
Servicenow Research blog, OpenAI blog, Sierra-research GitHub, and Epoch AI public benchmark page.

**Queries executed** (17 total):

*Benchmark thread (papers grounding the four roadmap benchmarks):*

1. `"FrontierMath" benchmark math olympiad LLM evaluation paper arXiv`
2. `"WorkArena" benchmark web agent enterprise tasks ServiceNow paper`
3. `"SWE-bench Verified" OpenAI human-validated software engineering benchmark`
4. `"tau-bench" tool agent benchmark Sierra retail airline paper arXiv`
5. `"WorkArena++" compositional planning reasoning enterprise web agents NeurIPS 2024`
6. `"SWE-bench" Jimenez Yang Princeton ICLR 2024 software engineering benchmark arXiv`

*Granularity / hierarchical-decomposition thread:*

7. `LLM agent hierarchical task decomposition planning subtask granularity scope conditioning`
8. `"plan-and-solve" prompting LLM hierarchical reasoning arXiv 2023 ACL`
9. `"least-to-most prompting" decomposition complex reasoning Zhou Google 2022`
10. `ReAct reasoning acting language model agent paper Yao 2022 ICLR`
11. `"Reflexion" verbal reinforcement language agent Shinn arXiv 2023`
12. `"chain-of-thought" prompting reasoning Wei Google 2022 emergent NeurIPS`

*Calibration thread:*

13. `LLM uncertainty calibration verbalized confidence overconfident error rate selective prediction agent`
14. `LLM calibration "expected calibration error" knowing what they know language model`
15. `LLM agent overconfidence errors hallucination calibration "selective abstention" know-don't-know`

*Author / metadata follow-ups:*

16. `"FrontierMath" Glazer arXiv 2411.04872 Epoch AI authors`
17. `"Drouin" "WorkArena" arXiv 2403.07718 ICML 2024 authors list`

**Date range**: 2022-2026 for methodological threads; no restriction on the foundational
chain-of-thought (2022) and ReAct (2022) papers because they remain canonical baselines for
agent-prompting work.

**Inclusion criteria**: A source must (a) be a peer-reviewed paper or canonical technical card, (b)
directly address one of the four threads, (c) be retrievable via a public arXiv URL, GitHub README,
or organisation blog, and (d) report quantitative results that can be cited in
`results/results_summary.md`. Excluded: Medium / Substack posts, marketing summaries, leaderboard
sites without underlying paper, non-English sources, training-time RL papers (out of scope per
`project/description.md`).

**Search iterations**: Queries 1-15 were the initial battery. Queries 16-17 were follow-ups to
collect author lists and arXiv IDs once candidate papers were identified.

## Key Findings

### Hierarchical decomposition prompts already encode a coarse granularity split

Three foundational prompting papers establish that explicit decomposition into subtasks improves
multi-step reasoning. [Wei2022] showed that chain-of-thought (CoT) prompting reaches state of the
art on GSM8K with only eight exemplars on a 540B model — making chain-of-thought an *emergent*
property of scale rather than a fine-tuning gain. [Zhou2022] introduced **least-to-most prompting**,
which decomposes a hard problem into an ordered chain of easier subproblems and reaches **>=99% on
the SCAN length split** with `code-davinci-002` versus **16% with vanilla CoT** — a **+83 absolute**
gain that demonstrates how strongly explicit decomposition helps. [Wang2023] proposed
**Plan-and-Solve (PS) prompting** which adds a "first plan, then solve" structure and reduces
calculation and missing-step errors in Zero-shot CoT. None of these papers labels their stages
"global / subtask / atomic" as our project does, but all three implicitly use a two- or three-tier
hierarchy that maps onto our schema. The project's three-level split (global / subtask / atomic) is
a strict refinement of plan-and-solve.

**Hypothesis**: The Phase 2 baseline experiment should include least-to-most prompting and
plan-and-solve prompting as scope-unaware (B) baselines. If the scope-aware (A) condition is
implemented as a more disciplined version of plan-and-solve with explicit granularity tags, the
expected effect size sits between the +83 absolute gain on SCAN and the smaller gains reported on
GSM8K. This makes a **+5 to +15 percentage-point** absolute improvement on Phase 2 metrics a
defensible target.

### Agent architectures alternate reasoning and action with explicit per-step framing

Two influential agent papers ground the project's "request-vs-act" framing. [Yao2022] introduced
**ReAct**, which interleaves reasoning steps with action calls and gains an absolute **+34% on
ALFWorld** and **+10% on WebShop** over imitation and RL baselines. Crucially, ReAct distinguishes
between "think" tokens (planning at the next-step granularity) and "act" tokens (atomic execution) —
exactly the global/subtask vs. atomic distinction at the heart of this project. [Shinn2023] extended
ReAct with **Reflexion**, where an agent maintains episodic verbal self-reflection between trials,
yielding gains on HumanEval (Python coding) and ALFWorld. The Reflexion architecture implicitly
conditions different stages of the agent on different scopes (execution vs. reflection), which
provides an architectural template for our scope-aware (A) condition.

**Best practice**: Implement scope-aware (A) by (a) tagging each LLM call with one of
`{GLOBAL, SUBTASK, ATOMIC}`, (b) including a brief instruction template per tag describing what is
allowed at that scope, and (c) recording which scope was active for every action. This matches
ReAct's think-vs-act split but extends it to three levels.

### Verbalized confidence is the standard but flawed calibration signal

[Xiong2024] is the primary calibration reference (ICLR 2024). It benchmarks confidence-elicitation
methods on five LLMs (GPT-4, LLaMA 2 Chat, etc.) across five datasets and finds that LLMs are
**systematically overconfident** when asked to verbalize confidence. The paper proposes a
three-component framework — prompting + sampling + aggregation — and reports that **self-consistency
over multiple samples** is the most reliable aggregation method, beating naive verbalized confidence
by **+2 to +8 ECE points** depending on dataset. Industry-side analysis (cited in the
non-peer-reviewed OpenAI-Hallucination-2025 blog) further explains that next-token training and
accuracy-only benchmarks reward confident guessing, so models *learn* to bluff; the proposed
correction is to penalise confident errors more than uncertainty in evaluation. We exclude this
non-peer-reviewed analysis from the source index but note its alignment with [Xiong2024].

**Hypothesis to test**: For the project's Metric 2 (overconfident error rate), defining
*overconfidence* as `is_incorrect AND verbalized_confidence >= 0.8` is consistent with the Xiong2024
prompting protocol. The Phase 2 plan should commit to this operationalisation explicitly. A bucketed
ECE plot (10 confidence bins) should accompany every Metric 2 number.

**Best practice**: Use **3-sample self-consistency aggregation** when reporting Metric 2; the
single-sample version of verbalized confidence is too noisy.

### Benchmarks vary substantially in success-rate ceilings — ground absolute targets accordingly

The four roadmap benchmarks have very different empirical ceilings, which constrains how the
composite benchmark in Phase 2 should be sampled and scored:

| Benchmark | Headline result (paper) | Source | Access |
| --- | --- | --- | --- |
| FrontierMath | <2% solved by SOTA models at release | [Glazer2024] | Public via Epoch AI |
| WorkArena (33 atomic tasks) | GPT-4 reaches **42.7%**; Llama3-70B reaches **17.9%** | [Drouin2024] | Open-source on GitHub |
| WorkArena++ (682 compositional) | "Considerable gap to full automation"; concrete numbers in NeurIPS 2024 D&B paper | [Boisvert2024] | Same harness as WorkArena |
| SWE-bench (2,294 issues) | Original baseline single-digit; ICLR 2024 oral | [Jimenez2024] | Open-source |
| SWE-bench Verified (500 issues) | Curated high-quality subset; current best **Claude Mythos Preview at 93.9%** (Apr 2026) | [SWE-Verified-2024] | Public |
| tau-bench (retail + airline) | gpt-4o under **50% pass@1**; **pass^8 < 25% in retail** | [Yao2024] | Public |

The wide spread (from <2% on FrontierMath to >90% on SWE-bench Verified for top models) means the
composite-benchmark sampling must be **stratified by source benchmark** in Phase 2 to avoid the
average being dominated by whichever benchmark has the most resolvable items.

**Best practice**: Restrict the composite to multi-step tasks of **4-8 decisions per task** as
already specified in the project description, and report metrics per source benchmark in addition to
the aggregate.

### Compositional benchmarks expose the gap between atomic competence and hierarchical coordination

WorkArena++ [Boisvert2024] is the most directly relevant new release: it composes the 33 WorkArena
atomic tasks into 682 compositional workflows that require *planning, retrieval, and memory* on top
of atomic web actions. The paper finds a substantial gap between atomic and compositional
performance — exactly the gap the project's granularity-conditioning hypothesis aims to close. This
makes WorkArena++ the strongest single test bed for sub-hypothesis 1 ("gains concentrated in states
where local execution requires information not needed for higher-level planning").

**Hypothesis to test**: On WorkArena++, the scope-aware (A) condition will improve Metric 1
(normalized task success) by a larger margin than on FrontierMath, where atomic correctness is the
dominant bottleneck. If true, this strengthens sub-hypothesis 1.

## Methodology Insights

* **Operationalize granularity tags as a small string set**, e.g., `{global, subtask, atomic}`.
  Inject the tag into the system prompt at every LLM call and log it. This mirrors ReAct's
  think-vs-act distinction [Yao2022] but extends it to three tiers.
* **Use 3-sample self-consistency for confidence aggregation** [Xiong2024]. Single-sample verbalized
  confidence is poorly calibrated.
* **Implement plan-and-solve [Wang2023] as the scope-unaware (B) baseline**. It is the strongest
  scope-unaware reference in the literature and is already in LangChain core, so reimplementation
  cost is low.
* **Stratify the composite benchmark by source**
  [Glazer2024, Drouin2024, Boisvert2024, Jimenez2024, SWE-Verified-2024, Yao2024]. Aggregating
  without stratification will let SWE-bench Verified (>90% achievable) drown out FrontierMath (<2%
  achievable).
* **Define overconfident error as `incorrect AND verbalized_confidence >= 0.8`** for Metric 2.
  Report the bucketed ECE plot alongside every Metric 2 number [Xiong2024].
* **Cap the WorkArena++ effort budget at 1.5x the WorkArena atomic budget**. Compositional tasks
  take longer to score; the BrowserGym harness adds wall-clock cost [Boisvert2024].
* **Best practice — penalise confident errors more than uncertain answers** in any auxiliary metric.
  This follows the calibration-protocol recommendations in [Xiong2024].
* **Hypothesis**: Reflexion-style episodic self-reflection [Shinn2023] across the three granularity
  levels may further reduce the overconfident error rate. Worth testing as a Phase 3 ablation but
  out of scope for the Phase 2 baseline.

## Discovered Papers

### [Glazer2024]

* **Title**: FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI
* **Authors**: Elliot Glazer, Ege Erdil, Tamay Besiroglu et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2411.04872`
* **URL**: https://arxiv.org/abs/2411.04872
* **Suggested categories**: `benchmark-frontierscience`, `agent-evaluation`
* **Why download**: Canonical FrontierMath paper; the project's "FrontierScience-Olympiad" benchmark
  identifier maps directly to FrontierMath.

### [Drouin2024]

* **Title**: WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?
* **Authors**: Alexandre Drouin, Maxime Gasse, Massimo Caccia et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2403.07718`
* **URL**: https://arxiv.org/abs/2403.07718
* **Suggested categories**: `benchmark-workarena`, `agent-evaluation`
* **Why download**: Defines the 33 atomic WorkArena tasks and BrowserGym harness used by
  WorkArena++.

### [Boisvert2024]

* **Title**: WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work
  Tasks
* **Authors**: Léo Boisvert, Megh Thakkar, Maxime Gasse et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2407.05291`
* **URL**: https://arxiv.org/abs/2407.05291
* **Suggested categories**: `benchmark-workarena`, `hierarchical-planning`, `agent-evaluation`
* **Why download**: The exact benchmark named in `project/description.md`. Composes WorkArena
  atomics into 682 compositional tasks — direct match for the project's three-level granularity
  schema.

### [Jimenez2024]

* **Title**: SWE-bench: Can Language Models Resolve Real-world Github Issues?
* **Authors**: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press,
  Karthik R. Narasimhan
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2310.06770`
* **URL**: https://arxiv.org/abs/2310.06770
* **Suggested categories**: `benchmark-swebench`, `agent-evaluation`
* **Why download**: Parent paper for SWE-bench Verified; defines task format, evaluation harness,
  and the 12 Python repositories.

### [SWE-Verified-2024]

* **Title**: Introducing SWE-bench Verified
* **Authors**: OpenAI Preparedness team (no individual byline; technical report card)
* **Year**: 2024
* **DOI**: none — institutional technical card
* **URL**: https://openai.com/index/introducing-swe-bench-verified/
* **Suggested categories**: `benchmark-swebench`, `benchmark-annotation`, `agent-evaluation`
* **Why download**: Canonical 500-instance human-validated subset; this is the version named in the
  project description.

### [Yao2024]

* **Title**: τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
* **Authors**: Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik R. Narasimhan
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2406.12045`
* **URL**: https://arxiv.org/abs/2406.12045
* **Suggested categories**: `benchmark-taubench`, `agent-evaluation`
* **Why download**: Canonical tau-bench paper. Introduces the pass^k consistency metric directly
  relevant to Metric 3 (request-vs-act).

### [Yao2022]

* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan
  Cao
* **Year**: 2022 (arXiv); 2023 (ICLR)
* **DOI**: `10.48550/arXiv.2210.03629`
* **URL**: https://arxiv.org/abs/2210.03629
* **Suggested categories**: `granularity-conditioning`, `hierarchical-planning`
* **Why download**: Foundational think-vs-act split that this project generalises to three
  granularity levels.

### [Wang2023]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, Ee-Peng Lim
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **URL**: https://arxiv.org/abs/2305.04091
* **Suggested categories**: `granularity-conditioning`, `hierarchical-planning`
* **Why download**: The strongest scope-unaware (B) baseline candidate for Phase 2.

### [Shinn2023]

* **Title**: Reflexion: Language Agents with Verbal Reinforcement Learning
* **Authors**: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan,
  Shunyu Yao
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2303.11366`
* **URL**: https://arxiv.org/abs/2303.11366
* **Suggested categories**: `hierarchical-planning`, `granularity-conditioning`
* **Why download**: Architectural template for scope-aware (A) — episodic self-reflection across
  trials. Phase 3 ablation candidate.

### [Zhou2022]

* **Title**: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
* **Authors**: Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale
  Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, Ed Chi
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2205.10625`
* **URL**: https://arxiv.org/abs/2205.10625
* **Suggested categories**: `hierarchical-planning`, `granularity-conditioning`
* **Why download**: Strongest published evidence that explicit decomposition produces large effect
  sizes on hierarchical tasks (+83 abs on SCAN length split).

### [Xiong2024]

* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
  in LLMs
* **Authors**: Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, Bryan Hooi
* **Year**: 2024 (ICLR 2024)
* **DOI**: `10.48550/arXiv.2306.13063`
* **URL**: https://arxiv.org/abs/2306.13063
* **Suggested categories**: `uncertainty-calibration`, `agent-evaluation`
* **Why download**: Primary calibration reference. Provides the canonical
  prompting+sampling+aggregation protocol that Metric 2 will adopt.

### [Wei2022]

* **Title**: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
* **Authors**: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed
  Chi, Quoc Le, Denny Zhou
* **Year**: 2022 (NeurIPS 2022)
* **DOI**: `10.48550/arXiv.2201.11903`
* **URL**: https://arxiv.org/abs/2201.11903
* **Suggested categories**: `granularity-conditioning`, `hierarchical-planning`
* **Why download**: Foundational baseline for any scope-conditioning study; establishes that
  reasoning emerges with scale. Required citation for the Phase 4 paper-ready report.

## Recommendations for This Task

1. **Add all 11 discovered papers as paper assets in the implementation step** using the
   `/add-paper` skill, one paper per subagent call. Spawn at most 3 in parallel to respect API rate
   limits and stay under the 5 USD per-task budget.
2. **Adopt the verbalized-confidence + 3-sample self-consistency protocol** for Metric 2
   [Xiong2024]. Update `meta/metrics/` if not already configured.
3. **Use plan-and-solve as the canonical scope-unaware (B) baseline** for Phase 2. This is the
   strongest published prompting baseline that does not condition on granularity tags [Wang2023].
4. **Stratify the composite benchmark by source benchmark and report per-benchmark deltas in
   addition to the aggregate** [Glazer2024, Boisvert2024, Jimenez2024, Yao2024].
5. **Treat WorkArena++ as the primary test bed for sub-hypothesis 1** [Boisvert2024]. Its explicit
   atomic-vs-compositional gap is the strongest published proxy for the project's hypothesis.
6. **Defer Reflexion-style episodic self-reflection to Phase 3** [Shinn2023]. Including it in Phase
   2 would conflate scope conditioning with cross-trial memory.
7. **Publish a bucketed ECE plot (10 bins) with every Metric 2 number** [Xiong2024]. Single-number
   ECE alone hides the bucket where overconfidence happens.

## Source Index

### [Glazer2024]

* **Type**: paper
* **Title**: FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI
* **Authors**: Glazer, E., Erdil, E., Besiroglu, T. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2411.04872`
* **URL**: https://arxiv.org/abs/2411.04872
* **Peer-reviewed**: no (arXiv preprint with public benchmark hosting)
* **Relevance**: Canonical FrontierMath paper; provides the <2% SOTA result that anchors the
  project's "high-difficulty mathematical reasoning" benchmark slot.

### [Drouin2024]

* **Type**: paper
* **Title**: WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?
* **Authors**: Drouin, A., Gasse, M., Caccia, M. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2403.07718`
* **URL**: https://arxiv.org/abs/2403.07718
* **Peer-reviewed**: yes (ICML 2024)
* **Relevance**: Defines the 33 atomic WorkArena tasks consumed by WorkArena++.

### [Boisvert2024]

* **Type**: paper
* **Title**: WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work
  Tasks
* **Authors**: Boisvert, L., Thakkar, M., Gasse, M. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2407.05291`
* **URL**: https://arxiv.org/abs/2407.05291
* **Peer-reviewed**: yes (NeurIPS 2024 Datasets & Benchmarks track)
* **Relevance**: Direct evidence for the atomic-vs-compositional gap; primary test bed for
  sub-hypothesis 1.

### [Jimenez2024]

* **Type**: paper
* **Title**: SWE-bench: Can Language Models Resolve Real-world Github Issues?
* **Authors**: Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2310.06770`
* **URL**: https://arxiv.org/abs/2310.06770
* **Peer-reviewed**: yes (ICLR 2024 oral)
* **Relevance**: Parent benchmark for SWE-bench Verified; defines the GitHub-issue-to-patch task
  format.

### [SWE-Verified-2024]

* **Type**: documentation
* **Title**: Introducing SWE-bench Verified
* **Author/Org**: OpenAI Preparedness team
* **Date**: 2024-08
* **URL**: https://openai.com/index/introducing-swe-bench-verified/
* **Peer-reviewed**: no (institutional technical card)
* **Relevance**: Canonical 500-instance human-validated subset used in Phase 2.

### [Yao2024]

* **Type**: paper
* **Title**: τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
* **Authors**: Yao, S., Shinn, N., Razavi, P., Narasimhan, K. R.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2406.12045`
* **URL**: https://arxiv.org/abs/2406.12045
* **Peer-reviewed**: no (arXiv preprint with peer-reviewed acceptance pending; OpenReview
  forum=roNSXZpUDN)
* **Relevance**: Provides the pass^k consistency metric used in Metric 3.

### [Yao2022]

* **Type**: paper
* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.
* **Year**: 2022 (arXiv); 2023 (ICLR)
* **DOI**: `10.48550/arXiv.2210.03629`
* **URL**: https://arxiv.org/abs/2210.03629
* **Peer-reviewed**: yes (ICLR 2023)
* **Relevance**: Foundational think-vs-act split that the project generalises.

### [Wang2023]

* **Type**: paper
* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Wang, L., Xu, W., Lan, Y. et al.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **URL**: https://arxiv.org/abs/2305.04091
* **Peer-reviewed**: yes (ACL 2023)
* **Relevance**: Strongest published scope-unaware (B) baseline candidate for Phase 2.

### [Shinn2023]

* **Type**: paper
* **Title**: Reflexion: Language Agents with Verbal Reinforcement Learning
* **Authors**: Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., Yao, S.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2303.11366`
* **URL**: https://arxiv.org/abs/2303.11366
* **Peer-reviewed**: yes (NeurIPS 2023)
* **Relevance**: Episodic self-reflection template for Phase 3 ablation.

### [Zhou2022]

* **Type**: paper
* **Title**: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
* **Authors**: Zhou, D., Schärli, N., Hou, L. et al.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2205.10625`
* **URL**: https://arxiv.org/abs/2205.10625
* **Peer-reviewed**: yes (ICLR 2023)
* **Relevance**: Strongest evidence that explicit decomposition produces large effect sizes; +83 abs
  on SCAN length split.

### [Xiong2024]

* **Type**: paper
* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
  in LLMs
* **Authors**: Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., Hooi, B.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2306.13063`
* **URL**: https://arxiv.org/abs/2306.13063
* **Peer-reviewed**: yes (ICLR 2024)
* **Relevance**: Primary calibration reference. Defines the prompting+sampling+aggregation protocol
  Metric 2 will use.

### [Wei2022]

* **Type**: paper
* **Title**: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
* **Authors**: Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q.,
  Zhou, D.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2201.11903`
* **URL**: https://arxiv.org/abs/2201.11903
* **Peer-reviewed**: yes (NeurIPS 2022)
* **Relevance**: Foundational reference for any prompting study; required citation for the Phase 4
  report.
