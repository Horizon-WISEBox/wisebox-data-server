from django.contrib.auth import get_user_model
from django.db import models


class Organisation(models.Model):

    name = models.CharField(
        blank=True,
        default='',
        max_length=256)

    users = models.ManyToManyField(
        get_user_model(),
        related_name='organisations')


class ApiKey(models.Model):

    key = models.CharField(
        max_length=32,
        unique=True)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='api_keys')


class Device(models.Model):

    mac = models.CharField(max_length=17)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='devices')


class Timezone(models.Model):
    name = models.CharField(max_length=50)


class Bucket(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='buckets')
    channel = models.PositiveSmallIntegerField()
    start_time = models.DateTimeField()
    timezone = models.ForeignKey(
        Timezone,
        on_delete=models.CASCADE,
        related_name='+')
    interval = models.PositiveIntegerField()
    count = models.PositiveSmallIntegerField()


class BucketRssi(models.Model):

    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.CASCADE,
        related_name='rssis')

    rssi = models.SmallIntegerField()


class BucketMetadata(models.Model):

    buckets = models.ManyToManyField(
        Bucket,
        related_name='metadata')

    name = models.TextField()

    value = models.TextField()
