# ⏹ Tasks: Not Started

5 tasks. ⏹ **5 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0023 — <strong>Phase 2 Confirmatory ABC Run with Sonnet on
SWE-bench</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0023_phase2_abc_confirmatory_sonnet_swebench` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0012-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Task page** | [Phase 2 Confirmatory ABC Run with Sonnet on SWE-bench](../../../overview/tasks/task_pages/t0023_phase2_abc_confirmatory_sonnet_swebench.md) |
| **Task folder** | [`t0023_phase2_abc_confirmatory_sonnet_swebench/`](../../../tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/) |

# Phase 2 Confirmatory ABC Run with Sonnet on SWE-bench

## Motivation

t0012's smoke run on FrontierScience-Olympiad with claude-haiku-4-5 hit the floor on all three
ABC conditions (A: 2.5%, B: 0%, C: 0%). It cannot answer RQ1 (does scope-aware A beat
scope-unaware B), RQ2 (do gains concentrate in scope-sensitive states), or RQ5 (do
scope-mismatched C agents degrade predictably) because the conditions are indistinguishable at
the floor.

Per the t0017 literature survey, three changes lift the experiment out of the floor regime:

1. **Stronger model**: claude-sonnet-4-6 instead of haiku (the literature consensus is that
   scope-conditioning effects only become legible above ~30% baseline accuracy, see Wang2023
   and Boisvert2024).
2. **Tractable benchmark**: SWE-bench Verified Lite at the per-instance level (haiku achieves
   roughly 12-18% on the public leaderboard for similar lite splits; sonnet should reach
   30-50%).
3. **Continuous and diagnostic metrics**: progress rate (Ma2024) plus EAI error taxonomy
   (Li2024), wired in via t0022, replace the binary-success metric that collapsed t0012.

This is the **headline experiment** of the upcoming paper. Everything in Wave 1 (t0019, t0020)
defends the schema headline; everything in Wave 2 (t0021, t0022) builds the instruments;
**Wave 3 (this task) produces the confirmatory N>=157 signal that the paper claims**.

This task covers `S-0012-02` (primary) and `S-0010-01` (secondary; the C-condition variants
provide partial coverage).

## Scope

Run a paired ABC experiment on **N>=157 SWE-bench Verified Lite instances** with
claude-sonnet-4-6, using the t0021 v2 Plan-and-Solve library (which emits `final_confidence`)
and the t0022 metrics library (progress rate + EAI error taxonomy).

Three conditions per instance, in randomized order to defuse position bias:

* **A scope-aware**: the agent receives the v2 hierarchical scope tag for each step.
* **B scope-unaware**: the agent receives no scope tag (matches the base Plan-and-Solve
  setting).
* **C scope-mismatched**: the agent receives a wrong scope tag.

C-condition variants (per S-0010-01):

* `C-random`: tag drawn uniformly from the wrong-tag set with seed=0.
* `C-adversarial`: tag chosen to be the most distant from the true scope (e.g., atomic on a
  global step).

If budget allows, also run a `C-phase-randomized` control where the hierarchy itself is
shuffled within the row but the tag is correct; this isolates step-order from scope-mismatch.

## Sample Size and Power

* **N>=157 paired rows** per condition (Phase 1 confirmatory power calculation from t0012's
  smoke output): detects a 10 pp success-rate delta at alpha=0.05 with power 0.8 under McNemar
  pairing.
* **Annotation pre-step**: SWE-bench Verified Lite needs hierarchical-decomposition
  annotations for the agent's scope-tag input. The current dataset has 23 SWE-bench rows from
  t0012; this task **must annotate ~150 fresh instances** before the agent runs. Annotation
  uses claude-haiku-4-5 with the t0014 v2 schema.

## Deliverables

1. **Predictions asset** (`assets/predictions/phase2_abc_swebench_sonnet/`): per-row
   trajectories for all three conditions plus the C variants, with `final_confidence`,
   `progress_rate`, and error taxonomy distributions filled in.
2. **Answer asset** addressing RQ1 ("Does explicit operating-granularity conditioning improve
   final task success?") with explicit numerical answers for:
   * `success_rate(A) - success_rate(B)` with 95% CI from McNemar paired test
   * `progress_rate(A) - progress_rate(B)` with 95% CI from paired t-test
   * `success_rate(A) - success_rate(C-random)` and `... - success_rate(C-adversarial)`
   * `overconfident_error_rate` per condition (using `final_confidence` from t0021)
3. **Reported metrics** in `results/metrics.json` (explicit multi-variant) covering:
   * Per condition: `task_success_rate`, `progress_rate_mean`, `overconfident_error_rate`,
     plus per-error-taxonomy-label counts.
   * Paired-difference statistics: McNemar p-values, paired t-test p-values, effect sizes.
   * Efficiency: `efficiency_inference_time_per_item_seconds`,
     `efficiency_inference_cost_per_item_usd` (per condition).
4. **Hard/easy split analysis** by SWE-bench Verified hunk count (RQ9): does
   scope-conditioning value increase with task complexity? Reported in
   `results/results_detailed.md` with per-bucket deltas and 95% CIs.
5. **Compare-literature step**: side-by-side table of A-vs-B deltas with Wang2023 and
   Boisvert2024's scope-conditioning numbers.

## Models and Configurations

* **Annotator** (pre-step): claude-haiku-4-5 with v2 tree schema (matching t0014).
* **Agent**: claude-sonnet-4-6 via the t0021 v2 Plan-and-Solve library.
* **Judge / metric scorer**: claude-haiku-4-5 (default; per t0022 cost analysis), with a
  sonnet spot-check on a 20-row stratified sample to bound judge bias.

## Cost Estimate

* **Annotation pre-step** (about 150 fresh SWE-bench rows with haiku at v2 schema): about 150
  calls, around 6k tokens in / 1k tokens out per call. **About $11**.
* **Agent run** (N=157 x 3 conditions + 1 C variant on a 50-row subset = 521 trajectories,
  about 10 calls per trajectory averaging 8k tokens in / 1k tokens out at sonnet pricing):
  about 5.2M input tokens, about 520k output tokens. **About $23-25**.
* **Metric scoring** (per t0022 cost analysis): **about $3**.
* **Sonnet spot-check** (20 rows x 3 conditions x about 5 steps = 300 calls, about 3k in, 200
  out at sonnet pricing): **about $3**.
* **Reserve for retries / extra rows**: **+$3**.
* **Total**: **about $40-45**. The per-task limit may need to be raised; pre-flag as a budget
  intervention. If it does not get raised, drop the C-adversarial variant or the sonnet
  spot-check.

## Decision Criteria (Headline)

* If `success_rate(A) - success_rate(B) >= +5 pp` with McNemar p<0.05, the paper's central
  claim (RQ1) holds and the v2 schema produces a **legible**, **non-floor**, **paired**
  signal.
* If `progress_rate(A) - progress_rate(B) >= +0.05` with paired-t p<0.05 even when binary
  success is closer, the granularity-conditioning effect manifests in subgoal coverage rather
  than terminal success. Both interpretations support the headline.
* If both deltas are within +/-2 pp / +/-0.02 of zero with tight CIs, the v2 schema does not
  transfer from offline annotation accept-rate to online agent task success on this benchmark;
  the paper pivots to "schema helps annotation, not online agents" and the brainstorm round
  after this task scopes the next experiment.
* The C-adversarial penalty must be at least as large as C-random for RQ5 to hold.

## Dependencies

* `t0021_plan_and_solve_v2_with_final_confidence` (library that emits `final_confidence`).
* `t0022_abc_harness_progress_rate_and_error_taxonomy` (progress rate + EAI taxonomy).

Both are in flight as of this task's creation. Sequential dependency: t0023 cannot start
implementation until both libraries pass their own verification.

## Source Suggestion

`S-0012-02` (primary). `S-0010-01` is partially covered by the C-random and C-adversarial
variants; the phase-randomized control is in scope only if budget permits.

## Risks and Fallbacks

* **Budget overrun**: if the run-cost exceeds $40, drop the C-adversarial variant first (saves
  about $5), then the sonnet spot-check (about $3). The paired A/B/C-random comparison is the
  minimum viable headline.
* **Sonnet hits a different floor on SWE-bench**: if A-condition success rate at N=20 pilot is
  below 10%, abort the full run and recompute the power requirement at the new effect size.
* **Annotation cost dominates**: if the v2 annotation pre-step exceeds $15, switch to a
  three-shot prompt instead of the full v2 schema for the SWE-bench corpus only and document
  the schema simplification.
* **Judge bias on SWE-bench**: SWE-bench has a deterministic test-suite ground truth, so
  task_success is judge-free. Progress rate is judge-dependent; the sonnet spot-check exists
  to bound this bias.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` has explicit variants for A, B, C-random, and (if run) C-adversarial,
  each with task_success_rate, progress_rate_mean, overconfident_error_rate, and efficiency
  metrics.
