"""Helper for documenting failed download attempts inside a dataset asset."""

from __future__ import annotations

from pathlib import Path


def write_access_attempt(
    *,
    asset_root: Path,
    benchmark_name: str,
    source_url: str,
    attempted_at: str,
    reason: str,
    fallback_proxy: str,
    extra_log: str = "",
) -> Path:
    """Write ``files/access-attempt.md`` documenting a failed download.

    Returns the path to the written file. The file satisfies dataset asset spec rule
    DA-E003 (``files/`` must contain at least one file) without faking a real download.
    """
    files_dir: Path = asset_root / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    target: Path = files_dir / "access-attempt.md"
    body: str = (
        f"# Access Attempt: {benchmark_name}\n\n"
        f"* **Source URL**: {source_url}\n"
        f"* **Attempted at (UTC)**: {attempted_at}\n"
        f"* **Status**: failed\n\n"
        "## Failure reason\n\n"
        f"{reason}\n\n"
        "## Fallback decision\n\n"
        f"This task freezes the existing pilot proxy: **{fallback_proxy}**.\n"
        "Phase 2 of the project will use the proxy unless a follow-up task resolves "
        "the access barrier.\n"
    )
    if extra_log != "":
        body += "\n## Attempt log\n\n```text\n" + extra_log.rstrip() + "\n```\n"
    target.write_text(body, encoding="utf-8")
    return target
