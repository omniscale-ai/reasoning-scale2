---
spec_version: "2"
library_id: "abc_harness_metrics"
documented_by_task: "t0022_abc_harness_progress_rate_and_error_taxonomy"
date_documented: "2026-05-01"
---
# ABC Harness Metrics

## Metadata

* **Name**: ABC Harness Metrics
* **Version**: 0.1.0
* **Task**: `t0022_abc_harness_progress_rate_and_error_taxonomy`
* **Dependencies**: `datasets` (Hugging Face) for SWE-bench Verified ingestion only
* **Modules**: `code/progress_rate.py`, `code/error_taxonomy.py`, `code/score_trajectory.py`,
  `code/types.py`, `code/judge_cache.py`, `code/model_call.py`, plus subgoal builders.

## Overview

The ABC Harness Metrics library extends the ABC (single-step / decision-counter / hierarchical
agent) evaluation harness used by t0023 with two trajectory-level metrics that decouple "did the
agent finish the task" from "how good was the path to the answer". The goal is to make condition C
(hierarchical planning + decision counter) measurable on dimensions other than final-answer
correctness so that t0023's confirmatory ABC run can detect intermediate progress and characterize
failure modes.

The first metric is the discrete-subgoal-coverage form of the AgentBoard progress rate from Ma et
al. 2024. For each environment we declare 3-5 subgoals; for each subgoal we ask a judge model
whether any step in the trajectory hits it; the rate is the fraction of subgoals that flipped to
"hit" with an early-exit short-circuit. The reference paper reports Pearson rho > 0.95 versus human
ratings on a 1013-environment evaluation, exclusively for this discrete-coverage form.

The second metric is the six-plus-one error taxonomy from the Embodied Agent Interface (Li et al.
2024). Each step is classified into one of `hallucination`, `affordance`, `missing_step`,
`extra_step`, `wrong_order`, `precondition_or_effect`, or the project-added `ok` sentinel for
correct steps. The aggregator returns both the per-step labels and a `Counter` distribution; t0023
will use the distribution shape to test whether condition C produces a different mix of failure
modes than condition A (the alternative hypothesis behind hierarchical planning).

Both metrics are implemented offline-first: the judge call is a `Callable[[str], str]`, so unit
tests pass deterministic mocks while live runs use a CLI-backed callable produced by
`make_judge_call`. A SHA-256 disk cache keyed by
`(environment_id, trajectory_hash, prompt_key, prompt_payload)` ensures that t0023's confirmatory
run does not re-pay for trajectories already classified during t0022's validation pass.

## API Reference

### `compute_progress_rate` (`code/progress_rate.py`)

```python
def compute_progress_rate(
    *,
    trajectory: Trajectory,
    environment_subgoals: EnvironmentSubgoals,
    judge_model: str = JUDGE_MODEL_DEFAULT,
    cost_tracker: CostTracker | None = None,
    judge: Callable[[str], str] | None = None,
) -> float: ...
```

Returns the discrete-subgoal-coverage progress rate `(1/K) * sum_k 1{some step hits subgoal_k}`.
Iterates `(subgoal, step)` pairs in order and short-circuits each subgoal on the first `yes` from
the judge. Either `judge` (a callable) or `cost_tracker` (so a default judge can be constructed via
`make_judge_call`) must be supplied. Raises `ValueError` if both are `None`. Returns `0.0` when the
environment has no subgoals.

### `classify_error` (`code/error_taxonomy.py`)

```python
def classify_error(
    *,
    trajectory_step: TrajectoryStep,
    environment_state: dict[str, Any],
    judge_model: str = JUDGE_MODEL_DEFAULT,
    cost_tracker: CostTracker | None = None,
    judge: Callable[[str], str] | None = None,
    environment_id: str = "",
) -> ErrorTaxonomyLabel: ...
```

Classifies one trajectory step into exactly one of the seven `ErrorTaxonomyLabel` values. Ambiguous
or unparseable judge responses fall back to `ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT` per the
t0022 task spec tie-break rule (this prevents silent under-counting of the harder label while not
corrupting the distribution with garbage). The companion `parse_error_label(*, response)` function
is exported for use in research code.

### `score_trajectory` (`code/score_trajectory.py`)

```python
def score_trajectory(
    *,
    trajectory: Trajectory,
    environment: EnvironmentSubgoals,
    judge_model: str = JUDGE_MODEL_DEFAULT,
    cost_tracker: CostTracker | None = None,
    progress_judge: Callable[[str], str] | None = None,
    error_judge: Callable[[str], str] | None = None,
    environment_state: dict[str, Any] | None = None,
) -> TrajectoryScore: ...
```

Composes the two metrics. Returns a `TrajectoryScore` dataclass with `task_success`,
`progress_rate`, `step_errors` (tuple of one `ErrorTaxonomyLabel` per step), and
`error_distribution` (a `Counter` over labels).

### Types (`code/types.py`)

* `TrajectoryStep(turn_index, granularity, thought, action, observation, confidence)` — frozen
  dataclass matching the t0012 ABC harness step schema.
* `Trajectory(task_id, steps, task_success)` — wraps a tuple of steps with a final-answer flag.
* `Subgoal(subgoal_id, description)` — one milestone in an environment.
* `EnvironmentSubgoals(environment_id, subgoals)` — the list of subgoals declared per environment.
* `ErrorTaxonomyLabel(StrEnum)` — the seven canonical labels.
* `TrajectoryScore(task_success, progress_rate, step_errors, error_distribution)` — the output of
  `score_trajectory`.

