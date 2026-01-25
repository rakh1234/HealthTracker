#!/bin/bash
set -e

echo "Starting application..."

# Set PYTHONPATH to the project root so Python can find the 'app' module
export PYTHONPATH=/opt/render/project/src

# Run migrations from the root directory using the full path to manage.py
echo "Running database migrations..."
python app/manage.py migrate --noinput
echo "Migrations completed successfully!"

# Collect static files (optional, won't fail if it doesn't work)
echo "Collecting static files..."
python app/manage.py collectstatic --noinput || echo "Static files collection skipped"

# Start gunicorn from the root directory (so it can find app.wsgi)
echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT app.wsgi:application

