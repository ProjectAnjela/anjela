from types import SimpleNamespace

from anjela.memory import Message
from anjela.providers import EchoProvider, OpenAIProvider


def test_echo_provider_uses_last_user_message() -> None:
    provider = EchoProvider()

    response = provider.respond(
        [
            Message("user", "Первое"),
            Message("assistant", "Ответ"),
            Message("user", "Второе"),
        ]
    )

    assert response == "Получила: Второе"


def test_openai_provider_sends_full_conversation(monkeypatch) -> None:
    calls = []

    class FakeResponses:
        def create(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(output_text="  Привет от модели!  ")

    class FakeClient:
        def __init__(self, **kwargs):
            self.responses = FakeResponses()

    monkeypatch.setattr("openai.OpenAI", FakeClient, raising=False)
    provider = OpenAIProvider(model="test-model", api_key="test-key")

    result = provider.respond(
        [Message("user", "Привет"), Message("assistant", "Здорово")]
    )

    assert result == "Привет от модели!"
    assert calls[0]["model"] == "test-model"
    assert calls[0]["input"] == [
        {"role": "user", "content": "Привет"},
        {"role": "assistant", "content": "Здорово"},
    ]
