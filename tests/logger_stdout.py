import logging
import sys

LOG_FORMAT = '%(asctime)s - %(filename)s:%(lineno)d - [%(levelname)s] %(message)s'


def get_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
