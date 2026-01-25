#!/bin/bash
set -e

echo "Starting application..."

# Run migrations from the app directory
cd app
echo "Running database migrations..."
python manage.py migrate --noinput
echo "Migrations completed successfully!"

# Start gunicorn from the root directory (so it can find app.wsgi)
cd ..
echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT app.wsgi:application

