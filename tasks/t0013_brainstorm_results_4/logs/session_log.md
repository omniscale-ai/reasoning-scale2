# Brainstorm Session 4 — Full Transcript

## Project State Presented

* Tasks: 11 completed (t0001-t0011), 1 in_progress (t0012). 0 not_started.
* Cost: $9.16 / $100 (~9.2%).
* Suggestions: 17 high-priority uncovered remained after Round 1 of t0008 brainstorm 3.

Key findings carried in:

* t0009 reports +58 pp v2-vs-v1 judge accept rate, but the annotation provider was swapped from
  Sonnet (v1) to Haiku (v2) mid-task. The +58 pp number conflates the tree-schema upgrade with the
  model swap.
* t0009's dataset labels Mind2Web rows as `WorkArena++` and HumanEval rows as `tau-bench`. The two
  proxy benchmarks need relabeling before any downstream consumer (or the t0012 in-flight smoke)
  reports per-benchmark numbers.
* t0010 (matched-mismatch C library) and t0011 (Metric 2 calibration) shipped at $0 with full test
  coverage (14/14 and 25/25 respectively).
* t0012 is in_progress with the FrontierScience-only filter — its results are unaffected by the
  proxy-benchmark relabel, so no t0012 modification is needed.

## Clarification Questions

Skipped — researcher's intent was clear from earlier context and the messages on the same day: fix
the v2 confound and the proxy-benchmark labels before t0012 finishes, prune the high-priority
backlog, defer multi-provider replication.

## Discussion — Round 1: New Tasks

AI proposed two parallel pre-Phase-2 tasks:

1. `t0014_v2_annotator_sonnet_rerun` — covers `S-0009-01`. Re-run v2 annotator with Sonnet on the
   same 115 rows; judge with the same haiku judge on the same stratified sample. Compare per-
   benchmark accept rate against v2-haiku to isolate the schema component. Budget ~$5. No deps.
2. `t0015_correct_proxy_benchmark_labels` — covers `S-0009-06` variant b. Write a correction file
   against the t0009 dataset asset that renames `WorkArena++` → `Mind2Web` and `tau-bench` →
   `HumanEval` with a one-paragraph rationale. No new annotation, no API spend. Budget $0. No deps.

Researcher: "сделай S-0009-01 Sonnet rerun и S-0009-06 (вариант b)" — confirmed both.

Researcher: "бюджет 10 долларов запускаем параллельно но t0012 пзже S-0010-0 оставляем как
Phase-2-followup после первого результата" — set wave budget cap to $10, parallel launch for t0014
and t0015, keep t0012 in_progress, keep S-0010-01 active as Phase-2 follow-up.

## Discussion — Round 2: Suggestion Cleanup

AI proposed Round 2 cleanup deferred from brainstorm 3 plus new redundancies surfaced after t0009-
t0011 landed.

Five rejections:

* `S-0002-04` ↔ duplicate of `S-0003-01` (FrontierMath access negotiation).
* `S-0003-02` ↔ duplicate of `S-0002-03` (ServiceNow lab provisioning).
* `S-0005-06` covered by t0012 (Phase 2 A/B/C smoke FrontierScience scope).
* `S-0007-02` covered by t0012 (matched-mismatch C condition is exercised inside t0012).
* `S-0005-01` superseded by `S-0009-03` + `S-0009-05` (the v2 follow-ups now own the scaling and
  human-review track; the v1-era "row-count expansion" framing is stale).

Three reprioritizations (high → medium):

* `S-0002-01` (pass^k metric — replication infrastructure; off the headline path).
* `S-0002-05` (SWE-bench Docker harness — compute infrastructure; off the headline path).
* `S-0006-01` (tool registries — registry instrumentation; off the headline path).

Researcher: "отклоняй чо хочешь" — delegated decision authority for both rejections and
reprioritizations.

## Discussion — Round 3: Confirmation

AI summarized the final list:

* New tasks: 2 (t0014 budget ~$5, t0015 budget $0).
* Suggestions rejected: 5.
* Suggestions reprioritized: 3.
* Suggestions kept active: S-0010-01 (Phase-2 follow-up), S-0009-01 (covered by t0014).
* Tasks cancelled or updated: 0.
* Wave budget cap: $10. Parallelism: t0014 || t0015. t0012 stays in_progress and is unmodified.

Researcher: "go" — authorized the entire remaining sequence (Phases 3-6).

## Decisions Summary

1. Create `t0014_v2_annotator_sonnet_rerun` (no deps, ~$5).
2. Create `t0015_correct_proxy_benchmark_labels` (no deps, $0).
3. Write 5 rejection correction files (`S-0002-04`, `S-0003-02`, `S-0005-06`, `S-0007-02`,
   `S-0005-01`).
4. Write 3 reprioritization correction files (`S-0002-01`, `S-0002-05`, `S-0006-01`).
5. Keep `S-0010-01` active as Phase-2 follow-up.
6. Defer multi-provider replication until t0012 produces a single-provider headline result.
7. After PR merge, fork two parallel `/execute-task` agents for `t0014` and `t0015`. `t0012` stays
   in_progress and is not modified by this session.
