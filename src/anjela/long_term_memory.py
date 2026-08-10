"""High-level interface for durable facts."""

from .facts import MemoryFact
from .sqlite_memory import SQLiteConversationStore


class LongTermMemory:
    def __init__(self, store: SQLiteConversationStore) -> None:
        self.store = store

    def remember(self, key: str, value: str, category: str = "general") -> None:
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError("Memory key and value cannot be empty")
        self.store.remember(MemoryFact(key=key, value=value, category=category.strip() or "general"))

    def forget(self, key: str) -> None:
        self.store.forget(key.strip())

    def all(self) -> list[MemoryFact]:
        return self.store.facts()

    def context(self) -> str:
        facts = self.all()
        if not facts:
            return ""
        return "\n".join(fact.as_context() for fact in facts)
