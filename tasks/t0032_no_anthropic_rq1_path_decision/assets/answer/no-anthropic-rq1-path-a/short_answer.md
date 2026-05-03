---
spec_version: "2"
answer_id: "no-anthropic-rq1-path-a"
answered_by_task: "t0032_no_anthropic_rq1_path_decision"
date_answered: "2026-05-03"
---
# No-Anthropic RQ1 path: option (a) existing-results-only verdict

## Question

Which RQ1 execution path do we follow under the permanent no-Anthropic constraint: (a)
existing-results-only verdict, (b) local / open-weight rerun, (c) alternative paid provider, or (d)
project-level underpowered / provider-blocked stop?

## Answer

Option (a), the existing-results-only verdict, is the right path. The t0031 re-derivation already
yields the formal RQ1 conclusion at $0 with arm-labelling comparability with t0027 / t0028 preserved
by construction: 12 / 130 = 9.23% discordance, 6 arm-A wins and 6 arm-B wins, two-sided
exact-binomial McNemar p = 1.0000, with a SWE-bench arm-B advantage and a FrontierScience arm-A
advantage that cancel in aggregate. Options (b) and (c) replace the policy under each arm label and
turn any rerun into a verdict on a new experiment, while option (d) forecloses the verdict that (a)
can deliver immediately.

## Sources

* Task: `t0031_rq1_rq4_no_new_api_salvage`
* Task: `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
* Task: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`
* Task: `t0028_brainstorm_results_8`
* Task: `t0029_rq1_discordance_rich_resample`
* URL: https://openai.com/api/pricing/
* URL: https://ai.google.dev/gemini-api/docs/pricing
* URL: https://www.anthropic.com/pricing
