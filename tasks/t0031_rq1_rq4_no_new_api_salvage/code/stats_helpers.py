"""Closed-form stats helpers (Wilson CI, exact-binomial p-values, McNemar power).

No scipy/statsmodels — only stdlib + math.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# z-score for a 95% two-sided normal interval (Wilson uses this).
Z_95: float = 1.959963984540054


@dataclass(frozen=True, slots=True)
class WilsonCI:
    point: float
    lower: float
    upper: float
    n: int
    successes: int


def wilson_ci(*, successes: int, n: int, z: float = Z_95) -> WilsonCI | None:
    """Closed-form Wilson 95% interval. Returns None when n == 0."""

    if n <= 0:
        return None
    p_hat = successes / n
    denom = 1.0 + (z * z) / n
    centre = (p_hat + (z * z) / (2.0 * n)) / denom
    half_width = (z * math.sqrt((p_hat * (1.0 - p_hat) / n) + (z * z) / (4.0 * n * n))) / denom
    lower = max(0.0, centre - half_width)
    upper = min(1.0, centre + half_width)
    return WilsonCI(
        point=p_hat,
        lower=lower,
        upper=upper,
        n=n,
        successes=successes,
    )


def binom_pmf(*, k: int, n: int, p: float) -> float:
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * (p**k) * ((1.0 - p) ** (n - k))


def binom_cdf(*, k: int, n: int, p: float) -> float:
    """P(X <= k) for X ~ Binomial(n, p)."""

    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return sum(binom_pmf(k=i, n=n, p=p) for i in range(k + 1))


def binom_sf(*, k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p) (one-sided right tail)."""

    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return sum(binom_pmf(k=i, n=n, p=p) for i in range(k, n + 1))


def binom_two_sided_p(*, k: int, n: int, p: float = 0.5) -> float:
    """Two-sided exact-binomial p-value. Used for McNemar exact test."""

    if n == 0:
        return 1.0
    p0 = binom_pmf(k=k, n=n, p=p)
    total = 0.0
    for i in range(n + 1):
        if binom_pmf(k=i, n=n, p=p) <= p0 + 1e-12:
            total += binom_pmf(k=i, n=n, p=p)
    return min(1.0, total)


def mcnemar_one_sided_critical_k(*, n_disc: int, alpha: float = 0.05) -> int | None:
    """Smallest k such that P(Binomial(n_disc, 0.5) >= k) <= alpha.

    Returns None if no such k exists (always rejecting impossible at this n).
    """

    if n_disc <= 0:
        return None
    for k in range(n_disc + 1):
        if binom_sf(k=k, n=n_disc, p=0.5) <= alpha:
            return k
    return None


def mcnemar_power_one_sided(
    *,
    n_disc: int,
    p1_b_wins: float,
    alpha: float = 0.05,
) -> float:
    """Power of one-sided McNemar exact-binomial test (alternative B > A).

    Under H1, the count of B-wins among discordant pairs is Binomial(n_disc, p1_b_wins).
    Power = P(reject H0 | H1) = P(Binomial(n_disc, p1_b_wins) >= critical_k).
    """

    if n_disc <= 0:
        return 0.0
    critical_k = mcnemar_one_sided_critical_k(n_disc=n_disc, alpha=alpha)
    if critical_k is None:
        return 0.0
    return binom_sf(k=critical_k, n=n_disc, p=p1_b_wins)


def smallest_n_disc_for_power(
    *,
    p1_b_wins: float,
    target_power: float = 0.80,
    alpha: float = 0.05,
    n_max: int = 200,
) -> int | None:
    """Smallest discordant N at which one-sided McNemar power >= target_power."""

    for n_disc in range(1, n_max + 1):
        power = mcnemar_power_one_sided(n_disc=n_disc, p1_b_wins=p1_b_wins, alpha=alpha)
        if power >= target_power:
            return n_disc
    return None


def best_case_p_value_one_sided(*, n_disc: int) -> float:
    """The smallest p-value achievable when ALL n_disc discordant outcomes go to B (one-sided)."""

    if n_disc <= 0:
        return 1.0
    return binom_sf(k=n_disc, n=n_disc, p=0.5)
