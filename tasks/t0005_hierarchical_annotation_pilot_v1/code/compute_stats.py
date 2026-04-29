"""Step 6: compute summary statistics and emit charts for the results step.

Reads the canonical dataset file and writes:

* `code/_outputs/stats.json` with per-benchmark row counts, completeness, and
  judge accept rates plus the mean `avg_decisions_per_task`.
* `results/images/per_benchmark_completeness.png` — per-benchmark
  hierarchy-completeness bar chart.
* `results/images/atomic_lengths.png` — histogram of atomic action lengths.
"""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

import matplotlib

matplotlib.use("Agg")  # noqa: E402  # must be set before pyplot import

import matplotlib.pyplot as plt  # noqa: E402

from tasks.t0005_hierarchical_annotation_pilot_v1.code.constants import (  # noqa: E402
    ALL_BENCHMARKS,
)
from tasks.t0005_hierarchical_annotation_pilot_v1.code.paths import (  # noqa: E402
    ATOMIC_LENGTHS_CHART_PATH,
    DATASET_FILE_PATH,
    PER_BENCHMARK_CHART_PATH,
    RESULTS_IMAGES_DIR,
    STATS_OUTPUT,
)


def _load_rows() -> list[dict[str, Any]]:
    with DATASET_FILE_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def _compute(*, rows: list[dict[str, Any]]) -> dict[str, Any]:
    bench_counts: Counter[str] = Counter()
    bench_complete: Counter[str] = Counter()
    bench_judged: Counter[str] = Counter()
    bench_accept: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    atomic_lengths: list[int] = []
    subtask_lengths: list[int] = []
    judge_verdicts: list[str | None] = []

    for row in rows:
        bench = row["benchmark"]
        bench_counts[bench] += 1
        if row.get("hierarchy_completeness"):
            bench_complete[bench] += 1
        domain_counts[row.get("domain", "")] += 1
        atomic_lengths.append(len(row["hierarchy"]["atomic"]))
        subtask_lengths.append(len(row["hierarchy"]["subtask"]))
        verdict = row.get("judge_verdict")
        judge_verdicts.append(verdict)
        if verdict is not None:
            bench_judged[bench] += 1
            if verdict == "acceptable":
                bench_accept[bench] += 1

    overall_judged = sum(bench_judged.values())
    overall_accept = sum(bench_accept.values())
    overall_accept_rate = overall_accept / overall_judged if overall_judged > 0 else None

    overall_complete = sum(bench_complete.values())
    overall_complete_rate = (
        overall_complete / sum(bench_counts.values()) if sum(bench_counts.values()) > 0 else None
    )

    return {
        "row_count": len(rows),
        "bench_counts": dict(bench_counts),
        "bench_complete": dict(bench_complete),
        "bench_judged": dict(bench_judged),
        "bench_accept": dict(bench_accept),
        "domain_counts": dict(domain_counts),
        "atomic_lengths": atomic_lengths,
        "subtask_lengths": subtask_lengths,
        "avg_decisions_per_task": (
            sum(atomic_lengths) / len(atomic_lengths) if atomic_lengths else 0.0
        ),
        "overall_complete_rate": overall_complete_rate,
        "judge": {
            "rows_judged": overall_judged,
            "rows_accepted": overall_accept,
            "accept_rate_overall": overall_accept_rate,
            "per_benchmark_accept_rate": {
                name: (bench_accept[name] / bench_judged[name] if bench_judged[name] > 0 else None)
                for name in bench_judged
            },
        },
    }


def _save_completeness_chart(*, stats: dict[str, Any]) -> None:
    benches = list(ALL_BENCHMARKS)
    counts = [stats["bench_counts"].get(b, 0) for b in benches]
    completeness = [
        100.0 * stats["bench_complete"].get(b, 0) / counts[i] if counts[i] > 0 else 0.0
        for i, b in enumerate(benches)
    ]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(benches, completeness, color=["#4c78a8", "#f58518", "#54a24b", "#e45756"])
    ax.set_ylim(0, 110)
    ax.set_ylabel("Hierarchy completeness (%)")
    ax.set_title("Per-benchmark hierarchy completeness (v1 pilot, n=115)")
    for bar, total, pct in zip(bars, counts, completeness, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            min(pct + 2.0, 105.0),
            f"{pct:.1f}%\n(n={total})",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.tick_params(axis="x", labelrotation=20)
    fig.tight_layout()
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PER_BENCHMARK_CHART_PATH, dpi=120)
    plt.close(fig)


def _save_atomic_histogram(*, stats: dict[str, Any]) -> None:
    atomic_lengths: list[int] = stats["atomic_lengths"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if atomic_lengths:
        ax.hist(atomic_lengths, bins=range(0, max(atomic_lengths) + 2), color="#4c78a8")
    ax.set_xlabel("Atomic actions per task")
    ax.set_ylabel("Number of tasks")
    ax.set_title("Distribution of atomic-action counts (v1 pilot)")
    fig.tight_layout()
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(ATOMIC_LENGTHS_CHART_PATH, dpi=120)
    plt.close(fig)


def main() -> None:
    rows = _load_rows()
    stats = _compute(rows=rows)
    STATS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with STATS_OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"Wrote {STATS_OUTPUT}")
    _save_completeness_chart(stats=stats)
    print(f"Wrote {PER_BENCHMARK_CHART_PATH}")
    _save_atomic_histogram(stats=stats)
    print(f"Wrote {ATOMIC_LENGTHS_CHART_PATH}")


if __name__ == "__main__":
    main()
