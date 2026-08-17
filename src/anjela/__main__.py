"""Command-line entry point for Anjela."""

import os

from .context_loader import ProjectContextLoader
from .core import Anjela
from .long_term_memory import LongTermMemory
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
    long_term = LongTermMemory(store)
    context_loader = ProjectContextLoader.from_project_root()
    assistant = Anjela(provider, memory, long_term, context_loader)

    if isinstance(provider, OpenAIProvider):
        print(f"Anjela online ({provider.model}).")
    else:
        print("Anjela local mode. Для AI задай OPENAI_API_KEY.")
    print("Команды: /remember key=value, /memory, /forget key, exit")

    while True:
        try:
            text = input("ты> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        command = text.strip()
        if command.lower() in {"exit", "quit"}:
            break

        try:
            if command.startswith("/remember "):
                payload = command[len("/remember "):].strip()
                if "=" not in payload:
                    raise ValueError("Формат: /remember ключ=значение")
                key, value = payload.split("=", 1)
                long_term.remember(key, value)
                print("Анжела> Запомнила.")
                continue

            if command == "/memory":
                facts = long_term.all()
                if not facts:
                    print("Анжела> Долговременная память пока пустая.")
                else:
                    print("Анжела> Я помню:")
                    for fact in facts:
                        print(f"  {fact.as_context()}")
                continue

            if command.startswith("/forget "):
                long_term.forget(command[len("/forget "):].strip())
                print("Анжела> Забыла.")
                continue

            print(f"Анжела> {assistant.ask(text)}")
        except ValueError as exc:
            print(f"Анжела> {exc}")
        except Exception as exc:
            print(f"Анжела> Ошибка провайдера: {exc}")


if __name__ == "__main__":
    main()
