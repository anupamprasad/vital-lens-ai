#!/usr/bin/env bash

# Railway/Front-end build helper script
# This script is invoked by Railpack when it cannot automatically
# determine how to run the application. It switches to the backend
# directory, installs dependencies, runs migrations, and starts Uvicorn.

set -e

cd phase3_application/backend

# install requirements (use production file if available)
if [ -f requirements-prod.txt ]; then
  pip install -r requirements-prod.txt
else
  pip install -r requirements.txt
fi

# run database migrations (assumes DATABASE_URL is set in env)
alembic upgrade head

# start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
