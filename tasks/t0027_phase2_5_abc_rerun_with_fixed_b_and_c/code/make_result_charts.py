"""Generate charts for the t0027 results step.

Charts produced (under tasks/<task_id>/results/images/):

* `success_rate_overall.png` — overall success rate per variant on the 130-paired set
* `success_rate_by_subset.png` — per-subset (swebench, taubench, frontsci) success rate per variant
* `mcnemar_discordant_overall.png` — discordant counts (b_only, c_only) for RQ1 and RQ5 contrasts
* `calibration_reliability.png` — reliability diagram (mean confidence vs mean outcome) per bin
  for variants B and C
* `recovery_path_distribution.png` — clean vs reprompt vs json_fallback vs all_failed counts for B
  and C
* `cost_breakdown.png` — stacked bar: agent vs judge vs smoke cost per variant
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

TASK_ROOT: Path = Path(
    "tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c",
)
DATA_DIR: Path = TASK_ROOT / "data"
RESULTS_DIR: Path = TASK_ROOT / "results"
IMAGES_DIR: Path = RESULTS_DIR / "images"


@dataclass(frozen=True, slots=True)
class _ChartContext:
    mcnemar: dict[str, Any]
    calibration: dict[str, Any]
    metrics: dict[str, Any]
    costs: dict[str, Any]


def _load_context() -> _ChartContext:
    mcnemar: dict[str, Any] = json.loads(
        (DATA_DIR / "mcnemar_results.json").read_text(encoding="utf-8"),
    )
    calibration: dict[str, Any] = json.loads(
        (DATA_DIR / "calibration.json").read_text(encoding="utf-8"),
    )
    metrics: dict[str, Any] = json.loads(
        (RESULTS_DIR / "metrics.json").read_text(encoding="utf-8"),
    )
    costs: dict[str, Any] = json.loads(
        (RESULTS_DIR / "costs.json").read_text(encoding="utf-8"),
    )
    return _ChartContext(
        mcnemar=mcnemar,
        calibration=calibration,
        metrics=metrics,
        costs=costs,
    )


def _success_rate_overall(ctx: _ChartContext) -> None:
    by_variant: dict[str, float] = {
        v["dimensions"]["variant"]: float(v["metrics"]["task_success_rate"])
        for v in ctx.metrics["variants"]
    }
    variants: list[str] = ["a", "b", "c"]
    values: list[float] = [by_variant[v] for v in variants]
    labels: list[str] = [f"{v.upper()}" for v in variants]
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    bars = ax.bar(
        labels,
        values,
        color=["#4c72b0", "#dd8452", "#55a467"],
    )
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            value + 0.001,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    ax.set_ylabel("Success rate (sonnet judge)")
    ax.set_title("Task success rate by variant on the 130-paired set")
    ax.set_ylim(0.0, max(values) * 1.5 + 0.01)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "success_rate_overall.png", dpi=150)
    plt.close(fig)


def _success_rate_by_subset(ctx: _ChartContext) -> None:
    rq1 = ctx.mcnemar["rq1_a_vs_b"]["per_subset"]
    rq5 = ctx.mcnemar["rq5_b_vs_c"]["per_subset"]
    subsets: list[str] = ["swebench", "taubench", "frontsci"]
    rate_a: list[float] = [rq1[s]["success_rate_first"] for s in subsets]
    rate_b: list[float] = [rq5[s]["success_rate_first"] for s in subsets]
    rate_c: list[float] = [rq5[s]["success_rate_second"] for s in subsets]
    x = np.arange(len(subsets), dtype=float)
    width = 0.27
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(x - width, rate_a, width=width, label="A (scope-aware ReAct)", color="#4c72b0")
    ax.bar(x, rate_b, width=width, label="B (plan_and_solve_v3)", color="#dd8452")
    ax.bar(x + width, rate_c, width=width, label="C (mismatch over v3)", color="#55a467")
    ax.set_xticks(x)
    ax.set_xticklabels([s.replace("frontsci", "FrontSci").upper() for s in subsets])
    ax.set_ylabel("Success rate")
    ax.set_title("Per-subset success rate by variant (paired n=130)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "success_rate_by_subset.png", dpi=150)
    plt.close(fig)


def _mcnemar_discordant_overall(ctx: _ChartContext) -> None:
    rq1 = ctx.mcnemar["rq1_a_vs_b"]["overall"]
    rq5 = ctx.mcnemar["rq5_b_vs_c"]["overall"]
    contrasts: list[str] = ["RQ1: A vs B", "RQ5: B vs C"]
    only_first: list[int] = [rq1["discordant_b"], rq5["discordant_b"]]
    only_second: list[int] = [rq1["discordant_c"], rq5["discordant_c"]]
    pvals: list[float] = [rq1["p_value"], rq5["p_value"]]
    x = np.arange(len(contrasts), dtype=float)
    width = 0.4
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.bar(x - width / 2, only_first, width=width, label="Only first wins", color="#4c72b0")
    ax.bar(x + width / 2, only_second, width=width, label="Only second wins", color="#dd8452")
    for i, p in enumerate(pvals):
        ax.text(
            x[i],
            max(only_first[i], only_second[i]) + 0.3,
            f"p={p:.3f}",
            ha="center",
            fontsize=9,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(contrasts)
    ax.set_ylabel("Discordant pair count")
    ax.set_title("McNemar discordant pairs (overall, paired n=130)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "mcnemar_discordant_overall.png", dpi=150)
    plt.close(fig)


def _calibration_reliability(ctx: _ChartContext) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    colors: dict[str, str] = {"b_t0027": "#dd8452", "c_t0027": "#55a467"}
    labels: dict[str, str] = {
        "b_t0027": "B — plan_and_solve_v3",
        "c_t0027": "C — mismatch over v3",
    }
    for variant_key in ("b_t0027", "c_t0027"):
        bins = ctx.calibration["variants"][variant_key]["bins"]
        ece = ctx.calibration["variants"][variant_key]["ece"]
        xs: list[float] = []
        ys: list[float] = []
        ns: list[int] = []
        for b in bins:
            if b["n"] == 0 or b["mean_confidence"] is None or b["mean_outcome"] is None:
                continue
            xs.append(float(b["mean_confidence"]))
            ys.append(float(b["mean_outcome"]))
            ns.append(int(b["n"]))
        sizes: list[float] = [20.0 + 8.0 * n for n in ns]
        ax.scatter(
            xs,
            ys,
            s=sizes,
            color=colors[variant_key],
            alpha=0.7,
            label=f"{labels[variant_key]} (ECE={ece:.3f})",
            edgecolors="black",
            linewidths=0.5,
        )
        ax.plot(xs, ys, color=colors[variant_key], linewidth=1.2, alpha=0.6)
    ax.plot(
        [0, 1], [0, 1], color="gray", linestyle="--", linewidth=1.0, label="Perfect calibration"
    )
    ax.set_xlabel("Mean predicted confidence (per bin)")
    ax.set_ylabel("Empirical success rate (per bin)")
    ax.set_title("Reliability diagram — Xiong2024 10-equal-width-bin ECE")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "calibration_reliability.png", dpi=150)
    plt.close(fig)


def _recovery_path_distribution(ctx: _ChartContext) -> None:
    rec = ctx.mcnemar["recovery_path_distribution"]
    paths: list[str] = ["clean", "reprompt", "json_fallback", "all_failed", "unknown"]
    counts_b: list[int] = [int(rec["b_t0027"].get(p, 0)) for p in paths]
    counts_c: list[int] = [int(rec["c_t0027"].get(p, 0)) for p in paths]
    x = np.arange(len(paths), dtype=float)
    width = 0.4
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(x - width / 2, counts_b, width=width, label="B (plan_and_solve_v3)", color="#dd8452")
    ax.bar(x + width / 2, counts_c, width=width, label="C (mismatch over v3)", color="#55a467")
    ax.set_xticks(x)
    ax.set_xticklabels(paths)
    ax.set_ylabel("Instance count (out of 130)")
    ax.set_title("Plan-parser recovery-path distribution per variant")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "recovery_path_distribution.png", dpi=150)
    plt.close(fig)


def _cost_breakdown(ctx: _ChartContext) -> None:
    bd: dict[str, Any] = ctx.costs["breakdown"]

    def _amount(key: str) -> float:
        entry = bd[key]
        if isinstance(entry, dict):
            return float(entry["cost_usd"])
        return float(entry)

    variants: list[str] = ["B", "C"]
    full = [_amount("variant_b_agent_full"), _amount("variant_c_agent_full")]
    judge = [_amount("variant_b_judge"), _amount("variant_c_judge")]
    smoke = [_amount("variant_b_smoke"), _amount("variant_c_smoke")]
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    x = np.arange(len(variants), dtype=float)
    ax.bar(x, full, label="Agent (full 130)", color="#4c72b0")
    ax.bar(x, judge, bottom=full, label="Sonnet judge", color="#dd8452")
    smoke_bottoms = [a + b for a, b in zip(full, judge, strict=True)]
    ax.bar(x, smoke, bottom=smoke_bottoms, label="Smoke gate", color="#55a467")
    totals = [a + b + c for a, b, c in zip(full, judge, smoke, strict=True)]
    for i, t in enumerate(totals):
        ax.text(
            x[i],
            t + 0.05,
            f"${t:.2f}",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )
    ax.set_xticks(x)
    ax.set_xticklabels(variants)
    ax.set_ylabel("Cost (USD)")
    ax.set_title("Cost breakdown per variant")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "cost_breakdown.png", dpi=150)
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    ctx = _load_context()
    _success_rate_overall(ctx=ctx)
    _success_rate_by_subset(ctx=ctx)
    _mcnemar_discordant_overall(ctx=ctx)
    _calibration_reliability(ctx=ctx)
    _recovery_path_distribution(ctx=ctx)
    _cost_breakdown(ctx=ctx)


if __name__ == "__main__":
    main()
