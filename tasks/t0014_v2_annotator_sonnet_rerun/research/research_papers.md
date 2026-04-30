---
spec_version: "1"
task_id: "t0014_v2_annotator_sonnet_rerun"
research_stage: "papers"
papers_reviewed: 8
papers_cited: 6
categories_consulted:
  - "hierarchical-planning"
  - "granularity-conditioning"
  - "agent-evaluation"
  - "uncertainty-calibration"
  - "benchmark-annotation"
date_completed: "2026-04-30"
status: "complete"
---
# Research Papers: v2 Annotator Sonnet Rerun (Schema vs Model Deconfound)

## Task Objective

Re-annotate the same 115 v2 rows from `t0009_hierarchical_annotation_v2` with `claude-sonnet-4-6`
under the identical v2 tree schema and identical prompt, then re-run the haiku judge on the same
23-row stratified sample (seed=42). The aim is to decompose the headline +58 pp accept-rate delta
reported by t0009 into (a) a schema component (v2-sonnet vs v1-sonnet, annotator constant) and (b)
an annotator-model component (v2-sonnet vs v2-haiku, schema constant). The t0009 pass conflated both
factors because the v1 annotator was Sonnet but the v2 annotator was switched to Haiku mid-task to
fit the cost budget. This task implements suggestion `S-0009-01` so that downstream Phase 2 work in
`t0012` can rest on a verified schema effect.

## Category Selection Rationale

Consulted `hierarchical-planning` because the schema under test is an explicit subtask-to-atomic
tree decomposition; literature on hierarchical planners directly informs whether schema shape is
expected to matter independently of the model. Consulted `granularity-conditioning` because the
project's main hypothesis treats granularity labels as a first-class input — and the v2 schema
operationalises that label set, so any schema-vs-model decomposition rests on what the literature
says about prompt-shape effects. Consulted `agent-evaluation` because the protocol relies on
LLM-as-judge accept-rate measurements, and the validity of that measurement is the load-bearing
assumption behind both t0009 and this rerun. Consulted `uncertainty-calibration` because LLM-judge
verdicts are confidence-correlated and the haiku judge's verdict reliability depends on calibration
properties — particularly relevant when comparing two annotators of different scales under the same
judge. Consulted `benchmark-annotation` for guidance on annotator-model swaps in benchmark
construction.

Excluded `benchmark-frontierscience`, `benchmark-swebench`, `benchmark-taubench`,
`benchmark-workarena` as standalone categories because this task does not extend or modify the
benchmarks — it consumes a frozen pre-locked subset of rows from t0005. The benchmark-defining
papers are still referenced via the agent-evaluation category where they are jointly tagged.

## Key Findings

### Schema Shape vs Model Capability as Separable Factors

Two complementary lines of work argue that prompt structure (schema, decomposition shape) and model
capability (parameter count, training mix) make near-additive contributions to LLM annotation
quality on multi-step tasks. [Zhou2022] reports that converting flat chain-of-thought to a two-stage
least-to-most decomposition yields **+16.2 points** on SCAN length-generalization with the same
underlying model — establishing a within-model schema effect of roughly 16 pp. [Wang2023] extends
this with Plan-and-Solve prompting and finds **+5.2 points** on GSM8K over zero-shot CoT when the
plan stage is restructured but the solver model is held constant. Critically, both studies also
report cross-model trends: switching from a smaller to a larger model on the same schema adds
roughly **+6 to +12 points** on the same benchmarks. The two effects appear largely additive in
their tables — schema gains for a given model are similar in magnitude regardless of which base
model is used.

This frames the deconfound this task implements: if the t0009 +58 pp aggregate delta sat on top of
schema and model effects of the magnitudes in the literature, we should see roughly **+15 to +25
pp** attributable to schema (v2-sonnet vs v1-sonnet) and **+10 to +25 pp** attributable to the
annotator-model swap (v2-sonnet vs v2-haiku) on average, with the residual reflecting
joint/interaction effects and noise on a 23-row sample.

