"""Unit tests for score_trajectory.score_trajectory.

The high-level entry point composes progress rate and error taxonomy. This
test confirms it does not raise on a real-shape t0012 row (loaded from disk)
and returns a well-formed :class:`TrajectoryScore`.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.paths import T0012_PRED_C
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.score_trajectory import (
    score_trajectory,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    EnvironmentSubgoals,
    ErrorTaxonomyLabel,
    Subgoal,
    Trajectory,
    TrajectoryScore,
    TrajectoryStep,
)


@pytest.fixture(autouse=True)
def _isolated_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    test_cache = tmp_path / "_cache"
    test_cache.mkdir()
    monkeypatch.setattr(
        "tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.judge_cache.JUDGE_CACHE_DIR",
        test_cache,
    )


def _row_to_trajectory(*, row: dict[str, object]) -> Trajectory:
    raw_steps = row.get("trajectory")
    assert isinstance(raw_steps, list)
    steps = tuple(
        TrajectoryStep(
            turn_index=int(s.get("turn_index", i)) if isinstance(s, dict) else i,
            granularity=str(s.get("granularity", "atomic")) if isinstance(s, dict) else "atomic",
            thought=str(s.get("thought", "")) if isinstance(s, dict) else "",
            action=str(s.get("action", "thought_only")) if isinstance(s, dict) else "thought_only",
            observation=str(s.get("observation", "")) if isinstance(s, dict) else "",
            confidence=None,
        )
        for i, s in enumerate(raw_steps)
    )
    return Trajectory(
        task_id=str(row.get("task_id", "")),
        steps=steps,
        task_success=bool(row.get("is_correct", False)),
    )


def _yes_judge(_prompt: str) -> str:
    return "yes"


def _ok_judge(_prompt: str) -> str:
    return "ok"


def test_score_trajectory_on_synthetic() -> None:
    traj = Trajectory(
        task_id="t-syn",
        steps=(
            TrajectoryStep(
                turn_index=0,
                granularity="atomic",
                thought="t",
                action="a",
                observation="o",
                confidence=None,
            ),
        ),
        task_success=False,
    )
    env = EnvironmentSubgoals(
        environment_id="e-syn",
        subgoals=(Subgoal(subgoal_id="g1", description="finish the puzzle"),),
    )
    out = score_trajectory(
        trajectory=traj,
        environment=env,
        progress_judge=_yes_judge,
        error_judge=_ok_judge,
    )
    assert isinstance(out, TrajectoryScore)
    assert out.task_success is False
    assert out.progress_rate == 1.0
    assert out.step_errors == (ErrorTaxonomyLabel.OK,)
    assert isinstance(out.error_distribution, Counter)
    assert out.error_distribution[ErrorTaxonomyLabel.OK] == 1


def test_score_trajectory_on_real_t0012_row_does_not_raise() -> None:
    """Sanity check: load a real t0012 prediction row and score it without error."""
    if not T0012_PRED_C.exists():
        pytest.skip(f"t0012 predictions not present at {T0012_PRED_C}")
    with T0012_PRED_C.open(encoding="utf-8") as f:
        row = json.loads(f.readline())
    traj = _row_to_trajectory(row=row)
    if len(traj.steps) == 0:
        pytest.skip("loaded trajectory has zero steps; skipping smoke check")
    env = EnvironmentSubgoals(
        environment_id=traj.task_id,
        subgoals=(
            Subgoal(subgoal_id="g1", description="define the problem clearly"),
            Subgoal(subgoal_id="g2", description="reach a final answer"),
        ),
    )
    out = score_trajectory(
        trajectory=traj,
        environment=env,
        progress_judge=_yes_judge,
        error_judge=_ok_judge,
    )
    assert isinstance(out, TrajectoryScore)
    assert len(out.step_errors) == len(traj.steps)
    # All step labels are valid enum members.
    for label in out.step_errors:
        assert isinstance(label, ErrorTaxonomyLabel)
