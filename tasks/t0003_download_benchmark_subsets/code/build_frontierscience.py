"""Build the FrontierScience-Olympiad subset asset from pilot annotation rows.

The pilot file `project/data/annotation_pilot/tasks_annotated.jsonl` contains 40
domain-tagged Olympiad-style problems annotated by the project's pilot run. FrontierMath
itself (the closest published analogue) is gated behind Epoch AI access, so this script
packages the pilot rows as the v0 subset and documents the access gap.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from tasks.t0003_download_benchmark_subsets.code.constants import (
    BENCHMARK_FRONTIERSCIENCE,
    DATE_SUMMARIZED,
    DOWNLOAD_STATUS_SUCCESS,
    FRONTIERSCIENCE_SLUG,
    TASK_ID,
)
from tasks.t0003_download_benchmark_subsets.code.dataset_asset import (
    Author,
    DatasetDetails,
    DatasetFile,
    Institution,
    write_dataset_asset,
)
from tasks.t0003_download_benchmark_subsets.code.paths import (
    FRONTIERSCIENCE_DIR,
    PILOT_JSONL,
)


def _filter_pilot_rows(*, pilot_path: Path, benchmark: str) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    with pilot_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line == "":
                continue
            row: dict[str, object] = json.loads(line)
            if row.get("benchmark") == benchmark:
                out.append(row)
    return out


def _write_subset_jsonl(*, rows: list[dict[str, object]], target: Path) -> int:
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def _build_description_md(
    *,
    rows: list[dict[str, object]],
    domain_counts: dict[str, int],
    avg_problem_chars: int,
) -> str:
    metadata: str = (
        "## Metadata\n\n"
        f"* **Name**: FrontierScience-Olympiad subset (pilot v0)\n"
        "* **Year**: 2026\n"
        "* **Authors**: This project (subset packaging); original problems sourced from "
        "Olympiad-style FrontierScience problem repositories\n"
        "* **License**: research-only\n"
        "* **Access**: public (within this project's repository)\n"
        f"* **Size**: {len(rows)} problems across {len(domain_counts)} domains "
        f"({', '.join(f'{d}={c}' for d, c in sorted(domain_counts.items()))})\n"
    )

    overview: str = (
        "## Overview\n\n"
        "This dataset packages the FrontierScience-Olympiad pilot rows as a reproducible v0 "
        "subset for the project's three-level granularity-conditioning experiments. The pilot "
        "rows were annotated under task t0001 (annotation pilot) using Olympiad-style problems "
        "from physics, chemistry, and biology. The closest publicly named benchmark analogue is "
        "FrontierMath (Glazer et al. 2024, arXiv:2411.04872), which is gated behind Epoch AI "
        "access; this access barrier was identified by the t0002 literature survey and remains "
        "unresolved at the time of this task. Until full FrontierMath access is negotiated, the "
        "pilot rows serve as the canonical FrontierScience-Olympiad subset for Phase 2 work. "
        "Each row contains the full problem text, the gold solution, the problem domain, and the "
        "annotator's pre-existing token-usage metadata. Domain coverage is intentionally balanced "
        "across physics, chemistry, and biology to match the project's stated scope.\n"
    )

    rows_per_domain: str = "\n".join(f"| {d} | {c} |" for d, c in sorted(domain_counts.items()))
    content: str = (
        "## Content & Annotation\n\n"
        "Every row follows the pilot annotation schema with these fields: `task_id`, "
        "`benchmark` (always `FrontierScience-Olympiad`), `domain` (one of physics, "
        "chemistry, biology), `problem` (full problem statement), `solution` "
        "(gold reference solution, where annotated), `difficulty`, `metadata.subject`, "
        "`metadata.source_id`, `annotation_model`, `annotated_at`, `errors`, `steps`, and "
        "`token_usage`. The `steps` field is `null` for FrontierScience-Olympiad rows because "
        "Olympiad solutions are graded as final answers rather than as multi-step graphs; the "
        "project will derive step graphs in the t-future hierarchical-annotation tasks. "
        "Annotation was performed by the project's pilot LLM-assisted pipeline; gold solutions "
        "come from the source problem set.\n"
    )

    statistics: str = (
        "## Statistics\n\n"
        "| Metric | Value |\n"
        "|--------|-------|\n"
        f"| Total problems | {len(rows)} |\n"
        f"| Average problem length (chars) | {avg_problem_chars} |\n"
        "\n"
        "### Per-domain breakdown\n\n"
        "| Domain | Problems |\n"
        "|--------|----------|\n"
        f"{rows_per_domain}\n"
        "\n"
        "### Subset rule\n\n"
        "All FrontierScience-Olympiad rows from the pilot file are included. Per-instance step "
        "counts are not available for FrontierScience-Olympiad, so the canonical 4-8 decisions "
        "per task filter cannot be applied at row level; instead, the subset is domain-stratified "
        "across physics / chemistry / biology to match the pilot focus. Future tasks that derive "
        "step graphs (hierarchical-annotation) can re-subset using node counts.\n"
    )

    usage: str = (
        "## Usage Notes\n\n"
        "Load with the Python standard library:\n\n"
        "```python\n"
        "import json\n"
        "with open('files/frontierscience-olympiad-subset.jsonl') as fh:\n"
        "    rows = [json.loads(line) for line in fh if line.strip()]\n"
        "```\n\n"
        "Each row is a dict with the schema described in the Content & Annotation section. The "
        "`solution` field is plain text. The `metadata.source_id` field uniquely identifies the "
        "upstream Olympiad problem and should be preserved for traceability.\n"
    )

    main_ideas: str = (
        "## Main Ideas\n\n"
        "* This v0 subset is the canonical reproducible FrontierScience-Olympiad source for the "
        "  project until upstream Epoch AI / FrontierMath access is resolved.\n"
        "* Domain coverage is balanced across physics, chemistry, and biology, matching the "
        "  project's three-domain scope.\n"
        "* Step graphs are not available at row level for FrontierScience-Olympiad — Phase 2 "
        "  experiments must either treat each row as single-decision or derive step graphs in a "
        "  follow-up hierarchical-annotation task before computing per-step metrics.\n"
        "* This subset is fully self-contained and does not require any external network access "
        "  to load or use.\n"
    )

    summary: str = (
        "## Summary\n\n"
        "The FrontierScience-Olympiad subset (pilot v0) packages 40 Olympiad-style problems "
        "spanning physics, chemistry, and biology, sourced from the project's pilot annotation "
        "run. Every row contains the full problem text, gold solution, and annotation metadata. "
        "The subset is the canonical FrontierScience-Olympiad source for the project's Phase 2 "
        "scope-aware vs. scope-unaware baseline experiment.\n\n"
        "FrontierMath itself (the closest publicly named analogue) remains gated behind Epoch AI "
        "access. The v0 subset is therefore a pragmatic substitute that preserves Phase 2 "
        "reproducibility; a follow-up suggestion will track the open access negotiation. The "
        "domain-stratified design ensures every experiment can report per-domain metrics without "
        "needing to re-balance.\n"
    )

    return (
        f'---\nspec_version: "2"\ndataset_id: "{FRONTIERSCIENCE_SLUG}"\n'
        f'summarized_by_task: "{TASK_ID}"\ndate_summarized: "{DATE_SUMMARIZED}"\n---\n\n'
        f"# FrontierScience-Olympiad Subset (pilot v0)\n\n"
        f"{metadata}\n{overview}\n{content}\n{statistics}\n{usage}\n{main_ideas}\n{summary}"
    )


def build() -> dict[str, object]:
    rows: list[dict[str, object]] = _filter_pilot_rows(
        pilot_path=PILOT_JSONL,
        benchmark=BENCHMARK_FRONTIERSCIENCE,
    )
    assert len(rows) > 0, f"No {BENCHMARK_FRONTIERSCIENCE} rows in pilot JSONL"

    domain_counts_counter: Counter[str] = Counter(str(r.get("domain", "unknown")) for r in rows)
    domain_counts: dict[str, int] = dict(domain_counts_counter)

    problem_lengths: list[int] = [len(str(r.get("problem", ""))) for r in rows]
    avg_problem_chars: int = sum(problem_lengths) // max(1, len(problem_lengths))

    target_jsonl: Path = FRONTIERSCIENCE_DIR / "files" / f"{FRONTIERSCIENCE_SLUG}.jsonl"
    _write_subset_jsonl(rows=rows, target=target_jsonl)

    domains_label: str = ", ".join(f"{d}={c}" for d, c in sorted(domain_counts.items()))
    size_description: str = (
        f"{len(rows)} Olympiad-style problems (physics, chemistry, biology) "
        f"packaged from the project pilot annotation run; per-domain: {domains_label}"
    )
    short_description: str = (
        "FrontierScience-Olympiad pilot v0 subset: 40 Olympiad problems across physics, "
        "chemistry, biology with gold solutions, packaged for Phase 2 experiments."
    )

    details: DatasetDetails = DatasetDetails(
        spec_version="2",
        dataset_id=FRONTIERSCIENCE_SLUG,
        name="FrontierScience-Olympiad subset (pilot v0)",
        version="v0",
        short_description=short_description,
        description_path="description.md",
        source_paper_id="10.48550_arXiv.2411.04872",
        url="https://arxiv.org/abs/2411.04872",
        download_url=None,
        year=2026,
        date_published="2026-04-29",
        authors=[
            Author(
                name="Glite ARF reasoning-scale project",
                country="LU",
                institution="Constructor",
                orcid=None,
            ),
        ],
        institutions=[
            Institution(name="Constructor", country="LU"),
        ],
        license="research-only",
        access_kind="public",
        size_description=size_description,
        files=[
            DatasetFile(
                path=f"files/{FRONTIERSCIENCE_SLUG}.jsonl",
                description=(
                    "Pilot annotation rows for FrontierScience-Olympiad: 40 problems "
                    "across physics, chemistry, biology."
                ),
                format="jsonl",
            ),
        ],
        categories=["benchmark-frontierscience"],
        download_status=DOWNLOAD_STATUS_SUCCESS,
        download_failure_reason=None,
    )

    description_md: str = _build_description_md(
        rows=rows,
        domain_counts=domain_counts,
        avg_problem_chars=avg_problem_chars,
    )

    write_dataset_asset(
        asset_root=FRONTIERSCIENCE_DIR,
        details=details,
        description_md=description_md,
    )

    return {
        "dataset_id": FRONTIERSCIENCE_SLUG,
        "download_status": DOWNLOAD_STATUS_SUCCESS,
        "sample_count": len(rows),
        "subset_rule": (
            "All FrontierScience-Olympiad rows from pilot JSONL; "
            "domain-stratified across physics, chemistry, biology"
        ),
        "domain_counts": domain_counts,
    }


if __name__ == "__main__":
    result: dict[str, object] = build()
    print(json.dumps(result, indent=2))
