from __future__ import annotations

import json
from pathlib import Path

from .metrics import compute_metrics, print_summary


def generate_report(results_dir: str | Path) -> None:
    results_dir = Path(results_dir)
    probes_file = results_dir / "probes.jsonl"

    if not probes_file.exists():
        print(f"No probes.jsonl found in {results_dir}")
        return

    probes = []
    for line in probes_file.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                probes.append(json.loads(line))
            except Exception:
                pass

    print(f"Loaded {len(probes)} probes from {probes_file}\n")
    metrics = compute_metrics(probes)
    print_summary(metrics)
    return metrics
