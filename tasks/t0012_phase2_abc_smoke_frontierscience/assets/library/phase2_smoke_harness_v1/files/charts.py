"""Generate the two required charts for the smoke run.

* ``condition_metric_bar.png`` — 3 conditions × 3 metrics with Wilson 95% CI bars on rates.
* ``per_row_success_heatmap.png`` — N rows × 3 conditions, green=correct, red=wrong.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from tasks.t0012_phase2_abc_smoke_frontierscience.code.constants import (
    METRIC_AVG_DECISIONS_PER_TASK,
    METRIC_OVERCONFIDENT_ERROR_RATE,
    METRIC_TASK_SUCCESS_RATE,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.stats import wilson_interval


def render_condition_metric_bar(
    *,
    metrics_by_condition: dict[str, dict[str, float]],
    successes_n_by_condition: dict[str, tuple[int, int]],
    output_path: Path,
) -> None:
    cond_keys = ["A", "B", "C"]
    metric_keys = [
        METRIC_TASK_SUCCESS_RATE,
        METRIC_OVERCONFIDENT_ERROR_RATE,
        METRIC_AVG_DECISIONS_PER_TASK,
    ]
    titles = {
        METRIC_TASK_SUCCESS_RATE: "Task Success Rate (higher is better)",
        METRIC_OVERCONFIDENT_ERROR_RATE: "Overconfident Error Rate (lower is better)",
        METRIC_AVG_DECISIONS_PER_TASK: "Avg Decisions / Task (informational)",
    }
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    colors = ["#2a9d8f", "#e9c46a", "#e76f51"]
    for ax, key in zip(axes, metric_keys, strict=True):
        values = [metrics_by_condition[ck].get(key, 0.0) for ck in cond_keys]
        if key in (METRIC_TASK_SUCCESS_RATE, METRIC_OVERCONFIDENT_ERROR_RATE):
            ci_lower: list[float] = []
            ci_upper: list[float] = []
            for ck in cond_keys:
                successes, n = successes_n_by_condition.get(ck, (0, 0))
                if key == METRIC_TASK_SUCCESS_RATE:
                    interval = wilson_interval(successes=successes, n=n)
                    ci_lower.append(interval.estimate - interval.lower)
                    ci_upper.append(interval.upper - interval.estimate)
                else:
                    # Overconfident-error has its own denominator (rows with confidence). Use
                    # the simple fraction approximation here so the chart is still informative.
                    rate = metrics_by_condition[ck].get(key, 0.0)
                    over_count = int(round(rate * n))
                    interval = wilson_interval(successes=over_count, n=max(n, 1))
                    ci_lower.append(interval.estimate - interval.lower)
                    ci_upper.append(interval.upper - interval.estimate)
            errs = np.array([ci_lower, ci_upper])
        else:
            errs = None
        bars = ax.bar(cond_keys, values, color=colors, yerr=errs, capsize=5, edgecolor="black")
        ax.set_title(titles[key])
        ax.set_xlabel("Condition")
        ax.set_ylabel(key)
        for bar, val in zip(bars, values, strict=True):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{val:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )
        if key in (METRIC_TASK_SUCCESS_RATE, METRIC_OVERCONFIDENT_ERROR_RATE):
            ax.set_ylim(0, max(1.0, max(values) * 1.2))
    fig.suptitle("Phase 2 A/B/C smoke harness on FrontierScience-Olympiad")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def render_per_row_success_heatmap(
    *,
    task_ids: Sequence[str],
    a_correct: Sequence[bool],
    b_correct: Sequence[bool],
    c_correct: Sequence[bool],
    output_path: Path,
) -> None:
    n = len(task_ids)
    if n == 0:
        return
    matrix = np.array(
        [[int(x) for x in a_correct], [int(x) for x in b_correct], [int(x) for x in c_correct]]
    )
    fig, ax = plt.subplots(figsize=(max(8, n * 0.25), 3.5))
    cmap = plt.get_cmap("RdYlGn")
    ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=1)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["A scope-aware", "B scope-unaware", "C scope-mismatched"])
    ax.set_xticks(range(n))
    ax.set_xticklabels([t[-6:] for t in task_ids], rotation=90, fontsize=7)
    ax.set_xlabel("Row (task_id suffix)")
    ax.set_title("Per-row success matrix (green=correct, red=wrong)")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
