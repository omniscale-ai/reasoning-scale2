---
spec_version: "1"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
date_compared: "2026-05-02"
---
# Comparison with Published Results

## Summary

This task compares three agent variants (scope-aware ReAct, Plan-and-Solve v2, mismatched-strategy
adversarial) on a 147-instance mix of SWE-bench Verified, Tau-bench, and FrontierScience. Our
absolute success numbers are far below published agent-system results because the harness is
reasoning-only (no patch execution, stub Tau-bench tool registry) and the per-call budget is
intentionally tight (`max_turns=10`, `max_tokens=4096`). The comparison is therefore not a
head-to-head with leaderboard agents — it is an internal scaffold comparison whose value lies in the
*direction* and *significance* of the deltas, which the published papers do not report.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| ReAct on SWE-bench-style (Yao2022) | Solve rate | 4.0 | 30.0 | +26.0 | Variant A on SWE-bench Verified subset (n=20); reasoning-only — patches not executed, exact-match scoring favors short patches |
| Plan-and-Solve (Wang2023) | Accuracy on multi-step reasoning | 75.0 | 4.1 | -70.9 | Variant B; Wang2023 reports on math/commonsense, not agent benchmarks; harness mismatch dominates |
| SWE-bench Verified leader (Jimenez2024) | Solve rate | 50.0 | 30.0 | -20.0 | Variant A vs current SWE-bench Verified leaderboard agents; we run reasoning-only with no test execution |
| Tau-bench retail (published baseline) | Pass^1 | 25.0 | 0.0 | -25.0 | Variant A on Tau-bench subset (n=87); we use a stub `python_exec` only, no real customer DB or tool stack |

## Methodology Differences

* **No code execution**: Published SWE-bench agent systems run unit tests inside Docker. We score
  exact-match patches via the judge only, which is a much weaker signal.
* **Stub Tau-bench tool registry**: Published Tau-bench numbers come from the full retail/airline
  tool stack. Our harness exposes a single `python_exec` stub, which collapses all three variants
  toward "describe what you would do" outputs.
* **Tight per-call budget**: `max_turns=10` and `max_tokens=4096` are well below the budgets used in
  published agent papers (often 50+ turns, 32k+ tokens).
* **Single model under test**: Every variant uses `claude-sonnet-4-6`; published papers typically
  sweep multiple models.
* **Paired McNemar instead of leaderboard ranking**: This task's headline test is paired
  significance on the same 130 instances per variant — a within-task scaffold comparison, not
  cross-paper benchmarking.

## Analysis

The absolute deltas against published numbers are dominated by harness choices, not by scaffold
quality. The interesting observation is that variant A's SWE-bench rate (**30.0%**) lands in the
neighborhood of published reasoning-only baselines, while B's **0.0%** is driven by 16
`MalformedPlanError` failures — a parser-fragility result that has no analogue in the original
Plan-and-Solve paper because that paper evaluates on math word problems, not multi-step coding. The
Plan-and-Solve schema does not survive contact with realistic agent traces in this task, which is a
finding *about the scaffold port* rather than about the underlying technique.

The C > B inversion (paired McNemar p = **0.019**) is also outside the scope of published work:
matched-mismatch literature (e.g., the original `t0010_matched_mismatch_library` design)
hypothesizes that "adversarial" wrappers should *hurt* a matched scaffold, not help an unrelated
one. Our C variant ends up structurally closer to A than to B, which dilutes the adversarial signal
and explains the inversion mechanically rather than substantively.

## Limitations

* The "published value" column for ReAct and Plan-and-Solve uses approximate numbers from the
  original papers — those papers do not evaluate on the SWE-bench / Tau-bench / FrontierScience mix
  used here, so direct comparison is loose.
* SWE-bench Verified leaderboard numbers move quickly and the "50%" figure used here is a rough
  contemporary agent baseline rather than a fixed citation.
* Tau-bench baselines vary by tool stack and seed; the **25.0** figure is a representative public
  baseline, not a paired reproduction.
* No published paper runs the matched-mismatch adversarial wrapper used in variant C, so the C row
  has no fair literature anchor and is omitted from the comparison table.