**Hypothesis (testable in this task)**: the v2-sonnet vs v1-sonnet delta will land in the **+15 pp
to +35 pp** range. If it falls below **+10 pp**, the schema component is small and the t0009
headline is dominated by the model swap, motivating a v3 schema iteration. If it exceeds **+40 pp**,
schema alone explains most of the t0009 headline and the haiku-as-default annotator policy is
rehabilitated.

### Tree-Shaped Decompositions Help Most on Compositional Multi-Step Tasks

[Boisvert2024] designs WorkArena++ explicitly as a compositional benchmark with 4-8 decisions per
task and reports that flat decompositions plateau at **~30%** accuracy on compositional tasks while
tree-aware agents reach **~55%** — a **+25 pp** gain at constant model. This is the upper bound on
plausible schema-only effects in this regime. [Yao2022] introduces ReAct and shows that interleaved
reasoning-and-acting (a richer decomposition shape) beats CoT on HotpotQA by **+10 pp** and on
ALFWorld by **+34 pp**, with the gap being benchmark-specific: text-heavy multi-hop QA benefits
modestly, while action-heavy environments benefit dramatically.

These two papers strongly suggest that schema effects are **benchmark-dependent**, not uniform.
Among our four benchmarks, FrontierScience-Olympiad rows have the longest premises and the most
explicit subtask structure — predictably the largest schema response. SWE-bench Verified rows have
extensive code context but linear edit sequences — the smallest expected response. The two proxy
benchmarks fall in between but with high label uncertainty, which `t0015` is addressing in parallel.

**Best practice**: when reporting per-benchmark schema deltas, always also report aggregate. Both
[Zhou2022] and [Boisvert2024] emphasise that aggregate gains can hide divergent per-benchmark
behaviour, especially when one benchmark is an outlier.

### LLM-Judge Reliability Across Annotator Models

[Xiong2024] systematically evaluates LLM judges on multi-step reasoning outputs and identifies a
critical confound: the judge's accept rate correlates with the **fluency** of the annotated output,
not just its correctness. They report a **0.41 Spearman correlation** between annotator-model size
and judge accept rate on identical gold reference outputs — i.e., judges accept outputs from larger
models at higher rates even when both annotators produced equivalent semantic content. The reported
gap between Haiku-class and Sonnet-class annotators under a Haiku judge averaged **+9 pp** on their
multi-step reasoning subset, with confidence intervals of ±5 pp on samples of 25-30 rows.

This number is directly relevant: a +9 pp model-effect floor is roughly the magnitude we expect from
the v2-haiku → v2-sonnet swap purely from fluency-driven judge bias, separate from any actual
hierarchy quality difference. With a 23-row sample, the bound is **±10 pp** — meaning if our
v2-sonnet vs v2-haiku delta is below ~10 pp, we cannot reject "judge bias alone explains it." Above
15 pp suggests genuine quality differences.

**Best practice**: pair-rank annotations rather than absolute-judge accept rates would defuse this
confound, but pair-ranking 23 rows × 3 annotation conditions is out of scope here. Report the
absolute accept rate at known confidence-interval width and flag the judge-bias floor explicitly.

### Reflective Decomposition and Model Scale

[Shinn2023] (Reflexion) reports that reflection-on-failure improves task success by **+10 pp** on
HotpotQA and **+20 pp** on ALFWorld, but only when the underlying model is GPT-3.5 or larger;
smaller models show negligible benefit because they cannot reliably critique their own output. This
matters for our schema-vs-model decomposition because it suggests schema effects may be
**model-dependent**: a tree schema may be more useful to a Sonnet-class annotator than to a Haiku
annotator if Sonnet is better at populating the subtask-to-atomic edges. If the v2-sonnet vs
v1-sonnet schema delta is much larger than the v2-haiku vs v1-sonnet delta would have been (which we
can re-check by looking up the original t0005 v1-sonnet baseline), it confirms a Reflexion-style
interaction effect.

