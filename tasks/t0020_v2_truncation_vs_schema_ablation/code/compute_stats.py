"""Compute three-way comparison and decomposition for t0020.

Reads:
- v2-tree-truncated judge outcomes (this task) — produced by `v2_truncated_judge.py`.
- v2-tree-full judge outcomes (t0009 reference) — filtered to the same `_pilot_row_index` set as
  this task's truncated judge sample (paired comparison).
- v1-flat-truncated judge verdicts (t0005 reference) — extracted from the v1 source jsonl.

Computes:
- Accept rate with Wilson 95% CI for each of the three conditions.
- pure-schema delta = v2-tree-truncated - v1-flat-truncated (UNPAIRED, different rows).
- pure-text delta   = v2-tree-full - v2-tree-truncated (PAIRED on the same _pilot_row_index set).

Outputs:
- `code/_outputs/three_way_comparison.json` — structured comparison.
- `code/_outputs/three_way_table.md` — markdown table for `results_detailed.md`.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from tasks.t0020_v2_truncation_vs_schema_ablation.code.paths import (
    OUTPUTS_DIR,
    THREE_WAY_COMPARISON_JSON,
    THREE_WAY_TABLE_MD,
    V1_INPUT_PATH,
    V2_HAIKU_JUDGE_OUTCOMES_PATH,
    V2_TRUNCATED_JUDGE_OUTCOMES_PATH,
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


def _benchmark_summary_from_outcomes(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Group rows by benchmark, count acceptable/needs_revision/total."""
    out: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"total": 0, "judged": 0, "acceptable": 0, "needs_revision": 0}
    )
    for row in rows:
        bench = row.get("benchmark", "")
        out[bench]["total"] += 1
        verdict = row.get("verdict") if "verdict" in row else row.get("judge_verdict")
        if verdict == "acceptable":
            out[bench]["acceptable"] += 1
            out[bench]["judged"] += 1
        elif verdict == "needs revision":
            out[bench]["needs_revision"] += 1
            out[bench]["judged"] += 1
    for _bench, b in out.items():
        b["accept_rate"] = (b["acceptable"] / b["judged"]) if b["judged"] > 0 else None
    return dict(out)


def _aggregate_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_judged = 0
    total_acceptable = 0
    total_needs_revision = 0
    for row in rows:
        verdict = row.get("verdict") if "verdict" in row else row.get("judge_verdict")
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
    """Wilson 95% confidence interval for a binomial proportion."""
    if n <= 0:
        return None, None
    phat = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (phat + z2 / (2.0 * n)) / denom
    half = (z * math.sqrt(phat * (1.0 - phat) / n + z2 / (4.0 * n * n))) / denom
    return center - half, center + half


def _wilson_diff_ci(
    *, k1: int, n1: int, k2: int, n2: int, z: float = 1.96
) -> tuple[float | None, float | None]:
    """Newcombe-Wilson 95% CI for the DIFFERENCE of two independent proportions p1 - p2.

    Reference: Newcombe (1998), method 10. Returns (lower, upper) on (p1 - p2).
    Returns (None, None) if either n is 0.
    """
    if n1 <= 0 or n2 <= 0:
        return None, None
    l1, u1 = _wilson_ci(k=k1, n=n1, z=z)
    l2, u2 = _wilson_ci(k=k2, n=n2, z=z)
    if l1 is None or u1 is None or l2 is None or u2 is None:
        return None, None
    p1 = k1 / n1
    p2 = k2 / n2
    delta = p1 - p2
    lower = delta - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    upper = delta + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return lower, upper


