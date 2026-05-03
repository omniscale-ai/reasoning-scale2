# Category: Uncertainty Calibration

Confidence reporting, overconfident error analysis, and calibration of agent action
probabilities.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (2)](../papers/by-category/uncertainty-calibration.md) | [Answers
(1)](../answers/by-category/uncertainty-calibration.md) | [Suggestions
(17)](../suggestions/by-category/uncertainty-calibration.md) | [Libraries
(3)](../libraries/by-category/uncertainty-calibration.md) | [Predictions
(1)](../predictions/by-category/uncertainty-calibration.md)

---

## Papers (2)

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

## Tasks (2)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |
| 0017 | [Literature: Hierarchical Agents and LLM-as-Judge](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) | completed | 2026-05-01 01:40 |

## Answers (1)

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

## Suggestions (13 open, 4 closed)

<details>
<summary>🔧 <strong>Replace verbalized final_confidence with a content-driven
calibrator over v3 features</strong> (S-0027-01)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-05-03 | **Source**:
[t0027_phase2_5_abc_rerun_with_fixed_b_and_c](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/)

After the parser fix, plan_and_solve_v3 still has 10-bin ECE = 0.336 on the 130-paired set and
matched_mismatch_v2 over v3 has 0.374. Verbalized confidence remains roughly uniform across
actually-correct and actually-wrong trajectories. Train a post-hoc calibrator (temperature
scaling first, then isotonic regression as a stretch) over the four content features used in
t0022 (subset, plan_length, n_actions, judge_program_agreement_proxy) plus the new v3
telemetry fields (parse_attempts, recovery_path) and report ECE on a held-out slice of the
same 130-paired set. Compare against raw verbalized confidence and against a constant-rate
predictor.

</details>

<details>
<summary>🔧 <strong>Recalibrate variant B's verbalized final_confidence</strong>
(S-0026-03)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0026_phase2_abc_runtime_n147_for_rq1_rq5](../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/)

Variant B's 10-bin Expected Calibration Error is 0.43 (n=49) and the [0.9, 1.0] bin succeeds
at only 25%. Add a calibration head — temperature scaling, isotonic regression, or a learned
post-hoc calibrator over the four content features (subset, plan_length, n_actions,
judge_program_agreement_proxy) — and report ECE on a held-out slice of the same 130-instance
paired set.

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
<summary>📚 <strong>Add Expected Calibration Error (ECE) computation alongside
overconfident_error_rate</strong> (S-0011-01)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0011_metric2_calibration_aggregator](../../tasks/t0011_metric2_calibration_aggregator/)

Extend the metric2_calibration_aggregator_v1 library (or add a sibling library) with Expected
Calibration Error (ECE) computation using the standard 10-bucket binning and produce
per-bucket calibration plots. Xiong2024 reports ECE as the primary headline metric; the
current library reports only the binary overconfident_error_rate. Adding ECE gives Phase 2 a
richer calibration signal and lets t0012's results display the bucket where overconfidence
concentrates rather than just a single number. Should be a small follow-up: bucket each
CalibrationRecord by predicted_confidence, compute |accuracy - mean_confidence| within each
bucket, weight by bucket size. Output should be both a scalar ECE value and a list of
(bucket_lower, bucket_upper, accuracy, mean_confidence, count) tuples for plotting.

</details>

<details>
<summary>🧪 <strong>Add provider-specific calibration prompt variants for
instruction-tuned vs reasoning models</strong> (S-0011-02)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0011_metric2_calibration_aggregator](../../tasks/t0011_metric2_calibration_aggregator/)

The current ConfidencePromptTemplate uses a single Xiong2024 human-inspired prompt.
Reasoning-focused models (e.g., o-series, Claude 4.5+ thinking models) often produce a
chain-of-thought before stating confidence, which the current parser handles but which
Xiong2024's own results show can hurt calibration in some configurations. Build a small
library of named prompt variants (instruction_tuned, reasoning_with_cot, reasoning_no_cot) and
benchmark them on a held-out 50-problem set during Phase 2. Goal: identify which variant
minimizes overconfident_error_rate per provider and ship that as the default mapping in
t0012's experiment harness. Out of scope for this task per task_description.md but identified
as the obvious next sweep.

</details>

<details>
<summary>📊 <strong>Sweep HIGH_CONFIDENCE_THRESHOLD to find the operating point that
maximizes signal in t0012</strong> (S-0011-03)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0011_metric2_calibration_aggregator](../../tasks/t0011_metric2_calibration_aggregator/)

The current default HIGH_CONFIDENCE_THRESHOLD = 0.75 sits between the verbalized medium (0.5)
and high (0.9) numeric anchor points and matches Xiong2024's high-bucket boundary. The
threshold is exposed as a module constant for sweeps. After t0012 runs, sweep the threshold
over {0.5, 0.6, 0.7, 0.75, 0.8, 0.9} and report overconfident_error_rate at each operating
point. The best threshold for the project's hierarchical agents may differ from Xiong2024's QA
setting because the project judges actions at trajectory steps, not final answers. Output: a
small chart and a recommended threshold for downstream tasks.

</details>
