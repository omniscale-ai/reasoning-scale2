---
spec_version: "1"
task_id: "t0032_no_anthropic_rq1_path_decision"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 5
libraries_found: 9
libraries_relevant: 0
date_completed: "2026-05-03"
status: "complete"
---
## Task Objective

Decide which of four required execution paths — (a) existing-results-only verdict, (b)
local/open-weight rerun, (c) alternative paid provider, (d) underpowered/provider-blocked stop — is
the right RQ1 disposition under the standing constraint that Anthropic API access is permanently
unavailable. This is an analysis-only task that re-loads existing on-disk outputs from `t0027`
(paired N=130 metrics, costs, predictions assets) and `t0031` (re-derived discordance rate, RQ4
stratification, RQ1 power grid, audit) and turns them into a single recommendation with a comparison
table. No new agent code is written, no model weights are loaded, and no API is called.

## Library Landscape

The `aggregate_libraries.py` aggregator returns **9 libraries** in the project (e.g.,
`scope_aware_react_v1`, `scope_unaware_planandsolve_v1`, `matched_mismatch_v1`,
`metric2_calibration_aggregator_v1`, `phase2_smoke_harness_v1`, `plan_and_solve_v3`,
`matched_mismatch_v2`, plus two more). All of them are agent-side libraries used in the upstream
A/B/C runtime experiments and their judges. **Zero** are relevant to this task: no agent will be
invoked here, no smoke harness will be executed, and no calibration aggregation will be re-run. All
numeric inputs are read from `tasks/t0031.../results/data/*.json` which were produced by t0031 with
no library-import dependency on this task.

## Key Findings

### Discordance and McNemar Numbers from `t0031` Are Authoritative

The re-derived discordance rate on the `t0027` paired N=130 sample is **12/130 = 9.23%**, with a
**6/6** symmetric split (arm A wins 6, arm B wins 6) and a two-sided exact-binomial **McNemar p =
1.0000** (`tasks/t0031/results/data/rq4_stratification.json`, ALL stratum) [t0031]. This is computed
directly from the paired DataFrame loaded by `t0031`'s `load_paired_outputs.py` and matches the
value embedded in `t0031/results/results_summary.md`. The same JSON file contains stratum-level
cells: SWE-bench (b_only=6, a_only=0; one-sided McNemar p=0.0312), FrontierScience (a_only=5,
b_only=0; one-sided p=0.0625), Tau-bench (1 discordant pair out of 84; both-fail dominates).

### RQ1 Power at the Locked t0029 Cap Depends Almost Entirely on `p1`

`tasks/t0031/results/data/rq1_power_grid.json` enumerates RQ1 power as a function of the
**conditional B-wins rate** `p1`, holding the cap arithmetic fixed (cap admits 218 new pairs at
$0.16/pair, expected 32 discordant pairs at the t0027 rate). Power crosses 80% only at **p1 ≥ 0.75**
(power = 0.846 at p1=0.75; 0.959 at p1=0.80) and is **<10%** at p1=0.55. The existing 12-discordant
sample is consistent with any p1 in roughly **[0.25, 0.75]** [t0031]. This means: even if a
no-Anthropic rerun produced exactly the cap-sized sample, RQ1 still yields a null verdict for any
plausible "true" `p1` short of 0.75 — the test is structurally underpowered against a realistic
alternative.

### Per-Instance Cost Shape Lets us Anchor Option (c)

`tasks/t0027/results/costs.json` reports realized agent costs of **$9.4534** for arm B over 130
instances and **$9.3392** for arm C over 130 instances on Claude Sonnet 4.6, i.e.
**~$0.0727/instance** and **~$0.0718/instance** respectively. `tasks/t0026/results/costs.json`
reports arm A at **$4.4659 / 130 = ~$0.0344/instance** [t0026, t0027]. These are realized, not
modelled; they include retries, judge overhead, and tool-call density. The implied
per-paired-instance cost on Claude Sonnet is **~$0.107**, used as the option (c) cost anchor in
`research/research_internet.md`.

### Arm Labelling Is Anchored to t0027 and Cannot Survive a Provider Swap

