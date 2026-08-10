from anjela.core import Anjela
from anjela.memory import ConversationMemory
from anjela.providers import EchoProvider


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
