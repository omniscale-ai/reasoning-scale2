"""Statistical helpers for t0019.

Adapted (copy + extension) from `tasks/t0014_v2_annotator_sonnet_rerun/code/compute_stats.py`.
Adds an `accept_rate_stderr_half_width` helper and a Cohen's kappa implementation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WilsonCi:
    lower: float | None
    upper: float | None


@dataclass(frozen=True, slots=True)
class CellSummary:
    judged: int
    acceptable: int
    accept_rate: float | None
    ci_lower: float | None
    ci_upper: float | None
    half_width: float | None


@dataclass(frozen=True, slots=True)
class DeltaSummary:
    a_judged: int
    a_acceptable: int
    a_accept_rate: float | None
    a_ci_lower: float | None
    a_ci_upper: float | None
    b_judged: int
    b_acceptable: int
    b_accept_rate: float | None
    b_ci_lower: float | None
    b_ci_upper: float | None
    delta: float | None


def wilson_ci(*, k: int, n: int, z: float = 1.96) -> WilsonCi:
    """Wilson 95% CI for a binomial proportion."""
    if n <= 0:
        return WilsonCi(lower=None, upper=None)
    phat = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (phat + z2 / (2.0 * n)) / denom
    half = (z * math.sqrt(phat * (1.0 - phat) / n + z2 / (4.0 * n * n))) / denom
    return WilsonCi(lower=center - half, upper=center + half)


def accept_rate_stderr_half_width(*, k: int, n: int) -> float | None:
    ci = wilson_ci(k=k, n=n)
    if ci.lower is None or ci.upper is None:
        return None
    return (ci.upper - ci.lower) / 2.0


def cell_summary(*, k: int, n: int) -> CellSummary:
    rate: float | None = (k / n) if n > 0 else None
    ci = wilson_ci(k=k, n=n)
    half = accept_rate_stderr_half_width(k=k, n=n)
    return CellSummary(
        judged=n,
        acceptable=k,
        accept_rate=rate,
        ci_lower=ci.lower,
        ci_upper=ci.upper,
        half_width=half,
    )


def delta_with_ci(*, a: CellSummary, b: CellSummary) -> DeltaSummary:
    delta: float | None = None
    if a.accept_rate is not None and b.accept_rate is not None:
        delta = a.accept_rate - b.accept_rate
    return DeltaSummary(
        a_judged=a.judged,
        a_acceptable=a.acceptable,
        a_accept_rate=a.accept_rate,
        a_ci_lower=a.ci_lower,
        a_ci_upper=a.ci_upper,
        b_judged=b.judged,
        b_acceptable=b.acceptable,
        b_accept_rate=b.accept_rate,
        b_ci_lower=b.ci_lower,
        b_ci_upper=b.ci_upper,
        delta=delta,
    )


def cohens_kappa(*, a_labels: list[str | None], b_labels: list[str | None]) -> float | None:
    """Cohen's kappa for binary categorical labels.

    Returns None if there are fewer than 2 paired observations or if either rater is constant.
    Pairs where either label is None are dropped.
    """
    if len(a_labels) != len(b_labels):
        raise ValueError("a_labels and b_labels must have the same length")
    pairs: list[tuple[str, str]] = []
    for a_val, b_val in zip(a_labels, b_labels, strict=True):
        if a_val is None or b_val is None:
            continue
        pairs.append((a_val, b_val))
    if len(pairs) < 2:
        return None
    categories = sorted({p[0] for p in pairs} | {p[1] for p in pairs})
    if len(categories) < 2:
        return 1.0  # both raters constant on the same label = perfect agreement
    n = len(pairs)
    observed_agree = sum(1 for a_val, b_val in pairs if a_val == b_val) / n
    a_marginals: dict[str, float] = {c: 0.0 for c in categories}
    b_marginals: dict[str, float] = {c: 0.0 for c in categories}
    for a_val, b_val in pairs:
        a_marginals[a_val] += 1.0 / n
        b_marginals[b_val] += 1.0 / n
    expected_agree = sum(a_marginals[c] * b_marginals[c] for c in categories)
    if expected_agree >= 1.0:
        return 1.0 if observed_agree >= 1.0 else 0.0
    return (observed_agree - expected_agree) / (1.0 - expected_agree)
