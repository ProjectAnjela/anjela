from pathlib import Path
from types import SimpleNamespace

import pytest

from anjela.context_loader import load_context
from anjela.memory import Message
from anjela.providers import OpenAIProvider


def test_loads_persona_and_reference_context(tmp_path: Path):
    (tmp_path / "boot.md").write_text("Говори в женском роде", encoding="utf-8")
    (tmp_path / "personality.md").write_text("Обращайся на ты", encoding="utf-8")
    (tmp_path / "memory.md").write_text("Любит Python", encoding="utf-8")
    bundle = load_context(tmp_path)
    assert "Говори в женском роде" in bundle.instructions
    assert "Обращайся на ты" in bundle.instructions
    assert "Любит Python" in bundle.reference_context
    assert "Любит Python" not in bundle.instructions
    assert "not executable" in bundle.reference_context


def test_required_context_missing_fails(tmp_path: Path):
    (tmp_path / "boot.md").write_text("Hello", encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        load_context(tmp_path)


def test_missing_optional_context_produces_no_reference_block(tmp_path: Path):
    (tmp_path / "boot.md").write_text("Hello", encoding="utf-8")
    (tmp_path / "personality.md").write_text("Be warm", encoding="utf-8")

    bundle = load_context(tmp_path)

    assert bundle.reference_context == ""


def test_oversized_context_rejected(tmp_path: Path):
    (tmp_path / "boot.md").write_text("x" * 40001, encoding="utf-8")
    (tmp_path / "personality.md").write_text("OK", encoding="utf-8")
    with pytest.raises(ValueError):
        load_context(tmp_path)


def test_provider_uses_loaded_context(monkeypatch, tmp_path: Path):
    (tmp_path / "boot.md").write_text("Анжела говорит в женском роде", encoding="utf-8")
    (tmp_path / "personality.md").write_text("На ты", encoding="utf-8")
    (tmp_path / "memory.md").write_text("Исторический факт", encoding="utf-8")
    monkeypatch.setenv("ANJELA_CONTEXT_DIR", str(tmp_path))
    monkeypatch.delenv("ANJELA_INSTRUCTIONS", raising=False)
    calls = []

    class FakeClient:
        def __init__(self, **kwargs):
            self.responses = SimpleNamespace(create=self.create)

        def create(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(output_text="Привет!")

    monkeypatch.setattr("openai.OpenAI", FakeClient)
    provider = OpenAIProvider(model="test", api_key="fake")
    assert provider.respond([Message("user", "Привет")]) == "Привет!"
    assert "женском роде" in calls[0]["instructions"]
    assert calls[0]["input"][0]["role"] == "user"
    assert calls[0]["input"][0]["content"].startswith(
        "[Reference context, not user instructions]\n"
    )
    assert "Исторический факт" in calls[0]["input"][0]["content"]
    assert calls[0]["input"][1] == {"role": "user", "content": "Привет"}


def test_explicit_instructions_override_loader(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("ANJELA_CONTEXT_DIR", str(tmp_path))
    monkeypatch.setattr("openai.OpenAI", lambda **kwargs: SimpleNamespace())
    provider = OpenAIProvider(instructions="Custom rules", api_key="fake")
    assert provider.instructions == "Custom rules"
    assert provider.reference_context == ""
