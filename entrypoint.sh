#!/bin/sh
set -e

echo "== MediaPulse backend : démarrage =="

echo "-- Application des migrations --"
python manage.py migrate --noinput

echo "-- Collecte des fichiers statiques --"
python manage.py collectstatic --noinput

echo "-- Lancement de gunicorn --"
exec gunicorn mediapulse_backend.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120
