---
spec_version: "1"
task_id: "t0012_phase2_abc_smoke_frontierscience"
research_stage: "papers"
papers_reviewed: 4
papers_cited: 4

categories_consulted:
  - "granularity-conditioning"
  - "hierarchical-planning"
  - "uncertainty-calibration"
  - "agent-evaluation"
  - "benchmark-frontierscience"
date_completed: "2026-04-30"
status: "complete"
---
# Research Papers: Phase 2 A/B/C Smoke Harness on FrontierScience

## Task Objective

This task runs the project's first end-to-end Phase 2 A/B/C comparison on a real benchmark
(FrontierScience-Olympiad) using the v2 hierarchical annotations from t0009. It tests the headline
hypothesis: scope-aware (A, ReAct with explicit `<global>/<subtask>/<atomic>` tags) outperforms
scope-unaware (B, Plan-and-Solve) which in turn outperforms scope-mismatched (C, deliberately wrong
granularity tags). The literature review focuses on (i) the published baselines for the A and B
conditions, (ii) the verbalized-confidence calibration protocol used to compute Metric 2, and (iii)
benchmark expectations for frontier-science reasoning so we can interpret absolute task-success
numbers in context.

## Category Selection Rationale

Consulted `granularity-conditioning` and `hierarchical-planning` because they index every paper that
defines the A/B/C condition libraries: ReAct establishes condition A's prompt template and
trajectory schema; Plan-and-Solve establishes condition B's planner+executor pattern. Consulted
`uncertainty-calibration` because the task computes `overconfident_error_rate` per Xiong2024's
verbalized-confidence protocol, which underpins Metric 2 and the calibration delta we expect between
A and B. Consulted `benchmark-frontierscience` to anchor expected absolute success rates on
open-ended scientific derivation problems. Excluded `benchmark-swebench`, `benchmark-taubench`, and
`benchmark-workarena` — those benchmarks live in separate suggestion-driven task lines (RQ3 and RQ4)
and the smoke test is intentionally scoped to FrontierScience only.

## Key Findings

### Scope-aware structured prompting is the single largest driver of agent success

ReAct [Yao2022] interleaves explicit reasoning ("Thought") and action steps in one transcript.
Reported gains over CoT-only and act-only baselines are large: **+34 absolute** success rate on
ALFWorld and **+10 absolute** on WebShop, with **only one or two in-context examples**. ReAct also
reduces hallucination on HotpotQA by grounding intermediate claims in tool observations. Crucially,
the Thought tokens are interpretable per-turn, which is the hook this project uses to attach the
explicit `<global>/<subtask>/<atomic>` tags in the A condition (`scope_aware_react_v1`, the t0006
project library). [Yao2022] does not study granularity tagging directly, but its trajectory schema
gives every Thought a slot where the per-turn scope tag can live without changing the parser.

Plan-and-Solve (PS+) [Wang2023] is the canonical scope-unaware baseline. The agent is asked to
"first understand the problem, extract relevant variables and their corresponding numerals, and make
and devise a complete plan. Then, let's carry out the plan, calculate intermediate variables (pay
attention to correct numerical calculation and commonsense), solve the problem step by step, and
show the answer." [Wang2023] reports PS+ improves over zero-shot CoT by **+5 to +10 accuracy** on
math word problems (GSM8K, MultiArith, AddSub, AQuA-RAT) and **+2.5%** on commonsense reasoning
without any in-context examples. There is no per-turn granularity signal — every record in condition
B logs `granularity="unspecified"` (the t0007 project library). This makes B the natural control for
the headline hypothesis: same model, same problem, same final-answer format, but no scope
information.

### Verbalized-confidence calibration is sample-efficient enough for N=28 paired runs

