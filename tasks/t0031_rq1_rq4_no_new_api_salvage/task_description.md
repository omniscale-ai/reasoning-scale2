# RQ1/RQ4 no-new-API preliminary salvage on existing t0026/t0027 outputs

This task runs strictly **no-new-API** preliminary analyses on already-paid-for outputs from
`t0026_phase2_abc_runtime_n147_for_rq1_rq5` and `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`. It
spends **$0.00** of new API budget. It does **not** replace `t0029_rq1_discordance_rich_resample`,
which remains the canonical source for the planned McNemar verdict and resumes from its locked plan
once an Anthropic API key becomes available.

* * *

## Motivation

`t0029_rq1_discordance_rich_resample` is currently `intervention_blocked` because the project does
not have an `ANTHROPIC_API_KEY` available, so the planned ~$35 paired resample cannot run. Until a
key is provisioned, no new RQ1 / RQ4 evidence can be collected through paired sampling. However, the
`t0026` and `t0027` runs already produced paired outputs (130 paired instances in `t0027` across
frontsci, taubench, and SWE-bench) plus extensive logs. Useful preliminary evidence can be extracted
from these existing artifacts at zero cost. This task does that extraction in a tightly scoped,
clearly-labelled way so that the project does not stall while waiting on credentials, and so that
when (or if) `t0029` resumes, its analysis pipeline can build on a verified, audited baseline.

The four analyses below are the maximum that can be done responsibly without new sampling. Anything
beyond them — re-running models, embedding new texts, recomputing per-instance metrics under a new
prompt — requires new API spend and belongs to `t0029` or to a future task. This task explicitly
forbids scope creep into a `t0029` redesign.

* * *

## Research questions addressed

* **RQ1 (preliminary)**: Given the observed `t0027` discordance rate, what is the expected paired-
  discordant yield and McNemar power under the locked `t0029` budget cap, and under what scenarios
  is the planned cap likely to be informative versus underpowered?
* **RQ4 (preliminary)**: How does the discordance/concordance pattern between arm A (Plan-and-Solve
  baseline) and arm B (scope-aware ReAct) stratify by dataset (frontsci, taubench, SWE-bench) on the
  existing `t0027` outputs?

Both findings are explicitly **preliminary**. They cannot replace the McNemar verdict planned in
`t0029` because they reuse a fixed sample (130 paired instances) rather than the discordance-rich
resample that `t0029` is designed to draw.

* * *

## Scope — exactly four analyses, in this order

### Analysis 1 — preliminary RQ4 stratification on existing t0027 outputs

* Compute the joint table dataset × (concordance | discordance) × (arm A outcome × arm B outcome)
  over the 130 paired instances in `t0027`.
* Datasets to stratify by: `frontsci`, `taubench`, `SWE-bench`.
* Variant labelling: arm A = Plan-and-Solve baseline, arm B = scope-aware ReAct. This matches the
  `t0028` task description naming convention. The `t0027` predictions assets use the inverted
  `variant_a` / `variant_b` labels — handle the inversion in **one** load helper inside this task's
  code only. Do not propagate the inversion elsewhere; do not introduce a new convention.
* Report cell counts, marginal totals (concordance vs. discordance per dataset, arm A correct vs.
  arm B correct per dataset), and Wilson 95% CIs per cell where N permits (N >= 5 in the cell).
* Cells with N < 5 must be reported with the count but flagged as having no usable CI.
* Label every result in this analysis as **PRELIMINARY** because per-dataset cell counts will be
  small.

### Analysis 2 — RQ1 power / futility analysis using t0027's observed discordance rate

* Read the exact paired-discordance numerator and denominator from `t0027`'s actual `results/` files
  (e.g., `results_summary.md`, `results_detailed.md`, or the underlying predictions). Do **not**
  hardcode a 4.6% discordance rate — that figure came from a different earlier summary and is not
  the rate this analysis must use. The relevant rate is approximately 12 / 130 ≈ 9.2%, but the exact
  numerator and denominator are to be re-derived from `t0027` files.
