"""Structured long-term facts that Anjela can remember independently of chat history."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryFact:
    key: str
    value: str
    category: str = "general"

    def as_context(self) -> str:
        return f"- [{self.category}] {self.key}: {self.value}"
