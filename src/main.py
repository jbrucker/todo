"""FastAPI implementation of the Todo REST API."""

from fastapi import FastAPI
from routers.todo import router as todo_router

# 'app' refers to FastAPI application instance.
# Routes have been moved to `routers/todo.py` and are included below.
app = FastAPI(
    title="Todo REST API",
    description="""
    A simple Todo REST API implemented with FastAPI.
    Be more effective by *prioritizing* your tasks.
    """,
    version="2026.2.9"
    )

app.include_router(todo_router)
