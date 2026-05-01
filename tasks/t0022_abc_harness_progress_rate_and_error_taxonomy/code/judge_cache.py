"""Disk cache for judge call results.

Caching is critical: t0023's confirmatory ABC run will replay the same
trajectories that t0022's t0012 replay does, and we do not want to re-spend
on identical (environment, trajectory_step, prompt) inputs.

The cache key is a SHA-256 hex digest of
``f"{environment_id}|{trajectory_hash}|{prompt_key}|{prompt_payload}"``.
Storage is one JSON file per key under
``code/_cache/<first-2-hex>/<rest-of-hex>.json`` (sharded to keep directory
sizes manageable).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.paths import (
    JUDGE_CACHE_DIR as _DEFAULT_JUDGE_CACHE_DIR,
)

# Module-level mutable default; tests monkeypatch this attribute. Functions read it
# back through ``sys.modules[__name__]`` so monkeypatch.setattr takes effect at call
# time rather than at function-definition time (which would bind the default arg).
JUDGE_CACHE_DIR: Path = _DEFAULT_JUDGE_CACHE_DIR


def _resolve_root(*, root: Path | None) -> Path:
    """Return the active cache root, looking up the module-level default each time."""
    if root is not None:
        return root
    return Path(sys.modules[__name__].JUDGE_CACHE_DIR)


def _shard_path(*, key: str, root: Path | None = None) -> Path:
    """Return the on-disk path for a cache key."""
    if len(key) < 3:
        raise ValueError(f"cache key too short: {key!r}")
    active_root = _resolve_root(root=root)
    return active_root / key[:2] / f"{key[2:]}.json"


def make_cache_key(
    *,
    environment_id: str,
    trajectory_hash: str,
    prompt_key: str,
    prompt_payload: str,
) -> str:
    """Compute a stable SHA-256 cache key.

    All four components are included in the digest so prompt-template changes
    automatically invalidate cached values.
    """
    raw = f"{environment_id}|{trajectory_hash}|{prompt_key}|{prompt_payload}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def cache_get(*, key: str, root: Path | None = None) -> str | None:
    """Return the cached value for ``key`` or ``None`` if not present."""
    path = _shard_path(key=key, root=root)
    if not path.exists():
        return None
    try:
        with path.open(encoding="utf-8") as f:
            data: Any = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    value = data.get("value")
    return value if isinstance(value, str) else None


def cache_put(*, key: str, value: str, root: Path | None = None) -> None:
    """Store ``value`` under ``key``. Overwrites any existing entry."""
    path = _shard_path(key=key, root=root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {"value": value}
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f)


def hash_trajectory_step(
    *,
    turn_index: int,
    granularity: str,
    thought: str,
    action: str,
    observation: str,
) -> str:
    """Stable hash for a trajectory step (used as the trajectory_hash component)."""
    raw = f"{turn_index}|{granularity}|{thought}|{action}|{observation}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
