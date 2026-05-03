---
spec_version: "2"
task_id: "t0032_no_anthropic_rq1_path_decision"
date_completed: "2026-05-03"
status: "complete"
---
## Objective

Pick exactly one RQ1 execution path under the standing constraint that Anthropic API access is
permanently unavailable for the remainder of this project. The four required candidate paths are
**(a) existing-results-only verdict**, **(b) local / open-weight rerun**, **(c) alternative paid
provider**, and **(d) project-level "underpowered, provider-blocked" stop**. The plan delivers one
`answer` asset under `assets/answer/<answer_id>/`, a comparison table, and a USD-point-estimate cost
for each non-(a) option. Done means: the answer asset, results bundle, and suggestions are on disk;
all verificators pass; the recommendation is exactly one of (a)/(b)/(c)/(d) (not a hybrid); no
proposed step depends on Anthropic credentials reappearing.

## Task Requirement Checklist

The operative request from `tasks/t0032_no_anthropic_rq1_path_decision/task_description.md`:

> Choose one RQ1 execution path under permanent no-Anthropic constraint: existing-only verdict,
> local rerun, alternate provider, or stop. Produce exactly one `answer` asset that picks one path
> and records the reasoning. Compare cost in USD (point estimate), validity / statistical-power
> risk, comparability with t0027 / t0028's labelled-arm baseline, and time-to-result. Recommendation
> is exactly one of {(a), (b), (c), (d)} — not a hybrid, not a hedge. The recommendation does not
> assume Anthropic access becomes available at any point.

Decomposed checklist:

* **REQ-1** — Evaluate option (a) (existing-results-only verdict): cite the t0031 re-derivations
  (12/130 = 9.23% discordance, McNemar p=1.0000, per-stratum cells from `rq4_stratification.json`,
  RQ1 power grid from `rq1_power_grid.json`). Evidence: comparison table row in
  `results/results_detailed.md`. Satisfied by Step 3.
* **REQ-2** — Evaluate option (b) (local / open-weight rerun): document which open-weight policies
  are realistically runnable for this project, with a USD-point-estimate cost (or `$0` if
  hardware-only) and an explicit comparability statement against the t0027 fixed-arm convention.
  Evidence: comparison table row + comparability paragraph. Satisfied by Step 4.
* **REQ-3** — Evaluate option (c) (alternative paid provider): use the per-paired-instance anchor of
  about $0.107 from t0027 costs and the cheapest credible non-Anthropic 2026 list price (GPT-5 or
  Gemini 2.5 Pro at $1.25 / $10.00 per MTok output) to derive a per-pair point estimate of about
  $0.07 and a total at the locked t0029 cap of 218 pairs. Evidence: comparison table row. Satisfied
  by Step 5.
* **REQ-4** — Evaluate option (d) (project-level stop): document what subsequent project work the
  unspent budget unblocks (RQ4 stratification on existing data, S-0031-03 cost-tracker fix).
  Evidence: comparison table row + Suggestions section. Satisfied by Step 6.
* **REQ-5** — State the comparability claim against t0027 / t0028 explicitly for every non-(a)
  option. Evidence: dedicated paragraph in `full_answer.md` keyed to the t0027 anchor. Satisfied by
  Step 7.
* **REQ-6** — Produce one `answer` asset under `assets/answer/<answer_id>/` containing
  `details.json`, `short_answer.md`, and `full_answer.md` per the answer asset specification.
  `answer_id` derives from the chosen path (e.g. `no-anthropic-rq1-path-a`). Evidence: answer
  verificator passes with 0 errors. Satisfied by Step 8.
* **REQ-7** — Produce `results/results_summary.md` whose first non-frontmatter line is the headline
  label of the chosen path (e.g. `RQ1 PATH DECISION — OPTION (A): EXISTING-RESULTS-ONLY VERDICT`),
  and `results/results_detailed.md` embedding the comparison table. Evidence: results verificator
  passes. Satisfied by Step 9 (orchestrator stage).
* **REQ-8** — Produce at most 3 follow-up suggestions in `results/suggestions.json` tied to the
  chosen path. Evidence: suggestions verificator passes with no warnings. Satisfied by Step 10
  (orchestrator stage).
