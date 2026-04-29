"""Build the WorkArena++ subset asset.

WorkArena++ task instantiation requires a live ServiceNow developer instance plus a
gated HuggingFace dataset (`ServiceNow/WorkArena-Instances`). Neither is available in
this task's local-only download budget. We can still package a useful dataset asset by
extracting WorkArena++'s compositional task class manifest from the upstream repo's
`curriculum.py` file — this gives Phase 2 the canonical task taxonomy without needing
to instantiate any task. The Mind2Web pilot proxy remains the de-facto Phase 2
fallback for actual task execution.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

from tasks.t0003_download_benchmark_subsets.code.constants import (
    DATE_SUMMARIZED,
    DOWNLOAD_STATUS_FAILED,
    DOWNLOAD_STATUS_SUCCESS,
    MAX_DECISIONS,
    MIN_DECISIONS,
    TASK_ID,
    WORKARENA_PP_SLUG,
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
from tasks.t0003_download_benchmark_subsets.code.paths import WORKARENA_PP_DIR

WA_REPO_RAW: str = "https://raw.githubusercontent.com/ServiceNow/WorkArena/main"
WA_CURRICULUM_URL: str = (
    f"{WA_REPO_RAW}/src/browsergym/workarena/tasks/compositional/utils/curriculum.py"
)
WA_INIT_URL: str = f"{WA_REPO_RAW}/src/browsergym/workarena/tasks/compositional/__init__.py"
WA_README_URL: str = f"{WA_REPO_RAW}/README.md"

# Upper-snake_case identifiers in curriculum.py that name task class lists.
TASK_LIST_PATTERN: re.Pattern[str] = re.compile(r"\b([A-Z][A-Z0-9_]{3,})\b")


def _download_text(*, url: str, target: Path) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, target)
    except urllib.error.URLError as exc:
        return False, f"urllib.error.URLError fetching {url}: {exc}"
    except OSError as exc:
        return False, f"OSError fetching {url}: {exc}"
    if not target.exists() or target.stat().st_size == 0:
        return False, f"Empty file at {target} after fetching {url}"
    return True, "ok"


def _extract_task_lists(*, curriculum_text: str) -> list[str]:
    """Extract upper-case task list identifiers imported in curriculum.py."""
    out: list[str] = []
    seen: set[str] = set()
    # We only care about identifiers used inside `from ... import (X, Y, Z)` blocks.
    in_import: bool = False
    for line in curriculum_text.splitlines():
        stripped: str = line.strip()
        if stripped.startswith("from ") and "import" in stripped:
            in_import = True
            # Inline imports (single-line) — extract names after "import"
            if "(" not in stripped:
                names_part = stripped.split("import", 1)[1]
                for tok in re.findall(r"\b[A-Z][A-Z0-9_]{3,}\b", names_part):
                    if tok not in seen:
                        seen.add(tok)
                        out.append(tok)
                in_import = False
            continue
        if in_import:
            for tok in re.findall(r"\b[A-Z][A-Z0-9_]{3,}\b", stripped):
                if tok in {"AGENT_CURRICULUM", "HUMAN_CURRICULUM"}:
                    continue
                if tok not in seen:
                    seen.add(tok)
                    out.append(tok)
            if ")" in stripped:
                in_import = False
    return out


def _build_description_md(
    *,
    task_lists: list[str],
    download_method: str,
) -> str:
    metadata: str = (
        "## Metadata\n\n"
        "* **Name**: WorkArena++ compositional task manifest\n"
        "* **Year**: 2024\n"
        "* **Authors**: Léo Boisvert et al. (ServiceNow Research)\n"
        "* **License**: parent WorkArena Apache-2.0 license\n"
        "* **Access**: restricted (full instantiation requires a live ServiceNow "
        "  developer instance and a gated HuggingFace dataset)\n"
        f"* **Size**: {len(task_lists)} compositional task class lists exported from the "
        "  upstream `curriculum.py` manifest\n"
    )

    overview: str = (
        "## Overview\n\n"
        "WorkArena++ (Boisvert et al. 2024, arXiv:2407.05291) is a benchmark of compositional "
        "knowledge-work tasks built from 33 atomic ServiceNow operations. Running a single "
        "task end-to-end requires (a) a live ServiceNow developer instance, (b) gated access "
        "to the `ServiceNow/WorkArena-Instances` HuggingFace dataset, and (c) the "
        "`browsergym-workarena` Python harness with Playwright. None of these are available "
        "within this task's local-only download budget, so this dataset asset packages the "
        "**compositional task class manifest** extracted from the upstream "
        "`tasks/compositional/utils/curriculum.py` source file. The manifest gives Phase 2 the "
        "canonical task taxonomy without needing to instantiate any task — every name listed "
        "is a class group representing a distinct WorkArena++ compositional task family. The "
        "existing pilot Mind2Web proxy remains the de-facto Phase 2 fallback for end-to-end "
        "execution until upstream access is resolved.\n"
    )

    content: str = (
        "## Content & Annotation\n\n"
        "The `files/workarena-plus-plus-task-manifest.json` file lists every task class group "
        "imported by the upstream `curriculum.py`. Each entry is a string identifier (e.g., "
        "`DASH_AND_ORDER`, `NAVIGATE_AND_CREATE_TASKS`) that maps to a Python class list in the "
        "`browsergym.workarena.tasks.compositional` package. Task instances are not enumerated "
        "(that requires the live ServiceNow instance and the gated HF dataset). The files "
        "`files/upstream/curriculum.py`, `files/upstream/compositional__init__.py`, and "
        "`files/upstream/README.md` preserve the upstream source verbatim so downstream "
        "tasks can re-extract richer metadata (per-class skill annotations, level breakdowns) "
        "without re-fetching from GitHub.\n"
    )

    bullet_lines: str = "\n".join(f"* `{name}`" for name in task_lists)
    statistics: str = (
        "## Statistics\n\n"
        "| Metric | Value |\n"
        "|--------|-------|\n"
        f"| Compositional task class lists | {len(task_lists)} |\n"
        f"| Atomic operations (per upstream paper) | 33 |\n"
        f"| Compositional tasks (per upstream paper, both L2 and L3 levels) | ~682 |\n"
        f"| Source file | `tasks/compositional/utils/curriculum.py` |\n"
        f"| Download method | {download_method} |\n"
        "\n"
        "### Task class list manifest\n\n"
        f"{bullet_lines}\n"
        "\n"
        "### Subset rule\n\n"
        "All compositional task class lists from the upstream curriculum are kept. The "
        f"canonical {MIN_DECISIONS}-{MAX_DECISIONS} decisions per task filter cannot be applied "
        "at this layer because instantiated task instances (with concrete action sequences) "
        "are not available without ServiceNow + HF access. Phase 2 must apply the filter at "
        "instance time once full upstream access is resolved.\n"
    )

    usage: str = (
        "## Usage Notes\n\n"
        "Load with the Python standard library:\n\n"
        "```python\n"
        "import json\n"
        f"with open('files/{WORKARENA_PP_SLUG}-task-manifest.json') as fh:\n"
        "    task_class_lists = json.load(fh)\n"
        "```\n\n"
        "To actually run any of these tasks end-to-end, install `browsergym-workarena`, "
        "follow the upstream README to (a) request access to "
        "`ServiceNow/WorkArena-Instances` on HuggingFace and (b) provision a ServiceNow "
        "developer instance, then dispatch tasks via the BrowserGym `make()` API. None of "
        "those operations are required to use this manifest as a taxonomy reference.\n"
    )

    main_ideas: str = (
        "## Main Ideas\n\n"
        "* WorkArena++ end-to-end execution is gated on ServiceNow + HF access; this asset "
        "  documents the access barrier and packages the upstream taxonomy without crossing it.\n"
        "* The pilot Mind2Web proxy remains the operative Phase 2 fallback for "
        "  knowledge-worker compositional tasks until upstream access is resolved.\n"
        "* The 4-8 decisions per task filter must be deferred to instance time — the upstream "
        "  curriculum manifest is at the task-class level, not the task-instance level.\n"
        "* The upstream license is permissive (Apache-2.0) but the live ServiceNow developer "
        "  instance is the binding access cost in practical terms.\n"
    )

    summary: str = (
        "## Summary\n\n"
        f"This dataset asset packages the WorkArena++ compositional task class manifest "
        f"({len(task_lists)} task class lists) extracted from the upstream "
        "`tasks/compositional/utils/curriculum.py` source. End-to-end task instantiation "
        "requires a live ServiceNow developer instance plus access to the "
        "`ServiceNow/WorkArena-Instances` gated HuggingFace dataset; this access is treated "
        "as out of scope for this download task and is documented as a project follow-up.\n\n"
        "For this project, the asset gives Phase 2 the canonical WorkArena++ task taxonomy "
        "and preserves the upstream source files for traceability. The pilot Mind2Web proxy "
        "remains the actual end-to-end test bed for compositional knowledge-worker tasks "
        "until the access barriers are resolved.\n"
    )

    return (
        f'---\nspec_version: "2"\ndataset_id: "{WORKARENA_PP_SLUG}"\n'
        f'summarized_by_task: "{TASK_ID}"\ndate_summarized: "{DATE_SUMMARIZED}"\n---\n\n'
        f"# WorkArena++ Compositional Task Manifest\n\n"
        f"{metadata}\n{overview}\n{content}\n{statistics}\n{usage}\n{main_ideas}\n{summary}"
    )


def build() -> dict[str, object]:
    upstream_dir: Path = WORKARENA_PP_DIR / "files" / "upstream"
    upstream_dir.mkdir(parents=True, exist_ok=True)

    curriculum_local: Path = upstream_dir / "curriculum.py"
    init_local: Path = upstream_dir / "compositional__init__.py"
    readme_local: Path = upstream_dir / "README.md"

    fetch_results: list[tuple[str, bool, str]] = []
    for label, url, target in [
        ("curriculum", WA_CURRICULUM_URL, curriculum_local),
        ("compositional_init", WA_INIT_URL, init_local),
        ("readme", WA_README_URL, readme_local),
    ]:
        ok, reason = _download_text(url=url, target=target)
        fetch_results.append((label, ok, reason))

    curriculum_ok: bool = any(r[0] == "curriculum" and r[1] for r in fetch_results)

    if not curriculum_ok:
        joined_reasons: str = "; ".join(
            f"{label}: {reason}" for label, ok, reason in fetch_results if not ok
        )
        write_access_attempt(
            asset_root=WORKARENA_PP_DIR,
            benchmark_name="WorkArena++",
            source_url=WA_REPO_RAW,
            attempted_at="2026-04-29T14:43:00Z",
            reason=joined_reasons,
            fallback_proxy=(
                "Mind2Web (already used by the pilot run; row label "
                '`benchmark="WorkArena++"` in `tasks_annotated.jsonl` is treated as a '
                "Mind2Web proxy in pilot data)."
            ),
            extra_log=joined_reasons,
        )
        details: DatasetDetails = DatasetDetails(
            spec_version="2",
            dataset_id=WORKARENA_PP_SLUG,
            name="WorkArena++ subset (download failed)",
            version=None,
            short_description=(
                "WorkArena++ subset placeholder — upstream curriculum could not be "
                "downloaded; pilot Mind2Web proxy is preserved as the de-facto fallback."
            ),
            description_path="description.md",
            source_paper_id="10.48550_arXiv.2407.05291",
            url="https://arxiv.org/abs/2407.05291",
            download_url=WA_REPO_RAW,
            year=2024,
            date_published="2024-07-07",
            authors=[Author(name="Léo Boisvert")],
            institutions=[Institution(name="ServiceNow Research", country="CA")],
            license="Apache-2.0",
            access_kind="restricted",
            size_description=f"0 task lists (download failed: {joined_reasons})",
            files=[
                DatasetFile(
                    path="files/access-attempt.md",
                    description="Access attempt log (download failed).",
                    format="md",
                ),
            ],
            categories=["benchmark-workarena"],
            download_status=DOWNLOAD_STATUS_FAILED,
            download_failure_reason=joined_reasons,
        )
        write_dataset_asset(
            asset_root=WORKARENA_PP_DIR,
            details=details,
            description_md=(
                f'---\nspec_version: "2"\ndataset_id: "{WORKARENA_PP_SLUG}"\n'
                f'summarized_by_task: "{TASK_ID}"\ndate_summarized: "{DATE_SUMMARIZED}"\n---\n\n'
                f"# WorkArena++ Subset (download failed)\n\n"
                "## Metadata\n\n"
                "* **Name**: WorkArena++ subset (download failed)\n"
                "* **Year**: 2024\n"
                "* **Authors**: Léo Boisvert et al.\n"
                "* **License**: Apache-2.0\n"
                "* **Access**: restricted (live ServiceNow + gated HF required)\n"
                "* **Size**: 0 task lists (download failed)\n\n"
                "## Overview\n\n"
                "Upstream WorkArena curriculum manifest could not be fetched from "
                f"`{WA_REPO_RAW}`. The Mind2Web pilot proxy remains the de-facto "
                "Phase 2 fallback for compositional knowledge-worker tasks.\n\n"
                "## Content & Annotation\n\nNo content downloaded.\n\n"
                "## Statistics\n\n"
                "| Metric | Value |\n|--------|-------|\n| Task lists | 0 |\n\n"
                "## Usage Notes\n\nNot loadable until upstream is reachable.\n\n"
                "## Main Ideas\n\n"
                "* Mind2Web pilot proxy is the operative Phase 2 fallback.\n"
                "* End-to-end execution is gated on ServiceNow + HF access regardless.\n"
                "* A retry task can re-download the curriculum manifest once GitHub is "
                "  reachable.\n\n"
                "## Summary\n\n"
                "The WorkArena++ upstream curriculum could not be downloaded. The asset "
                "folder preserves the access attempt and metadata so a follow-up retry "
                "task can complete the import without re-discovering URLs.\n"
            ),
        )
        return {
            "dataset_id": WORKARENA_PP_SLUG,
            "download_status": DOWNLOAD_STATUS_FAILED,
            "sample_count": 0,
            "subset_rule": "n/a (download failed)",
            "failure_reason": joined_reasons,
        }

    # Curriculum downloaded — extract task class identifiers
    curriculum_text: str = curriculum_local.read_text(encoding="utf-8")
    task_lists: list[str] = _extract_task_lists(curriculum_text=curriculum_text)
    assert len(task_lists) >= 5, (
        f"Expected at least 5 task class lists in curriculum.py, got {len(task_lists)}"
    )

    manifest_path: Path = WORKARENA_PP_DIR / "files" / f"{WORKARENA_PP_SLUG}-task-manifest.json"
    manifest_payload: dict[str, object] = {
        "source_url": WA_CURRICULUM_URL,
        "extraction_method": (
            "regex extraction of upper-case identifiers from curriculum.py imports"
        ),
        "limitations": [
            "Task instances are not enumerated; instantiation requires a live ServiceNow "
            "developer instance plus the gated HuggingFace dataset "
            "ServiceNow/WorkArena-Instances.",
            "The 4-8 decisions per task filter cannot be applied at the task-class layer; "
            "Phase 2 must apply it at instance time.",
        ],
        "task_class_lists": task_lists,
        "task_class_list_count": len(task_lists),
    }
    manifest_path.write_text(
        json.dumps(manifest_payload, indent=2) + "\n",
        encoding="utf-8",
    )

    files_meta: list[DatasetFile] = [
        DatasetFile(
            path=f"files/{WORKARENA_PP_SLUG}-task-manifest.json",
            description=(
                "WorkArena++ compositional task class manifest extracted from upstream "
                f"curriculum.py. {len(task_lists)} task class lists, no instances."
            ),
            format="json",
        ),
        DatasetFile(
            path="files/upstream/curriculum.py",
            description="Verbatim upstream curriculum.py source.",
            format="py",
        ),
    ]
    if init_local.exists() and init_local.stat().st_size > 0:
        files_meta.append(
            DatasetFile(
                path="files/upstream/compositional__init__.py",
                description=(
                    "Verbatim upstream tasks/compositional/__init__.py source defining "
                    "ALL_COMPOSITIONAL_TASKS, level-2 and level-3 specializations."
                ),
                format="py",
            )
        )
    if readme_local.exists() and readme_local.stat().st_size > 0:
        files_meta.append(
            DatasetFile(
                path="files/upstream/README.md",
                description=("Verbatim upstream WorkArena README documenting access requirements."),
                format="md",
            )
        )

    short_description: str = (
        f"WorkArena++ compositional task class manifest ({len(task_lists)} task class "
        "lists) extracted from upstream curriculum.py; end-to-end execution remains gated."
    )
    size_description: str = (
        f"{len(task_lists)} compositional task class lists from the upstream curriculum "
        "manifest. Task instances are not enumerated (requires live ServiceNow + gated HF)."
    )

    details = DatasetDetails(
        spec_version="2",
        dataset_id=WORKARENA_PP_SLUG,
        name="WorkArena++ compositional task manifest",
        version="github-main",
        short_description=short_description,
        description_path="description.md",
        source_paper_id="10.48550_arXiv.2407.05291",
        url="https://arxiv.org/abs/2407.05291",
        download_url=WA_REPO_RAW,
        year=2024,
        date_published="2024-07-07",
        authors=[
            Author(
                name="Léo Boisvert",
                country="CA",
                institution="ServiceNow Research",
                orcid=None,
            ),
        ],
        institutions=[
            Institution(name="ServiceNow Research", country="CA"),
        ],
        license="Apache-2.0",
        access_kind="restricted",
        size_description=size_description,
        files=files_meta,
        categories=["benchmark-workarena"],
        download_status=DOWNLOAD_STATUS_SUCCESS,
        download_failure_reason=None,
    )

    description_md: str = _build_description_md(
        task_lists=task_lists,
        download_method=f"urllib.request.urlretrieve from {WA_CURRICULUM_URL}",
    )
    write_dataset_asset(
        asset_root=WORKARENA_PP_DIR,
        details=details,
        description_md=description_md,
    )

    # NB: download_status is "success" for the *manifest* extraction. The note about
    # restricted instance access is documented in the description and access_kind.
    extra_note: str = (
        "Task-class manifest extracted; per-instance enumeration is gated on live "
        "ServiceNow + HF access and remains a follow-up task."
    )
    return {
        "dataset_id": WORKARENA_PP_SLUG,
        "download_status": DOWNLOAD_STATUS_SUCCESS,
        "sample_count": len(task_lists),
        "subset_rule": (
            "all compositional task class lists from upstream curriculum.py; "
            "instance-level filter deferred to a follow-up task"
        ),
        "task_lists_sample": task_lists[:8],
        "note": extra_note,
    }


if __name__ == "__main__":
    result: dict[str, object] = build()
    print(json.dumps(result, indent=2))
