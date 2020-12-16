#!/bin/bash

/wisebox/wait-for db:5432
/wisebox/manage.py collectstatic --noinput
/wisebox/manage.py migrate
/wisebox/manage.py createcachetable
unset DJANGO_ADMIN_USER DJANGO_ADMIN_EMAIL DJANGO_ADMIN_PASSWORD
gunicorn -b 0.0.0.0:80 -w 4 --timeout 600 $@ wisebox.wsgi