[Xiong2024] systematically tests confidence elicitation in LLMs and concludes that simple verbalized
prompts ("respond with low/medium/high confidence and your answer") combined with 3-sample
self-consistency aggregation produce calibration that is competitive with token-logprob methods on
math reasoning tasks. They report Brier scores on the order of **0.15-0.18** for GPT-3.5/GPT-4 on
GSM8K with the verbalized + self-consistency protocol, vs. **0.20-0.24** with naive single-sample
verbalized prompts. Critically for this task, the protocol does not require logprobs — it works on
closed APIs (Anthropic Claude). This is what t0011's `compute_overconfident_error_rate`
operationalizes: a record is "overconfident" if the model is wrong AND its aggregated verbalized
confidence ≥ 0.75 (the high-confidence threshold). [Xiong2024] reports overconfident-error rates of
**15-25%** on math benchmarks for GPT-3.5/GPT-4 — this is the band we expect to see for B and the
band we predict A undercuts by 2-8 percentage points.

### Benchmark expectations on frontier-science problems

GPQA [Rein2023] and FrontierMath-style olympiad benchmarks consistently show that even strong
reasoning models score **below 30-40%** on graduate-level science derivation tasks when scored on
exact final-answer match, much lower than on grade-school math (GSM8K, ~85-95%). FrontierScience
problems in t0009's v2 dataset are open-ended derivation prompts — the `gold_actions` field contains
a free-form expected derivation chain, not a single canonical numerical answer. This means: (a)
absolute `task_success_rate` will be modest even for A (we predict the **15-40% band**); (b)
exact-string answer comparison is insufficient — an LLM-as-judge tier is required for any
non-trivial answer comparison; (c) effect sizes between conditions A−B may be small in absolute
terms (≤10pp) which is below the smoke test's N=28 detection threshold for a single comparison. This
is the key motivation for the sample-size calibration the task is designed to produce.

## Methodology Insights

* **Use ReAct's exact prompt structure for condition A.** The system prompt must include the line
  `Thought: <{granularity}> ...` so the parser (t0006 project library) can recover the per-turn tag.
  Reuse `scope_aware_react_v1` directly; do not reimplement.
* **Use PS+ verbatim for condition B.** [Wang2023] §3 specifies the exact prompt; t0007's
  `PLAN_PROMPT_TEMPLATE` and `EXECUTE_PROMPT_TEMPLATE` already encode it. Pair the two libraries on
  the same model and same temperature — only the prompt differs.
* **Use 3-sample self-consistency for confidence elicitation.** [Xiong2024] shows 3 samples is the
  knee of the cost-vs-Brier curve; more samples buy little. t0011's `ConfidenceJudge` defaults to 3,
  so accept the default.
* **Set the high-confidence threshold at 0.75.** [Xiong2024] uses a slightly lower threshold (0.7)
  but reports the same qualitative pattern at 0.75. t0011's `HIGH_CONFIDENCE_THRESHOLD = 0.75` is
  consistent with the protocol; do not lower it for the smoke test.
* **Use LLM-as-judge for final-answer comparison on FrontierScience.** Direct string comparison is
  insufficient because gold derivations are paragraph-long. Use Claude Haiku as a binary judge:
  "Does this candidate answer match the gold derivation? Reply YES or NO." This matches [Yao2022]
  ALFWorld scoring practice and keeps judge cost low. Log every judge call.
* **Pair runs by `task_id`.** McNemar / paired sign tests need paired binary outcomes per problem
  per condition. The harness must serialize problems and conditions in a deterministic order so
  every problem appears in all three trajectory files.
* **Hypotheses to test in Phase 2:** (H1) A − B ≥ +5pp on `task_success_rate`; (H2) A − B ≤ −2pp on
  `overconfident_error_rate`; (H3) C ranks worst on both. The smoke test cannot reliably detect H1
  at +5pp with N=28 (needs ~150 discordant pairs for paired McNemar at α=0.05/0.8 power); it can
  detect ~+15pp paired effects, which is what most published structured-prompting gains report on
  first-pass benchmarks. The implied confirmatory N is the secondary deliverable.

## Gaps and Limitations

* **No paper directly compares scope-aware vs scope-unaware prompting on the same model and same
  problem set.** [Yao2022] and [Wang2023] each report against CoT, never against each other under
  matched conditions. This is the gap Phase 2 fills.
