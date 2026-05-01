"""Ma2024 AgentBoard subgoal-coverage progress rate.

The discrete-subgoal-coverage form averages 0/1 hit indicators across the
environment's subgoal list:

    progress_rate = (1/K) * sum_{k in subgoals} 1{some step hits subgoal_k}

A subgoal is "hit" iff the judge model returns ``yes`` for at least one step
in the trajectory. The implementation short-circuits as soon as a subgoal
flips to hit, so the worst-case cost is K * len(steps) judge calls and the
best case (every subgoal hit by the first step) is K calls.

References:
    Ma et al. 2024, AgentBoard (NeurIPS 2024 D&B), supplementary §C.2
    progress-rate prompt schema. Pearson rho > 0.95 against humans on the
    1013-environment evaluation in the paper.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.constants import (
    JUDGE_MODEL_DEFAULT,
    MAX_OBSERVATION_CHARS,
    MAX_SUBGOAL_DESC_CHARS,
    MAX_THOUGHT_CHARS,
    PROGRESS_RATE_PROMPT_KEY,
    PROGRESS_RATE_SYSTEM_PROMPT,
    PROGRESS_RATE_USER_TEMPLATE,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.judge_cache import (
    cache_get,
    cache_put,
    hash_trajectory_step,
    make_cache_key,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.model_call import (
    CostTracker,
    make_judge_call,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    EnvironmentSubgoals,
    Subgoal,
    Trajectory,
    TrajectoryStep,
)

# Type alias for a callable matching the (prompt, system_prompt) -> response signature used in
# tests with mock judges. The default callable comes from ``make_judge_call``.
JudgeCallable = Callable[[str], str]


def _truncate(*, text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def _build_progress_prompt(*, subgoal: Subgoal, step: TrajectoryStep) -> str:
    return PROGRESS_RATE_USER_TEMPLATE.format(
        subgoal_description=_truncate(text=subgoal.description, max_chars=MAX_SUBGOAL_DESC_CHARS),
        thought=_truncate(text=step.thought or "", max_chars=MAX_THOUGHT_CHARS),
        action=_truncate(text=step.action or "", max_chars=MAX_THOUGHT_CHARS),
        observation=_truncate(text=step.observation or "", max_chars=MAX_OBSERVATION_CHARS),
    )


def _parse_yes_no(*, response: str) -> bool:
    """Strict yes/no parser: returns True only on a leading 'yes'."""
    cleaned = response.strip().lower()
    return cleaned.startswith("yes")


def _judge_step_hits_subgoal(
    *,
    subgoal: Subgoal,
    step: TrajectoryStep,
    environment_id: str,
    judge: JudgeCallable,
) -> bool:
    """One (subgoal, step) judge call with disk-cache lookup."""
    prompt = _build_progress_prompt(subgoal=subgoal, step=step)
    step_hash = hash_trajectory_step(
        turn_index=step.turn_index,
        granularity=step.granularity,
        thought=step.thought,
        action=step.action,
        observation=step.observation,
    )
    key = make_cache_key(
        environment_id=environment_id,
        trajectory_hash=f"{step_hash}|{subgoal.subgoal_id}",
        prompt_key=PROGRESS_RATE_PROMPT_KEY,
        prompt_payload=prompt,
    )
    cached = cache_get(key=key)
    if cached is not None:
        return _parse_yes_no(response=cached)
    response = judge(prompt)
    cache_put(key=key, value=response)
    return _parse_yes_no(response=response)


def compute_progress_rate(
    *,
    trajectory: Trajectory,
    environment_subgoals: EnvironmentSubgoals,
    judge_model: str = JUDGE_MODEL_DEFAULT,
    cost_tracker: CostTracker | None = None,
    judge: JudgeCallable | None = None,
) -> float:
    """Compute the Ma2024 discrete-subgoal-coverage progress rate.

    Either ``judge`` (a callable) or a non-``None`` ``cost_tracker`` must be
    provided. When ``judge`` is ``None`` we construct one via
    ``make_judge_call`` so live runs against the local Claude CLI work
    out-of-the-box; tests pass a mock callable.

    Returns a float in [0, 1]. Returns 0.0 when the environment has no
    subgoals (this should not happen in practice; subgoal JSONs always
    declare at least one subgoal per instance).
    """
    if len(environment_subgoals.subgoals) == 0:
        return 0.0
    if judge is None:
        if cost_tracker is None:
            raise ValueError(
                "compute_progress_rate requires either a judge callable or a cost_tracker"
            )
        judge = make_judge_call(
            model=judge_model,
            cost_tracker=cost_tracker,
            system_prompt=PROGRESS_RATE_SYSTEM_PROMPT,
            note="progress_rate",
        )
    hits = 0
    for subgoal in environment_subgoals.subgoals:
        for step in trajectory.steps:
            if _judge_step_hits_subgoal(
                subgoal=subgoal,
                step=step,
                environment_id=environment_subgoals.environment_id,
                judge=judge,
            ):
                hits += 1
                break
    return hits / len(environment_subgoals.subgoals)


def _public_signature_marker(*args: Any, **kwargs: Any) -> None:
    """Marker so static analyzers can confirm public symbols.

    The library exports :func:`compute_progress_rate` as the single public
    entry point. This helper is unused at runtime.
    """
    del args, kwargs