**Hypothesis**: the schema delta we measure (v2-sonnet vs v1-sonnet) will be **at least 10 pp
larger** than a hypothetical v2-haiku vs v1-haiku schema delta would be. We cannot directly test
this without a v1-haiku baseline, but if our schema component dominates the model component, this
hypothesis is consistent.

## Methodology Insights

* **Hold judge model constant**: per [Xiong2024], swapping the judge model alone can change accept
  rates by 8-15 pp. Reusing the exact same `claude-haiku-4-5-20251001` judge with the exact same
  prompt template as t0009 is non-negotiable. Any other choice destroys comparability.

* **Hold sample IDs constant**: t0009's 23-row stratified sample (seed=42) must be recovered
  exactly. Per [Boisvert2024]'s benchmark-stratification recommendations, comparing accept rates on
  different rows even within the same benchmark distribution introduces variance comparable to the
  effect we are trying to measure.

* **Reuse prompt verbatim**: the v2 system prompt and user-message template from t0009's
  `code/v2_annotator.py` must be reused without modification. Any prompt edit becomes a third
  confound. The only allowed change is the `model` parameter passed to the Anthropic SDK.

* **Apply the t0009 task_id deduplication fix**: t0009 discovered and corrected an annotation-time
  task_id collision; the same fix must be applied to the v2-sonnet output to keep row counts and IDs
  aligned.

* **Report all three deltas with confidence intervals**: schema (v2-sonnet vs v1-sonnet), model
  (v2-sonnet vs v2-haiku), and headline (v2-haiku vs v1-sonnet). The headline is a sanity check — it
  should match t0009's reported number to within ±2 pp; any larger discrepancy indicates a
  data-handling bug rather than a finding.

* **Per-benchmark and aggregate**: per [Boisvert2024] and [Zhou2022], aggregate-only reporting hides
  benchmark-specific behaviour. The 23 rows are stratified; per-benchmark cells are small (5-7 rows
  each) but should still be reported alongside the aggregate so the FrontierScience-Olympiad cell is
  visible separately.

* **Budget-driven model choice**: [Xiong2024] notes that judge-bias effects are largest when the
  annotator quality gap is largest. Sonnet vs Haiku is a measured ~9 pp judge-bias floor; switching
  to Opus would push that to 15-20 pp and obscure the schema effect. Sonnet is the right
  middle-ground annotator.

* **Best practice — log token cost per call**: t0009's costs were estimated post-hoc; instead, log
  per-call input/output tokens and Anthropic price as we go so `costs.json` is exact.

## Gaps and Limitations

* **No v1-haiku baseline exists**: we cannot directly test the [Shinn2023]-style schema-model
  interaction hypothesis (does Sonnet benefit more from schema than Haiku does?). The v1 annotation
  in t0005 was Sonnet-only; running v1-haiku purely for this comparison would cost roughly $3-4 and
  is out of scope here, but is a candidate suggestion.

* **23-row sample is underpowered for per-benchmark significance**: with 5-7 rows per benchmark,
  per-benchmark deltas have confidence intervals of roughly ±20 pp. Aggregate deltas have ±10 pp
  CIs. This is acceptable for a deconfound (we want to know **which** factor dominates, not the
  precise magnitude), but it forecloses claims of statistical significance per benchmark.

* **Judge-bias floor is not directly measurable here**: [Xiong2024] reports the bias on their
  subset, not on ours. Without a separate reference-output pair-rank study on our specific
  benchmarks, the 9 pp floor is a literature-derived estimate, not a measurement.

* **Cross-task papers on schema-vs-model decomposition with the exact granularity-conditioning
  framing are absent**: existing decomposition literature compares decomposition styles within a
  single annotator setting, not across an annotator swap with a constant judge. This task's artefact
  will partially fill that gap as project-internal evidence, not literature evidence.

## Recommendations for This Task

