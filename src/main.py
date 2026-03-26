"""FastAPI implementation of the Todo REST API."""

import os
from fastapi import FastAPI
from routers.todo import router as todo_router
from routers.health import router as health_check
from routers.headers import router as headers_router
import logging_config


# Prefix for API endpoint paths and OpenAPI docs.
API_ROOT = os.getenv("ROOT_PATH", "")

logging_config.configure_logging()

# 'app' refers to FastAPI application instance.
# Routes have been moved to `routers/todo.py` and are included below.
app = FastAPI(
    title="Todo REST API",
    description="""
    A simple Todo REST API implemented with FastAPI.
    """,
    version="2026.2.22",
    root_path=API_ROOT
    )
# These FastAPI attributes set paths for API documentation independent of the root_path.
#   openapi_url=API_PREFIX+"/openapi.json",
#   docs_url=API_PREFIX+"/docs",
#   redoc_url=API_PREFIX+"/redoc",
#   swagger_ui_oauth2_redirect_url=API_PREFIX+"/docs/oauth2-redirect"

app.include_router(todo_router)
app.include_router(health_check)
app.include_router(headers_router)
