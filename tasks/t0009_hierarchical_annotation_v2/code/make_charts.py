"""Generate the two required charts for results/images/.

Chart 1: per-benchmark v1 vs v2 judge accept rate (bar chart).
Chart 2: per-row total atomics distribution by benchmark (boxplot).
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from tasks.t0009_hierarchical_annotation_v2.code.paths import (
    TASK_ROOT,
    V1_VS_V2_COMPARISON_JSON,
    V2_FINAL_JSONL,
)

IMAGES_DIR: Path = TASK_ROOT / "results" / "images"


def _load_jsonl(*, path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def chart_accept_rate() -> Path:
    payload = json.loads(V1_VS_V2_COMPARISON_JSON.read_text(encoding="utf-8"))
    benches: list[str] = []
    v1_rates: list[float] = []
    v2_rates: list[float] = []
    for entry in payload["per_benchmark"]:
        benches.append(entry["benchmark"])
        v1_rates.append((entry["v1_accept_rate"] or 0.0) * 100)
        v2_rates.append((entry["v2_accept_rate"] or 0.0) * 100)

    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(benches))
    width = 0.35
    ax.bar([i - width / 2 for i in x], v1_rates, width, label="v1 (flat schema)", color="#a0a0a0")
    ax.bar(
        [i + width / 2 for i in x],
        v2_rates,
        width,
        label="v2 (tree schema, full text)",
        color="#2a7fbf",
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(benches, rotation=20, ha="right")
    ax.set_ylabel("Judge accept rate (%)")
    ax.set_title("LLM-as-judge accept rate: v2 (tree schema) vs v1 (flat schema)")
    ax.set_ylim(0, 110)
    ax.legend(loc="lower left")
    for i, (v1, v2) in enumerate(zip(v1_rates, v2_rates, strict=True)):
        ax.annotate(f"{v1:.0f}%", (i - width / 2, v1 + 2), ha="center", fontsize=9, color="#404040")
        ax.annotate(f"{v2:.0f}%", (i + width / 2, v2 + 2), ha="center", fontsize=9, color="#1a4f7a")
    fig.tight_layout()
    out_path = IMAGES_DIR / "v1_vs_v2_accept_rate.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def chart_atomics_distribution() -> Path:
    rows = _load_jsonl(path=V2_FINAL_JSONL)
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
    ax.set_title("v2 atomics-per-row distribution by benchmark")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    out_path = IMAGES_DIR / "v2_atomics_distribution.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate v2 results charts")
    parser.parse_args()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Wrote {chart_accept_rate()}")
    print(f"Wrote {chart_atomics_distribution()}")


if __name__ == "__main__":
    main()
