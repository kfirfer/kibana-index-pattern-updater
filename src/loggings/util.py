# -*- coding: utf-8 -*-
import random
import string


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def random_string(size=64):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
