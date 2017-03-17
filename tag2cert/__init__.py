__version__ = '0.0.1'

import os
import logging
import time
from datetime import datetime

def set_stream_logger(name="tag2cert", level=logging.INFO,
                      format_string=None):
    """
    """

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    time_format = "%Y-%m-%dT%H:%M:%S"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(level)
    streamFormatter = logging.Formatter(format_string, time_format)
    streamHandler.setFormatter(streamFormatter)
    logger.addHandler(streamHandler)


def set_file_logger(case_number, name="tag2cert", level=logging.INFO,
                    base_dir="/tmp", desc="tag2cert Action"):
    """
    """

    log_file = "{base_dir}/tag2cert.log".format(
                   base_dir=base_dir
               )

    logger = logging.getLogger(name)
    logger.setLevel(level)
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setLevel(level)
    fileFormatter = logging.Formatter(
        "\t{'timestamp': %(unixtime)s, 'message': '%(message)s', " +
        "desc: '{desc}', 'datetime': '%(isotime)s'}},".format(desc=desc)
    )
    fileHandler.setFormatter(fileFormatter)
    logger.addHandler(fileHandler)





class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger('tag2cert').addHandler(NullHandler())
