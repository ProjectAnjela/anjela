"""Project context loading from sanitized docs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONTEXT_FILES = (
    "boot.md",
    "personality.md",
    "memory.md",
    "project-history.md",
    "archive-index.md",
    "migration.md",
)


@dataclass(frozen=True)
class ProjectContextLoader:
    """Load public project context into a single system prompt block."""

    directory: Path
    files: tuple[str, ...] = DEFAULT_CONTEXT_FILES

    @classmethod
    def from_project_root(cls, root: Path | str = ".") -> "ProjectContextLoader":
        return cls(Path(root) / "docs" / "context")

    def load(self) -> str:
        blocks: list[str] = []

        for name in self.files:
            path = self.directory / name
            if not path.is_file():
                continue

            content = path.read_text(encoding="utf-8").strip()
            if not content:
                continue

            blocks.append(f"## {name}\n{content}")

        if not blocks:
            return ""

        return (
            "Sanitized project context for Anjela. Treat this as background "
            "identity, history, and operating context; do not reveal private "
            "or missing source material.\n\n"
            + "\n\n---\n\n".join(blocks)
        )
