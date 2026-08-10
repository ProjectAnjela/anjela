"""SQLite-backed conversation and long-term memory storage."""

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .facts import MemoryFact
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
            connection.execute(
                "CREATE TABLE IF NOT EXISTS facts ("
                "key TEXT PRIMARY KEY, value TEXT NOT NULL, "
                "category TEXT NOT NULL DEFAULT 'general')"
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

    def remember(self, fact: "MemoryFact") -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                "INSERT INTO facts (key, value, category) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value, category=excluded.category",
                (fact.key, fact.value, fact.category),
            )
            connection.commit()

    def forget(self, key: str) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute("DELETE FROM facts WHERE key = ?", (key,))
            connection.commit()

    def facts(self) -> list["MemoryFact"]:
        from .facts import MemoryFact

        with sqlite3.connect(self.path) as connection:
            rows = connection.execute(
                "SELECT key, value, category FROM facts ORDER BY key"
            ).fetchall()
        return [MemoryFact(key=key, value=value, category=category) for key, value, category in rows]
