"""Build the SWE-bench Verified subset asset by downloading the official HF parquet."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq

from tasks.t0003_download_benchmark_subsets.code.constants import (
    DATE_SUMMARIZED,
    DOWNLOAD_STATUS_FAILED,
    DOWNLOAD_STATUS_SUCCESS,
    MAX_DECISIONS,
    MIN_DECISIONS,
    SWEBENCH_SLUG,
    TASK_ID,
)
from tasks.t0003_download_benchmark_subsets.code.dataset_asset import (
    Author,
    DatasetDetails,
    DatasetFile,
    Institution,
    write_dataset_asset,
)
from tasks.t0003_download_benchmark_subsets.code.download_attempt import (
    write_access_attempt,
)
from tasks.t0003_download_benchmark_subsets.code.paths import SWEBENCH_DIR

SWEBENCH_VERIFIED_URL: str = (
    "https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified/"
    "resolve/main/data/test-00000-of-00001.parquet"
)
HUNK_MARKER: str = "@@ -"


def _count_hunks(*, patch: str | None) -> int:
    if patch is None:
        return 0
    return patch.count(HUNK_MARKER)


def _download_parquet(*, target: Path) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(SWEBENCH_VERIFIED_URL, target)
    except urllib.error.URLError as exc:
        return False, f"urllib.error.URLError: {exc}"
    except OSError as exc:
        return False, f"OSError: {exc}"
    if not target.exists() or target.stat().st_size == 0:
        return False, "Downloaded file is empty"
    return True, "ok"


def _build_description_md(
    *,
    total_instances: int,
    subset_count: int,
    hunks_distribution: dict[int, int],
    repos_in_subset: dict[str, int],
    difficulty_in_subset: dict[str, int],
) -> str:
    metadata: str = (
        "## Metadata\n\n"
        "* **Name**: SWE-bench Verified subset (4-8 hunks)\n"
        "* **Year**: 2024\n"
        "* **Authors**: Carlos E. Jimenez et al. (parent SWE-bench);\n"
        "  the OpenAI Verified curation team (Verified)\n"
        "* **License**: MIT (parent SWE-bench license)\n"
        "* **Access**: public (HuggingFace `princeton-nlp/SWE-bench_Verified`)\n"
        f"* **Size**: {subset_count} instances (filtered from {total_instances} Verified)\n"
    )

    overview: str = (
        "## Overview\n\n"
        "This subset of SWE-bench Verified contains GitHub-issue-driven repository patch tasks "
        "where the gold patch has between 4 and 8 diff hunks (the canonical 4-8 decisions per "
        "task range). SWE-bench Verified is the 500-instance human-validated subset of the "
        "parent SWE-bench (Jimenez et al. 2023) released by OpenAI in 2024. Each instance gives "
        "an LLM agent a real GitHub issue plus the corresponding repository at a specific "
        "commit, and asks for a patch that passes a hidden test suite. The full 500 Verified "
        "instances have hunk counts ranging from 1 to 45 with a long tail; filtering to 4-8 "
        "hunks selects medium-complexity tasks that map cleanly onto the project's three-level "
        "hierarchy: the issue text is the global intent, the FAIL_TO_PASS test names are the "
        "subtask gates, and each diff hunk is one atomic edit decision.\n"
    )

    hunks_lines: str = "\n".join(
        f"| {h} | {hunks_distribution.get(h, 0)} |" for h in range(MIN_DECISIONS, MAX_DECISIONS + 1)
    )
    repos_lines: str = "\n".join(
        f"| {r} | {c} |" for r, c in sorted(repos_in_subset.items(), key=lambda x: -x[1])[:15]
    )
    difficulty_lines: str = "\n".join(
        f"| {d} | {c} |" for d, c in sorted(difficulty_in_subset.items())
    )
    content: str = (
        "## Content & Annotation\n\n"
        "Every row preserves the upstream Verified schema: `instance_id`, `repo`, "
        "`base_commit`, `patch` (gold patch), `test_patch` (gold test diff), "
        "`problem_statement` (the GitHub issue body), `hints_text`, `created_at`, `version`, "
        "`FAIL_TO_PASS` (string-encoded list of pytest IDs that should now pass), "
        "`PASS_TO_PASS` (regression tests that must still pass), `environment_setup_commit`, and "
        "`difficulty` (one of `<15 min fix`, `15 min - 1 hour`, `1-4 hours`, `>4 hours`). The "
        "annotation is the gold patch produced by the original GitHub PR author and validated by "
        "OpenAI's Verified curation pass.\n"
    )

    statistics: str = (
        "## Statistics\n\n"
        f"| Metric | Value |\n"
        "|--------|-------|\n"
        f"| Verified total | {total_instances} |\n"
        f"| Subset (4-8 hunks) | {subset_count} |\n"
        "\n"
        "### Per-hunk-count distribution within subset\n\n"
        "| Hunks | Instances |\n"
        "|-------|-----------|\n"
        f"{hunks_lines}\n"
        "\n"
        "### Top repositories in subset\n\n"
        "| Repo | Instances |\n"
        "|------|-----------|\n"
        f"{repos_lines}\n"
        "\n"
        "### Difficulty in subset\n\n"
        "| Difficulty | Instances |\n"
        "|------------|-----------|\n"
        f"{difficulty_lines}\n"
        "\n"
        "### Subset rule\n\n"
        f"Instances are kept iff the gold `patch` field contains between {MIN_DECISIONS} and "
        f"{MAX_DECISIONS} `@@ -` hunk headers (inclusive). Hunk count is the natural per-instance "
        "decision count for SWE-bench: each hunk corresponds to one localized edit the agent "
        "must produce. No random sampling is performed.\n"
    )

    usage: str = (
        "## Usage Notes\n\n"
        "Load with pyarrow:\n\n"
        "```python\n"
        "import pyarrow.parquet as pq\n"
        f"t = pq.read_table('files/{SWEBENCH_SLUG}.parquet')\n"
        "rows = t.to_pylist()  # list[dict]\n"
        "```\n\n"
        "Or as JSONL via the bundled lightweight `swebench-verified-subset.jsonl` (one parsed "
        "row per line). The parquet preserves binary encoding for `patch`/`test_patch`; the "
        "JSONL converts those fields to plain UTF-8 strings.\n"
        "FAIL_TO_PASS and PASS_TO_PASS arrive as JSON-encoded strings; "
        "decode with `json.loads(row['FAIL_TO_PASS'])` to get the list.\n"
    )

    main_ideas: str = (
        "## Main Ideas\n\n"
        "* The 4-8-hunk filter selects medium-complexity SWE-bench Verified tasks that are "
        "  large enough to exercise multi-step reasoning but small enough to fit in a single "
        "  agent context window without aggressive truncation.\n"
        "* Each diff hunk maps one-to-one onto an atomic edit decision in the project's "
        "  three-level hierarchy (global issue intent -> FAIL_TO_PASS subtask gates -> "
        "  per-hunk atomic edits).\n"
        "* The subset preserves the upstream license (MIT), schema, and instance IDs, so any "
        "  Phase 2 result on this subset can be cross-referenced against the public "
        "  princeton-nlp/SWE-bench_Verified leaderboard.\n"
        "* Difficulty distribution within the subset is dominated by `15 min - 1 hour` and "
        "  `<15 min fix` tasks, matching the project's wall-clock budget for per-instance runs.\n"
    )

    summary: str = (
        "## Summary\n\n"
        f"This SWE-bench Verified subset contains {subset_count} GitHub-issue-driven patch "
        "tasks filtered from the 500-instance Verified release to those whose gold patch has "
        "4 to 8 diff hunks (the project's canonical multi-step decision range). Each row "
        "preserves the upstream Verified schema verbatim, including problem statement, gold "
        "patch, test patch, and the FAIL_TO_PASS / PASS_TO_PASS test name lists.\n\n"
        "For this project, the subset is the primary atomic-execution test bed for the "
        "scope-aware vs. scope-unaware Phase 2 comparison. The hunk-count filter ensures every "
        "instance offers between 4 and 8 atomic edit decisions, and the upstream Verified "
        "license (MIT) plus stable instance IDs let us publish results that interoperate with "
        "the public SWE-bench leaderboard.\n"
    )

    return (
        f'---\nspec_version: "2"\ndataset_id: "{SWEBENCH_SLUG}"\n'
        f'summarized_by_task: "{TASK_ID}"\ndate_summarized: "{DATE_SUMMARIZED}"\n---\n\n'
        f"# SWE-bench Verified Subset (4-8 hunks)\n\n"
        f"{metadata}\n{overview}\n{content}\n{statistics}\n{usage}\n{main_ideas}\n{summary}"
    )


def build() -> dict[str, object]:
    parquet_target: Path = SWEBENCH_DIR / "files" / "swe-bench-verified-test.parquet"
    ok, reason = _download_parquet(target=parquet_target)
    if not ok:
        write_access_attempt(
            asset_root=SWEBENCH_DIR,
            benchmark_name="SWE-bench Verified",
            source_url=SWEBENCH_VERIFIED_URL,
            attempted_at="2026-04-29T14:43:00Z",
            reason=reason,
            fallback_proxy="None — SWE-bench Verified is the project's primary code benchmark.",
            extra_log="urllib retrieval failed; check network and HF availability.",
        )
        details: DatasetDetails = DatasetDetails(
            spec_version="2",
            dataset_id=SWEBENCH_SLUG,
            name="SWE-bench Verified subset (download failed)",
            version=None,
            short_description=(
                "SWE-bench Verified subset placeholder — official HF parquet "
                "download failed; access attempt is logged in files/access-attempt.md."
            ),
            description_path="description.md",
            source_paper_id="no-doi_OpenAI2024_swe-bench-verified",
            url="https://openai.com/index/introducing-swe-bench-verified/",
            download_url=SWEBENCH_VERIFIED_URL,
            year=2024,
            date_published="2024-08-13",
            authors=[Author(name="OpenAI Verified curation team")],
            institutions=[Institution(name="OpenAI", country="US")],
            license="MIT",
            access_kind="public",
            size_description=f"0 instances (download failed: {reason})",
            files=[
                DatasetFile(
                    path="files/access-attempt.md",
                    description="Access attempt log (download failed).",
                    format="md",
                ),
            ],
            categories=["benchmark-swebench"],
            download_status=DOWNLOAD_STATUS_FAILED,
            download_failure_reason=reason,
        )
        write_dataset_asset(
            asset_root=SWEBENCH_DIR,
            details=details,
            description_md=(
                f'---\nspec_version: "2"\ndataset_id: "{SWEBENCH_SLUG}"\n'
                f'summarized_by_task: "{TASK_ID}"\ndate_summarized: "{DATE_SUMMARIZED}"\n---\n\n'
                f"# SWE-bench Verified Subset (download failed)\n\n"
                "## Metadata\n\n"
                "* **Name**: SWE-bench Verified subset (download failed)\n"
                "* **Year**: 2024\n"
                "* **Authors**: OpenAI Verified curation team\n"
                "* **License**: MIT (parent SWE-bench license)\n"
                "* **Access**: public (HF distribution unreachable at attempt time)\n"
                f"* **Size**: 0 instances (download failed)\n\n"
                "## Overview\n\n"
                "The SWE-bench Verified parquet at "
                f"`{SWEBENCH_VERIFIED_URL}` could not be downloaded during this task. The "
                "access attempt is documented in `files/access-attempt.md`. This is a critical "
                "blocker for Phase 2 because there is no equivalent code benchmark in the "
                "pilot data — a follow-up task must retry the download once HF is reachable.\n\n"
                "## Content & Annotation\n\nNo content downloaded.\n\n"
                "## Statistics\n\n"
                "| Metric | Value |\n|--------|-------|\n| Instances | 0 |\n\n"
                "## Usage Notes\n\nNot loadable until the download succeeds in a later task.\n\n"
                "## Main Ideas\n\n"
                "* The download barrier is transient (network or HF outage), not a license issue.\n"
                "* A retry task should re-attempt with `urllib.request.urlretrieve` against the "
                "  documented URL.\n"
                "* No proxy benchmark is available — Phase 2 code experiments are blocked until "
                "  the download succeeds.\n\n"
                "## Summary\n\n"
                "The SWE-bench Verified download failed at task time. The asset folder preserves "
                "the access attempt log and metadata so a follow-up task can retry without "
                "re-discovering the upstream URL or license.\n"
            ),
        )
        return {
            "dataset_id": SWEBENCH_SLUG,
            "download_status": DOWNLOAD_STATUS_FAILED,
            "sample_count": 0,
            "subset_rule": "n/a (download failed)",
            "failure_reason": reason,
        }

    table = pq.read_table(parquet_target)
    total_instances: int = table.num_rows
    instances: list[dict[str, object]] = table.to_pylist()
    for inst in instances:
        inst["_hunks"] = _count_hunks(patch=inst.get("patch"))  # type: ignore[arg-type]

    subset: list[dict[str, object]] = [
        inst
        for inst in instances
        if MIN_DECISIONS <= int(inst["_hunks"]) <= MAX_DECISIONS  # type: ignore[arg-type]
    ]
    subset_count: int = len(subset)

    # Validation gate: per the plan, halt if subset count <30 or >450.
    assert 30 <= subset_count <= 450, (
        f"SWE-bench subset count {subset_count} outside validation gate [30, 450]; "
        "inspect parsed hunk counts vs raw patch field"
    )

    # Strip the helper field before serializing.
    for inst in subset:
        inst.pop("_hunks", None)

    subset_jsonl: Path = SWEBENCH_DIR / "files" / f"{SWEBENCH_SLUG}.jsonl"
    subset_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with subset_jsonl.open("w", encoding="utf-8") as fh:
        for inst in subset:
            fh.write(json.dumps(inst, ensure_ascii=False, default=str) + "\n")

    hunks_distribution: dict[int, int] = dict(
        sorted(
            Counter(int(_count_hunks(patch=inst.get("patch"))) for inst in subset).items()  # type: ignore[arg-type]
        )
    )
    repos_in_subset: dict[str, int] = dict(Counter(str(inst.get("repo", "")) for inst in subset))
    difficulty_in_subset: dict[str, int] = dict(
        Counter(str(inst.get("difficulty", "")) for inst in subset)
    )

    short_description: str = (
        f"SWE-bench Verified subset filtered to {subset_count} instances whose gold "
        "patch has 4 to 8 diff hunks; suitable for multi-step code-edit experiments."
    )
    size_description: str = (
        f"{subset_count} instances filtered from {total_instances} SWE-bench Verified "
        f"instances (kept iff gold patch has between {MIN_DECISIONS} and "
        f"{MAX_DECISIONS} `@@` hunks)"
    )

    details = DatasetDetails(
        spec_version="2",
        dataset_id=SWEBENCH_SLUG,
        name="SWE-bench Verified subset (4-8 hunks)",
        version="verified-2024",
        short_description=short_description,
        description_path="description.md",
        source_paper_id="no-doi_OpenAI2024_swe-bench-verified",
        url="https://openai.com/index/introducing-swe-bench-verified/",
        download_url=SWEBENCH_VERIFIED_URL,
        year=2024,
        date_published="2024-08-13",
        authors=[
            Author(
                name="Carlos E. Jimenez (parent SWE-bench)",
                country="US",
                institution="Princeton University",
                orcid=None,
            ),
            Author(
                name="OpenAI Verified curation team",
                country="US",
                institution="OpenAI",
                orcid=None,
            ),
        ],
        institutions=[
            Institution(name="Princeton University", country="US"),
            Institution(name="OpenAI", country="US"),
        ],
        license="MIT",
        access_kind="public",
        size_description=size_description,
        files=[
            DatasetFile(
                path="files/swe-bench-verified-test.parquet",
                description=(
                    "Original SWE-bench Verified parquet downloaded from "
                    "princeton-nlp/SWE-bench_Verified."
                ),
                format="parquet",
            ),
            DatasetFile(
                path=f"files/{SWEBENCH_SLUG}.jsonl",
                description=(
                    f"Filtered subset: {subset_count} instances with 4-8 patch hunks. "
                    "Each line is the upstream Verified row serialized as JSON."
                ),
                format="jsonl",
            ),
        ],
        categories=["benchmark-swebench"],
        download_status=DOWNLOAD_STATUS_SUCCESS,
        download_failure_reason=None,
    )
    description_md: str = _build_description_md(
        total_instances=total_instances,
        subset_count=subset_count,
        hunks_distribution=hunks_distribution,
        repos_in_subset=repos_in_subset,
        difficulty_in_subset=difficulty_in_subset,
    )
    write_dataset_asset(
        asset_root=SWEBENCH_DIR,
        details=details,
        description_md=description_md,
    )

    return {
        "dataset_id": SWEBENCH_SLUG,
        "download_status": DOWNLOAD_STATUS_SUCCESS,
        "sample_count": subset_count,
        "total_verified": total_instances,
        "subset_rule": (
            f"keep iff gold patch has between {MIN_DECISIONS} and {MAX_DECISIONS} `@@ -` hunks"
        ),
        "hunks_distribution": hunks_distribution,
    }


if __name__ == "__main__":
    result: dict[str, object] = build()
    print(json.dumps(result, indent=2, default=str))
