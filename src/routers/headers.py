"""Router that returns request headers and context info as HTML."""

from http import HTTPStatus as status
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["headers"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("/headers/", response_class=HTMLResponse, status_code=status.OK)
async def get_headers(request: Request) -> HTMLResponse:
    """Return an HTML page showing request headers and request context values."""
    headers = [
        {"name": name, "value": value}
        for name, value in request.headers.items()
    ]
    context_items = [
        {"key": key, "value": repr(value)}
        for key, value in request.scope.items()
    ]
    return templates.TemplateResponse(
        request=request,
        name="headers.html",
        context={"headers": headers, "request_context": context_items},
    )
