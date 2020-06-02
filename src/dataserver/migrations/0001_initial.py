# Generated by Django 3.0.6 on 2020-06-02 17:03

import os

from django.contrib.auth import get_user_model
from django.db import migrations


def create_default_superuser(apps, schema_editor):
    env = os.environ
    if 'DJANGO_ADMIN_USER' in env \
            and 'DJANGO_ADMIN_EMAIL' in env \
            and 'DJANGO_ADMIN_PASSWORD' in env:
        user = get_user_model().objects.create_superuser(
            env['DJANGO_ADMIN_USER'],
            env['DJANGO_ADMIN_EMAIL'],
            env['DJANGO_ADMIN_PASSWORD'])


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_default_superuser),
    ]
