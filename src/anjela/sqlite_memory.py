"""SQLite-backed conversation storage."""

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .memory import Message


class SQLiteConversationStore:
    def __init__(self, path: str | Path = "anjela.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS messages ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "role TEXT NOT NULL, content TEXT NOT NULL)"
            )
            connection.commit()

    def add(self, message: "Message") -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                "INSERT INTO messages (role, content) VALUES (?, ?)",
                (message.role, message.content),
            )
            connection.commit()

    def history(self) -> list["Message"]:
        from .memory import Message

        with sqlite3.connect(self.path) as connection:
            rows = connection.execute(
                "SELECT role, content FROM messages ORDER BY id"
            ).fetchall()
        return [Message(role=role, content=content) for role, content in rows]
