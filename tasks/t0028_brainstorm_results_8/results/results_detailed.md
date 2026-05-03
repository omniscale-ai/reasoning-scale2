# Brainstorm Session 8 — Detailed Results

## Summary

Brainstorm session 8 chose a minimum viable wave (t0029 + t0030) to close RQ1 and RQ4 within the
$66.54 remaining project budget. Hard $35 cap on t0029 with an abort rule that produces a partial
verdict on cap. Eight suggestion corrections applied (2 rejections, 6 demotions).

## Methodology

Pure planning session. No API calls, no compute, no remote machines. Decisions captured in step logs
001-004 and applied via correction files plus two child task scaffolds.

## Project State at Session Start

* Total spend: $133.46 / $200. Remaining: $66.54.
* Tasks: 27 (1 cancelled t0023, 26 completed).
* Uncovered suggestions: 64 (9 HIGH, 35 MEDIUM, 20 LOW).
* Answer assets: 2 (none directly answer RQ1-RQ5).
* Tasks completed since Brainstorm Session 7: t0025 (literature survey, $0.20), t0026 (Phase 2
  N=147, $38.61, over original $10 limit), t0027 (Phase 2.5 N=130, $20.76).

## Per-RQ Status After t0027

| RQ | Status | Direct evidence | Blocker | Cost to close |
| --- | --- | --- | --- | --- |
| RQ1 granularity → success | Underpowered | t0027 6 vs 6 disc., p=1.0 | Need >=30 disc. pairs | ~$21-32 |
| RQ2 overconfident error rate | Stuck at 100% confidence | t0027 ECE B=0.336 / C=0.374 | Plan-and-Solve floor; need content-driven calibrator + A patch | ~$10-22 |
| RQ3 execute-now vs request-info | Not operationalised | None | Need decision field in agent output | ~$5-18 |
| RQ4 info-asymmetric gain | Underpowered | t0027 per-subset rates suggestive | Stratification of >=30 disc. sample | ~$3-5 |
| RQ5 scope-mismatched strict-worse | Counter-direction | t0027 C=7 vs B=6 | C wrapper not structurally distinct enough | ~$12-32 |

## Independent Priority Reassessment of HIGH Suggestions

| Suggestion | Original priority | Reassessed | Action |
| --- | --- | --- | --- |
| S-0020-01 | high | low | Demote (HIGH→LOW). Pre-Phase-2 instruction-following hypothesis superseded by t0026/t0027 runtime data. |
| S-0021-02 | high | low | Demote (HIGH→LOW). Plan-and-Solve framing tweaks; floor confirmed content-driven by t0027. |
| S-0022-02 | high | low | Demote (HIGH→LOW). Progress-rate variant; binding constraint is power, not metric design. |
| S-0022-05 | high | low | Demote (HIGH→LOW). Error-taxonomy refinement; t0027 already produced first-order recovery distributions. |
| S-0025-01 | high | rejected | Reject obsolete. Pre-Phase-2 sampling proposal superseded by t0029. |
| S-0025-04 | high | covered | Source suggestion for t0029. |
| S-0026-02 | high | rejected | Reject duplicate of S-0027-02. |
| S-0027-01 | high | medium | Demote. Calibrator deferred to next wave. |
| S-0027-02 | high | medium | Demote. C structural rebuild deferred to next wave. |

Net: 9 HIGH → 0 HIGH (2 covered, 1 rejected duplicate, 1 rejected obsolete, 4 demoted to LOW, 2
demoted to MEDIUM).

## Decision Rationale

The minimum viable wave (t0029 + t0030) was chosen over the full five-RQ closure (TaskA-E, ~$48-104)
for these reasons:

1. **Budget headroom for cap overruns**: t0026 already overran its $10 limit by 286%. A $35 cap on
   t0029 with $66 remaining preserves $31 of headroom for unexpected overruns plus the next
   session's wave.
2. **RQ1 is the headline question**: a project-wide verdict on the main hypothesis is the Phase 4
   deliverable in `project/description.md`. RQ1 closure has the highest information value per
   dollar.
