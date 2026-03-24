#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies using Pipenv
# We use --system so the packages are installed in the container's global python
# which is the standard way Render handles Python environments.
pip install pipenv
pipenv install --system --deploy

# FORCE INSTALL GUNICORN JUST IN CASE
pip install gunicorn whitenoise dj-database-url

# 2. Collect Static Files
# This gathers all CSS/JS into the 'staticfiles' folder for WhiteNoise to serve.
python manage.py collectstatic --no-input

# 3. Apply Database Migrations
# This ensures your Render PostgreSQL database matches your local models.
python manage.py migrate