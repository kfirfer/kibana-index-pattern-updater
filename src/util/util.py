# -*- coding: utf-8 -*-
import hashlib
import random
import string
from datetime import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def random_string(size=64):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def iso_format(datetime_):
    try:
        utc = datetime_ + datetime_.utcoffset()
    except TypeError:
        utc = datetime_
    iso_string = datetime.strftime(utc, '%Y-%m-%dT%H:%M:%S.{:03}Z')
    return iso_string.format(int(round(utc.microsecond / 1000.0)))


def iso_format_string_to_datetime(date_string):
    datetime_ = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return datetime_


def get_sha1(data):
    sha1 = hashlib.sha1(data.encode("utf-8"))
    sha1 = sha1.hexdigest()
    return sha1