3. **TaskE is free**: piggy-backing t0030 on t0029's predictions delivers RQ4 at zero API cost.
4. **Cap-on-cap guardrail**: the researcher explicitly forbade in-wave replacement tasks if t0029
   hits the cap. This preserves budget and the suggestion backlog for an informed next session
   rather than spending blind on RQ2/RQ3/RQ5 before the RQ1 verdict.

## New Tasks

### t0029 RQ1 Discordance-Rich Paired Resample

* Status: `not_started`. Source suggestion: S-0025-04. Covers: S-0027-05.
* Hard $35 cap. Abort rule: if cap hit before 30 discordant pairs, partial verdict + power caveat,
  no in-wave replacements.
* Reuses t0021 Plan-and-Solve v2 (arm A) and t0027 fault-tolerant scope-aware ReAct (arm B).
* Saves predictions assets so t0030 can run with no additional API spend.
* Dependencies: t0010, t0021, t0027.

### t0030 RQ4 Info-Asymmetry Stratification

* Status: `not_started`. Source suggestion: none.
* Zero API cost. Stratifies t0029's paired sample by subset and info-asymmetry tertile.
* Tests whether granularity gain rate (success_rate(B) - success_rate(A)) concentrates in
  high-asymmetry strata via stratified McNemar / CMH with Bonferroni alpha=0.025.
* Dependencies: t0029.

## Suggestion Corrections

| Correction ID | Target | Action | Rationale (short) |
| --- | --- | --- | --- |
| C-0028-01 | S-0026-02 | reject | Duplicate of S-0027-02. |
| C-0028-02 | S-0025-01 | reject | Obsolete; t0029 supersedes. |
| C-0028-03 | S-0027-01 | priority MEDIUM | Calibrator deferred to next wave. |
| C-0028-04 | S-0027-02 | priority MEDIUM | C rebuild deferred to next wave. |
| C-0028-05 | S-0020-01 | priority LOW | Pre-Phase-2 hypothesis superseded. |
| C-0028-06 | S-0021-02 | priority LOW | Floor is content-driven, not template. |
| C-0028-07 | S-0022-02 | priority LOW | Power, not metric design, is binding. |
| C-0028-08 | S-0022-05 | priority LOW | Taxonomy already established. |

## Verification

* `verify_task_file t0028_brainstorm_results_8` — passed.
* `verify_corrections t0028_brainstorm_results_8` — passed (0 errors, 0 warnings).
* `verify_task_file t0029_rq1_discordance_rich_resample` — passed.
* `verify_task_file t0030_rq4_info_asymmetry_stratification` — passed.
* `verify_logs t0028_brainstorm_results_8` — passed.

## Files Created

* `tasks/t0028_brainstorm_results_8/task.json`
* `tasks/t0028_brainstorm_results_8/task_description.md`
* `tasks/t0028_brainstorm_results_8/step_tracker.json`
* `tasks/t0028_brainstorm_results_8/plan/plan.md`
* `tasks/t0028_brainstorm_results_8/research/{research_papers,research_internet,research_code}.md`
* `tasks/t0028_brainstorm_results_8/results/{results_summary,results_detailed}.md`
* `tasks/t0028_brainstorm_results_8/results/{metrics,suggestions,costs,remote_machines_used}.json`
* `tasks/t0028_brainstorm_results_8/logs/steps/00{1,2,3,4}_*/step_log.md`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0020-01.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0021-02.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0022-02.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0022-05.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0025-01.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0026-02.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0027-01.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0027-02.json`
* `tasks/t0029_rq1_discordance_rich_resample/{task.json,task_description.md}`
* `tasks/t0030_rq4_info_asymmetry_stratification/{task.json,task_description.md}`

## Limitations

* No RQ answered in this session by design.
* If t0029 hits the cap, the wave produces only a partial RQ1 verdict and a partial RQ4
  stratification.
* RQ2, RQ3, RQ5 remain open and depend on a future brainstorm session deciding whether the project
  continues, based on the RQ1 / RQ4 outcomes.

## Next Steps

* Execute t0029 (hard $35 cap, abort on cap).
* Execute t0030 immediately after.
* Run brainstorm session 9 with t0029 / t0030 results in hand.
