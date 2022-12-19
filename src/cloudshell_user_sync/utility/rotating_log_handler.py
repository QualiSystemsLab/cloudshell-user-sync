import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import platform

LOG_FOLDER = "CloudshellUserSync"
LOG_FILE_NAME = "UserSync.log"


def get_windows_log_path():
    return os.path.join(os.getenv("PROGRAMDATA"), LOG_FOLDER, LOG_FILE_NAME)


def get_linux_log_path():
    return os.path.join("/var/log", LOG_FOLDER, LOG_FILE_NAME)


def get_system_log_path():
    curr_platform = platform.system().lower()
    if curr_platform == "windows":
        return get_windows_log_path()

    if curr_platform == "linux":
        return get_linux_log_path()

    raise ValueError(f"Unknown platform: {curr_platform}")


def get_rotating_logger():
    log_file_path = get_system_log_path()
    output_file = Path(log_file_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    rotating_handler = RotatingFileHandler(filename=log_file_path,
                                           mode='w',
                                           maxBytes=512000,
                                           backupCount=4)
    handlers = [rotating_handler]
    logging.basicConfig(handlers=handlers,
                        level=logging.INFO,
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y%I:%M:%S %p')
    return logging.getLogger('cloudshell-user-sync')


if __name__ == "__main__":
    logger = get_rotating_logger()
    logger.info("hello test")
