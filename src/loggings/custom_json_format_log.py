# -*- coding: utf-8 -*-
import json
import logging
import os
import traceback
from datetime import datetime

from src.loggings.logger import LOG_TO_CONSOLE


JSON_LOG_CONSOLE = False
if "JSON_LOG_CONSOLE" in os.environ and os.environ["JSON_LOG_CONSOLE"] == "1":
    JSON_LOG_CONSOLE = True

SKIP_MESSAGE_IN_JSON_LOG = "skip_message_in_json_log"


def json_serializer(log):
    return json.dumps(log, ensure_ascii=False)


def _sanitize_log_msg(record):
    return record.getMessage().replace('\n', '_').replace('\r', '_').replace('\t', '_')


def get_json_log_object(record):
    datetime_ = datetime.utcnow()
    formatted_date = '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (
        datetime_.year, datetime_.month, datetime_.day, datetime_.hour, datetime_.minute, datetime_.second,
        int(datetime_.microsecond / 1000))
    json_log_object = {
        "date": formatted_date,
        "logger": record.name,
        "thread": record.threadName,
        "level": record.levelname,
        "module": record.module,
        "file_name": record.filename,
        "function_name": record.funcName,
        "line_number": record.lineno,
        "pid": record.process
    }
    if not hasattr(record, SKIP_MESSAGE_IN_JSON_LOG):
        json_log_object["message"] = _sanitize_log_msg(record)
    if hasattr(record, 'props'):
        json_log_object.update(record.props)
    return json_log_object


class CustomJSONLog(logging.Formatter):
    elastic_search_logger = None
    f = None

    def __init__(self):
        super().__init__()
        self.f = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(msg)s')

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {
            'exc_info': exc_info,
            'filename': record.filename,
        }

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):
        json_log_object = get_json_log_object(record)

        if record.exc_info or record.exc_text:
            json_log_object.update(self.get_exc_fields(record))

        if not LOG_TO_CONSOLE:
            return ""
        if JSON_LOG_CONSOLE:
            return json_serializer(json_log_object)
        else:
            return self.f.format(record)
