#!/usr/bin/env bash
#
# Test the containerized Todo application.
# It runs tests in the project's /tests directory by
# sending http requests to expected endpoints.
#
# Set
# BASE_URL = where service is listening, e.g. "http://localhost"
#
# See:
# tests/testconf.py - global test config, including client fixture
# requirements.txt  - includes `pytest` and `requests` for testing
set -euo pipefail

echo "Running tests..."

# Where the todo application is running.
export BASE_URL="http://localhost"

# Search for pytest in a) virtualenv 'bin', b) on PATH, c) as a Python module
if [ -x "env/bin/pytest" ]; then
  env/bin/pytest -v tests/routing_test.py "$@"
elif command -v pytest >/dev/null 2>&1; then
  pytest -v tests "$@"
else
  python -m pytest -v tests "$@"
fi
