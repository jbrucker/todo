"""Abstract class defining methods provided by a Todo Data Access Object (DAO).

Concrete implementations should provide this methods.
"""
from abc import abstractmethod

from models import Todo, TodoCreate


class TodoDao:
    """Persistence operations for Todo items.

    Methods:
        get(todo_id: int) -> Todo|None: Get a Todo by id.
        get_all() -> list[Todo]:        Get all Todo items.
        save(new_todo: TodoCreate) -> Todo: Save a new Todo.
        update(todo: Todo) -> None:     Update an existing Todo.
        delete(todo_id: int) -> None:   Delete a Todo by id.

    Args:
        storage_path: (str) a path or URL to the todo store.
           For file-based storage this is path to the file.
           For database, this may be a path or URL to database.
    """

    @abstractmethod
    def get(self, todo_id: int) -> Todo | None:
        """Get a Todo by its id.

        :param todo_id: The identifier of the todo to retrieve.
        :return: The Todo with the given id, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Todo]:
        """Get a list of all Todo items.
        
        :return: A list of all Todo items, possibly empty.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, todo_id: int) -> bool:
        """Check if a Todo with the given id exists in persistent storage.

        :param todo_id: The identifier of the todo to check.
        :return: True if a Todo with the given id exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, todo_create: TodoCreate) -> Todo:
        """Save a new Todo and assign it an id.

        :param todo_create: a TodoCreate object with info for the new Todo.
        :return: The created Todo with its assigned id.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, todo: Todo) -> Todo:
        """Update an existing Todo.
        
        :param todo: The Todo object with updated data.
        :return: The updated Todo object.
        :raises ValueError: if the Todo id does not exist in persistent storage.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, todo_id: int) -> None:
        """Delete a Todo by its id.
        
        :param todo_id: The identifier of the todo to delete.
        :raises ValueError: if the Todo id does not exist in persistent storage.
        """
        raise NotImplementedError
