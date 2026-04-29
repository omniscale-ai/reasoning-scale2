from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from enum import Enum
from pathlib import Path

from src.storage.schema import ExperimentRun, ProbeRecord, RevisionRecord


def _to_dict(obj) -> dict:
    """Recursively convert dataclass to dict, handling Enum and datetime."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {k: _to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, list):
        return [_to_dict(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    return obj


class Repository:
    """JSONL-based append-only storage with checkpoint-resume support."""

    def __init__(self, results_dir: str | Path):
        self._dir = Path(results_dir)
        self._dir.mkdir(parents=True, exist_ok=True)

        self._runs_file = self._dir / "runs.jsonl"
        self._probes_file = self._dir / "probes.jsonl"
        self._revisions_file = self._dir / "revisions.jsonl"

        # In-memory checkpoint index: (task_id, model_id, mode, probe_step) → True
        self._checkpoint: set[tuple] = set()
        self._load_checkpoints()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def save_run(self, run: ExperimentRun) -> None:
        self._append(self._runs_file, _to_dict(run))

    def save_probe(self, probe: ProbeRecord) -> None:
        self._append(self._probes_file, _to_dict(probe))
        mode_val = (
            probe.simulation_mode.value
            if hasattr(probe.simulation_mode, "value")
            else probe.simulation_mode
        )
        key = (probe.task_id, probe.model_id, mode_val, probe.probed_step, probe.context_mode)
        self._checkpoint.add(key)

    def save_revision(self, revision: RevisionRecord) -> None:
        self._append(self._revisions_file, _to_dict(revision))

    # ------------------------------------------------------------------
    # Checkpoint
    # ------------------------------------------------------------------

    def is_done(
        self, task_id: str, model_id: str, mode: str, probe_step: int, context_mode: str
    ) -> bool:
        return (task_id, model_id, mode, probe_step, context_mode) in self._checkpoint

    def _load_checkpoints(self) -> None:
        if not self._probes_file.exists():
            return
        for line in self._probes_file.read_text().splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                key = (
                    row.get("task_id", ""),
                    row.get("model_id", ""),
                    row.get("simulation_mode", ""),
                    row.get("probed_step", 0),
                    row.get("context_mode", "full"),
                )
                self._checkpoint.add(key)
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def load_probes(self) -> list[dict]:
        return self._read_jsonl(self._probes_file)

    def load_revisions(self) -> list[dict]:
        return self._read_jsonl(self._revisions_file)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _append(self, path: Path, data: dict) -> None:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, default=str) + "\n")

    def _read_jsonl(self, path: Path) -> list[dict]:
        if not path.exists():
            return []
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass
        return rows
