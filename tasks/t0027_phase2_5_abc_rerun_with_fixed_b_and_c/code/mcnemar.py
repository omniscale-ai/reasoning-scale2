"""Paired McNemar test (exact binomial for small samples; chi-squared with continuity otherwise).

Forked verbatim from t0026 with no behavioural changes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

_SMALL_SAMPLE_THRESHOLD: int = 25


@dataclass(frozen=True, slots=True)
class McNemarResult:
    statistic: float
    p_value: float
    method: str
    discordant_b: int
    discordant_c: int


def _exact_two_sided_binomial(*, k: int, n: int, p: float = 0.5) -> float:
    if n == 0:
        return 1.0
    probs: list[float] = []
    for i in range(n + 1):
        log_coef = math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
        log_pmf = log_coef + i * math.log(p) + (n - i) * math.log(1.0 - p)
        probs.append(math.exp(log_pmf))
    observed = probs[k]
    pval = sum(prob for prob in probs if prob <= observed + 1e-12)
    if pval > 1.0:
        return 1.0
    if pval < 0.0:
        return 0.0
    return pval


def _chi_squared_p_value(*, statistic: float) -> float:
    if statistic <= 0.0:
        return 1.0
    return math.erfc(math.sqrt(statistic / 2.0))


def mcnemar_paired(*, b: int, c: int) -> McNemarResult:
    assert b >= 0 and c >= 0, "discordant counts must be non-negative"
    n = b + c
    if n == 0:
        return McNemarResult(
            statistic=0.0,
            p_value=1.0,
            method="trivial",
            discordant_b=b,
            discordant_c=c,
        )
    if n < _SMALL_SAMPLE_THRESHOLD:
        k_min = min(b, c)
        pval = _exact_two_sided_binomial(k=k_min, n=n, p=0.5)
        return McNemarResult(
            statistic=float(k_min),
            p_value=pval,
            method="exact_binomial",
            discordant_b=b,
            discordant_c=c,
        )
    statistic = (abs(b - c) - 1.0) ** 2 / (b + c)
    pval = _chi_squared_p_value(statistic=statistic)
    return McNemarResult(
        statistic=statistic,
        p_value=pval,
        method="chi_squared_continuity",
        discordant_b=b,
        discordant_c=c,
    )


def pairwise_mcnemar(
    *,
    success_first: list[bool],
    success_second: list[bool],
) -> dict[str, float | int | str]:
    assert len(success_first) == len(success_second), (
        f"paired arrays must align: {len(success_first)} vs {len(success_second)}"
    )
    discordant_b = sum(1 for x, y in zip(success_first, success_second, strict=True) if x and not y)
    discordant_c = sum(
        1 for x, y in zip(success_first, success_second, strict=True) if (not x) and y
    )
    result = mcnemar_paired(b=discordant_b, c=discordant_c)
    return {
        "discordant_b": discordant_b,
        "discordant_c": discordant_c,
        "statistic": result.statistic,
        "p_value": result.p_value,
        "method": result.method,
    }
