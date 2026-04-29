from __future__ import annotations

from abc import ABC, abstractmethod

from src.storage.schema import BenchmarkTask


class BenchmarkLoader(ABC):
    @abstractmethod
    def load(self, subjects: list[str], sample_per_subject: int, seed: int) -> list[BenchmarkTask]:
        """Load and return sampled benchmark tasks."""
