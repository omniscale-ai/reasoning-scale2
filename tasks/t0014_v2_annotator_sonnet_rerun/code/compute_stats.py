"""Compute v2-sonnet statistics and three-way comparison (t0014).

Reads:
- v2-sonnet final dataset asset (this task)
- v2-haiku reference dataset asset (t0009)
- v1 reference dataset asset (t0005)

Computes per-benchmark and aggregate accept-rate deltas in three pairings:
- schema-only: v2-sonnet vs v1-sonnet (annotator held constant on sonnet,
  schema flat -> tree)
- model-only: v2-sonnet vs v2-haiku (schema held constant on tree,
  annotator haiku -> sonnet)
- original headline: v2-haiku vs v1-sonnet (both schema and annotator change;
  reproduces t0009's reported delta)

Each delta is reported with the count, accept-rate, and a Wilson 95% CI on the
v2-sonnet accept rate (the population that varies in this task).

Outputs:
- `code/_outputs/three_way_comparison.json` — structured comparison
- `code/_outputs/three_way_table.md` — markdown table fragment for results_detailed.md
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from tasks.t0014_v2_annotator_sonnet_rerun.code.paths import (
    OUTPUTS_DIR,
    THREE_WAY_COMPARISON_JSON,
    THREE_WAY_TABLE_MD,
    V1_INPUT_PATH,
    V2_HAIKU_INPUT_PATH,
    V2_SONNET_FINAL_JSONL,
)


def _load_jsonl(*, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _benchmark_judge_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "total": 0,
            "judged": 0,
            "acceptable": 0,
            "needs_revision": 0,
        }
    )
    for row in rows:
        bench = row.get("benchmark", "")
        out[bench]["total"] += 1
        verdict = row.get("judge_verdict")
        if verdict == "acceptable":
            out[bench]["acceptable"] += 1
            out[bench]["judged"] += 1
        elif verdict == "needs revision":
            out[bench]["needs_revision"] += 1
            out[bench]["judged"] += 1
    for _bench, b in out.items():
        b["accept_rate"] = (b["acceptable"] / b["judged"]) if b["judged"] > 0 else None
    return dict(out)


def _aggregate_judge_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_judged = 0
    total_acceptable = 0
    total_needs_revision = 0
    for row in rows:
        verdict = row.get("judge_verdict")
        if verdict == "acceptable":
            total_acceptable += 1
            total_judged += 1
        elif verdict == "needs revision":
            total_needs_revision += 1
            total_judged += 1
    rate = (total_acceptable / total_judged) if total_judged > 0 else None
    return {
        "judged": total_judged,
        "acceptable": total_acceptable,
        "needs_revision": total_needs_revision,
        "accept_rate": rate,
    }


def _wilson_ci(*, k: int, n: int, z: float = 1.96) -> tuple[float | None, float | None]:
    """Wilson 95% confidence interval for a binomial proportion.

    Returns (lower, upper) bounds on (k/n). Returns (None, None) if n == 0.
    """
    if n <= 0:
        return None, None
    phat = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (phat + z2 / (2.0 * n)) / denom
    half = (z * math.sqrt(phat * (1.0 - phat) / n + z2 / (4.0 * n * n))) / denom
    return center - half, center + half


def _delta_with_ci(
    *,
    a: dict[str, Any],
    b: dict[str, Any],
) -> dict[str, Any]:
    """Return a dict describing accept-rate delta a - b with Wilson CI on each side."""
    a_rate = a.get("accept_rate")
    b_rate = b.get("accept_rate")
    delta = (a_rate - b_rate) if a_rate is not None and b_rate is not None else None
    a_lo, a_hi = _wilson_ci(k=int(a.get("acceptable", 0)), n=int(a.get("judged", 0)))
    b_lo, b_hi = _wilson_ci(k=int(b.get("acceptable", 0)), n=int(b.get("judged", 0)))
    return {
        "a_judged": int(a.get("judged", 0)),
        "a_acceptable": int(a.get("acceptable", 0)),
        "a_accept_rate": a_rate,
        "a_ci_low": a_lo,
        "a_ci_high": a_hi,
        "b_judged": int(b.get("judged", 0)),
        "b_acceptable": int(b.get("acceptable", 0)),
        "b_accept_rate": b_rate,
        "b_ci_low": b_lo,
        "b_ci_high": b_hi,
        "delta": delta,
    }


def _three_way_per_benchmark(
    *,
    sonnet: dict[str, dict[str, Any]],
    haiku: dict[str, dict[str, Any]],
    v1: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    benches = sorted(set(sonnet) | set(haiku) | set(v1))
    rows: list[dict[str, Any]] = []
    for bench in benches:
        s = sonnet.get(bench, {"judged": 0, "acceptable": 0, "accept_rate": None})
        h = haiku.get(bench, {"judged": 0, "acceptable": 0, "accept_rate": None})
        v = v1.get(bench, {"judged": 0, "acceptable": 0, "accept_rate": None})
        rows.append(
            {
                "benchmark": bench,
                "schema_only": _delta_with_ci(a=s, b=v),
                "model_only": _delta_with_ci(a=s, b=h),
                "headline": _delta_with_ci(a=h, b=v),
            }
        )
    return rows


def _completeness_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "complete": 0})
    for row in rows:
        bench = row.get("benchmark", "")
        out[bench]["total"] += 1
        if row.get("hierarchy_completeness"):
            out[bench]["complete"] += 1
    return dict(out)


def compute() -> dict[str, Any]:
    sonnet_rows = _load_jsonl(path=V2_SONNET_FINAL_JSONL)
    haiku_rows = _load_jsonl(path=V2_HAIKU_INPUT_PATH)
    v1_rows = _load_jsonl(path=V1_INPUT_PATH)

    sonnet_per_bench = _benchmark_judge_summary(sonnet_rows)
    haiku_per_bench = _benchmark_judge_summary(haiku_rows)
    v1_per_bench = _benchmark_judge_summary(v1_rows)

    sonnet_agg = _aggregate_judge_summary(sonnet_rows)
    haiku_agg = _aggregate_judge_summary(haiku_rows)
    v1_agg = _aggregate_judge_summary(v1_rows)

    per_benchmark = _three_way_per_benchmark(
        sonnet=sonnet_per_bench,
        haiku=haiku_per_bench,
        v1=v1_per_bench,
    )

    aggregate = {
        "schema_only": _delta_with_ci(a=sonnet_agg, b=v1_agg),
        "model_only": _delta_with_ci(a=sonnet_agg, b=haiku_agg),
        "headline": _delta_with_ci(a=haiku_agg, b=v1_agg),
    }

    completeness = _completeness_summary(sonnet_rows)
    n_complete_sonnet = sum(b["complete"] for b in completeness.values())

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "v2_sonnet_total_rows": len(sonnet_rows),
        "v2_haiku_total_rows": len(haiku_rows),
        "v1_total_rows": len(v1_rows),
        "v2_sonnet_completeness_per_benchmark": completeness,
        "v2_sonnet_n_complete": n_complete_sonnet,
        "per_benchmark": per_benchmark,
        "aggregate": aggregate,
    }
    THREE_WAY_COMPARISON_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    def _fmt_rate(r: float | None) -> str:
        return f"{r:.0%}" if r is not None else "n/a"

    def _fmt_delta(d: float | None) -> str:
        return f"{d:+.0%}" if d is not None else "n/a"

    table_lines = [
        "| Benchmark | v1-sonnet (flat) | v2-haiku (tree) | v2-sonnet (tree) | "
        "Δ schema-only | Δ model-only | Δ headline |",
        "|-----------|------------------|------------------|------------------|"
        "---------------|--------------|------------|",
    ]
    for entry in per_benchmark:
        s_only = entry["schema_only"]
        m_only = entry["model_only"]
        h = entry["headline"]
        v1_str = (
            f"{_fmt_rate(s_only['b_accept_rate'])} ({s_only['b_acceptable']}/{s_only['b_judged']})"
        )
        haiku_str = (
            f"{_fmt_rate(m_only['b_accept_rate'])} ({m_only['b_acceptable']}/{m_only['b_judged']})"
        )
        sonnet_str = (
            f"{_fmt_rate(s_only['a_accept_rate'])} ({s_only['a_acceptable']}/{s_only['a_judged']})"
        )
        table_lines.append(
            f"| {entry['benchmark']} | {v1_str} | {haiku_str} | {sonnet_str} | "
            f"{_fmt_delta(s_only['delta'])} | {_fmt_delta(m_only['delta'])} | "
            f"{_fmt_delta(h['delta'])} |"
        )
    # Aggregate row
    s_only = aggregate["schema_only"]
    m_only = aggregate["model_only"]
    h = aggregate["headline"]
    v1_str = f"{_fmt_rate(s_only['b_accept_rate'])} ({s_only['b_acceptable']}/{s_only['b_judged']})"
    haiku_str = (
        f"{_fmt_rate(m_only['b_accept_rate'])} ({m_only['b_acceptable']}/{m_only['b_judged']})"
    )
    sonnet_str = (
        f"{_fmt_rate(s_only['a_accept_rate'])} ({s_only['a_acceptable']}/{s_only['a_judged']})"
    )
    table_lines.append(
        f"| **Aggregate** | {v1_str} | {haiku_str} | {sonnet_str} | "
        f"{_fmt_delta(s_only['delta'])} | {_fmt_delta(m_only['delta'])} | "
        f"{_fmt_delta(h['delta'])} |"
    )
    THREE_WAY_TABLE_MD.write_text("\n".join(table_lines) + "\n", encoding="utf-8")

    print(
        f"Wrote {THREE_WAY_COMPARISON_JSON} and {THREE_WAY_TABLE_MD}\n"
        f"  v2_sonnet_total_rows={payload['v2_sonnet_total_rows']}, "
        f"n_complete={payload['v2_sonnet_n_complete']}\n"
        f"  Aggregate: schema-only Δ={_fmt_delta(aggregate['schema_only']['delta'])}, "
        f"model-only Δ={_fmt_delta(aggregate['model_only']['delta'])}, "
        f"headline Δ={_fmt_delta(aggregate['headline']['delta'])}"
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute three-way comparison")
    parser.parse_args()
    compute()


if __name__ == "__main__":
    main()
