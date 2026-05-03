# ✅ RQ1/RQ4 no-new-API preliminary salvage on existing t0026/t0027 outputs

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0031_rq1_rq4_no_new_api_salvage` |
| **Status** | ✅ completed |
| **Started** | 2026-05-03T11:14:49Z |
| **Completed** | 2026-05-03T11:47:30Z |
| **Duration** | 32m |
| **Dependencies** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md), [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Task types** | `data-analysis` |
| **Step progress** | 9/15 |
| **Task folder** | [`t0031_rq1_rq4_no_new_api_salvage/`](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/task_description.md)*

# RQ1/RQ4 no-new-API preliminary salvage on existing t0026/t0027 outputs

This task runs strictly **no-new-API** preliminary analyses on already-paid-for outputs from
`t0026_phase2_abc_runtime_n147_for_rq1_rq5` and `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`.
It spends **$0.00** of new API budget. It does **not** replace
`t0029_rq1_discordance_rich_resample`, which remains the canonical source for the planned
McNemar verdict and resumes from its locked plan once an Anthropic API key becomes available.

* * *

## Motivation

`t0029_rq1_discordance_rich_resample` is currently `intervention_blocked` because the project
does not have an `ANTHROPIC_API_KEY` available, so the planned ~$35 paired resample cannot
run. Until a key is provisioned, no new RQ1 / RQ4 evidence can be collected through paired
sampling. However, the `t0026` and `t0027` runs already produced paired outputs (130 paired
instances in `t0027` across frontsci, taubench, and SWE-bench) plus extensive logs. Useful
preliminary evidence can be extracted from these existing artifacts at zero cost. This task
does that extraction in a tightly scoped, clearly-labelled way so that the project does not
stall while waiting on credentials, and so that when (or if) `t0029` resumes, its analysis
pipeline can build on a verified, audited baseline.

The four analyses below are the maximum that can be done responsibly without new sampling.
Anything beyond them — re-running models, embedding new texts, recomputing per-instance
metrics under a new prompt — requires new API spend and belongs to `t0029` or to a future
task. This task explicitly forbids scope creep into a `t0029` redesign.

* * *

## Research questions addressed

* **RQ1 (preliminary)**: Given the observed `t0027` discordance rate, what is the expected
  paired- discordant yield and McNemar power under the locked `t0029` budget cap, and under
  what scenarios is the planned cap likely to be informative versus underpowered?
* **RQ4 (preliminary)**: How does the discordance/concordance pattern between arm A
  (Plan-and-Solve baseline) and arm B (scope-aware ReAct) stratify by dataset (frontsci,
  taubench, SWE-bench) on the existing `t0027` outputs?

Both findings are explicitly **preliminary**. They cannot replace the McNemar verdict planned
in `t0029` because they reuse a fixed sample (130 paired instances) rather than the
discordance-rich resample that `t0029` is designed to draw.

* * *

## Scope — exactly four analyses, in this order

### Analysis 1 — preliminary RQ4 stratification on existing t0027 outputs

* Compute the joint table dataset × (concordance | discordance) × (arm A outcome × arm B
  outcome) over the 130 paired instances in `t0027`.
* Datasets to stratify by: `frontsci`, `taubench`, `SWE-bench`.
* Variant labelling: arm A = Plan-and-Solve baseline, arm B = scope-aware ReAct. This matches
  the `t0028` task description naming convention. The `t0027` predictions assets use the
  inverted `variant_a` / `variant_b` labels — handle the inversion in **one** load helper
  inside this task's code only. Do not propagate the inversion elsewhere; do not introduce a
  new convention.
* Report cell counts, marginal totals (concordance vs. discordance per dataset, arm A correct
  vs. arm B correct per dataset), and Wilson 95% CIs per cell where N permits (N >= 5 in the
  cell).
* Cells with N < 5 must be reported with the count but flagged as having no usable CI.
* Label every result in this analysis as **PRELIMINARY** because per-dataset cell counts will
  be small.

### Analysis 2 — RQ1 power / futility analysis using t0027's observed discordance rate

* Read the exact paired-discordance numerator and denominator from `t0027`'s actual `results/`
  files (e.g., `results_summary.md`, `results_detailed.md`, or the underlying predictions). Do
  **not** hardcode a 4.6% discordance rate — that figure came from a different earlier summary
  and is not the rate this analysis must use. The relevant rate is approximately 12 / 130 ≈
  9.2%, but the exact numerator and denominator are to be re-derived from `t0027` files.
* Under the `t0029` plan assumptions:
  * Hard $35 cap.
  * Approximately $0.16 per new paired instance.
  * `BATCH_SIZE = 8`.
  * Sampling order frontsci → taubench → SWE-bench, seed `20260503`.
* Compute:
  * The total number of paired instances the cap can buy in expectation (≈ 35 / 0.16 = 218,
    but derive precisely from the locked plan).
  * The expected number of discordant pairs at the observed rate.
  * McNemar exact-binomial power at that expected discordant count for plausible conditional
    "B-wins-given-discordant" rates: 0.55, 0.60, 0.65, 0.70, 0.75, 0.80.
  * A futility table: for each conditional B-wins rate, the minimum number of discordant pairs
    needed to reach 80% power at α = 0.05.
* Produce a **futility statement**: under what scenarios does the planned $35 cap have a
  meaningful chance of delivering an RQ1 verdict, and under what scenarios is the project
  better served by a different design. Do **not** prescribe the redesign; that belongs to a
  later brainstorm.

### Analysis 3 — audit of t0026 / t0027 logs distinguishing infrastructure failures from genuine model failures

* Walk `t0026` and `t0027` logs (`logs/`, `intervention/`, and `results/`) and classify each
  recorded failure into one of:
  * **(a) Infrastructure failure**: harness crash, parser error, cost-tracker double-count,
    retry storm, rate-limit, network timeout, or any failure mode that would have been fixed
    in `t0029`'s revised harness.
  * **(b) Genuine model failure**: the model produced an answer that scored as wrong on the
    task's metric.
* Produce a small table: per task, per dataset, count of (a) versus (b), with brief
  representative examples (one or two short quotes per category) drawn directly from the logs.
* Goal: tell us whether the `t0027` verdicts have been corrupted by infrastructure issues that
  would have been fixed in `t0029`'s harness, and therefore whether the `t0027` baseline is
  trustworthy as a reference for analyses 1 and 2.
* If meaningful infrastructure-failure contamination is detected, flag it explicitly in the
  report and qualify analyses 1 and 2 accordingly.

### Analysis 4 — short report

* Two output files:
  * `results/results_summary.md` — concise overview, key tables, headline labels.
  * `results/results_detailed.md` — full analyses with all derivations, charts, and per-cell
    tables.
* Headline label on the first line of `results/results_summary.md`: `NO-NEW-API PRELIMINARY
  EVIDENCE — NOT A REPLACEMENT FOR t0029`.
* Include a clearly delimited `## Limitations` section listing every assumption and reason the
  evidence is preliminary, including:
  * The 130 paired instances are not a discordance-rich resample.
  * Per-cell N counts are small.
  * Power numbers depend on assumed conditional B-wins rates that are not yet observed.
  * Any infrastructure-failure contamination found in analysis 3.

