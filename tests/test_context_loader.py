from pathlib import Path

from anjela.context_loader import ProjectContextLoader


def test_context_loader_reads_known_context_files_in_order(tmp_path: Path) -> None:
    context_dir = tmp_path / "docs" / "context"
    context_dir.mkdir(parents=True)
    (context_dir / "personality.md").write_text("Personality", encoding="utf-8")
    (context_dir / "boot.md").write_text("Boot", encoding="utf-8")
    (context_dir / "README.md").write_text("Index", encoding="utf-8")
    (context_dir / "memory.md").write_text("   ", encoding="utf-8")

    context = ProjectContextLoader.from_project_root(tmp_path).load()

    assert "Sanitized project context for Anjela." in context
    assert context.index("## boot.md") < context.index("## personality.md")
    assert "Boot" in context
    assert "Personality" in context
    assert "README.md" not in context
    assert "memory.md" not in context


def test_context_loader_returns_empty_string_without_context(tmp_path: Path) -> None:
    loader = ProjectContextLoader(tmp_path / "missing")

    assert loader.load() == ""