* Under the `t0029` plan assumptions:
  * Hard $35 cap.
  * Approximately $0.16 per new paired instance.
  * `BATCH_SIZE = 8`.
  * Sampling order frontsci → taubench → SWE-bench, seed `20260503`.
* Compute:
  * The total number of paired instances the cap can buy in expectation (≈ 35 / 0.16 = 218, but
    derive precisely from the locked plan).
  * The expected number of discordant pairs at the observed rate.
  * McNemar exact-binomial power at that expected discordant count for plausible conditional
    "B-wins-given-discordant" rates: 0.55, 0.60, 0.65, 0.70, 0.75, 0.80.
  * A futility table: for each conditional B-wins rate, the minimum number of discordant pairs
    needed to reach 80% power at α = 0.05.
* Produce a **futility statement**: under what scenarios does the planned $35 cap have a meaningful
  chance of delivering an RQ1 verdict, and under what scenarios is the project better served by a
  different design. Do **not** prescribe the redesign; that belongs to a later brainstorm.

### Analysis 3 — audit of t0026 / t0027 logs distinguishing infrastructure failures from genuine model failures

* Walk `t0026` and `t0027` logs (`logs/`, `intervention/`, and `results/`) and classify each
  recorded failure into one of:
  * **(a) Infrastructure failure**: harness crash, parser error, cost-tracker double-count, retry
    storm, rate-limit, network timeout, or any failure mode that would have been fixed in `t0029`'s
    revised harness.
  * **(b) Genuine model failure**: the model produced an answer that scored as wrong on the task's
    metric.
* Produce a small table: per task, per dataset, count of (a) versus (b), with brief representative
  examples (one or two short quotes per category) drawn directly from the logs.
* Goal: tell us whether the `t0027` verdicts have been corrupted by infrastructure issues that would
  have been fixed in `t0029`'s harness, and therefore whether the `t0027` baseline is trustworthy as
  a reference for analyses 1 and 2.
* If meaningful infrastructure-failure contamination is detected, flag it explicitly in the report
  and qualify analyses 1 and 2 accordingly.

### Analysis 4 — short report

* Two output files:
  * `results/results_summary.md` — concise overview, key tables, headline labels.
  * `results/results_detailed.md` — full analyses with all derivations, charts, and per-cell tables.
* Headline label on the first line of `results/results_summary.md`:
  `NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`.
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
   * Maps `variant_a` → arm B (scope-aware ReAct) and `variant_b` → arm A (Plan-and-Solve baseline)
     iff the inversion is confirmed by inspecting `t0027`'s task description and predictions
     metadata. Otherwise apply the inverse mapping. **Do not guess** — verify against `t0027`'s own
     files before locking the mapping in the helper.
   * Emits a single, internally-consistent paired DataFrame in arm-A / arm-B terms for downstream
     use.
2. `code/analysis_rq4_stratification.py` — analysis 1 implementation.
3. `code/analysis_rq1_power.py` — analysis 2 implementation, including the McNemar exact-binomial
   power computation.
4. `code/analysis_log_audit.py` — analysis 3 log walk and classification.
5. `code/build_report.py` — emits both report files into `results/` and saves all charts to
   `results/images/`.
6. All scripts are wrapped via `uv run python -m arf.scripts.utils.run_with_logs` per project rule
   1; each major step gets its own log entry under `logs/`.

* * *

## Constraints

* **Zero API spend.** No paid LLM calls. No embedding calls. No vast.ai. The plan's cost estimate
  must be `$0.00`. `costs.json` must reflect zero third-party costs.
* **Local CPU only.** No remote machines. The `setup-machines` and `destroy-machines` stages are not
  applicable.
