"""Inline 10-equal-width-bin Expected Calibration Error on `final_confidence`.

Forked verbatim from t0026 with no behavioural changes.
"""

from __future__ import annotations

from dataclasses import dataclass

_N_BINS: int = 10


@dataclass(frozen=True, slots=True)
class BinRecord:
    bin_index: int
    lower: float
    upper: float
    n: int
    mean_confidence: float | None
    mean_outcome: float | None
    abs_gap: float | None


@dataclass(frozen=True, slots=True)
class ECEResult:
    ece: float
    bins: list[BinRecord]
    n_total: int


def compute_ece_10bin(
    *,
    confidences: list[float],
    outcomes: list[bool],
) -> ECEResult:
    assert len(confidences) == len(outcomes), (
        f"confidence and outcome lists must align: {len(confidences)} vs {len(outcomes)}"
    )
    n_total = len(confidences)
    bin_width = 1.0 / _N_BINS
    bins: list[BinRecord] = []
    weighted_gap_sum: float = 0.0
    for i in range(_N_BINS):
        lower = i * bin_width
        upper = (i + 1) * bin_width if i + 1 < _N_BINS else 1.0 + 1e-9
        bin_confs: list[float] = []
        bin_outs: list[bool] = []
        for c, o in zip(confidences, outcomes, strict=True):
            if c >= lower and c < upper:
                bin_confs.append(c)
                bin_outs.append(o)
        n_in_bin = len(bin_confs)
        if n_in_bin == 0:
            bins.append(
                BinRecord(
                    bin_index=i,
                    lower=lower,
                    upper=min(upper, 1.0),
                    n=0,
                    mean_confidence=None,
                    mean_outcome=None,
                    abs_gap=None,
                )
            )
            continue
        mean_conf = sum(bin_confs) / n_in_bin
        mean_out = sum(1.0 for o in bin_outs if o) / n_in_bin
        abs_gap = abs(mean_conf - mean_out)
        weighted_gap_sum += (n_in_bin / n_total) * abs_gap
        bins.append(
            BinRecord(
                bin_index=i,
                lower=lower,
                upper=min(upper, 1.0),
                n=n_in_bin,
                mean_confidence=mean_conf,
                mean_outcome=mean_out,
                abs_gap=abs_gap,
            )
        )
    return ECEResult(ece=weighted_gap_sum, bins=bins, n_total=n_total)
