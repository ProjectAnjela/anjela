"""LLM provider boundary and concrete model adapters."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any

from .memory import Message


class Provider(ABC):
    @abstractmethod
    def respond(self, messages: list[Message]) -> str:
        """Generate a response from conversation messages."""


class EchoProvider(Provider):
    """Tiny deterministic provider used by tests and offline development."""

    def respond(self, messages: list[Message]) -> str:
        user_messages = [m.content for m in messages if m.role == "user"]
        if not user_messages:
            return "Я здесь."
        return f"Получила: {user_messages[-1]}"


class OpenAIProvider(Provider):
    """OpenAI Responses API adapter.

    The SDK is imported lazily so Anjela can still run with EchoProvider
    without installing the optional OpenAI dependency.
    """

    def __init__(
        self,
        model: str | None = None,
        instructions: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.model = model or os.getenv("ANJELA_MODEL", "gpt-5.5")
        self.instructions = instructions or os.getenv(
            "ANJELA_INSTRUCTIONS",
            "You are Anjela, a helpful personal AI assistant. Speak naturally, clearly, and warmly.",
        )

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "OpenAI support is not installed. Run: pip install -e '.[openai]'"
            ) from exc

        self._client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def respond(self, messages: list[Message]) -> str:
        if not messages:
            raise ValueError("Conversation cannot be empty")

        response = self._client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input=[
                {"role": message.role, "content": message.content}
                for message in messages
            ],
        )
        text = response.output_text.strip()
        if not text:
            raise RuntimeError("OpenAI returned an empty response")
        return text