* **Read-only consumption** of `t0026`, `t0027`, and `t0029` outputs. No writes outside this task
  folder. No edits to other task folders. Top-level tooling files (`pyproject.toml`, `uv.lock`,
  `ruff.toml`, `.gitignore`) may change only if a new local-only dependency is genuinely needed —
  this task should not require any.
* **Single variant-labelling convention.** Reuse the `t0028` task-description naming (arm A =
  baseline, arm B = scope-aware) throughout all task-internal code, charts, and report tables. The
  `t0027` `variant_a` / `variant_b` inversion is isolated in `code/load_paired_outputs.py` only.
* **No spawning of follow-up tasks** from within `t0031`. Any follow-up redesign ideas go in
  `results/suggestions.json` only and are picked up by a later brainstorm.
* **Bounded scope.** The four analyses defined above are the entire scope. Do not expand into a full
  re-analysis of `t0026` / `t0027` or a `t0029` redesign.
* **Urgent but bounded.** The task is urgent in that it is the next thing the project should do, but
  every analysis must finish in well under a working day of agent time.

* * *

## Dependencies

* `t0026_phase2_abc_runtime_n147_for_rq1_rq5` — completed; provides earlier paired outputs and logs.
  Read-only.
* `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` — completed; provides the 130 paired instances and
  logs that anchor analyses 1, 2, and 3.

`t0029_rq1_discordance_rich_resample` is **not** a dependency: it is `intervention_blocked` and not
yet completed, and `t0031` does not require its output. `t0031` explicitly does not replace `t0029`.

* * *

## Compute and budget

* **API budget**: $0.00. No new model calls of any kind.
* **Compute**: local CPU only. Estimated wall-clock time: well under one hour for all four analyses
  combined, dominated by file I/O and small-N statistical computations.
* **No GPU**, no remote machines, no long-running jobs.

* * *

## Expected assets

`expected_assets`: `{}`. This is a pure analysis task. It produces no new datasets, models, papers,
libraries, predictions, or answers — only the report files in `results/` and supporting code in
`code/`.

* * *

## Output specification

* `code/load_paired_outputs.py` — the single load helper that reconciles `t0027`'s `variant_a` /
  `variant_b` inversion into arm A / arm B.
* `code/analysis_rq4_stratification.py` — analysis 1.
* `code/analysis_rq1_power.py` — analysis 2 (includes McNemar exact-binomial power).
* `code/analysis_log_audit.py` — analysis 3.
* `code/build_report.py` — analysis 4, emits the report files.
* `results/results_summary.md` — concise overview. Headline first line:
  `NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`. Includes the per-dataset RQ4
  joint table, the RQ1 power / futility headline, the log-audit headline, and the `## Limitations`
  section.
* `results/results_detailed.md` — full analyses with all derivations, per-cell tables with Wilson
  95% CIs, the full power table across plausible conditional B-wins rates, and the full log-audit
  classification.
* `results/images/` — charts referenced by `results_detailed.md`. Required charts:
  1. `rq4_stratification_heatmap.png` — dataset × outcome combination heatmap with cell counts.
     Question answered: where do discordant pairs concentrate?
  2. `rq1_power_curve.png` — McNemar power as a function of expected discordant count, one curve per
     conditional B-wins rate. Question answered: at what discordant-pair count does the planned cap
     deliver 80% power?
  3. `log_audit_failure_breakdown.png` — stacked bars per task per dataset showing
     infrastructure-failure vs. genuine-model-failure counts. Question answered: are `t0027`'s
     verdicts contaminated by infrastructure issues?
* `results/metrics.json` — registered metrics (`task_success_rate`, `overconfident_error_rate`,
  `avg_decisions_per_task`) computed only where they can be derived without new API calls; if a
  metric is not derivable from existing outputs, set its value to `null` with an explanatory note.
