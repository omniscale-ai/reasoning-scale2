"""Unit tests for error_taxonomy.classify_error and parse_error_label.

Each test mocks the judge to return a specific raw response and checks that
the parser recovers the right label (or falls back to the tie-break label
on ambiguity).
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.error_taxonomy import (
    classify_error,
    parse_error_label,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    ErrorTaxonomyLabel,
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


def _step(*, turn: int = 0) -> TrajectoryStep:
    return TrajectoryStep(
        turn_index=turn,
        granularity="atomic",
        thought="t",
        action="a",
        observation="o",
        confidence=None,
    )


def _judge(*, response: str) -> Callable[[str], str]:
    def call(_prompt: str) -> str:
        return response

    return call


@pytest.mark.parametrize(
    "label",
    [
        ErrorTaxonomyLabel.HALLUCINATION,
        ErrorTaxonomyLabel.AFFORDANCE,
        ErrorTaxonomyLabel.MISSING_STEP,
        ErrorTaxonomyLabel.EXTRA_STEP,
        ErrorTaxonomyLabel.WRONG_ORDER,
        ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT,
        ErrorTaxonomyLabel.OK,
    ],
)
def test_each_label_is_producible(label: ErrorTaxonomyLabel) -> None:
    """For every one of the seven labels, a hand-crafted response yields it."""
    judge = _judge(response=label.value)
    out = classify_error(
        trajectory_step=_step(),
        environment_state={},
        judge=judge,
        environment_id="e-test",
    )
    assert out == label


def test_parse_error_label_strips_whitespace_and_lowercases() -> None:
    assert parse_error_label(response="  Hallucination  \n") == ErrorTaxonomyLabel.HALLUCINATION
    assert parse_error_label(response="OK") == ErrorTaxonomyLabel.OK


def test_parse_error_label_substring_match() -> None:
    """A response with extra prose but exactly one label substring resolves."""
    raw = "After consideration, the label is: missing_step."
    assert parse_error_label(response=raw) == ErrorTaxonomyLabel.MISSING_STEP


def test_parse_error_label_ambiguous_falls_back_to_precondition() -> None:
    """A response containing two label substrings falls back to the tie-break."""
    raw = "I cannot decide between hallucination and affordance"
    assert parse_error_label(response=raw) == ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT


def test_parse_error_label_garbage_falls_back_to_precondition() -> None:
    raw = "absolutely incoherent response with no recognized label"
    assert parse_error_label(response=raw) == ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT


def test_classify_error_raises_without_judge_or_tracker() -> None:
    with pytest.raises(ValueError, match="judge callable or a cost_tracker"):
        classify_error(trajectory_step=_step(), environment_state={})
