"""Main assistant orchestration."""

from .context_loader import ProjectContextLoader
from .long_term_memory import LongTermMemory
from .memory import ConversationMemory, Message
from .providers import Provider


class Anjela:
    def __init__(
        self,
        provider: Provider,
        memory: ConversationMemory | None = None,
        long_term_memory: LongTermMemory | None = None,
        context_loader: ProjectContextLoader | None = None,
    ) -> None:
        self.provider = provider
        self.memory = memory or ConversationMemory()
        self.long_term_memory = long_term_memory
        self.context_loader = context_loader

    def ask(self, text: str) -> str:
        text = text.strip()
        if not text:
            raise ValueError("Message cannot be empty")

        self.memory.add("user", text)
        messages = self.memory.history()
        system_messages: list[Message] = []

        if self.context_loader is not None:
            project_context = self.context_loader.load()
            if project_context:
                system_messages.append(Message(role="system", content=project_context))

        if self.long_term_memory is not None:
            context = self.long_term_memory.context()
            if context:
                system_messages.append(
                    Message(
                        role="system",
                        content="Durable facts about the user. Use them when relevant; do not invent facts.\n"
                        + context,
                    )
                )

        if system_messages:
            messages = [*system_messages, *messages]

        response = self.provider.respond(messages)
        self.memory.add("assistant", response)
        return response
