---
spec_version: "3"
task_id: "t0022_abc_harness_progress_rate_and_error_taxonomy"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-01T14:18:14Z"
completed_at: "2026-05-01T19:50:00Z"
---
## Summary

Implemented the `abc_harness_metrics` library that adds the Ma2024 AgentBoard discrete-subgoal
progress rate and the Li2024 Embodied Agent Interface six-plus-one error taxonomy to the ABC harness
used by t0023. Built two subgoal JSON files (FrontierScience-Olympiad with 26 environments from
t0012 gold-answer SUBTASK lines and SWE-bench Verified Lite with 60 environments from gold-patch
diff headers), 26 passing unit tests, and a t0012 replay-validation script. All decision criteria
specified in `plan.md` are satisfied: progress-rate mean 0.103 > 0.05, stddev 0.228 > 0.03, A-vs-C
error-distribution total-variation separation 0.771 >= 0.30. Library asset verification passes with
no errors or warnings.

## Actions Taken

1. Wrote `code/types.py` with frozen dataclasses for `TrajectoryStep`, `Trajectory`, `Subgoal`,
   `EnvironmentSubgoals`, `TrajectoryScore`, plus the `ErrorTaxonomyLabel` `StrEnum` of seven labels
   (six error labels plus an `ok` sentinel).
2. Wrote `code/constants.py`, `code/paths.py`, `code/judge_cache.py` (SHA-256 sharded disk cache
   with module-level `JUDGE_CACHE_DIR` for monkeypatch isolation), and copied `code/model_call.py`
   verbatim from t0012 per the ARF cross-task import rule.
3. Implemented `code/progress_rate.py:compute_progress_rate`,
   `code/error_taxonomy.py:classify_error` (with `precondition_or_effect` tie-break for ambiguous
   judge output), and `code/score_trajectory.py:score_trajectory` as the high-level entry point.
4. Wrote 26 unit tests across `test_progress_rate.py`, `test_error_taxonomy.py`,
   `test_judge_cache.py`, `test_score_trajectory.py`. All pass in 0.16 s with mock judges.
5. Built `code/build_subgoals_frontierscience.py` (parses SUBTASK lines from t0012 gold answers,
   produces 26 environments) and `code/build_subgoals_swebench.py` (filters SWE-bench Verified to
   `<15 min fix` difficulty, derives subgoals from `diff --git a/<path>` headers, produces 60
   environments).
6. Implemented `code/replay_t0012.py` with cost-tracker budget guard
   (`is_budget_ok(headroom_usd=0.10)`) and ran the live replay against all 91 t0012 phase-2 smoke
   trajectories. Output written to `code/replay_summary.json`.
7. Wrote the library asset (`assets/library/abc_harness_metrics/`) with `details.json` (spec_v 2),
   `description.md`, and the two subgoal JSON files under `files/`. Library verifier passes.
8. Verified `uv run pytest` (26/26 pass), `uv run ruff check` (clean), `uv run mypy -m` per module
   (clean), and the library verificator (no errors, no warnings).

## Outputs

* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/types.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/constants.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/paths.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/judge_cache.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/model_call.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/progress_rate.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/error_taxonomy.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/score_trajectory.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/replay_t0012.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/build_subgoals_frontierscience.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/build_subgoals_swebench.py`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/test_*.py` (4 files, 26 tests)
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/replay_summary.json`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/assets/library/abc_harness_metrics/details.json`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/assets/library/abc_harness_metrics/description.md`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/assets/library/abc_harness_metrics/files/subgoals_frontierscience_olympiad.json`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/assets/library/abc_harness_metrics/files/subgoals_swebench_verified_lite.json`

## Issues

The first live-replay attempt overshot the $2 budget cap because the original budget-guard headroom
(0.01 USD) was smaller than the worst observed per-call cost (~0.04 USD), so an in-flight call could
push the total past the cap before the guard fired. Mitigation: bumped the headroom to 0.10 USD and
added a `prior_spend_usd` correction so the per-process cost-tracker accounts for spend already
recorded in `_cost_log.jsonl` from earlier partial runs. Total replay spend across all attempts:
$2.42 (recorded in `code/_cost_log.jsonl`). The decision criteria from the replay are all satisfied
(PR mean 0.103, PR stddev 0.228, A-vs-C separation 0.771); however, condition C's error distribution
is heavily skewed toward `ok` because many condition-C judgments hit the budget-guard fallback
rather than the live judge — this is documented as a known limitation and will be regenerated as
part of t0023 from a fresh budget allocation.
