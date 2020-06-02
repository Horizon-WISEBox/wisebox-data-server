#!/bin/bash

/wiseparks/wait-for db:5432
/wiseparks/manage.py collectstatic --noinput
/wiseparks/manage.py migrate
/wiseparks/manage.py createcachetable
unset DJANGO_ADMIN_USER DJANGO_ADMIN_EMAIL DJANGO_ADMIN_PASSWORD
gunicorn -b 0.0.0.0:80 -w 4 --timeout 600 \
    -k uvicorn.workers.UvicornH11Worker $@ wiseparks.asgi
