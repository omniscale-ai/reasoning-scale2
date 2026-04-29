# Brainstorm Session 3

## Context

Wave 2 (t0004 brainstorm + t0005, t0006, t0007) merged at $0.06 total cost. The literature survey,
benchmark download, annotation pilot v1, and both scope-aware / scope-unaware libraries are
complete. The project is poised for the first Phase 2 result — but the v1 annotation schema has a
structural gap that must be fixed first.

## Schema gap discovered

While modelling A/C condition prompts on the `is_bored` (HumanEval/91) row, we found that the v1
annotation schema is **flat**: `subtask` is a list of strings, `atomic` is a list of strings, and
there is **no encoded edge** mapping atomics to their parent subtask. For the
`hierarchical-annotation-v1` smoke harness this forces one of three orderings — none of them
faithful to how humans actually reason hierarchically — and undermines the cleanliness of the
A-vs-B-vs-C contrast in the planned Phase 2 smoke test.

The fix is a tree-shaped v2 schema:

```json
{
  "hierarchy": {
    "global": "...",
    "subtasks": [
      {"subtask": "...", "atomics": ["...", "..."]},
      ...
    ],
    "global_atomics": ["..."]
  }
}
```

This change is **inserted as the new ASAP task** (t0009) before any of the previously-planned wave 3
tasks can build on it.

## Decisions

Four new tasks created, all `not_started`. Three are parallel-safe; one waits on the others:

* `t0009_hierarchical_annotation_v2` (covers `S-0005-01` partial + `S-0005-02` + new schema finding)
  — re-annotate all 115 rows under the tree schema with full problem text. **No deps.**
* `t0010_matched_mismatch_library` (covers `S-0007-01`) — matched-mismatch (C) library; reuses
  t0007's `TRAJECTORY_RECORD_FIELDS`. Schema-independent. **No deps.**
* `t0011_metric2_calibration_aggregator` (covers `S-0002-02`) — Xiong2024 verbalized-confidence
  + 3-sample self-consistency aggregator. Schema-independent. **No deps.**
* `t0012_phase2_abc_smoke_frontierscience` (covers `S-0006-03`, `S-0007-02`, `S-0005-06`) — first
  end-to-end Phase 2 A/B/C run on the FrontierScience subset of the **v2** dataset. **Deps**: t0009,
  t0010, t0011.

## Why this wave

Three tasks unblock the headline experiment:

* t0009 fixes the schema so the harness can drive granularity transitions naturally (depth-first by
  subtask in v2) instead of by an artificial phase walk over flat lists.
* t0010 provides the C condition without which RQ5 (sub-hypothesis 2) cannot be tested.
* t0011 implements Metric 2; without it the smoke test can only report Metric 1.

t0012 is the first run that produces a directional A/B/C signal on a real benchmark. It is
deliberately scoped as a smoke test (N=28 on hierarchy-complete FS-Olympiad rows, single provider
Anthropic, paired across conditions) rather than a definitive experiment. The follow-up
multi-provider replication (Gemini + OpenAI keys are now available) is queued for the next
brainstorm.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03; demoting four high-priority access/infrastructure suggestions to medium) — flagged
  earlier but explicitly deferred to keep this session focused on the v2 ASAP work.
* Multi-provider (Gemini, OpenAI) replication of the smoke test — deferred until t0012 produces a
  single-provider headline result.
* Annotation v2 row-count expansion to ≥200 (covered by S-0005-01 in part; t0009 only re-encodes the
  existing 115 rows, not new annotation work).
* SWE-bench Docker harness, ServiceNow provisioning, FrontierMath access negotiation.
