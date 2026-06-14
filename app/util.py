# -*- coding: utf-8 -*-
from enum import Enum, auto

"""
Util module to concetrate all reusable code.

This module support all other classes/modules with usefull source code that doesn't belong to any other entity.
"""

from datetime import datetime
import logging

from termcolor import colored


class DebugBot(Enum):
    NORMAL = auto()
    DRY_RUN = auto()
    DEBUG = auto()


class Util:
    """Helper class used to provide configuration, defaults and so on."""
    LOG_FORMAT_FULL = colored('[%(asctime)s][%(process)d:%(processName)s]', 'green', attrs=['bold', 'dark']) + colored(
        '[%(filename)s#%(funcName)s:%(lineno)d]', 'white', attrs=['bold', 'dark']) + colored(
        '[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s '
    LOG_FORMAT_INFO = colored('[%(asctime)s]', 'green', attrs=['bold', 'dark']) + colored(
        '[%(filename)s:%(lineno)d]', 'white', attrs=['bold', 'dark']) + colored(
        '[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'
    LOG_FORMAT_SIMPLE = colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'
    DEFAULT_LOGGER_NAME = 'geconbot'
    DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
    # TODO use default lib to convert month into number
    MONTHS_DICT = {
        'jan': '01',
        'fev': '02',
        'mar': '03',
        'abr': '04',
        'mai': '05',
        'jun': '06',
        'jul': '07',
        'ago': '08',
        'set': '09',
        'out': '10',
        'nov': '11',
        'dez': '12'
    }

    @staticmethod
    def info(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'cyan')

    @staticmethod
    def warning(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'yellow', attrs=['bold'])

    @staticmethod
    def error(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'red', attrs=['bold', 'underline'])

    @staticmethod
    def debug(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'grey', attrs=['reverse', 'bold', 'underline'])

    @staticmethod
    def init_logger(log_type='normal', use_file_handler=True):
        if log_type == 'quiet':
            level = logging.WARN
            logformat = Util.LOG_FORMAT_SIMPLE
        elif log_type == 'verbose':
            level = logging.DEBUG
            logformat = Util.LOG_FORMAT_FULL
        else:                   # elif log_type == 'normal':
            level = logging.INFO
            logformat = Util.LOG_FORMAT_INFO

        bot_logger = logging.getLogger(Util.DEFAULT_LOGGER_NAME)
        bot_logger.setLevel(level)

        c_handler = logging.StreamHandler()
        c_handler.setFormatter(logging.Formatter(logformat))
        c_handler.setLevel(level)
        bot_logger.addHandler(c_handler)

        if use_file_handler:
            f_handler = logging.FileHandler(f'tmp/logs/bot_{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.log')
            f_handler.setFormatter(logging.Formatter(Util.LOG_FORMAT_FULL))
            f_handler.setLevel(logging.DEBUG)
            bot_logger.addHandler(f_handler)

        return bot_logger

    @staticmethod
    def logger_factory():
        return logging.getLogger(Util.DEFAULT_LOGGER_NAME)

    @staticmethod
    def parse_period(period: str) -> str:
        """Set period in default format: YYYY-mm-01. Is expected that period is in format DD/[mm | mmm]/YYYY"""

        return f'{period[-4:]}-{Util.MONTHS_DICT[period[:3].lower()] if len(period) == 8 else period[:2]}-01'
