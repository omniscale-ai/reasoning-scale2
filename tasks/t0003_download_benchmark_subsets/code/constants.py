"""Constants for the benchmark-subset download task."""

from __future__ import annotations

from typing import Final

FRONTIERSCIENCE_SLUG: Final[str] = "frontierscience-olympiad-subset"
WORKARENA_PP_SLUG: Final[str] = "workarena-plus-plus-subset"
SWEBENCH_SLUG: Final[str] = "swebench-verified-subset"
TAUBENCH_SLUG: Final[str] = "taubench-subset"

RANDOM_SEED: Final[int] = 42
MIN_DECISIONS: Final[int] = 4
MAX_DECISIONS: Final[int] = 8

TASK_ID: Final[str] = "t0003_download_benchmark_subsets"
DATE_SUMMARIZED: Final[str] = "2026-04-29"

BENCHMARK_FRONTIERSCIENCE: Final[str] = "FrontierScience-Olympiad"
BENCHMARK_WORKARENA_PP: Final[str] = "WorkArena++"
BENCHMARK_SWEBENCH: Final[str] = "SWE-bench-Verified"
BENCHMARK_TAUBENCH: Final[str] = "tau-bench"

DOWNLOAD_STATUS_SUCCESS: Final[str] = "success"
DOWNLOAD_STATUS_FAILED: Final[str] = "failed"

ACCESS_PUBLIC: Final[str] = "public"
ACCESS_RESTRICTED: Final[str] = "restricted"
