# -*- coding: utf-8 -*-
import logging
import os
import sys

from src.loggings.util import random_string

LOG_TO_CONSOLE = True
if "LOG_TO_CONSOLE" in os.environ and os.environ["LOG_TO_CONSOLE"] == "0":
    LOG_TO_CONSOLE = False


def logger(log_name=random_string(10)):
    log = logging.getLogger(log_name)
    level = logging.DEBUG
    if 'LOGGER_LEVEL' in os.environ:
        logger_level = os.environ['LOGGER_LEVEL'].lower()
        if logger_level == "debug":
            level = logging.DEBUG
        elif logger_level == "info":
            level = logging.INFO
        elif logger_level == "warning" or logger_level == "warn":
            level = logging.WARN
        elif logger_level == "error":
            level = logging.ERROR
    log.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    if not LOG_TO_CONSOLE:
        handler.terminator = ""
    log.addHandler(handler)
    return log
