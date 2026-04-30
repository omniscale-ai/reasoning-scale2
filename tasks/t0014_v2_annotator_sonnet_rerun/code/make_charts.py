"""Generate the three required charts for results/images/ (t0014).

Chart 1: per-benchmark accept rate, three bars: v1-sonnet, v2-haiku, v2-sonnet.
Chart 2: aggregate decomposition: schema-only, model-only, and headline deltas.
Chart 3: per-row total atomics distribution by benchmark (v2-sonnet).
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from tasks.t0014_v2_annotator_sonnet_rerun.code.paths import (  # noqa: E402
    RESULTS_IMAGES_DIR,
    THREE_WAY_COMPARISON_JSON,
    V2_SONNET_FINAL_JSONL,
)


def _load_jsonl(*, path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def chart_three_way_accept_rate() -> Path:
    payload = json.loads(THREE_WAY_COMPARISON_JSON.read_text(encoding="utf-8"))
    benches: list[str] = []
    v1_rates: list[float] = []
    haiku_rates: list[float] = []
    sonnet_rates: list[float] = []
    for entry in payload["per_benchmark"]:
        benches.append(entry["benchmark"])
        v1_rates.append((entry["schema_only"]["b_accept_rate"] or 0.0) * 100)
        haiku_rates.append((entry["model_only"]["b_accept_rate"] or 0.0) * 100)
        sonnet_rates.append((entry["schema_only"]["a_accept_rate"] or 0.0) * 100)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    x = range(len(benches))
    width = 0.27
    ax.bar(
        [i - width for i in x],
        v1_rates,
        width,
        label="v1-sonnet (flat schema)",
        color="#a0a0a0",
    )
    ax.bar(
        list(x),
        haiku_rates,
        width,
        label="v2-haiku (tree schema)",
        color="#2a7fbf",
    )
    ax.bar(
        [i + width for i in x],
        sonnet_rates,
        width,
        label="v2-sonnet (tree schema)",
        color="#2aa84a",
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(benches, rotation=20, ha="right")
    ax.set_ylabel("Judge accept rate (%)")
    ax.set_title("LLM-as-judge accept rate by benchmark: v1-sonnet vs v2-haiku vs v2-sonnet")
    ax.set_ylim(0, 115)
    ax.legend(loc="lower left")
    for i, (v1, h, s) in enumerate(zip(v1_rates, haiku_rates, sonnet_rates, strict=True)):
        ax.annotate(f"{v1:.0f}%", (i - width, v1 + 2), ha="center", fontsize=8, color="#404040")
        ax.annotate(f"{h:.0f}%", (i, h + 2), ha="center", fontsize=8, color="#1a4f7a")
        ax.annotate(f"{s:.0f}%", (i + width, s + 2), ha="center", fontsize=8, color="#185c2a")
    fig.tight_layout()
    out_path = RESULTS_IMAGES_DIR / "three_way_accept_rate.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_aggregate_decomposition() -> Path:
    payload = json.loads(THREE_WAY_COMPARISON_JSON.read_text(encoding="utf-8"))
    agg = payload["aggregate"]
    labels = [
        "Schema-only\n(v2-sonnet vs v1-sonnet)",
        "Model-only\n(v2-sonnet vs v2-haiku)",
        "Headline\n(v2-haiku vs v1-sonnet)",
    ]
    deltas = [
        (agg["schema_only"]["delta"] or 0.0) * 100,
        (agg["model_only"]["delta"] or 0.0) * 100,
        (agg["headline"]["delta"] or 0.0) * 100,
    ]
    colors = ["#2a7fbf", "#2aa84a", "#a0a0a0"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, deltas, color=colors)
    ax.axhline(y=0, color="black", linewidth=0.6)
    ax.set_ylabel("Aggregate accept-rate delta (pp)")
    ax.set_title("Aggregate decomposition of t0009 +58 pp gain")
    for bar, d in zip(bars, deltas, strict=True):
        ax.annotate(
            f"{d:+.0f} pp",
            (bar.get_x() + bar.get_width() / 2, d + (1 if d >= 0 else -3)),
            ha="center",
            fontsize=10,
            color="#202020",
        )
    fig.tight_layout()
    out_path = RESULTS_IMAGES_DIR / "aggregate_decomposition.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_atomics_distribution() -> Path:
    rows = _load_jsonl(path=V2_SONNET_FINAL_JSONL)
    counts: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        hierarchy = row.get("hierarchy") or {}
        n = len(hierarchy.get("global_atomics") or [])
        for sub in hierarchy.get("subtasks") or []:
            n += len(sub.get("atomics") or [])
        counts[row.get("benchmark", "")].append(n)

    benches = sorted(counts.keys())
    data = [counts[b] for b in benches]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.boxplot(data, tick_labels=benches, showmeans=True)
    ax.set_ylabel("Total atomics per row (subtask + global_atomics)")
    ax.set_title("v2-sonnet atomics-per-row distribution by benchmark")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    out_path = RESULTS_IMAGES_DIR / "v2_sonnet_atomics_distribution.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate v2-sonnet results charts")
    parser.parse_args()
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Wrote {chart_three_way_accept_rate()}")
    print(f"Wrote {chart_aggregate_decomposition()}")
    print(f"Wrote {chart_atomics_distribution()}")


if __name__ == "__main__":
    main()
