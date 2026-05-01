"""Shared dataclasses and enums for the abc_harness_metrics library.

These types are the public contract between the three judge-backed scoring
functions (``compute_progress_rate``, ``classify_error``, ``score_trajectory``)
and downstream callers (notably t0023's confirmatory ABC run).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ErrorTaxonomyLabel(StrEnum):
    """Li2024 Embodied Agent Interface error taxonomy.

    The six error labels come from Li et al. 2024 (NeurIPS 2024) appendix A.4.
    The ``OK`` sentinel is added by this project to mark non-error steps so the
    classifier can be applied to every step in a trajectory rather than only
    failing ones.

    Tie-break rule (per t0022 task spec): if the judge returns an ambiguous
    or unparseable label, callers must default to
    :attr:`ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT`.
    """

    HALLUCINATION = "hallucination"
    AFFORDANCE = "affordance"
    MISSING_STEP = "missing_step"
    EXTRA_STEP = "extra_step"
    WRONG_ORDER = "wrong_order"
    PRECONDITION_OR_EFFECT = "precondition_or_effect"
    OK = "ok"


@dataclass(frozen=True, slots=True)
class TrajectoryStep:
    """One step in an agent trajectory using the t0006/t0012 six-field schema."""

    turn_index: int
    granularity: str
    thought: str
    action: str
    observation: str
    confidence: float | None = None


@dataclass(frozen=True, slots=True)
class Trajectory:
    """A complete agent trajectory plus the binary success bit."""

    task_id: str
    steps: tuple[TrajectoryStep, ...]
    task_success: bool
    final_answer: str = ""


@dataclass(frozen=True, slots=True)
class Subgoal:
    """One milestone in an environment's subgoal list."""

    subgoal_id: str
    description: str


@dataclass(frozen=True, slots=True)
class EnvironmentSubgoals:
    """The subgoal definitions for one environment / problem instance."""

    environment_id: str
    subgoals: tuple[Subgoal, ...]


@dataclass(frozen=True, slots=True)
class TrajectoryScore:
    """High-level score record returned by :func:`score_trajectory`."""

    task_success: bool
    progress_rate: float
    step_errors: tuple[ErrorTaxonomyLabel, ...]
    error_distribution: Counter[ErrorTaxonomyLabel] = field(default_factory=Counter)


def _trajectory_step_to_dict(*, step: TrajectoryStep) -> dict[str, Any]:
    """Plain-dict view used by hashing helpers."""
    return {
        "turn_index": step.turn_index,
        "granularity": step.granularity,
        "thought": step.thought,
        "action": step.action,
        "observation": step.observation,
        "confidence": step.confidence,
    }
