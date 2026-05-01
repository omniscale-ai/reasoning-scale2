"""Local copy of the t0011 calibration aggregator (Metric 2 ``overconfident_error_rate``).

This module is a self-contained subset of
``tasks/t0011_metric2_calibration_aggregator/code/calibration.py``. It exposes only the pieces the
v2 smoke harness actually uses: :class:`CalibrationRecord` and
:func:`compute_overconfident_error_rate`. The heavier self-consistency / verbalized-label
machinery from t0011 is not needed here because the v2 protocol elicits a single numeric
confidence per row directly (Xiong2024 §3.2).

Importing the t0011 module across task folders would require an extra cross-task dependency that
violates the project's compose-via-libraries principle (only registered libraries may be imported
across tasks). Copying the minimal subset here keeps the v2 task self-contained.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.constants import (
    HIGH_CONFIDENCE_THRESHOLD,
)


@dataclass(frozen=True, slots=True)
class CalibrationRecord:
    """One calibrated prediction consumed by :func:`compute_overconfident_error_rate`.

    ``predicted_confidence`` is the aggregated numeric confidence in ``[0.0, 1.0]``. ``is_correct``
    compares the predicted answer against the gold label externally; this library does not infer
    correctness on its own.
    """

    problem_id: str
    predicted_label: str
    predicted_confidence: float
    is_correct: bool


def compute_overconfident_error_rate(
    *,
    records: Iterable[CalibrationRecord],
    threshold: float = HIGH_CONFIDENCE_THRESHOLD,
) -> float:
    """Return the fraction of ``records`` that are incorrect with high stated confidence.

    A record is "overconfident" if ``not is_correct`` and ``predicted_confidence >= threshold``.
    Returns ``0.0`` for an empty input iterable.
    """
    materialized = list(records)
    if len(materialized) == 0:
        return 0.0
    overconfident = sum(
        1
        for record in materialized
        if (not record.is_correct) and record.predicted_confidence >= threshold
    )
    return overconfident / len(materialized)
