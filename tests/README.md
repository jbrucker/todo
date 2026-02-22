## Web-based tests

These tests invoked HTTP endpoints in your running application.

They test the "live" service and may cause changes to the Todo
database. Hence, you may want to save your database file before
testing and restore it after testing.

### Required Packages

`requests` and `pytest`.

### Prerequisites

Your Nginx proxy server and todo service should be running.

The tests will expect that and test for:

- Service is listening at `http://localhost`  See `BASE_URL` in `tests/conftext.py`.
- Nginx returns a web page for `http://localhost/` or `http://localhost/index.html` **and** the web page contains an `<html>` tag (proper start of HTML5 pages).
- API docs are at `/api/openapi.json` and `/api/docs`.  See the `ROOT_PATH` variable in `tests/conftest.py`.
- The Todo service urls are prefixed with `/api`, such as `GET /api/todos/{id}`.
- The `POST /api/todos` endpoint will save a new todo to persistence and then return the `Location` header containing the relative URL of the new todo 
- The `DELETE` endpoint returns 200 or 204 when its deletes a Todo, 404 if the todo is not found.


### Running the Tests

1. Start the containerized application.
2. Run the bash script `run-tests.sh`