### Disk cache (`code/judge_cache.py`)

`make_cache_key`, `cache_get`, `cache_put`, and `hash_trajectory_step` form the SHA-256 sharded disk
cache. The cache root is module-level (`JUDGE_CACHE_DIR`) so tests can monkeypatch it; live calls
write to `code/_cache/<2-hex>/<rest>.json`.

### CLI judge (`code/model_call.py`)

Copied verbatim from t0012 per the ARF cross-task import rule (no library imports across tasks).
`make_judge_call(model, cost_tracker, system_prompt, note)` returns a `Callable[[str], str]` that
shells out to the local `claude` CLI. `CostTracker(cap_usd)` enforces the $2 cap per
`MAX_BUDGET_USD`.

## Usage Examples

```python
from collections.abc import Callable

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    EnvironmentSubgoals, Subgoal, Trajectory, TrajectoryStep,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.score_trajectory import (
    score_trajectory,
)


def yes_judge(_prompt: str) -> str:
    return "yes"


def ok_judge(_prompt: str) -> str:
    return "ok"


traj = Trajectory(
    task_id="demo-1",
    steps=(
        TrajectoryStep(
            turn_index=0,
            granularity="atomic",
            thought="define the problem",
            action="thought_only",
            observation="",
            confidence=None,
        ),
    ),
    task_success=True,
)
env = EnvironmentSubgoals(
    environment_id="demo-1",
    subgoals=(Subgoal(subgoal_id="g1", description="state the problem clearly"),),
)
score = score_trajectory(
    trajectory=traj,
    environment=env,
    progress_judge=yes_judge,
    error_judge=ok_judge,
)
print(score.progress_rate, score.error_distribution)
```

For a live evaluation against the local Claude CLI, omit `progress_judge` and `error_judge` and pass
a `CostTracker(cap_usd=2.0)` instead. A complete end-to-end example lives in `code/replay_t0012.py`,
which validates the library on the t0012 phase-2 smoke trajectories.

## Dependencies

* **`datasets`** (Hugging Face) — used only by `code/build_subgoals_swebench.py` to pull the
  SWE-bench Verified split when regenerating
  `assets/library/abc_harness_metrics/files/subgoals_swebench_verified_lite.json`. The runtime
  metric code does not depend on it.
* All other code uses only the Python standard library and the project's existing `pydantic`,
  `numpy`, `pandas` stack.

## Testing

```bash
uv run python -u -m arf.scripts.utils.run_with_logs \
  --task-id t0022_abc_harness_progress_rate_and_error_taxonomy -- \
  uv run pytest tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/ -v
```

The 26 unit tests cover: progress-rate endpoints (0.0, 1.0, 0.5), short-circuit behaviour, empty
subgoal list, missing judge guard, every one of the seven `ErrorTaxonomyLabel` values, the parser
fallback to `precondition_or_effect`, the disk-cache round-trip and corruption recovery, the
trajectory-step hash stability, and a smoke test against a real t0012 prediction row to confirm the
library does not raise on production-shape inputs.

## Main Ideas

* **Discrete-subgoal coverage, not continuous coverage.** The Ma2024 paper validates only the
  `(1/K) * sum_k 1{hit}` form against human ratings; weighted or fractional variants were not
  reported with comparable reliability and should not be substituted.
* **Tie-break on `precondition_or_effect`.** When the error-classifier judge produces an ambiguous
  or garbage response, the parser returns `PRECONDITION_OR_EFFECT` rather than discarding the step.
  This concentrates noise into a single label so the distribution shape stays interpretable.
* **Cache before judge.** Every progress and error judgment goes through the SHA-256 disk cache
  first. The cache key includes the prompt payload so prompt-template changes invalidate stale
  entries automatically.
* **Judge is injectable.** Tests pass mock callables; live runs construct the CLI-backed callable
  via `make_judge_call`. Either `judge` or `cost_tracker` must be provided to every public function
  — there is no implicit default.
* **No cross-task imports.** `model_call.py` is a verbatim copy of t0012's, not an import. This
  keeps t0022 self-contained per ARF rules, at the cost of one duplicated module.

## Summary

`abc_harness_metrics` is the t0022 deliverable that turns the ABC harness from a single-number
correctness benchmark into a trajectory-quality benchmark. Two metrics — Ma2024 discrete-subgoal
progress rate and Li2024 6+1 error taxonomy — are exposed via a single high-level
`score_trajectory(trajectory, environment) -> TrajectoryScore` entry point, with judge calls
abstracted behind a `Callable[[str], str]` so the library is unit-testable offline.

The library is the input to t0023's confirmatory ABC re-run, where condition C trajectories
(hierarchical planning + decision counter) are expected to show both higher progress rate and a
qualitatively different error distribution than condition A (single step). The validation pass
shipped with this task replays the 91 t0012 phase-2 smoke trajectories through the same code path to
confirm the metrics do not collapse to degenerate values on production-shape inputs.

Known limitation: the FrontierScience-Olympiad subgoal JSON is generated from the gold answers'
SUBTASK lines, which means subgoal quality is bounded by the dataset's annotation depth. The
SWE-bench Verified Lite subgoal JSON uses a simple file-path heuristic on the gold patch and may
miss task-specific milestones; both files are designed to be regenerated by their `build_*.py`
script if a future task improves the subgoal definitions.