* Paired-difference statistics for at least RQ1 and RQ5 are reported with explicit p-values.
* `results/results_detailed.md` contains the hard/easy split analysis (RQ9) and the
  literature-comparison table.
* Cost in `results/costs.json` is documented with the per-stage breakdown above and is at or
  below the agreed limit (currently ~$45).

</details>

<details>
<summary>⏹ 0022 — <strong>ABC Harness with Progress Rate and EAI Error
Taxonomy</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0022_abc_harness_progress_rate_and_error_taxonomy` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0017-02` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [ABC Harness with Progress Rate and EAI Error Taxonomy](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Task folder** | [`t0022_abc_harness_progress_rate_and_error_taxonomy/`](../../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/) |

# ABC Harness with Progress Rate and EAI Error Taxonomy

## Motivation

t0012's smoke run on FrontierScience-Olympiad with claude-haiku-4-5 hit the floor across all
three ABC conditions (A: 2.5%, B: 0%, C: 0%). At the floor, **binary task success cannot
distinguish** scope-aware from scope-unaware behaviour, so RQ1, RQ2, and RQ5 are invisible no
matter how big the sample.

t0017 surfaced two literature instruments that fix this:

* **AgentBoard progress rate** (Ma2024, NeurIPS 2024 D&B): subgoal coverage scoring with
  Pearson rho \> 0.95 against humans across 1013 environments. A continuous metric in `[0, 1]`
  that gives signal even when no run reaches the terminal goal.
* **Embodied Agent Interface error taxonomy** (Li2024, NeurIPS 2024): a 6-class per-step
  taxonomy (hallucination, affordance violation, missing step, extra step, wrong-order step,
  precondition/effect error) that attributes failures to specific modes.

Both instruments must be in place **before** t0023's confirmatory N>=157 run, otherwise t0023
risks producing the same uninformative floor result that t0012 produced. This task is a
zero-API library task that builds the two instruments and validates them on the t0012 sample.

This task covers `S-0017-02`.

## Scope

Build a single library that the existing ABC harness can import and call, exposing two
functions:

1. `compute_progress_rate(trajectory, environment_subgoals) -> float`
   * Implements the Ma2024 protocol: a list of subgoals defined per environment, scored 0/1 by
     a judge model, averaged over the trajectory. Returns a float in `[0, 1]`.
2. `classify_error(trajectory_step, environment_state) -> ErrorTaxonomyLabel`
   * Implements the Li2024 protocol: a strict-output judge call that returns one of six labels
     (`hallucination`, `affordance`, `missing_step`, `extra_step`, `wrong_order`,
     `precondition_or_effect`) plus an "ok" sentinel for non-error steps.

Both functions delegate to a judge model (default: claude-haiku-4-5; configurable to sonnet).
Subgoal definitions for FrontierScience-Olympiad and SWE-bench Verified live in a JSON
side-file in the library asset's `files/` directory. SWE-bench coverage is the priority since
t0023 runs there.

The library exposes a single high-level entry point `score_trajectory(trajectory, environment)
-> TrajectoryScore` that returns:

* `task_success: bool`
* `progress_rate: float`
* `step_errors: list[ErrorTaxonomyLabel]`
* `error_distribution: dict[label, count]`

## Deliverables

1. **Library asset** (`assets/library/abc_harness_metrics/`) with `details.json`, canonical
   description document, source code under `files/`, and subgoal-definition JSON for at least
   FrontierScience-Olympiad and SWE-bench Verified Lite.
2. **Unit tests** in `tasks/t0022_*/code/test_*.py`:
   * Progress rate is `0.0` when no subgoal is hit and `1.0` when all subgoals are hit, on a
     synthetic trajectory.
   * Each error taxonomy label is producible on a hand-crafted trajectory step.
   * The high-level entry point composes the two without raising on a known-good t0012 row.
3. **Validation against t0012**: replay the t0012 smoke trajectories through the new library
   and report progress rate and error distribution per ABC condition. Save these as a
   side-by-side table in `results/results_detailed.md`.
4. **Subgoal-definition JSON** for SWE-bench Verified Lite covering at least 50 instances (the
   subset t0023 will use). Use the SWE-bench Verified hint annotations as the seed.

## Implementation Notes

* **Subgoal scoring is a judge call**, not a deterministic check. Cache results to disk keyed
  by (environment, trajectory hash, subgoal text) so re-runs in t0023 do not re-spend.
* **Judge prompt** for progress rate: copy the Ma2024 supplementary material §C.2 prompt
  verbatim where licensing allows; otherwise paraphrase with explicit attribution in the
  library description document.
* **Error taxonomy prompt** for `classify_error`: use Li2024's appendix A.4 schema. The
  classifier returns exactly one label; ties default to `precondition_or_effect`.
* **Subgoal coverage on SWE-bench**: a "subgoal hit" is operationalised as the agent producing
  an edit that touches the same file as the gold patch hunk; finer-grained subgoals (line
  ranges, AST nodes) are out of scope here and can land in a follow-up.

## Cost Estimate

* Validation pass on t0012 smoke trajectories (~40 rows x 3 conditions x ~5 steps each = 600
  step-classifications + 120 progress-rate scores): **~720 haiku judge calls**.
* Haiku ~2k tokens in, ~150 tokens out per call: **~1.4M in, ~110k out**.
* At haiku pricing: **~$1.50**.
* Reserve: **+$0.50**.
* Total: **~$2**.

## Decision Criteria

After this task:

* If progress rate on the t0012 sample produces a non-degenerate distribution (mean > 0.05 and
  stddev > 0.03), the metric is a viable Metric 1 candidate for t0023. Otherwise, document the
  calibration problem and propose a different subgoal granularity.
* If the error taxonomy correctly distinguishes condition C trajectories from condition A
  trajectories on at least **30% of paired steps**, the taxonomy is doing real work and t0023
  can rely on it. Otherwise, flag and recommend tightening the per-environment subgoal lists
  before t0023.

## Dependencies

None. Output is consumed by t0023.

## Source Suggestion

`S-0017-02`.

## Risks and Fallbacks

* **Judge cost on t0023 explodes**: t0023 with N=157 x 3 conditions x ~5 steps each = ~2400
  step-classifications. Plan haiku as the default judge; reserve sonnet for spot-check
  re-grading on a 20-row stratified sample only.
* **Subgoal definitions miscalibrate**: the SWE-bench JSON has to be reviewed by hand on a
  10-instance pilot before t0023 ships.

## Verification Criteria

* Library asset passes `verify_library_asset.py`.
* Unit tests pass.
* Subgoal-definition JSON contains entries for at least 50 SWE-bench Verified Lite instances.
* The t0012 replay produces a per-condition breakdown of progress rate and error distribution
  in `results/results_detailed.md`.
* Cost in `results/costs.json` is at or below **$2**.

</details>

<details>
<summary>⏹ 0021 — <strong>Plan-and-Solve v2 with final_confidence Field</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0021_plan_and_solve_v2_with_final_confidence` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0012-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Plan-and-Solve v2 with final_confidence Field](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) |
| **Task folder** | [`t0021_plan_and_solve_v2_with_final_confidence/`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/) |

# Plan-and-Solve v2 with final_confidence Field

## Motivation

The t0007 `scope_unaware_planandsolve_v1` library does not emit a `final_confidence` field on
trajectory records. As a result, t0012's smoke run collapsed Metric 2
(overconfident_error_rate) to **0.0** for conditions B and C, making **RQ4 untestable** in any
confirmatory ABC experiment that reuses this library.

Before scaling to t0023 (sonnet on SWE-bench, N>=157), the library has to emit a verbalized
confidence label so Metric 2 is non-degenerate. This is a prerequisite library task with
**zero external API cost**.

This task covers `S-0012-01`.

## Scope

Extend the existing `tasks/t0007_*/code/` library (or the active fork of it) so that every
trajectory record produced by `scope_unaware_planandsolve_v1` carries a `final_confidence`
field in the range `[0.0, 1.0]`, populated by a verbalized confidence call following the
**Xiong2024 section 3.2 protocol**:

* After the model produces its final action / answer for the trajectory, issue **one
  additional prompt** asking the model to rate its confidence in the just-produced output on a
  0-1 scale, with explicit anchor-language ("0.0 = certain wrong, 0.5 = coin flip, 1.0 =
  certain right").
* Parse the numeric value with a strict regex; on parse failure, retry once with a clearer
  prompt; on second failure, write `null` and increment a `final_confidence_parse_failures`
  counter on the trajectory metadata.

The new `final_confidence` field must be emitted by **all three conditions** (A scope-aware, B
scope-unaware, C scope-mismatched) so paired analysis is well-defined.

## Deliverables

1. **Library asset** (`assets/library/scope_unaware_planandsolve_v2/`) with full
   `details.json`, canonical description document, and source code under `files/`. The library
   keeps backward compatibility: the v1 entry point still exists and still returns
   trajectories without `final_confidence`; the new v2 entry point returns trajectories that
   always carry the field.
2. **Unit tests** in `tasks/t0021_*/code/test_*.py`:
   * `final_confidence` is in `[0.0, 1.0]` whenever the parse succeeds.
   * `final_confidence` is `null` when the parse fails.
   * `final_confidence_parse_failures` count matches the number of `null` rows.
   * Trajectories from all three conditions (A, B, C) carry the field.
   * The v1 entry point continues to return the legacy schema.
3. **Smoke validation**: run the v2 library on a 5-row instance pool with claude-haiku-4-5 and
   confirm Metric 2 (overconfident_error_rate) returns a non-degenerate, non-zero value when
   at least one row is wrong with high confidence.
4. **Verbalized confidence prompt template** copied into `assets/library/.../files/prompts/`
   verbatim, with an inline citation to Xiong2024 §3.2 in the description document.

## Implementation Notes

* **Prompt protocol**: Xiong2024 section 3.2 says: "After answering, on a separate line,
  output a number between 0 and 1 representing your confidence that your answer is correct,
  where 0 means certain wrong and 1 means certain correct." Reuse this exact phrasing.
* **Two-call vs one-call**: prefer the two-call protocol (final answer first, confidence
  second) to avoid the model conditioning its answer on its own confidence claim. One-call is
  acceptable only if the cost difference matters at scale.
* **Caching**: confidence calls must reuse the same conversation prefix as the answer call to
  avoid double-charging for the prompt context. Use claude prompt caching where available.

## Cost Estimate

* Smoke validation: 5 rows x 3 conditions x 2 calls each (answer + confidence) with
  claude-haiku-4-5 = **30 calls**.
* Haiku input ~4k tokens per call x 30 = **~120k input tokens**.
* Haiku output ~300 tokens per call x 30 = **~9k output tokens**.
* At haiku pricing: **<$0.20**.
* Total: **<$1**.

## Decision Criteria

After this task:

* If unit tests and the smoke validation pass, the library is unblocked for t0023.
* If the confidence parse fails on more than **20%** of haiku rows, raise the parse failure
  rate in the description document and either tighten the prompt or move to JSON-mode output.
  Do not ship a library that is unreliable at parsing.

## Dependencies

None. The library will be reused by t0023.

## Source Suggestion

`S-0012-01`.

## Risks and Fallbacks

* **Sonnet-vs-haiku confidence drift**: haiku may produce flat confidence distributions
  (everything 0.7-0.9). If so, document this and flag it as an interpretability risk for
  t0023's Metric 2 analysis. The library does not need to fix the model's calibration; it only
  needs to emit the field.
* **Refusal rate increase**: adding a confidence call may push some models toward hedging the
  primary answer. Compare the smoke-run accuracy at A condition to the t0007/t0012 numbers; if
  accuracy drops by more than 5 pp, run an ablation with the confidence call moved to a
  separate trajectory.

## Verification Criteria

* Library asset passes `verify_library_asset.py`.
* Unit tests pass (`uv run pytest tasks/t0021_*/code/`).
* Smoke validation produces a non-zero, non-1 value for Metric 2 when ground truth shows at
  least one high-confidence error.
* `results/metrics.json` records the smoke run's Metric 2 value to confirm the field is wired
  end-to-end.
* Cost in `results/costs.json` is at or below **$1**.

</details>

<details>
<summary>⏹ 0020 — <strong>v2 Truncation vs Schema Ablation</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0020_v2_truncation_vs_schema_ablation` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0009-04` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Task page** | [v2 Truncation vs Schema Ablation](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Task folder** | [`t0020_v2_truncation_vs_schema_ablation/`](../../../tasks/t0020_v2_truncation_vs_schema_ablation/) |

# v2 Truncation vs Schema Ablation

## Motivation

The t0009 -> t0014 v2 upgrade changed two things at once:

1. **Schema**: flat list -> nested tree (global -> subtask -> atomic).
2. **Text completeness**: prompts moved from a 1500-char truncation to the full problem text.

On FrontierScience-Olympiad and WorkArena++, v2 saw +67% and +100% accept-rate deltas. Either
the truncation fix is doing the work (Xiong2024's prediction: longer context -> better
calibration), or the schema upgrade is doing the work, or both.

t0019 attacks the judge side of this question. **t0020 attacks the input side.** It runs a
third condition that holds the schema constant and reverts the truncation, so any drop
relative to v2-full isolates the truncation contribution.

This task covers `S-0009-04`.

## Scope

Run **one new annotation condition**: the v2 tree schema applied to the same instance pool as
t0014, but with the problem text truncated to **1500 characters** in both annotator and judge
prompts (matching the t0009 baseline exactly).

The result feeds a 3-way comparison with already-collected data:

| Condition | Schema | Text | Source |
| --- | --- | --- | --- |
| v1-flat-truncated | flat | 1500 chars | t0009 baseline |
| v2-tree-truncated | tree | 1500 chars | **this task** (new) |
| v2-tree-full | tree | full text | t0014 (existing) |

Effects decompose:

* `v2-tree-truncated - v1-flat-truncated` = pure schema effect (text held constant).
* `v2-tree-full - v2-tree-truncated` = pure text-length effect (schema held constant).
* The t0014 +57 pp delta = sum of the two.

## Deliverables

1. **Predictions asset** (`assets/predictions/v2_truncated_ablation/`): per-row annotator and
   judge outputs for the v2-tree-truncated condition. Same row pool as t0014 for paired
   comparison.
2. **Answer asset** addressing: "Of the t0014 +57 pp schema-only delta, how much is
   attributable to the schema upgrade vs the truncation fix, holding the other constant?"
3. **Reported metrics** with three explicit variants (one per row in the table above):
   * `accept_rate`
   * `accept_rate_stderr` (Wilson 95% CI)
   * `efficiency_inference_cost_per_item_usd`
   * `efficiency_inference_time_per_item_seconds`
4. **Decomposition table** in `results/results_detailed.md` showing the two isolated deltas
   with 95% CIs.

## Models and Configurations

* **Annotator**: claude-haiku-4-5 (matching t0009/t0014 baseline; haiku is cheap and used for
  the schema-effect reading).
* **Judge**: claude-haiku-4-5 with the t0014 original judge prompt (held constant; t0019
  handles the judge-side calibration).
* Same instance pool as t0014 (subtract the 3 known sonnet-timeout rows so n is matched across
  conditions).

Total annotation calls: ~40 rows x 1 condition = **~40 haiku annotation calls**. Total judge
calls: ~40 rows = **~40 haiku judge calls**.

## Cost Estimate

* Haiku input ~3k tokens per call x 80 calls = **~240k input tokens**.
* Haiku output ~500 tokens per call x 80 calls = **~40k output tokens**.
* At claude-haiku-4-5 pricing (approximately $0.80/M in, $4/M out): **about $0.36** haiku
  spend.
* Reserve for retry: **+$1**.
* Total: **~$1-2**.

## Decision Criteria

After this task:

* If `v2-tree-truncated - v1-flat-truncated >= +40 pp`, the schema upgrade is the dominant
  cause; Xiong2024's truncation hypothesis is rejected at this scale and the v2 schema
  deserves the headline.
* If `v2-tree-full - v2-tree-truncated >= +40 pp`, the truncation fix is the dominant cause;
  the v2 schema wins per row roughly because v1 truncation was clipping the problem before the
  model could reason about it. The headline shifts from "tree schema helps" to "include the
  full problem".
* If both contributions are within +/-15 pp of each other, the two compose roughly additively
  and both must be retained for the schema-effect claim.

## Dependencies

None.

## Source Suggestion

`S-0009-04`.

## Risks and Fallbacks

* **Truncation alters which instances are answerable at all**: some FrontierScience-Olympiad
  problems may be unparseable when clipped to 1500 chars. Log per-row truncation impact (did
  the model receive a complete problem statement) and report n for each (truncated, full)
  split.
* **Haiku is too noisy at small n**: if accept-rate stderr exceeds +/-15 pp on the new
  condition, flag the result as inconclusive and mark the decomposition as "underpowered,
  needs n=80 to resolve". Do not over-claim from n=40.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` has the three variants with stderr.
* `results/results_detailed.md` contains the decomposition table and a paired-row check that
  the same instance ids appear in all three conditions.
* Cost in `results/costs.json` is at or below **$2**.

</details>

<details>
<summary>⏹ 0019 — <strong>v2 Judge Calibration with Sonnet (Substantive + Familial
Bias)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0019_v2_judge_calibration_sonnet` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0014-02` |
| **Task types** | [`comparative-analysis`](../../../meta/task_types/comparative-analysis/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Task page** | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |
| **Task folder** | [`t0019_v2_judge_calibration_sonnet/`](../../../tasks/t0019_v2_judge_calibration_sonnet/) |

# v2 Judge Calibration with Sonnet (Substantive + Familial Bias)

## Motivation

t0014 produced a schema-only delta of **+57 pp** for v2 over v1, well above Zhou2022's +16 pp
and Boisvert2024's +25 pp published bands, and a model-only delta of **-1 pp** that sits below
Xiong2024's lower edge (0 pp). Two plausible threats to validity remain:

1. **Judge anchoring** (S-0014-02): the haiku judge may be partially scoring "the model
   produced a parseable tree with subtask-to-atomic edges" rather than "the decomposition is
   substantively right". If so, the +57 pp gap to literature is a judge artefact, not a schema
   effect.
2. **Familial bias** (S-0014-03): the haiku judge gives the v2-haiku annotator a same-family
   agreement bonus (~5-10 pp per Xiong2024). If so, the -1 pp model-only delta is masking a
   real sonnet annotator advantage.

Both threats can be tested at the same 43-row pool used in t0014 by swapping the judge prompt
and judge model. Defending the +57 pp schema-only headline before scaling to a confirmatory
experiment is the cheapest paper-defensible step on the critical path.

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary).

## Scope

Re-judge **the same 43 v2 rows** that t0014 produced (20 v2-sonnet + 23 v2-haiku) plus the
matched 20 v1-sonnet rows from t0009/t0014, under two new judge configurations:

* **Substantive critic** prompt (S-0014-02): the judge simulates execution ("verify each
  atomic, executed in order, would actually solve the problem") and outputs a binary
  accept/reject plus a per-criterion sub-score.
* **Model-rotated** judge (S-0014-03): keep the original t0014 judge prompt, swap the judge
  model from haiku to claude-sonnet-4-6.

Both judges run against the same row pool. Combined output is a 4-condition matrix per row:

| Condition | Annotator | Judge Prompt | Judge Model |
| --- | --- | --- | --- |
| Baseline (from t0014) | v1-sonnet / v2-haiku / v2-sonnet | original | haiku |
| Substantive | v1-sonnet / v2-haiku / v2-sonnet | substantive critic | sonnet |
| Model-rotated | v1-sonnet / v2-haiku / v2-sonnet | original | sonnet |

This task does not re-annotate. It only re-judges. Annotation rows from t0014 are read in via
the existing predictions overlay applied by t0015.

## Deliverables

1. **Predictions asset** (`assets/predictions/v2_judge_calibration/`): per-row judge verdicts
   under the substantive and model-rotated conditions, plus the cached baseline t0014/t0015
   verdicts as reference. Includes prompt-version and judge-model fields per row.
2. **Answer asset** (`assets/answer/.../`) addressing the question: "Does the v2 schema retain
   a 30+ pp accept-rate delta over v1 under a substantive judge and under a sonnet judge, or
   is the +57 pp t0014 headline an artefact of haiku judge anchoring?"
3. **Reported metrics** in `results/metrics.json` using the explicit multi-variant format, one
   variant per (annotator x judge-prompt x judge-model) cell. Each cell reports:
   * `accept_rate`
   * `accept_rate_stderr` (Wilson 95% CI)
   * `efficiency_inference_cost_per_item_usd`
   * `efficiency_inference_time_per_item_seconds`
4. **Comparison table** in `results/results_detailed.md` showing the schema-only and
   model-only deltas under all three judge configurations side by side, with explicit deltas
   vs t0014.

## Models and Configurations

* **Annotator outputs** (already produced; not re-run): claude-sonnet-4-6 v1 (20 rows), haiku
  v2 (23 rows), sonnet v2 (20 rows). All from t0014.
* **Substantive critic judge**: claude-sonnet-4-6 with the new prompt template.
* **Model-rotated judge**: claude-sonnet-4-6 with the original t0014 judge prompt.

Total judge calls: 43 rows x 2 new judge configurations = **86 sonnet judge calls**.

## Cost Estimate

* Sonnet input ~5k tokens per call x 86 = **~430k input tokens**.
* Sonnet output ~600 tokens per call x 86 = **~52k output tokens**.
* At claude-sonnet-4-6 pricing (approximately $3/M in, $15/M out): **about $2.05** sonnet
  spend.
* Reserve for retry/repair: **+$1**.
* Total: **~$3-5**.

This sits well within the remaining $51 budget.

## Decision Criteria

After this task:

* If schema-only delta drops below **+30 pp** under the substantive judge, the +57 pp t0014
  headline is partly judge-anchoring; reset the headline to the substantive number and revisit
  S-0014-01 (v3 schema iteration).
* If schema-only delta stays at or above **+45 pp** under both new judges, the schema effect
  is robust; commit to the t0023 confirmatory run as planned.
* If model-only delta swings to **at least +5 pp** under the sonnet judge, the t0014 -1 pp
  result is a haiku familial bias, and v2-sonnet should be the production annotator going
  forward.
* If model-only delta stays within +/-2 pp under the sonnet judge, the v2 schema does the work
  and sonnet annotation is not worth the cost premium.

## Dependencies

None on uncompleted tasks. Reads from t0014's predictions and t0015's correction overlay; both
are merged.

## Source Suggestion

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary). Both suggestions remain
active as `source_suggestion` until t0019 results are merged; the secondary will be marked
covered in the next brainstorm round if the data answers it.

## Risks and Fallbacks

* **Substantive judge is slow or unstable**: if per-row judge time exceeds 30 s, drop
  sub-criteria and use a binary verdict only.
* **Sonnet judge disagrees with itself across the two prompt variants on the same row**: log
  per-row agreement; report Cohen's kappa across (substantive, model-rotated) at the same
  model. This is a free signal about prompt-vs-anchoring effects.
* **The t0014 row pool has masked instances** (we know 3 sonnet timeouts exist; S-0014-05 was
  rejected): exclude those rows from all conditions consistently and report the effective n.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` contains all 9 cells (3 annotators x 3 judge configs) with
  accept_rate and stderr.
* `results/results_detailed.md` contains a side-by-side delta table and an explicit
  decision-criteria check-off against the four bullets above.
* Cost in `results/costs.json` is at or below **$5**.

</details>
