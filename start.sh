#!/bin/bash
set -e

echo "Starting application..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo "Current directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"

if [ "$NO_DB" != "1" ]; then
    echo "Running database migrations..."
    python app/manage.py migrate --noinput
    echo "Migrations completed successfully!"
else
    echo "NO_DB=1 detected, skipping migrations."
fi

echo "Collecting static files..."
python app/manage.py collectstatic --noinput || echo "Static files collection skipped"

echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT app.wsgi:application