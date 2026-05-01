"""Unit tests for the judge_cache module."""

from __future__ import annotations

from pathlib import Path

import pytest

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.judge_cache import (
    cache_get,
    cache_put,
    hash_trajectory_step,
    make_cache_key,
)


def test_cache_round_trip(tmp_path: Path) -> None:
    root = tmp_path / "_cache"
    key = make_cache_key(
        environment_id="e1",
        trajectory_hash="h1",
        prompt_key="progress.v1",
        prompt_payload="prompt",
    )
    assert cache_get(key=key, root=root) is None
    cache_put(key=key, value="yes", root=root)
    assert cache_get(key=key, root=root) == "yes"


def test_cache_keys_are_deterministic() -> None:
    a = make_cache_key(
        environment_id="e1", trajectory_hash="h1", prompt_key="p1", prompt_payload="payload"
    )
    b = make_cache_key(
        environment_id="e1", trajectory_hash="h1", prompt_key="p1", prompt_payload="payload"
    )
    assert a == b


def test_cache_keys_differ_on_any_component() -> None:
    base = make_cache_key(
        environment_id="e1", trajectory_hash="h1", prompt_key="p1", prompt_payload="x"
    )
    diff_env = make_cache_key(
        environment_id="e2", trajectory_hash="h1", prompt_key="p1", prompt_payload="x"
    )
    diff_traj = make_cache_key(
        environment_id="e1", trajectory_hash="h2", prompt_key="p1", prompt_payload="x"
    )
    diff_prompt_key = make_cache_key(
        environment_id="e1", trajectory_hash="h1", prompt_key="p2", prompt_payload="x"
    )
    diff_payload = make_cache_key(
        environment_id="e1", trajectory_hash="h1", prompt_key="p1", prompt_payload="y"
    )
    assert len({base, diff_env, diff_traj, diff_prompt_key, diff_payload}) == 5


def test_cache_get_returns_none_on_corrupt_file(tmp_path: Path) -> None:
    root = tmp_path / "_cache"
    key = "ab" + "cd" * 31
    target = root / "ab" / f"{key[2:]}.json"
    target.parent.mkdir(parents=True)
    target.write_text("not json", encoding="utf-8")
    assert cache_get(key=key, root=root) is None


def test_hash_trajectory_step_stable() -> None:
    a = hash_trajectory_step(
        turn_index=1, granularity="atomic", thought="t", action="a", observation="o"
    )
    b = hash_trajectory_step(
        turn_index=1, granularity="atomic", thought="t", action="a", observation="o"
    )
    assert a == b
    different = hash_trajectory_step(
        turn_index=2, granularity="atomic", thought="t", action="a", observation="o"
    )
    assert a != different


def test_make_cache_key_short_key_raises() -> None:
    with pytest.raises(ValueError):
        from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.judge_cache import (
            _shard_path,
        )

        _shard_path(key="ab")
