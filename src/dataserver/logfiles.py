import datetime
import json
import struct

import pytz
from django.core.exceptions import ObjectDoesNotExist

from . import models

__ENCODING = 'utf_8'


def decode_and_save(data: bytes, org: models.Organisation):
    i = 0

    mac_bytes = struct.unpack_from('<BBBBBB', data, i)
    mac = ':'.join([f'{x:02x}' for x in mac_bytes])
    i += 6
    try:
        device = models.Device.objects.get(
            mac__exact=mac,
            organisation__id=org.id)
    except ObjectDoesNotExist:
        device = models.Device()
        device.mac = mac
        device.organisation = org
        device.save()

    channel = struct.unpack_from('<B', data, i)[0]
    i += 1

    interval = struct.unpack_from('<I', data, i)[0]
    i += 4

    tz_len = struct.unpack_from('<B', data, i)[0]
    i += 1
    tz_name = data[i:i+tz_len].decode(__ENCODING)
    i += tz_len
    try:
        timezone = models.Timezone.objects.get(name__exact=tz_name)
    except ObjectDoesNotExist:
        timezone = models.Timezone(name=tz_name)
        timezone.save()

    metadata_len = struct.unpack_from('<I', data, i)[0]
    i += 4
    metadata_dict = json.loads(data[i:i+metadata_len].decode(__ENCODING))
    i += metadata_len
    metadata = []
    for k, v in metadata_dict.items():
        mval = models.BucketMetadata(name=k, value=str(v))
        mval.save()
        metadata.append(mval)

    while i < len(data):
        bucket = models.Bucket()
        bucket.device = device
        bucket.channel = channel
        bucket.timezone = timezone
        bucket.interval = interval

        (a, b) = struct.unpack_from('<iH', data, i)
        bucket.start_time = datetime.datetime.fromtimestamp(a, tz=pytz.UTC)
        bucket.count = b
        bucket.save()
        for md in metadata:
            bucket.metadata.add(md)
        i += 6
        j = i + b
        while i < j:
            (rssi, ) = struct.unpack_from('<b', data, i)
            bucket_rssi = models.BucketRssi(bucket=bucket, rssi=rssi)
            bucket_rssi.save()
            i += 1
