"""Build the tau-bench subset asset by downloading task definitions from GitHub.

The tau-bench source repository (sierra-research/tau-bench) ships task definitions as
plain Python files containing `TASKS = [Task(...), ...]` lists. We can download those
files directly without installing the package or providing API keys, parse the action
sequence length per task, and filter to tasks whose action count is in [4, 8]. If the
download fails, we keep the HumanEval pilot proxy and document the access attempt.
"""

from __future__ import annotations

import ast
import json
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from tasks.t0003_download_benchmark_subsets.code.constants import (
    DATE_SUMMARIZED,
    DOWNLOAD_STATUS_FAILED,
    DOWNLOAD_STATUS_SUCCESS,
    MAX_DECISIONS,
    MIN_DECISIONS,
    TASK_ID,
    TAUBENCH_SLUG,
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
from tasks.t0003_download_benchmark_subsets.code.paths import TAUBENCH_DIR

TAUBENCH_REPO: str = "sierra-research/tau-bench"
TAUBENCH_RAW_BASE: str = "https://raw.githubusercontent.com/sierra-research/tau-bench/main"
DOMAINS: list[tuple[str, str, str]] = [
    ("airline", "test", f"{TAUBENCH_RAW_BASE}/tau_bench/envs/airline/tasks_test.py"),
    ("retail", "test", f"{TAUBENCH_RAW_BASE}/tau_bench/envs/retail/tasks_test.py"),
    ("retail", "train", f"{TAUBENCH_RAW_BASE}/tau_bench/envs/retail/tasks_train.py"),
]


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


def _parse_action_counts(*, source_path: Path) -> list[int]:
    """Parse a tau-bench tasks Python file and return action counts per task.

    The file is expected to contain `TASKS = [Task(annotator=..., user_id=...,
    instruction=..., actions=[Action(...), Action(...)], outputs=[...]), ...]`. We use
    the AST module to count the number of elements in each task's `actions` keyword arg.
    """
    src: str = source_path.read_text(encoding="utf-8")
    tree: ast.Module = ast.parse(src, filename=str(source_path))
    counts: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        targets = node.targets
        if len(targets) != 1:
            continue
        tgt = targets[0]
        if not isinstance(tgt, ast.Name) or not tgt.id.startswith("TASKS"):
            continue
        value = node.value
        if not isinstance(value, ast.List):
            continue
        for task_call in value.elts:
            if not isinstance(task_call, ast.Call):
                continue
            for kw in task_call.keywords:
                if kw.arg != "actions":
                    continue
                if isinstance(kw.value, ast.List):
                    counts.append(len(kw.value.elts))
                else:
                    counts.append(0)
    return counts


def _extract_task_records(
    *,
    source_path: Path,
    domain: str,
    split: str,
) -> list[dict[str, object]]:
    """Extract task instances as plain dicts: instruction, action count, action names."""
    src: str = source_path.read_text(encoding="utf-8")
    tree: ast.Module = ast.parse(src, filename=str(source_path))
    records: list[dict[str, object]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        targets = node.targets
        if len(targets) != 1:
            continue
        tgt = targets[0]
        if not isinstance(tgt, ast.Name) or not tgt.id.startswith("TASKS"):
            continue
        value = node.value
        if not isinstance(value, ast.List):
            continue
        for idx, task_call in enumerate(value.elts):
            if not isinstance(task_call, ast.Call):
                continue
            rec: dict[str, object] = {
                "domain": domain,
                "split": split,
                "task_index": idx,
            }
            for kw in task_call.keywords:
                if kw.arg in ("annotator", "user_id"):
                    if isinstance(kw.value, ast.Constant):
                        rec[str(kw.arg)] = kw.value.value
                elif kw.arg == "instruction" and isinstance(kw.value, ast.Constant):
                    rec["instruction"] = kw.value.value
                elif kw.arg == "actions" and isinstance(kw.value, ast.List):
                    action_names: list[str] = []
                    for action_call in kw.value.elts:
                        if not isinstance(action_call, ast.Call):
                            continue
                        for ak in action_call.keywords:
                            if ak.arg == "name" and isinstance(ak.value, ast.Constant):
                                action_names.append(str(ak.value.value))
                    rec["actions"] = action_names
                    rec["action_count"] = len(action_names)
                elif kw.arg == "outputs" and isinstance(kw.value, ast.List):
                    outputs: list[object] = []
                    for elt in kw.value.elts:
                        if isinstance(elt, ast.Constant):
                            outputs.append(elt.value)
                    rec["outputs"] = outputs
            records.append(rec)
    return records


def _build_description_md(
    *,
    total_records: int,
    subset_count: int,
    domain_split_counts: dict[str, int],
    action_distribution: dict[int, int],
) -> str:
    metadata: str = (
        "## Metadata\n\n"
        "* **Name**: tau-bench subset (4-8 actions)\n"
        "* **Year**: 2024\n"
        "* **Authors**: Shunyu Yao et al. (Sierra Research)\n"
        "* **License**: MIT (parent tau-bench repository license)\n"
        "* **Access**: public (GitHub `sierra-research/tau-bench`)\n"
        f"* **Size**: {subset_count} tasks (filtered from {total_records} total)\n"
    )

    overview: str = (
        "## Overview\n\n"
        "tau-bench (Yao et al. 2024, arXiv:2406.12045) is a tool-agent-user interaction "
        "benchmark spanning two domains: airline customer service and retail returns/exchanges. "
        "Each task gives the agent a user intent and a domain API; the agent must produce a "
        "sequence of API calls (`Action` objects) that satisfies the user. The original "
        "benchmark ships task definitions as Python source files in the upstream repository — "
        "this dataset asset extracts those task definitions without installing the harness or "
        "calling any LLM, so the subset is a pure metadata export. Each subset row records the "
        "domain, split (test or train), instruction text, gold action sequence (names only), "
        "and action count. We filter to tasks whose gold sequence has 4 to 8 actions (the "
        "project's canonical multi-step decision range).\n"
    )

    content: str = (
        "## Content & Annotation\n\n"
        "Each row has these fields: `domain` (`airline` or `retail`), `split` (`test` or "
        "`train`), `task_index` (position in the upstream `TASKS` list), `annotator` (the "
        "upstream annotator id, where present), `user_id` (the synthetic user id), "
        "`instruction` (the user's natural-language request), `actions` (list of API call names "
        "in the gold sequence), `action_count` (length of `actions`), and `outputs` (list of "
        "expected agent outputs, where annotated). The gold action sequence is what the "
        "upstream project uses to grade an agent's pass/fail at the task level.\n"
    )

    domain_split_lines: str = "\n".join(
        f"| {ds} | {c} |" for ds, c in sorted(domain_split_counts.items())
    )
    action_lines: str = "\n".join(
        f"| {a} | {action_distribution.get(a, 0)} |"
        for a in range(MIN_DECISIONS, MAX_DECISIONS + 1)
    )
    statistics: str = (
        "## Statistics\n\n"
        "| Metric | Value |\n"
        "|--------|-------|\n"
        f"| Total tasks across upstream Python files | {total_records} |\n"
        f"| Subset (4-8 actions) | {subset_count} |\n"
        "\n"
        "### Per-domain-split breakdown of subset\n\n"
        "| Domain / split | Tasks |\n"
        "|----------------|-------|\n"
        f"{domain_split_lines}\n"
        "\n"
        "### Action-count distribution within subset\n\n"
        "| Actions | Tasks |\n"
        "|---------|-------|\n"
        f"{action_lines}\n"
        "\n"
        "### Subset rule\n\n"
        f"Tasks are kept iff the gold `actions` list has between {MIN_DECISIONS} and "
        f"{MAX_DECISIONS} entries (inclusive). Action counts are extracted from the upstream "
        "Python source files via the `ast` module — no installation required.\n"
    )

    usage: str = (
        "## Usage Notes\n\n"
        "Load with the Python standard library:\n\n"
        "```python\n"
        "import json\n"
        f"with open('files/{TAUBENCH_SLUG}.jsonl') as fh:\n"
        "    rows = [json.loads(line) for line in fh if line.strip()]\n"
        "```\n\n"
        "The full upstream Python source for each (domain, split) pair is preserved verbatim in "
        "`files/upstream/<domain>__tasks_<split>.py` so downstream tasks can re-extract richer "
        "fields (action kwargs, output shapes) without re-fetching from GitHub. Note that "
        "running tau-bench end-to-end (instantiating the env and querying an LLM) still "
        "requires installing the harness and providing API keys — this asset only captures the "
        "task metadata needed for the project's scope-aware vs scope-unaware comparison.\n"
    )

    main_ideas: str = (
        "## Main Ideas\n\n"
        "* The action sequence length is the natural per-task decision count for tau-bench: "
        "  each `Action(...)` call is one tool invocation the agent must produce.\n"
        "* By extracting metadata from upstream source rather than installing the harness, this "
        "  asset is fully reproducible, requires no API keys, and stays under 1 MB.\n"
        "* The subset combines all available splits (test + train where present) so Phase 2 can "
        "  use train tasks for prompt tuning and test tasks for unbiased evaluation if needed.\n"
        "* Action kwargs (e.g., flight numbers, user IDs) are intentionally omitted from the "
        "  subset rows to keep them small; the full upstream Python is preserved separately for "
        "  agents that need the kwargs.\n"
    )

    summary: str = (
        "## Summary\n\n"
        f"This tau-bench subset contains {subset_count} tasks from the upstream Sierra Research "
        "tau-bench repository, filtered to the 4-8 actions per task range. Tasks span the "
        "airline customer-service and retail return/exchange domains. Metadata is extracted "
        "from upstream Python source files using the `ast` module, so this asset works fully "
        "offline once the source files are downloaded.\n\n"
        "For this project, the subset is the primary tool-use multi-step test bed for the "
        "scope-aware vs. scope-unaware Phase 2 comparison. The upstream MIT license and stable "
        "task indices preserve interoperability with the public tau-bench leaderboard.\n"
    )

    return (
        f'---\nspec_version: "2"\ndataset_id: "{TAUBENCH_SLUG}"\n'
        f'summarized_by_task: "{TASK_ID}"\ndate_summarized: "{DATE_SUMMARIZED}"\n---\n\n'
        f"# tau-bench Subset (4-8 actions)\n\n"
        f"{metadata}\n{overview}\n{content}\n{statistics}\n{usage}\n{main_ideas}\n{summary}"
    )


def build() -> dict[str, object]:
    upstream_dir: Path = TAUBENCH_DIR / "files" / "upstream"
    upstream_dir.mkdir(parents=True, exist_ok=True)

    downloaded_paths: list[Path] = []
    failures: list[str] = []
    for domain, split, url in DOMAINS:
        local: Path = upstream_dir / f"{domain}__tasks_{split}.py"
        ok, reason = _download_text(url=url, target=local)
        if ok:
            downloaded_paths.append(local)
        else:
            failures.append(reason)

    if len(downloaded_paths) == 0:
        joined_reasons: str = "; ".join(failures) if failures else "no files downloaded"
        write_access_attempt(
            asset_root=TAUBENCH_DIR,
            benchmark_name="tau-bench",
            source_url=TAUBENCH_RAW_BASE,
            attempted_at="2026-04-29T14:43:00Z",
            reason=joined_reasons,
            fallback_proxy=(
                "HumanEval (already used by the pilot run; row label "
                '`benchmark="tau-bench"` in `tasks_annotated.jsonl` is treated as a '
                "HumanEval proxy in pilot data)."
            ),
            extra_log=joined_reasons,
        )
        details: DatasetDetails = DatasetDetails(
            spec_version="2",
            dataset_id=TAUBENCH_SLUG,
            name="tau-bench subset (download failed)",
            version=None,
            short_description=(
                "tau-bench subset placeholder — upstream Python sources could not be "
                "downloaded; pilot HumanEval proxy is preserved as the de-facto Phase 2 "
                "fallback."
            ),
            description_path="description.md",
            source_paper_id="10.48550_arXiv.2406.12045",
            url="https://arxiv.org/abs/2406.12045",
            download_url=TAUBENCH_RAW_BASE,
            year=2024,
            date_published="2024-06-17",
            authors=[Author(name="Shunyu Yao")],
            institutions=[Institution(name="Sierra Research", country="US")],
            license="MIT",
            access_kind="public",
            size_description=f"0 tasks (download failed: {joined_reasons})",
            files=[
                DatasetFile(
                    path="files/access-attempt.md",
                    description="Access attempt log (download failed).",
                    format="md",
                ),
            ],
            categories=["benchmark-taubench"],
            download_status=DOWNLOAD_STATUS_FAILED,
            download_failure_reason=joined_reasons,
        )
        write_dataset_asset(
            asset_root=TAUBENCH_DIR,
            details=details,
            description_md=(
                f'---\nspec_version: "2"\ndataset_id: "{TAUBENCH_SLUG}"\n'
                f'summarized_by_task: "{TASK_ID}"\ndate_summarized: "{DATE_SUMMARIZED}"\n---\n\n'
                f"# tau-bench Subset (download failed)\n\n"
                "## Metadata\n\n"
                "* **Name**: tau-bench subset (download failed)\n"
                "* **Year**: 2024\n"
                "* **Authors**: Shunyu Yao et al.\n"
                "* **License**: MIT\n"
                "* **Access**: public (upstream unreachable at attempt time)\n"
                "* **Size**: 0 tasks (download failed)\n\n"
                "## Overview\n\n"
                "Upstream tau-bench task definitions could not be fetched from "
                f"`{TAUBENCH_RAW_BASE}`. The access attempt is logged in "
                "`files/access-attempt.md`. The pilot HumanEval proxy remains the "
                "de-facto Phase 2 fallback for tool-use experiments.\n\n"
                "## Content & Annotation\n\nNo content downloaded.\n\n"
                "## Statistics\n\n"
                "| Metric | Value |\n|--------|-------|\n| Tasks | 0 |\n\n"
                "## Usage Notes\n\nNot loadable until upstream is reachable.\n\n"
                "## Main Ideas\n\n"
                "* HumanEval pilot proxy is the operative Phase 2 fallback.\n"
                "* A retry task can re-download once GitHub raw URLs are reachable.\n"
                "* No license barrier; this is a transient network failure.\n\n"
                "## Summary\n\n"
                "The tau-bench Python source files at the upstream raw URL could not be "
                "downloaded. The asset folder preserves metadata so a follow-up retry "
                "task can complete the import without re-discovering URLs.\n"
            ),
        )
        return {
            "dataset_id": TAUBENCH_SLUG,
            "download_status": DOWNLOAD_STATUS_FAILED,
            "sample_count": 0,
            "subset_rule": "n/a (download failed)",
            "failure_reason": joined_reasons,
        }

    # Extract records and filter
    all_records: list[dict[str, object]] = []
    for domain, split, _url in DOMAINS:
        local = upstream_dir / f"{domain}__tasks_{split}.py"
        if not local.exists():
            continue
        records: list[dict[str, object]] = _extract_task_records(
            source_path=local,
            domain=domain,
            split=split,
        )
        all_records.extend(records)

    total_records: int = len(all_records)
    subset: list[dict[str, object]] = [
        r
        for r in all_records
        if MIN_DECISIONS <= int(r.get("action_count", 0)) <= MAX_DECISIONS  # type: ignore[arg-type]
    ]
    subset_count: int = len(subset)

    subset_jsonl: Path = TAUBENCH_DIR / "files" / f"{TAUBENCH_SLUG}.jsonl"
    with subset_jsonl.open("w", encoding="utf-8") as fh:
        for rec in subset:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    domain_split_counts: dict[str, int] = dict(
        Counter(f"{r.get('domain')}/{r.get('split')}" for r in subset)
    )
    action_distribution: dict[int, int] = dict(
        sorted(Counter(int(r.get("action_count", 0)) for r in subset).items())  # type: ignore[arg-type]
    )

    short_description: str = (
        f"tau-bench subset: {subset_count} tool-agent-user interaction tasks across airline "
        "and retail domains, filtered to 4-8 gold actions per task."
    )
    size_description: str = (
        f"{subset_count} tasks filtered from {total_records} upstream tau-bench tasks "
        f"(kept iff gold action sequence has between {MIN_DECISIONS} and "
        f"{MAX_DECISIONS} actions)"
    )

    files_meta: list[DatasetFile] = [
        DatasetFile(
            path=f"files/{TAUBENCH_SLUG}.jsonl",
            description=(
                f"Filtered subset: {subset_count} tau-bench tasks (4-8 actions). "
                "Each row has domain, split, instruction, action names, and action count."
            ),
            format="jsonl",
        ),
    ]
    for path in downloaded_paths:
        rel: str = "files/upstream/" + path.name
        files_meta.append(
            DatasetFile(
                path=rel,
                description=(
                    f"Verbatim upstream tau-bench task definitions for "
                    f"{path.name.replace('__', '/').replace('.py', '')}."
                ),
                format="py",
            )
        )

    details = DatasetDetails(
        spec_version="2",
        dataset_id=TAUBENCH_SLUG,
        name="tau-bench subset (4-8 actions)",
        version="github-main",
        short_description=short_description,
        description_path="description.md",
        source_paper_id="10.48550_arXiv.2406.12045",
        url="https://arxiv.org/abs/2406.12045",
        download_url=TAUBENCH_RAW_BASE,
        year=2024,
        date_published="2024-06-17",
        authors=[
            Author(
                name="Shunyu Yao",
                country="US",
                institution="Sierra Research",
                orcid=None,
            ),
        ],
        institutions=[
            Institution(name="Sierra Research", country="US"),
        ],
        license="MIT",
        access_kind="public",
        size_description=size_description,
        files=files_meta,
        categories=["benchmark-taubench"],
        download_status=DOWNLOAD_STATUS_SUCCESS,
        download_failure_reason=None,
    )

    description_md: str = _build_description_md(
        total_records=total_records,
        subset_count=subset_count,
        domain_split_counts=domain_split_counts,
        action_distribution=action_distribution,
    )
    write_dataset_asset(
        asset_root=TAUBENCH_DIR,
        details=details,
        description_md=description_md,
    )

    return {
        "dataset_id": TAUBENCH_SLUG,
        "download_status": DOWNLOAD_STATUS_SUCCESS,
        "sample_count": subset_count,
        "total_upstream_tasks": total_records,
        "subset_rule": (
            f"keep iff gold action sequence has between {MIN_DECISIONS} and {MAX_DECISIONS} actions"
        ),
        "domain_split_counts": domain_split_counts,
        "action_distribution": action_distribution,
    }


if __name__ == "__main__":
    result: dict[str, object] = build()
    print(json.dumps(result, indent=2))
