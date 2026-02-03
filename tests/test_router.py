"""Tests for the todo router endpoints."""
import pytest
from fastapi.testclient import TestClient

from main import app
from persistence import TodoDao
from models import TodoCreate


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a test client with a temporary todo data file."""
    # Create a temporary file for the test
    test_file = tmp_path / "test_todos.json"
    
    # Patch the dao to use the test file
    from routers import todo
    test_dao = TodoDao(str(test_file))
    monkeypatch.setattr(todo, "dao", test_dao)
    
    return TestClient(app)


def test_delete_existing_todo(client):
    """Test deleting an existing todo returns 204."""
    # Create a todo first
    response = client.post("/todos/", json={"text": "Test Todo", "done": False})
    assert response.status_code == 201
    todo_id = response.json()["id"]
    
    # Delete the todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    assert response.text == ""
    
    # Verify the todo is deleted by trying to get it
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404


def test_delete_nonexistent_todo(client):
    """Test deleting a non-existent todo returns 404."""
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"
