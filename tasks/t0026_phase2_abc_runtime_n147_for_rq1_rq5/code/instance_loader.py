"""Loads the three benchmark JSONL files into a paired N=147 instance manifest."""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.paths import (
    FRONTIERSCIENCE_JSONL_PATH,
    N_FRONTSCI_TARGET,
    N_SWEBENCH_TARGET,
    N_TAUBENCH_TARGET,
    SEED,
    SUBSET_FRONTSCI,
    SUBSET_SWEBENCH,
    SUBSET_TAUBENCH,
    SWEBENCH_JSONL_PATH,
    TAUBENCH_JSONL_PATH,
)

type SubsetName = Literal["swebench", "taubench", "frontsci"]


@dataclass(frozen=True, slots=True)
class Instance:
    instance_id: str
    subset: str
    problem_text: str
    gold: dict[str, Any] | None


def _read_jsonl(*, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if len(stripped) == 0:
                continue
            obj = json.loads(stripped)
            assert isinstance(obj, dict), f"row in {path} is not an object: {obj!r}"
            rows.append(obj)
    return rows


def _sha256_of_file(*, path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_swebench_stratified(*, n_target: int, seed: int) -> list[Instance]:
    rows = _read_jsonl(path=SWEBENCH_JSONL_PATH)
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        difficulty = str(row.get("difficulty", "unknown"))
        buckets.setdefault(difficulty, []).append(row)
    rng = random.Random(seed)
    for bucket_rows in buckets.values():
        bucket_rows.sort(key=lambda r: str(r["instance_id"]))
        rng.shuffle(bucket_rows)
    bucket_keys = sorted(buckets.keys())
    total_available = sum(len(buckets[k]) for k in bucket_keys)
    sampled: list[dict[str, Any]] = []
    cursor: dict[str, int] = {k: 0 for k in bucket_keys}
    while len(sampled) < n_target and len(sampled) < total_available:
        for k in bucket_keys:
            if len(sampled) >= n_target:
                break
            idx = cursor[k]
            if idx < len(buckets[k]):
                sampled.append(buckets[k][idx])
                cursor[k] = idx + 1
    sampled.sort(key=lambda r: str(r["instance_id"]))
    out: list[Instance] = []
    for row in sampled:
        instance_id = str(row["instance_id"])
        problem_text = str(row.get("problem_statement", ""))
        gold: dict[str, Any] = {
            "FAIL_TO_PASS": row.get("FAIL_TO_PASS"),
            "PASS_TO_PASS": row.get("PASS_TO_PASS"),
            "patch": row.get("patch"),
            "test_patch": row.get("test_patch"),
            "repo": row.get("repo"),
            "base_commit": row.get("base_commit"),
            "difficulty": row.get("difficulty"),
        }
        out.append(
            Instance(
                instance_id=instance_id,
                subset=SUBSET_SWEBENCH,
                problem_text=problem_text,
                gold=gold,
            )
        )
    return out


def _load_taubench(*, n_target: int) -> list[Instance]:
    rows = _read_jsonl(path=TAUBENCH_JSONL_PATH)
    rows.sort(key=lambda r: (str(r.get("domain", "")), int(r.get("task_index", 0))))
    selected = rows[:n_target]
    out: list[Instance] = []
    for row in selected:
        domain = str(row.get("domain", "unknown"))
        task_index = int(row.get("task_index", 0))
        instance_id = f"tau-{domain}-{task_index:04d}"
        problem_text = str(row.get("instruction", ""))
        gold: dict[str, Any] = {
            "outputs": row.get("outputs"),
            "actions": row.get("actions"),
            "domain": domain,
        }
        out.append(
            Instance(
                instance_id=instance_id,
                subset=SUBSET_TAUBENCH,
                problem_text=problem_text,
                gold=gold,
            )
        )
    return out


def _load_frontsci(*, n_target: int) -> list[Instance]:
    rows = _read_jsonl(path=FRONTIERSCIENCE_JSONL_PATH)
    rows.sort(key=lambda r: str(r.get("task_id", "")))
    selected = rows[:n_target]
    out: list[Instance] = []
    for row in selected:
        instance_id = str(row.get("task_id", ""))
        problem_text = str(row.get("problem", ""))
        gold: dict[str, Any] = {
            "solution": row.get("solution"),
            "domain": row.get("domain"),
            "difficulty": row.get("difficulty"),
        }
        out.append(
            Instance(
                instance_id=instance_id,
                subset=SUBSET_FRONTSCI,
                problem_text=problem_text,
                gold=gold,
            )
        )
    return out


def load_instances() -> list[Instance]:
    swe = _load_swebench_stratified(n_target=N_SWEBENCH_TARGET, seed=SEED)
    tau = _load_taubench(n_target=N_TAUBENCH_TARGET)
    fs = _load_frontsci(n_target=N_FRONTSCI_TARGET)
    assert len(swe) == N_SWEBENCH_TARGET, f"SWE-bench: expected {N_SWEBENCH_TARGET}, got {len(swe)}"
    assert len(tau) == N_TAUBENCH_TARGET, f"Tau-bench: expected {N_TAUBENCH_TARGET}, got {len(tau)}"
    assert len(fs) == N_FRONTSCI_TARGET, f"FrontSci: expected {N_FRONTSCI_TARGET}, got {len(fs)}"
    return swe + tau + fs


def sample_per_subset(*, instances: list[Instance], n_per_subset: int) -> list[Instance]:
    by_subset: dict[str, list[Instance]] = {}
    for inst in instances:
        by_subset.setdefault(inst.subset, []).append(inst)
    out: list[Instance] = []
    for subset_name in (SUBSET_SWEBENCH, SUBSET_TAUBENCH, SUBSET_FRONTSCI):
        subset_instances = by_subset.get(subset_name, [])
        out.extend(subset_instances[:n_per_subset])
    return out


def write_manifest(*, instances: list[Instance], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    per_subset_counts: dict[str, int] = {}
    per_subset_ids: dict[str, list[str]] = {}
    for inst in instances:
        per_subset_counts[inst.subset] = per_subset_counts.get(inst.subset, 0) + 1
        per_subset_ids.setdefault(inst.subset, []).append(inst.instance_id)
    manifest: dict[str, Any] = {
        "seed": SEED,
        "n_total": len(instances),
        "per_subset_counts": per_subset_counts,
        "source_sha256": {
            SUBSET_SWEBENCH: _sha256_of_file(path=SWEBENCH_JSONL_PATH),
            SUBSET_TAUBENCH: _sha256_of_file(path=TAUBENCH_JSONL_PATH),
            SUBSET_FRONTSCI: _sha256_of_file(path=FRONTIERSCIENCE_JSONL_PATH),
        },
        "instance_ids": [inst.instance_id for inst in instances],
        "per_subset_instance_ids": per_subset_ids,
    }
    output_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
