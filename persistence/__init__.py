"""Facade for getting persistence implementations."""
from persistence import base_todo_dao
from persistence.todo_dao_file import TodoFileDao

class TodoDao(base_todo_dao.TodoDao):
    """Alias for the file-based Todo DAO implementation."""
    def __new__(cls, *args, **kwargs):
        return TodoFileDao(*args, **kwargs)
    
