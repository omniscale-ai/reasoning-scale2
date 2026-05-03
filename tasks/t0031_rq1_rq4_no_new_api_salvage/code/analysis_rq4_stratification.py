"""Analysis 1: per-subset stratification of arm_a × arm_b 2x2 contingency."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0031_rq1_rq4_no_new_api_salvage.code.constants import SUBSET_ORDER
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.load_paired_outputs import load_paired_frame
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.paths import (
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    RQ4_HEATMAP_PNG,
    RQ4_JSON,
)
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.stats_helpers import (
    binom_two_sided_p,
    wilson_ci,
)


@dataclass(frozen=True, slots=True)
class CIResult:
    point: float | None
    lower: float | None
    upper: float | None
    n: int
    successes: int


@dataclass(frozen=True, slots=True)
class StratumResult:
    label: str
    n: int
    both_pass: int
    a_only: int
    b_only: int
    both_fail: int
    arm_a_pass_ci: CIResult
    arm_b_pass_ci: CIResult
    discordant_n: int
    mcnemar_p_two_sided: float | None
    note: str


def _to_ci_result(*, successes: int, n: int) -> CIResult:
    if n < 5:
        return CIResult(point=None, lower=None, upper=None, n=n, successes=successes)
    ci = wilson_ci(successes=successes, n=n)
    if ci is None:
        return CIResult(point=None, lower=None, upper=None, n=n, successes=successes)
    return CIResult(point=ci.point, lower=ci.lower, upper=ci.upper, n=n, successes=successes)


def _compute_stratum(*, label: str, df: pd.DataFrame) -> StratumResult:
    n = len(df)
    a = df["arm_a_judge_success"].astype(bool)
    b = df["arm_b_judge_success"].astype(bool)
    both_pass = int((a & b).sum())
    a_only = int((a & (~b)).sum())
    b_only = int(((~a) & b).sum())
    both_fail = int(((~a) & (~b)).sum())
    arm_a_pass_n = int(a.sum())
    arm_b_pass_n = int(b.sum())
    discordant_n = a_only + b_only
    mcnemar_p: float | None = (
        binom_two_sided_p(k=b_only, n=discordant_n, p=0.5) if discordant_n >= 1 else None
    )
    note_parts: list[str] = []
    if n < 5:
        note_parts.append("N<5: no usable CI")
    if discordant_n < 1:
        note_parts.append("no discordant pairs: McNemar p undefined")
    return StratumResult(
        label=label,
        n=n,
        both_pass=both_pass,
        a_only=a_only,
        b_only=b_only,
        both_fail=both_fail,
        arm_a_pass_ci=_to_ci_result(successes=arm_a_pass_n, n=n),
        arm_b_pass_ci=_to_ci_result(successes=arm_b_pass_n, n=n),
        discordant_n=discordant_n,
        mcnemar_p_two_sided=mcnemar_p,
        note="; ".join(note_parts),
    )


def _draw_heatmap(*, strata: list[StratumResult], output_path: str) -> None:
    fig, axes = plt.subplots(1, 4, figsize=(14, 4.0))
    for ax, stratum in zip(axes, strata, strict=True):
        cells = np.array(
            [
                [stratum.both_pass, stratum.a_only],
                [stratum.b_only, stratum.both_fail],
            ],
            dtype=float,
        )
        im = ax.imshow(cells, cmap="Blues", aspect="equal")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["B pass", "B fail"])
        ax.set_yticklabels(["A pass", "A fail"])
        ax.set_xlabel("arm B (scope-aware ReAct)")
        ax.set_ylabel("arm A (Plan-and-Solve)")
        ax.set_title(f"{stratum.label}\nN={stratum.n}, disc={stratum.discordant_n}")
        for (i, j), val in np.ndenumerate(cells):
            ax.text(
                j,
                i,
                f"{int(val)}",
                ha="center",
                va="center",
                fontsize=14,
                color="black" if val < cells.max() * 0.6 else "white",
            )
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle(
        "RQ4 stratification — arm A (Plan-and-Solve baseline) × arm B "
        "(scope-aware ReAct) per benchmark",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    frame = load_paired_frame()
    df = frame.df

    strata: list[StratumResult] = []
    for subset in SUBSET_ORDER:
        sub_df = df[df["subset"] == subset]
        strata.append(_compute_stratum(label=subset, df=sub_df))
    strata.append(_compute_stratum(label="ALL", df=df))

    payload = {
        "spec_version": "1",
        "task_id": "t0031_rq1_rq4_no_new_api_salvage",
        "n_total": frame.n_total,
        "n_per_subset": frame.n_per_subset,
        "discordance_rate_overall": frame.discordance_rate,
        "discordant_b_wins_overall": frame.discordant_b_wins,
        "discordant_a_wins_overall": frame.discordant_a_wins,
        "strata": [
            {
                "label": s.label,
                "n": s.n,
                "cells": {
                    "both_pass": s.both_pass,
                    "a_only": s.a_only,
                    "b_only": s.b_only,
                    "both_fail": s.both_fail,
                },
                "discordant_n": s.discordant_n,
                "mcnemar_p_two_sided": s.mcnemar_p_two_sided,
                "arm_a_pass_ci": asdict(s.arm_a_pass_ci),
                "arm_b_pass_ci": asdict(s.arm_b_pass_ci),
                "note": s.note,
            }
            for s in strata
        ],
    }
    RQ4_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _draw_heatmap(strata=strata, output_path=str(RQ4_HEATMAP_PNG))
    print(f"Wrote {RQ4_JSON}")
    print(f"Wrote {RQ4_HEATMAP_PNG}")
    for s in strata:
        print(
            f"  {s.label}: n={s.n} cells=(BP={s.both_pass}, A={s.a_only}, "
            f"B={s.b_only}, BF={s.both_fail}) disc={s.discordant_n} "
            f"p={s.mcnemar_p_two_sided}"
        )


if __name__ == "__main__":
    main()
