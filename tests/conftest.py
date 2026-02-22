import os
import requests
import pytest

"""Pytest fixtures for running tests against a live web service.

This provides a `client` fixture used by tests in `tests/` that issues HTTP
requests to the running application. The base URL is taken from the
`BASE_URL` environment variable or defaults to `http://localhost`.
"""

BASE_URL = os.environ.get("BASE_URL", "http://localhost")

# The root path for the API, used in tests to prefix URLs for API endpoints.
# Use an empty string for no prefix.
ROOT_PATH = "/api"


class _SimpleClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, **kwargs):
        p = path.lstrip("/")
        url = f"{self.base_url}/{p}" if p else f"{self.base_url}/"
        return requests.get(url, **kwargs)


@pytest.fixture(scope="session")
def client():
    """Return a minimal client with a `.get()` method returning requests.Response.

    Tests call `client.get(path)` with path values like `/index.html` or
    `/api/docs`. The fixture concatenates the base URL and the path and
    performs a blocking HTTP request using `requests`.
    """
    yield _SimpleClient(BASE_URL)
