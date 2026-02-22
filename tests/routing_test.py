"""Tests of nginx request handling."""

from config import ROOT_PATH


def test_get_index(client):
    """/index.html should return the index page."""
    response = client.get("/index.html")
    content = response.text
    assert response.status_code == 200
    assert "<html>" in content


def test_slash_returns_index(client):
    """The / route should return index.html."""
    response = client.get("/")
    assert response.status_code == 200
    content = response.text
    assert "<html>" in content


def test_api_docs(client):
    """The {ROOT_PATH}/docs route should return the API docs."""
    response = client.get(f"{ROOT_PATH}/docs")
    assert response.status_code == 200
    content = response.text
    assert "Swagger UI" in content


def test_api_json(client):
    """The {ROOT_PATH}/openapi.json route should return the OpenAPI JSON schema."""
    response = client.get(f"{ROOT_PATH}/openapi.json")
    assert response.status_code == 200
    content: str = response.text
    assert content.startswith('{"openapi":')
    # content should be valid JSON dict with an "openapi" key
    import json
    data = json.loads(content)
    assert "openapi" in data
