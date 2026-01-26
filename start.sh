#!/bin/bash
set -e

echo "Starting application..."

# Get the directory where this script is located (project root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# Set PYTHONPATH to the project root so Python can find the 'app' module
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Change to project root directory
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"
echo "Current directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"

# Run migrations using the full path to manage.py
echo "Running database migrations..."
python app/manage.py migrate --noinput
echo "Migrations completed successfully!"

# Collect static files (optional, won't fail if it doesn't work)
echo "Collecting static files..."
python app/manage.py collectstatic --noinput || echo "Static files collection skipped"

# Start gunicorn from the root directory (so it can find app.wsgi)
echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT app.wsgi:application

