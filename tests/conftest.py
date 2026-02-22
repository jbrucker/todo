"""Pytest fixtures for running tests against a live web service.

This provides a `client` fixture used by tests in `tests/` that issues HTTP
requests to the running application. The base URL is taken from the
`BASE_URL` environment variable or defaults to `http://localhost`.
"""
import os
import requests
import pytest

BASE_URL = os.environ.get("BASE_URL", "http://localhost")


class _SimpleClient:
    """Wrapper around `requests` to provide a simple interface for tests."""
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, **kwargs):
        p = path.lstrip("/")
        url = f"{self.base_url}/{p}" if p else f"{self.base_url}/"
        return requests.get(url, **kwargs)

    def post(self, path: str, **kwargs):
        p = path.lstrip("/")
        url = f"{self.base_url}/{p}" if p else f"{self.base_url}/"
        return requests.post(url, **kwargs)

    def delete(self, path: str, **kwargs):
        p = path.lstrip("/")
        url = f"{self.base_url}/{p}" if p else f"{self.base_url}/"
        return requests.delete(url, **kwargs)


@pytest.fixture(scope="session")
def client():
    """Return a minimal client as a test fixture.

    Tests call `client.get(path)` with path values like `/index.html` or
    `/api/docs`. The fixture concatenates the base URL and the path and
    performs a blocking HTTP request using `requests`.
    """
    yield _SimpleClient(BASE_URL)
