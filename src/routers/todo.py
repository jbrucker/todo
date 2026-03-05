from fastapi import APIRouter, HTTPException, Request, Response
# for longer status code names, use: from fastapi import status
from http import HTTPStatus as status
import logging
from decouple import config

import models
from persistence import TodoDao


logger = logging.getLogger(__name__)

# Data Access Object (dao) provides persistence operations for todo.
todo_file = config("TODO_URL", default="data/todo_data.json")
dao = TodoDao(todo_file)

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
    # Use reverse mapping to ensure we can correct enternal URL.
    location_url = request.url_for("get_todo", todo_id=created.id)
    location = location_url.path
    if location.startswith("http"):
        # Screwed up. Path should not include the scheme and host.
        import re
        match = re.search(r"https?://[^/]*(/.*)", location)
        if match is not None: location = match.group(1)
    # This doesn't work. It doesn't includes the API root path.
    # location = router.url_path_for("get_todo", todo_id=created.id)
    response.headers["Location"] = str(location)
    logger.warning(f"Created todo with id {created.id} at {location}")
    return created


@router.get("/{todo_id}", response_model=models.Todo)
def get_todo(todo_id: int):
    """Get a specific todo by id.

    :param todo_id: identifier of the todo to get.
    """
    todo = dao.get(todo_id)
    if not todo:
        raise HTTPException(status_code=status.NOT_FOUND, detail=f"Todo {todo_id} not found")
    return todo


@router.put("/{todo_id}", response_model=models.Todo)
def update_todo(todo_id: int, todo: models.TodoCreate):
    """Update an existing Todo.

    :param todo_id: identifier of the todo to update
    :param todo: revised data for the todo
    """
    existing = dao.get(todo_id)
    if not existing:
        raise HTTPException(status_code=status.NOT_FOUND, detail=f"Todo {todo_id} not found")

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
    Return 404 if the todo id is not found.
    """
    if not dao.exists(todo_id):
        raise HTTPException(status_code=status.NOT_FOUND, detail=f"Todo {todo_id} not found")
    dao.delete(todo_id)
    if dao.exists(todo_id):
        raise HTTPException(status_code=status.SERVICE_UNAVAILABLE, 
                            detail=f"Persistence FAILed to delete Todo {todo_id}")
    return {"message": f"Todo {todo_id} deleted."}


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
