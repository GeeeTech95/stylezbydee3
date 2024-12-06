#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

export DEBUG=False

# Convert static asset files
python manage.py collectstatic --no-input



#Apply any outstanding database migrations
python manage.py migrate 
python manage.py loaddata admin-data.json
python manage.py loaddata custom_permissions.json

export DJANGO_SUPERUSER_EMAIL=admin2@stylezbydee.com
export DJANGO_SUPERUSER_PASSWORD=VlopGoikB8 

#python manage.py createsuperuser --no-input



