#!/bin/bash

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn nstw_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3