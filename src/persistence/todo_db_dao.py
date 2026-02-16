"""SQLite-backed Todo DAO implementing `TodoDao` from `base_todo_dao`.

This implementation is safe for multi-threaded use by serializing
database access with a re-entrant lock and using SQLite WAL mode.
"""
from __future__ import annotations

import sqlite3
import threading
from typing import Optional, List

from models import Todo, TodoCreate
from .base_todo_dao import TodoDao


class TodoSqliteDao(TodoDao):
    """Thread-safe SQLite implementation of the Todo DAO.

    Args:
        db_path: Path to the SQLite database file. Defaults to `todo.sqlite3`.
    See:
        base_todo_dao.TodoDao for method documentation.
    """

    def __init__(self, db_path: str = "todo.sqlite3") -> None:
        self._db_path = db_path
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(
            self._db_path, check_same_thread=False, isolation_level=None
        )
        self._conn.row_factory = sqlite3.Row
        # Initialize DB and tune pragmas under lock
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("PRAGMA journal_mode=WAL;")
            cur.execute("PRAGMA foreign_keys = ON;")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    done INTEGER NOT NULL
                )
                """
            )
            cur.close()

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            try:
                self._conn.close()
            except Exception:
                pass

    def __del__(self) -> None:  # pragma: no cover - best-effort cleanup
        try:
            self.close()
        except Exception:
            pass

    def get(self, todo_id: int) -> Optional[Todo]:
        with self._lock:
            cur = self._conn.execute(
                "SELECT id, text, done FROM todos WHERE id = ?", (todo_id,)
            )
            row = cur.fetchone()
            if row is None:
                return None
            return Todo(id=int(row["id"]), text=row["text"], done=bool(row["done"]))

    def get_all(self) -> List[Todo]:
        with self._lock:
            cur = self._conn.execute("SELECT id, text, done FROM todos ORDER BY id")
            rows = cur.fetchall()
            return [
                Todo(id=int(r["id"]), text=r["text"], done=bool(r["done"]))
                for r in rows
            ]

    def save(self, todo_create: TodoCreate) -> Todo:
        with self._lock:
            cur = self._conn.execute(
                "INSERT INTO todos (text, done) VALUES (?, ?)",
                (todo_create.text, int(todo_create.done)),
            )
            new_id = cur.lastrowid or 1
            return Todo(id=int(new_id), text=todo_create.text, done=bool(todo_create.done))

    def update(self, todo: Todo) -> Todo:
        with self._lock:
            cur = self._conn.execute(
                "UPDATE todos SET text = ?, done = ? WHERE id = ?",
                (todo.text, int(todo.done), todo.id),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Todo with id {todo.id} does not exist")
            return todo

    def delete(self, todo_id: int) -> None:
        with self._lock:
            cur = self._conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            if cur.rowcount == 0:
                raise ValueError(f"Todo with id {todo_id} does not exist")
