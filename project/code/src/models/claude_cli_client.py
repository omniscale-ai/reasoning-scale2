from __future__ import annotations

"""
LLM client that calls Claude via the `claude` CLI using stdin.
No API key required — uses the authenticated Claude Code session.
Prompt is passed via stdin to avoid ARG_MAX / segfault issues with long prompts.
"""

import subprocess

from .base import LLMClient


class ClaudeCLIClient(LLMClient):
    """
    Wraps `claude -p -` (reads prompt from stdin) for single-turn completions.
    Multi-turn conversations are flattened into a single prompt with XML tags.
    """

    MAX_RETRIES = 2  # fail fast — 2 × 90s = 3 min max per call
    RETRY_BASE_DELAY = 1.0

    def __init__(self, model_id: str = "claude-sonnet-4-6"):
        self.model_id = model_id

    def _call(
        self,
        messages: list[dict],
        system: str | None,
        max_tokens: int,
    ) -> tuple[str, dict[str, int]]:
        prompt = self._flatten(messages, system)

        result = subprocess.run(
            ["claude", "-p", "-"],  # read from stdin — avoids ARG_MAX limits
            input=prompt,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode != 0:
            stderr = result.stderr[:300] if result.stderr else "(no stderr)"
            raise RuntimeError(f"claude CLI error (rc={result.returncode}): {stderr}")

        text = result.stdout.strip()
        if not text:
            raise RuntimeError("claude CLI returned empty output")

        usage = {
            "input_tokens": len(prompt) // 4,
            "output_tokens": len(text) // 4,
        }
        return text, usage

    def _flatten(self, messages: list[dict], system: str | None) -> str:
        parts = []
        if system:
            parts.append(f"<system>\n{system}\n</system>")
        for m in messages:
            role = m["role"].upper()
            parts.append(f"<{role}>\n{m['content']}\n</{role}>")
        parts.append("\nPlease respond as ASSISTANT. Output only what ASSISTANT should say.")
        return "\n\n".join(parts)
