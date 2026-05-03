# RQ1 path decision comparison table

Generated from `decision_inputs.json` by `build_comparison_table.py`. All four required execution
paths under the permanent no-Anthropic constraint.

| Option | USD point estimate | Validity / power risk | Comparability with t0027 / t0028 | Time-to-result |
| --- | ---: | --- | --- | --- |
| (a) existing-results-only verdict | $0.00 | Aggregate McNemar p=1.0000 on N=130 (12 discordant); verdict is null aggregate with documented per-stratum interaction. No new sampling. | Trivially preserved; no rerun, t0027 fixed-arm convention untouched. | Hours (analysis-only; no compute). |
| (b) local / open-weight rerun | $0.00 (hardware-bound) | Same structural underpowering as (c) at the t0029 cap; open-weight policy quality is unbounded variance vs Sonnet baseline. | Lost: replaces the policy under arm A or arm B; verdict is on a different model, not on the t0027 arms. | Days to weeks (engineering + GPU provisioning). |
| (c) alternative paid provider (GPT-5 / Gemini 2.5 Pro) | $0.07 / pair x 218 = $15.26 (band $15-$25) | Power < 0.80 unless true p1 >= 0.75 (per t0031 power grid); cap-sized rerun still likely null. | Lost: GPT-5 or Gemini 2.5 Pro plays arm B in place of Claude Sonnet 4.6; arm label preserved, policy under label changed. | About 1-2 days (provider onboarding + 218-pair sweep). |
| (d) project-level underpowered / provider-blocked stop | $0.00 | No verdict produced; forecloses analysis that (a) can already deliver. | Trivially preserved (no rerun); but the comparability is moot without a verdict. | Immediate (hard stop). |
