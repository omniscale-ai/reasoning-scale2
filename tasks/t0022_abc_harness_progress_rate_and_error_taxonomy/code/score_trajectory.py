"""High-level entry point composing progress rate and error taxonomy.

The function ``score_trajectory`` is what downstream callers (notably the
t0023 confirmatory ABC run) will invoke per row. It returns a
:class:`TrajectoryScore` dataclass with all four fields specified in the
t0022 task spec: ``task_success``, ``progress_rate``, ``step_errors``,
``error_distribution``.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from typing import Any

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.constants import (
    JUDGE_MODEL_DEFAULT,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.error_taxonomy import (
    classify_error,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.model_call import (
    CostTracker,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.progress_rate import (
    compute_progress_rate,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    EnvironmentSubgoals,
    ErrorTaxonomyLabel,
    Trajectory,
    TrajectoryScore,
)

JudgeCallable = Callable[[str], str]


def score_trajectory(
    *,
    trajectory: Trajectory,
    environment: EnvironmentSubgoals,
    judge_model: str = JUDGE_MODEL_DEFAULT,
    cost_tracker: CostTracker | None = None,
    progress_judge: JudgeCallable | None = None,
    error_judge: JudgeCallable | None = None,
    environment_state: dict[str, Any] | None = None,
) -> TrajectoryScore:
    """Compose progress rate and per-step error classification.

    Either ``cost_tracker`` (for live runs) or both ``progress_judge`` and
    ``error_judge`` (for tests with mock judges) must be supplied. We use
    separate judges for progress and error classification because they have
    different system prompts.

    The returned :class:`TrajectoryScore`:

    * ``task_success`` — copied from ``trajectory.task_success``
    * ``progress_rate`` — output of :func:`compute_progress_rate`
    * ``step_errors`` — tuple of one :class:`ErrorTaxonomyLabel` per step
    * ``error_distribution`` — :class:`collections.Counter` over labels
    """
    state = environment_state if environment_state is not None else {}

    progress_rate = compute_progress_rate(
        trajectory=trajectory,
        environment_subgoals=environment,
        judge_model=judge_model,
        cost_tracker=cost_tracker,
        judge=progress_judge,
    )

    step_errors_list: list[ErrorTaxonomyLabel] = []
    for step in trajectory.steps:
        label = classify_error(
            trajectory_step=step,
            environment_state=state,
            judge_model=judge_model,
            cost_tracker=cost_tracker,
            judge=error_judge,
            environment_id=environment.environment_id,
        )
        step_errors_list.append(label)

    error_distribution: Counter[ErrorTaxonomyLabel] = Counter(step_errors_list)

    return TrajectoryScore(
        task_success=trajectory.task_success,
        progress_rate=progress_rate,
        step_errors=tuple(step_errors_list),
        error_distribution=error_distribution,
    )