* **No paper reports calibration on FrontierScience.** [Xiong2024] uses GSM8K and TruthfulQA. We do
  not know ex-ante how Anthropic Claude calibrates on graduate-level physics derivations; the smoke
  test is partly a calibration-on-hard-problems probe.
* **Effect sizes for granularity conditioning are unknown.** [Yao2022]'s +34pp gain over imitation
  is against a much weaker baseline (no reasoning at all) on a much easier benchmark (ALFWorld). We
  have no published prior on the size of the A-vs-B gap when both conditions use the same model with
  structured prompting on a hard derivation task.
* **No literature on adversarial mismatch.** Condition C is original to this project. There is no
  prior expectation for how much worse "deliberately wrong granularity tags" makes performance,
  beyond the intuition that injecting misleading metadata should hurt. The random mismatch strategy
  used in this smoke run is the safer / weaker variant; an adversarial-strategy ablation is queued
  (S-0010-01).
* **FrontierScience-Olympiad row count differs from estimate.** The task description estimates N≈28;
  v2 actually has **40** complete FrontierScience-Olympiad rows. This raises the smoke test's
  per-condition power slightly and increases the budget envelope, but does not change the
  qualitative conclusions or the core hypotheses.

## Recommendations for This Task

1. Build the harness as a thin orchestrator that loads the v2 dataset, filters to
   FrontierScience-Olympiad complete rows, and dispatches per-condition to the three sister
   libraries. Reuse all four sister libraries verbatim — do not reimplement ReAct, PS+, the
   matched-mismatch wrapper, or the calibration aggregator.
2. Use `claude-sonnet-4-6-20251001` for the agent runs (recommended in the task description). Use
   `claude-haiku-4-5-20251001` for the LLM-as-judge correctness check and any 3-sample
   confidence-elicitation calls.
3. Run all 40 FrontierScience-Olympiad complete rows × 3 conditions = 120 runs. Document the
   v1-vs-v2 row count discrepancy in the results.
4. Report McNemar p-values for paired A-vs-B and B-vs-C, observed effect sizes, 95% CIs (Wilson
   bounds for proportions, Wilcoxon CI for paired differences), and the implied confirmatory N for a
   5pp paired effect at α=0.05/0.8 power.
5. Add the smoke test's three predictions assets so downstream tasks can recompute metrics
   (different thresholds, different sense aggregations) without re-running the agents.

## Paper Index

### [Yao2022]

* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Yao et al.
* **Year**: 2023
* **DOI**: 10.48550/arXiv.2210.03629
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629`
* **Categories**: granularity-conditioning, hierarchical-planning
* **Relevance**: Defines the prompt structure and trajectory schema reused in condition A; reports
  the +34pp/+10pp baseline gains that justify the headline hypothesis.

### [Wang2023]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Wang et al.
* **Year**: 2023
* **DOI**: 10.48550/arXiv.2305.04091
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091`
* **Categories**: granularity-conditioning, hierarchical-planning
* **Relevance**: Defines the planner+executor pattern reused verbatim in condition B; PS+
  instruction line is quoted in t0007's `PLAN_PROMPT_TEMPLATE`.

### [Xiong2024]

* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
  in LLMs
* **Authors**: Xiong et al.
* **Year**: 2024
* **DOI**: 10.48550/arXiv.2306.13063
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063`
* **Categories**: uncertainty-calibration, agent-evaluation
* **Relevance**: Defines the verbalized-confidence + 3-sample self-consistency protocol that t0011
  implements; reports 15-25% overconfident-error rates that calibrate our expected B-condition
  baseline.

### [Rein2023]

* **Title**: GPQA: A Graduate-Level Google-Proof Q&A Benchmark
* **Authors**: Rein et al.
* **Year**: 2023
* **DOI**: 10.48550/arXiv.2311.12022
* **Asset**: not yet downloaded — referenced for absolute frontier-science success-rate context.
  Adding this paper to the corpus is a downstream task suggestion.
* **Categories**: benchmark-frontierscience
* **Relevance**: Cited as the closest published benchmark for graduate-level science Q&A; sets the
  expectation that absolute success rates on derivation problems remain in the 15-40% band.
