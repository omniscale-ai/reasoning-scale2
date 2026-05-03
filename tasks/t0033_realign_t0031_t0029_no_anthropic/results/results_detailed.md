# T0031/T0029 NO-ANTHROPIC REALIGNMENT — CORRECTIONS APPLIED

## Summary

Two correction files realign t0031's high-priority follow-up suggestions to the permanent
no-Anthropic reality, and a direct cross-task edit of `t0029_rq1_discordance_rich_resample` records
its true state (`intervention_blocked` on permanent provider unavailability) along with an
intervention markdown file. No paid spend, no remote machines, no metrics, and no new follow-up
suggestions. The replacement-path decision for RQ1 is owned by
`t0032_no_anthropic_rq1_path_decision`.

## Methodology

* **Machine**: local laptop. No remote machines provisioned.
* **Runtime**: < 5 minutes of agent time across all 13 steps (3 active, 6 skipped, 4 reporting).
* **Wall-clock**: started 2026-05-03T13:07:33Z, implementation complete 2026-05-03T13:10:59Z.
* **Cost**: $0.00 paid-API spend. The task only edits framework artefacts.
* **Workers**: single-threaded.

## Inputs

* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/suggestions.json` — the canonical source of
  `S-0031-01`, `S-0031-02`, `S-0031-03`. Read-only; not modified.
* `tasks/t0029_rq1_discordance_rich_resample/task.json` — `status` field directly edited.
* `tasks/t0032_no_anthropic_rq1_path_decision/task.json` — read-only reference; the new `S-0031-01`
  description points at this task as the no-Anthropic decision owner.
* `arf/specifications/corrections_specification.md` (v3) — schema for the two correction files.

## Implementation Detail

### `corrections/suggestion_S-0031-01.json` (`C-0033-01`)

* `target_kind`: `suggestion`
* `target_task`: `t0031_rq1_rq4_no_new_api_salvage`
* `target_id`: `S-0031-01`
* `action`: `update`
* `changes`: replaces both `title` and `description`. New title: "Decide a no-Anthropic RQ1
  execution path." New description redirects the suggestion to t0032 and enumerates the four options
  that task evaluates.
* `priority` and `kind` are deliberately not in `changes` so the original `priority: high` and
  `kind: experiment` are preserved.

### `corrections/suggestion_S-0031-02.json` (`C-0033-02`)

* `target_kind`: `suggestion`
* `target_task`: `t0031_rq1_rq4_no_new_api_salvage`
* `target_id`: `S-0031-02`
* `action`: `update`
* `changes`: rewrites `description` only. The new description makes the cap-reconsideration
  explicitly conditional on a future non-Anthropic paid execution path. It also specifies that if
  t0032 picks option (a) "existing-results-only verdict" or option (d) "project-level stop", a
  follow-up correction should mark this suggestion `rejected`.
* `priority: high` and `kind: evaluation` preserved.

### `tasks/t0029_rq1_discordance_rich_resample/task.json` (cross-task direct edit)

* Field changed: `status` from `in_progress` to `intervention_blocked`.
* Fields preserved: `start_time` (`2026-05-03T09:55:36Z`), `end_time` (`null`), `dependencies`,
  `expected_assets`, `task_types`, `source_suggestion`.
* `task_description.md` deliberately not modified — the locked pre-registered plan stays on the
  record as historical.

### `tasks/t0029_rq1_discordance_rich_resample/intervention/anthropic_provider_unavailable.md`

New file. States that Anthropic provider access is unavailable indefinitely, names the locked $35
cap and pre-registered design as preserved-but-not-executable, transfers replacement-path ownership
to t0032, and documents resolution criteria (block stays under options a/d; may be re-opened or
replaced under options b/c).

## What is intentionally not done

* `S-0031-03` ("Fix the cost-tracker boundary that produces unknown parser-recovery") — untouched.
  It remains a valid medium-priority library suggestion independent of the Anthropic constraint.
* `t0030_rq4_info_asymmetry_stratification` — not launched. Its preconditions are gated on whichever
  path t0032 chooses.
* `t0032_no_anthropic_rq1_path_decision` — read-only here. Its scope is owned by itself.
* `task_description.md` of t0029 — not modified.

## Cross-Task Edit Justification

The corrections specification v3 (`arf/specifications/corrections_specification.md`) lists target
kinds `suggestion`, `paper`, `answer`, `dataset`, `library`, `model`, `predictions` — there is no
`task` target kind. The t0029 status flip therefore cannot be expressed as a correction file. The
framework-correct alternative is a direct edit of t0029's `task.json` from this task's branch. This
is permissible because t0029 has status `in_progress`, not `completed`, so rule 5 of `CLAUDE.md`
("nothing in a completed task folder may be changed; use the corrections mechanism in later tasks")
does not apply. The risks-and-fallbacks section of `task_description.md` documents what to do if
`verify_pr_premerge` rejects the cross-task edit (escalate to user, do not silently revert).

## Verification

* `verify_corrections t0033_realign_t0031_t0029_no_anthropic` — passed (0 errors, 0 warnings).
* `verify_task_dependencies t0033_realign_t0031_t0029_no_anthropic` — passed via prestep.
* `verify_task_file t0033_realign_t0031_t0029_no_anthropic` — passed at task creation (1 warning:
  TF-W005 `expected_assets` empty, expected for a correction task).
* Reporting-step verificators (`verify_task_results`, `verify_suggestions`, etc.) run in step 13.

## Limitations

* This task does not verify by running the aggregator that `S-0031-01` and `S-0031-02` are now
  presented in their corrected effective form. That happens automatically once the PR merges and
  `aggregate_suggestions` is re-run, and is left as the post-merge sanity check in the PR body.
* The intervention file is human-readable Markdown; there is no machine-readable schema enforcing
  intervention metadata in this project's framework version, so the file's structure is
  conventional.

## Files Created

* `corrections/suggestion_S-0031-01.json`
* `corrections/suggestion_S-0031-02.json`
* `tasks/t0029_rq1_discordance_rich_resample/intervention/anthropic_provider_unavailable.md`
* `results/results_summary.md`
* `results/results_detailed.md`
* `results/metrics.json`
* `results/suggestions.json`
* `results/costs.json`
* `results/remote_machines_used.json`

## Files Modified

* `tasks/t0029_rq1_discordance_rich_resample/task.json` — `status` field only.

## Next Steps

* `t0032_no_anthropic_rq1_path_decision` runs next and produces a single `answer` asset with the
  recommended RQ1 path. That decision determines whether `S-0031-02` activates or is auto-rejected
  by a follow-up correction.
* If t0032 picks option (a) or (d), a follow-up corrections task should mark `S-0031-02`
  `status: rejected`.
* No new suggestions are emitted from this task.
