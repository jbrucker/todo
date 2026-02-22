"""Tests of Todo web service endpoint URLs.""" 

import json
import pytest

from conftest import BASE_URL, ROOT_PATH

known_todo_ids: list[str] = []


def test_get_todos(client):
    """GET {ROOT_PATH}/todos should return a JSON list of todos."""
    response = client.get(f"{ROOT_PATH}/todos")
    assert response.status_code == 200
    content = response.text
    # content should be valid JSON list
    import json
    data = json.loads(content)
    assert isinstance(data, list)
    # each item in the list should be a dict with an "id" key
    global known_todo_ids
    for item in data:
        known_todo_ids.append(item.get("id"))


def test_create_todo(client):
    """POST {ROOT_PATH}/todos should create a new todo and return Location header."""
    new_todo = {"text": "Test todo", "done": False}
    response = client.post(f"{ROOT_PATH}/todos", json=new_todo)
    assert response.status_code in [200, 201]
    location = response.headers.get("Location")
    assert location is not None
    # Location should be a relative URL and inside the API root path
    assert location.startswith(f"{ROOT_PATH}/todos")
    todo_id = location.rsplit("/", 1)[-1]
    
    # Get the todo
    response2 = client.get(f"{BASE_URL}{location}")
    assert response2.status_code == 200
    # todo should be in JSON format
    todo = json.loads(response2.text)
    assert isinstance(todo, dict)
    assert str(todo.get("id")) == todo_id
    assert todo.get("text") == new_todo["text"]

    global known_todo_ids
    known_todo_ids.append(todo["id"])


@pytest.mark.skipif(not known_todo_ids, reason="No known todo IDs to test for")
def test_get_todo_by_id(client):
    """GET {ROOT_PATH}/todos/{id} should return a JSON object for todo with known id."""
    todo_id = known_todo_ids[0]
    response = client.get(f"{ROOT_PATH}/todos/{todo_id}")
    assert response.status_code == 200
    content = response.text
    # content should be valid JSON dict with an "id" key equal to 1
    import json
    data = json.loads(content)
    assert isinstance(data, dict)
    assert data.get("id") == todo_id


def test_get_nonexistent_todo(client):
    """GET {ROOT_PATH}/todos/9999 should return 404 for non-existent todo."""
    todo_id = 9999
    while str(todo_id) in known_todo_ids:
        todo_id += 1
    response = client.get(f"{ROOT_PATH}/todos/{todo_id}")
    assert response.status_code == 404


def test_delete_todo(client):
    """DELETE {ROOT_PATH}/todos/{id} should delete the todo and return 200 or 204."""
    # First create a new todo to delete
    new_todo = {"text": "Todo to delete", "done": False}
    response = client.get(f"{ROOT_PATH}/todos", json=new_todo)
    assert response.status_code in [200, 201]
    location = response.headers.get("Location")
    assert location is not None
    # todo_id = location.rsplit("/", 1)[-1]

    # Now delete the todo
    response2 = client.delete(f"{BASE_URL}{location}")
    assert response2.status_code in [200, 204]

    # Verify that the todo is deleted
    response3 = client.get(f"{BASE_URL}{location}")
    assert response3.status_code == 404
    # If Todo service is working correctly, the todo added by
    # this test was not added to known_todo_ids.