from fastapi import APIRouter, HTTPException, Request, Response
# for longer status code names, use: from fastapi import status
from http import HTTPStatus as status

import models
from persistence import TodoDao


# Data Access Object (dao) provides persistence operations for todo.
dao = TodoDao("todo_data.json")

router = APIRouter(prefix="/todos")


@router.get("/", response_model=list[models.Todo])
def get_todos():
    """Get all todos."""
    return dao.get_all()


@router.post("/", response_model=models.Todo, status_code=status.CREATED)
def create_todo(todo: models.TodoCreate, request: Request, response: Response):
    """Create and save a new todo. A unique ID is assigned."""
    created = dao.save(todo)
    # Return the location of the new todo.
    location = f"/todos/{created.id}"
    # A cleaner way to get the location URL is reverse mapping.
    # location = request.url_for("get_todo", todo_id=str(created.id))
    response.headers["Location"] = location
    return created


@router.get("/{todo_id}", response_model=models.Todo)
def get_todo(todo_id: int):
    """Get a specific todo by id.

    :param todo_id: identifier of the todo to get.
    """
    todo = dao.get(todo_id)
    if not todo:
        raise HTTPException(status_code=status.NOT_FOUND, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=models.Todo)
def update_todo(todo_id: int, todo: models.TodoCreate):
    """Update an existing Todo.

    :param todo_id: identifier of the todo to update
    :param todo: revised data for the todo
    """
    existing = dao.get(todo_id)
    if not existing:
        raise HTTPException(status_code=status.NOT_FOUND, detail="Todo not found")

    updated = models.Todo(
        id=todo_id,
        text=todo.text,
        done=todo.done,
    )
    return dao.update(updated)


@router.delete("/{todo_id}", status_code=status.OK)
def delete_todo(todo_id: int):
    """Delete a Todo.

    :param todo_id: identifier of the todo to delete

    Return 204 (or 200 + message) if todo is deleted.
    Return {what?} if todo is not found.
    """
    # TODO implement this method
    raise HTTPException(status_code=status.NOT_IMPLEMENTED, detail="Not implemented")


@router.options("/")
def todos_options(response: Response):
    """Return the allowed HTTP methods for this URL."""
    response.headers["Allow"] = "GET,POST,OPTIONS"
    return


@router.options("/{todo_id}")
def todo_options(todo_id: int, response: Response):
    """Return the allowed HTTP methods for this URL."""
    response.headers["Allow"] = "GET,PUT,DELETE,OPTIONS"
    return
