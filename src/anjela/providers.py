"""LLM provider boundary.

The core does not depend on a specific AI vendor. A real provider can be
plugged in later without rewriting the assistant loop.
"""

from abc import ABC, abstractmethod

from .memory import Message


class Provider(ABC):
    @abstractmethod
    def respond(self, messages: list[Message]) -> str:
        """Generate a response from conversation messages."""


class EchoProvider(Provider):
    """Tiny deterministic provider used for the first MVP and tests."""

    def respond(self, messages: list[Message]) -> str:
        user_messages = [m.content for m in messages if m.role == "user"]
        if not user_messages:
            return "Я здесь."
        return f"Получила: {user_messages[-1]}"
