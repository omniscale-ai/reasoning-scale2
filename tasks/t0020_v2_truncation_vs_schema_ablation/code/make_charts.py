"""Render the two charts referenced from the t0020 results writeup.

Outputs:
  results/images/accept_rate_three_way.png
  results/images/decomposition.png
"""

from __future__ import annotations

import json
from typing import Any

import matplotlib.pyplot as plt

from tasks.t0020_v2_truncation_vs_schema_ablation.code.paths import (
    RESULTS_IMAGES_DIR,
    THREE_WAY_COMPARISON_JSON,
)


def _load_comparison() -> dict[str, Any]:
    return json.loads(THREE_WAY_COMPARISON_JSON.read_text(encoding="utf-8"))


def _accept_rate_chart(*, data: dict[str, Any]) -> None:
    aggregate = data["aggregate"]
    conditions = ["v1-flat-truncated", "v2-tree-truncated", "v2-tree-full"]
    rates = [
        aggregate["v1_flat_truncated"]["accept_rate"],
        aggregate["v2_tree_truncated"]["accept_rate"],
        aggregate["v2_tree_full"]["accept_rate"],
    ]
    counts = [
        f"{aggregate['v1_flat_truncated']['acceptable']}/"
        f"{aggregate['v1_flat_truncated']['judged']}",
        f"{aggregate['v2_tree_truncated']['acceptable']}/"
        f"{aggregate['v2_tree_truncated']['judged']}",
        f"{aggregate['v2_tree_full']['acceptable']}/{aggregate['v2_tree_full']['judged']}",
    ]
    schema_lo = aggregate["pure_schema"]["b_ci_low"]
    schema_hi = aggregate["pure_schema"]["b_ci_high"]
    trunc_lo = aggregate["pure_schema"]["a_ci_low"]
    trunc_hi = aggregate["pure_schema"]["a_ci_high"]
    full_lo = aggregate["headline"]["a_ci_low"]
    full_hi = aggregate["headline"]["a_ci_high"]

    err_lower = [
        rates[0] - schema_lo,
        rates[1] - trunc_lo,
        rates[2] - full_lo,
    ]
    err_upper = [
        schema_hi - rates[0],
        trunc_hi - rates[1],
        full_hi - rates[2],
    ]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    colors = ["#bd6f6f", "#6f8fbd", "#4f7c4f"]
    bars = ax.bar(conditions, rates, color=colors, edgecolor="black")
    ax.errorbar(
        x=conditions,
        y=rates,
        yerr=[err_lower, err_upper],
        fmt="none",
        ecolor="black",
        capsize=5,
        linewidth=1.2,
    )
    for bar, count, rate in zip(bars, counts, rates, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            min(rate + 0.04, 1.02),
            f"{rate:.0%}\n({count})",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Accept rate (haiku judge)")
    ax.set_title("Accept rate by condition (matched 20-row pool; v1 has 12 judged)")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    out = RESULTS_IMAGES_DIR / "accept_rate_three_way.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Wrote {out}")


def _decomposition_chart(*, data: dict[str, Any]) -> None:
    aggregate = data["aggregate"]
    deltas = [
        ("Pure-schema\n(v2-trunc - v1-trunc)", aggregate["pure_schema"]),
        ("Pure-text\n(v2-full - v2-trunc)", aggregate["pure_text"]),
        ("Headline\n(v2-full - v1-trunc)", aggregate["headline"]),
    ]
    labels = [name for name, _ in deltas]
    values = [d["delta"] for _, d in deltas]
    err_lo = [d["delta"] - d["delta_ci_low"] for _, d in deltas]
    err_hi = [d["delta_ci_high"] - d["delta"] for _, d in deltas]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    colors = ["#4f7c4f", "#bd6f6f", "#444444"]
    bars = ax.bar(labels, values, color=colors, edgecolor="black")
    ax.errorbar(
        x=labels,
        y=values,
        yerr=[err_lo, err_hi],
        fmt="none",
        ecolor="black",
        capsize=5,
        linewidth=1.2,
    )
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.02 if value >= 0 else value - 0.06,
            f"{value:+.0%}",
            ha="center",
            va="bottom" if value >= 0 else "top",
            fontsize=11,
            fontweight="bold",
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(-0.25, 1.0)
    ax.set_ylabel("Δ accept rate (pp)")
    ax.set_title("Decomposition of v2-full vs v1-truncated gap (Newcombe-Wilson 95% CIs)")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    out = RESULTS_IMAGES_DIR / "decomposition.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> None:
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    data = _load_comparison()
    _accept_rate_chart(data=data)
    _decomposition_chart(data=data)


if __name__ == "__main__":
    main()
