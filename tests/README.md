## Web-based tests of Todo API

These tests invoked HTTP endpoints in your running Todo application.

They test the "live" service and **may make changes to the Todo
database**. Hence, you may want to save your database file before
testing and restore it after testing.

### Required Packages

`requests` and `pytest`.

### Prerequisites

1.  Your Nginx proxy server and todo service should be running.
2.  Todo server should use **only one worker thread** (one request handler) when using the dumb, file-based database.
    This is because pytest runs quickly and if using multiple "worker" threads to handle requests, they may get inconsistent views of the database, resulting in test failures.


The tests will expect that and test for:

- Service is listening at `http://localhost` (port 80). See `BASE_URL` in `tests/conftext.py`.
- Nginx returns a web page for `http://localhost/` or `http://localhost/index.html` **and** the web page contains an `<html>` tag (proper start of HTML5 pages).
- API docs are at `/api/openapi.json` and `/api/docs`.  See the `ROOT_PATH` variable in `tests/conftest.py`.
- The Todo service urls are prefixed with `/api`, such as `GET /api/todos/{id}`.
- The `POST /api/todos` endpoint will save a new todo to persistence and then return the **`Location`** header containing the relative URL of the new todo 
- The `DELETE` endpoint returns 200 or 201 when its deletes a Todo, 404 if the todo is not found.


### Running the Tests

1.  Make sure that your containers only create a single worker thread. Both the todo Dockerfile and Nginx config make contain code for multiple worker threads.  Select only 1 worker.
2.  Start the containerized application.
3.  Run the bash script `run-tests.sh`.  Alternatively, you can run pytest at the command line:
    ```bash
    pytest -v test_routing.py test_todo_service.py
    ```

