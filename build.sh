#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt

echo "Running Django migrations..."
cd backend
python manage.py makemigrations --noinput
python manage.py migrate --noinput


echo "Build completed successfully!"
