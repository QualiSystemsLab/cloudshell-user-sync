import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_rotating_logger(program_data_folder="CloudshellUserSync", log_file_name="UserSync.log"):
    log_file_path = os.path.join(os.getenv("PROGRAMDATA"), program_data_folder, log_file_name)
    output_file = Path(log_file_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)

    handlers = [RotatingFileHandler(filename=log_file_path,
                                    mode='w',
                                    maxBytes=512000,
                                    backupCount=4)
                ]
    logging.basicConfig(handlers=handlers,
                        level=logging.INFO,
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y%I:%M:%S %p')

    return logging.getLogger('cloudshell-user-sync')


if __name__ == "__main__":
    logger = get_rotating_logger()
    logger.info("hello test")