* **REQ-9** — `results/costs.json` reports `total_cost_usd: 0.00` and
  `results/remote_machines_used.json` is `[]`. Evidence: file diff. Satisfied by Step 9.

## Approach

This is an **analysis-only task**: no agent, no remote compute, no paid API call. The plan loads
already-computed JSON sidecars from `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/` and the
realized cost totals from `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/costs.json` and
`tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json`, derives per-option numbers
arithmetically, and writes them into a comparison table that drives the answer asset.

Key research findings carried into the plan:

* **Discordance is symmetric on the existing N=130 sample**: 12 discordant pairs, 6 arm-A wins, 6
  arm-B wins, two-sided exact-binomial McNemar p = 1.0000. The aggregate signal is null, and the
  per-stratum cells from `rq4_stratification.json` show a real but cancelling benchmark-by-arm
  interaction (SWE-bench one-sided p=0.0312 for B; FrontierScience one-sided p=0.0625 for A;
  Tau-bench dominated by both-fail). Source: `research/research_code.md` and
  `t0031/results/results_summary.md`.
* **Power at the locked t0029 cap is structurally underpowered**: `rq1_power_grid.json` shows power
  crosses 80% only at p1 ≥ 0.75 and is below 10% at p1 ≤ 0.55. Even a fresh cap-sized rerun yields a
  null verdict for any plausible "true" p1 short of 0.75.
* **Per-paired-instance cost on Claude Sonnet 4.6 is ≈ $0.107** ($0.0344 arm A + $0.0727 arm B,
  realized from `t0026/results/costs.json` and `t0027/results/costs.json`). Output-token list prices
  on GPT-5 and Gemini 2.5 Pro are about 33% cheaper than Claude Sonnet 4.6, so option (c)
  per-paired-instance cost is anchored at about $0.07. Source: `research/research_internet.md`.
* **Arm labelling is anchored to t0027** (where `plan_and_solve_v3` and `matched_mismatch_v2` pinned
  the policies under the labels A=Plan-and-Solve, B=scope-aware-ReAct, C=matched-mismatch on Claude
  Sonnet 4.6). Replacing the model under any arm label is a category change, not a continuation.
  Source: `research/research_code.md`.

**Recommended path: option (a) — existing-results-only verdict.** Rationale:

1. Cost is $0 and no provider access is required.
2. Arm-labelling comparability with t0027/t0028 is trivially preserved because no rerun happens.
3. The McNemar-null + benchmark-by-arm interaction is itself the formal RQ1 verdict; t0031 already
   proved the conclusion is stable to pre-registration.
4. Options (b) and (c) replace the policy under each arm label, making any verdict a verdict on a
   new experiment, not a continuation of t0027 — they cannot answer RQ1 as posed.
5. Option (d) forecloses analysis without delivering the verdict that (a) can deliver for $0.

**Alternatives considered**:

* Option (c) on GPT-5 or Gemini 2.5 Pro at about $16 total. Rejected because it changes the policy
  under arm labels A/B and would have to be re-justified as a new experiment, not as RQ1.
* Option (d) hard-stop with budget reallocation. Rejected because (a) delivers the same budget
  release plus a defensible verdict at the same $0 cost; (d) forecloses analysis pointlessly.
* A discordance-only rerun (creative-thinking step). Will be evaluated in step 11; not the default
  because it still introduces the policy-swap confound.

**Task type**: `answer-question` (already declared in `task.json`). The Planning Guideline for
answer-question tasks emphasizes single-asset output with explicit method declaration in
`details.json` `answer_methods` (set to `["existing_data_analysis"]` for option (a)).

## Cost Estimation

| Item | USD |
| --- | ---: |
| Paid API calls (this task) | $0.00 |
| Remote compute (this task) | $0.00 |
| **Total this task** | **$0.00** |

No new paid API call is made; the analysis re-reads JSON sidecars produced by t0031, t0027, and
t0026. Compare against `project/budget.json` per-task default limit — well inside.

The recommendation surfaces costed downstream options for completeness:

| Option | Per-pair USD | Total at 218-pair cap | Notes |
| --- | ---: | ---: | --- |
| (a) existing-only | n/a | **$0.00** | No rerun; recommended |
| (b) open-weight local | n/a | $0.00 hardware-bound | Comparability lost |
| (c) GPT-5 / Gemini 2.5 Pro | $0.07 | **$16 (point); $15-25 band** | Comparability lost |
| (d) hard stop | n/a | $0.00 | No verdict produced |

