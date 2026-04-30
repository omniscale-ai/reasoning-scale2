"""Compute v2 statistics and v1-vs-v2 comparison.

Reads the v2 final dataset asset and the v1 dataset asset, computes per-benchmark accept-rate
deltas, and writes:

- `code/_outputs/v1_vs_v2_comparison.json` — structured comparison
- `code/_outputs/v1_vs_v2_table.md` — markdown table fragment for results_detailed.md
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from tasks.t0009_hierarchical_annotation_v2.code.paths import (
    OUTPUTS_DIR,
    V1_INPUT_PATH,
    V1_VS_V2_COMPARISON_JSON,
    V1_VS_V2_TABLE_MD,
    V2_FINAL_JSONL,
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


def _completeness_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "complete": 0})
    for row in rows:
        bench = row.get("benchmark", "")
        out[bench]["total"] += 1
        if row.get("hierarchy_completeness"):
            out[bench]["complete"] += 1
    return dict(out)


def _global_atomics_fraction(rows: list[dict[str, Any]]) -> tuple[int, int, float | None]:
    total_global_atomics = 0
    total_subtask_atomics = 0
    for row in rows:
        hierarchy = row.get("hierarchy") or {}
        total_global_atomics += len(hierarchy.get("global_atomics", []) or [])
        for sub in hierarchy.get("subtasks", []) or []:
            total_subtask_atomics += len(sub.get("atomics", []) or [])
    denom = total_global_atomics + total_subtask_atomics
    fraction = total_global_atomics / denom if denom > 0 else None
    return total_global_atomics, total_subtask_atomics, fraction


def _mean_atomics_per_row(rows: list[dict[str, Any]]) -> float | None:
    if not rows:
        return None
    totals: list[int] = []
    for row in rows:
        hierarchy = row.get("hierarchy") or {}
        count = len(hierarchy.get("global_atomics", []) or [])
        for sub in hierarchy.get("subtasks", []) or []:
            count += len(sub.get("atomics", []) or [])
        totals.append(count)
    return sum(totals) / len(totals) if totals else None


def compute() -> dict[str, Any]:
    v2_rows = _load_jsonl(path=V2_FINAL_JSONL)
    v1_rows = _load_jsonl(path=V1_INPUT_PATH)

    v2_judge = _benchmark_judge_summary(v2_rows)
    v1_judge = _benchmark_judge_summary(v1_rows)

    benches = sorted(set(v2_judge) | set(v1_judge))
    deltas: list[dict[str, Any]] = []
    for bench in benches:
        v2 = v2_judge.get(bench, {})
        v1 = v1_judge.get(bench, {})
        v2_rate = v2.get("accept_rate")
        v1_rate = v1.get("accept_rate")
        if v2_rate is not None and v1_rate is not None:
            delta = v2_rate - v1_rate
            improved = delta > 0
        else:
            delta = None
            improved = None
        deltas.append(
            {
                "benchmark": bench,
                "v1_judged": v1.get("judged", 0),
                "v1_acceptable": v1.get("acceptable", 0),
                "v1_accept_rate": v1_rate,
                "v2_judged": v2.get("judged", 0),
                "v2_acceptable": v2.get("acceptable", 0),
                "v2_accept_rate": v2_rate,
                "delta": delta,
                "v2_improved": improved,
            }
        )

    completeness = _completeness_summary(v2_rows)
    n_complete_v2 = sum(b["complete"] for b in completeness.values())

    total_global_atomics, total_subtask_atomics, ga_fraction = _global_atomics_fraction(v2_rows)
    mean_atomics = _mean_atomics_per_row(v2_rows)

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "v2_total_rows": len(v2_rows),
        "v1_total_rows": len(v1_rows),
        "v2_completeness_per_benchmark": completeness,
        "v2_n_complete": n_complete_v2,
        "v2_global_atomics_count": total_global_atomics,
        "v2_subtask_atomics_count": total_subtask_atomics,
        "v2_global_atomics_fraction": ga_fraction,
        "mean_atomics_per_row_v2": mean_atomics,
        "per_benchmark": deltas,
    }
    V1_VS_V2_COMPARISON_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    table_lines = [
        "| Benchmark | v1 judged | v1 accept rate | v2 judged | v2 accept rate | Δ |",
        "|-----------|-----------|----------------|-----------|----------------|---|",
    ]
    for d in deltas:
        v1_rate_str = (
            f"{d['v1_accept_rate']:.0%} ({d['v1_acceptable']}/{d['v1_judged']})"
            if d["v1_accept_rate"] is not None
            else "n/a"
        )
        v2_rate_str = (
            f"{d['v2_accept_rate']:.0%} ({d['v2_acceptable']}/{d['v2_judged']})"
            if d["v2_accept_rate"] is not None
            else "n/a"
        )
        delta_str = f"{d['delta']:+.0%}" if d["delta"] is not None else "n/a"
        table_lines.append(
            f"| {d['benchmark']} | {d['v1_judged']} | {v1_rate_str} | "
            f"{d['v2_judged']} | {v2_rate_str} | {delta_str} |"
        )
    V1_VS_V2_TABLE_MD.write_text("\n".join(table_lines) + "\n", encoding="utf-8")

    print(
        f"Wrote {V1_VS_V2_COMPARISON_JSON} and {V1_VS_V2_TABLE_MD}\n"
        f"  v2_total_rows={payload['v2_total_rows']}, "
        f"n_complete={payload['v2_n_complete']}, "
        f"mean_atomics={mean_atomics:.2f}, "
        f"global_atomics_fraction={ga_fraction:.3f}"
    ) if mean_atomics is not None and ga_fraction is not None else print(
        f"Wrote {V1_VS_V2_COMPARISON_JSON} and {V1_VS_V2_TABLE_MD} (some stats unavailable)"
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute v1-vs-v2 comparison")
    parser.parse_args()
    compute()


if __name__ == "__main__":
    main()
