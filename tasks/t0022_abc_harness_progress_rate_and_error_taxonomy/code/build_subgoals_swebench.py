"""Build the SWE-bench Verified Lite subgoal JSON.

Pulls the SWE-bench Verified split from Hugging Face (cached locally on first run),
filters to the easy subset (`difficulty == "<15 min fix"`) — the working
definition of "Verified Lite" — and emits >= 50 EnvironmentSubgoals entries.

Subgoals are derived heuristically from the gold-patch `diff --git a/<path>`
headers per the plan.md Step 8 schema:

* "Locate the relevant code in `<file>`."
* "Modify `<file>` to fix the bug."
* "Verify the fix preserves existing behavior."

Run via:
    uv run python -m \\
        tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.build_subgoals_swebench
"""  # noqa: E501

from __future__ import annotations

import json
import re
from typing import Any

from datasets import load_dataset  # type: ignore[import-untyped]

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.paths import (
    LIBRARY_ASSET_FILES_DIR,
    SUBGOALS_SWEBENCH_JSON,
)

EASY_DIFFICULTY: str = "<15 min fix"
TARGET_INSTANCES: int = 60  # >= 50 per plan REQ-6
DIFF_HEADER_RE: re.Pattern[str] = re.compile(r"^diff --git a/(\S+)")
MAX_FILE_PATHS: int = 3


def _extract_file_paths(*, patch: str) -> list[str]:
    paths: list[str] = []
    seen: set[str] = set()
    for line in patch.splitlines():
        m = DIFF_HEADER_RE.match(line)
        if m is None:
            continue
        path = m.group(1)
        if path in seen:
            continue
        seen.add(path)
        paths.append(path)
        if len(paths) >= MAX_FILE_PATHS:
            break
    return paths


def _build_one(*, instance_id: str, patch: str) -> dict[str, Any] | None:
    paths = _extract_file_paths(patch=patch)
    if len(paths) == 0:
        return None
    subgoals: list[dict[str, str]] = []
    if len(paths) == 1:
        path = paths[0]
        subgoals = [
            {"id": "g1", "description": f"Locate the relevant code in `{path}`."},
            {"id": "g2", "description": f"Modify `{path}` to fix the reported bug."},
            {
                "id": "g3",
                "description": "Verify the fix preserves existing behavior on related tests.",
            },
        ]
    else:
        for i, path in enumerate(paths, start=1):
            subgoals.append(
                {
                    "id": f"g{i}",
                    "description": f"Edit `{path}` as part of the multi-file fix.",
                }
            )
    return {"environment_id": instance_id, "subgoals": subgoals}


def main() -> None:
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    environments: list[dict[str, Any]] = []
    for row in ds:
        if row.get("difficulty") != EASY_DIFFICULTY:
            continue
        instance_id = row.get("instance_id")
        patch = row.get("patch", "")
        if not isinstance(instance_id, str) or not isinstance(patch, str):
            continue
        env = _build_one(instance_id=instance_id, patch=patch)
        if env is None:
            continue
        environments.append(env)
        if len(environments) >= TARGET_INSTANCES:
            break
    assert len(environments) >= 50, (
        f"only {len(environments)} environments built; need >= 50 per REQ-6"
    )
    LIBRARY_ASSET_FILES_DIR.mkdir(parents=True, exist_ok=True)
    SUBGOALS_SWEBENCH_JSON.write_text(
        json.dumps(environments, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(environments)} environments to {SUBGOALS_SWEBENCH_JSON}")
    sub_counts = [len(e["subgoals"]) for e in environments]
    mean_subgoals = sum(sub_counts) / len(sub_counts)
    print(f"  subgoals/env: min={min(sub_counts)} max={max(sub_counts)} mean={mean_subgoals:.1f}")


if __name__ == "__main__":
    main()
