"""Application health check, invoked by the container to verify app is responding."""
from fastapi import APIRouter
from http import HTTPStatus as status

router = APIRouter(tags=['health'])


@router.get("/health", status_code=status.OK)
async def health():
    """Lightweight health endpoint for Docker health checks."""
    return {"status": "ok"}
