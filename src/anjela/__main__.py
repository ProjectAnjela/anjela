"""Command-line entry point for Anjela."""

import os

from .core import Anjela
from .memory import ConversationMemory
from .providers import EchoProvider, OpenAIProvider, Provider
from .sqlite_memory import SQLiteConversationStore


def build_provider() -> Provider:
    """Use OpenAI when configured, otherwise keep the local MVP available."""
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIProvider()
    return EchoProvider()


def main() -> None:
    provider = build_provider()
    store = SQLiteConversationStore(os.getenv("ANJELA_DB", "anjela.db"))
    memory = ConversationMemory(store=store)
    assistant = Anjela(provider, memory)

    if isinstance(provider, OpenAIProvider):
        print(f"Anjela online ({provider.model}). Напиши 'exit' для выхода.")
    else:
        print("Anjela local mode. Для AI задай OPENAI_API_KEY. Напиши 'exit' для выхода.")

    while True:
        try:
            text = input("ты> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if text.strip().lower() in {"exit", "quit"}:
            break

        try:
            print(f"Анжела> {assistant.ask(text)}")
        except ValueError as exc:
            print(f"Анжела> {exc}")
        except Exception as exc:
            print(f"Анжела> Ошибка провайдера: {exc}")


if __name__ == "__main__":
    main()
