from __future__ import annotations

import time
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract LLM client with retry and token tracking."""

    MAX_RETRIES = 5
    RETRY_BASE_DELAY = 2.0  # seconds

    @abstractmethod
    def _call(
        self, messages: list[dict], system: str | None, max_tokens: int
    ) -> tuple[str, dict[str, int]]:
        """Raw API call. Returns (text, token_usage)."""

    def complete(
        self,
        messages: list[dict[str, str]],
        system: str | None = None,
        max_tokens: int = 2048,
    ) -> tuple[str, dict[str, int]]:
        """Call the LLM with exponential backoff retry. Returns (text, usage)."""
        last_error: Exception | None = None
        for attempt in range(self.MAX_RETRIES):
            try:
                return self._call(messages, system, max_tokens)
            except Exception as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_BASE_DELAY * (2**attempt)
                    time.sleep(delay)
        raise RuntimeError(f"LLM call failed after {self.MAX_RETRIES} attempts") from last_error
