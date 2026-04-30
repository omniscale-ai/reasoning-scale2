# Brainstorm Session 4

## Context

Three of the four wave 3 tasks completed: t0009 (v2 tree-schema annotation), t0010 (matched-
mismatch library), t0011 (Metric 2 calibration aggregator). t0012 (Phase 2 A/B/C smoke on
FrontierScience) is `in_progress`. Total spend stands at roughly $9.16 of the $100 project budget.

Two issues surfaced in t0009 that the headline experiment cannot rest on cleanly:

1. **Schema-vs-model confound.** t0009 reports a +58 pp judge-acceptance delta over v1, but the
   annotation provider was swapped from Claude Sonnet (v1) to Claude Haiku (v2) midway. The +58 pp
   number conflates the tree-schema upgrade with the model swap. Without a Sonnet rerun on the v2
   schema, we cannot say whether the schema actually moved acceptance — and the "v2 unblocks Phase
   2" story has a load-bearing dependency on that being a real schema effect.
2. **Proxy-benchmark provenance.** The v2 dataset labels two of its four benchmarks "WorkArena++"
   and "tau-bench". The underlying rows are actually Mind2Web and HumanEval rows used as proxies.
   Downstream consumers (and the t0012 in-flight smoke) read the labels at face value, which would
   misrepresent results once the headline numbers are reported.

Suggestion backlog also accumulated: 17 high-priority suggestions across S-0001-* through S-0011-*,
several with overlap and a few that the t0012 in-flight task already covers.

## Decisions

Two new tasks created, both `not_started`, parallel-safe, no dependencies on each other:

* `t0014_v2_annotator_sonnet_rerun` (covers `S-0009-01`) — re-run the v2 annotator on the same 115
  rows using `claude-sonnet-4-6`, judge with the same haiku judge on the same stratified sample.
  Compare per-benchmark accept rate against v2-haiku to isolate the schema component of the +58 pp
  delta. Budget: ~$5.
* `t0015_correct_proxy_benchmark_labels` (covers `S-0009-06` variant b) — write a correction file
  against the t0009 dataset asset that renames the `WorkArena++` benchmark label to `Mind2Web` and
  the `tau-bench` benchmark label to `HumanEval`, with a one-paragraph rationale. No new annotation,
  no API spend. Budget: $0.

Wave budget cap: **$10** combined for both tasks (t0014 ~$5; t0015 ~$0; ~$5 of headroom).

Parallelism: t0014 and t0015 launch in parallel. t0012 stays in_progress and is not modified by this
session — its FrontierScience filter is unaffected by the proxy-benchmark relabel.

## Suggestion cleanup

Five rejections (duplicates or already covered by an in-flight task):

* `S-0002-04` — duplicate of `S-0003-01` (FrontierMath access negotiation).
* `S-0003-02` — duplicate of `S-0002-03` (ServiceNow lab provisioning).
* `S-0005-06` — covered by t0012 (Phase 2 A/B/C smoke FrontierScience scope).
* `S-0007-02` — covered by t0012 (matched-mismatch C condition is exercised inside t0012).
* `S-0005-01` — superseded by `S-0009-03` + `S-0009-05` (the v2 follow-ups are now the canonical
  scaling and human-review track, not the v1-era "row-count expansion" framing).

Three reprioritizations (high → medium):

* `S-0002-01` — pass^k metric (replication infrastructure; not on the headline path until after the
  smoke).
* `S-0002-05` — SWE-bench Docker harness (compute infrastructure; not on the headline path).
* `S-0006-01` — tool registries (registry instrumentation; not on the headline path).

Two follow-ups intentionally **not** corrected:

* `S-0010-01` — kept active as a Phase-2 follow-up to land after t0012's first headline result.
* `S-0009-01` — covered by `t0014`, so it stays active and the new task references it through
  `source_suggestion`.

## Out of scope this session

* Multi-provider replication of t0012 (Gemini, OpenAI). Deferred until t0012 produces a single-
  provider headline result.
* v2 row-count expansion beyond 115 rows. Tracked under `S-0009-03`/`S-0009-05`.
* Human review pass over v2 annotations.
* SWE-bench Docker harness, ServiceNow provisioning, FrontierMath access negotiation.
* Any change to t0012 itself (in_progress; immutable for this session).