def _delta_with_ci(*, a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Return a dict describing accept-rate delta a - b with Wilson CI on diff and each rate."""
    a_rate = a.get("accept_rate")
    b_rate = b.get("accept_rate")
    delta = (a_rate - b_rate) if a_rate is not None and b_rate is not None else None
    a_lo, a_hi = _wilson_ci(k=int(a.get("acceptable", 0)), n=int(a.get("judged", 0)))
    b_lo, b_hi = _wilson_ci(k=int(b.get("acceptable", 0)), n=int(b.get("judged", 0)))
    diff_lo, diff_hi = _wilson_diff_ci(
        k1=int(a.get("acceptable", 0)),
        n1=int(a.get("judged", 0)),
        k2=int(b.get("acceptable", 0)),
        n2=int(b.get("judged", 0)),
    )
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
        "delta_ci_low": diff_lo,
        "delta_ci_high": diff_hi,
    }


def _v1_judged_outcomes() -> list[dict[str, Any]]:
    """Read t0005 v1 jsonl and return rows that have a judge_verdict (12 rows)."""
    rows = _load_jsonl(path=V1_INPUT_PATH)
    return [r for r in rows if r.get("judge_verdict") in {"acceptable", "needs revision"}]


def _filter_haiku_outcomes_to_indices(*, indices: set[int]) -> list[dict[str, Any]]:
    """Read t0009 v2-haiku judge outcomes and filter to the given _pilot_row_index set."""
    rows = _load_jsonl(path=V2_HAIKU_JUDGE_OUTCOMES_PATH)
    out: list[dict[str, Any]] = []
    for r in rows:
        idx = r.get("pilot_row_index")
        if isinstance(idx, int) and idx in indices:
            out.append(r)
    return out


def compute() -> dict[str, Any]:
    truncated_outcomes = _load_jsonl(path=V2_TRUNCATED_JUDGE_OUTCOMES_PATH)
    truncated_indices: set[int] = {
        int(r["pilot_row_index"]) for r in truncated_outcomes if "pilot_row_index" in r
    }

    full_outcomes = _filter_haiku_outcomes_to_indices(indices=truncated_indices)
    v1_outcomes = _v1_judged_outcomes()

    truncated_per_bench = _benchmark_summary_from_outcomes(truncated_outcomes)
    full_per_bench = _benchmark_summary_from_outcomes(full_outcomes)
    v1_per_bench = _benchmark_summary_from_outcomes(v1_outcomes)

    truncated_agg = _aggregate_summary(truncated_outcomes)
    full_agg = _aggregate_summary(full_outcomes)
    v1_agg = _aggregate_summary(v1_outcomes)

    benches = sorted(set(truncated_per_bench) | set(full_per_bench) | set(v1_per_bench))
    per_benchmark: list[dict[str, Any]] = []
    for bench in benches:
        t = truncated_per_bench.get(
            bench, {"judged": 0, "acceptable": 0, "needs_revision": 0, "accept_rate": None}
        )
        f = full_per_bench.get(
            bench, {"judged": 0, "acceptable": 0, "needs_revision": 0, "accept_rate": None}
        )
        v = v1_per_bench.get(
            bench, {"judged": 0, "acceptable": 0, "needs_revision": 0, "accept_rate": None}
        )
        per_benchmark.append(
            {
                "benchmark": bench,
                "v1_flat_truncated": v,
                "v2_tree_truncated": t,
                "v2_tree_full": f,
                "pure_schema": _delta_with_ci(a=t, b=v),
                "pure_text": _delta_with_ci(a=f, b=t),
                "headline": _delta_with_ci(a=f, b=v),
            }
        )

    aggregate = {
        "v1_flat_truncated": v1_agg,
        "v2_tree_truncated": truncated_agg,
        "v2_tree_full": full_agg,
        "pure_schema": _delta_with_ci(a=truncated_agg, b=v1_agg),
        "pure_text": _delta_with_ci(a=full_agg, b=truncated_agg),
        "headline": _delta_with_ci(a=full_agg, b=v1_agg),
    }

    # Extra diagnostics: which indices are in the paired comparison?
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "n_truncated_judged": truncated_agg["judged"],
        "n_full_judged_paired": full_agg["judged"],
        "n_v1_judged": v1_agg["judged"],
        "paired_indices": sorted(truncated_indices),
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
        "| Benchmark | v1-flat-trunc | v2-tree-trunc | v2-tree-full | "
        "Δ pure-schema | Δ pure-text | Δ headline |",
        "|-----------|---------------|----------------|---------------|"
        "----------------|--------------|------------|",
    ]
    for entry in per_benchmark:
        v1 = entry["v1_flat_truncated"]
        t = entry["v2_tree_truncated"]
        f = entry["v2_tree_full"]
        ps = entry["pure_schema"]
        pt = entry["pure_text"]
        hd = entry["headline"]
        v1_str = f"{_fmt_rate(v1['accept_rate'])} ({v1['acceptable']}/{v1['judged']})"
        t_str = f"{_fmt_rate(t['accept_rate'])} ({t['acceptable']}/{t['judged']})"
        f_str = f"{_fmt_rate(f['accept_rate'])} ({f['acceptable']}/{f['judged']})"
        table_lines.append(
            f"| {entry['benchmark']} | {v1_str} | {t_str} | {f_str} | "
            f"{_fmt_delta(ps['delta'])} | {_fmt_delta(pt['delta'])} | "
            f"{_fmt_delta(hd['delta'])} |"
        )
    # Aggregate row.
    v1 = aggregate["v1_flat_truncated"]
    t = aggregate["v2_tree_truncated"]
    f = aggregate["v2_tree_full"]
    ps = aggregate["pure_schema"]
    pt = aggregate["pure_text"]
    hd = aggregate["headline"]
    v1_str = f"{_fmt_rate(v1['accept_rate'])} ({v1['acceptable']}/{v1['judged']})"
    t_str = f"{_fmt_rate(t['accept_rate'])} ({t['acceptable']}/{t['judged']})"
    f_str = f"{_fmt_rate(f['accept_rate'])} ({f['acceptable']}/{f['judged']})"
    table_lines.append(
        f"| **Aggregate** | {v1_str} | {t_str} | {f_str} | "
        f"{_fmt_delta(ps['delta'])} | {_fmt_delta(pt['delta'])} | "
        f"{_fmt_delta(hd['delta'])} |"
    )
    THREE_WAY_TABLE_MD.write_text("\n".join(table_lines) + "\n", encoding="utf-8")

    print(
        f"Wrote {THREE_WAY_COMPARISON_JSON} and {THREE_WAY_TABLE_MD}\n"
        f"  n_truncated={payload['n_truncated_judged']}, "
        f"n_full_paired={payload['n_full_judged_paired']}, n_v1={payload['n_v1_judged']}\n"
        f"  Aggregate: pure-schema Δ={_fmt_delta(ps['delta'])}, "
        f"pure-text Δ={_fmt_delta(pt['delta'])}, "
        f"headline Δ={_fmt_delta(hd['delta'])}"
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute three-way comparison")
    parser.parse_args()
    compute()


if __name__ == "__main__":
    main()
