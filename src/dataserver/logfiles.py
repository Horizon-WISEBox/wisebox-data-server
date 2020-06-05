import datetime
import json
import struct

import pytz
from django.core.exceptions import ObjectDoesNotExist

from . import models

__ENCODING = 'utf_8'

__frequencies_by_channel = {
    '1': 2412,
    '2': 2417,
    '3': 2422,
    '4': 2427,
    '5': 2432,
    '6': 2437,
    '7': 2442,
    '8': 2447,
    '9': 2452,
    '10': 2457,
    '11': 2462,
    '12': 2467,
    '13': 2472,
    '14': 2484,
    '32': 5160,
    '34': 5170,
    '36': 5180,
    '38': 5190,
    '40': 5200,
    '42': 5210,
    '44': 5220,
    '46': 5230,
    '48': 5240,
    '50': 5250,
    '52': 5260,
    '54': 5270,
    '56': 5280,
    '58': 5290,
    '60': 5300,
    '62': 5310,
    '64': 5320,
    '68': 5340,
    '96': 5480,
    '100': 5500,
    '102': 5510,
    '104': 5520,
    '106': 5530,
    '108': 5540,
    '110': 5550,
    '112': 5560,
    '114': 5570,
    '116': 5580,
    '118': 5590,
    '120': 5600,
    '122': 5610,
    '124': 5620,
    '126': 5630,
    '128': 5640,
    '132': 5660,
    '134': 5670,
    '136': 5680,
    '138': 5690,
    '140': 5700,
    '142': 5710,
    '144': 5720,
    '149': 5745,
    '151': 5755,
    '153': 5765,
    '155': 5775,
    '157': 5785,
    '159': 5795,
    '161': 5805,
    '165': 5825,
    '169': 5845,
    '173': 5865,
    '183': 4915,
    '184': 4920,
    '185': 4925,
    '187': 4935,
    '188': 4940,
    '189': 4945,
    '192': 4960,
    '196': 4980,
}


class UnknownFormatException(Exception):
    def __init__(self, version, message=''):
        self.version = version
        super().__init__(message)


def frequency_lookup(channel: int):
    chan = str(channel)
    if chan in __frequencies_by_channel:
        return __frequencies_by_channel[chan]
    return 0


def decode_and_save(data: bytes, org: models.Organisation):
    (version, ) = struct.unpack_from('<H', data, 0)
    if version == 1:
        _decode_and_save_v1(data[2:], org)
    else:
        raise UnknownFormatException(version)


def _decode_and_save_v1(data: bytes, org: models.Organisation):
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
        bucket.timezone = timezone
        bucket.interval = interval

        (a, b, c) = struct.unpack_from('<iHH', data, i)
        bucket.start_time = datetime.datetime.fromtimestamp(a, tz=pytz.UTC)
        bucket.frequency = b
        bucket.count = c
        bucket.save()
        for md in metadata:
            bucket.metadata.add(md)
        i += 8
        j = i + c
        while i < j:
            (rssi, ) = struct.unpack_from('<b', data, i)
            bucket_rssi = models.BucketRssi(bucket=bucket, rssi=rssi)
            bucket_rssi.save()
            i += 1


def decode_and_save_vnone(data: bytes, org: models.Organisation):
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
    frequency = frequency_lookup(channel)
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
        bucket.timezone = timezone
        bucket.interval = interval
        bucket.frequency = frequency

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
