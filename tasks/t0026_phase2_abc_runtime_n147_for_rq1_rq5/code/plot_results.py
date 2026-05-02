"""Generate result charts for t0026 phase-2 A/B/C runtime sweep."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

_TASK_ROOT: Final[Path] = Path(__file__).resolve().parents[1]
_METRICS_PATH: Final[Path] = _TASK_ROOT / "results" / "metrics.json"
_CALIBRATION_PATH: Final[Path] = _TASK_ROOT / "data" / "calibration.json"
_MCNEMAR_PATH: Final[Path] = _TASK_ROOT / "data" / "mcnemar_results.json"
_IMAGES_DIR: Final[Path] = _TASK_ROOT / "results" / "images"


def _load_json(*, path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _plot_success_rates_by_subset(*, metrics: dict[str, Any]) -> Path:
    subsets = ["swebench", "taubench", "frontsci"]
    variants = ["a", "b", "c"]
    labels = {
        "a": "A scope-aware ReAct",
        "b": "B Plan-and-Solve v2",
        "c": "C mismatched-adversarial",
    }
    data: dict[str, list[float]] = {
        v: [float(metrics[f"success_rate_{v}_{s}"]) * 100.0 for s in subsets] for v in variants
    }
    fig, ax = plt.subplots(figsize=(8.0, 4.5))
    bar_width = 0.27
    x_positions = list(range(len(subsets)))
    for offset_idx, variant in enumerate(variants):
        offsets = [pos + (offset_idx - 1) * bar_width for pos in x_positions]
        ax.bar(offsets, data[variant], width=bar_width, label=labels[variant])
    ax.set_xticks(x_positions)
    ax.set_xticklabels(["SWE-bench Verified", "Tau-bench", "FrontierScience"])
    ax.set_ylabel("success rate (%)")
    ax.set_title("Phase-2 A/B/C success rate by benchmark subset (paired N=130)")
    ax.legend(loc="upper left", frameon=False)
    ax.set_ylim(0.0, max(35.0, max(max(d) for d in data.values()) * 1.2))
    fig.tight_layout()
    out = _IMAGES_DIR / "success_rate_by_subset.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def _plot_overall_success(*, metrics: dict[str, Any]) -> Path:
    variants = ["a", "b", "c"]
    labels = {
        "a": "A scope-aware ReAct",
        "b": "B Plan-and-Solve v2",
        "c": "C mismatched-adversarial",
    }
    rates = [float(metrics[f"success_rate_{v}"]) * 100.0 for v in variants]
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    bars = ax.bar(
        [labels[v] for v in variants],
        rates,
        color=["#3a7bd5", "#d97706", "#b45309"],
    )
    ax.set_ylabel("overall success rate (%)")
    ax.set_title("Phase-2 A/B/C overall success rate")
    for bar, rate in zip(bars, rates, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            rate + 0.4,
            f"{rate:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    ax.set_ylim(0.0, max(rates) * 1.4 + 1.0)
    fig.tight_layout()
    out = _IMAGES_DIR / "success_rate_overall.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def _plot_calibration(*, calibration: dict[str, Any]) -> Path:
    bins = calibration["bins"]
    centers: list[float] = []
    confs: list[float] = []
    outcomes: list[float] = []
    weights: list[int] = []
    for b in bins:
        if b.get("n", 0) == 0 or b.get("mean_confidence") is None:
            continue
        centers.append((b["lower"] + b["upper"]) / 2.0)
        confs.append(float(b["mean_confidence"]))
        outcomes.append(float(b["mean_outcome"]))
        weights.append(int(b["n"]))
    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    ax.plot([0.0, 1.0], [0.0, 1.0], linestyle="--", color="#888", label="perfect calibration")
    sizes = [max(40.0, w * 30.0) for w in weights]
    ax.scatter(confs, outcomes, s=sizes, color="#d97706", alpha=0.85, label="bin (size = n)")
    for x, y, w in zip(confs, outcomes, weights, strict=True):
        ax.annotate(f"n={w}", xy=(x, y), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("verbalized confidence (bin mean)")
    ax.set_ylabel("empirical success rate (bin mean)")
    ax.set_title(
        f"Variant B final_confidence calibration (ECE = {calibration['ece']:.2f}, n = "
        f"{calibration['n_total']})"
    )
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    out = _IMAGES_DIR / "calibration_reliability.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def _plot_mcnemar(*, mcnemar: dict[str, Any]) -> Path:
    pairs = [("a_vs_b", "A vs B"), ("b_vs_c", "B vs C")]
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.0))
    for ax, (key, label) in zip(axes, pairs, strict=True):
        d = mcnemar[key]
        a_only = int(d["discordant_b"])
        b_only = int(d["discordant_c"])
        ax.bar(
            ["1st-only correct", "2nd-only correct"],
            [a_only, b_only],
            color=["#3a7bd5", "#b45309"],
        )
        for i, val in enumerate([a_only, b_only]):
            ax.text(i, val + 0.2, str(val), ha="center", va="bottom", fontsize=11)
        ax.set_title(f"McNemar {label}\np = {d['p_value']:.3f}")
        ax.set_ylabel("discordant pairs")
        ax.set_ylim(0, max(a_only, b_only) * 1.4 + 1.0)
    fig.suptitle("Paired McNemar discordant counts (N=130 paired)")
    fig.tight_layout()
    out = _IMAGES_DIR / "mcnemar_discordants.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def main() -> None:
    _IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    metrics = _load_json(path=_METRICS_PATH)
    calibration = _load_json(path=_CALIBRATION_PATH)
    mcnemar = _load_json(path=_MCNEMAR_PATH)
    out_paths = [
        _plot_success_rates_by_subset(metrics=metrics),
        _plot_overall_success(metrics=metrics),
        _plot_calibration(calibration=calibration),
        _plot_mcnemar(mcnemar=mcnemar),
    ]
    for p in out_paths:
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