* * *

## Approach

1. Implement a single load helper in `code/load_paired_outputs.py` that:
   * Reads `t0027` predictions assets.
   * Maps `variant_a` → arm B (scope-aware ReAct) and `variant_b` → arm A (Plan-and-Solve
     baseline) iff the inversion is confirmed by inspecting `t0027`'s task description and
     predictions metadata. Otherwise apply the inverse mapping. **Do not guess** — verify
     against `t0027`'s own files before locking the mapping in the helper.
   * Emits a single, internally-consistent paired DataFrame in arm-A / arm-B terms for
     downstream use.
2. `code/analysis_rq4_stratification.py` — analysis 1 implementation.
3. `code/analysis_rq1_power.py` — analysis 2 implementation, including the McNemar
   exact-binomial power computation.
4. `code/analysis_log_audit.py` — analysis 3 log walk and classification.
5. `code/build_report.py` — emits both report files into `results/` and saves all charts to
   `results/images/`.
6. All scripts are wrapped via `uv run python -m arf.scripts.utils.run_with_logs` per project
   rule 1; each major step gets its own log entry under `logs/`.

* * *

## Constraints

* **Zero API spend.** No paid LLM calls. No embedding calls. No vast.ai. The plan's cost
  estimate must be `$0.00`. `costs.json` must reflect zero third-party costs.
