#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt

echo "Running Django migrations..."
cd backend
python manage.py makemigrations --noinput 2>/dev/null || true
python manage.py migrate --noinput 2>/dev/null || true


echo "Build completed successfully!"