The `tasks/t0027/results/results_summary.md` fixes the arm mapping as **A = Plan-and-Solve baseline,
B = scope-aware ReAct, C = matched-mismatch** with the policy implemented by `plan_and_solve_v3` and
`matched_mismatch_v2` (both created in t0027) on **Claude Sonnet 4.6** [t0027]. Note that t0027
deliberately flipped the A/B convention used in t0026 (where A was scope-aware-ReAct and B was
Plan-and-Solve), so any prior or downstream task that cites the arm labels must be read against the
t0027 convention. Replacing the underlying model (option (b) or (c)) preserves the arm **label** but
changes the **policy under the label** — judging the new policy as if it were the same arm B that
t0027 ran is a category error. Any RQ1 verdict from options (b)/(c) is a verdict on a new
experiment, not a continuation.

### t0031's Audit Identifies the Real Infrastructure Risk

`tasks/t0031/results/data/log_audit.json` (read indirectly via results_summary.md) confirms **zero**
post-fix `MalformedPlanError` in t0027 (down from 16 in t0026's pre-fix arm B) but flags **22.3% /
25.4%** of paired arm-A / arm-C rows as parser-recovery `unknown` because the cost-tracker boundary
swallowed the recovery label. The audit explicitly classifies this as **cost-tracker-boundary
infrastructure noise that does not affect the discordance signal** [t0031]. Implication for this
task: there is no parser-failure ambiguity to resolve before delivering a verdict.

## Reusable Code and Assets

* **Source**: `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq1_power_grid.json`
  * **What it does**: serialized RQ1 power grid (six p1 values, each with power-at-expected and the
    smallest discordant-N for 80% power)
  * **Reuse method**: **read directly via `json.load`** in this task's `code/` if the answer asset
    needs an embedded or recomputed copy of the table; do not modify
  * **Adaptation needed**: none — the file is already in its canonical form
  * **Line count**: ~62 lines

* **Source**: `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq4_stratification.json`
  * **What it does**: per-stratum discordance cells (both_pass, a_only, b_only, both_fail), Wilson
    95% CIs, and McNemar p-values for SWE-bench / FrontierScience / Tau-bench / ALL
  * **Reuse method**: **read directly via `json.load`**
  * **Adaptation needed**: none
  * **Line count**: ~123 lines

* **Source**: `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/log_audit.json`
  * **What it does**: paired infrastructure audit (parser-failure counts, parser-recovery unknown
    buckets) keyed by arm
  * **Reuse method**: **read directly via `json.load`** if the answer asset cites the
    parser-recovery percentages explicitly
  * **Adaptation needed**: none
  * **Line count**: small JSON

* **Source**: `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json` and
  `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/costs.json`
  * **What it does**: realized per-arm dollar totals on N=130, dividing by 130 yields the
    per-instance shape used as the option (c) anchor
  * **Reuse method**: **read directly**; arithmetic only (no numerical libraries needed)
  * **Adaptation needed**: none
  * **Line count**: small JSON

No agent libraries are imported or copied. No code crosses the cross-task import rule because this
task only reads JSON sidecars produced by upstream tasks.

## Lessons Learned

* **Numbers must be re-derived, never hard-coded.** `t0031/results/results_summary.md` explicitly
  warns that the discordance count was re-derived by `load_paired_outputs.py` and that no hardcoded
  4.6% or 9.2% figure was used [t0031]. This task should follow the same rule: any number that
  appears in the answer asset must be either a direct quote of a JSON field from
  `t0031/results/data/*.json` or a simple arithmetic combination of fields cited inline.

* **The arm-labelling convention is the binding artefact.** `t0027` fixed the A=Plan-and-Solve /
  B=scope-aware-ReAct / C=matched-mismatch labelling by anchoring it to `plan_and_solve_v3` and
  `matched_mismatch_v2` on Claude Sonnet 4.6 [t0027]; this convention is what t0028's brainstorming
  scheduled t0029 against. A rerun on a different provider cannot reuse the labels without an
  explicit "policy under label X has changed from claude-sonnet-4-6 to <provider/model>" note in the
  comparison table — this is the central comparability claim the user asked us to make explicit.

* **Per-stratum signals are not the same as the aggregate.** SWE-bench shows a one-sided arm-B
  advantage (p=0.0312) and FrontierScience shows a one-sided arm-A advantage (p=0.0625); they cancel
  in the ALL row [t0031]. Any verdict that says "RQ1 is null" must also say "but the cancellation is
  itself the finding" — option (a) is exactly the option that lets us publish that finding without
  spinning up a new experiment.

* **Tau-bench is dominated by both-fail.** 83/84 pairs are both-fail; 1 pair is discordant [t0031].
  No amount of additional Tau-bench paired data will move RQ1 because the conditional-event rate is
  too low. This is an upstream sampling problem, not an analysis problem.

## Recommendations for This Task

1. **Read `rq1_power_grid.json`, `rq4_stratification.json`, and the t0026 / t0027 `costs.json` files
   directly into a small Python script in this task's `code/` folder.** Emit a single JSON sidecar
   (e.g., `decision_inputs.json`) containing the option-table fields. Do not re-implement McNemar,
   Wilson, or power calculations — quote `t0031`'s numbers verbatim.

2. **Quote `t0031`'s power grid in the answer asset's comparison table** rather than recomputing it.
   The grid already enumerates the relevant `p1` band; the only new column per option is the
   comparability statement and the cost point estimate.

3. **Cite the t0027 fixed-arm convention explicitly** when describing the comparability risk for
   options (b) and (c). Without this anchor, the comparability claim is hand-wave; with it, the
   claim is a direct contradiction of the t0027 fixed-arm definition.

4. **Do not import or copy any agent library.** This task is analysis-only; the only "reusable"
   assets are JSON sidecars produced by t0031, t0027, and t0026.

5. **Treat the t0029 cap (218 new pairs at $0.16/pair, $35) as the upper bound** for option (c)
   total cost. Re-derive the dollar number on the cheaper non-Anthropic prices (per
   `research/research_internet.md`) but keep the 218-pair denominator unchanged.

## Task Index

### [t0026]

* **Task ID**: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`
* **Name**: Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5
* **Status**: completed
* **Relevance**: source of arm A's per-instance realized cost (about $0.0344) and the original
  paired sample that t0027 reused; note that t0026 used the pre-fix arm convention
  (A=scope-aware-ReAct, B=Plan-and-Solve), which t0027 then flipped to the canonical convention used
  in this task.

### [t0027]

* **Task ID**: `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
* **Name**: Phase 2.5 A/B/C re-run with fixed B and C
* **Status**: completed
* **Relevance**: canonical paired N=130 outputs on Claude Sonnet 4.6 with `plan_and_solve_v3` and
  `matched_mismatch_v2`. Source of arm B and arm C per-instance costs and the metrics-level RQ1
  paired McNemar (p=1.0).

### [t0028]

* **Task ID**: `t0028_brainstorm_results_8`
* **Name**: Brainstorm 8: close RQ1/RQ4 via discordance-rich resample under $35 cap
* **Status**: completed
* **Relevance**: brainstorming session that scheduled t0029 (RQ1 cap rerun) and t0030 (RQ4
  stratification) under the t0027 fixed-arm convention. This task is the upstream causal parent of
  the no-Anthropic disposition decision being made here.

### [t0029]

* **Task ID**: `t0029_rq1_discordance_rich_resample`
* **Name**: RQ1 discordance-rich paired resample with hard $35 cap
* **Status**: intervention_blocked
* **Relevance**: defines the locked $35 cap, $0.16/pair cost assumption, and 218 new-pair upper
  bound used in the option (c) total-cost band. Currently blocked on Anthropic API access.

### [t0031]

* **Task ID**: `t0031_rq1_rq4_no_new_api_salvage`
* **Name**: RQ1/RQ4 no-new-API preliminary salvage
* **Status**: completed
* **Relevance**: produces the three JSON sidecars (`rq1_power_grid.json`, `rq4_stratification.json`,
  `log_audit.json`) that this task quotes verbatim. Also issues the explicit warning that t0031 does
  not replace t0029 — which is precisely the gap this task closes by recommending a no-Anthropic
  disposition.