## Step by Step

The implementation step (step 9 in the canonical task lifecycle) executes these substeps:

1. **Load decision inputs.** Write `code/build_decision_inputs.py` that reads the 5 upstream JSON
   files enumerated under **Assets Needed** (the t0031 power-grid, RQ4 stratification, and log-audit
   sidecars; the t0026 and t0027 realized cost totals) and emits `code/decision_inputs.json` with
   the option-table cells. Use only `json.load`, `pathlib.Path`, and arithmetic — no statistical
   libraries. Inputs: 5 JSON files. Output: `code/decision_inputs.json`. Expected: file size > 200
   bytes; contains keys `discordance`, `power_grid`, `per_arm_costs`, `option_costs`. Satisfies
   REQ-1.

2. **Build the comparison table.** Write `code/build_comparison_table.py` that consumes
   `decision_inputs.json` and emits `code/comparison_table.md` (a 4-row × 5-column markdown table:
   option, USD point estimate, validity / power risk, t0027/t0028 comparability statement,
   time-to-result). Inputs: `code/decision_inputs.json`. Output: `code/comparison_table.md`.
   Expected: table has exactly 4 data rows, one per option. Satisfies REQ-1, REQ-2, REQ-3, REQ-4.

3. **[CRITICAL] Evaluate option (a).** Verify in `decision_inputs.json` that the discordance
   stratification and McNemar p-value match the values reported in the t0031 results bundle
   verbatim. If any field disagrees, halt and create an intervention file rather than silently
   choosing a different path. Expected: 12 discordant pairs, 6 a_only, 6 b_only, McNemar p=1.0000,
   per-stratum cells (SWE-bench b_only=6 a_only=0; FrontierScience a_only=5 b_only=0; Tau-bench 1
   discordant of 84). Satisfies REQ-1.

4. **Evaluate option (b).** Document the comparability gap explicitly in
   `assets/answer/.../full_answer.md` (paragraph "Why option (b) is rejected"). State that any
   open-weight rerun replaces the policy under arm A or arm B, breaking t0027's fixed-arm
   convention. Cite `research/research_code.md` for the labelling anchor. No code change here — this
   is reasoning recorded in the answer asset. Satisfies REQ-2, REQ-5.

5. **Evaluate option (c).** Use `code/decision_inputs.json` `option_costs` to confirm option (c)
   per-pair point estimate of about $0.07 and total of about $16 over 218 paired instances. Document
   in `full_answer.md` that even at $16, the policy-under-arm-label change makes the resulting
   verdict a verdict on GPT-5 or Gemini 2.5 Pro, not on the t0027 arms. Satisfies REQ-3, REQ-5.

6. **Evaluate option (d).** Document in `full_answer.md` that a hard stop forecloses the verdict
   that option (a) can already deliver for $0; the budget release is achievable under (a) without
   the foreclosure. Satisfies REQ-4.

7. **Lock in option (a) and write the comparability section.** In `full_answer.md`, write a
   dedicated section "Comparability with t0027 / t0028 fixed-arm convention" that states (a) and (d)
   preserve comparability trivially (no rerun); (b) and (c) replace the policy under each arm label
   and would have to be re-justified as new experiments. Satisfies REQ-5.

8. **Produce the answer asset.** Create `assets/answer/no-anthropic-rq1-path-a/details.json`,
   `assets/answer/no-anthropic-rq1-path-a/short_answer.md`, and
   `assets/answer/no-anthropic-rq1-path-a/full_answer.md` per
   `meta/asset_types/answer/specification.md`. Set `answer_methods: ["existing_data_analysis"]` and
   `confidence: "high"` (or `"medium"` if creative-thinking finds a non-obvious wrinkle). Run
   `uv run python -m arf.scripts.verificators.verify_answer_asset no-anthropic-rq1-path-a --task-id t0032_no_anthropic_rq1_path_decision`
   and fix any errors. Satisfies REQ-6.

The Step by Step ends here. REQ-7, REQ-8, and REQ-9 are satisfied downstream by orchestrator-managed
steps (results, suggestions, reporting) outside the scope of this plan.

## Remote Machines

