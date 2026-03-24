#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies
# If you have a requirements.txt, this is the most reliable way on Render.
pip install --upgrade pip
pip install -r requirements.txt

# 2. Collect Static Files
# Gathers CSS/JS for WhiteNoise.
python manage.py collectstatic --no-input

# 3. Apply Database Migrations
# This creates the 'django_site' table that is currently missing.
python manage.py migrate