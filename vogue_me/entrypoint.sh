#!/bin/bash

#echo "Migrating DB Models' changes."
#python manage.py makemigrations
#python manage.py migrate

echo "Collecting and Uploading static files into S3 bucket."
python manage.py collectstatic --noinput

echo "Run gunicorn."
exec gunicorn -c gunicorn.conf.py --timeout 600
