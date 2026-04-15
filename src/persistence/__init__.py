"""Facade for getting persistence implementations.

Expose `TodoDao` as the default, file-based DAO class so tests
can monkeypatch class-level helpers like `_write_all`.
"""
from .todo_file_dao import TodoFileDao

# Export the concrete file-backed DAO as the public `TodoDao` symbol.
TodoDao = TodoFileDao
