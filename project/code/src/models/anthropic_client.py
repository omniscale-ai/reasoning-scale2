from __future__ import annotations

import os

import anthropic

from .base import LLMClient


class AnthropicClient(LLMClient):
    def __init__(self, model_id: str, temperature: float = 0.0):
        self.model_id = model_id
        self.temperature = temperature
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        self._client = anthropic.Anthropic(api_key=api_key)

    def _call(
        self,
        messages: list[dict],
        system: str | None,
        max_tokens: int,
    ) -> tuple[str, dict[str, int]]:
        kwargs: dict = dict(
            model=self.model_id,
            max_tokens=max_tokens,
            messages=messages,
            temperature=self.temperature,
        )
        if system:
            kwargs["system"] = system

        response = self._client.messages.create(**kwargs)
        text = response.content[0].text
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        return text, usage
