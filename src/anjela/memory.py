"""Conversation memory primitives."""

from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ConversationMemory:
    messages: list[Message] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def history(self) -> list[Message]:
        return list(self.messages)
