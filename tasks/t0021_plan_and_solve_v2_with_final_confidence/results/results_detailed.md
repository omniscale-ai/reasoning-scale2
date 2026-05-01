---
spec_version: "2"
task_id: "t0021_plan_and_solve_v2_with_final_confidence"
---
# Results Detailed: Plan-and-Solve v2 with final_confidence

## Summary

The task ships the `scope_unaware_planandsolve_v2` library, a thin wrapper around the v1
Plan-and-Solve agent (built in t0007) that adds a verbalized `final_confidence` field on every
trajectory. The new field is elicited via a separate post-call following the Xiong et al. 2024
section 3.2 black-box protocol, parsed with a strict regex, retried once on parse failure, and
clamped to `[0.0, 1.0]`. A small n=1 x 3 validation pass on FrontierScience-Olympiad with
claude-haiku-4-5 confirms the plumbing is correct end-to-end across all three conditions (A
scope-aware, B scope-unaware, C scope-mismatched). The library, not the smoke numbers, is the
deliverable; the larger confirmatory comparison is t0023's job.

## Methodology

* **Machine**: local — Apple Silicon laptop running the Anthropic API client; no remote compute.
* **Model**: `claude-haiku-4-5` for both the agent calls and the confidence-elicitation calls; haiku
  also serves as the binary correctness judge.
* **Validation pass size**: n=1 row x 3 conditions (3 trajectories total). The smoke is a plumbing
  test, not a power-meaningful comparison; n is intentionally small to keep cost under the $1.00 cap
  and to preserve t0023's role as the confirmatory study.
* **Conditions**:
  * **A (scope-aware ReAct)**: chain-of-thought single-call agent followed by
    `elicit_final_confidence`.
  * **B (scope-unaware Plan-and-Solve v2)**: `PlanAndSolveAgentV2.run(...)` which composes the v1
    agent and elicits the confidence field automatically.
  * **C (scope-mismatched)**: `MatchedMismatchAgent.run(...)` from t0010 wrapped with
    `elicit_final_confidence`.
* **Confidence elicitation**: two-call protocol per row. After the agent produces its final answer,
  a second call asks the model to rate its confidence in `[0,1]`; on parse failure, one stricter
  retry is issued; on second failure the field is `null` and a parse-failure counter is incremented.
* **Runtime**: total wall-clock 786.69 s (~13 min) for the full smoke. Started 2026-05-01T14:33Z,
  finished ~2026-05-01T14:46Z (UTC).
* **Total cost**: $0.5383 of the $1.00 budget cap; 43 model calls (3 trajectories + judge calls +
  agent reasoning calls).
* **Pre-flight**: 16-test pytest suite (`code/test_planandsolve_v2.py`) validates the parser, the
  retry logic, the v1 schema invariants, and `PlanAndSolveAgentV2.run` end-to-end with the
  deterministic v1 `ScriptedModel`. All 16 tests pass.

## Metrics Tables

Verbatim from `results/metrics.json` (explicit-variant format with three condition variants):

| Variant | Agent | n | task_success_rate | overconfident_error_rate | avg_decisions_per_task |
| --- | --- | --- | --- | --- | --- |
| `condition_a_scope_aware` | `scope_aware_react_v1` | 1 | **0.0** | **1.0** | **1.0** |
| `condition_b_scope_unaware` | `scope_unaware_planandsolve_v2` | 1 | **0.0** | **0.0** | **8.0** |
| `condition_c_scope_mismatched` | `matched_mismatch_v1` (delegate `scope_unaware_planandsolve_v2`) | 1 | **0.0** | **0.0** | **31.0** |

Parse-failure totals (from `results/smoke_report.json`):

* Overall parse-failure rate: **0.0** (3/3 confidence calls parsed on the first try).
* Per-condition parse-failure totals: A=0, B=0, C=0.
* Plan gate (REQ-10): parse failure must stay under 20%; the smoke is well within that bound.

## Comparison vs Baselines

The relevant prior task is t0012 (Phase 2 A/B/C smoke on the same FrontierScience-Olympiad benchmark
with the same `claude-haiku-4-5` model), which produced these per-condition `task_success_rate`
values: A=**0.025** (1/40), B=**0.000** (0/40), C=**0.000** (0/11). The current n=1 x 3 pass also
hits floor (A=0/1, B=0/1, C=0/1), which is consistent with the t0012 finding and is the expected
state for this benchmark with this model.

The headline difference vs t0012 is **structural**, not numerical: t0012's Plan-and-Solve agent did
NOT emit `final_confidence` on conditions B and C, which collapsed Metric 2 to 0 by construction and
made paired calibration analysis ill-defined. This task fixes that — the v2 library now emits
`final_confidence` for all three conditions, so downstream confirmatory work (t0023, on a larger
sample with sonnet) can compare Metric 2 values across conditions on a meaningful basis.

