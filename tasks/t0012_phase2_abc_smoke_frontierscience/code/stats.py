"""Paired McNemar / sign test and Wilson 95% CI helpers for the smoke run.

No SciPy dependency: McNemar's exact two-tailed p-value is the cumulative-binomial probability of
seeing at least ``min(b, c)`` discordant pairs out of ``b + c`` under H0 of p = 0.5, doubled and
clipped at 1.0. Wilson interval implemented from the standard formula. Confirmatory-N is computed
from the standard sample-size formula for paired binary outcomes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class McNemarResult:
    """Result of one paired McNemar / exact binomial sign test."""

    n_pairs: int
    discordant_pairs: int
    pos_minus_neg: int
    p_value: float
    statistic: float | None  # chi-squared statistic when not using exact path
    method: str


@dataclass(frozen=True, slots=True)
class WilsonInterval:
    """Wilson 95% confidence interval for a proportion."""

    estimate: float
    lower: float
    upper: float


def mcnemar_paired(*, a_correct: list[bool], b_correct: list[bool]) -> McNemarResult:
    """Paired McNemar test on two equal-length boolean sequences.

    For each row, ``a_correct[i]`` and ``b_correct[i]`` indicate whether condition A and condition
    B were correct. Pairs where the verdicts agree (both correct, both wrong) carry no information
    about the difference; the test uses only discordant pairs.

    For ``b + c <= 25`` we use the exact two-tailed binomial test; otherwise we use the
    chi-squared continuity-corrected approximation.
    """
    if len(a_correct) != len(b_correct):
        raise ValueError("a_correct and b_correct must have the same length")
    n_pairs = len(a_correct)
    b_count = 0  # A correct, B wrong
    c_count = 0  # A wrong, B correct
    for ai, bi in zip(a_correct, b_correct, strict=True):
        if ai and not bi:
            b_count += 1
        elif (not ai) and bi:
            c_count += 1
    discordant = b_count + c_count
    pos_minus_neg = b_count - c_count
    if discordant == 0:
        return McNemarResult(
            n_pairs=n_pairs,
            discordant_pairs=0,
            pos_minus_neg=0,
            p_value=1.0,
            statistic=None,
            method="exact_binomial_no_discordant",
        )
    if discordant <= 25:
        smaller = min(b_count, c_count)
        # Exact two-tailed: P(X<=smaller) + P(X>=discordant-smaller) under
        # Binomial(n=discordant, p=0.5).
        prob = 0.0
        for k in range(0, smaller + 1):
            prob += _binomial_pmf(n=discordant, k=k, p=0.5)
        # Symmetric tail.
        if smaller != discordant - smaller:
            for k in range(discordant - smaller, discordant + 1):
                prob += _binomial_pmf(n=discordant, k=k, p=0.5)
        else:
            # Equal split: doubling double-counts the median. Subtract one tail.
            prob = min(prob * 2.0, 1.0)
        p_value = min(prob, 1.0)
        return McNemarResult(
            n_pairs=n_pairs,
            discordant_pairs=discordant,
            pos_minus_neg=pos_minus_neg,
            p_value=p_value,
            statistic=None,
            method="exact_binomial",
        )
    # Chi-squared with continuity correction.
    chi_sq = (abs(b_count - c_count) - 1) ** 2 / (b_count + c_count)
    p_value = _chi_sq_pvalue_df1(chi_sq=chi_sq)
    return McNemarResult(
        n_pairs=n_pairs,
        discordant_pairs=discordant,
        pos_minus_neg=pos_minus_neg,
        p_value=p_value,
        statistic=chi_sq,
        method="chi_sq_continuity_corrected",
    )


def _binomial_pmf(*, n: int, k: int, p: float) -> float:
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * (p**k) * ((1 - p) ** (n - k))


def _chi_sq_pvalue_df1(*, chi_sq: float) -> float:
    """P-value for chi-squared with df=1.

    For df=1, P(X^2 > x) = erfc(sqrt(x/2)).
    """
    if chi_sq <= 0:
        return 1.0
    return math.erfc(math.sqrt(chi_sq / 2.0))


def wilson_interval(*, successes: int, n: int, z: float = 1.959964) -> WilsonInterval:
    """Wilson 95% (z=1.96) confidence interval for a binomial proportion."""
    if n == 0:
        return WilsonInterval(estimate=0.0, lower=0.0, upper=0.0)
    p_hat = successes / n
    denom = 1 + (z * z) / n
    centre = p_hat + (z * z) / (2 * n)
    spread = z * math.sqrt((p_hat * (1 - p_hat) + (z * z) / (4 * n)) / n)
    return WilsonInterval(
        estimate=p_hat,
        lower=max(0.0, (centre - spread) / denom),
        upper=min(1.0, (centre + spread) / denom),
    )


def confirmatory_n_for_paired_difference(
    *,
    discordant_rate_estimate: float,
    target_effect_pp: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> int:
    """Estimate the paired-N needed to detect a target absolute difference at given alpha/power.

    Uses the standard formula for paired binary outcomes:

        n = ((z_alpha/2 + z_beta)^2 * p_disc) / (target_effect^2)

    where ``p_disc`` is the expected fraction of discordant pairs (estimated from the smoke run),
    and ``target_effect`` is the absolute difference in proportions we want to detect (in the
    [0,1] range, e.g. 0.05 for 5pp).

    Returns the rounded-up integer N.
    """
    if target_effect_pp <= 0:
        return -1
    z_alpha = 1.959964  # two-tailed alpha=0.05
    z_beta = 0.84162  # power=0.8
    if discordant_rate_estimate <= 0:
        return -1
    target_effect = target_effect_pp / 100.0
    n_float = ((z_alpha + z_beta) ** 2) * discordant_rate_estimate / (target_effect**2)
    return int(math.ceil(n_float))
