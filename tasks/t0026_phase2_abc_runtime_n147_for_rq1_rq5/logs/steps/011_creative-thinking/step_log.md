---
spec_version: "3"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
step_number: 11
step_name: "creative-thinking"
status: "completed"
started_at: "2026-05-02T14:31:05Z"
completed_at: "2026-05-02T14:35:00Z"
---
## Summary

Out-of-the-box reading of the unexpected pattern in the runtime sweep results: A and B are
statistically tied while C — the *adversarial mismatched* baseline — significantly outperforms B on
the paired N=130 set. This step records alternative explanations for the inversion and the
subset-specific direction reversals (SWE-bench: A best; FrontierScience: C best) so the results step
can choose which lines of analysis to surface.

## Actions Taken

1. Reviewed `results/metrics.json`, `data/mcnemar_results.json`, `data/calibration.json`, and a
   sample of trajectories from each variant to look for systematic differences in failure modes.
2. Brainstormed five alternative interpretations of the headline inversion (C > B) and three
   subset-level explanations.
3. Recorded the four most promising follow-up angles for the suggestions step.

## Outputs

* This step log captures the creative-thinking output. Specific candidate explanations are
  enumerated below; the most actionable ones are flagged for the results write-up and the
  suggestions list.

### Candidate explanations for C > B (4 vs 15 discordant; p = 0.019)

1. **Adversarial-mismatch acts as a noise injection that breaks Plan-and-Solve's brittle plan
   schemas.** B's `MalformedPlanError` count was 16 (12% of B's runs). When B fails to produce a
   parseable plan, the run is recorded as a hard error. C's adversarial wrapper bypasses the
   plan-and-solve schema entirely (it delegates to `scope_aware_react` under a perturbed strategy
   label), so it never trips the plan parser. The "adversarial" label is partly cosmetic — it ends
   up running a ReAct-shaped loop without B's plan-schema overhead.
2. **The judge rewards short, definite answers.** Both A and B tend to emit reasoning chains plus a
   structured final block; C's adversarial path is more likely to terminate with a single short
   string. On FrontierScience (where C wins 17.5% vs 0% for A), the judge may be accepting
   confident-but-shallow answers that A's longer chains would have dragged into "couldn't conclude"
   territory. This is a judge-bias hypothesis worth checking against the 91.7% program-truth
   agreement (the gap is concentrated where program truth is unavailable).
3. **B's confidence overhead is wasted compute.** B is the only variant that estimates
   `final_confidence`, and ECE = 0.43 says the estimates are essentially uninformative. Some of B's
   per-instance budget goes toward an unused calibration scaffold. Stripping the confidence pass
   might recover B's success rate by ~1-2 points.
4. **The "mismatch" name is misleading.** Variant C in this implementation is
   `delegate = scope_aware_react` with `mismatch_strategy = adversarial`. So C is structurally
   closer to A than to B. A vs C McNemar (not run by `mcnemar.py` because we only need RQ5's two
   pairs) would likely show A ≈ C. The result we have is consistent with C being a "scope-aware
   ReAct with a slightly noisier system prompt," not a fundamentally weaker baseline.
5. **17 missing instances bias the paired set.** The same 17 instances per variant were skipped
   (pre-existing trajectory files from a corrupted partial run). If the skipped set is enriched in
   instances where A or B had structural advantages, we lose that signal. The variants share the
   same 130 ids so the *relative* comparison is valid, but the *absolute* success rates may
   understate A and B.

### Subset-level patterns

* **SWE-bench: A 30%, B 0%, C 5%.** A is the only variant with a positive SWE-bench rate. SWE is the
  only subset with explicit `expected_patch` ground truth, where program-truth scoring rewards
  exact-match patches that A's atomic-granularity ReAct can produce. B's plan-and-solve overhead
  burns the 10-turn budget on planning before patches converge.
* **Tau-bench: all near zero.** Tau-bench is tool-use heavy; we ran it without a real tool registry
  (stub `python_exec` only). All three variants degrade to "describe what you would do," and the
  judge is strict about `_judge_tau_bench` action checks.
* **FrontierScience: C 17.5%, B 10%, A 0%.** Olympiad-style problems reward concise final numerical
  answers. C's shorter trajectories happen to land more often on a single integer guess. A's longer
  chains over-think and emit non-final-answer text.

### Most actionable angles to carry into results / suggestions

* Run an ablation of B without the confidence head to see if ECE-induced waste explains the gap.
* Re-run with a real Tau-bench tool registry; the current zero rate is a harness artifact.
* Replace C with a clean "Plan-and-Solve without confidence" baseline so RQ5's third tier is
  methodologically distinct from A.
* Refresh the 17 skipped instances on a clean restart to confirm the paired set is unbiased.

## Issues

No issues encountered.
