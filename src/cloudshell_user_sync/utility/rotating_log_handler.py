import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from cloudshell_user_sync.utility import path_helper

LOGGER_NAME = "cloudshell-user-sync"
LOG_FORMAT = "%(levelname)s - %(asctime)s: %(message)s"
LOG_DATE_FORMAT = "%m/%d/%Y%I:%M:%S %p"


def get_rotating_logger(log_level: str = logging.INFO):
    """get logger, set new one of it doesn't exist"""
    if LOGGER_NAME in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(LOGGER_NAME)
    else:
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(log_level)

        # build intermediate path
        log_file_path = path_helper.get_system_log_path()
        output_file = Path(log_file_path)
        output_file.parent.mkdir(exist_ok=True, parents=True)

        # set handler and formatter
        rotating_handler = RotatingFileHandler(filename=log_file_path, mode="w", maxBytes=512000, backupCount=4)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)
    return logger


if __name__ == "__main__":
    my_logger = get_rotating_logger()
    my_logger.info("hello test")