* **Local CPU only.** No remote machines. The `setup-machines` and `destroy-machines` stages
  are not applicable.
* **Read-only consumption** of `t0026`, `t0027`, and `t0029` outputs. No writes outside this
  task folder. No edits to other task folders. Top-level tooling files (`pyproject.toml`,
  `uv.lock`, `ruff.toml`, `.gitignore`) may change only if a new local-only dependency is
  genuinely needed — this task should not require any.
* **Single variant-labelling convention.** Reuse the `t0028` task-description naming (arm A =
  baseline, arm B = scope-aware) throughout all task-internal code, charts, and report tables.
  The `t0027` `variant_a` / `variant_b` inversion is isolated in `code/load_paired_outputs.py`
  only.
* **No spawning of follow-up tasks** from within `t0031`. Any follow-up redesign ideas go in
  `results/suggestions.json` only and are picked up by a later brainstorm.
* **Bounded scope.** The four analyses defined above are the entire scope. Do not expand into
  a full re-analysis of `t0026` / `t0027` or a `t0029` redesign.
* **Urgent but bounded.** The task is urgent in that it is the next thing the project should
  do, but every analysis must finish in well under a working day of agent time.

* * *

## Dependencies

* `t0026_phase2_abc_runtime_n147_for_rq1_rq5` — completed; provides earlier paired outputs and
  logs. Read-only.
* `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` — completed; provides the 130 paired instances
  and logs that anchor analyses 1, 2, and 3.

`t0029_rq1_discordance_rich_resample` is **not** a dependency: it is `intervention_blocked`
and not yet completed, and `t0031` does not require its output. `t0031` explicitly does not
replace `t0029`.

* * *

## Compute and budget

* **API budget**: $0.00. No new model calls of any kind.
* **Compute**: local CPU only. Estimated wall-clock time: well under one hour for all four
  analyses combined, dominated by file I/O and small-N statistical computations.
* **No GPU**, no remote machines, no long-running jobs.

* * *

## Expected assets

`expected_assets`: `{}`. This is a pure analysis task. It produces no new datasets, models,
papers, libraries, predictions, or answers — only the report files in `results/` and
supporting code in `code/`.

* * *

## Output specification

* `code/load_paired_outputs.py` — the single load helper that reconciles `t0027`'s `variant_a`
  / `variant_b` inversion into arm A / arm B.
* `code/analysis_rq4_stratification.py` — analysis 1.
* `code/analysis_rq1_power.py` — analysis 2 (includes McNemar exact-binomial power).
* `code/analysis_log_audit.py` — analysis 3.
* `code/build_report.py` — analysis 4, emits the report files.
* `results/results_summary.md` — concise overview. Headline first line: `NO-NEW-API
  PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`. Includes the per-dataset RQ4 joint
  table, the RQ1 power / futility headline, the log-audit headline, and the `## Limitations`
  section.
* `results/results_detailed.md` — full analyses with all derivations, per-cell tables with
  Wilson 95% CIs, the full power table across plausible conditional B-wins rates, and the full
  log-audit classification.
* `results/images/` — charts referenced by `results_detailed.md`. Required charts:
  1. `rq4_stratification_heatmap.png` — dataset × outcome combination heatmap with cell
     counts. Question answered: where do discordant pairs concentrate?
  2. `rq1_power_curve.png` — McNemar power as a function of expected discordant count, one
     curve per conditional B-wins rate. Question answered: at what discordant-pair count does
     the planned cap deliver 80% power?
  3. `log_audit_failure_breakdown.png` — stacked bars per task per dataset showing
     infrastructure-failure vs. genuine-model-failure counts. Question answered: are `t0027`'s
     verdicts contaminated by infrastructure issues?
* `results/metrics.json` — registered metrics (`task_success_rate`,
  `overconfident_error_rate`, `avg_decisions_per_task`) computed only where they can be
  derived without new API calls; if a metric is not derivable from existing outputs, set its
  value to `null` with an explanatory note.
