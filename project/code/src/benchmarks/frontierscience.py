from __future__ import annotations

import random
from pathlib import Path

from src.storage.schema import BenchmarkTask

from .base import BenchmarkLoader


class FrontierScienceLoader(BenchmarkLoader):
    """Load tasks from the openai/frontierscience HuggingFace dataset."""

    HF_DATASET = "openai/frontierscience"
    # Mapping from config subject names to dataset field values
    SUBJECT_MAP = {
        "physics": "physics",
        "chemistry": "chemistry",
        "biology": "biology",
    }

    def __init__(self, cache_dir: str | Path | None = None):
        self._cache_dir = str(cache_dir) if cache_dir else None

    def load(
        self,
        subjects: list[str],
        sample_per_subject: int,
        seed: int = 42,
    ) -> list[BenchmarkTask]:
        from datasets import load_dataset  # lazy import

        ds = load_dataset(
            self.HF_DATASET,
            split="test",
            cache_dir=self._cache_dir,
        )

        tasks: list[BenchmarkTask] = []
        rng = random.Random(seed)

        for subject in subjects:
            subject_key = self.SUBJECT_MAP.get(subject, subject)
            # Filter to olympiad-style tasks for this subject
            subset = [row for row in ds if self._matches_subject(row, subject_key)]
            if not subset:
                raise ValueError(
                    f"No tasks found for subject '{subject}' in {self.HF_DATASET}. "
                    f"Available fields: {list(ds.features.keys())}"
                )

            sample = rng.sample(subset, min(sample_per_subject, len(subset)))

            for row in sample:
                task = self._row_to_task(row, subject)
                tasks.append(task)

        return tasks

    def _matches_subject(self, row: dict, subject_key: str) -> bool:
        val = row.get("subject", "")
        return str(val).lower() == subject_key.lower()

    def _row_to_task(self, row: dict, subject: str) -> BenchmarkTask:
        task_id = str(row.get("task_group_id") or "")
        problem = str(row.get("problem") or "")
        answer = str(row.get("answer") or "")
        metadata = {"subject": row.get("subject", "")}
        return BenchmarkTask(
            task_id=task_id,
            source="frontierscience_olympiad",
            subject=subject,
            problem=problem,
            ground_truth=answer,
            metadata=metadata,
        )