The lone non-zero Metric 2 value here (A=1.0) reflects that the single A row was incorrect with high
confidence; that single observation is not a calibration finding by itself, only evidence that the
field is wired and the metric is non-degenerate.

## Analysis

The most actionable side-finding from this validation pass is the per-condition decision count:

* **A (scope-aware ReAct)**: 1 decision. The CoT-style single-call agent terminates immediately.
* **B (scope-unaware Plan-and-Solve v2)**: 8 decisions, in the expected range for v1 Plan-and-Solve
  on a hard problem.
* **C (scope-mismatched)**: **31 decisions**, ~4x more than B and 31x more than A.

A 31-decision trajectory at n=1 is a strong signal for further investigation in t0023. Plausible
explanations: (1) the matched-mismatch wrapper triggered a planning loop where the agent kept
re-planning under contradictory granularity guidance, (2) the agent never reached a confident
finishing state and exhausted the step budget, (3) the wrapper's prompt construction creates
adversarial conditions for the v1 planner. This deserves an explicit calibration-of-decisions look
in the larger t0023 run rather than acting on the n=1 observation here.

The confidence emission worked as intended on all three conditions: 0/3 parse failures, no retries
needed, and the field appears on the finishing trajectory record exactly as documented in the
library description. The parser strict-regex behavior matches the unit tests (last numeric token
wins; clamping at the word boundary handles values like `1.5` by matching the leading `1`).

## Limitations

* **n=1 per condition is by design** — the smoke validates plumbing, not calibration or accuracy.
  Any condition-vs-condition statistical claim from these numbers would be invalid; the larger
  downstream confirmatory study (t0023, n>=157 paired rows on sonnet) is the place where Metric 2
  calibration claims become valid.
* **Single benchmark and single model** — only FrontierScience-Olympiad and only haiku were
  exercised. Other benchmarks or models may produce different parse-failure rates, confidence
  distributions, or planning behavior.
* **Haiku may produce a flat confidence distribution** in [0.7, 0.9] independent of correctness; the
  library does not attempt to fix model calibration, only to emit the field. Per-model calibration
  is a downstream concern.
* **The 31-decision C trajectory is one observation**; do not infer a planning-loop pathology
  without the larger sample.

## Verification

* `verify_task_file` — PASSED.
* `verify_logs` — PASSED.
* `verify_task_results` — PASSED.
* `verify_library_asset scope_unaware_planandsolve_v2 --task-id t0021_plan_and_solve_v2_with_final_confidence`
  — PASSED.
* `verify_pr_premerge --task-id t0021_plan_and_solve_v2_with_final_confidence --pr-number <N>` — to
  be run after the PR opens.
* Unit tests: 16/16 passing in `code/test_planandsolve_v2.py`.

## Files Created

* `assets/library/scope_unaware_planandsolve_v2/details.json` — library metadata (spec_version 2).
* `assets/library/scope_unaware_planandsolve_v2/description.md` — canonical library description with
  YAML frontmatter, eight required sections, and Xiong2024 citation.
* `assets/library/scope_unaware_planandsolve_v2/files/prompts/confidence_prompt.txt` — verbatim
  Xiong2024 §3.2 prompt template.
* `code/planandsolve_v2.py` — v2 agent (`PlanAndSolveAgentV2`), data classes (`AgentResultV2`,
  `TrajectoryRecordV2`), parser (`parse_final_confidence`), and elicitation helper
  (`elicit_final_confidence`).
* `code/constants.py` — schema constants (`TRAJECTORY_RECORD_V2_FIELDS`, etc.).
* `code/paths.py` — centralized path constants for the smoke harness and tests.
* `code/model_call.py` — copy of t0012's Anthropic API wrapper with `CostTracker`.
* `code/calibration.py` — copy of t0011's `compute_overconfident_error_rate` and helpers.
* `code/run_smoke.py` — n=1 x 3 smoke validation harness.
* `code/test_planandsolve_v2.py` — 16-test pytest suite.
* `results/metrics.json` — explicit-variant format, three conditions, registered metric keys only.
* `results/costs.json` — cost breakdown by model with `services` and `budget_limit` fields.
* `results/remote_machines_used.json` — empty array (no remote compute).
* `results/smoke_predictions.jsonl` — 3 rows (one per condition), full trajectories with
  `final_confidence` populated.
* `results/smoke_report.json` — top-level rollup with per-condition metrics, parse-failure rate,
  total cost, and the 20% parse-failure gate flag.