None required. This is an analysis-only task that operates entirely on local JSON sidecars.

## Assets Needed

* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq1_power_grid.json` (from t0031)
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq4_stratification.json` (from t0031)
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/log_audit.json` (from t0031)
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json` (from t0027)
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/costs.json` (from t0026)

No new external assets, no new internet downloads.

## Expected Assets

This task produces exactly **one `answer` asset** matching `expected_assets: {"answer": 1}` in
`task.json`:

* **Type**: `answer`
* **Asset ID**: `no-anthropic-rq1-path-a` (or `-b` / `-c` / `-d` if creative-thinking flips the
  recommendation in step 11)
* **Description**: Decision asset that records the chosen RQ1 execution path under the permanent
  no-Anthropic constraint, with the four-option comparison table, USD-point-estimate cost,
  validity-risk discussion, and the explicit comparability statement against t0027/t0028.

## Time Estimation

* Implementation (code + answer asset): about 30 minutes.
* Creative thinking + comparison-table review: about 15 minutes.
* Results / suggestions / reporting (orchestrator-managed): about 30 minutes.
* Total wall-clock: about 75 minutes.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `decision_inputs.json` numeric fields disagree with `t0031/results/results_summary.md` | Low | Halts decision | Step 3 is `[CRITICAL]`: halt + intervention file rather than silent substitution |
| Creative-thinking surfaces a discordance-only rerun cheap enough to flip the recommendation | Medium | Recommendation changes from (a) to (c)-restricted | If creative-thinking finds a sub-$2 discordance-only resample with preserved comparability, document and rerun the comparison-table step |
| Answer-asset verificator flags missing `answer_methods` or `confidence` | Low | Blocks step 9 | Step 8 explicitly sets both fields per the answer asset spec |
| The chosen `answer_id` slug collides with an existing answer | Low | Verificator error | Run `aggregate_answers --format ids` before step 8 to confirm uniqueness |
| Reader interprets the McNemar-null as "no benchmark-by-arm interaction" | Medium | Wrong takeaway propagates downstream | The headline label and `full_answer.md` must say "null *aggregate* with documented per-stratum interaction"; do not let the per-stratum cells drop out of the headline |

## Verification Criteria

* `code/decision_inputs.json` exists, is valid JSON, and contains keys `discordance`, `power_grid`,
  `per_arm_costs`, `option_costs`. Run:
  `uv run python -c "import json, pathlib; json.loads(pathlib.Path('tasks/t0032_no_anthropic_rq1_path_decision/code/decision_inputs.json').read_text())"`.
* `assets/answer/no-anthropic-rq1-path-a/details.json` exists with `spec_version: "2"`,
  `answer_methods: ["existing_data_analysis"]`, and a non-empty `confidence` field. Run:
  `uv run python -m arf.scripts.verificators.verify_answer_asset no-anthropic-rq1-path-a --task-id t0032_no_anthropic_rq1_path_decision`.
  Expected: 0 errors.
* `results/results_summary.md` first non-frontmatter line is exactly
  `# RQ1 PATH DECISION — OPTION (A): EXISTING-RESULTS-ONLY VERDICT`. Run:
  `head -n 20 tasks/t0032_no_anthropic_rq1_path_decision/results/results_summary.md`.
* `results/results_detailed.md` contains a 4-row markdown table with one row per option (REQ-1
  through REQ-4 coverage). Run: `grep -c "^|" results/results_detailed.md` and confirm at least 6
  pipe-rows (header + separator + 4 data rows).
* `results/costs.json` has `"total_cost_usd": 0.00` and `results/remote_machines_used.json` contains
  `[]`. Run: `cat results/costs.json results/remote_machines_used.json`.
* `verify_task_results`, `verify_suggestions`, and `verify_answer_asset` all pass with 0 errors.
* The answer asset `full_answer.md` contains a section literally titled
  `## Comparability with t0027 / t0028 fixed-arm convention` (REQ-5 evidence).
* No file produced by this task references `ANTHROPIC_API_KEY`, an Anthropic credential, or any step
  that depends on Anthropic access reappearing. Run:
  `grep -RInl 'ANTHROPIC_API_KEY\|anthropic.*credential\|anthropic.*available' tasks/t0032_*` —
  expected: no matches in implementation outputs.
