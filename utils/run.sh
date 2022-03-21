#!/bin/sh

# python manage.py makemigrations

# python manage.py migrate

#python manage.py collectstatic --no-input
#python manage.py collectstatic --no-post-process --no-input

# gunicorn core.wsgi --bind=0.0.0.0:80 --timeout 120
uvicorn app.main --bind=0.0.0.0:80 --timeout 120

# --timeout 1800 --graceful-timeout 1800
# --workers=2
