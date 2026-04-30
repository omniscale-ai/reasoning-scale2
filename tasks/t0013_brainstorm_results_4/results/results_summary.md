# Brainstorm Session 4 — Results Summary

## Summary

Fourth brainstorm produced two new not-started tasks (t0014 and t0015) and applied eight correction
files for the Round 2 cleanup deferred from brainstorm 3. The two tasks address the schema-vs-model
confound and proxy-benchmark provenance issues surfaced by t0009. Wave budget cap: $10. Both new
tasks are parallel-safe; t0012 stays in_progress and unaffected.

## Session Overview

* **Date**: 2026-04-30
* **Context**: Triggered after t0009-t0011 merged with $9.16 / $100 spent. t0012 is in_progress.
  t0009 reported a +58 pp v2-vs-v1 judge accept rate but the annotation provider was swapped from
  Sonnet (v1) to Haiku (v2), so the headline delta is confounded with the model swap. The v2 dataset
  also labels two proxy benchmarks under their proxy targets' names instead of the true source
  corpora.
* **Prompt**: Resolve both pre-Phase-2 issues so t0012's headline experiment can rest on a clean v2
  foundation, and prune the 17-suggestion high-priority backlog.

## Decisions

1. **Create `t0014_v2_annotator_sonnet_rerun`** (covers `S-0009-01`). Re-run the v2 annotator on the
   same 115 rows with `claude-sonnet-4-6`; judge with the same haiku judge on the same stratified
   sample. Compare per-benchmark accept rate against v2-haiku. Budget ~$5. No deps.
2. **Create `t0015_correct_proxy_benchmark_labels`** (covers `S-0009-06` variant b). Write a
   correction file against the t0009 dataset asset that renames `WorkArena++` to `Mind2Web` and
   `tau-bench` to `HumanEval` with a one-paragraph rationale. No API spend. No deps.
3. **Reject 5 suggestions** as duplicates or already-covered:
   * `S-0002-04` ↔ `S-0003-01` duplicate (FrontierMath access).
   * `S-0003-02` ↔ `S-0002-03` duplicate (ServiceNow lab provisioning).
   * `S-0005-06` covered by t0012 (Phase 2 A/B/C smoke FrontierScience).
   * `S-0007-02` covered by t0012 (matched-mismatch C condition).
   * `S-0005-01` superseded by `S-0009-03` + `S-0009-05` (v2 follow-ups now own the scaling track).
4. **Reprioritize 3 suggestions** from high to medium (off the headline path):
   * `S-0002-01` (pass^k metric).
   * `S-0002-05` (SWE-bench Docker harness).
   * `S-0006-01` (tool registries).
5. **Keep `S-0010-01`** active as a Phase-2 follow-up to land after t0012's first headline result.
6. **Defer multi-provider replication** (Gemini + OpenAI) until t0012 produces a single-provider
   headline.
7. **Wave budget cap**: $10. Parallelism: t0014 and t0015 launch in parallel. t0012 stays
   in_progress and is not modified.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 2 |
| Suggestions covered by new tasks | 2 |
| Suggestions rejected | 5 |
| Suggestions reprioritized | 3 |
| Corrections written | 8 |
| Answer assets produced | 0 |

## Verification

* `verify_task_file` — t0013, t0014, t0015 PASSED.
* `verify_corrections` — t0013 PASSED (8 correction files).
* `verify_suggestions` — t0013 PASSED (no new suggestions).
* `verify_logs` — t0013 PASSED (LG-W001/W005/W007/W008 acceptable for a planning task).

## Next Steps

After this PR merges, fork two parallel `/execute-task` background agents for `t0014` and `t0015`.
`t0012` continues independently. Plan brainstorm 5 once t0012 lands plus at least one of t0014 /
t0015 — to address multi-provider replication, v2 row-count expansion, and any v3 schema iteration
the deconfound result motivates.
