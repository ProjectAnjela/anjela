"""Main assistant orchestration."""

from .memory import ConversationMemory
from .providers import Provider


class Anjela:
    def __init__(self, provider: Provider, memory: ConversationMemory | None = None) -> None:
        self.provider = provider
        self.memory = memory or ConversationMemory()

    def ask(self, text: str) -> str:
        text = text.strip()
        if not text:
            raise ValueError("Message cannot be empty")

        self.memory.add("user", text)
        response = self.provider.respond(self.memory.history())
        self.memory.add("assistant", response)
        return response
