#!/bin/bash
# Run the Todo service

ROOT_PATH=/api
 
# Activate virtual environment
activate_venv() {
    DIR=$( dirname "${BASH_SOURCE[0]}" )
    ENVDIR="$DIR/env"
    echo "Activate virtual env in $ENVDIR"
    . $ENVDIR/bin/activate
}

if [[ ! -v VIRTUAL_ENV ]]; then
    activate_venv
fi

cd src
uvicorn main:app --port 8000 --reload --root-path $ROOT_PATH
