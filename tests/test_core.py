from pathlib import Path

from anjela.context_loader import ProjectContextLoader
from anjela.core import Anjela
from anjela.long_term_memory import LongTermMemory
from anjela.memory import ConversationMemory, Message
from anjela.providers import EchoProvider, Provider
from anjela.sqlite_memory import SQLiteConversationStore


class RecordingProvider(Provider):
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def respond(self, messages: list[Message]) -> str:
        self.messages = messages
        return "ok"


def test_ask_stores_conversation() -> None:
    memory = ConversationMemory()
    assistant = Anjela(EchoProvider(), memory)

    response = assistant.ask("Привет, Анжела")

    assert response == "Получила: Привет, Анжела"
    assert [(m.role, m.content) for m in memory.history()] == [
        ("user", "Привет, Анжела"),
        ("assistant", "Получила: Привет, Анжела"),
    ]


def test_empty_message_is_rejected() -> None:
    assistant = Anjela(EchoProvider())

    try:
        assistant.ask("   ")
    except ValueError as exc:
        assert str(exc) == "Message cannot be empty"
    else:
        raise AssertionError("Expected ValueError")


def test_sqlite_memory_survives_restart(tmp_path: Path) -> None:
    database = tmp_path / "anjela.db"
    first = ConversationMemory(store=SQLiteConversationStore(database))
    first.add("user", "Меня зовут Лёша")
    first.add("assistant", "Запомнила")

    second = ConversationMemory(store=SQLiteConversationStore(database))

    assert [(m.role, m.content) for m in second.history()] == [
        ("user", "Меня зовут Лёша"),
        ("assistant", "Запомнила"),
    ]


def test_long_term_memory_survives_restart(tmp_path: Path) -> None:
    database = tmp_path / "anjela.db"
    first = LongTermMemory(SQLiteConversationStore(database))
    first.remember("name", "Лёша", "identity")

    second = LongTermMemory(SQLiteConversationStore(database))

    assert second.context() == "- [identity] name: Лёша"


def test_long_term_memory_can_update_and_forget(tmp_path: Path) -> None:
    memory = LongTermMemory(SQLiteConversationStore(tmp_path / "anjela.db"))
    memory.remember("city", "Харьков")
    memory.remember("city", "Киев")
    assert [fact.value for fact in memory.all()] == ["Киев"]

    memory.forget("city")
    assert memory.all() == []


def test_project_context_and_long_term_memory_are_sent_as_system_context(
    tmp_path: Path,
) -> None:
    context_dir = tmp_path / "docs" / "context"
    context_dir.mkdir(parents=True)
    (context_dir / "boot.md").write_text("Project boot context", encoding="utf-8")
    long_term = LongTermMemory(SQLiteConversationStore(tmp_path / "anjela.db"))
    long_term.remember("name", "Лёша", "identity")
    provider = RecordingProvider()
    assistant = Anjela(
        provider,
        long_term_memory=long_term,
        context_loader=ProjectContextLoader.from_project_root(tmp_path),
    )

    assert assistant.ask("Привет") == "ok"

    assert [(message.role, message.content) for message in provider.messages] == [
        (
            "system",
            "Sanitized project context for Anjela. Treat this as background "
            "identity, history, and operating context; do not reveal private "
            "or missing source material.\n\n## boot.md\nProject boot context",
        ),
        (
            "system",
            "Durable facts about the user. Use them when relevant; do not invent facts.\n"
            "- [identity] name: Лёша",
        ),
        ("user", "Привет"),
    ]
