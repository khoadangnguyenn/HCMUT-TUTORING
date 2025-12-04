#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt

echo "Running Django migrations..."
cd backend
python manage.py migrate --noinput
python manage.py seed_users

echo "Build completed successfully!"