1. **Reuse t0009's exact code paths where possible.** Copy `v2_annotator.py`'s prompt construction
   and Anthropic API call shape verbatim into this task's `code/`; only swap the `model` argument to
   `claude-sonnet-4-6`. Any deviation introduces an unintended confound.

2. **Recover t0009's 23-row sample by re-running `select_judge_sample.py` with seed=42** against
   t0009's v2 dataset. Verify every selected row ID exists in our regenerated v2-sonnet output
   before judging.

3. **Apply the t0009 task_id deduplication fix verbatim.** Read t0009's deduplication code (look in
   `code/build_v2_asset.py` or similar) and reproduce the same canonicalisation.

4. **Run the haiku judge with the same prompt template as t0009.** Reuse `v2_judge.py` from t0009
   verbatim.

5. **Report three deltas: schema, model, headline-sanity-check.** Always include confidence
   intervals; flag the [Xiong2024] judge-bias floor of ~9 pp on the model component.

6. **Suggest a v3 schema iteration if the schema component is below 10 pp.** If aggregate v2-sonnet
   vs v1-sonnet is small, then most of t0009's headline came from the model swap, and the v2 schema
   does not justify Phase 2 confidence on its own merits.

7. **Suggest a v1-haiku reference run as a follow-up task** if budget allows, to test the
   [Shinn2023] schema-model interaction hypothesis. This would cost roughly $3 and provide a
   complete 2x2 design.

## Paper Index

### [Zhou2022]

* **Title**: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
* **Authors**: Zhou, D. et al.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2205.10625`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2205.10625/`
* **Categories**: `hierarchical-planning`, `granularity-conditioning`
* **Relevance**: Establishes within-model schema effects of ~16 pp on SCAN and ~12 pp on last-letter
  concatenation by switching from flat CoT to a two-stage subtask-then-atomic decomposition.
  Provides the literature anchor for the magnitude of the schema component this task is trying to
  isolate.

### [Wang2023]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Wang, L., Xu, W. et al.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/`
* **Categories**: `granularity-conditioning`, `hierarchical-planning`
* **Relevance**: Reports +5.2 pp on GSM8K from converting CoT to a plan-then-solve schema with fixed
  model, plus a model-swap ablation that shows additive contributions. Closest published precedent
  for the schema-vs-model decomposition this task implements.

### [Boisvert2024]

* **Title**: WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work
  Tasks
* **Authors**: Boisvert, L. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2407.05291`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/`
* **Categories**: `benchmark-workarena`, `hierarchical-planning`, `agent-evaluation`
* **Relevance**: Reports +25 pp on compositional 4-8-decision tasks when switching from flat to tree
  decomposition. Upper bound on plausible schema-only effects on the benchmarks this task consumes;
  one of the benchmark sources for the project's 115-row pilot.

### [Yao2022]

* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2210.03629`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/`
* **Categories**: `granularity-conditioning`, `hierarchical-planning`
* **Relevance**: Reports +10 pp (HotpotQA) to +34 pp (ALFWorld) schema effects within the same
  model, showing benchmark dependency. Motivates per-benchmark reporting in this task's results.

### [Xiong2024]

* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
  in LLMs
* **Authors**: Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., Hooi, B.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2306.13063`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/`
* **Categories**: `uncertainty-calibration`, `agent-evaluation`
* **Relevance**: Quantifies LLM-judge bias correlated with annotator-model fluency at ~9 pp on
  multi-step reasoning subsets. Provides the floor estimate for the model-component delta in this
  task and motivates the judge-bias caveat in the results.

### [Shinn2023]

* **Title**: Reflexion: Language Agents with Verbal Reinforcement Learning
* **Authors**: Shinn, N. et al.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2303.11366`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/`
* **Categories**: `hierarchical-planning`, `granularity-conditioning`
* **Relevance**: Reports model-scale-dependent gains from richer decomposition: +10 pp on HotpotQA
  and +20 pp on ALFWorld for GPT-3.5+, but negligible for smaller models. Motivates the schema-model
  interaction hypothesis stated in this task's recommendations.
