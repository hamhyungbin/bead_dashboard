#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
# Run database migrations if you have them and want auto-migration
# flask db upgrade # Ensure Flask-Migrate is set up