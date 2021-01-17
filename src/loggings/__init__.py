# -*- coding: utf-8 -*-
import inspect
import logging

from src.loggings import util


def init(custom_formatter):
    if inspect.isclass(custom_formatter) and issubclass(custom_formatter, logging.Formatter):
        formatter = custom_formatter
        logging._defaultFormatter = formatter()
    else:
        logging._defaultFormatter = custom_formatter

    existing_loggers = list(map(logging.getLogger, logging.Logger.manager.loggerDict))

    if inspect.isclass(custom_formatter) and issubclass(custom_formatter, logging.Formatter):
        formatter = custom_formatter
        update_formatter_for_loggers(existing_loggers, formatter)


def update_formatter_for_loggers(loggers_iter, formatter):
    for logger in loggers_iter:
        if not isinstance(logger, logging.Logger):
            raise RuntimeError("%s is not a logging.Logger instance", logger)
        for handler in logger.handlers:
            if not isinstance(handler.formatter, formatter) and logger.name != 'sqlalchemy.engine.base.Engine':
                handler.formatter = formatter()