* `results/costs.json` — total `0.00` USD across all services.
* `results/suggestions.json` — follow-up suggestions only (e.g., "redesign `t0029` cap given the
  futility analysis"). No work is spawned from `t0031`.
* `results/remote_machines_used.json` — empty (no remote machines used).

All charts must be embedded into `results_detailed.md` with markdown image links and short captions
that name the question they answer.

* * *

## Key questions (numbered, falsifiable)

1. **Q1 (RQ4)**: Does the per-dataset stratified joint table show discordance concentrated in any
   one of {frontsci, taubench, SWE-bench}, with at least one cell having a Wilson 95% CI that does
   not overlap the across-dataset average? **Falsifiable**: if every dataset's discordance fraction
   sits inside the across-dataset CI, the answer is no.
2. **Q2 (RQ1 power)**: At the observed `t0027` discordance rate and the locked $35 cap, is the
   expected discordant-pair count high enough to give 80% McNemar power at conditional B-wins rate ≥
   0.65? **Falsifiable**: if the expected discordant count falls below the 80%-power threshold for
   every conditional B-wins rate < 0.75, the answer is no, and the futility statement must say so
   explicitly.
3. **Q3 (RQ1 futility)**: Is there a conditional B-wins rate at or above which the planned cap can
   deliver 80% power, and is that rate plausible given `t0027`'s observed paired outcomes?
   **Falsifiable**: yes / no with a numeric threshold and a one-sentence justification grounded in
   the `t0027` joint table.
4. **Q4 (log audit)**: Do infrastructure failures account for less than 10% of `t0027`'s failed
   instances per dataset? **Falsifiable**: if any dataset has >= 10% infrastructure-failure share,
   the `t0027` baseline must be flagged as contaminated and analyses 1 and 2 must carry that
   qualification through to `results_summary.md`.

* * *

## Verification criteria

* `results/results_summary.md` exists and its first non-empty line is exactly
  `NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`.
* `results/results_summary.md` contains a `## Limitations` section.
* `results/results_detailed.md` exists, embeds all three required charts, and contains the full
  per-cell tables with Wilson 95% CIs.
* `results/costs.json` shows `0.00` USD total cost across all services.
* `results/remote_machines_used.json` is empty.
* No files outside `tasks/t0031_rq1_rq4_no_new_api_salvage/` are modified.
* The variant-labelling helper in `code/load_paired_outputs.py` is the **only** place where the
  `t0027` `variant_a` / `variant_b` inversion is handled.
* All four analyses are present and clearly labelled in both report files.
* All charts are saved under `results/images/` and embedded in `results_detailed.md`.

* * *

## Risks and fallbacks

* **Risk**: the inversion of `variant_a` / `variant_b` between `t0027` predictions and `t0028` task
  description is not as expected. **Fallback**: confirm the mapping by reading both files before
  locking the helper; if ambiguity remains, write an `intervention/` file rather than guessing.
* **Risk**: per-cell counts in the RQ4 stratification are too small to compute meaningful CIs.
  **Fallback**: report counts only and flag the cell as N < 5; do not invent a CI.
* **Risk**: the McNemar exact-binomial power computation is sensitive to the assumed conditional
  B-wins rate. **Fallback**: report a full grid of conditional B-wins rates rather than a single
  point estimate, and let the futility statement quantify uncertainty.
* **Risk**: log audit reveals so much infrastructure contamination that analyses 1 and 2 are
  effectively unusable. **Fallback**: the report must say so explicitly in `## Limitations` and in
  the headline summary; this is itself a useful preliminary finding.

* * *

## Cross-references

* Prior tasks whose results this task consumes: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`,
  `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`.
* Locked plan this task references but does not run: `t0029_rq1_discordance_rich_resample`.
* Naming convention this task follows: `t0028_brainstorm_results_8` task description (arm A =
  baseline, arm B = scope-aware).
* Source suggestion: none. This task was created by direct user instruction during a session in
  which `t0029` was `intervention_blocked`. It is not derived from a brainstorm suggestion.
