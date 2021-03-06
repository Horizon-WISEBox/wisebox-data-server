# Generated by Django 3.0.6 on 2020-08-20 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0003_device_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='dataserver.Device')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='dataserver.Location')),
            ],
        ),
    ]
