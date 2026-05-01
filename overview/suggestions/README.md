# Research Suggestions Backlog

67 suggestions **53 open** (13 high, 24 medium, 16 low), **14 closed**.

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

## High Priority

<details>
<summary>🧪 <strong>Add a uniform-random vs. adversarial vs. matched ablation to
t0012</strong> (S-0010-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../tasks/t0010_matched_mismatch_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

When t0012 runs the A-vs-B-vs-C harness, include three C-condition variants in addition to A
and B: matched_mismatch_v1 with mismatch_strategy='random' and seed=0, matched_mismatch_v1
with mismatch_strategy='adversarial', and a phase-randomised C control (random walk over the
v2 hierarchy with the correct tag). The three-way ablation decomposes the C-condition gap into
'phase order matters', 'any wrong tag matters', and 'most-distant wrong tag matters',
preventing the granularity-mismatch effect from being conflated with a step-order-mismatch
effect (see research_papers.md, Wang2023 and Zhou2022).

</details>

<details>
<summary>🔧 <strong>Adopt a haiku-default annotation policy for Phase 2: model swap
is not justified</strong> (S-0014-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-04` |
| **Kind** | technique |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

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
<summary>📊 <strong>Adopt Trust-or-Escalate selective evaluation for the multi-judge
agreement study</strong> (S-0017-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-01` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Source paper** | [`10.48550_arXiv.2407.18370`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2407.18370/) |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

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
<summary>📂 <strong>Hierarchical annotation v2: scale to >=200 rows with full human
review</strong> (S-0005-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

Extend the v1 pilot to >=200 rows by re-running the upstream pilot pipeline with a stricter
retry policy (eliminate the 11 FrontierScience-Olympiad rows where steps==null), then perform
a full human-rater review of every row. Compute inter-rater agreement (Krippendorff's alpha or
Cohen's kappa) between the human rater and the LLM annotator.

</details>

<details>
<summary>📂 <strong>Negotiate FrontierMath access via Epoch AI evaluation
pipeline</strong> (S-0002-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/) |

FrontierMath [Glazer2024] uses contamination-resistant unpublished problems hosted via Epoch
AI's evaluation pipeline; the raw problems are not publicly downloadable. The project needs an
explicit access conversation with Epoch AI, plus a fallback to public Olympiad benchmarks
(MATH-500, AIME) if access is denied or delayed. Schedule this as a planning task before Phase
1 to avoid blocking the FrontierScience-Olympiad slot of the composite benchmark.

</details>

<details>
<summary>🧪 <strong>Phase 2 A-vs-B-vs-C evaluation harness</strong> (S-0007-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../tasks/t0007_scope_unaware_planandsolve_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |

Build the experiment harness that runs all three libraries (scope_aware_react_v1,
scope_unaware_planandsolve_v1, and the planned matched-mismatch library) on a fixed benchmark
slice with a single shared LLM provider, recording trajectory_records.jsonl per condition and
computing the registered metrics task_success_rate, avg_decisions_per_task, and
overconfident_error_rate per condition. The harness must depend on this library only via the
trajectory schema, never via internal helpers, to preserve isolation.

</details>

<details>
<summary>📂 <strong>Provision a ServiceNow developer instance for WorkArena++ live
evaluation</strong> (S-0003-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-02` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-workarena`](../../meta/categories/benchmark-workarena/) |

WorkArena++ instance enumeration requires a live ServiceNow developer instance plus access to
the gated `ServiceNow/WorkArena-Instances` HuggingFace dataset. This task captures only the
upstream task-class manifest. Provision a free ServiceNow developer instance, request HF
access, install browsergym-workarena, and produce an instance-level subset filtered to 4-8
decisions per task. Until then, the Mind2Web pilot proxy is frozen as the de-facto Phase 2
fallback.

</details>

<details>
<summary>🧪 <strong>Re-judge the remaining 8 v1 paired rows to tighten the
pure-schema CI</strong> (S-0020-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

The pure-schema delta CI (+22.5 to +77.5 pp) is dominated by the v1 sample size (n=12) because
t0005 only judged 12 of the 20 paired rows in its subsampled pool. Re-running the t0005 v1
judge on the remaining 8 paired indices (rows that t0014 judged but t0005 did not) would
extend v1 from n=12 to n=20 with no new annotation calls and tighten the pure-schema CI from a
half-width of ~28 pp to ~14 pp. Cost is ~8 haiku judge calls (~$0.50). This is the cheapest
possible follow-up that materially improves statistical power.

</details>

<details>
<summary>🧪 <strong>Rotate the judge model to test the haiku-vs-haiku familial bias
hypothesis on the model-only delta</strong> (S-0014-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

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
<summary>🧪 <strong>Run t0023's confirmatory ABC re-run with N>=157 using
abc_harness_metrics</strong> (S-0022-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

The whole purpose of t0022 is to make t0023's confirmatory N>=157 ABC re-run produce signal at
the floor where binary task success failed in t0012. Schedule t0023 to consume
abc_harness_metrics: import score_trajectory, log per-trajectory progress_rate and per-step
error labels into the existing harness output, and report progress-rate means and
error-distribution mixtures per ABC condition with bootstrap CIs. Reuse the cached judge
responses from t0022 to keep marginal cost low. This is the direct downstream consumer this
task was built for.

</details>

<details>
<summary>📚 <strong>Set up ServiceNow + BrowserGym harness shared by WorkArena and
WorkArena++</strong> (S-0002-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-03` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-workarena`](../../meta/categories/benchmark-workarena/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Both WorkArena [Drouin2024] and WorkArena++ [Boisvert2024] require a self-hosted ServiceNow
developer instance and the BrowserGym Python harness. This is a substantial infrastructure
task with credentials, container orchestration, and end-to-end smoke tests. Schedule it before
any task that needs WorkArena or WorkArena++ data so the harness is ready when Phase 1
annotation begins.

</details>

<details>
<summary>📊 <strong>Tighten FrontierScience-Olympiad subgoal lists by hand on a
5-task pilot before t0023</strong> (S-0022-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Current FrontierScience-Olympiad subgoals are derived mechanically from SUBTASK lines in t0012
gold answers (mean 4.6 per environment). On the 89-row replay, 73 of 89 trajectories scored
0.0 progress rate, suggesting the subgoals may be too coarse to register intermediate
progress. Hand-review subgoals for 5 randomly chosen environments, refining them into 3-5
verifiable intermediate states each (e.g., "derived intermediate equation X", "identified
relevant principle Y"). If hand-tightening doubles the non-zero rate, roll the recipe out to
all 26 environments before t0023 ships. Cheap and high-leverage for t0023 signal quality.

</details>

<details>
<summary>🧪 <strong>Use hierarchical-annotation-v1 to seed Phase 2 scope-conditioning
experiments</strong> (S-0005-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The dataset asset is now ready for downstream consumption. Plan a baseline-evaluation task
that uses the 102 hierarchy-complete rows to compare scope-conditioned vs scope-unaware agent
prompts (B vs G/S/A from the project's research questions).

</details>

## Medium Priority

<details>
<summary>🔧 <strong>Add a gold_actions structural-mirror validator for non-empty
global_atomics</strong> (S-0009-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-02` |
| **Kind** | technique |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/) |

The two needs-revision rows on FrontierScience-Olympiad both failed for the same reason: the
annotator emitted hierarchy.global_atomics correctly but produced gold_actions.global_atomics
empty or merged into a subtask. This is a structural-mirror inconsistency, not a content
error. Add a post-parse validator to v2_annotator.py that detects this pattern, re-prompts the
model on just the gold_actions block (or rejects the row to the parse-failure bucket), and
logs the rate. This should bring the FrontierScience-Olympiad accept rate from 67% to ~100%
with zero additional model cost on the happy path.

</details>

<details>
<summary>📚 <strong>Add Expected Calibration Error (ECE) computation alongside
overconfident_error_rate</strong> (S-0011-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |

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
<summary>📊 <strong>Add finer-grained SWE-bench subgoals at the line-range and
AST-node level</strong> (S-0022-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-swebench`](../../meta/categories/benchmark-swebench/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Current SWE-bench Verified Lite subgoals are file-level ("agent edit touches the same file as
a gold patch hunk"). This is a permissive subgoal that may not differentiate scope-aware from
scope-unaware agent behaviour as sharply as line-range or AST-node level subgoals would.
Implement a second subgoals JSON file with per-hunk line ranges parsed from the gold patch,
and a small AST-node helper that maps line ranges to the enclosing function/class. Compare
progress-rate distributions on the t0012 sample (or a fresh small SWE-bench eval) between the
two granularities. Useful Metric 1 calibration step independent of t0023.

</details>

<details>
<summary>📚 <strong>Build benchmark-specific tool registries for the four roadmap
benchmarks</strong> (S-0006-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/), [`benchmark-workarena`](../../meta/categories/benchmark-workarena/), [`benchmark-swebench`](../../meta/categories/benchmark-swebench/), [`benchmark-taubench`](../../meta/categories/benchmark-taubench/) |

scope_aware_react_v1 accepts an arbitrary tool_registry but ships none. Phase 2 needs
registries for FrontierScience-Olympiad (calculator, search, paper lookup), WorkArena++
(browser, form filler, table lookup), SWE-bench Verified (file read, file write, run tests,
git diff), and tau-bench (DB query, API call, customer-action stubs). Each should be its own
write-library task that imports scope_aware_react_v1 and registers a registry with consistent
naming conventions.

</details>

<details>
<summary>📂 <strong>Build the SWE-bench Verified Docker harness</strong> (S-0002-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-05` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`no-doi_OpenAI2024_swe-bench-verified`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/no-doi_OpenAI2024_swe-bench-verified/) |
| **Categories** | [`benchmark-swebench`](../../meta/categories/benchmark-swebench/) |

SWE-bench Verified [OpenAI2024] is the canonical atomic-execution slot in the four-source
composite. Its evaluation harness uses Docker per repository to isolate test runs. This task
would download the Verified problem set, pull the Docker images, and run a 10-instance smoke
test to confirm the harness reproduces published baseline numbers (e.g., one of the early
Claude or GPT scores).

</details>

<details>
<summary>🧪 <strong>Derive step graphs for FrontierScience-Olympiad rows</strong>
(S-0003-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

FrontierScience-Olympiad pilot rows currently lack per-instance step graphs because Olympiad
solutions are graded as final answers. Run a hierarchical-annotation task that decomposes each
problem into global / subtask / atomic steps with gold actions at each level, so Phase 2 can
apply the canonical 4-8 decisions filter consistently across all four benchmarks.

</details>

<details>
<summary>📂 <strong>Expand the v2 dataset from 115 rows to >=200 rows by sampling
additional benchmark instances</strong> (S-0009-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-05` |
| **Kind** | dataset |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The Phase 1 success criterion is >=100 annotated tasks per condition; v2 is at 115 which is
just over the threshold. The downstream Phase 2 experiments need stratification by difficulty
AND by benchmark, which becomes statistically thin at 5-6 rows per stratum. Expand to >=200
rows by sampling 20-25 additional rows from each of the four benchmarks (especially the
smaller ones: SWE-bench Verified, tau-bench). Re-use v2_annotator.py at the same haiku-CLI
rate, ~$5-6 added cost. Inherits S-0005-01.

</details>

<details>
<summary>📂 <strong>Fix task_id collision in FrontierScience-Olympiad pilot
dataset</strong> (S-0012-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-04` |
| **Kind** | dataset |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |

The hierarchical-annotation-v2 FrontierScience-Olympiad subset has 40 rows but only 26 unique
task_ids. Multiple rows share the same task_id (different granularity levels of the same
problem), which means the pairing logic treats them as separate predictions for the same task.
A deduplication or re-keying correction task should produce a version of the dataset with
unique task_ids per row, or document the intended semantics of multi-row task_ids.

</details>

<details>
<summary>📊 <strong>Measure the missing-tag fallback rate against real LLMs</strong>
(S-0006-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The library defaults to atomic when the model omits a granularity tag and emits a
tag_missing_defaulted_to_atomic warning observation. The deterministic tests cover the parser
path but the fallback rate against real LLMs (GPT-4o, Claude 3.7 Sonnet, Llama-3.1-70B) is
unknown. Build an evaluation task that runs each library at each granularity over N=20
problems per benchmark and reports the fallback rate alongside task success.

</details>

<details>
<summary>📂 <strong>Negotiate Epoch AI access for full FrontierMath
benchmark</strong> (S-0003-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/) |

FrontierMath (Glazer et al. 2024) is the closest publicly named analogue to
FrontierScience-Olympiad and is gated behind Epoch AI access. The current dataset asset uses
40 pilot rows as the v0 subset. Open a conversation with Epoch AI to obtain bona-fide research
access; if access is denied or delayed, add MATH-500 / AIME as a public Olympiad fallback per
the t0002 fallback plan.

</details>

<details>
<summary>📚 <strong>Per-step strategy override for matched_mismatch_v1</strong>
(S-0010-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |

Extend matched_mismatch_v1 with a per-step strategy override so callers can inject targeted
mismatches in specific phases (e.g., wrong-tag only at the global level; correct everywhere
else). This decomposes the C-condition gap by phase kind and supports follow-up analysis on
which structural slots are most sensitive to tag mismatch. Should be additive: the existing
uniform-strategy API stays the default. Keep the trajectory schema unchanged; the override is
constructor-side only.

</details>

<details>
<summary>🔧 <strong>Reconcile WorkArena++ flat-action sequences with the three-level
schema</strong> (S-0005-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-03` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-workarena`](../../meta/categories/benchmark-workarena/) |

The judge rejected all three WorkArena++ rows because the upstream annotation lacks
`conceptual` nodes, causing the mapper to emit empty subtask lists. Investigate whether the
WorkArena++ source carries an implicit subtask boundary (e.g., screen transitions) that can be
detected automatically, or alternatively change the v2 schema to accept flat atomic-only rows
as a distinct hierarchy_kind. Document the chosen approach and update the mapper.

</details>

<details>
<summary>📊 <strong>Register pass^k as a project metric for reliability
reporting</strong> (S-0002-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2406.12045`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2406.12045/) |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`benchmark-taubench`](../../meta/categories/benchmark-taubench/) |

tau-bench [Yao2024] introduces pass^k, a metric that measures whether an agent succeeds across
k independent rollouts. The 25-percentage-point gap between pass@1 and pass^8 in retail
demonstrates that single-rollout pass@1 systematically overstates agent reliability. The
project should register a pass_at_k metric (with k=1, 8) under meta/metrics/ to complement
task_success_rate. This enables Phase 4 paper-ready claims to be robust to single-rollout
luck.

</details>

<details>
<summary>📂 <strong>Remediate proxy benchmark naming and task_id
non-uniqueness</strong> (S-0005-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/) |

The pilot file uses tau-bench and WorkArena++ as proxies but task_id prefixes are still `he_*`
(HumanEval) and `m2w_*` (Mind2Web) from earlier drafts; additionally 14 of 115 task_ids are
duplicated. Re-key the source data with synthetic per-row UUIDs and align task_id prefixes
with the actual benchmark slugs (`tau_*`, `wa_*`).

</details>

<details>
<summary>📂 <strong>Replace Mind2Web/HumanEval proxy rows with native WorkArena++
and tau-bench data</strong> (S-0015-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0015_correct_proxy_benchmark_labels`](../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

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
<summary>📊 <strong>Run a single-blind human review pass on the 115 v2 rows and
report human-vs-judge agreement (Cohen's kappa)</strong> (S-0009-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

v2 is judged only by a single LLM call per row. The dataset is 'LLM-judge-acceptable' but not
'human-validated'. To upgrade to v3, recruit 1-2 human annotators to review the same 23-row
stratified sample (or all 115 rows for higher precision) and emit acceptable/needs-revision
verdicts. Compute Cohen's kappa between human and the haiku judge to estimate how much of the
+58% v2-vs-v1 aggregate gain is real quality vs judge-LLM agreement-with-itself. Budget
estimate: 4-6 hours of human review time at $50/hour = $200-300.

</details>

<details>
<summary>🧪 <strong>Scale the truncated-v2 condition to n=80 to detect a true +5 pp
pure-text effect if it exists</strong> (S-0020-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

The pure-text delta on this run is +5 pp with a CI of [-15, +26] pp at n=20. To resolve
whether the true pure-text effect is zero, +5 pp, or larger, the experiment needs n>=80 per
condition (Newcombe-Wilson half-width drops to ~10 pp at n=80 vs ~20 pp at n=20). This
requires running the v2 annotator and judge on 60 additional matched rows from the same
hierarchical-annotation-v1 source dataset, with both truncated and full conditions. Estimated
cost: 60 haiku annotations + 120 haiku judge verdicts at ~$0.07/call = ~$13. The result would
either confirm the schema-dominance claim with tight bounds or upgrade pure-text to a
meaningful contributor.

</details>

<details>
<summary>📊 <strong>Schema-parity dedup task between t0006 and t0007</strong>
(S-0007-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |

After t0006 (scope_aware_react_v1) merges, run a small deduplication-style task that imports
both libraries' TRAJECTORY_RECORD_FIELDS tuples and asserts they are identical, plus a smoke
test that runs both libraries on the same toy problem and verifies the trajectory JSON shapes
round-trip through a single Pydantic loader. If they diverge, file a correction in the
later-merged task. This is the cheapest insurance against silent schema drift.

</details>

<details>
<summary>🧪 <strong>Scope a v3 schema iteration motivated by per-benchmark
schema-only deltas, not aggregate</strong> (S-0014-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/) |

The aggregate schema-only delta is +57 pp (90% v2-sonnet vs 33% v1-sonnet) but the
per-benchmark split is bimodal: FrontierScience-Olympiad and WorkArena++ are at +100 pp (0% ->
100%), while SWE-bench Verified and tau-bench are at +13-17 pp (67% -> 80-83%). The +100 pp
cells suggest the v2 tree schema converts unsolvable v1 outputs into acceptable v2 outputs,
but this is potentially confounded with the truncation fix bundled into v2 (S-0009-04). The
+13-17 pp cells suggest a real but modest schema improvement on benchmarks where v1 was
already adequate. A v3 schema should target SWE/tau-style structured-action tasks specifically
— e.g., add explicit precondition/postcondition fields to atomics, since the SWE/tau cells
already saturate the high-level subtask abstraction.

</details>

<details>
<summary>📊 <strong>Sensitivity-check the SWE-bench Verified 4-8-hunks subset against
[3, 12]</strong> (S-0003-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`no-doi_OpenAI2024_swe-bench-verified`](../../tasks/t0003_download_benchmark_subsets/assets/paper/no-doi_OpenAI2024_swe-bench-verified/) |
| **Categories** | [`benchmark-swebench`](../../meta/categories/benchmark-swebench/) |

The current SWE-bench Verified subset filters to 60 instances with exactly 4-8 patch hunks.
The full 500 Verified instances have hunks ranging from 1 to 45. Run a sensitivity check by
re-filtering with windows [3, 12] and [2, 16] and comparing the difficulty / repo
distributions; this informs whether the 4-8 boundary is too narrow for Phase 2's atomic-edit
experiments.

</details>

<details>
<summary>📊 <strong>Sonnet judge rerun on the v2-tree-truncated condition to confirm
schema effect is not haiku-specific</strong> (S-0020-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

All three conditions in t0020 use a haiku judge for fairness, but this means the result is
haiku-judge accept rates rather than ground-truth quality. A sonnet rerun on the
v2-tree-truncated annotations (existing 20 rows, no new annotator calls) would confirm whether
the +57 pp pure-schema effect is robust to a stronger judge or whether it shrinks. t0014
already showed sonnet times out on some rows, so the rerun should set max_turns conservatively
and accept timeouts as null verdicts rather than retries. Estimated cost ~$3-5 sonnet judge.

</details>

<details>
<summary>📊 <strong>Spot-check Haiku judge calls against Sonnet on a 20-step
stratified sample</strong> (S-0022-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Both progress_rate and error_taxonomy judge calls default to claude-haiku-4-5 to keep t0023
cost bounded. Risk: haiku miscalibration could produce systematic bias on the error taxonomy
(e.g., over-classifying steps as "ok"). Build a small re-grading script that picks 20 steps
stratified by (condition, predicted label) and re-classifies them with claude-sonnet. Report
agreement rate per label. If overall agreement < 70% or any label has < 50% agreement,
escalate to sonnet for the headline t0023 numbers and document in t0023's Limitations.

</details>

<details>
<summary>📚 <strong>Tighten budget-guard wrapper to skip-write fallback responses
to disk cache</strong> (S-0022-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-01` |
| **Kind** | library |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

When the budget guard returns a deterministic fallback ("no" for progress rate, "ok" for error
taxonomy), the current wrapper still calls cache_put on the response. As a result the disk
cache for t0022 grew to 2592 entries, ~80% of which are fallback strings rather than real
judge responses. Add a flag to judge_cache.cache_put that lets the budget-guarded wrapper
skip-write fallback values; this keeps the cache useful for t0023 instead of polluting it.
Trivially small change in code/judge_cache.py and code/replay_t0012.py; covers a real risk for
the t0023 confirmatory ABC re-run.

</details>

<details>
<summary>🔧 <strong>Use SELF-DISCOVER reasoning scaffolds as the scope-aware (A)
condition prompt template</strong> (S-0017-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-03` |
| **Kind** | technique |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Source paper** | [`10.48550_arXiv.2402.03620`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.03620/) |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

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

## Low Priority

<details>
<summary>📊 <strong>Add a row-level original_benchmark provenance field to future
relabel corrections</strong> (S-0015-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0015_correct_proxy_benchmark_labels`](../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/) |

The t0015 overlay rewrites the per-row benchmark string but does not preserve the original
proxy label inside the row. A reader inspecting only the effective JSONL cannot tell that the
row was previously labeled differently — provenance lives only in the corrections overlay's
description.md. For future relabel corrections, the framework would benefit from a soft
convention where the corrected row carries an original_benchmark field (or, more generally,
original_<field> for any field rewritten by a corrections overlay). This makes per-row
provenance auditable without round-tripping through the corrections file. The task should: (1)
propose the convention as a small extension to the corrections specification, (2) update the
dataset-asset verificator to surface a warning when an overlay rewrites a per-row field
without preserving the original, and (3) backfill the convention into the t0015 overlay.

</details>

<details>
<summary>📚 <strong>Add a write-library task for shared dataset-asset
writers</strong> (S-0003-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-05` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | — |
| **Categories** | — |

This task wrote the `code/dataset_asset.py` helper inline, but the same DatasetDetails /
write_dataset_asset helpers will be needed by every future download-dataset task. Promote this
code to a registered library asset (under a future task) so subsequent tasks can import the
helpers via `assets/library/` rather than re-implementing them.

</details>

<details>
<summary>📚 <strong>Add an async ScopeAwareReactAgent variant for streaming and
parallel tool calls</strong> (S-0006-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The current agent is synchronous. Phase 2 experiments at scale will benefit from streaming
model output and from issuing multiple independent tool calls concurrently within a single
Thought block. Build async_scope_aware_react.py exposing AsyncScopeAwareReactAgent with an
async model_call signature and asyncio.gather over Action lists. Tests should use
AsyncScriptedModel mirroring the sync helper.

</details>

<details>
<summary>🧪 <strong>Add provider-specific calibration prompt variants for
instruction-tuned vs reasoning models</strong> (S-0011-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |

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
<summary>🧪 <strong>Add tool use (search, code execution) to the smoke harness for
FrontierScience-Olympiad</strong> (S-0012-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/) |

The smoke ran with calculator+finish only. FrontierScience-Olympiad requires multi-step
numerical computation, retrieval, and code execution for most problems. Adding a Python code
execution tool and a retrieval tool would lift accuracy above the current floor and make
A-vs-B-vs-C differences observable even on haiku. Cost per row would increase by ~2-5x but
confirmatory N would decrease proportionally.

</details>

<details>
<summary>📊 <strong>Cost-quality Pareto chart across t0009/t0014/t0020 to inform
downstream task budgets</strong> (S-0020-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/) |

Three conditions now exist on the same 20-row pool: v1-flat-truncated (cheap, low quality),
v2-tree-truncated (cheap, high quality), v2-tree-full (expensive, slightly higher quality). A
Pareto chart with cost-per-row on the x-axis and accept rate on the y-axis would crisply
communicate that v2-tree-truncated is on the Pareto frontier and v2-tree-full is dominated by
it once the +5 pp gain is weighed against the ~2x cost. Useful as input to the t0022 ABC
harness budget planning.

</details>

<details>
<summary>🧪 <strong>Defer Reflexion-style episodic memory to a Phase 3
ablation</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2303.11366`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/) |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

Reflexion [Shinn2023] adds verbal self-reflection across trials and reaches 91% pass@1 on
HumanEval vs. 80% for vanilla GPT-4. Including episodic memory in Phase 2 would conflate scope
conditioning with cross-trial memory. Schedule a dedicated Phase 3 ablation that tests whether
Reflexion-style memory adds further gains on top of the scope-aware (A) condition established
in Phase 2.

</details>

<details>
<summary>🔧 <strong>Extend the library to support a granularity that varies within
a single run</strong> (S-0006-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-05` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

Currently ScopeAwareReactAgent takes one fixed granularity for an entire run. A natural
extension is to let the agent emit a granularity transition (e.g., start global, drop to
subtask once a plan is established, drop to atomic during execution). Add a model-driven mode
where the parser also accepts <transition_to:subtask> markers and the agent updates the active
granularity per turn. This is a research extension worth Phase 2 ablation.

</details>

<details>
<summary>📊 <strong>Multi-judge disagreement study on hierarchical
annotation</strong> (S-0005-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Run the same 12-row spot-check with two judge models (claude-haiku-4-5 + claude-sonnet-4-6)
and compute pairwise verdict agreement plus a confusion matrix. The v1 single-judge accept
rate of 33% may be miscalibrated; multi-judge agreement gives a more reliable quality
estimate. Estimated cost: ~$0.30 per run.

</details>

<details>
<summary>🧪 <strong>Multi-provider replication: run Phase 2 harness with GPT-4o and
Gemini 1.5 Pro</strong> (S-0012-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The smoke used only claude-haiku-4-5. Replicating on GPT-4o and Gemini 1.5 Pro (both now
available via project API keys) would test whether the granularity conditioning effect is
model-specific or generalizes across providers. The harness's model_call.py abstraction layer
makes this a configuration change rather than a code change. Defer until the confirmatory N
result is available from S-0012-02 to avoid spending budget before the primary hypothesis is
tested.

</details>

<details>
<summary>📊 <strong>Re-download Wang2023 PDF and verify the verbatim PS+ prompt
text</strong> (S-0007-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../tasks/t0007_scope_unaware_planandsolve_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

The PS+ instruction string in scope_unaware_planandsolve_v1 was sourced through the t0002
paper summary, which was itself grounded only in the abstract because the PDF download failed
in t0002. A small download-paper task should re-attempt the download against arXiv:2305.04091
and verify that the prompt text in code/planandsolve.py matches the published version
verbatim. If it diverges, file a correction.

</details>

<details>
<summary>📚 <strong>Re-fetch the 11 paper PDFs with git LFS enabled</strong>
(S-0002-09)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-09` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | — |
| **Categories** | — |

All 11 paper assets in t0002 have download_status: failed because PDF download was deferred to
a future task that enables git LFS. Once LFS is configured, run a download-paper task per
asset that fetches the PDF (or markdown conversion) into the asset's files/ directory and
updates download_status to success. This will let later tasks (especially compare-literature)
cite specific page numbers and tables from the source PDFs.

</details>

<details>
<summary>🧪 <strong>Re-run the three FrontierScience-Olympiad sonnet timeouts under a
longer CLI timeout to recover the missing rows</strong> (S-0014-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/) |

Three FrontierScience-Olympiad rows (pilot indices 7, 8, 14) timed out at the 300s Claude Code
CLI ceiling during the sonnet annotation pass. They were dropped from the judge sample,
reducing FS sample size from 6 (t0009 v2-haiku) to 3 (t0014 v2-sonnet). The +33 pp model-only
delta on FS (67% v2-haiku vs 100% v2-sonnet, n=6 vs n=3) is therefore on a smaller sample than
the other benchmarks. Re-run those three rows with a 600s or 900s CLI timeout (or via direct
Anthropic API which has no per-call wall-clock cap) and re-judge. If all three pass, FS
aggregate v2-sonnet stays at 100% on n=6 and the +33 pp model-only delta becomes more
credible. Cost <$1.

</details>

<details>
<summary>📊 <strong>Resolve the subtask-adversarial ambiguity with empirical
evidence</strong> (S-0010-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

ADVERSARIAL_MAP currently pins 'subtask -> atomic' because subtask is equidistant from global
and atomic. Run a small ablation in t0012 with both 'subtask -> atomic' and 'subtask ->
global' adversarial maps and report the per-step contribution. If the two choices differ
materially, document the chosen direction and the empirical justification in
matched_mismatch_v1's description.md. If they do not differ, lock the current choice and
remove the ambiguity note.

</details>

<details>
<summary>📊 <strong>Sweep HIGH_CONFIDENCE_THRESHOLD to find the operating point that
maximizes signal in t0012</strong> (S-0011-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |

The current default HIGH_CONFIDENCE_THRESHOLD = 0.75 sits between the verbalized medium (0.5)
and high (0.9) numeric anchor points and matches Xiong2024's high-bucket boundary. The
threshold is exposed as a module constant for sweeps. After t0012 runs, sweep the threshold
over {0.5, 0.6, 0.7, 0.75, 0.8, 0.9} and report overconfident_error_rate at each operating
point. The best threshold for the project's hierarchical agents may differ from Xiong2024's QA
setting because the project judges actions at trajectory steps, not final answers. Output: a
small chart and a recommended threshold for downstream tasks.

</details>

<details>
<summary>🧪 <strong>Truncation-budget sweep to map the marginal value of additional
context</strong> (S-0020-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`benchmark-swebench`](../../meta/categories/benchmark-swebench/) |

t0020 shows 1500 chars is sufficient on 3 of 4 benchmarks but loses ~17 pp on SWE-bench
Verified. A finer truncation grid (500 / 1000 / 1500 / 2500 / 5000 / full) on a
SWE-bench-heavy pool would map where the marginal value of additional context drops to zero.
This is a single-condition sweep (v2 schema held constant; only the truncation budget varies)
so the cost scales linearly with the number of budget points. Estimated cost: 6 budgets x 20
SWE-bench rows x 2 calls per row x ~$0.07 = ~$17.

</details>

## Closed

<details>
<summary>✅ <s>Add an ablation: tree-schema-with-truncated-text to isolate the
truncation fix from the schema upgrade</s> — covered by <a
href="../../tasks/t0020_v2_truncation_vs_schema_ablation/"><code>t0020_v2_truncation_vs_schema_ablation</code></a>
(S-0009-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../tasks/t0009_hierarchical_annotation_v2/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |

v2 changed two things at once: schema (flat -> tree) and text completeness (truncated 1500
chars -> full). On FrontierScience-Olympiad and WorkArena++ the +67% and +100% deltas could be
entirely from the truncation fix (Xiong2024's prediction) or entirely from the schema upgrade.
Run a third condition: the v2 tree schema but truncate the problem to 1500 chars in both the
annotator and judge prompts. If accept rate drops materially below v2-full-text on
FrontierScience-Olympiad, truncation is the dominant cause; if it stays at v2-full-text
levels, the schema is the dominant cause. Cost ~$2 with haiku.

</details>

<details>
<summary>✅ <s>Adopt AgentBoard progress-rate metric and EAI error taxonomy in the
next ABC-condition run</s> — covered by <a
href="../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/"><code>t0022_abc_harness_progress_rate_and_error_taxonomy</code></a>
(S-0017-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Source paper** | [`10.48550_arXiv.2401.13178`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2401.13178/) |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/) |

t0012's smoke showed that all three ABC conditions hit the floor on FrontierScience-Olympiad
with claude-haiku-4-5 (A: 2.5%, B: 0%, C: 0%), so binary task success cannot distinguish the
conditions. Ma2024 (AgentBoard, NeurIPS 2024 D&B) defines a subgoal-coverage "progress rate"
with Pearson rho > 0.95 against humans across 1013 environments; Li2024 (Embodied Agent
Interface, NeurIPS 2024) defines a fine-grained error taxonomy (hallucination, affordance,
missing/extra/wrong-order steps, precondition/effect errors) that attributes failures to
specific modes. Adopt both: progress rate becomes a stronger Metric 1 candidate than binary
success, and the EAI taxonomy becomes the per-row diagnostic when scope-aware (A) and
scope-mismatched (C) conditions diverge. This is a precondition for S-0012-02 (sonnet
confirmatory run) producing legible results. Estimated effort: 1-2 days of
metric-implementation work.

</details>

<details>
<summary>✅ <s>Confirmatory Phase 2 run: sonnet on SWE-bench Verified or
tau-bench</s> — covered by <a
href="../../tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/"><code>t0023_phase2_abc_confirmatory_sonnet_swebench</code></a>
(S-0012-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`benchmark-swebench`](../../meta/categories/benchmark-swebench/) |

The smoke shows FrontierScience-Olympiad is beyond haiku capacity without tools (A: 2.5%, B:
0%, C: 0%). All three conditions are at the floor, making granularity conditioning effects
invisible. A confirmatory run requires: (1) a benchmark where the model can achieve 10-50%
accuracy without tools (SWE-bench Verified lite or tau-bench at the instance level), (2)
claude-sonnet-4-6 instead of haiku, (3) N≥157 paired rows per the confirmatory-N estimate from
this smoke. This is the highest-priority next experiment for RQ1/RQ5.

</details>

<details>
<summary>✅ <s>Extend scope_unaware_planandsolve_v1 to emit final_confidence</s> —
covered by <a
href="../../tasks/t0021_plan_and_solve_v2_with_final_confidence/"><code>t0021_plan_and_solve_v2_with_final_confidence</code></a>
(S-0012-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-01` |
| **Kind** | library |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The t0007 Plan-and-Solve library does not emit a final_confidence field in trajectory records.
This collapses Metric 2 (overconfident_error_rate) to 0.0 for conditions B and C, making RQ2
untestable. Extend the library to emit a verbalized confidence label per the Xiong2024 §3.2
protocol: add a follow-up call after the final plan step asking the model to rate its
confidence on a 0-1 scale. This is a prerequisite for any confirmatory A-vs-B-vs-C run that
wants to test RQ2.

</details>

<details>
<summary>✅ <s>Implement matched-mismatch (C) library on top of
scope_unaware_planandsolve_v1</s> — covered by <a
href="../../tasks/t0010_matched_mismatch_library/"><code>t0010_matched_mismatch_library</code></a>
(S-0007-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Create a third agent library that wraps scope_unaware_planandsolve_v1 (or
scope_aware_react_v1) with a tag-classifier that retroactively labels each step's granularity,
producing the matched-mismatch (C) condition for the project's A-vs-B-vs-C comparison. Reuse
this task's TRAJECTORY_RECORD_FIELDS export so all three libraries share the same trajectory
schema. The classifier should be a small fine-tuned model or heuristic so the task is
local-only and deterministic.

</details>

<details>
<summary>✅ <s>Implement Plan-and-Solve as the canonical scope-unaware (B)
baseline</s> — covered by <a
href="../../tasks/t0007_scope_unaware_planandsolve_library/"><code>t0007_scope_unaware_planandsolve_library</code></a>
(S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

Plan-and-Solve [Wang2023] is the strongest published prompt-only baseline that does not
condition on explicit granularity tags. The project should reuse LangChain's Plan-and-Execute
implementation rather than reimplementing from scratch. This task would adapt the LangChain
implementation to the project's task harness, log both stages (plan and solve) separately, and
produce a 10-instance validation run on the composite benchmark to confirm the baseline beats
vanilla Zero-shot-CoT.

</details>

<details>
<summary>✅ <s>Implement scope-aware (A) as ReAct extended with explicit granularity
tags</s> — covered by <a
href="../../tasks/t0006_scope_aware_react_library/"><code>t0006_scope_aware_react_library</code></a>
(S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2210.03629`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/) |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

The scope-aware (A) condition can be implemented as ReAct [Yao2022] extended with a per-token
granularity tag from the set {global, subtask, atomic}. This task would specify the prompt
template per granularity, the tagging logic that decides which granularity is active at each
LLM call, and a logging schema that records the active granularity for every action so
post-hoc per-granularity analysis is possible. Replicate Least-to-Most's solution-reuse
pattern [Zhou2022] inside the implementation.

</details>

<details>
<summary>✅ <s>Implement verbalized-confidence + 3-sample self-consistency aggregator
for Metric 2</s> — covered by <a
href="../../tasks/t0011_metric2_calibration_aggregator/"><code>t0011_metric2_calibration_aggregator</code></a>
(S-0002-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Xiong2024 establishes that single-sample verbalized confidence is poorly calibrated and that
3-sample self-consistency aggregation reduces ECE by 2-8 points. The project should commit to
this protocol for Metric 2 (overconfident error rate). This task would specify the
human-inspired confidence prompt template (low/medium/high + brief justification), implement
the self-consistency aggregator, and validate calibration on a small held-out set before Phase
2 launches.

</details>

<details>
<summary>✅ <s>Re-run LLM-as-judge with full problem text (no truncation)</s> —
covered by <a
href="../../tasks/t0009_hierarchical_annotation_v2/"><code>t0009_hierarchical_annotation_v2</code></a>
(S-0005-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/) |

The v1 judge sees only the first 1500 chars of each problem. Three of four needs-revision
verdicts on FrontierScience-Olympiad rows complain about content not present in the truncated
excerpt. Re-run the audit using the full problem text (or a structured per-section summary)
and compare accept rates. Predict an absolute accept-rate increase of >=15 percentage points
on FrontierScience-Olympiad.

</details>

<details>
<summary>✅ <s>Re-run v2 annotator with claude-sonnet-4-6 via direct API to
disentangle schema vs model effect</s> — covered by <a
href="../../tasks/t0014_v2_annotator_sonnet_rerun/"><code>t0014_v2_annotator_sonnet_rerun</code></a>
(S-0009-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The v2 annotator was switched from sonnet to haiku to fit the $15 task budget under Claude
Code CLI overhead. The v2-vs-v1 accept rate delta therefore conflates the schema upgrade (flat
-> tree) with a model downgrade (sonnet -> haiku). Re-run all 115 rows on claude-sonnet-4-6
using the direct Anthropic API (no CLI), where per-call cost is ~$0.02 and 115 rows costs
~$2.30. Compare the resulting per-benchmark accept rate against both v1 (sonnet, flat) and
v2-haiku (haiku, tree) to attribute the +33% to +100% deltas between schema and model
contributions.

</details>

<details>
<summary>✅ <s>Replace the WorkArena++ proxy and HumanEval-as-tau-bench-proxy rows
with the actual benchmark data</s> — covered by <a
href="../../tasks/t0015_correct_proxy_benchmark_labels/"><code>t0015_correct_proxy_benchmark_labels</code></a>
(S-0009-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-06` |
| **Kind** | dataset |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

Inspecting the v1 (and now v2) rows shows the 'WorkArena++' rows are actually Mind2Web proxy
data and the 'tau-bench' rows are HumanEval proxy data — neither benchmark is loaded directly
because of access restrictions noted in the v1 task. For Phase 2 the benchmark provenance
matters: agent-evaluation results on Mind2Web do not generalize to WorkArena++. Either (a)
acquire WorkArena++ and tau-bench proper and re-annotate those rows, or (b) rename the
benchmark fields to match what is actually stored (Mind2Web, HumanEval) and update downstream
consumers. This is necessary before any Phase 2 paper claim about WorkArena++ performance.

</details>

<details>
<summary>✅ <s>Run a Phase 1 pilot annotation on 20 tasks before scaling to 100</s> —
covered by <a
href="../../tasks/t0005_hierarchical_annotation_pilot_v1/"><code>t0005_hierarchical_annotation_pilot_v1</code></a>
(S-0002-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-08` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |

The project's success criteria require 100 tasks annotated at three granularity levels. Before
scaling, run a 20-task pilot to validate the annotation schema, measure inter-annotator
agreement, and refine the rubric. WorkArena++ [Boisvert2024] offers the cleanest
atomic-vs-compositional structure for the pilot; its synthetic trace generator can supply gold
atomic actions, leaving manual annotation effort focused on global and subtask levels.

</details>

<details>
<summary>✅ <s>Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience
subset</s> — covered by <a
href="../../tasks/t0012_phase2_abc_smoke_frontierscience/"><code>t0012_phase2_abc_smoke_frontierscience</code></a>
(S-0006-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | [`10.48550_arXiv.2210.03629`](../../tasks/t0006_scope_aware_react_library/assets/paper/10.48550_arXiv.2210.03629/) |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/) |

scope_aware_react_v1 (A) and the in-progress scope_unaware_planandsolve_v1 (B) are now ready
as substrates. Run a controlled experiment on the t0003 FrontierScience subset with both
libraries plus a no-prompt-engineering baseline (C), measuring task_success_rate,
overconfident_error_rate, and avg_decisions_per_task across N=50 problems. Expected effect
size: +5 to +15 absolute success rate for A over B based on the Yao2022 ALFWorld result
anchor.

</details>

<details>
<summary>✅ <s>Stress-test the +57 pp schema-only delta with a stricter substantive
judge</s> — covered by <a
href="../../tasks/t0019_v2_judge_calibration_sonnet/"><code>t0019_v2_judge_calibration_sonnet</code></a>
(S-0014-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |

The schema-only delta of +57 pp is well above Zhou2022's +16 pp and Boisvert2024's +25 pp
published bands. One plausible cause is judge anchoring on tree shape: the haiku judge may be
partially scoring 'did the model produce a parseable tree with subtask-to-atomic edges' rather
than 'is the decomposition substantively right'. Replace the haiku judge with a substantive
critic prompt that simulates execution ('verify each atomic, executed in order, would actually
solve the problem') and re-judge the same 20-row sample under all three conditions (v1-sonnet,
v2-haiku, v2-sonnet). If schema-only drops materially below +57 pp under the substantive
judge, the gap to literature was judge anchoring; if schema-only stays near +57 pp, the schema
is doing real work. Cost ~$3 with sonnet judge.

</details>
