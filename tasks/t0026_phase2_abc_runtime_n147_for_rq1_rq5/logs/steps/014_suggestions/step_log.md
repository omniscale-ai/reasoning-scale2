---
spec_version: "3"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-02T14:44:55Z"
completed_at: "2026-05-02T14:50:00Z"
---
## Summary

Filled in `results/suggestions.json` with six concrete follow-ups derived directly from this task's
findings: fixing variant B's brittle plan parser (high), redesigning the matched-mismatch wrapper so
C is structurally distinct from A (high), recalibrating B's `final_confidence` (medium), wiring a
real Tau-bench tool registry (medium), repeating the grid on Opus (medium), and recovering the 17
missing paired instances (low). Each suggestion cites the specific metric or failure-mode evidence
from this run and prescribes the exact paired re-test that would resolve it. The verificator passes
with zero errors and zero warnings.

## Actions Taken

1. Read `arf/specifications/suggestions_specification.md` to confirm required fields, the
   `S-XXXX-NN` id format, and the allowed `kind`, `priority`, and `status` values.
2. Listed `meta/categories/` to use only existing category slugs.
3. Wrote six suggestions into `results/suggestions.json`, each grounded in a specific number from
   this task's results: B's 16 `MalformedPlanError` failures, the C > B McNemar p = 0.019, the
   `final_confidence_ece = 0.43` on n = 49, the harness-bound Tau-bench floor, the Sonnet-only
   single-model risk, and the 17-instance paired-set shortfall.
4. Ran `verify_suggestions.py` and confirmed PASSED — no errors or warnings.

## Outputs

* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/suggestions.json` (6 suggestions)

## Issues

No issues encountered.