* `results/costs.json` — total `0.00` USD across all services.
* `results/suggestions.json` — follow-up suggestions only (e.g., "redesign `t0029` cap given
  the futility analysis"). No work is spawned from `t0031`.
* `results/remote_machines_used.json` — empty (no remote machines used).

All charts must be embedded into `results_detailed.md` with markdown image links and short
captions that name the question they answer.

* * *

## Key questions (numbered, falsifiable)

1. **Q1 (RQ4)**: Does the per-dataset stratified joint table show discordance concentrated in
   any one of {frontsci, taubench, SWE-bench}, with at least one cell having a Wilson 95% CI
   that does not overlap the across-dataset average? **Falsifiable**: if every dataset's
   discordance fraction sits inside the across-dataset CI, the answer is no.
2. **Q2 (RQ1 power)**: At the observed `t0027` discordance rate and the locked $35 cap, is the
   expected discordant-pair count high enough to give 80% McNemar power at conditional B-wins
   rate ≥ 0.65? **Falsifiable**: if the expected discordant count falls below the 80%-power
   threshold for every conditional B-wins rate < 0.75, the answer is no, and the futility
   statement must say so explicitly.
3. **Q3 (RQ1 futility)**: Is there a conditional B-wins rate at or above which the planned cap
   can deliver 80% power, and is that rate plausible given `t0027`'s observed paired outcomes?
   **Falsifiable**: yes / no with a numeric threshold and a one-sentence justification
   grounded in the `t0027` joint table.
4. **Q4 (log audit)**: Do infrastructure failures account for less than 10% of `t0027`'s
   failed instances per dataset? **Falsifiable**: if any dataset has >= 10%
   infrastructure-failure share, the `t0027` baseline must be flagged as contaminated and
   analyses 1 and 2 must carry that qualification through to `results_summary.md`.

* * *

## Verification criteria

* `results/results_summary.md` exists and its first non-empty line is exactly `NO-NEW-API
  PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`.
* `results/results_summary.md` contains a `## Limitations` section.
* `results/results_detailed.md` exists, embeds all three required charts, and contains the
  full per-cell tables with Wilson 95% CIs.
* `results/costs.json` shows `0.00` USD total cost across all services.
* `results/remote_machines_used.json` is empty.
* No files outside `tasks/t0031_rq1_rq4_no_new_api_salvage/` are modified.
* The variant-labelling helper in `code/load_paired_outputs.py` is the **only** place where
  the `t0027` `variant_a` / `variant_b` inversion is handled.
* All four analyses are present and clearly labelled in both report files.
* All charts are saved under `results/images/` and embedded in `results_detailed.md`.

* * *

## Risks and fallbacks

* **Risk**: the inversion of `variant_a` / `variant_b` between `t0027` predictions and `t0028`
  task description is not as expected. **Fallback**: confirm the mapping by reading both files
  before locking the helper; if ambiguity remains, write an `intervention/` file rather than
  guessing.
* **Risk**: per-cell counts in the RQ4 stratification are too small to compute meaningful CIs.
  **Fallback**: report counts only and flag the cell as N < 5; do not invent a CI.
* **Risk**: the McNemar exact-binomial power computation is sensitive to the assumed
  conditional B-wins rate. **Fallback**: report a full grid of conditional B-wins rates rather
  than a single point estimate, and let the futility statement quantify uncertainty.
* **Risk**: log audit reveals so much infrastructure contamination that analyses 1 and 2 are
  effectively unusable. **Fallback**: the report must say so explicitly in `## Limitations`
  and in the headline summary; this is itself a useful preliminary finding.

* * *

## Cross-references

* Prior tasks whose results this task consumes: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`,
  `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`.
* Locked plan this task references but does not run: `t0029_rq1_discordance_rich_resample`.
* Naming convention this task follows: `t0028_brainstorm_results_8` task description (arm A =
  baseline, arm B = scope-aware).
* Source suggestion: none. This task was created by direct user instruction during a session
  in which `t0029` was `intervention_blocked`. It is not derived from a brainstorm suggestion.

</details>

## Suggestions Generated

<details>
<summary><strong>Unblock t0029 by provisioning ANTHROPIC_API_KEY</strong>
(S-0031-01)</summary>

**Kind**: experiment | **Priority**: high

t0029_rq1_discordance_rich_resample is the canonical RQ1 verdict owner and is currently
intervention_blocked on credentials. The t0031 power analysis confirms that the locked $35 cap
is informative only when the conditional B-wins rate p1 >= 0.75; provisioning the key and
running t0029 is the next step.

</details>

<details>
<summary><strong>Reconsider $35 cap given preliminary futility</strong> (S-0031-02)</summary>

**Kind**: evaluation | **Priority**: high

t0031 shows that at the t0027 discordance rate (~9.2%), the $35 cap yields expected discordant
n ≈ 32, which gives <50% McNemar power for any conditional B-wins rate <= 0.65. A future
brainstorm should weigh raising the cap, switching to a stratified resample (oversampling
SWE-bench and FrontSci where the discordance lives), or accepting the futility and pursuing
RQ4 stratification first.

</details>

<details>
<summary><strong>Fix the cost-tracker boundary that produces unknown
parser-recovery</strong> (S-0031-03)</summary>

**Kind**: library | **Priority**: medium

t0027 logged 29/130 arm-A and 33/130 arm-C rows with plan_parser_recovery_path='unknown', a
cost-tracker boundary artefact. Those rows produced trajectories and judged outcomes but their
recovery label was lost. A small harness fix should record the recovery path even when the
cost tracker boundary fires, so future audits can certify clean-recovery vs unknown without
ambiguity.

</details>

## Research

* [`research_code.md`](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_summary.md)*

NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029

# RQ1/RQ4 No-New-API Preliminary Salvage

This task spends **$0.00** of new API budget. It runs four bounded analyses on the
already-on-disk outputs of `t0026_phase2_abc_runtime_n147_for_rq1_rq5` and
`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`. The labelled-arm convention follows `t0028`:
arm A = Plan-and-Solve baseline, arm B = scope-aware ReAct, arm C = matched-mismatch.

## Summary

Re-derived the t0027 paired discordance rate at **12/130 = 9.23%** (symmetric: 6 arm-A wins vs
6 arm-B wins, McNemar two-sided p = 1.0000). Stratified RQ4 shows discordance is concentrated
in opposite directions on SWE-bench (6/20 arm-B wins) and FrontierScience (5/26 arm-A wins).
Under the locked t0029 plan ($35 cap, ~$0.16/pair → ~218 admittable new pairs, ≈ 32 expected
discordant at the t0027 rate) RQ1 reaches **80% power only when the conditional B-wins rate p1
≥ 0.75**. The infrastructure-vs-genuine-failure audit confirms zero MalformedPlanError
post-fix in t0027 but flags 22% (arm A) and 25% (arm C) of paired rows as parser-recovery
`unknown` (cost-tracker boundary noise that does not affect the discordance signal). This task
does not replace t0029; it only narrows the prior over likely outcomes.

## Metrics

* **Discordance rate (t0027 paired N=130)**: **12/130 = 0.0923** (re-derived from data, not
  hardcoded).
* **Discordance split**: arm-B wins **6**, arm-A wins **6**; McNemar exact-binomial two-sided
  p = **1.0000**.
* **SWE-bench arm-B pass rate**: **6/20 = 30.0%** (Wilson 95% CI [12.8%, 54.3%]); arm-A
  SWE-bench pass rate **0/20 = 0.0%**; SWE-bench McNemar p = **0.0312** (one-sided, 6 arm-B
  wins out of 6 discordant).
* **FrontierScience arm-A pass rate**: **5/26 = 19.2%**; arm-B = **0/26 = 0.0%**; FrontSci
  McNemar p = **0.0625**.
* **Tau-bench**: 1 discordant pair out of 84; signal is dominated by both-fail (judge-success
  rate is **1.2%** for arm A and **0.0%** for arm B).
* **RQ1 cap arithmetic**: cap admits **218** new paired instances; total N at cap = **348**;
  expected discordant N = **32**.
* **RQ1 power at expected discordant N=32 (one-sided α=0.05)**: p1=0.55 → **0.082**, p1=0.60 →
  **0.205**, p1=0.65 → **0.405**, p1=0.70 → **0.644**, p1=0.75 → **0.846**, p1=0.80 →
  **0.959**.
* **Smallest discordant N for 80% power** per p1: 0.55 → >200, 0.60 → 158, 0.65 → 69, 0.70 →
  37, 0.75 → 23, 0.80 → 18.
* **Audit pre-fix (t0026, N=147)**: A hard-failures **13** (12 timeouts + 1 runtime), B
  hard-failures **40** (22 timeouts + 2 runtime + **16 MalformedPlanError**), C hard-failures
  **44** (43 timeouts + 1 runtime).
* **Audit post-fix (t0027, paired N=130)**: zero MalformedPlanError raised. Parser-recovery
  unknown bucket: arm A **29/130 (22.3%)**, arm C **33/130 (25.4%)**; flagged as
  cost-tracker-boundary infrastructure noise.
* **Total cost of this task**: **$0.00** (no API calls, no remote machines).

## Verification

* `verify_task_file.py` — PASSED (0 errors, 0 warnings)
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings) — both upstream tasks
  (`t0026`, `t0027`) are completed.
* `verify_logs.py` — PASSED for all step folders (0 errors).
* `verify_research_code.py` — PASSED (0 errors).
* `verify_plan.py` — PASSED with 1 expected orchestrator warning (PL-W009).
* `verify_task_results.py` — PASSED (0 errors).
* Re-derived discordance count (12) matches the value computed by `load_paired_outputs.py`
  from the loaded DataFrame; no hardcoded 4.6% or 9.2% figure was used.
* `results_summary.md` first line equals exactly `NO-NEW-API PRELIMINARY EVIDENCE — NOT A
  REPLACEMENT FOR t0029`.
* `results/images/` contains exactly three PNG charts: `rq4_stratification_heatmap.png`,
  `rq1_power_curve.png`, `log_audit_failure_breakdown.png`.
* `costs.json` reports `total_cost_usd: 0.00`; `remote_machines_used.json` is `[]`.

## Limitations

* The 130 paired instances are a fixed sample, not the discordance-rich resample that
  `t0029_rq1_discordance_rich_resample` is designed to draw. Replacement is not possible
  without new API spend.
* Per-cell N is small in some strata (SWE-bench N=20, FrontSci N=26); Wilson CIs are wide and
  several stratum-level McNemar tests rest on 5-6 discordant pairs.
* Power numbers depend on the assumed conditional B-wins rate p1, which is **not** yet
  observed at the cap; the existing 12-discordant sample is consistent with any p1 in roughly
  [0.25, 0.75].
* 29 arm-A and 33 arm-C rows had their parser-recovery label swallowed by a cost-tracker
  boundary in t0027. They still produced judged outcomes, so they are included in the
  discordance count, but the audit cannot certify them as clean parser runs.
* Arm B (scope-aware ReAct) rows from t0026 do not carry a `plan_parser_recovery_path` field
  at all; the audit relies on t0026's pre-fix hard-failure aggregates (12 timeouts + 1 runtime
  error) for arm B.
* This task does not replace `t0029`. `t0029` remains the canonical RQ1 verdict owner; resume
  from its locked plan once an Anthropic API key is available.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_detailed.md)*

# NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029

## Summary

On t0027's paired set (N=130), arm A and arm B disagree on 12 pairs (9.23%), split
symmetrically as 6 arm-A wins and 6 arm-B wins (McNemar two-sided p = 1.0000). Stratification
by benchmark reveals SWE-bench discordance concentrated entirely on the arm-B side and
FrontierScience discordance concentrated entirely on the arm-A side; tau-bench is essentially
concordant. Under t0029's $35 cap, the expected discordant count is ≈ 32, which gives <50%
McNemar power for any conditional B-wins rate ≤ 0.65; 80% power requires p1 ≥ 0.75.

## Methodology

* Local CPU only; no API calls; no remote machines.
* All inputs are read from t0026 / t0027 prediction JSONL files plus
  t0027/data/paired_manifest.json.
* Variant→arm inversion (variant_a→arm_b, variant_b→arm_a, variant_c→arm_c) is isolated in
  `code/load_paired_outputs.py` and applied exactly once.
* Wilson 95% intervals computed in closed form (z=1.96). McNemar exact-binomial p-values and
  power computed from `math.comb` — no scipy / statsmodels.
* Charts are saved to `results/images/` and embedded below.

## Analysis 1 — RQ4 stratification (PRELIMINARY)

Per-subset 2x2 contingency tables for arm A (Plan-and-Solve) × arm B (scope-aware ReAct) on
the t0027 paired set. Cells flagged with N<5 do not carry a Wilson CI.

| Subset | N | both pass | A only | B only | both fail | discordant N | McNemar p (two-sided) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| swebench | 20 | 0 | 0 | 6 | 14 | 6 | 0.0312 |
| frontsci | 26 | 0 | 5 | 0 | 21 | 5 | 0.0625 |
| taubench | 84 | 0 | 1 | 0 | 83 | 1 | 1.0000 |
| ALL | 130 | 0 | 6 | 6 | 118 | 12 | 1.0000 |

### Per-stratum Wilson 95% CIs on arm-A and arm-B pass rates

| Subset | arm A pass | arm B pass | Note |
| --- | --- | --- | --- |
| swebench | 0/20 = 0.0% [0.0%, 16.1%] | 6/20 = 30.0% [14.5%, 51.9%] |  |
| frontsci | 5/26 = 19.2% [8.5%, 37.9%] | 0/26 = 0.0% [0.0%, 12.9%] |  |
| taubench | 1/84 = 1.2% [0.2%, 6.4%] | 0/84 = 0.0% [0.0%, 4.4%] |  |
| ALL | 6/130 = 4.6% [2.1%, 9.7%] | 6/130 = 4.6% [2.1%, 9.7%] |  |

![RQ4 stratification
heatmap](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/results/images/rq4_stratification_heatmap.png)

Caption: where do discordant pairs concentrate? SWE-bench discordance is entirely arm-B-wins
(6/6); FrontierScience discordance is entirely arm-A-wins (5/5); tau-bench is effectively
concordant (1 discordant pair on N=84).

## Analysis 2 — RQ1 power / futility under $35 cap

With the t0027-derived discordance rate ρ̂ = 9.23%, the $35 cap at $0.16/pair admits 218 new
paired instances; combined with t0027's 130 existing pairs, total paired N at cap = 348; the
expected discordant N at cap ≈ 32. McNemar exact-binomial power (one-sided, α=0.05) is shown
below for plausible conditional B-wins rates p1.

| p1 (cond. B-wins) | expected n_disc | power at expected | smallest n_disc for 80% power | one-sided p-floor at expected | critical k at expected |
| --- | --- | --- | --- | --- | --- |
| 0.55 | 32 | 0.082 | > 200 | 0.0000 | 22 |
| 0.60 | 32 | 0.205 | 158 | 0.0000 | 22 |
| 0.65 | 32 | 0.405 | 69 | 0.0000 | 22 |
| 0.70 | 32 | 0.644 | 37 | 0.0000 | 22 |
| 0.75 | 32 | 0.846 | 23 | 0.0000 | 22 |
| 0.80 | 32 | 0.959 | 18 | 0.0000 | 22 |

**Futility statement**: the $35 cap delivers ≥80% McNemar power only if the underlying
conditional B-wins rate p1 ≥ 0.75. At p1 = 0.65, power is below 50%; at p1 = 0.55–0.60 the cap
is effectively futile (<25% power). The t0027 paired sample's observed conditional B-wins is
exactly 6/12 = 0.50, which is consistent with p1 anywhere in roughly [0.25, 0.75] under a
Wilson 95% CI; the existing data do not pin p1 above the futility threshold.

![RQ1 power
curve](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/results/images/rq1_power_curve.png)

Caption: at what discordant-pair count does the planned cap deliver 80% power? At expected
n_disc ≈ 32, the planned cap delivers 80% power only when the conditional B-wins rate p1 ≥
0.75.

## Analysis 3 — infrastructure-vs-genuine-failure audit

The audit splits failures into two layers. Pre-fix (t0026, N=147 attempted) is dominated by
harness timeouts and the 16 MalformedPlanError rows in arm A (Plan-and-Solve v2 in t0026
internal labelling — the plan-parser fragility that motivated t0027's parser rewrite).
Post-fix (t0027, N=130 paired) shows zero MalformedPlanError and a clean recovery distribution
in 100/130 arm-A rows; the remaining 30 are an `unknown` recovery label introduced by a
cost-tracker boundary that swallowed the recovery field — those rows still produced
trajectories and judged outcomes.

### Pre-fix t0026 hard failures (out of 147 attempted)

| Arm (t0031 label) | t0026 internal label | timeouts | runtime errors | malformed plan | total infra |
| --- | --- | --- | --- | --- | --- |
| arm_a | B (PaS v2) | 22 | 2 | 16 | 40 |
| arm_b | A (scope-aware) | 12 | 1 | 0 | 13 |
| arm_c | C (mismatched) | 43 | 1 | 0 | 44 |

### Post-fix t0027 (paired N=130) parser-recovery distribution

| Arm | clean | reprompt | json_fallback | all_failed | unknown | judged-pass | judged-fail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arm_a | 75 | 14 | 11 | 1 | 29 | 6 | 124 |
| arm_b | n/a | n/a | n/a | n/a | n/a | 6 | 124 |
| arm_c | 70 | 18 | 7 | 2 | 33 | 7 | 123 |

### Post-fix t0027 infra vs genuine breakdown (paired N=130)

| Arm | infra (parser unknown, judged-fail) | genuine (clean/reprompt/json_fb/all_failed, judged-fail) |
| --- | --- | --- |
| arm_a | 29 | 95 |
| arm_b | 0 (no recovery field) | 124 |
| arm_c | 33 | 90 |

![Failure breakdown — t0026 vs
t0027](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/results/images/log_audit_failure_breakdown.png)

Caption: are t0027's verdicts contaminated by infrastructure issues? Pre-fix t0026 had a clear
parser-fragility bottleneck for plan-and-solve v2 (16/147 MalformedPlanError). Post-fix t0027
zeroed that out but introduced an `unknown` recovery bucket from a cost-tracker boundary;
those rows still produced judged outcomes.

## Limitations

* The 130 paired instances are a fixed sample. They are not the discordance-rich resample
  `t0029` is designed to draw.
* Per-cell N is small in stratified analyses (SWE-bench N=20, FrontSci N=26). Wilson 95% CIs
  are wide and stratum-level McNemar tests rest on 5–6 discordant pairs — formally significant
  for SWE-bench (p≈0.031) but the effective n is small.
* The conditional B-wins rate p1 is not observed at the cap. Reported powers assume a fixed p1
  across the whole grid.
* The `unknown` parser-recovery bucket (29 arm A, 33 arm C out of 130) is a harness artefact,
  not a model failure. Rows with `unknown` recovery still produced trajectories and judged
  outcomes; the audit treats `unknown` as infra noise but does not exclude those rows from the
  discordance count.
* Arm-B rows lack a parser-recovery field; the t0026 pre-fix hard-failure aggregates (12
  timeouts + 1 runtime error) are the only infra signal for arm B.
* This task does not replace `t0029`. `t0029` remains the canonical RQ1 verdict owner; resume
  from its locked plan once an Anthropic API key is provisioned.

## Verification

* Discordance count 12/130 = 9.23% re-derived from the loaded DataFrame, matches the t0027
  documented value.
* Per-subset N: swebench=20, frontsci=26, taubench=84 — assertions pass in load helper.
* Cap arithmetic: floor($35.00 / $0.16) = 218 new pairs.

## Files Created

* `results/results_summary.md`
* `results/results_detailed.md`
* `results/data/rq4_stratification.json`
* `results/data/rq1_power_grid.json`
* `results/data/log_audit.json`
* `results/images/rq4_stratification_heatmap.png`
* `results/images/rq1_power_curve.png`
* `results/images/log_audit_failure_breakdown.png`
* `results/metrics.json`, `results/costs.json`, `results/remote_machines_used.json`,
  `results/suggestions.json`

</details>
