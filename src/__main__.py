# -*- coding: utf-8 -*-
import src
from src.loggings.custom_json_format_log import CustomJSONLog
from src.loggings.logger import logger

log = logger(__name__)
src.loggings.init(custom_formatter=CustomJSONLog)

if __name__ == '__main__':
    from src.job.updater import job

    try:
        job()
    except Exception:
        log.error("", exc_info=True)
    log.info("job finished")
