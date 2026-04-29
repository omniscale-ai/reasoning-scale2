"""Dataclasses and helpers for writing v2 dataset asset metadata."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Author:
    name: str
    country: str | None = None
    institution: str | None = None
    orcid: str | None = None


@dataclass(frozen=True, slots=True)
class Institution:
    name: str
    country: str


@dataclass(frozen=True, slots=True)
class DatasetFile:
    path: str
    description: str
    format: str


@dataclass(frozen=True, slots=True)
class DatasetDetails:
    """Mirrors the v2 dataset asset details.json schema."""

    spec_version: str
    dataset_id: str
    name: str
    version: str | None
    short_description: str
    description_path: str
    source_paper_id: str | None
    url: str | None
    year: int
    authors: list[Author]
    institutions: list[Institution]
    license: str | None
    access_kind: str
    size_description: str
    files: list[DatasetFile]
    categories: list[str]
    download_url: str | None = None
    date_published: str | None = None
    download_status: str | None = None
    download_failure_reason: str | None = None
    extra_notes: list[str] = field(default_factory=list)


def details_to_dict(*, details: DatasetDetails) -> dict[str, object]:
    """Serialize details to dict, omitting fields that are not part of the spec.

    The spec requires ``download_status`` and ``download_failure_reason`` to be present
    for this project's purposes (we treat them as standard registry fields even though they
    are not in the v2 spec); they are written verbatim. The extra ``extra_notes`` field
    is not part of the spec and is omitted from the output.
    """
    raw: dict[str, object] = asdict(obj=details)
    raw.pop("extra_notes", None)
    return raw


def write_dataset_asset(
    *,
    asset_root: Path,
    details: DatasetDetails,
    description_md: str,
) -> Path:
    """Write details.json and the description document.

    Caller is responsible for ensuring ``files/`` exists and contains at least one file
    listed in ``details.files``.
    """
    asset_root.mkdir(parents=True, exist_ok=True)
    files_dir: Path = asset_root / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    details_path: Path = asset_root / "details.json"
    details_path.write_text(
        json.dumps(details_to_dict(details=details), indent=2) + "\n",
        encoding="utf-8",
    )

    description_path: Path = asset_root / details.description_path
    description_path.write_text(description_md, encoding="utf-8")

    return asset_root
