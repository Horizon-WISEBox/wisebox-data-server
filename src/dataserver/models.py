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

    def __str__(self):
        return f'Organisation(id={self.id}, name={self.name})'

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class ApiKey(models.Model):

    key = models.CharField(
        max_length=32,
        unique=True)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='api_keys')

    def __str__(self):
        return f'ApiKey(id={self.id})'

    class Meta:
        indexes = [
            models.Index(fields=['key']),
        ]


class Device(models.Model):

    mac = models.CharField(max_length=17)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='devices')

    description = models.TextField(
        blank=True,
        default='')

    def __str__(self):
        return f'Device(id={self.id}, mac={self.mac})'

    class Meta:
        indexes = [
            models.Index(fields=['mac']),
        ]
        unique_together = [['mac', 'organisation']]


class Timezone(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'Timezone(id={self.id}, name={self.name})'

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class Bucket(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='buckets')
    start_time = models.DateTimeField()
    timezone = models.ForeignKey(
        Timezone,
        on_delete=models.CASCADE,
        related_name='+')
    interval = models.PositiveIntegerField()
    frequency = models.PositiveSmallIntegerField()
    count = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Bucket(id={self.id}'


class BucketRssi(models.Model):

    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.CASCADE,
        related_name='rssis')

    rssi = models.SmallIntegerField()

    def __str__(self):
        return f'BucketRssi(id={self.id}'


class BucketMetadata(models.Model):

    buckets = models.ManyToManyField(
        Bucket,
        related_name='metadata')

    name = models.TextField()

    value = models.TextField()

    def __str__(self):
        return (
            f'BucketMetadata(id={self.id}, name={self.name}, value={self.value}'
        )


class Location(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f'Location(id={self.id}, name={self.name})'


class DeviceSession(models.Model):

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='sessions')

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='locations')

    start_date = models.DateTimeField(null=True, default=None, blank=True)

    end_date = models.DateTimeField(null=True, default=None, blank=True)

    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return (f'DeviceSession(id={self.id}, device={self.device.mac}'
                + f', location={self.location.name})')