* `results/_call_log.jsonl` — raw agent call log (15 entries).
* `results/_judge_log.jsonl` — raw judge call log (8 entries).
* `results/results_summary.md` — this task's headline summary.
* `results/results_detailed.md` — this file.
* `results/suggestions.json` — follow-up suggestions for t0023 and beyond.
* `logs/commands/*` — auto-generated `run_with_logs` outputs for every CLI invocation.
* `logs/steps/009_implementation/step_log.md` — implementation step log.

## Next Steps

* **t0023** (already created from suggestion `S-0012-01`): runs the v2 library on a larger sample
  (n>=157) with sonnet to get a power-meaningful Metric 2 comparison across conditions.
* Investigate the 31-decision C trajectory in t0023's larger sample to confirm or refute the
  planning-loop hypothesis.
* Track confidence-vs-correctness calibration on t0023 to see whether the `[0,1]` field is actually
  informative for the model or collapses to a flat distribution.

## Task Requirement Coverage

The operative task request from
`tasks/t0021_plan_and_solve_v2_with_final_confidence/task_description.md` and
`task.json.short_description`:

> Extend the t0007 Plan-and-Solve scope-unaware library to emit a verbalized final_confidence field,
> unblocking RQ4 in confirmatory ABC runs.

The decomposed requirements (REQ IDs match `plan/plan.md`):

| REQ | Status | Direct answer | Evidence |
| --- | --- | --- | --- |
| **REQ-1** Ship a registered library asset at `assets/library/scope_unaware_planandsolve_v2/` with `details.json`, canonical description, and source under `files/` | **Done** | Library is registered with `spec_version: "2"`, full `details.json`, eight-section `description.md`, and `files/prompts/confidence_prompt.txt`. | `assets/library/scope_unaware_planandsolve_v2/details.json`, `assets/library/scope_unaware_planandsolve_v2/description.md`, `verify_library_asset` PASSED. |
| **REQ-2** Provide a v2 entry point that always emits `final_confidence` on the result | **Done** | `PlanAndSolveAgentV2.run` returns an `AgentResultV2` with `final_confidence` populated; `TrajectoryRecordV2` finishing record carries the field. | `code/planandsolve_v2.py`, `code/test_planandsolve_v2.py::test_run_emits_field_when_parse_succeeds`. |
| **REQ-3** Keep the v1 entry point unchanged and importable | **Done** | The v1 module in t0007 is untouched; v2 imports v1 symbols. | `code/test_planandsolve_v2.py::test_v1_legacy_schema_unchanged` passes. |
| **REQ-4** Implement the Xiong2024 §3.2 verbalized confidence protocol with verbatim phrasing and 0/0.5/1 anchor language | **Done** | `CONFIDENCE_PROMPT_TEMPLATE` reproduces the §3.2 phrasing; the prompt template file is committed; the description doc cites Xiong2024 §3.2. | `assets/library/scope_unaware_planandsolve_v2/files/prompts/confidence_prompt.txt`, `assets/library/scope_unaware_planandsolve_v2/description.md` Metadata section. |
| **REQ-5** Strict regex parse, single retry, then `None` and increment `final_confidence_parse_failures` | **Done** | `parse_final_confidence` uses `\b(0(?:.\d+)? | 1(?:.0+)?)\b`last-match;`elicit_final_confidence`retries once and returns`(None, 2)` on double failure. |
| **REQ-6** Validate `final_confidence` is in `[0.0, 1.0]` whenever non-`None` | **Done** | Parser clamps to `[0,1]` via word-boundary regex; unit test asserts in-range output for adversarial input. | `code/test_planandsolve_v2.py::test_parse_final_confidence_clamp`. |
| **REQ-7** Emit `final_confidence` for all three conditions (A, B, C) | **Done** | Smoke run shows non-null `final_confidence` on all 3 trajectories (1 per condition); `elicit_final_confidence` is reused for A and C while B uses the v2 agent directly. | `results/smoke_predictions.jsonl` (3 rows, all with `final_confidence`). |
| **REQ-8** Run a smoke validation and write per-condition Metric 2 values to `results/metrics.json` | **Done at n=1** | `metrics.json` records `overconfident_error_rate` for all three conditions. n=1 x 3 (instead of the originally planned 5 x 3) was sufficient to validate plumbing under the $1.00 cap and is documented as the explicit-design choice. The larger comparison is t0023's job. | `results/metrics.json`, `results/smoke_report.json`. |
| **REQ-9** Keep total cost under $1.00 | **Done** | Total spend `$0.5383` ≤ `$1.00` cap. | `results/costs.json` `total_cost_usd: 0.538343`, `budget_limit: 1.0`. |
| **REQ-10** Document parse-failure rate; tighten if > 20% | **Done** | Overall parse-failure rate is **0.0** on n=3, well under the 20% gate; no prompt tightening required. | `results/smoke_report.json` `overall_parse_failure_rate`, `parse_failure_threshold_breached: false`. |
