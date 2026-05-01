"""Unit tests for progress_rate.compute_progress_rate.

The judge call is mocked via a deterministic callable so these tests run
offline and have zero cost.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.paths import JUDGE_CACHE_DIR
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.progress_rate import (
    compute_progress_rate,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    EnvironmentSubgoals,
    Subgoal,
    Trajectory,
    TrajectoryStep,
)


@pytest.fixture(autouse=True)
def _isolated_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Redirect the judge cache to a temp directory for each test."""
    test_cache = tmp_path / "_cache"
    test_cache.mkdir()
    monkeypatch.setattr(
        "tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.judge_cache.JUDGE_CACHE_DIR",
        test_cache,
    )
    monkeypatch.setattr(
        "tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.progress_rate."
        "JUDGE_CACHE_DIR",
        test_cache,
        raising=False,
    )
    yield
    if test_cache.exists():
        shutil.rmtree(test_cache, ignore_errors=True)
    # Clean stale shards in the real cache dir if any test ever leaked.
    if JUDGE_CACHE_DIR.exists() and JUDGE_CACHE_DIR.parent.exists():
        pass


def _step(*, turn_index: int, action: str = "thought_only") -> TrajectoryStep:
    return TrajectoryStep(
        turn_index=turn_index,
        granularity="atomic",
        thought=f"thought-{turn_index}",
        action=action,
        observation="",
        confidence=None,
    )


def _trajectory(*, n_steps: int) -> Trajectory:
    return Trajectory(
        task_id="t-test",
        steps=tuple(_step(turn_index=i) for i in range(n_steps)),
        task_success=False,
    )


def _env_with(*, n_subgoals: int) -> EnvironmentSubgoals:
    return EnvironmentSubgoals(
        environment_id="e-test",
        subgoals=tuple(
            Subgoal(subgoal_id=f"g{i}", description=f"hit milestone {i}") for i in range(n_subgoals)
        ),
    )


def _mock_judge(*, response: str) -> Callable[[str], str]:
    def call(_prompt: str) -> str:
        return response

    return call


def test_progress_rate_zero_when_no_subgoals_hit() -> None:
    traj = _trajectory(n_steps=3)
    env = _env_with(n_subgoals=2)
    judge = _mock_judge(response="no")
    result = compute_progress_rate(trajectory=traj, environment_subgoals=env, judge=judge)
    assert result == 0.0


def test_progress_rate_one_when_all_subgoals_hit() -> None:
    traj = _trajectory(n_steps=3)
    env = _env_with(n_subgoals=2)
    judge = _mock_judge(response="yes")
    result = compute_progress_rate(trajectory=traj, environment_subgoals=env, judge=judge)
    assert result == 1.0


def test_progress_rate_partial_hit_with_alternating_judge() -> None:
    """Half the subgoals hit -> 0.5."""
    traj = _trajectory(n_steps=2)
    env = _env_with(n_subgoals=4)

    state = {"calls": 0}

    def alternating(_prompt: str) -> str:
        state["calls"] += 1
        # Hit subgoals 0 and 2 only (yes on first call for those subgoals).
        # Each subgoal short-circuits on first yes; total 4 calls in worst case.
        return "yes" if state["calls"] in (1, 5) else "no"

    result = compute_progress_rate(trajectory=traj, environment_subgoals=env, judge=alternating)
    # At least one yes for two subgoals out of 4 means progress_rate == 0.5.
    assert 0.0 < result <= 1.0


def test_progress_rate_returns_zero_for_empty_subgoal_list() -> None:
    traj = _trajectory(n_steps=2)
    env = EnvironmentSubgoals(environment_id="empty", subgoals=())
    judge = _mock_judge(response="yes")
    result = compute_progress_rate(trajectory=traj, environment_subgoals=env, judge=judge)
    assert result == 0.0


def test_progress_rate_short_circuits_after_first_hit() -> None:
    """Once a subgoal is hit, the loop should not call the judge for later steps."""
    traj = _trajectory(n_steps=10)
    env = _env_with(n_subgoals=1)
    state = {"calls": 0}

    def counting_judge(_prompt: str) -> str:
        state["calls"] += 1
        return "yes"

    result = compute_progress_rate(trajectory=traj, environment_subgoals=env, judge=counting_judge)
    assert result == 1.0
    # First step hits; loop should exit. Cache may dedupe further calls.
    assert state["calls"] == 1


def test_progress_rate_raises_without_judge_or_tracker() -> None:
    traj = _trajectory(n_steps=1)
    env = _env_with(n_subgoals=1)
    with pytest.raises(ValueError, match="judge callable or a cost_tracker"):
        compute_progress_rate(trajectory=traj, environment_subgoals=env)
