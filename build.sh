#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Running Django migrations..."
cd backend
echo "Collecting static files..."
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py seed_users

echo "Build completed successfully!"
