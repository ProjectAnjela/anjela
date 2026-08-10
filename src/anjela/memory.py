"""Conversation memory primitives."""

from dataclasses import dataclass, field

from .sqlite_memory import SQLiteConversationStore


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ConversationMemory:
    messages: list[Message] = field(default_factory=list)
    store: SQLiteConversationStore | None = None

    def __post_init__(self) -> None:
        if self.store is not None and not self.messages:
            self.messages = self.store.history()

    def add(self, role: str, content: str) -> None:
        message = Message(role=role, content=content)
        self.messages.append(message)
        if self.store is not None:
            self.store.add(message)

    def history(self) -> list[Message]:
        return list(self.messages)
