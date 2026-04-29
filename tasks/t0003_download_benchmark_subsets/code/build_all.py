"""Run all four benchmark builders and the access-status manifest builder."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable

from tasks.t0003_download_benchmark_subsets.code import (
    build_frontierscience,
    build_status_manifest,
    build_swebench,
    build_taubench,
    build_workarena_pp,
)


def main() -> int:
    builders: list[tuple[str, Callable[[], dict[str, object]]]] = [
        ("frontierscience-olympiad-subset", build_frontierscience.build),
        ("workarena-plus-plus-subset", build_workarena_pp.build),
        ("swebench-verified-subset", build_swebench.build),
        ("taubench-subset", build_taubench.build),
    ]
    results: list[dict[str, object]] = []
    for name, fn in builders:
        print(f"=== Building {name} ===", file=sys.stderr)
        result: dict[str, object] = fn()
        print(json.dumps(result, indent=2, default=str), file=sys.stderr)
        results.append({"dataset_id": name, **result})

    print("=== Building access-status manifest ===", file=sys.stderr)
    manifest: dict[str, object] = build_status_manifest.build_status_manifest()
    print(
        json.dumps({"results": results, "manifest_rows": len(manifest["rows"])}, indent=2),  # type: ignore[arg-type]
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
