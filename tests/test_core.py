from pathlib import Path

from anjela.core import Anjela
from anjela.long_term_memory import LongTermMemory
from anjela.memory import ConversationMemory
from anjela.providers import EchoProvider
from anjela.sqlite_memory import SQLiteConversationStore


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
